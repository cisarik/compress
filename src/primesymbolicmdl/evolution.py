"""Deterministicke evolucne hladanie indexovanych anchor modelov."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from random import Random

from .bitcost import bits_raw, bits_signed_range, bits_unsigned_range
from .blocks import bytes_to_uint_blocks
from .prime_anchors import nearest_lower_prime, prime_count

_FIXED_MODEL_BITS = 12
_FIXED_HEADER_BITS = 32
_SUPPORTED_FAMILIES = ("prime_lower", "multiple", "power", "square")


@dataclass(frozen=True, order=True)
class AnchorGenome:
    """Jednoducha genomova reprezentacia anchor rodiny a parametra."""

    family: str
    param: int = 0


def _canonicalize_genome(genome: AnchorGenome, max_value: int) -> AnchorGenome:
    """Normalizuje genom do maleho deterministickeho priestoru."""

    if genome.family not in _SUPPORTED_FAMILIES:
        raise ValueError(f"Unsupported genome family: {genome.family}")

    if genome.family == "prime_lower":
        return AnchorGenome("prime_lower", 0)
    if genome.family == "square":
        return AnchorGenome("square", 0)
    if genome.family == "multiple":
        upper = max(1, min(max_value, 4096))
        return AnchorGenome("multiple", min(max(1, genome.param), upper))
    upper = max(2, min(max_value, 16))
    return AnchorGenome("power", min(max(2, genome.param), upper))


def encode_block_with_genome(block: int, genome: AnchorGenome) -> dict:
    """Zakoduje jeden blok cez lower-anchor genom."""

    if block < 0:
        raise ValueError("block must be non-negative")

    if genome.family == "prime_lower":
        if block < 2:
            return {"escaped": True, "anchor": None, "index": None, "residual": None}
        anchor = nearest_lower_prime(block)
        if anchor is None:
            return {"escaped": True, "anchor": None, "index": None, "residual": None}
        return {
            "escaped": False,
            "anchor": anchor,
            "index": prime_count(anchor) - 1,
            "residual": block - anchor,
        }

    if genome.family == "multiple":
        step = max(1, genome.param)
        anchor = (block // step) * step
        return {
            "escaped": False,
            "anchor": anchor,
            "index": anchor // step,
            "residual": block - anchor,
        }

    if genome.family == "power":
        base = max(2, genome.param)
        if block < 1:
            return {"escaped": True, "anchor": None, "index": None, "residual": None}
        anchor = 1
        index = 0
        while anchor * base <= block:
            anchor *= base
            index += 1
        return {
            "escaped": False,
            "anchor": anchor,
            "index": index,
            "residual": block - anchor,
        }

    if genome.family == "square":
        root = isqrt(block)
        anchor = root * root
        return {
            "escaped": False,
            "anchor": anchor,
            "index": root,
            "residual": block - anchor,
        }

    raise ValueError(f"Unsupported genome family: {genome.family}")


def estimate_genome_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    genome: AnchorGenome,
) -> dict:
    """Spocita fitnes kandidata ako plnu odhadovanu cenu modelu."""

    if width_bits <= 0:
        raise ValueError("width_bits must be positive")
    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    raw_bits = bits_raw(original_size)
    block_count = len(blocks)
    flag_bits = block_count

    escaped_count = 0
    indices: list[int] = []
    residuals: list[int] = []

    for block in blocks:
        encoded = encode_block_with_genome(block, genome)
        if encoded["escaped"]:
            escaped_count += 1
            continue
        indices.append(int(encoded["index"]))
        residuals.append(int(encoded["residual"]))

    index_bits = 0
    if indices:
        index_width = bits_unsigned_range(max(indices))
        index_bits = index_width * len(indices)

    residual_bits = 0
    if residuals:
        residual_width = bits_signed_range(min(residuals), max(residuals))
        residual_bits = residual_width * len(residuals)

    param_bits = 0 if genome.param <= 0 else bits_unsigned_range(genome.param)
    model_bits = _FIXED_MODEL_BITS + 3 + param_bits
    escape_bits = escaped_count * width_bits
    total_bits = (
        model_bits
        + _FIXED_HEADER_BITS
        + flag_bits
        + index_bits
        + residual_bits
        + escape_bits
    )

    return {
        "family": genome.family,
        "param": genome.param,
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "header_bits": _FIXED_HEADER_BITS,
        "flag_bits": flag_bits,
        "index_bits": index_bits,
        "residual_bits": residual_bits,
        "escape_bits": escape_bits,
        "escape_count": escaped_count,
        "block_count": block_count,
        "total_bits": total_bits,
        "fitness": raw_bits - total_bits,
        "ratio_vs_raw": 0.0 if raw_bits == 0 and total_bits == 0 else (total_bits / raw_bits if raw_bits else float("inf")),
    }


def _random_genome(rng: Random, max_value: int) -> AnchorGenome:
    """Vygeneruje nahodny genom v malom priestore kandidatov."""

    family = rng.choice(_SUPPORTED_FAMILIES)
    if family == "multiple":
        return _canonicalize_genome(AnchorGenome(family, rng.randint(1, max(1, min(max_value, 4096)))), max_value)
    if family == "power":
        return _canonicalize_genome(AnchorGenome(family, rng.randint(2, max(2, min(max_value, 16)))), max_value)
    return _canonicalize_genome(AnchorGenome(family, 0), max_value)


def _genome_space_size(max_value: int) -> int:
    """Vrati horny odhad poctu rozlisitelnych genomov v malom priestore."""

    multiple_count = max(1, min(max_value, 4096))
    power_count = max(1, min(max_value, 16) - 1)
    return 2 + multiple_count + power_count


def _mutate_genome(genome: AnchorGenome, rng: Random, max_value: int) -> AnchorGenome:
    """Aplikuje malu deterministicku mutaciu parametra alebo rodiny."""

    if rng.random() < 0.25:
        return _random_genome(rng, max_value)

    if genome.family == "multiple":
        delta = rng.choice((-64, -16, -4, -1, 1, 4, 16, 64))
        return _canonicalize_genome(AnchorGenome("multiple", genome.param + delta), max_value)
    if genome.family == "power":
        delta = rng.choice((-2, -1, 1, 2))
        return _canonicalize_genome(AnchorGenome("power", genome.param + delta), max_value)
    if genome.family == "prime_lower":
        return _canonicalize_genome(AnchorGenome(rng.choice(("prime_lower", "square")), 0), max_value)
    return _canonicalize_genome(AnchorGenome(rng.choice(("square", "prime_lower")), 0), max_value)


def _crossover_genomes(left: AnchorGenome, right: AnchorGenome, rng: Random, max_value: int) -> AnchorGenome:
    """Zlozi dieta z dvoch rodicov bez narusenia deterministickosti."""

    family = rng.choice((left.family, right.family))
    if family == "multiple":
        params = [genome.param for genome in (left, right) if genome.family == "multiple"]
        if params:
            param = sum(params) // len(params)
        else:
            param = rng.randint(1, max(1, min(max_value, 4096)))
        return _canonicalize_genome(AnchorGenome("multiple", param), max_value)
    if family == "power":
        params = [genome.param for genome in (left, right) if genome.family == "power"]
        if params:
            param = max(2, sum(params) // len(params))
        else:
            param = rng.randint(2, max(2, min(max_value, 16)))
        return _canonicalize_genome(AnchorGenome("power", param), max_value)
    return _canonicalize_genome(AnchorGenome(family, 0), max_value)


def search_best_genome(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    *,
    generations: int = 12,
    population_size: int = 24,
    seed: int = 1234,
) -> dict:
    """Spusti male evolucne hladanie nad anchor rodinami a vrati najlepsi genom."""

    max_value = max(blocks) if blocks else 16
    effective_population_size = min(population_size, _genome_space_size(max_value))
    rng = Random(seed)

    population = {
        _canonicalize_genome(AnchorGenome("prime_lower", 0), max_value),
        _canonicalize_genome(AnchorGenome("square", 0), max_value),
        _canonicalize_genome(AnchorGenome("multiple", 1), max_value),
        _canonicalize_genome(AnchorGenome("multiple", 2), max_value),
        _canonicalize_genome(AnchorGenome("multiple", 4), max_value),
        _canonicalize_genome(AnchorGenome("power", 2), max_value),
    }

    while len(population) < effective_population_size:
        population.add(_random_genome(rng, max_value))

    history: list[dict] = []
    best_costs: dict | None = None
    best_genome: AnchorGenome | None = None

    for generation in range(generations):
        scored = []
        for genome in sorted(population):
            costs = estimate_genome_cost(blocks, width_bits, original_size, genome)
            scored.append((costs["total_bits"], -costs["fitness"], genome, costs))

        scored.sort(key=lambda item: (item[0], item[1], item[2]))
        current_best = scored[0]
        best_genome = current_best[2]
        best_costs = current_best[3]
        history.append(
            {
                "generation": generation,
                "family": best_genome.family,
                "param": best_genome.param,
                "fitness": best_costs["fitness"],
                "total_bits": best_costs["total_bits"],
            }
        )

        elite_count = max(2, effective_population_size // 4)
        elites = [entry[2] for entry in scored[:elite_count]]
        next_population = set(elites)

        while len(next_population) < effective_population_size:
            left = rng.choice(elites)
            right = rng.choice(elites)
            child = _crossover_genomes(left, right, rng, max_value)
            child = _mutate_genome(child, rng, max_value)
            next_population.add(child)

        population = next_population

    if best_genome is None or best_costs is None:
        raise RuntimeError("Evolution search did not produce a best genome")

    return {
        "best_genome": {"family": best_genome.family, "param": best_genome.param},
        "best_costs": best_costs,
        "history": history,
        "seed": seed,
        "generations": generations,
        "population_size": effective_population_size,
    }


def search_best_genome_for_bytes(
    data: bytes,
    width_bits: int = 16,
    *,
    generations: int = 12,
    population_size: int = 24,
    seed: int = 1234,
) -> dict:
    """Pomocna obalka pre evolucne hladanie priamo nad bytmi."""

    payload = bytes(data)
    blocks = bytes_to_uint_blocks(payload, width_bits)
    return search_best_genome(
        blocks,
        width_bits,
        len(payload),
        generations=generations,
        population_size=population_size,
        seed=seed,
    )
