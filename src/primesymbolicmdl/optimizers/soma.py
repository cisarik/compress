"""Maly deterministicky SOMA-like optimizer pre spojite parametre."""

from __future__ import annotations

from dataclasses import dataclass
from math import floor
from random import Random

from .base import OptimizerRequest, OptimizerResult
from ..bitcost import bits_unsigned_range
from ..blocks import bytes_to_uint_blocks
from ..index_branch import estimate_law_cost

_PARAMETER_SCALE = 1000
_FAMILY_MODEL_BITS = {"affine": 10, "quadratic": 14}
_BOUNDS = (-16.0, 16.0)
_PATH_LENGTH = 1.5
_STEP = 0.5
_PRT = 0.6


@dataclass(frozen=True)
class ContinuousLaw:
    """Spojity zakon s malym poctom parametrov pre SOMA vetvu."""

    family: str
    params: tuple[float, float, float]

    def anchor_at(self, index: int) -> int:
        """Vyhodnoti anchor zakon A(i) a oreze ho na nezaporny rozsah."""

        if self.family == "affine":
            a, b, _ = self.params
            return max(0, floor((a * index) + b))
        if self.family == "quadratic":
            a, b, c = self.params
            return max(0, floor((a * index * index) + (b * index) + c))
        raise ValueError(f"Unsupported SOMA family: {self.family}")

    def model_bits(self) -> int:
        """Vrati konzervativnu modelovu cenu rodiny bez parametrov."""

        return _FAMILY_MODEL_BITS[self.family]

    def parameter_bits(self) -> int:
        """Vrati konzervativny pocet bitov pre kvantizovane parametre."""

        count = 2 if self.family == "affine" else 3
        total = 0
        for value in self.params[:count]:
            scaled = abs(int(round(value * _PARAMETER_SCALE)))
            total += 1 if scaled == 0 else 1 + bits_unsigned_range(scaled)
        return total

    def render(self) -> str:
        """Vrati stabilnu textualnu podobu zakona."""

        if self.family == "affine":
            return f"affine(a={self.params[0]:.3f}, b={self.params[1]:.3f})"
        return (
            f"quadratic(a={self.params[0]:.3f}, "
            f"b={self.params[1]:.3f}, c={self.params[2]:.3f})"
        )


class SomaOptimizer:
    """Registry adapter pre SOMA-like search."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "SOMA"

    def available(self) -> bool:
        """SOMA implementacia je dostupna v tomto repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti SOMA-like search nad malou rodinou spojitych zakonov."""

        return run_soma_search(request)


def run_soma_search(request: OptimizerRequest) -> OptimizerResult:
    """Spusti maly deterministicky SOMA-like optimizer."""

    payload = bytes(request.data)
    blocks = bytes_to_uint_blocks(payload, request.width_bits)
    resolved_max_index = _resolve_max_index(blocks, request.max_index)
    rng = Random(request.seed)

    population = _initial_population(rng, request.population_size)
    history: list[dict] = []
    best_law: ContinuousLaw | None = None
    best_cost: dict | None = None

    for generation in range(request.generations):
        scored = _score_population(
            population,
            blocks,
            request.width_bits,
            len(payload),
            resolved_max_index,
            request.strict_lower,
        )
        leader = scored[0]
        best_law = leader["law"]
        best_cost = leader["cost"]
        history.append(
            {
                "generation": generation,
                "best_model": best_law.render(),
                "total_bits": best_cost["total_bits"],
                "saving_bits": best_cost["saving_bits"],
            }
        )

        next_population = [best_law]
        for item in scored[1:]:
            next_population.append(
                _migrate_individual(
                    item["law"],
                    best_law,
                    blocks,
                    request.width_bits,
                    len(payload),
                    resolved_max_index,
                    request.strict_lower,
                    rng,
                )
            )

        while len(next_population) < request.population_size:
            next_population.append(_random_law(rng))

        population = next_population[: request.population_size]

    if best_law is None or best_cost is None:
        fallback = ContinuousLaw("affine", (0.0, 0.0, 0.0))
        best_cost = estimate_law_cost(blocks, request.width_bits, len(payload), fallback, resolved_max_index, request.strict_lower)
        best_law = fallback

    return OptimizerResult(
        optimizer_name="SOMA",
        status="ok",
        best_model=best_law.render(),
        raw_bits=best_cost["raw_bits"],
        total_bits=best_cost["total_bits"],
        saving_bits=best_cost["saving_bits"],
        ratio_vs_raw=best_cost["ratio_vs_raw"],
        history=history,
        details={
            "best_cost": best_cost,
            "max_index": resolved_max_index,
            "note": "Float parameters are estimated research parameters, not a final codec format.",
        },
    )


def _resolve_max_index(blocks: list[int], max_index: int | None) -> int:
    """Vrati maly bezpecny limit indexu."""

    if max_index is not None:
        return max(0, max_index)
    if not blocks:
        return 0
    return min(31, max(blocks), max(0, len(blocks) - 1))


def _initial_population(rng: Random, population_size: int) -> list[ContinuousLaw]:
    """Vytvori uvodnu populaciu s oboma rodinami."""

    population = [
        ContinuousLaw("affine", (1.0, 0.0, 0.0)),
        ContinuousLaw("affine", (0.5, 0.0, 0.0)),
        ContinuousLaw("quadratic", (0.0, 1.0, 0.0)),
        ContinuousLaw("quadratic", (0.0, 0.5, 0.0)),
    ]
    while len(population) < max(1, population_size):
        population.append(_random_law(rng))
    return population[: max(1, population_size)]


def _score_population(
    population: list[ContinuousLaw],
    blocks: list[int],
    width_bits: int,
    original_size: int,
    max_index: int,
    strict_lower: bool,
) -> list[dict]:
    """Ohodnoti a stabilne utriedi populaciu."""

    scored = []
    for law in population:
        cost = estimate_law_cost(blocks, width_bits, original_size, law, max_index, strict_lower)
        scored.append({"law": law, "cost": cost})
    scored.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["law"].render()))
    return scored


def _migrate_individual(
    current: ContinuousLaw,
    leader: ContinuousLaw,
    blocks: list[int],
    width_bits: int,
    original_size: int,
    max_index: int,
    strict_lower: bool,
    rng: Random,
) -> ContinuousLaw:
    """Presunie jedinca po ceste smerom k liderovi a ponecha najlepsiu poziciu."""

    best_law = current
    best_cost = estimate_law_cost(blocks, width_bits, original_size, current, max_index, strict_lower)
    current_vector = list(current.params)
    leader_vector = list(leader.params)

    if current.family != leader.family and rng.random() < 0.25:
        current = ContinuousLaw(leader.family, current.params)
        best_law = current
        best_cost = estimate_law_cost(blocks, width_bits, original_size, current, max_index, strict_lower)

    step_count = int(_PATH_LENGTH / _STEP)
    for step_index in range(1, step_count + 1):
        t = step_index * _STEP
        mask = _prt_mask(rng, 3)
        candidate_vector = []
        for value, target, use_dim in zip(current_vector, leader_vector, mask):
            migrated = value + ((target - value) * t * use_dim)
            candidate_vector.append(_clip(migrated))
        candidate = ContinuousLaw(current.family, tuple(candidate_vector))
        candidate_cost = estimate_law_cost(blocks, width_bits, original_size, candidate, max_index, strict_lower)
        if (candidate_cost["total_bits"], candidate.render()) < (best_cost["total_bits"], best_law.render()):
            best_law = candidate
            best_cost = candidate_cost

    if rng.random() < 0.15:
        mutated = _random_perturbation(best_law, rng)
        mutated_cost = estimate_law_cost(blocks, width_bits, original_size, mutated, max_index, strict_lower)
        if (mutated_cost["total_bits"], mutated.render()) < (best_cost["total_bits"], best_law.render()):
            best_law = mutated

    return best_law


def _prt_mask(rng: Random, dimensions: int) -> list[int]:
    """Vrati PRT masku a zaruci, ze aspon jedna dimenzia ostane aktivna."""

    mask = [1 if rng.random() < _PRT else 0 for _ in range(dimensions)]
    if any(mask):
        return mask
    mask[rng.randrange(dimensions)] = 1
    return mask


def _random_law(rng: Random) -> ContinuousLaw:
    """Vrati nahodneho jedinca v povolenych hraniciach."""

    family = rng.choice(("affine", "quadratic"))
    values = tuple(rng.uniform(*_BOUNDS) for _ in range(3))
    if family == "affine":
        return ContinuousLaw(family, (values[0], values[1], 0.0))
    return ContinuousLaw(family, values)


def _random_perturbation(law: ContinuousLaw, rng: Random) -> ContinuousLaw:
    """Vykona malu lokalnu mutaciu spojitych parametrov."""

    values = list(law.params)
    index = rng.randrange(2 if law.family == "affine" else 3)
    values[index] = _clip(values[index] + rng.uniform(-1.5, 1.5))
    if law.family == "affine":
        values[2] = 0.0
    return ContinuousLaw(law.family, tuple(values))


def _clip(value: float) -> float:
    """Oreze parameter do bezpecnych hranic."""

    return max(_BOUNDS[0], min(_BOUNDS[1], value))
