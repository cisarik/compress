"""Male deterministicke codec baseline vrstvy pre rezidua a bajtove streamy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResidualCodecResult:
    """Stabilny vysledok jedneho residual alebo byte codec kandidata."""

    codec_name: str
    bits: int
    payload: dict
    details: dict


def zigzag_encode(n: int) -> int:
    """Prevedie podpisane cele cislo na nezaporny zigzag tvar."""

    value = int(n)
    return (value << 1) if value >= 0 else ((-value << 1) - 1)


def zigzag_decode(z: int) -> int:
    """Vrati povodne podpisane cele cislo zo zigzag reprezentacie."""

    value = int(z)
    if value < 0:
        raise ValueError("zigzag value must be non-negative")
    if value % 2 == 0:
        return value // 2
    return -((value + 1) // 2)


def signed_width_for_range(min_value: int, max_value: int) -> int:
    """Vrati minimalnu signed fixed-width sirku pre zadany rozsah."""

    if min_value > max_value:
        raise ValueError("min_value must not exceed max_value")
    if min_value == 0 and max_value == 0:
        return 0

    width = 1
    while min_value < -(1 << (width - 1)) or max_value > ((1 << (width - 1)) - 1):
        width += 1
    return width


def unsigned_width_for_max(max_value: int) -> int:
    """Vrati minimalnu unsigned fixed-width sirku pre rozsah 0..max_value."""

    if max_value < 0:
        raise ValueError("max_value must be non-negative")
    if max_value == 0:
        return 0

    width = 0
    limit = 1
    while limit <= max_value:
        width += 1
        limit <<= 1
    return width


def estimate_fixed_signed_residual_bits(residuals: list[int]) -> ResidualCodecResult:
    """Vrati fixed-width signed baseline pre residual stream."""

    values = [int(value) for value in residuals]
    if not values:
        return ResidualCodecResult(
            codec_name="fixed_signed",
            bits=0,
            payload={"codec": "fixed_signed", "count": 0, "residual_width": 0, "values": []},
            details={"count": 0, "min_residual": 0, "max_residual": 0, "residual_width": 0},
        )

    min_residual = min(values)
    max_residual = max(values)
    residual_width = signed_width_for_range(min_residual, max_residual)
    bits = residual_width * len(values)
    payload_values = [] if residual_width == 0 else [zigzag_encode(value) for value in values]
    return ResidualCodecResult(
        codec_name="fixed_signed",
        bits=bits,
        payload={
            "codec": "fixed_signed",
            "count": len(values),
            "residual_width": residual_width,
            "values": payload_values,
        },
        details={
            "count": len(values),
            "min_residual": min_residual,
            "max_residual": max_residual,
            "residual_width": residual_width,
        },
    )


def decode_fixed_signed_residual_payload(payload: dict) -> list[int]:
    """Dekoduje research payload fixed signed residual codec-u."""

    count = payload.get("count")
    residual_width = payload.get("residual_width")
    values = payload.get("values")

    if payload.get("codec") not in {None, "fixed_signed"}:
        raise ValueError("Unsupported fixed signed payload codec")
    if not isinstance(count, int) or count < 0:
        raise ValueError("count must be a non-negative integer")
    if not isinstance(residual_width, int) or residual_width < 0:
        raise ValueError("residual_width must be a non-negative integer")
    if not isinstance(values, list):
        raise ValueError("values must be a list")

    if residual_width == 0:
        return [0] * count
    if len(values) != count:
        raise ValueError("values length does not match count")
    return [zigzag_decode(value) for value in values]


def estimate_zero_rle_residual_bits(residuals: list[int]) -> ResidualCodecResult:
    """Vrati zero-run-length codec baseline pre residual stream."""

    values = [int(value) for value in residuals]
    if not values:
        return ResidualCodecResult(
            codec_name="zero_rle",
            bits=0,
            payload={
                "codec": "zero_rle",
                "count": 0,
                "tokens": [],
                "run_length_width": 0,
                "literal_width": 0,
            },
            details={
                "count": 0,
                "token_count": 0,
                "zero_token_count": 0,
                "literal_token_count": 0,
                "max_run_length": 0,
                "run_length_width": 0,
                "literal_width": 0,
            },
        )

    tokens: list[dict] = []
    index = 0
    while index < len(values):
        if values[index] == 0:
            run_length = 1
            index += 1
            while index < len(values) and values[index] == 0:
                run_length += 1
                index += 1
            tokens.append({"kind": "zero_run", "run_length": run_length})
            continue

        tokens.append({"kind": "literal", "value": zigzag_encode(values[index])})
        index += 1

    run_lengths = [token["run_length"] for token in tokens if token["kind"] == "zero_run"]
    literal_values = [value for value in values if value != 0]
    max_run_length = max(run_lengths, default=0)
    run_length_width = unsigned_width_for_max(max_run_length)
    if literal_values:
        literal_width = signed_width_for_range(min(literal_values), max(literal_values))
    else:
        literal_width = 0

    bits = 0
    for token in tokens:
        bits += 1
        if token["kind"] == "zero_run":
            bits += run_length_width
        else:
            bits += literal_width

    return ResidualCodecResult(
        codec_name="zero_rle",
        bits=bits,
        payload={
            "codec": "zero_rle",
            "count": len(values),
            "tokens": tokens,
            "run_length_width": run_length_width,
            "literal_width": literal_width,
        },
        details={
            "count": len(values),
            "token_count": len(tokens),
            "zero_token_count": len(run_lengths),
            "literal_token_count": len(literal_values),
            "max_run_length": max_run_length,
            "run_length_width": run_length_width,
            "literal_width": literal_width,
        },
    )


def decode_zero_rle_residual_payload(payload: dict) -> list[int]:
    """Dekoduje research payload zero-RLE residual codec-u."""

    count = payload.get("count")
    tokens = payload.get("tokens")

    if payload.get("codec") not in {None, "zero_rle"}:
        raise ValueError("Unsupported zero_rle payload codec")
    if not isinstance(count, int) or count < 0:
        raise ValueError("count must be a non-negative integer")
    if not isinstance(tokens, list):
        raise ValueError("tokens must be a list")

    decoded: list[int] = []
    for token in tokens:
        if not isinstance(token, dict):
            raise ValueError("token must be a dict")
        kind = token.get("kind")
        if kind == "zero_run":
            run_length = token.get("run_length")
            if not isinstance(run_length, int) or run_length <= 0:
                raise ValueError("zero_run token requires a positive run_length")
            decoded.extend([0] * run_length)
            continue
        if kind == "literal":
            value = token.get("value")
            if not isinstance(value, int):
                raise ValueError("literal token requires an integer value")
            decoded.append(zigzag_decode(value))
            continue
        raise ValueError(f"Unsupported token kind: {kind}")

    if len(decoded) != count:
        raise ValueError("Decoded residual count does not match payload count")
    return decoded


def estimate_byte_rle_bits(data: bytes) -> ResidualCodecResult:
    """Vrati byte-run-length baseline pre bajtovy stream."""

    payload = bytes(data)
    if not payload:
        return ResidualCodecResult(
            codec_name="byte_rle",
            bits=0,
            payload={"codec": "byte_rle", "length": 0, "tokens": [], "run_length_width": 0},
            details={"length": 0, "token_count": 0, "max_run_length": 0, "run_length_width": 0},
        )

    tokens: list[dict] = []
    index = 0
    while index < len(payload):
        value = payload[index]
        run_length = 1
        index += 1
        while index < len(payload) and payload[index] == value:
            run_length += 1
            index += 1
        tokens.append({"run_length": run_length, "byte_value": value})

    max_run_length = max(token["run_length"] for token in tokens)
    run_length_width = unsigned_width_for_max(max_run_length)
    bits = len(tokens) * (run_length_width + 8)
    return ResidualCodecResult(
        codec_name="byte_rle",
        bits=bits,
        payload={
            "codec": "byte_rle",
            "length": len(payload),
            "tokens": tokens,
            "run_length_width": run_length_width,
        },
        details={
            "length": len(payload),
            "token_count": len(tokens),
            "max_run_length": max_run_length,
            "run_length_width": run_length_width,
            "token_bits": run_length_width + 8,
        },
    )


def decode_byte_rle_payload(payload: dict) -> bytes:
    """Dekoduje research payload byte-RLE codec-u."""

    length = payload.get("length")
    tokens = payload.get("tokens")

    if payload.get("codec") not in {None, "byte_rle"}:
        raise ValueError("Unsupported byte_rle payload codec")
    if not isinstance(length, int) or length < 0:
        raise ValueError("length must be a non-negative integer")
    if not isinstance(tokens, list):
        raise ValueError("tokens must be a list")

    decoded = bytearray()
    for token in tokens:
        if not isinstance(token, dict):
            raise ValueError("token must be a dict")
        run_length = token.get("run_length")
        byte_value = token.get("byte_value")
        if not isinstance(run_length, int) or run_length <= 0:
            raise ValueError("run_length must be a positive integer")
        if not isinstance(byte_value, int) or byte_value < 0 or byte_value > 255:
            raise ValueError("byte_value must be in range 0..255")
        decoded.extend([byte_value] * run_length)

    if len(decoded) != length:
        raise ValueError("Decoded byte length does not match payload length")
    return bytes(decoded)


def choose_best_residual_codec(residuals: list[int]) -> ResidualCodecResult:
    """Vyberie najlacnejsi residual codec kandidat pre zadany stream."""

    candidates = [
        estimate_fixed_signed_residual_bits(residuals),
        estimate_zero_rle_residual_bits(residuals),
    ]
    return min(enumerate(candidates), key=lambda item: (item[1].bits, item[0]))[1]


def choose_best_byte_codec(data: bytes) -> ResidualCodecResult:
    """Vyberie najlacnejsi byte codec kandidat pre zadany bajtovy stream."""

    payload = bytes(data)
    candidates = [
        ResidualCodecResult(
            codec_name="raw_bytes",
            bits=len(payload) * 8,
            payload={"codec": "raw_bytes", "data": payload},
            details={"length": len(payload)},
        ),
        estimate_byte_rle_bits(payload),
    ]
    return min(enumerate(candidates), key=lambda item: (item[1].bits, item[0]))[1]
