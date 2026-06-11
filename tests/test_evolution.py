from primesymbolicmdl.evolution import (
    AnchorGenome,
    encode_block_with_genome,
    estimate_genome_cost,
    search_best_genome_for_bytes,
)
from primesymbolicmdl.experiments import dataset_random, dataset_zeros


def test_encode_block_with_genome_reconstructs_exactly() -> None:
    for genome in (
        AnchorGenome("prime_lower", 0),
        AnchorGenome("multiple", 4),
        AnchorGenome("power", 2),
        AnchorGenome("square", 0),
    ):
        encoded = encode_block_with_genome(37, genome)

        if encoded["escaped"]:
            continue

        assert encoded["anchor"] <= 37
        assert encoded["anchor"] + encoded["residual"] == 37


def test_estimate_genome_cost_reports_numeric_fitness() -> None:
    costs = estimate_genome_cost([0, 0, 0, 0], 8, 4, AnchorGenome("multiple", 1))

    assert isinstance(costs["fitness"], int)
    assert costs["fitness"] == costs["raw_bits"] - costs["total_bits"]


def test_evolution_search_is_deterministic_for_same_seed() -> None:
    data = dataset_zeros(128)
    left = search_best_genome_for_bytes(data, 8, generations=8, population_size=16, seed=1234)
    right = search_best_genome_for_bytes(data, 8, generations=8, population_size=16, seed=1234)

    assert left["best_genome"] == right["best_genome"]
    assert left["best_costs"]["total_bits"] == right["best_costs"]["total_bits"]


def test_evolution_search_finds_improvement_on_zero_data() -> None:
    result = search_best_genome_for_bytes(dataset_zeros(256), 8, generations=8, population_size=16, seed=1234)

    assert result["best_costs"]["fitness"] > 0
    assert result["best_costs"]["total_bits"] < result["best_costs"]["raw_bits"]


def test_evolution_search_does_not_crash_on_random_data() -> None:
    result = search_best_genome_for_bytes(dataset_random(128, 1234), 8, generations=6, population_size=12, seed=1234)

    assert "best_genome" in result
    assert "history" in result
