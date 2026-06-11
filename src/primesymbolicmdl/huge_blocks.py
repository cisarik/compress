"""Pomocne funkcie pre balenie vacsich blokov do Python int."""

from __future__ import annotations

SUPPORTED_HUGE_WIDTHS = {8, 16, 24, 32, 40, 48, 56, 64, 96, 128}


def _width_bytes(width_bits: int) -> int:
    """Vrati sirku bloku v bajtoch alebo vyhodi chybu."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")
    return width_bits // 8


def bytes_to_huge_blocks(data: bytes, width_bits: int) -> list[int]:
    """Prevedie bajty na big-endian bloky a posledny blok nulovo doplni."""

    width_bytes = _width_bytes(width_bits)
    payload = bytes(data)
    if not payload:
        return []

    blocks: list[int] = []
    for start in range(0, len(payload), width_bytes):
        chunk = payload[start : start + width_bytes]
        if len(chunk) < width_bytes:
            chunk = chunk + (b"\x00" * (width_bytes - len(chunk)))
        blocks.append(int.from_bytes(chunk, "big"))
    return blocks


def huge_blocks_to_bytes(blocks: list[int], width_bits: int, original_size: int) -> bytes:
    """Zlozi bloky spat na bajty a oreze nulove doplnenie na povodnu dlzku."""

    if original_size < 0:
        raise ValueError("original_size must be non-negative")

    width_bytes = _width_bytes(width_bits)
    upper_bound = 1 << width_bits
    output = bytearray()

    for block in blocks:
        if int(block) < 0 or int(block) >= upper_bound:
            raise ValueError(f"Block out of range for {width_bits} bits: {block}")
        output.extend(int(block).to_bytes(width_bytes, "big"))

    if original_size > len(output):
        raise ValueError("original_size exceeds decoded byte length")

    return bytes(output[:original_size])
