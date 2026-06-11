"""Male deterministicke GP-lite hladanie anchor zakonov A(i)."""

from __future__ import annotations

from random import Random

from .anchor_laws import (
    LawNode,
    add_law,
    clamp_nonnegative_law,
    const_law,
    floordiv_pow2_law,
    idx_law,
    mul_small_law,
    render_law,
    square_law,
    sub_law,
)
from .blocks import bytes_to_uint_blocks
from .index_branch import estimate_law_cost


def search_best_law_for_bytes(
    data: bytes,
    width_bits: int = 16,
    seed: int = 1234,
    population_size: int = 64,
    generations: int = 40,
    max_depth: int = 4,
    max_index: int | None = None,
    strict_lower: bool = False,
) -> dict:
    """Spusti male deterministicke GP-lite hladanie nad zakonmi A(i)."""

    payload = bytes(data)
    blocks = bytes_to_uint_blocks(payload, width_bits)
    resolved_max_index = _resolve_max_index(blocks, max_index)
    rng = Random(seed)

    population = _seed_population(max_depth)
    attempts = 0
    while len(population) < population_size and attempts < population_size * 20:
        candidate = _random_law(rng, max_depth)
        population[_law_key(candidate)] = candidate
        attempts += 1

    history: list[dict] = []
    best_law: LawNode | None = None
    best_cost: dict | None = None

    for generation_index in range(generations):
        scored = _score_population(
            list(population.values()),
            blocks,
            width_bits,
            len(payload),
            resolved_max_index,
            strict_lower,
        )
        best_law = scored[0]["law"]
        best_cost = scored[0]["cost"]
        history.append(
            {
                "generation": generation_index,
                "best_law": render_law(best_law),
                "total_bits": best_cost["total_bits"],
                "saving_bits": best_cost["saving_bits"],
            }
        )

        elite_count = max(2, min(len(scored), population_size // 8 or 1))
        next_population = {
            _law_key(item["law"]): item["law"]
            for item in scored[:elite_count]
        }

        fill_attempts = 0
        while len(next_population) < population_size and fill_attempts < population_size * 40:
            parent = _tournament_select(scored, rng)
            if rng.random() < 0.35:
                donor = _tournament_select(scored, rng)
                child = _crossover_laws(parent["law"], donor["law"], rng, max_depth)
            else:
                child = _mutate_law(parent["law"], rng, max_depth)
            next_population[_law_key(child)] = child
            fill_attempts += 1

        extra_attempts = 0
        while len(next_population) < population_size and extra_attempts < population_size * 20:
            extra = _random_law(rng, max_depth)
            next_population[_law_key(extra)] = extra
            extra_attempts += 1

        population = next_population

    if best_law is None or best_cost is None:
        raise RuntimeError("Law search did not produce a best candidate")

    return {
        "best_law": best_law,
        "best_law_string": render_law(best_law),
        "best_cost": best_cost,
        "raw_bits": best_cost["raw_bits"],
        "total_bits": best_cost["total_bits"],
        "saving_bits": best_cost["saving_bits"],
        "ratio_vs_raw": best_cost["ratio_vs_raw"],
        "generations": generations,
        "population_size": population_size,
        "seed": seed,
        "history": history,
        "max_index": resolved_max_index,
        "strict_lower": strict_lower,
    }


def _resolve_max_index(blocks: list[int], max_index: int | None) -> int:
    """Vrati maly predvoleny limit indexu pre rychly lokalny search."""

    if max_index is not None:
        if max_index < 0:
            raise ValueError("max_index must be non-negative")
        return max_index
    if not blocks:
        return 0
    return min(31, max(blocks))


def _seed_population(max_depth: int) -> dict[str, LawNode]:
    """Vrati malu sadu rozumnych startovacich zakonov."""

    laws = [
        idx_law(),
        const_law(0),
        const_law(1),
        add_law(idx_law(), const_law(1)),
        sub_law(idx_law(), const_law(1)),
        mul_small_law(idx_law(), 2),
        floordiv_pow2_law(idx_law(), 1),
        square_law(idx_law()),
        clamp_nonnegative_law(sub_law(idx_law(), const_law(1))),
    ]
    return {_law_key(_prune_law(law, max_depth)): _prune_law(law, max_depth) for law in laws}


def _score_population(
    population: list[LawNode],
    blocks: list[int],
    width_bits: int,
    original_size: int,
    max_index: int,
    strict_lower: bool,
) -> list[dict]:
    """Ohodnoti populaciu podla total_bits a stabilne ju utriedi."""

    scored = []
    for law in population:
        cost = estimate_law_cost(blocks, width_bits, original_size, law, max_index, strict_lower)
        scored.append({"law": law, "cost": cost, "law_string": render_law(law)})

    scored.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law_string"]))
    return scored


def _tournament_select(scored: list[dict], rng: Random, size: int = 3) -> dict:
    """Vyberie rodica cez maly turnaj."""

    sample_size = min(size, len(scored))
    candidates = rng.sample(scored, sample_size)
    candidates.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law_string"]))
    return candidates[0]


def _random_law(rng: Random, max_depth: int) -> LawNode:
    """Vygeneruje nahodny zakon malej hlbky."""

    if max_depth <= 0 or rng.random() < 0.3:
        return _random_terminal(rng)

    choice = rng.choice(("add", "sub", "mul_small", "floordiv_pow2", "square", "clamp_nonnegative"))
    if choice == "add":
        return add_law(_random_law(rng, max_depth - 1), _random_law(rng, max_depth - 1))
    if choice == "sub":
        return sub_law(_random_law(rng, max_depth - 1), _random_law(rng, max_depth - 1))
    if choice == "mul_small":
        return mul_small_law(_random_law(rng, max_depth - 1), rng.randint(1, 8))
    if choice == "floordiv_pow2":
        return floordiv_pow2_law(_random_law(rng, max_depth - 1), rng.randint(0, 4))
    if choice == "square":
        return square_law(_random_law(rng, max_depth - 1))
    return clamp_nonnegative_law(_random_law(rng, max_depth - 1))


def _random_terminal(rng: Random) -> LawNode:
    """Vygeneruje terminal idx alebo malu konstantu."""

    if rng.random() < 0.5:
        return idx_law()
    return const_law(rng.randint(-8, 16))


def _mutate_law(law: LawNode, rng: Random, max_depth: int) -> LawNode:
    """Aplikuje malu deterministicku mutaciu podstromu."""

    paths = _subtree_paths(law)
    target_path = rng.choice(paths)
    target = _get_subtree(law, target_path)
    mode = rng.choice(("replace", "wrap", "tweak"))

    if mode == "replace":
        replacement = _random_law(rng, 2)
    elif mode == "wrap":
        replacement = _wrap_subtree(target, rng)
    else:
        replacement = _tweak_subtree(target, rng)

    return _prune_law(_replace_subtree(law, target_path, replacement), max_depth)


def _crossover_laws(left: LawNode, right: LawNode, rng: Random, max_depth: int) -> LawNode:
    """Zlozi dieta nahradenim podstromu darcovskym podstromom."""

    left_path = rng.choice(_subtree_paths(left))
    right_subtree = _get_subtree(right, rng.choice(_subtree_paths(right)))
    return _prune_law(_replace_subtree(left, left_path, right_subtree), max_depth)


def _wrap_subtree(law: LawNode, rng: Random) -> LawNode:
    """Obali podstrom jednoduchym operatorom."""

    choice = rng.choice(("add", "sub", "mul_small", "floordiv_pow2", "square", "clamp_nonnegative"))
    if choice == "add":
        return add_law(law, _random_terminal(rng))
    if choice == "sub":
        return sub_law(law, _random_terminal(rng))
    if choice == "mul_small":
        return mul_small_law(law, rng.randint(1, 8))
    if choice == "floordiv_pow2":
        return floordiv_pow2_law(law, rng.randint(0, 4))
    if choice == "square":
        return square_law(law)
    return clamp_nonnegative_law(law)


def _tweak_subtree(law: LawNode, rng: Random) -> LawNode:
    """Jemne upravi operator alebo jeho parameter."""

    if law.kind == "idx":
        return const_law(rng.randint(-4, 8))
    if law.kind == "const":
        return const_law(int(law.value or 0) + rng.choice((-3, -1, 1, 3)))
    if law.kind == "mul_small":
        return mul_small_law(_require_left(law), max(1, int(law.value or 1) + rng.choice((-2, -1, 1, 2))))
    if law.kind == "floordiv_pow2":
        return floordiv_pow2_law(_require_left(law), min(8, max(0, int(law.value or 0) + rng.choice((-1, 1)))))
    if law.kind == "add":
        return sub_law(_require_left(law), _require_right(law))
    if law.kind == "sub":
        return add_law(_require_left(law), _require_right(law))
    if law.kind == "square":
        return clamp_nonnegative_law(_require_left(law))
    if law.kind == "clamp_nonnegative":
        return square_law(_require_left(law))
    return law


def _subtree_paths(law: LawNode, prefix: tuple[int, ...] = ()) -> list[tuple[int, ...]]:
    """Vrati vsetky cesty k podstromom."""

    paths = [prefix]
    if law.left is not None:
        paths.extend(_subtree_paths(law.left, prefix + (0,)))
    if law.right is not None:
        paths.extend(_subtree_paths(law.right, prefix + (1,)))
    return paths


def _get_subtree(law: LawNode, path: tuple[int, ...]) -> LawNode:
    """Vrati podstrom na zadanej ceste."""

    node = law
    for step in path:
        if step == 0:
            node = _require_left(node)
        else:
            node = _require_right(node)
    return node


def _replace_subtree(law: LawNode, path: tuple[int, ...], replacement: LawNode) -> LawNode:
    """Vrati novy strom s nahradenym podstromom."""

    if not path:
        return replacement

    step = path[0]
    if step == 0:
        return LawNode(law.kind, law.value, _replace_subtree(_require_left(law), path[1:], replacement), law.right)
    return LawNode(law.kind, law.value, law.left, _replace_subtree(_require_right(law), path[1:], replacement))


def _prune_law(law: LawNode, max_depth: int) -> LawNode:
    """Oreze strom na povolenu hlbku, aby search ostal maly."""

    if max_depth <= 0:
        if law.kind == "const":
            return law
        return idx_law()

    if law.kind in {"idx", "const"}:
        return law
    if law.kind == "add":
        return add_law(_prune_law(_require_left(law), max_depth - 1), _prune_law(_require_right(law), max_depth - 1))
    if law.kind == "sub":
        return sub_law(_prune_law(_require_left(law), max_depth - 1), _prune_law(_require_right(law), max_depth - 1))
    if law.kind == "mul_small":
        return mul_small_law(_prune_law(_require_left(law), max_depth - 1), max(1, int(law.value or 1)))
    if law.kind == "floordiv_pow2":
        return floordiv_pow2_law(_prune_law(_require_left(law), max_depth - 1), min(8, max(0, int(law.value or 0))))
    if law.kind == "square":
        return square_law(_prune_law(_require_left(law), max_depth - 1))
    if law.kind == "clamp_nonnegative":
        return clamp_nonnegative_law(_prune_law(_require_left(law), max_depth - 1))
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def _law_key(law: LawNode) -> str:
    """Vrati stabilny kluc pre deduplikaciu populacie."""

    return render_law(law)


def _require_left(law: LawNode) -> LawNode:
    """Overi pritomnost laveho potomka."""

    if law.left is None:
        raise ValueError("law node is missing a left child")
    return law.left


def _require_right(law: LawNode) -> LawNode:
    """Overi pritomnost praveho potomka."""

    if law.right is None:
        raise ValueError("law node is missing a right child")
    return law.right
