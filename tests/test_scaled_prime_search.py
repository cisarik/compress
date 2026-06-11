from primesymbolicmdl.scaled_prime_search import search_best_scaled_prime_model


def test_scaled_prime_search_runs_on_tiny_deterministic_data() -> None:
    data = b"\x00\x02\x00\x03\x00\x05\x00\x07"
    result = search_best_scaled_prime_model(data, width_bits=16)

    assert result["best_model_string"]
    assert result["raw_bits"] == len(data) * 8
    assert result["roundtrip_ok"] is True
    assert result["history"]


def test_scaled_prime_search_is_deterministic_for_same_seed() -> None:
    data = b"\x00\x02\x00\x03\x00\x05\x00\x07"
    left = search_best_scaled_prime_model(data, width_bits=16, seed=1234)
    right = search_best_scaled_prime_model(data, width_bits=16, seed=1234)

    assert left["best_model"] == right["best_model"]
    assert left["best_model_string"] == right["best_model_string"]
    assert left["total_bits"] == right["total_bits"]
    assert left["history"] == right["history"]


def test_scaled_prime_search_handles_random_data_without_crashing() -> None:
    data = bytes(range(24))
    result = search_best_scaled_prime_model(data, width_bits=24)

    assert result["roundtrip_ok"] is True
    assert isinstance(result["total_bits"], int)
    assert isinstance(result["saving_bits"], int)


def test_scaled_prime_search_handles_structured_low_range_data() -> None:
    data = (b"\x00\x11" * 8) + (b"\x00\x13" * 8)
    result = search_best_scaled_prime_model(data, width_bits=16)

    assert result["roundtrip_ok"] is True
    assert result["best_model_string"].startswith("scaled_prime(")
