from primesymbolicmdl.bitstream import (
    BitReader,
    BitWriter,
    decode_unsigned_varint,
    encode_unsigned_varint,
    zigzag_decode,
    zigzag_encode,
)


def test_bit_writer_and_reader_use_stable_msb_first_order() -> None:
    writer = BitWriter()
    for bit in (1, 0, 1, 1):
        writer.write_bit(bit)

    payload = writer.to_bytes()

    assert payload == b"\xb0"

    reader = BitReader(payload)
    assert [reader.read_bit() for _ in range(4)] == [1, 0, 1, 1]


def test_write_bits_and_read_bits_roundtrip_for_mixed_widths() -> None:
    values = (
        (0, 0),
        (1, 1),
        (2, 2),
        (5, 3),
        (0xAB, 8),
        (0x1234, 16),
        (0x12345, 20),
    )

    writer = BitWriter()
    for value, width in values:
        writer.write_bits(value, width)

    reader = BitReader(writer.to_bytes())
    decoded = [reader.read_bits(width) for value, width in values]

    assert decoded == [value for value, width in values]


def test_unsigned_varint_roundtrip_is_deterministic() -> None:
    values = [0, 1, 2, 127, 128, 255, 300, 16384, (1 << 32) + 5]

    decoded = []
    for value in values:
        encoded = encode_unsigned_varint(value)
        roundtrip, offset = decode_unsigned_varint(encoded)
        assert offset == len(encoded)
        decoded.append(roundtrip)

    assert encode_unsigned_varint(300) == b"\xac\x02"
    assert decoded == values


def test_zigzag_roundtrip_handles_negative_and_positive_values() -> None:
    values = [-99, -3, -1, 0, 1, 3, 99]

    assert [zigzag_decode(zigzag_encode(value)) for value in values] == values
