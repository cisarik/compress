"""Deterministicky Image-GP-lite search nad 2D pixel kontextom."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .base import OptimizerRequest, OptimizerResult
from ..image_context_laws import (
    ImageLawNode,
    add_law,
    avg_law,
    checker_parity_law,
    clamp_byte_law,
    eq_const_law,
    floordiv_const_law,
    gradient_law,
    mod_const_law,
    parity_byte_law,
    render_image_law,
    sub_law,
    terminal_law,
)
from ..image_datasets import GrayImage, make_gray_image
from ..image_law_branch import encode_image_law_payload, estimate_image_law_cost

_MAX_DEPTH = 4
_PRIMITIVE_SET_ALIASES = {
    "local": "local",
    "ramp": "ramp",
    "structure": "structure",
    "full": "structure",
}
_STRUCTURE_BLOCKS = (1, 2, 4, 8, 16)
_EQ_CONST_VALUES = tuple(range(17))
_MOD_DIV_VALUES = (2, 4, 8, 16)


@dataclass(frozen=True)
class PrimitiveSetSpec:
    """Popis dostupnych terminalov a operatorov pre jeden primitive set."""

    name: str
    terminals: tuple[str, ...]
    allows_structure_primitives: bool


_PRIMITIVE_SPECS = {
    "local": PrimitiveSetSpec(
        name="local",
        terminals=("left", "up", "up_left"),
        allows_structure_primitives=False,
    ),
    "ramp": PrimitiveSetSpec(
        name="ramp",
        terminals=("left", "up", "up_left", "x_ramp", "y_ramp", "diag_ramp"),
        allows_structure_primitives=False,
    ),
    "structure": PrimitiveSetSpec(
        name="structure",
        terminals=("col", "row", "left", "up", "up_left", "x_ramp", "y_ramp", "diag_ramp"),
        allows_structure_primitives=True,
    ),
}


class ImageGPLiteOptimizer:
    """Registry adapter pre maly 2D expression-tree search."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "Image-GP-lite"

    def available(self) -> bool:
        """Image-aware GP-lite je plne implementovany v repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti maly deterministicky search nad 2D image law stromami."""

        width = request.metadata.get("image_width")
        height = request.metadata.get("image_height")
        dataset_name = request.metadata.get("dataset_name", "external")
        primitive_set_name = request.metadata.get("image_gplite_primitive_set", "full")

        if not isinstance(width, int) or width <= 0:
            raise ValueError("Image-GP-lite requires positive metadata['image_width']")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Image-GP-lite requires positive metadata['image_height']")

        image_name = str(dataset_name) if isinstance(dataset_name, str) else "external"
        image = make_gray_image(image_name, width, height, bytes(request.data))
        search = search_best_image_law(
            image,
            seed=request.seed,
            population_size=request.population_size,
            generations=request.generations,
            primitive_set=str(primitive_set_name),
        )
        best_law = search["best_law"]
        best_cost = search["best_cost"]
        payload = encode_image_law_payload(image, best_law)
        return OptimizerResult(
            optimizer_name=self.name(),
            status="ok",
            best_model=render_image_law(best_law),
            raw_bits=best_cost["raw_bits"],
            total_bits=best_cost["total_bits"],
            saving_bits=best_cost["saving_bits"],
            ratio_vs_raw=best_cost["ratio_vs_raw"],
            history=search["history"],
            details={
                "image_law_model": best_law,
                "payload": payload,
                "residual_bits": best_cost["residual_bits"],
                "residual_codec": best_cost["residual_codec"],
                "residual_codec_details": best_cost["residual_codec_details"],
                "min_residual": best_cost["min_residual"],
                "max_residual": best_cost["max_residual"],
                "would_use_fallback": best_cost["total_bits"] >= best_cost["raw_bits"],
                "best_cost": best_cost,
                "search_seed": request.seed,
                "primitive_set": search["requested_primitive_set"],
                "resolved_primitive_set": search["resolved_primitive_set"],
            },
        )


def available_image_gplite_primitive_sets() -> list[str]:
    """Vrati stabilny zoznam akceptovanych primitive set mien."""

    return ["local", "ramp", "structure", "full"]


def search_best_image_law(
    image: GrayImage,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 20,
    max_depth: int = _MAX_DEPTH,
    primitive_set: str = "full",
) -> dict:
    """Spusti malu deterministicku GP-lite search smycku nad image law stromami."""

    resolved_name, spec = _resolve_primitive_set(primitive_set)
    rng = Random(seed)
    resolved_population = max(1, population_size)
    resolved_generations = max(1, generations)

    population = _seed_population(spec, max_depth)
    attempts = 0
    while len(population) < resolved_population and attempts < resolved_population * 20:
        candidate = _random_law(rng, spec, max_depth)
        population[_law_key(candidate)] = candidate
        attempts += 1

    history: list[dict] = []
    best_law: ImageLawNode | None = None
    best_cost: dict | None = None

    for generation_index in range(resolved_generations):
        scored = _score_population(list(population.values()), image)
        best_law = scored[0]["law"]
        best_cost = scored[0]["cost"]
        history.append(
            {
                "generation": generation_index,
                "best_model": render_image_law(best_law),
                "total_bits": best_cost["total_bits"],
                "saving_bits": best_cost["saving_bits"],
                "primitive_set": resolved_name,
            }
        )

        elite_count = max(2, min(len(scored), resolved_population // 8 or 1))
        next_population = {
            _law_key(item["law"]): item["law"]
            for item in scored[:elite_count]
        }

        fill_attempts = 0
        while len(next_population) < resolved_population and fill_attempts < resolved_population * 40:
            parent = _tournament_select(scored, rng)
            if rng.random() < 0.35:
                donor = _tournament_select(scored, rng)
                child = _crossover_laws(parent["law"], donor["law"], rng, spec, max_depth)
            else:
                child = _mutate_law(parent["law"], rng, spec, max_depth)
            next_population[_law_key(child)] = child
            fill_attempts += 1

        extra_attempts = 0
        while len(next_population) < resolved_population and extra_attempts < resolved_population * 20:
            extra = _random_law(rng, spec, max_depth)
            next_population[_law_key(extra)] = extra
            extra_attempts += 1

        population = next_population

    if best_law is None or best_cost is None:
        raise RuntimeError("Image-GP-lite did not produce a best candidate")

    return {
        "best_law": best_law,
        "best_cost": best_cost,
        "history": history,
        "generations": resolved_generations,
        "population_size": resolved_population,
        "seed": seed,
        "requested_primitive_set": primitive_set,
        "resolved_primitive_set": resolved_name,
    }


def _resolve_primitive_set(name: str) -> tuple[str, PrimitiveSetSpec]:
    """Prevedie alias primitive setu na internu specifikaciu."""

    normalized = str(name).strip()
    resolved = _PRIMITIVE_SET_ALIASES.get(normalized)
    if resolved is None:
        raise ValueError(f"Unknown Image-GP-lite primitive set: {name}")
    return resolved, _PRIMITIVE_SPECS[resolved]


def _seed_population(spec: PrimitiveSetSpec, max_depth: int) -> dict[str, ImageLawNode]:
    """Vrati malu sadu rozumnych startovacich stromov pre dany primitive set."""

    laws: list[ImageLawNode] = [
        terminal_law("left"),
        terminal_law("up"),
        terminal_law("up_left"),
        avg_law(terminal_law("left"), terminal_law("up")),
        gradient_law(terminal_law("left"), terminal_law("up"), terminal_law("up_left")),
        clamp_byte_law(gradient_law(terminal_law("left"), terminal_law("up"), terminal_law("up_left"))),
    ]

    if "x_ramp" in spec.terminals:
        laws.extend(
            [
                terminal_law("x_ramp"),
                terminal_law("y_ramp"),
                terminal_law("diag_ramp"),
            ]
        )

    if spec.allows_structure_primitives:
        laws.extend(checker_parity_law(block) for block in _STRUCTURE_BLOCKS)
        laws.extend(
            [
                parity_byte_law(terminal_law("col")),
                parity_byte_law(terminal_law("row")),
                mod_const_law(terminal_law("col"), 2),
                mod_const_law(terminal_law("row"), 2),
                floordiv_const_law(terminal_law("col"), 4),
                floordiv_const_law(terminal_law("row"), 4),
                eq_const_law(mod_const_law(terminal_law("col"), 2), 1),
            ]
        )

    return {_law_key(_prune_law(law, spec, max_depth)): _prune_law(law, spec, max_depth) for law in laws}


def _score_population(population: list[ImageLawNode], image: GrayImage) -> list[dict]:
    """Ohodnoti populaciu podla total_bits a stabilne ju utriedi."""

    scored = []
    for law in population:
        cost = estimate_image_law_cost(image, law)
        scored.append({"law": law, "cost": cost, "law_string": render_image_law(law)})
    scored.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law_string"]))
    return scored


def _tournament_select(scored: list[dict], rng: Random, size: int = 3) -> dict:
    """Vyberie rodica cez maly deterministicky turnaj."""

    sample_size = min(size, len(scored))
    candidates = rng.sample(scored, sample_size)
    candidates.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law_string"]))
    return candidates[0]


def _random_law(rng: Random, spec: PrimitiveSetSpec, max_depth: int) -> ImageLawNode:
    """Vygeneruje nahodny zakon malej hlbky v ramci primitive setu."""

    if max_depth <= 0 or rng.random() < 0.28:
        return _random_terminal(rng, spec)

    choices = ["add", "sub", "avg", "gradient", "clamp_byte"]
    if spec.allows_structure_primitives:
        choices.extend(["mod_const", "floordiv_const", "eq_const", "parity_byte", "checker_parity"])

    choice = rng.choice(choices)
    if choice == "add":
        return add_law(_random_law(rng, spec, max_depth - 1), _random_law(rng, spec, max_depth - 1))
    if choice == "sub":
        return sub_law(_random_law(rng, spec, max_depth - 1), _random_law(rng, spec, max_depth - 1))
    if choice == "avg":
        return avg_law(_random_law(rng, spec, max_depth - 1), _random_law(rng, spec, max_depth - 1))
    if choice == "gradient":
        return gradient_law(
            _random_law(rng, spec, max_depth - 1),
            _random_law(rng, spec, max_depth - 1),
            _random_law(rng, spec, max_depth - 1),
        )
    if choice == "mod_const":
        return mod_const_law(_random_law(rng, spec, max_depth - 1), rng.choice(_MOD_DIV_VALUES))
    if choice == "floordiv_const":
        return floordiv_const_law(_random_law(rng, spec, max_depth - 1), rng.choice(_MOD_DIV_VALUES))
    if choice == "eq_const":
        return eq_const_law(_random_law(rng, spec, max_depth - 1), rng.choice(_EQ_CONST_VALUES))
    if choice == "parity_byte":
        return parity_byte_law(_random_law(rng, spec, max_depth - 1))
    if choice == "checker_parity":
        return checker_parity_law(rng.choice(_STRUCTURE_BLOCKS))
    return clamp_byte_law(_random_law(rng, spec, max_depth - 1))


def _random_terminal(rng: Random, spec: PrimitiveSetSpec) -> ImageLawNode:
    """Vygeneruje terminal alebo explicitnu checker primitive."""

    if spec.allows_structure_primitives and rng.random() < 0.18:
        return checker_parity_law(rng.choice(_STRUCTURE_BLOCKS))
    return terminal_law(rng.choice(spec.terminals))


def _mutate_law(law: ImageLawNode, rng: Random, spec: PrimitiveSetSpec, max_depth: int) -> ImageLawNode:
    """Aplikuje malu deterministicku mutaciu podstromu."""

    paths = _subtree_paths(law)
    target_path = rng.choice(paths)
    target = _get_subtree(law, target_path)
    mode = rng.choice(("replace", "wrap", "tweak"))

    if mode == "replace":
        replacement = _random_law(rng, spec, 2)
    elif mode == "wrap":
        replacement = _wrap_subtree(target, rng, spec)
    else:
        replacement = _tweak_subtree(target, rng, spec)

    return _prune_law(_replace_subtree(law, target_path, replacement), spec, max_depth)


def _crossover_laws(
    left: ImageLawNode,
    right: ImageLawNode,
    rng: Random,
    spec: PrimitiveSetSpec,
    max_depth: int,
) -> ImageLawNode:
    """Zlozi dieta nahradenim podstromu darcovskym podstromom."""

    left_path = rng.choice(_subtree_paths(left))
    right_subtree = _get_subtree(right, rng.choice(_subtree_paths(right)))
    return _prune_law(_replace_subtree(left, left_path, right_subtree), spec, max_depth)


def _wrap_subtree(law: ImageLawNode, rng: Random, spec: PrimitiveSetSpec) -> ImageLawNode:
    """Obali podstrom jednoduchym operatorom dostupnym v primitive sete."""

    choices = ["add", "sub", "avg", "clamp_byte"]
    if spec.allows_structure_primitives:
        choices.extend(["mod_const", "floordiv_const", "eq_const", "parity_byte"])

    choice = rng.choice(choices)
    if choice == "add":
        return add_law(law, _random_terminal(rng, spec))
    if choice == "sub":
        return sub_law(law, _random_terminal(rng, spec))
    if choice == "avg":
        return avg_law(law, _random_terminal(rng, spec))
    if choice == "mod_const":
        return mod_const_law(law, rng.choice(_MOD_DIV_VALUES))
    if choice == "floordiv_const":
        return floordiv_const_law(law, rng.choice(_MOD_DIV_VALUES))
    if choice == "eq_const":
        return eq_const_law(law, rng.choice(_EQ_CONST_VALUES))
    if choice == "parity_byte":
        return parity_byte_law(law)
    return clamp_byte_law(law)


def _tweak_subtree(law: ImageLawNode, rng: Random, spec: PrimitiveSetSpec) -> ImageLawNode:
    """Jemne upravi operator alebo jeho parameter."""

    if law.kind in spec.terminals:
        return _random_terminal(rng, spec)
    if law.kind == "add":
        return sub_law(law.children[0], law.children[1])
    if law.kind == "sub":
        return avg_law(law.children[0], law.children[1])
    if law.kind == "avg":
        return add_law(law.children[0], law.children[1])
    if law.kind == "gradient":
        return clamp_byte_law(law)
    if law.kind == "clamp_byte":
        return law.children[0]
    if law.kind == "mod_const":
        current = int(law.value or _MOD_DIV_VALUES[0])
        return mod_const_law(law.children[0], _next_value(_MOD_DIV_VALUES, current, rng))
    if law.kind == "floordiv_const":
        current = int(law.value or _MOD_DIV_VALUES[0])
        return floordiv_const_law(law.children[0], _next_value(_MOD_DIV_VALUES, current, rng))
    if law.kind == "eq_const":
        current = int(law.value or 0)
        return eq_const_law(law.children[0], _next_value(_EQ_CONST_VALUES, current, rng))
    if law.kind == "parity_byte":
        return law.children[0]
    if law.kind == "checker_parity":
        current = int(law.value or _STRUCTURE_BLOCKS[0])
        return checker_parity_law(_next_value(_STRUCTURE_BLOCKS, current, rng))
    return _random_terminal(rng, spec)


def _subtree_paths(law: ImageLawNode, prefix: tuple[int, ...] = ()) -> list[tuple[int, ...]]:
    """Vrati vsetky cesty k podstromom."""

    paths = [prefix]
    for index, child in enumerate(law.children):
        paths.extend(_subtree_paths(child, prefix + (index,)))
    return paths


def _get_subtree(law: ImageLawNode, path: tuple[int, ...]) -> ImageLawNode:
    """Vrati podstrom na zadanej ceste."""

    node = law
    for step in path:
        node = node.children[step]
    return node


def _replace_subtree(law: ImageLawNode, path: tuple[int, ...], replacement: ImageLawNode) -> ImageLawNode:
    """Vrati novy strom s nahradenym podstromom."""

    if not path:
        return replacement

    step = path[0]
    children = list(law.children)
    children[step] = _replace_subtree(children[step], path[1:], replacement)
    return ImageLawNode(law.kind, law.value, tuple(children))


def _prune_law(law: ImageLawNode, spec: PrimitiveSetSpec, max_depth: int) -> ImageLawNode:
    """Oreze strom na malu hlbku, aby search ostal rychly a validny."""

    if max_depth <= 0:
        if law.kind in spec.terminals or law.kind == "checker_parity":
            return law
        if law.children:
            return _prune_law(law.children[0], spec, 0)
        return terminal_law(spec.terminals[0])

    if law.kind in spec.terminals or law.kind == "checker_parity":
        return law

    if law.kind in {"add", "sub", "avg"}:
        return ImageLawNode(
            law.kind,
            None,
            (_prune_law(law.children[0], spec, max_depth - 1), _prune_law(law.children[1], spec, max_depth - 1)),
        )
    if law.kind == "gradient":
        return ImageLawNode(
            law.kind,
            None,
            (
                _prune_law(law.children[0], spec, max_depth - 1),
                _prune_law(law.children[1], spec, max_depth - 1),
                _prune_law(law.children[2], spec, max_depth - 1),
            ),
        )
    if law.kind in {"clamp_byte", "mod_const", "floordiv_const", "eq_const", "parity_byte"}:
        return ImageLawNode(law.kind, law.value, (_prune_law(law.children[0], spec, max_depth - 1),))

    if law.children:
        return _prune_law(law.children[0], spec, max_depth - 1)
    return terminal_law(spec.terminals[0])


def _next_value(options: tuple[int, ...], current: int, rng: Random) -> int:
    """Vrati iny validny parameter z konecnej mnoziny hodnôt."""

    if current not in options:
        return options[0]
    candidates = [value for value in options if value != current]
    if not candidates:
        return current
    return rng.choice(candidates)


def _law_key(law: ImageLawNode) -> str:
    """Vrati stabilny kluc pre deduplikaciu populacie."""

    return render_image_law(law)
