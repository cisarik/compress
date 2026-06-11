import pytest

from primesymbolicmdl.huge_anchor_binary import (
    compress_best_huge_anchor_binary,
    decode_huge_anchor_binary,
    encode_huge_anchor_binary,
    rerank_huge_anchor_candidates_by_actual_size,
)
from primesymbolicmdl.huge_anchor_datasets import make_huge_anchor_dataset
from primesymbolicmdl.huge_anchor_models import HugeAnchorModel
from primesymbolicmdl.huge_anchor_search import search_best_huge_anchor_model


@pytest.mark.parametrize(
    ("dataset_name", "width_bits"),
    [
        ("linear_shift_generated", 16),
        ("square_generated", 64),
        ("multiple_generated", 32),
    ],
)
def test_huge_anchor_binary_exact_roundtrip_for_generated_datasets(dataset_name: str, width_bits: int) -> None:
    data = make_huge_anchor_dataset(dataset_name, width_bits, count=32, seed=1234)
    model = compress_best_huge_anchor_binary(data, width_bits=width_bits)["best_model"]
    blob = encode_huge_anchor_binary(data, width_bits, model)

    assert decode_huge_anchor_binary(blob) == data


def test_huge_anchor_binary_random_data_decodes_exactly() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=32)

    assert decode_huge_anchor_binary(result["binary_blob"]) == data
    assert result["roundtrip_ok"] is True


def test_huge_anchor_binary_rejects_corrupt_magic() -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 16, count=8, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=16)
    corrupt = b"BADMAGIC" + result["binary_blob"][8:]

    with pytest.raises(ValueError, match="magic"):
        decode_huge_anchor_binary(corrupt)


def test_huge_anchor_binary_rejects_unsupported_family() -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 16, count=8, seed=1234)

    with pytest.raises(ValueError, match="Unsupported huge anchor family"):
        encode_huge_anchor_binary(data, 16, HugeAnchorModel("imaginary_family", {}))


def test_compress_best_huge_anchor_binary_roundtrips_square_generated() -> None:
    data = make_huge_anchor_dataset("square_generated", 64, count=32, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=64)

    assert result["roundtrip_ok"] is True
    assert decode_huge_anchor_binary(result["binary_blob"]) == data
    assert result["actual_rerank_candidates"]
    assert result["estimated_best_model_string"]


def test_at_least_one_synthetic_dataset_is_truly_smaller_in_actual_bytes() -> None:
    results = []
    for dataset_name in ("linear_shift_generated", "square_generated", "multiple_generated"):
        for width_bits in (16, 32, 64):
            data = make_huge_anchor_dataset(dataset_name, width_bits, count=32, seed=1234)
            results.append(compress_best_huge_anchor_binary(data, width_bits=width_bits))

    assert any(result["decision"] == "compressed" for result in results)
    assert any(result["compressed_bytes"] < result["raw_bytes"] for result in results)


def test_random_data_is_not_reported_as_fake_actual_win() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=32)

    assert result["roundtrip_ok"] is True
    if result["decision"] == "compressed":
        assert result["compressed_bytes"] < result["raw_bytes"]
    else:
        assert result["compressed_bytes"] >= result["raw_bytes"]


def test_actual_rerank_candidates_are_exact_and_use_actual_bytes() -> None:
    data = make_huge_anchor_dataset("repeating_pattern", 32, count=32, seed=1234)
    search_result = search_best_huge_anchor_model(data, width_bits=32)
    candidates = rerank_huge_anchor_candidates_by_actual_size(data, 32, search_result, top_n=4)

    successful = [candidate for candidate in candidates if candidate["status"] == "ok"]

    assert len(successful) >= 2
    assert all(candidate["roundtrip_ok"] is True for candidate in successful)
    assert all(candidate["actual_bits"] == candidate["compressed_bytes"] * 8 for candidate in successful)
    for candidate in successful:
        if candidate["decision"] == "compressed":
            assert candidate["compressed_bytes"] < candidate["raw_bytes"]
        else:
            assert candidate["compressed_bytes"] >= candidate["raw_bytes"]


def test_compress_best_huge_anchor_binary_reports_estimated_vs_actual_winner() -> None:
    data = make_huge_anchor_dataset("repeating_pattern", 32, count=32, seed=1234)
    result = compress_best_huge_anchor_binary(data, width_bits=32, actual_rerank_top_n=4)

    assert result["actual_rerank_top_n"] == 4
    assert result["best_model_string"]
    assert result["estimated_best_model_string"]
    assert isinstance(result["actual_rerank_changed_winner"], bool)
