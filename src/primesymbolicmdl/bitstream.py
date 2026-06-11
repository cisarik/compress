"""Male deterministicke bitstream primitiva pre binarne payloady."""

from __future__ import annotations


class BitWriter:
    """Zapisuje bity po jednom v stabilnom poradi od najvyssieho bitu."""

    def __init__(self) -> None:
        self._buffer = bytearray()
        self._current_byte = 0
        self._bits_in_current = 0
        self._bit_length = 0

    @property
    def bit_length(self) -> int:
        """Vrati pocet uz zapisanych bitov pred paddingom."""

        return self._bit_length

    def write_bit(self, value: int) -> None:
        """Zapise jeden bit do streamu."""

        bit = _coerce_bit(value)
        self._current_byte = (self._current_byte << 1) | bit
        self._bits_in_current += 1
        self._bit_length += 1

        if self._bits_in_current == 8:
            self._buffer.append(self._current_byte)
            self._current_byte = 0
            self._bits_in_current = 0

    def write_bits(self, value: int, width: int) -> None:
        """Zapise `width` bitov z hodnoty v MSB-first poradi."""

        if not isinstance(width, int) or width < 0:
            raise ValueError("width must be a non-negative integer")
        if not isinstance(value, int) or value < 0:
            raise ValueError("value must be a non-negative integer")
        if width == 0:
            if value != 0:
                raise ValueError("value must be zero when width is zero")
            return
        if value >= (1 << width):
            raise ValueError("value does not fit into the requested width")

        for shift in range(width - 1, -1, -1):
            self.write_bit((value >> shift) & 1)

    def write_bool(self, value: bool) -> None:
        """Zapise bool ako jeden bit."""

        self.write_bit(1 if value else 0)

    def to_bytes(self) -> bytes:
        """Vrati aktualny stream doplneny nulami po koniec posledneho bajtu."""

        output = bytearray(self._buffer)
        if self._bits_in_current:
            output.append(self._current_byte << (8 - self._bits_in_current))
        return bytes(output)


class BitReader:
    """Cita bity v rovnakom MSB-first poradi ako `BitWriter` zapisuje."""

    def __init__(self, data: bytes) -> None:
        self._data = bytes(data)
        self._byte_index = 0
        self._bit_index = 0
        self._bits_consumed = 0

    @property
    def bits_consumed(self) -> int:
        """Vrati pocet precitanych bitov."""

        return self._bits_consumed

    def read_bit(self) -> int:
        """Precita jeden bit zo streamu."""

        if self._byte_index >= len(self._data):
            raise ValueError("No more bits remain in the stream")

        current_byte = self._data[self._byte_index]
        bit = (current_byte >> (7 - self._bit_index)) & 1

        self._bit_index += 1
        self._bits_consumed += 1
        if self._bit_index == 8:
            self._byte_index += 1
            self._bit_index = 0

        return bit

    def read_bits(self, width: int) -> int:
        """Precita `width` bitov a vrati ich ako nezapornu hodnotu."""

        if not isinstance(width, int) or width < 0:
            raise ValueError("width must be a non-negative integer")

        value = 0
        for _ in range(width):
            value = (value << 1) | self.read_bit()
        return value

    def read_bool(self) -> bool:
        """Precita jeden bit a vrati ho ako bool."""

        return bool(self.read_bit())


def encode_unsigned_varint(n: int) -> bytes:
    """Zakoduje nezaporne cele cislo do deterministickeho unsigned varintu."""

    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")

    value = n
    output = bytearray()
    while True:
        chunk = value & 0x7F
        value >>= 7
        if value:
            output.append(chunk | 0x80)
            continue
        output.append(chunk)
        return bytes(output)


def decode_unsigned_varint(data: bytes, offset: int = 0) -> tuple[int, int]:
    """Dekoduje unsigned varint zo zadaneho offsetu a vrati novy offset."""

    payload = bytes(data)
    if not isinstance(offset, int) or offset < 0 or offset > len(payload):
        raise ValueError("offset must point inside the input bytes")

    value = 0
    shift = 0
    position = offset

    while position < len(payload):
        byte_value = payload[position]
        position += 1
        value |= (byte_value & 0x7F) << shift
        if not (byte_value & 0x80):
            return value, position
        shift += 7

    raise ValueError("Truncated unsigned varint")


def zigzag_encode(n: int) -> int:
    """Prevedie podpisane cele cislo na nezaporny zigzag tvar."""

    value = int(n)
    return (value << 1) if value >= 0 else ((-value << 1) - 1)


def zigzag_decode(z: int) -> int:
    """Vrati povodne podpisane cele cislo zo zigzag reprezentacie."""

    value = int(z)
    if value < 0:
        raise ValueError("zigzag value must be non-negative")
    if value % 2 == 0:
        return value // 2
    return -((value + 1) // 2)


def _coerce_bit(value: int) -> int:
    """Prevedie vstup na korektny 0/1 bit."""

    if value in {0, False}:
        return 0
    if value in {1, True}:
        return 1
    raise ValueError("bit value must be 0 or 1")
