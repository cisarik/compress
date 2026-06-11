"""Binarna serializacia residual streamov pre exact-lossless roundtrip."""

from __future__ import annotations

from .bitstream import BitReader, BitWriter, decode_unsigned_varint, encode_unsigned_varint, zigzag_decode, zigzag_encode
from .residual_codecs import choose_best_residual_codec, signed_width_for_range

_CODEC_NAME_TO_ID = {
    "fixed_signed": 0,
    "zero_rle": 1,
    "varint_residuals": 2,
}
_CODEC_ID_TO_NAME = {value: key for key, value in _CODEC_NAME_TO_ID.items()}


def encode_residuals_binary(residuals: list[int], codec_name: str | None = None) -> bytes:
    """Zakoduje residual stream do realnych bytes."""

    values = [int(value) for value in residuals]
    chosen_codec = _select_codec_name(values, codec_name)

    if chosen_codec == "fixed_signed":
        return _encode_fixed_signed(values)
    if chosen_codec == "zero_rle":
        return _encode_zero_rle(values)
    return _encode_varint_residuals(values)


def decode_residuals_binary(blob: bytes, residual_count: int) -> list[int]:
    """Dekoduje residual stream z binarneho payloadu."""

    if not isinstance(residual_count, int) or residual_count < 0:
        raise ValueError("residual_count must be a non-negative integer")

    payload = bytes(blob)
    codec_id, offset = decode_unsigned_varint(payload, 0)
    codec_name = _CODEC_ID_TO_NAME.get(codec_id)
    if codec_name is None:
        raise ValueError(f"Unsupported residual binary codec id: {codec_id}")

    body = payload[offset:]
    if codec_name == "fixed_signed":
        return _decode_fixed_signed(body, residual_count)
    if codec_name == "zero_rle":
        return _decode_zero_rle(body, residual_count)
    return _decode_varint_residuals(body, residual_count)


def _select_codec_name(residuals: list[int], codec_name: str | None) -> str:
    """Vyberie finalne meno codec-u pre binarnu serializaciu."""

    if codec_name is None:
        return choose_best_residual_codec(residuals).codec_name
    if codec_name in _CODEC_NAME_TO_ID:
        return codec_name
    return "varint_residuals"


def _encode_fixed_signed(residuals: list[int]) -> bytes:
    """Zakoduje residualy do fixed-width zigzag bitstreamu."""

    if residuals:
        width = signed_width_for_range(min(residuals), max(residuals))
    else:
        width = 0

    output = bytearray()
    output.extend(encode_unsigned_varint(_CODEC_NAME_TO_ID["fixed_signed"]))
    output.extend(encode_unsigned_varint(width))
    if width == 0:
        return bytes(output)

    writer = BitWriter()
    for value in residuals:
        writer.write_bits(zigzag_encode(value), width)
    output.extend(writer.to_bytes())
    return bytes(output)


def _decode_fixed_signed(blob: bytes, residual_count: int) -> list[int]:
    """Dekoduje fixed-width residual stream."""

    width, offset = decode_unsigned_varint(blob, 0)
    payload = blob[offset:]

    if width == 0:
        if payload:
            raise ValueError("Zero-width fixed_signed payload must not contain extra bytes")
        return [0] * residual_count

    reader = BitReader(payload)
    values = [zigzag_decode(reader.read_bits(width)) for _ in range(residual_count)]
    _validate_zero_padding(payload, residual_count * width, "fixed_signed payload")
    return values


def _encode_zero_rle(residuals: list[int]) -> bytes:
    """Zakoduje residualy cez jednoduchy zero-run varint stream."""

    output = bytearray()
    output.extend(encode_unsigned_varint(_CODEC_NAME_TO_ID["zero_rle"]))

    index = 0
    while index < len(residuals):
        if residuals[index] == 0:
            run_length = 1
            index += 1
            while index < len(residuals) and residuals[index] == 0:
                run_length += 1
                index += 1
            output.extend(encode_unsigned_varint((run_length - 1) << 1))
            continue

        output.extend(encode_unsigned_varint((zigzag_encode(residuals[index]) << 1) | 1))
        index += 1

    return bytes(output)


def _decode_zero_rle(blob: bytes, residual_count: int) -> list[int]:
    """Dekoduje zero-run varint stream na povodne residualy."""

    values: list[int] = []
    offset = 0

    while len(values) < residual_count:
        token, offset = decode_unsigned_varint(blob, offset)
        if token & 1:
            values.append(zigzag_decode(token >> 1))
            continue

        run_length = (token >> 1) + 1
        if len(values) + run_length > residual_count:
            raise ValueError("zero_rle payload exceeds declared residual_count")
        values.extend([0] * run_length)

    if offset != len(blob):
        raise ValueError("zero_rle payload has trailing bytes")
    return values


def _encode_varint_residuals(residuals: list[int]) -> bytes:
    """Zakoduje residualy cez fallback zigzag varinty."""

    output = bytearray()
    output.extend(encode_unsigned_varint(_CODEC_NAME_TO_ID["varint_residuals"]))
    for value in residuals:
        output.extend(encode_unsigned_varint(zigzag_encode(value)))
    return bytes(output)


def _decode_varint_residuals(blob: bytes, residual_count: int) -> list[int]:
    """Dekoduje fallback varint residual stream."""

    offset = 0
    values: list[int] = []
    for _ in range(residual_count):
        encoded, offset = decode_unsigned_varint(blob, offset)
        values.append(zigzag_decode(encoded))
    if offset != len(blob):
        raise ValueError("varint_residuals payload has trailing bytes")
    return values


def _validate_zero_padding(payload: bytes, used_bits: int, label: str) -> None:
    """Overi, ze padding za skutocnymi datami zostal nulovy."""

    total_bits = len(payload) * 8
    if used_bits > total_bits:
        raise ValueError(f"{label} is shorter than required")
    if used_bits == total_bits:
        return

    full_bytes, used_tail_bits = divmod(used_bits, 8)
    if used_tail_bits:
        mask = (1 << (8 - used_tail_bits)) - 1
        if payload[full_bytes] & mask:
            raise ValueError(f"{label} contains non-zero padding bits")
        full_bytes += 1

    for byte_value in payload[full_bytes:]:
        if byte_value:
            raise ValueError(f"{label} contains non-zero trailing bytes")
