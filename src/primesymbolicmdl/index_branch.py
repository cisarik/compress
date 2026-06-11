"""Indexova vetva pre zakon A(i) plus reziduum."""

from __future__ import annotations

import math

from .anchor_laws import LawNode, anchor_value, law_model_bits, law_parameter_bits, render_law
from .bitcost import bits_raw, bits_signed_range, bits_unsigned_range
from .blocks import SUPPORTED_WIDTHS, bytes_to_uint_blocks, uint_blocks_to_bytes

_FIXED_HEADER_BITS = 32


def encode_block_with_law(x: int, law, max_index: int, strict_lower: bool = False) -> dict:
    """Najde najlepsi index pre anchor zakon alebo vrati escape."""

    if x < 0:
        raise ValueError("x must be non-negative")
    if max_index < 0:
        raise ValueError("max_index must be non-negative")

    best: tuple[int, int, int] | None = None

    for index in range(max_index + 1):
        anchor = _anchor_from_law(law, index)
        if not _is_valid_anchor(anchor, x, strict_lower):
            continue

        residual = x - anchor
        candidate = (residual, -anchor, index)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        return {
            "index": None,
            "anchor": 0,
            "residual": x,
            "escaped": True,
        }

    residual, negative_anchor, index = best
    return {
        "index": index,
        "anchor": -negative_anchor,
        "residual": residual,
        "escaped": False,
    }


def estimate_law_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    law,
    max_index: int,
    strict_lower: bool = False,
) -> dict:
    """Spocita odhad ceny indexovej vetvy pre zadany anchor zakon."""

    if width_bits not in SUPPORTED_WIDTHS:
        raise ValueError(f"Unsupported block width: {width_bits}")
    if original_size < 0:
        raise ValueError("original_size must be non-negative")
    if max_index < 0:
        raise ValueError("max_index must be non-negative")

    upper_bound = 1 << width_bits
    max_decoded_size = len(blocks) * (width_bits // 8)
    if original_size > max_decoded_size:
        raise ValueError("original_size exceeds the decoded block capacity")

    for block in blocks:
        if block < 0 or block >= upper_bound:
            raise ValueError(f"Block out of range for {width_bits} bits: {block}")

    raw_bits = bits_raw(original_size)
    block_count = len(blocks)
    flag_bits = block_count
    encoded_blocks = [encode_block_with_law(block, law, max_index, strict_lower) for block in blocks]

    used_indices = [entry["index"] for entry in encoded_blocks if not entry["escaped"]]
    residuals = [entry["residual"] for entry in encoded_blocks if not entry["escaped"]]
    escape_count = sum(1 for entry in encoded_blocks if entry["escaped"])

    if used_indices:
        index_width = bits_unsigned_range(max(int(index) for index in used_indices))
        index_bits = index_width * len(used_indices)
    else:
        index_bits = 0

    if residuals:
        residual_width = bits_signed_range(min(int(value) for value in residuals), max(int(value) for value in residuals))
        residual_bits = residual_width * len(residuals)
    else:
        residual_bits = 0

    model_bits = _law_model_bits(law)
    parameter_bits = _law_parameter_bits(law)
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
        "escape_bits": escape_bits,
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "escape_count": escape_count,
        "block_count": block_count,
        "max_index": max_index,
        "strict_lower": strict_lower,
        "law": _render_law(law),
    }


def roundtrip_law_payload(
    data: bytes,
    width_bits: int,
    law,
    max_index: int,
    strict_lower: bool = False,
) -> bytes:
    """Zakoduje a spatne dekoduje data cez law branch bez straty informacie."""

    blocks = bytes_to_uint_blocks(bytes(data), width_bits)
    decoded_blocks: list[int] = []

    for block in blocks:
        encoded = encode_block_with_law(block, law, max_index, strict_lower)
        if encoded["escaped"]:
            decoded_blocks.append(int(encoded["residual"]))
            continue

        index = encoded["index"]
        if index is None:
            raise ValueError("Non-escaped block must have an index")
        anchor = _anchor_from_law(law, int(index))
        decoded_blocks.append(anchor + int(encoded["residual"]))

    return uint_blocks_to_bytes(decoded_blocks, width_bits, len(data))


def _is_valid_anchor(anchor: int, x: int, strict_lower: bool) -> bool:
    """Overi platnost anchoru pre konkretny blok."""

    if strict_lower:
        return 0 <= anchor < x
    return 0 <= anchor <= x


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer ceny law vetvy voci raw vetve."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits


def _anchor_from_law(law, index: int) -> int:
    """Vrati anchor z GP-lite stromu alebo z ineho kompatibilneho modelu."""

    if isinstance(law, LawNode):
        return anchor_value(law, index)
    if hasattr(law, "anchor_at"):
        return int(law.anchor_at(index))
    raise TypeError("Unsupported law object for anchor evaluation")


def _law_model_bits(law) -> int:
    """Vrati modelovu cenu zakona alebo kompatibilneho modelu."""

    if isinstance(law, LawNode):
        return law_model_bits(law)
    if hasattr(law, "model_bits"):
        return int(law.model_bits())
    raise TypeError("Unsupported law object for model bit accounting")


def _law_parameter_bits(law) -> int:
    """Vrati parameter bit cost zakona alebo kompatibilneho modelu."""

    if isinstance(law, LawNode):
        return law_parameter_bits(law)
    if hasattr(law, "parameter_bits"):
        return int(law.parameter_bits())
    raise TypeError("Unsupported law object for parameter bit accounting")


def _render_law(law) -> str:
    """Vrati stabilnu textualnu reprezentaciu zakona alebo modelu."""

    if isinstance(law, LawNode):
        return render_law(law)
    if hasattr(law, "render"):
        return str(law.render())
    raise TypeError("Unsupported law object for rendering")
