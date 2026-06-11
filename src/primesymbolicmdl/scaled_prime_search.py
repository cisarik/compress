"""Deterministicke hladanie najlepsieho scaled-prime modelu."""

from __future__ import annotations

from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks
from .scaled_prime_index import (
    ScaledPrimeModel,
    estimate_scaled_prime_cost,
    render_scaled_prime_model,
    roundtrip_scaled_prime,
)


def search_best_scaled_prime_model(
    data: bytes,
    width_bits: int = 32,
    shifts: tuple[int, ...] | None = None,
    search_radii: tuple[int, ...] = (0, 1, 2, 4),
    seed: int = 1234,
) -> dict:
    """Vyskusa malu deterministicku mriezku scaled-prime modelov."""

    del seed

    payload = bytes(data)
    _validate_search_width(width_bits)
    if not search_radii:
        raise ValueError("search_radii must not be empty")

    resolved_shifts = shifts if shifts is not None else _default_shifts(width_bits)
    if not resolved_shifts:
        raise ValueError("No shifts are available for the selected width")

    blocks = bytes_to_huge_blocks(payload, width_bits)
    history: list[dict] = []
    best_model: ScaledPrimeModel | None = None
    best_cost: dict | None = None
    best_key: tuple[int, int, int, int] | None = None

    candidate_index = 0
    for shift in resolved_shifts:
        for search_radius in search_radii:
            model = ScaledPrimeModel(shift=shift, direction="lower", search_radius=search_radius)
            cost = estimate_scaled_prime_cost(blocks, width_bits, len(payload), model)
            history.append(
                {
                    "candidate_index": candidate_index,
                    "shift": shift,
                    "search_radius": search_radius,
                    "model": render_scaled_prime_model(model),
                    "total_bits": cost["total_bits"],
                    "saving_bits": cost["saving_bits"],
                    "ratio_vs_raw": cost["ratio_vs_raw"],
                    "escape_count": cost["escape_count"],
                    "residual_codec": cost["residual_codec"],
                }
            )
            candidate_index += 1

            candidate_key = (cost["total_bits"], cost["parameter_bits"], shift, search_radius)
            if best_key is None or candidate_key < best_key:
                best_key = candidate_key
                best_model = model
                best_cost = cost

    if best_model is None or best_cost is None:
        raise RuntimeError("Scaled-prime search did not produce any candidate model")

    roundtrip_ok = roundtrip_scaled_prime(payload, width_bits, best_model) == payload
    return {
        "best_model": best_model,
        "best_model_string": render_scaled_prime_model(best_model),
        "raw_bits": best_cost["raw_bits"],
        "total_bits": best_cost["total_bits"],
        "saving_bits": best_cost["saving_bits"],
        "ratio_vs_raw": best_cost["ratio_vs_raw"],
        "history": history,
        "width_bits": width_bits,
        "roundtrip_ok": roundtrip_ok,
        "residual_codec": best_cost["residual_codec"],
        "escape_count": best_cost["escape_count"],
        "block_count": best_cost["block_count"],
        "cost_details": best_cost,
    }


def _validate_search_width(width_bits: int) -> None:
    """Overi, ze hladanie bezi iba v presne podporovanom rozsahu."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS or width_bits > 64:
        raise ValueError("Scaled-prime search currently supports only exact widths up to 64 bits.")


def _default_shifts(width_bits: int) -> tuple[int, ...]:
    """Vrati rozumne default shift kandidaty pre danu sirku bloku."""

    if width_bits == 8:
        return tuple(range(1, 7))
    if width_bits == 16:
        return tuple(range(1, 13))
    if width_bits == 24:
        return tuple(range(1, 21))
    if width_bits == 32:
        return tuple(range(1, 29))
    if width_bits == 40:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36)
    if width_bits == 48:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36, 40)
    if width_bits == 56:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    if width_bits == 64:
        return (8, 12, 16, 20, 24, 28, 32)
    raise ValueError(f"Unsupported width for default shift selection: {width_bits}")
