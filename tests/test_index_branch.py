from primesymbolicmdl.anchor_laws import const_law, idx_law, sub_law
from primesymbolicmdl.index_branch import (
    encode_block_with_law,
    estimate_law_cost,
    roundtrip_law_payload,
)


def test_encode_block_with_law_reconstructs_x() -> None:
    encoded = encode_block_with_law(7, idx_law(), max_index=10)

    assert not encoded["escaped"]
    assert encoded["anchor"] + encoded["residual"] == 7


def test_strict_lower_false_allows_equal_anchor() -> None:
    encoded = encode_block_with_law(7, idx_law(), max_index=10, strict_lower=False)

    assert encoded["anchor"] == 7
    assert encoded["residual"] == 0


def test_strict_lower_true_disallows_equal_anchor() -> None:
    encoded = encode_block_with_law(7, idx_law(), max_index=10, strict_lower=True)

    assert encoded["anchor"] == 6
    assert encoded["residual"] == 1


def test_escape_case_works() -> None:
    encoded = encode_block_with_law(3, const_law(10), max_index=0)

    assert encoded["escaped"]
    assert encoded["index"] is None
    assert encoded["anchor"] == 0
    assert encoded["residual"] == 3


def test_estimate_law_cost_returns_required_fields() -> None:
    costs = estimate_law_cost([0, 1, 2, 3], 8, 4, idx_law(), max_index=3)

    required = {
        "raw_bits",
        "model_bits",
        "parameter_bits",
        "header_bits",
        "flag_bits",
        "index_bits",
        "residual_bits",
        "residual_codec",
        "residual_codec_details",
        "escape_bits",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "escape_count",
        "block_count",
        "max_index",
        "strict_lower",
        "law",
    }

    assert required.issubset(costs)
    assert costs["raw_bits"] == 32
    assert isinstance(costs["total_bits"], int)
    assert isinstance(costs["saving_bits"], int)
    assert isinstance(costs["ratio_vs_raw"], float)


def test_roundtrip_law_payload_width_8() -> None:
    data = b"\x00\x01\x02\x03\x04"

    assert roundtrip_law_payload(data, 8, idx_law(), max_index=4) == data


def test_roundtrip_law_payload_width_16() -> None:
    data = b"\x00\x00\x00\x01\x00\x02\x00\x03"
    law = sub_law(idx_law(), const_law(0))

    assert roundtrip_law_payload(data, 16, law, max_index=3) == data
