import random

from primesymbolicmdl.codec import compress_experimental, decompress_experimental


def test_random_bytes_prefer_raw_fallback() -> None:
    rng = random.Random(1234)
    data = bytes(rng.randrange(256) for _ in range(1024))
    payload = compress_experimental(data, width_bits=16, mode="nearest")

    assert payload["codec"] == "raw"
    assert decompress_experimental(payload) == data
