import pytest

from primesymbolicmdl.huge_blocks import bytes_to_huge_blocks
from primesymbolicmdl.scaled_prime_index import (
    ScaledPrimeModel,
    decode_scaled_prime_payload,
    encode_block_scaled_prime,
    encode_scaled_prime_payload,
    estimate_scaled_prime_cost,
    model_bits_scaled_prime,
    parameter_bits_scaled_prime,
    render_scaled_prime_model,
    roundtrip_scaled_prime,
)


def test_encode_block_scaled_prime_reconstructs_block() -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=2)
    encoded = encode_block_scaled_prime(37, 16, model)

    assert not encoded["escaped"]
    assert encoded["anchor"] + encoded["diff"] == 37


def test_encode_block_scaled_prime_escape_for_zero() -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=0)
    encoded = encode_block_scaled_prime(0, 8, model)

    assert encoded["escaped"]
    assert encoded["index"] is None
    assert encoded["diff"] == 0


def test_scaled_prime_helpers_return_stable_metadata() -> None:
    model = ScaledPrimeModel(shift=4, direction="lower", search_radius=2)

    assert render_scaled_prime_model(model) == "scaled_prime(direction=lower, shift=4, search_radius=2)"
    assert model_bits_scaled_prime(model) > 0
    assert parameter_bits_scaled_prime(model) > 0


def test_estimate_scaled_prime_cost_returns_required_fields() -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=2)
    data = b"\x00\x02\x00\x03\x00\x05\x00\x07"
    blocks = bytes_to_huge_blocks(data, 16)
    costs = estimate_scaled_prime_cost(blocks, 16, len(data), model)

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
    ("width_bits", "data"),
    [
        (16, b"\x00\x02\x00\x03\x00\x05\x00\x07"),
        (32, b"\x00\x00\x00\x11\x00\x00\x00\x13"),
        (64, b"\x00\x00\x00\x00\x00\x00\x00\x11"),
    ],
)
def test_scaled_prime_payload_roundtrip_is_exact(width_bits: int, data: bytes) -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=2)
    payload = encode_scaled_prime_payload(data, width_bits, model)

    assert decode_scaled_prime_payload(payload) == data
    assert roundtrip_scaled_prime(data, width_bits, model) == data


def test_scaled_prime_branch_rejects_width_above_64() -> None:
    model = ScaledPrimeModel(shift=1, direction="lower", search_radius=0)

    with pytest.raises(ValueError):
        encode_scaled_prime_payload(b"\x00" * 12, 96, model)
