"""Portfolio search nad viacerymi huge-anchor families."""

from __future__ import annotations

from .huge_anchor_branch import estimate_huge_anchor_cost, roundtrip_huge_anchor
from .huge_anchor_models import HugeAnchorModel, huge_anchor_model_to_dict, render_huge_anchor_model
from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks

_FAMILY_RANK = {
    "linear_shift": 0,
    "multiple": 1,
    "square": 2,
    "affine_shift": 3,
    "scaled_prime": 4,
}


def candidate_huge_anchor_models(width_bits: int) -> list[HugeAnchorModel]:
    """Vrati malu deterministicku mriezku kandidatov pre danu sirku."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")

    models: list[HugeAnchorModel] = []
    shift_values = _general_shift_values(width_bits)
    bias_values = (-16, -1, 0, 1, 16)
    step_values = (2, 3, 4, 5, 7, 8, 16, 31, 64, 127, 256)

    for shift in shift_values:
        models.append(HugeAnchorModel("linear_shift", {"shift": shift}))
    for shift in shift_values:
        for bias in bias_values:
            models.append(HugeAnchorModel("affine_shift", {"shift": shift, "bias": bias}))
    for step in step_values:
        models.append(HugeAnchorModel("multiple", {"step": step}))
    models.append(HugeAnchorModel("square", {}))

    if width_bits <= 64:
        for shift in _scaled_prime_shift_values(width_bits):
            models.append(HugeAnchorModel("scaled_prime", {"shift": shift, "search_radius": 0}))

    return models


def search_best_huge_anchor_model(
    data: bytes,
    width_bits: int = 32,
    search_radius_values: tuple[int, ...] = (0, 1, 2, 4),
    seed: int = 1234,
) -> dict:
    """Vyskusa portfolio huge-anchor families a vrati najlepsi model."""

    del seed

    payload = bytes(data)
    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")
    if not search_radius_values:
        raise ValueError("search_radius_values must not be empty")

    blocks = bytes_to_huge_blocks(payload, width_bits)
    history: list[dict] = []
    best_model: HugeAnchorModel | None = None
    best_cost: dict | None = None
    best_radius = 0
    best_key: tuple[int, int, int, str, int] | None = None

    for model in candidate_huge_anchor_models(width_bits):
        model_string = render_huge_anchor_model(model)
        model_dict = huge_anchor_model_to_dict(model)
        for search_radius in search_radius_values:
            cost = estimate_huge_anchor_cost(blocks, width_bits, len(payload), model, search_radius=search_radius)
            history.append(
                {
                    "family": model.family,
                    "model_dict": dict(model_dict),
                    "model": model_string,
                    "search_radius": search_radius,
                    "total_bits": cost["total_bits"],
                    "saving_bits": cost["saving_bits"],
                    "residual_codec": cost["residual_codec"],
                    "escape_count": cost["escape_count"],
                }
            )
            candidate_key = (
                cost["total_bits"],
                cost["parameter_bits"],
                _FAMILY_RANK[model.family],
                model_string,
                search_radius,
            )
            if best_key is None or candidate_key < best_key:
                best_key = candidate_key
                best_model = model
                best_cost = cost
                best_radius = search_radius

    if best_model is None or best_cost is None:
        raise RuntimeError("Huge-anchor portfolio search did not produce any candidate model")

    ordered_history = sorted(
        history,
        key=lambda row: (row["total_bits"], _FAMILY_RANK[row["family"]], row["model"], row["search_radius"]),
    )
    top_candidates = _top_unique_models(ordered_history, limit=3)
    roundtrip_ok = roundtrip_huge_anchor(payload, width_bits, best_model, search_radius=best_radius) == payload

    return {
        "best_model": best_model,
        "best_model_dict": huge_anchor_model_to_dict(best_model),
        "best_model_string": render_huge_anchor_model(best_model),
        "raw_bits": best_cost["raw_bits"],
        "total_bits": best_cost["total_bits"],
        "saving_bits": best_cost["saving_bits"],
        "ratio_vs_raw": best_cost["ratio_vs_raw"],
        "history": ordered_history,
        "width_bits": width_bits,
        "search_radius": best_radius,
        "roundtrip_ok": roundtrip_ok,
        "decision": "win" if best_cost["total_bits"] < best_cost["raw_bits"] else "raw_fallback",
        "residual_codec": best_cost["residual_codec"],
        "escape_count": best_cost["escape_count"],
        "top_candidates": top_candidates,
    }


def _general_shift_values(width_bits: int) -> tuple[int, ...]:
    """Vrati rozumne, ale obmedzene, shift kandidaty pre linear/affine family."""

    preferred = (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 112, 120)
    return tuple(value for value in preferred if 0 <= value < width_bits)


def _scaled_prime_shift_values(width_bits: int) -> tuple[int, ...]:
    """Vrati mensiu sadu shift kandidatov pre scaled-prime family."""

    if width_bits == 8:
        return (1, 2, 3, 4, 5, 6)
    if width_bits == 16:
        return tuple(range(1, 13))
    if width_bits == 24:
        return (1, 2, 4, 6, 8, 10, 12, 16, 20)
    if width_bits == 32:
        return (1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 28)
    if width_bits == 40:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36)
    if width_bits == 48:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36, 40)
    if width_bits == 56:
        return (4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    if width_bits == 64:
        return (8, 12, 16, 20, 24, 28, 32)
    raise ValueError(f"Scaled-prime family is unsupported for width {width_bits}")


def _top_unique_models(history: list[dict], limit: int) -> list[dict]:
    """Vrati prvych N kandidatov s jedinecnym model stringom."""

    selected: list[dict] = []
    seen_models: set[str] = set()
    for row in history:
        if row["model"] in seen_models:
            continue
        selected.append(row)
        seen_models.add(row["model"])
        if len(selected) >= limit:
            break
    return selected
