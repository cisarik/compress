from primesymbolicmdl.experiments import dataset_random, dataset_zeros
from primesymbolicmdl.law_search import search_best_law_for_bytes


def test_search_result_includes_required_fields() -> None:
    result = search_best_law_for_bytes(
        dataset_zeros(64),
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_depth=3,
        max_index=7,
    )

    required = {
        "best_law",
        "best_law_string",
        "best_cost",
        "raw_bits",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "generations",
        "population_size",
        "seed",
        "history",
        "max_index",
        "strict_lower",
    }

    assert required.issubset(result)
    assert result["history"]


def test_search_is_deterministic_for_same_seed() -> None:
    left = search_best_law_for_bytes(
        dataset_zeros(64),
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_depth=3,
        max_index=7,
    )
    right = search_best_law_for_bytes(
        dataset_zeros(64),
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_depth=3,
        max_index=7,
    )

    assert left["best_law_string"] == right["best_law_string"]
    assert left["total_bits"] == right["total_bits"]


def test_search_finishes_and_can_improve_on_zero_data() -> None:
    result = search_best_law_for_bytes(
        dataset_zeros(64),
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_depth=3,
        max_index=7,
    )

    assert result["saving_bits"] > 0


def test_search_does_not_need_to_beat_random_data() -> None:
    result = search_best_law_for_bytes(
        dataset_random(64, 1234),
        width_bits=8,
        seed=1234,
        population_size=10,
        generations=5,
        max_depth=3,
        max_index=7,
    )

    assert "best_law_string" in result
    assert isinstance(result["total_bits"], int)
