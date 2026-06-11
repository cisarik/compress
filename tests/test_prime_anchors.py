import pytest

from primesymbolicmdl.prime_anchors import (
    is_prime,
    nearest_lower_prime,
    nearest_prime,
    nearest_upper_prime,
    prime_anchor_residual,
    primes_up_to,
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
    ],
)
def test_is_prime_known_values(value: int, expected: bool) -> None:
    assert is_prime(value) is expected


def test_primes_up_to_small_limit() -> None:
    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]


@pytest.mark.parametrize(
    ("value", "lower", "upper", "nearest"),
    [
        (1, None, 2, 2),
        (2, 2, 2, 2),
        (4, 3, 5, 3),
        (8, 7, 11, 7),
        (12, 11, 13, 11),
        (14, 13, 17, 13),
    ],
)
def test_nearest_prime_helpers(value: int, lower: int | None, upper: int, nearest: int) -> None:
    assert nearest_lower_prime(value) == lower
    assert nearest_upper_prime(value) == upper
    assert nearest_prime(value) == nearest


@pytest.mark.parametrize(
    ("value", "mode"),
    [
        (0, "nearest"),
        (1, "lower"),
        (1, "upper"),
        (2, "nearest"),
        (10, "lower"),
        (10, "upper"),
        (10, "nearest"),
        (255, "nearest"),
    ],
)
def test_prime_anchor_residual_reconstructs_exactly(value: int, mode: str) -> None:
    anchor, residual = prime_anchor_residual(value, mode)

    assert is_prime(anchor)
    assert value == anchor + residual
