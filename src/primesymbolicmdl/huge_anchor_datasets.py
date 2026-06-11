"""Kontrolovane datasety pre huge-anchor portfolio experimenty."""

from __future__ import annotations

from .experiments import dataset_random
from .huge_blocks import huge_blocks_to_bytes

_DATASET_NAMES = [
    "linear_shift_generated",
    "square_generated",
    "multiple_generated",
    "random_bytes",
    "ascii_small",
    "repeating_pattern",
]


def get_huge_anchor_dataset_names() -> list[str]:
    """Vrati stabilny zoznam podporovanych nazvov datasetov."""

    return list(_DATASET_NAMES)


def make_huge_anchor_dataset(name: str, width_bits: int, count: int = 32, seed: int = 1234) -> bytes:
    """Vrati jeden deterministicky dataset pre zvolenu sirku a pocet blokov."""

    if count < 0:
        raise ValueError("count must be non-negative")
    width_bytes = width_bits // 8
    total_size = count * width_bytes

    if name == "linear_shift_generated":
        shift = _generated_shift(width_bits)
        blocks = [((index << shift) + _small_positive_diff(index)) % (1 << width_bits) for index in range(count)]
        return huge_blocks_to_bytes(blocks, width_bits, total_size)

    if name == "square_generated":
        blocks = [((index * index) + _small_positive_diff(index)) % (1 << width_bits) for index in range(count)]
        return huge_blocks_to_bytes(blocks, width_bits, total_size)

    if name == "multiple_generated":
        step = _generated_step(width_bits)
        blocks = [((index * step) + _small_positive_diff(index)) % (1 << width_bits) for index in range(count)]
        return huge_blocks_to_bytes(blocks, width_bits, total_size)

    if name == "random_bytes":
        return dataset_random(total_size, seed=seed)

    if name == "ascii_small":
        phrase = b"PrimeSymbolicMDL-huge-anchor-demo|"
        return _repeat_to_length(phrase, total_size)

    if name == "repeating_pattern":
        pattern = b"ABCD"
        return _repeat_to_length(pattern, total_size)

    raise ValueError(f"Unknown huge-anchor dataset: {name}")


def _generated_shift(width_bits: int) -> int:
    """Vrati shift pouzity pre synthetic linear dataset."""

    return max(1, min(8, width_bits // 4))


def _generated_step(width_bits: int) -> int:
    """Vrati step pouzity pre synthetic multiple dataset."""

    del width_bits
    return 31


def _small_positive_diff(index: int) -> int:
    """Vrati malu deterministicku odchylku bez zapornych diffov."""

    return (index * 3) % 3


def _repeat_to_length(pattern: bytes, total_size: int) -> bytes:
    """Opakuje bajtovy vzor na presnu pozadovanu dlzku."""

    if total_size == 0:
        return b""
    repeats = (total_size + len(pattern) - 1) // len(pattern)
    return (pattern * repeats)[:total_size]
