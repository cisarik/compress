import random

from primesymbolicmdl.residual_binary import decode_residuals_binary, encode_residuals_binary


def test_fixed_signed_binary_roundtrip_for_all_zero_residuals() -> None:
    residuals = [0] * 32
    blob = encode_residuals_binary(residuals, codec_name="fixed_signed")

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals


def test_fixed_signed_binary_roundtrip_for_mixed_values() -> None:
    residuals = [-7, -1, 0, 2, 9, -3, 4]
    blob = encode_residuals_binary(residuals, codec_name="fixed_signed")

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals


def test_zero_rle_binary_roundtrip_for_zero_heavy_stream() -> None:
    residuals = [0, 0, 0, 5, 0, 0, -2, 0, 0, 0, 0, 8]
    blob = encode_residuals_binary(residuals, codec_name="zero_rle")

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals


def test_unknown_codec_name_falls_back_to_varint_residuals() -> None:
    residuals = [-11, 0, 17, -3, 4]
    blob = encode_residuals_binary(residuals, codec_name="unsupported_codec_name")

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals


def test_random_deterministic_residual_roundtrip_with_auto_codec() -> None:
    rng = random.Random(1234)
    residuals = [rng.randint(-20, 20) for _ in range(64)]
    blob = encode_residuals_binary(residuals, codec_name=None)

    assert decode_residuals_binary(blob, residual_count=len(residuals)) == residuals
