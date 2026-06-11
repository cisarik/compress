"""Konzervativne a citatelne bitove odhady pre v0 experiment."""

from __future__ import annotations

import math

from .blocks import SUPPORTED_WIDTHS
from .prime_anchors import prime_anchor_residual, prime_count

# Konzervativny fixny rozpocet pre identifikator transformacie a mod kotvy.
_FIXED_MODEL_BITS = 8
# Konzervativny fixny rozpocet pre experimentalny header chunku vo v0.
_FIXED_HEADER_BITS = 32


def bits_raw(data_size_bytes: int) -> int:
    """Vrati presny pocet bitov pre surove bajty."""

    if data_size_bytes < 0:
        raise ValueError("data_size_bytes must be non-negative")
    return data_size_bytes * 8


def bits_unsigned_range(max_value: int) -> int:
    """Vrati pocet bitov potrebnych pre rozsah od 0 po max_value."""

    if max_value < 0:
        raise ValueError("max_value must be non-negative")
    if max_value == 0:
        return 0
    return math.ceil(math.log2(max_value + 1))


def bits_signed_range(min_value: int, max_value: int) -> int:
    """Vrati pocet bitov potrebnych pre cely podpisany rozsah."""

    if min_value > max_value:
        raise ValueError("min_value must not exceed max_value")

    span = max_value - min_value + 1
    if span <= 1:
        return 0
    return math.ceil(math.log2(span))


def _validate_width_bits(width_bits: int) -> None:
    """Overi, ze sirka blokov patri medzi podporovane hodnoty."""

    if width_bits not in SUPPORTED_WIDTHS:
        raise ValueError(f"Unsupported block width: {width_bits}")


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer celkovej ceny voci raw vetve."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits


def estimate_prime_anchor_cost(
    blocks: list[int],
    width_bits: int,
    original_size: int,
    mode: str,
) -> dict:
    """Odhadne cenu prime-index plus reziduum reprezentacie pre v0 vyskum."""

    _validate_width_bits(width_bits)

    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    max_block_value = 1 << width_bits
    max_decoded_size = len(blocks) * (width_bits // 8)
    if original_size > max_decoded_size:
        raise ValueError("original_size exceeds the decoded block capacity")

    for block in blocks:
        if block < 0 or block >= max_block_value:
            raise ValueError(f"Block out of range for {width_bits} bits: {block}")

    raw_bits = bits_raw(original_size)
    block_count = len(blocks)
    flag_bits = block_count

    anchors: list[int] = []
    residuals: list[int] = []
    escape_count = 0

    for block in blocks:
        if mode == "lower" and block < 2:
            escape_count += 1
            continue

        anchor, residual = prime_anchor_residual(block, mode)
        residuals.append(residual)
        anchors.append(anchor)

    if anchors:
        # Maximalny index je zhodny s poziciou najvacsieho anchoru v utriedenom
        # zozname vsetkych prvocisel do danej hranice, ale nepouzivame jeho
        # plnu materializaciu iba na ucel odhadu sirky indexu.
        max_index = prime_count(max(anchors)) - 1
        index_width = bits_unsigned_range(max_index)
        index_bits = index_width * len(anchors)
    else:
        index_bits = 0

    if residuals:
        residual_width = bits_signed_range(min(residuals), max(residuals))
        residual_bits = residual_width * len(residuals)
    else:
        residual_bits = 0

    escape_bits = width_bits * escape_count
    total_bits = (
        _FIXED_MODEL_BITS
        + _FIXED_HEADER_BITS
        + flag_bits
        + index_bits
        + residual_bits
        + escape_bits
    )

    return {
        "raw_bits": raw_bits,
        "model_bits": _FIXED_MODEL_BITS,
        "header_bits": _FIXED_HEADER_BITS,
        "flag_bits": flag_bits,
        "index_bits": index_bits,
        "residual_bits": residual_bits,
        "escape_bits": escape_bits,
        "total_bits": total_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "escape_count": escape_count,
        "mode": mode,
        "width_bits": width_bits,
        "block_count": block_count,
    }
