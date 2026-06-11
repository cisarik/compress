"""Reverzibilny experimentalny codec s raw fallbackom."""

from __future__ import annotations

from .bitcost import estimate_prime_anchor_cost
from .blocks import bytes_to_uint_blocks, uint_blocks_to_bytes
from .prime_anchors import prime_anchor_residual


def compress_experimental(data: bytes, width_bits: int = 16, mode: str = "nearest") -> dict:
    """Skusi prime-anchor vetvu a inak ulozi data ako raw."""

    raw_bytes = bytes(data)
    blocks = bytes_to_uint_blocks(raw_bytes, width_bits)
    estimated_costs = estimate_prime_anchor_cost(blocks, width_bits, len(raw_bytes), mode)

    metadata = {
        "mode": mode,
        "estimated_costs": estimated_costs,
        "experimental": True,
    }

    if estimated_costs["total_bits"] >= estimated_costs["raw_bits"]:
        return {
            "codec": "raw",
            "width_bits": width_bits,
            "original_size": len(raw_bytes),
            "data": raw_bytes,
            "metadata": metadata,
        }

    anchors: list[int] = []
    residuals: list[int] = []
    for block in blocks:
        anchor, residual = prime_anchor_residual(block, mode)
        anchors.append(anchor)
        residuals.append(residual)

    return {
        "codec": "prime_anchor",
        "width_bits": width_bits,
        "original_size": len(raw_bytes),
        "anchors": anchors,
        "residuals": residuals,
        "metadata": metadata,
    }


def decompress_experimental(payload: dict) -> bytes:
    """Dekoduje raw alebo prime-anchor payload bez straty informacie."""

    codec = payload.get("codec")
    width_bits = payload.get("width_bits")
    original_size = payload.get("original_size")

    if not isinstance(width_bits, int):
        raise ValueError("width_bits must be an integer")
    if not isinstance(original_size, int) or original_size < 0:
        raise ValueError("original_size must be a non-negative integer")

    if codec == "raw":
        raw_bytes = bytes(payload.get("data", b""))
        if len(raw_bytes) != original_size:
            raise ValueError("Raw payload length does not match original_size")
        return raw_bytes

    if codec == "prime_anchor":
        anchors = payload.get("anchors")
        residuals = payload.get("residuals")

        if not isinstance(anchors, list) or not isinstance(residuals, list):
            raise ValueError("Prime-anchor payload must contain anchor and residual lists")
        if len(anchors) != len(residuals):
            raise ValueError("Anchor and residual counts must match")

        blocks = [anchor + residual for anchor, residual in zip(anchors, residuals)]
        return uint_blocks_to_bytes(blocks, width_bits, original_size)

    raise ValueError(f"Unsupported codec: {codec}")
