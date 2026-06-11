import random

from primesymbolicmdl.codec import compress_experimental, decompress_experimental


def _u16_bytes(values: list[int]) -> bytes:
    return b"".join(value.to_bytes(2, "big") for value in values)


def test_codec_roundtrip_empty_data() -> None:
    data = b""
    payload = compress_experimental(data)

    assert payload["codec"] == "raw"
    assert decompress_experimental(payload) == data


def test_codec_roundtrip_short_ascii_data() -> None:
    data = b"PrimeSymbolicMDL"
    payload = compress_experimental(data, width_bits=8)

    assert decompress_experimental(payload) == data


def test_codec_roundtrip_deterministic_random_bytes() -> None:
    rng = random.Random(1234)
    data = bytes(rng.randrange(256) for _ in range(513))
    payload = compress_experimental(data, width_bits=16)

    assert decompress_experimental(payload) == data


def test_codec_roundtrip_structured_integer_like_bytes() -> None:
    values = [2, 3, 5, 7, 11, 13, 17, 19] * 8
    data = _u16_bytes(values)
    payload = compress_experimental(data, width_bits=16, mode="nearest")

    assert payload["codec"] == "prime_anchor"
    assert payload["metadata"]["estimated_costs"]["total_bits"] < payload["metadata"]["estimated_costs"]["raw_bits"]
    assert decompress_experimental(payload) == data
