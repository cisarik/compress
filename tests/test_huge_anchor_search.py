from primesymbolicmdl.huge_anchor_datasets import make_huge_anchor_dataset
from primesymbolicmdl.huge_anchor_models import huge_anchor_model_from_dict, huge_anchor_model_to_dict
from primesymbolicmdl.huge_anchor_search import candidate_huge_anchor_models, search_best_huge_anchor_model


def test_candidate_huge_anchor_models_include_expected_families() -> None:
    families = {model.family for model in candidate_huge_anchor_models(32)}

    assert {"linear_shift", "affine_shift", "multiple", "square", "scaled_prime"}.issubset(families)


def test_huge_anchor_search_runs_on_tiny_deterministic_data() -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 16, count=16, seed=1234)
    result = search_best_huge_anchor_model(data, width_bits=16)

    assert result["best_model_string"]
    assert result["raw_bits"] == len(data) * 8
    assert result["roundtrip_ok"] is True
    assert result["history"]
    first_candidate = result["history"][0]
    assert first_candidate["model_dict"]
    assert huge_anchor_model_to_dict(huge_anchor_model_from_dict(first_candidate["model_dict"])) == first_candidate["model_dict"]


def test_huge_anchor_search_is_deterministic_for_same_seed() -> None:
    data = make_huge_anchor_dataset("multiple_generated", 32, count=16, seed=1234)
    left = search_best_huge_anchor_model(data, width_bits=32, seed=1234)
    right = search_best_huge_anchor_model(data, width_bits=32, seed=1234)

    assert left["best_model"] == right["best_model"]
    assert left["best_model_dict"] == right["best_model_dict"]
    assert left["best_model_string"] == right["best_model_string"]
    assert left["total_bits"] == right["total_bits"]
    assert left["history"] == right["history"]


def test_huge_anchor_search_handles_random_data_without_crashing() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=16, seed=1234)
    result = search_best_huge_anchor_model(data, width_bits=32)

    assert result["roundtrip_ok"] is True
    assert isinstance(result["total_bits"], int)
    assert isinstance(result["saving_bits"], int)


def test_huge_anchor_search_finds_synthetic_win() -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 32, count=32, seed=1234)
    result = search_best_huge_anchor_model(data, width_bits=32)

    assert result["roundtrip_ok"] is True
    assert result["decision"] == "win"
    assert result["saving_bits"] > 0
