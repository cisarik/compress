"""Scaled prime-index branch s exact 64-bit prvociselnymi anchor-mi."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks, huge_blocks_to_bytes
from .prime_bigint import prev_prime_64
from .residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    signed_width_for_range,
    unsigned_width_for_max,
)

_FIXED_MODEL_BITS = 12
_FIXED_HEADER_BITS = 32
_MAX_UINT64 = 1 << 64


@dataclass(frozen=True, order=True)
class ScaledPrimeModel:
    """Parametre scaled prime-index modelu."""

    shift: int
    direction: str
    search_radius: int


def render_scaled_prime_model(model: ScaledPrimeModel) -> str:
    """Vrati stabilnu textualnu reprezentaciu modelu."""

    _validate_model(model)
    return f"scaled_prime(direction={model.direction}, shift={model.shift}, search_radius={model.search_radius})"


def model_bits_scaled_prime(model: ScaledPrimeModel) -> int:
    """Vrati fixnu cenu identifikacie scaled-prime vetvy."""

    _validate_model(model)
    return _FIXED_MODEL_BITS


def parameter_bits_scaled_prime(model: ScaledPrimeModel) -> int:
    """Vrati konzervativny odhad ceny parametrov modelu."""

    _validate_model(model)
    direction_bits = 2
    return direction_bits + unsigned_width_for_max(model.shift) + unsigned_width_for_max(model.search_radius)


def encode_block_scaled_prime(x: int, width_bits: int, model: ScaledPrimeModel) -> dict:
    """Zakoduje jeden blok cez scaled prime-index anchor alebo vrati escape."""

    _validate_width_bits(width_bits)
    _validate_model(model)
    _validate_block_value(x, width_bits)

    base_index = x >> model.shift
    lower_index = max(0, base_index - model.search_radius)
    upper_index = base_index + model.search_radius

    best: tuple[int, int, int, int] | None = None

    for index in range(lower_index, upper_index + 1):
        anchor = _anchor_from_index(index, model)
        if anchor is None or anchor > x:
            continue

        diff = x - anchor
        candidate = (abs(diff), _rough_local_cost(index, diff), index, anchor)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        return {
            "index": None,
            "anchor": 0,
            "diff": x,
            "escaped": True,
            "base_index": base_index,
        }

    _, _, index, anchor = best
    return {
        "index": index,
        "anchor": anchor,
        "diff": x - anchor,
        "escaped": False,
        "base_index": base_index,
    }


def estimate_scaled_prime_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    model: ScaledPrimeModel,
) -> dict:
    """Spocita plny MDL-style cost scaled-prime vetvy bez auto fallbacku."""

    _validate_width_bits(width_bits)
    _validate_model(model)
    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    max_decoded_size = len(blocks) * (width_bits // 8)
    if original_size > max_decoded_size:
        raise ValueError("original_size exceeds the decoded block capacity")

    for block in blocks:
        _validate_block_value(int(block), width_bits)

    raw_bits = original_size * 8
    block_count = len(blocks)
    flag_bits = block_count
    encoded_blocks = [encode_block_scaled_prime(int(block), width_bits, model) for block in blocks]

    indices = [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    escape_count = sum(1 for entry in encoded_blocks if entry["escaped"])

    if indices:
        index_width = unsigned_width_for_max(max(indices))
        index_bits = index_width * len(indices)
    else:
        index_bits = 0

    residual_codec = choose_best_residual_codec(residuals)
    residual_bits = residual_codec.bits
    model_bits = model_bits_scaled_prime(model)
    parameter_bits = parameter_bits_scaled_prime(model)
    escape_bits = width_bits * escape_count
    total_bits = (
        model_bits
        + parameter_bits
        + _FIXED_HEADER_BITS
        + flag_bits
        + index_bits
        + residual_bits
        + escape_bits
    )
    saving_bits = raw_bits - total_bits

    return {
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "parameter_bits": parameter_bits,
        "header_bits": _FIXED_HEADER_BITS,
        "flag_bits": flag_bits,
        "index_bits": index_bits,
        "residual_bits": residual_bits,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "escape_bits": escape_bits,
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "escape_count": escape_count,
        "block_count": block_count,
        "model": render_scaled_prime_model(model),
    }


def encode_scaled_prime_payload(data: bytes, width_bits: int, model: ScaledPrimeModel) -> dict:
    """Zakoduje data do exact payloadu scaled-prime vetvy."""

    _validate_width_bits(width_bits)
    _validate_model(model)

    payload = bytes(data)
    blocks = bytes_to_huge_blocks(payload, width_bits)
    encoded_blocks = [encode_block_scaled_prime(block, width_bits, model) for block in blocks]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    residual_codec = choose_best_residual_codec(residuals)

    return {
        "codec": "scaled_prime_index",
        "width_bits": width_bits,
        "original_size": len(payload),
        "block_count": len(blocks),
        "model": {
            "shift": model.shift,
            "direction": model.direction,
            "search_radius": model.search_radius,
        },
        "flags": [bool(entry["escaped"]) for entry in encoded_blocks],
        "indices": [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None],
        "raw_blocks": [int(block) for block, entry in zip(blocks, encoded_blocks) if entry["escaped"]],
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "residual_payload": residual_codec.payload,
    }


def decode_scaled_prime_payload(payload: dict) -> bytes:
    """Dekoduje payload scaled-prime vetvy spat na povodne bajty."""

    if payload.get("codec") not in {None, "scaled_prime_index"}:
        raise ValueError("Unsupported scaled-prime payload codec")

    width_bits = payload.get("width_bits")
    original_size = payload.get("original_size")
    block_count = payload.get("block_count")
    flags = payload.get("flags")
    indices = payload.get("indices")
    raw_blocks = payload.get("raw_blocks")
    model_payload = payload.get("model")
    residual_payload = payload.get("residual_payload")

    if not isinstance(width_bits, int):
        raise ValueError("width_bits must be an integer")
    if not isinstance(original_size, int) or original_size < 0:
        raise ValueError("original_size must be a non-negative integer")
    if not isinstance(block_count, int) or block_count < 0:
        raise ValueError("block_count must be a non-negative integer")
    if not isinstance(flags, list):
        raise ValueError("flags must be a list")
    if not isinstance(indices, list):
        raise ValueError("indices must be a list")
    if not isinstance(raw_blocks, list):
        raise ValueError("raw_blocks must be a list")
    if not isinstance(model_payload, dict):
        raise ValueError("model must be a dict")
    if not isinstance(residual_payload, dict):
        raise ValueError("residual_payload must be a dict")

    _validate_width_bits(width_bits)
    if len(flags) != block_count:
        raise ValueError("flags length does not match block_count")

    model = ScaledPrimeModel(
        shift=int(model_payload.get("shift")),
        direction=str(model_payload.get("direction")),
        search_radius=int(model_payload.get("search_radius")),
    )
    _validate_model(model)

    residuals = _decode_residual_payload(residual_payload)
    index_position = 0
    residual_position = 0
    raw_position = 0
    decoded_blocks: list[int] = []

    for flag in flags:
        escaped = _coerce_flag(flag)
        if escaped:
            if raw_position >= len(raw_blocks):
                raise ValueError("raw_blocks are shorter than escape flags")
            block = int(raw_blocks[raw_position])
            raw_position += 1
            decoded_blocks.append(block)
            continue

        if index_position >= len(indices):
            raise ValueError("indices are shorter than non-escape flags")
        if residual_position >= len(residuals):
            raise ValueError("residual stream is shorter than non-escape flags")

        index = int(indices[index_position])
        residual = int(residuals[residual_position])
        index_position += 1
        residual_position += 1

        anchor = _anchor_from_index(index, model)
        if anchor is None:
            raise ValueError("Stored index cannot reconstruct a valid prime anchor")
        decoded_blocks.append(anchor + residual)

    if index_position != len(indices):
        raise ValueError("Unused indices remain after decoding")
    if residual_position != len(residuals):
        raise ValueError("Unused residual values remain after decoding")
    if raw_position != len(raw_blocks):
        raise ValueError("Unused raw blocks remain after decoding")

    return huge_blocks_to_bytes(decoded_blocks, width_bits, original_size)


def roundtrip_scaled_prime(data: bytes, width_bits: int, model: ScaledPrimeModel) -> bytes:
    """Zakoduje a spatne dekoduje data cez scaled-prime payload."""

    return decode_scaled_prime_payload(encode_scaled_prime_payload(bytes(data), width_bits, model))


def _validate_width_bits(width_bits: int) -> None:
    """Overi, ze sirka blokov patri medzi podporovane hodnoty vetvy."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS or width_bits > 64:
        raise ValueError(f"Scaled-prime branch supports only width_bits <= 64 from {sorted(value for value in SUPPORTED_HUGE_WIDTHS if value <= 64)}.")


def _validate_model(model: ScaledPrimeModel) -> None:
    """Overi, ze model patri do zatial podporovanej podmnoziny."""

    if not isinstance(model.shift, int) or model.shift < 1:
        raise ValueError("shift must be a positive integer")
    if model.direction != "lower":
        raise ValueError('Only direction="lower" is currently supported')
    if not isinstance(model.search_radius, int) or model.search_radius < 0:
        raise ValueError("search_radius must be a non-negative integer")


def _validate_block_value(x: int, width_bits: int) -> None:
    """Overi rozsah jedneho bloku pre danu sirku."""

    if x < 0 or x >= (1 << width_bits):
        raise ValueError(f"Block out of range for {width_bits} bits: {x}")


def _rough_local_cost(index: int, diff: int) -> int:
    """Vrati hruby lokalny cost pre rozlisovanie remiz kandidatov."""

    return unsigned_width_for_max(index) + signed_width_for_range(diff, diff)


def _anchor_from_index(index: int, model: ScaledPrimeModel) -> int | None:
    """Rekonstruuje lower-prime anchor z indexu a modelu."""

    if index < 0:
        raise ValueError("index must be non-negative")

    base = index << model.shift
    if base >= _MAX_UINT64:
        return None
    return prev_prime_64(base)


def _decode_residual_payload(payload: dict) -> list[int]:
    """Dekoduje residual payload podla ulozeneho codec mena."""

    codec_name = payload.get("codec")
    if codec_name in {None, "fixed_signed"}:
        return decode_fixed_signed_residual_payload(payload)
    if codec_name == "zero_rle":
        return decode_zero_rle_residual_payload(payload)
    raise ValueError(f"Unsupported residual payload codec: {codec_name}")


def _coerce_flag(flag: object) -> bool:
    """Prevedie payload flag na bool s kontrolou povoleneho tvaru."""

    if isinstance(flag, bool):
        return flag
    if isinstance(flag, int) and flag in {0, 1}:
        return bool(flag)
    raise ValueError("Flag values must be bool or 0/1 integers")


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer ceny modelu voci raw vetve."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
