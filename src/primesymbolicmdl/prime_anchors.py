"""Jednoduche deterministicke prvociselne kotvy."""

from __future__ import annotations

from functools import lru_cache
from math import isqrt


def is_prime(n: int) -> bool:
    """Vrati pravdu iba pre prvocisla."""

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    limit = isqrt(n)
    for candidate in range(3, limit + 1, 2):
        if n % candidate == 0:
            return False
    return True


def primes_up_to(n: int) -> list[int]:
    """Vrati zoznam vsetkych prvocisel mensich alebo rovnych n."""

    if n < 2:
        return []

    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"

    for candidate in range(2, isqrt(n) + 1):
        if sieve[candidate]:
            start = candidate * candidate
            count = ((n - start) // candidate) + 1
            sieve[start : n + 1 : candidate] = b"\x00" * count

    return [index for index, flag in enumerate(sieve) if flag]


def _integer_cuberoot(n: int) -> int:
    """Vrati celu tretiu odmocninu zaokruhlenu nadol."""

    if n < 0:
        raise ValueError("n must be non-negative")

    candidate = int(round(n ** (1.0 / 3.0)))
    while (candidate + 1) ** 3 <= n:
        candidate += 1
    while candidate**3 > n:
        candidate -= 1
    return candidate


@lru_cache(maxsize=None)
def _phi(x: int, a: int) -> int:
    """Vrati pocet cisel do x nesudelitelnych prvymi a prvocislami."""

    if a == 0:
        return x
    return _phi(x, a - 1) - _phi(x // _SMALL_PRIMES[a - 1], a - 1)


_SMALL_PRIMES = tuple(primes_up_to(10_000))
_DIRECT_COUNT_LIMIT = 1_000_000


@lru_cache(maxsize=None)
def prime_count(n: int) -> int:
    """Vrati presny pocet prvocisel mensich alebo rovnych n."""

    if n < 2:
        return 0
    if n <= _DIRECT_COUNT_LIMIT:
        return len(primes_up_to(n))

    fourth_root = isqrt(isqrt(n))
    square_root = isqrt(n)
    cube_root = _integer_cuberoot(n)

    a = prime_count(fourth_root)
    b = prime_count(square_root)
    c = prime_count(cube_root)
    primes = primes_up_to(square_root)

    total = _phi(n, a) + ((b + a - 2) * (b - a + 1) // 2)

    for i in range(a + 1, b + 1):
        prime_i = primes[i - 1]
        quotient = n // prime_i
        total -= prime_count(quotient)

        if i <= c:
            quotient_root = isqrt(quotient)
            quotient_root_count = prime_count(quotient_root)
            for j in range(i, quotient_root_count + 1):
                total -= prime_count(quotient // primes[j - 1]) - (j - 1)

    return total


def nearest_lower_prime(n: int) -> int | None:
    """Vrati najblizsie prvocislo zdola alebo None, ak neexistuje."""

    if n < 2:
        return None
    if n == 2:
        return 2

    candidate = n if n % 2 == 1 else n - 1
    while candidate >= 2:
        if is_prime(candidate):
            return candidate
        candidate -= 2
    return None


def nearest_upper_prime(n: int) -> int:
    """Vrati najblizsie prvocislo zhora."""

    if n <= 2:
        return 2
    if n == 3:
        return 3

    candidate = n if n % 2 == 1 else n + 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def nearest_prime(n: int) -> int:
    """Vrati najblizsie prvocislo, pri remize preferuje spodnu kotvu."""

    lower = nearest_lower_prime(n)
    upper = nearest_upper_prime(n)

    if lower is None:
        return upper
    if (n - lower) <= (upper - n):
        return lower
    return upper


def prime_anchor_residual(x: int, mode: str) -> tuple[int, int]:
    """Vrati kotvu a reziduum tak, aby platilo x == kotva + reziduum."""

    if mode == "lower":
        anchor = nearest_lower_prime(x)
        if anchor is None:
            anchor = 2
    elif mode == "upper":
        anchor = nearest_upper_prime(x)
    elif mode == "nearest":
        anchor = nearest_prime(x)
    else:
        raise ValueError(f"Unsupported prime-anchor mode: {mode}")

    return anchor, x - anchor
