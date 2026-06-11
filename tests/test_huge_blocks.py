import random

import pytest

from primesymbolicmdl.huge_blocks import bytes_to_huge_blocks, huge_blocks_to_bytes


@pytest.mark.parametrize("width_bits", [8, 16, 24, 32, 40, 48, 56, 64, 96, 128])
def test_huge_blocks_roundtrip_supported_widths(width_bits: int) -> None:
    data = bytes(range(1, 80))
    blocks = bytes_to_huge_blocks(data, width_bits)

    assert huge_blocks_to_bytes(blocks, width_bits, len(data)) == data


def test_huge_blocks_roundtrip_empty_bytes() -> None:
    assert bytes_to_huge_blocks(b"", 64) == []
    assert huge_blocks_to_bytes([], 64, 0) == b""


@pytest.mark.parametrize(
    ("width_bits", "data"),
    [
        (8, b"\x01\x02\x03"),
        (16, b"\x01"),
        (24, b"\x01\x02\x03\x04"),
        (40, b"\x10\x20\x30"),
        (64, b"\x10\x20\x30\x40\x50"),
        (128, b"\xAA\xBB\xCC"),
    ],
)
def test_huge_blocks_roundtrip_non_multiple_sizes(width_bits: int, data: bytes) -> None:
    blocks = bytes_to_huge_blocks(data, width_bits)

    assert huge_blocks_to_bytes(blocks, width_bits, len(data)) == data


def test_huge_blocks_roundtrip_deterministic_random_bytes() -> None:
    rng = random.Random(1234)
    data = bytes(rng.randrange(256) for _ in range(257))
    blocks = bytes_to_huge_blocks(data, 96)

    assert huge_blocks_to_bytes(blocks, 96, len(data)) == data


def test_huge_blocks_unsupported_width_raises() -> None:
    with pytest.raises(ValueError):
        bytes_to_huge_blocks(b"\x00", 72)
