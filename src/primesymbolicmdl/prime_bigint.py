"""Deterministicke 64-bit prvociselne utility bez probabilistickych skratiek."""

from __future__ import annotations

from functools import lru_cache

_MAX_UINT64 = 1 << 64
_MR_BASES_64 = (2, 325, 9_375, 28_178, 450_775, 9_780_504, 1_795_265_022)
_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def _validate_uint64_domain(n: int) -> None:
    """Overi, ze vstup patri do podporovaneho 64-bit priestoru."""

    if n >= _MAX_UINT64:
        raise ValueError("Exact prime utilities currently support only n < 2**64.")


@lru_cache(maxsize=131072)
def is_probably_prime_deterministic_64(n: int) -> bool:
    """Vrati presny vysledok pre prvociselnost v rozsahu n < 2**64."""

    if n < 2:
        return False
    _validate_uint64_domain(n)

    if n in _SMALL_PRIMES:
        return True
    for prime in _SMALL_PRIMES:
        if n % prime == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for base in _MR_BASES_64:
        if base % n == 0:
            continue
        witness = pow(base, d, n)
        if witness in {1, n - 1}:
            continue
        for _ in range(s - 1):
            witness = pow(witness, 2, n)
            if witness == n - 1:
                break
        else:
            return False
    return True


@lru_cache(maxsize=131072)
def prev_prime_64(n: int) -> int | None:
    """Vrati najvacsie prvocislo mensie alebo rovne n, inak None."""

    if n < 2:
        return None
    _validate_uint64_domain(n)

    if n == 2:
        return 2

    candidate = n if n % 2 == 1 else n - 1
    while candidate >= 3:
        if is_probably_prime_deterministic_64(candidate):
            return candidate
        candidate -= 2
    return 2


@lru_cache(maxsize=131072)
def next_prime_64(n: int) -> int:
    """Vrati najmensie prvocislo vacsie alebo rovne n v 64-bit priestore."""

    if n <= 2:
        return 2
    _validate_uint64_domain(n)

    candidate = n if n % 2 == 1 else n + 1
    while candidate < _MAX_UINT64:
        if is_probably_prime_deterministic_64(candidate):
            return candidate
        candidate += 2

    raise ValueError("No exact 64-bit prime exists at or above the requested value.")
