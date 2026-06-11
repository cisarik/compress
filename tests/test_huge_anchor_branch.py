import pytest

from primesymbolicmdl.huge_anchor_branch import (
    decode_huge_anchor_payload,
    encode_block_huge_anchor,
    encode_huge_anchor_payload,
    estimate_huge_anchor_cost,
    roundtrip_huge_anchor,
)
from primesymbolicmdl.huge_anchor_models import HugeAnchorModel
from primesymbolicmdl.huge_blocks import bytes_to_huge_blocks


@pytest.mark.parametrize(
    ("model", "x", "width_bits"),
    [
        (HugeAnchorModel("linear_shift", {"shift": 3}), 41, 16),
        (HugeAnchorModel("affine_shift", {"shift": 3, "bias": 1}), 41, 16),
        (HugeAnchorModel("multiple", {"step": 7}), 43, 16),
        (HugeAnchorModel("square", {}), 83, 16),
        (HugeAnchorModel("scaled_prime", {"shift": 4, "search_radius": 0}), 53, 16),
    ],
)
def test_encode_block_huge_anchor_reconstructs_block(model: HugeAnchorModel, x: int, width_bits: int) -> None:
    encoded = encode_block_huge_anchor(x, width_bits, model, search_radius=2)

    assert encoded["anchor"] + encoded["diff"] == x


def test_encode_block_huge_anchor_escape_works_for_unreachable_prime_case() -> None:
    model = HugeAnchorModel("scaled_prime", {"shift": 1, "search_radius": 0})
    encoded = encode_block_huge_anchor(0, 8, model)

    assert encoded["escaped"]
    assert encoded["index"] is None
    assert encoded["diff"] == 0


def test_estimate_huge_anchor_cost_returns_required_fields() -> None:
    model = HugeAnchorModel("linear_shift", {"shift": 4})
    data = b"\x00\x10\x00\x20\x00\x30\x00\x40"
    blocks = bytes_to_huge_blocks(data, 16)
    costs = estimate_huge_anchor_cost(blocks, 16, len(data), model, search_radius=1)

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
        "model",
    }

    assert required.issubset(costs)
    assert costs["raw_bits"] == len(data) * 8


@pytest.mark.parametrize(
    ("model", "width_bits", "data"),
    [
        (HugeAnchorModel("linear_shift", {"shift": 4}), 16, b"\x00\x10\x00\x20\x00\x30\x00\x40"),
        (HugeAnchorModel("multiple", {"step": 31}), 32, b"\x00\x00\x00\x1f\x00\x00\x00>\x00\x00\x00]"),
        (HugeAnchorModel("square", {}), 64, b"\x00\x00\x00\x00\x00\x00\x00\x04"),
        (HugeAnchorModel("linear_shift", {"shift": 8}), 128, b"\x00" * 16 + b"\x01" * 16),
        (HugeAnchorModel("scaled_prime", {"shift": 4, "search_radius": 0}), 16, b"\x00/\x003\x005\x007"),
    ],
)
def test_huge_anchor_payload_roundtrip_is_exact(model: HugeAnchorModel, width_bits: int, data: bytes) -> None:
    payload = encode_huge_anchor_payload(data, width_bits, model, search_radius=2)

    assert decode_huge_anchor_payload(payload) == data
    assert roundtrip_huge_anchor(data, width_bits, model, search_radius=2) == data


def test_huge_anchor_roundtrip_supports_width_96_for_non_prime_family() -> None:
    model = HugeAnchorModel("multiple", {"step": 31})
    data = (31).to_bytes(12, "big") + (62).to_bytes(12, "big")

    assert roundtrip_huge_anchor(data, 96, model, search_radius=1) == data
