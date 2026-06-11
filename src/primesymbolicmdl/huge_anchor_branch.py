"""Vseobecna huge-anchor vetva nad index-plus-diff reprezentaciou."""

from __future__ import annotations

import math
from math import isqrt

from .huge_anchor_models import (
    HugeAnchorModel,
    anchor_from_index,
    huge_anchor_model_bits,
    huge_anchor_parameter_bits,
    render_huge_anchor_model,
)
from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks, huge_blocks_to_bytes
from .residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    unsigned_width_for_max,
)

_FIXED_HEADER_BITS = 32


def encode_block_huge_anchor(
    x: int,
    width_bits: int,
    model: HugeAnchorModel,
    max_index: int | None = None,
    search_radius: int = 0,
) -> dict:
    """Najde najlepsi index pre zvolenu anchor family alebo vrati escape."""

    _validate_width_bits(width_bits)
    _validate_block_value(x, width_bits)
    if max_index is not None and max_index < 0:
        raise ValueError("max_index must be non-negative")
    if search_radius < 0:
        raise ValueError("search_radius must be non-negative")

    estimated_index = _estimate_index(x, model)
    effective_radius = _effective_search_radius(model, search_radius)
    lower_index = max(0, estimated_index - effective_radius)
    upper_index = estimated_index + effective_radius
    if max_index is not None:
        upper_index = min(upper_index, max_index)

    best: tuple[int, int, int, int] | None = None

    for index in range(lower_index, upper_index + 1):
        anchor = anchor_from_index(index, model, width_bits)
        if anchor is None or anchor > x:
            continue

        diff = x - anchor
        local_cost = unsigned_width_for_max(index) + unsigned_width_for_max(diff)
        candidate = (diff, local_cost, index, anchor)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        return {
            "index": None,
            "anchor": 0,
            "diff": x,
            "escaped": True,
            "estimated_index": estimated_index,
        }

    _, _, index, anchor = best
    return {
        "index": index,
        "anchor": anchor,
        "diff": x - anchor,
        "escaped": False,
        "estimated_index": estimated_index,
    }


def estimate_huge_anchor_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    model: HugeAnchorModel,
    search_radius: int = 0,
) -> dict:
    """Spocita plny MDL-style cost vseobecnej huge-anchor vetvy."""

    _validate_width_bits(width_bits)
    if original_size < 0:
        raise ValueError("original_size must be non-negative")
    if search_radius < 0:
        raise ValueError("search_radius must be non-negative")

    max_decoded_size = len(blocks) * (width_bits // 8)
    if original_size > max_decoded_size:
        raise ValueError("original_size exceeds the decoded block capacity")
    for block in blocks:
        _validate_block_value(int(block), width_bits)

    raw_bits = original_size * 8
    block_count = len(blocks)
    flag_bits = block_count
    encoded_blocks = [encode_block_huge_anchor(int(block), width_bits, model, search_radius=search_radius) for block in blocks]

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
    model_bits = huge_anchor_model_bits(model)
    parameter_bits = huge_anchor_parameter_bits(model)
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
        "model": render_huge_anchor_model(model),
        "search_radius": search_radius,
    }


def encode_huge_anchor_payload(
    data: bytes,
    width_bits: int,
    model: HugeAnchorModel,
    search_radius: int = 0,
) -> dict:
    """Zakoduje data do exact payloadu vseobecnej huge-anchor vetvy."""

    _validate_width_bits(width_bits)
    if search_radius < 0:
        raise ValueError("search_radius must be non-negative")

    payload = bytes(data)
    blocks = bytes_to_huge_blocks(payload, width_bits)
    encoded_blocks = [encode_block_huge_anchor(block, width_bits, model, search_radius=search_radius) for block in blocks]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    residual_codec = choose_best_residual_codec(residuals)

    return {
        "codec": "huge_anchor_index",
        "width_bits": width_bits,
        "original_size": len(payload),
        "block_count": len(blocks),
        "model": {
            "family": model.family,
            "params": dict(model.params),
        },
        "flags": [bool(entry["escaped"]) for entry in encoded_blocks],
        "indices": [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None],
        "raw_blocks": [int(block) for block, entry in zip(blocks, encoded_blocks) if entry["escaped"]],
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "residual_payload": residual_codec.payload,
    }


def decode_huge_anchor_payload(payload: dict) -> bytes:
    """Dekoduje payload huge-anchor vetvy spat na povodne bajty."""

    if payload.get("codec") not in {None, "huge_anchor_index"}:
        raise ValueError("Unsupported huge-anchor payload codec")

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

    raw_model_params = model_payload.get("params")
    if not isinstance(raw_model_params, dict):
        raise ValueError("model.params must be a dict")
    model = HugeAnchorModel(family=str(model_payload.get("family")), params={str(key): int(value) for key, value in raw_model_params.items()})

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
            decoded_blocks.append(int(raw_blocks[raw_position]))
            raw_position += 1
            continue

        if index_position >= len(indices):
            raise ValueError("indices are shorter than non-escape flags")
        if residual_position >= len(residuals):
            raise ValueError("residual stream is shorter than non-escape flags")

        index = int(indices[index_position])
        residual = int(residuals[residual_position])
        index_position += 1
        residual_position += 1

        anchor = anchor_from_index(index, model, width_bits)
        if anchor is None:
            raise ValueError("Stored index cannot reconstruct a valid anchor")
        decoded_blocks.append(anchor + residual)

    if index_position != len(indices):
        raise ValueError("Unused indices remain after decoding")
    if residual_position != len(residuals):
        raise ValueError("Unused residual values remain after decoding")
    if raw_position != len(raw_blocks):
        raise ValueError("Unused raw blocks remain after decoding")

    return huge_blocks_to_bytes(decoded_blocks, width_bits, original_size)


def roundtrip_huge_anchor(
    data: bytes,
    width_bits: int,
    model: HugeAnchorModel,
    search_radius: int = 0,
) -> bytes:
    """Zakoduje a spatne dekoduje data cez huge-anchor payload."""

    return decode_huge_anchor_payload(encode_huge_anchor_payload(bytes(data), width_bits, model, search_radius=search_radius))


def _validate_width_bits(width_bits: int) -> None:
    """Overi, ze sirka blokov patri medzi podporovane huge bloky."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")


def _validate_block_value(x: int, width_bits: int) -> None:
    """Overi rozsah jedneho bloku pre danu sirku."""

    if x < 0 or x >= (1 << width_bits):
        raise ValueError(f"Block out of range for {width_bits} bits: {x}")


def _estimate_index(x: int, model: HugeAnchorModel) -> int:
    """Vrati analyticky odhad indexu pre danu family."""

    family = model.family
    params = model.params

    if family == "linear_shift":
        return x >> params["shift"]
    if family == "affine_shift":
        shifted = x - params["bias"]
        if shifted <= 0:
            return 0
        return shifted >> params["shift"]
    if family == "multiple":
        return x // params["step"]
    if family == "square":
        return isqrt(x)
    if family == "scaled_prime":
        return x >> params["shift"]
    raise ValueError(f"Unsupported huge anchor family: {family}")


def _effective_search_radius(model: HugeAnchorModel, search_radius: int) -> int:
    """Vrati skutocny encoder-side search radius pre kandidata."""

    model_radius = int(model.params.get("search_radius", 0))
    return max(search_radius, model_radius)


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
    """Vrati pomer ceny huge-anchor vetvy voci raw vetve."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
