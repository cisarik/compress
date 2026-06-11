import pytest

from primesymbolicmdl.prime_bigint import (
    is_probably_prime_deterministic_64,
    next_prime_64,
    prev_prime_64,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (21, False),
        (2**31 - 1, True),
    ],
)
def test_is_probably_prime_deterministic_64_known_values(value: int, expected: bool) -> None:
    assert is_probably_prime_deterministic_64(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, None),
        (1, None),
        (2, 2),
        (3, 3),
        (4, 3),
        (20, 19),
        (30, 29),
    ],
)
def test_prev_prime_64_returns_expected_values(value: int, expected: int | None) -> None:
    assert prev_prime_64(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 3),
        (4, 5),
        (20, 23),
        (30, 31),
    ],
)
def test_next_prime_64_returns_expected_values(value: int, expected: int) -> None:
    assert next_prime_64(value) == expected


def test_prime_bigint_rejects_values_at_or_above_two_to_the_64() -> None:
    limit = 1 << 64
    with pytest.raises(ValueError):
        is_probably_prime_deterministic_64(limit)
    with pytest.raises(ValueError):
        prev_prime_64(limit)
    with pytest.raises(ValueError):
        next_prime_64(limit)
