from primesymbolicmdl.residual_codecs import (
    choose_best_byte_codec,
    choose_best_residual_codec,
    decode_byte_rle_payload,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    estimate_byte_rle_bits,
    estimate_fixed_signed_residual_bits,
    estimate_zero_rle_residual_bits,
    zigzag_decode,
    zigzag_encode,
)


def test_zigzag_roundtrip_for_signed_values() -> None:
    values = [-9, -2, -1, 0, 1, 2, 9]

    assert [zigzag_decode(zigzag_encode(value)) for value in values] == values


def test_fixed_signed_codec_roundtrips() -> None:
    residuals = [-3, 0, 4, -1, 2]
    result = estimate_fixed_signed_residual_bits(residuals)

    assert decode_fixed_signed_residual_payload(result.payload) == residuals


def test_all_zero_fixed_signed_codec_has_zero_bits() -> None:
    result = estimate_fixed_signed_residual_bits([0] * 12)

    assert result.bits == 0
    assert decode_fixed_signed_residual_payload(result.payload) == [0] * 12


def test_zero_rle_roundtrips_mixed_residuals() -> None:
    residuals = [0, 0, 5, 0, -3, 0, 0, 0, 7]
    result = estimate_zero_rle_residual_bits(residuals)

    assert decode_zero_rle_residual_payload(result.payload) == residuals


def test_zero_rle_has_low_cost_for_long_zero_run() -> None:
    residuals = [0] * 64
    result = estimate_zero_rle_residual_bits(residuals)

    assert result.bits > 0
    assert result.bits < (len(residuals) * 8)


def test_byte_rle_roundtrips_repeated_bytes() -> None:
    data = b"\x00\x00\x00\xff\xff\x01\x01\x01\x01"
    result = estimate_byte_rle_bits(data)

    assert decode_byte_rle_payload(result.payload) == data


def test_choose_best_byte_codec_is_stable_for_random_like_data() -> None:
    data = bytes(range(32))
    result = choose_best_byte_codec(data)

    assert result.codec_name in {"raw_bytes", "byte_rle"}
    assert isinstance(result.bits, int)


def test_residual_codec_selector_returns_required_fields() -> None:
    result = choose_best_residual_codec([0, 0, 1, 0, -1])

    assert result.codec_name in {"fixed_signed", "zero_rle"}
    assert isinstance(result.bits, int)
    assert isinstance(result.payload, dict)
    assert isinstance(result.details, dict)
