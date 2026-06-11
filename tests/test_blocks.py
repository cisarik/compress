import pytest

from primesymbolicmdl.blocks import bytes_to_uint_blocks, uint_blocks_to_bytes


@pytest.mark.parametrize("width_bits", [8, 16, 24, 32])
def test_blocks_roundtrip_supported_widths(width_bits: int) -> None:
    data = bytes(range(1, 40))
    blocks = bytes_to_uint_blocks(data, width_bits)

    assert uint_blocks_to_bytes(blocks, width_bits, len(data)) == data


def test_blocks_roundtrip_empty_bytes() -> None:
    assert bytes_to_uint_blocks(b"", 16) == []
    assert uint_blocks_to_bytes([], 16, 0) == b""


@pytest.mark.parametrize(
    ("width_bits", "data"),
    [
        (8, b"\x01\x02\x03"),
        (16, b"\x01"),
        (24, b"\x01\x02\x03\x04"),
        (32, b"\x10\x20\x30"),
    ],
)
def test_blocks_roundtrip_non_multiple_sizes(width_bits: int, data: bytes) -> None:
    blocks = bytes_to_uint_blocks(data, width_bits)

    assert uint_blocks_to_bytes(blocks, width_bits, len(data)) == data


def test_unsupported_width_raises() -> None:
    with pytest.raises(ValueError):
        bytes_to_uint_blocks(b"\x00", 12)
