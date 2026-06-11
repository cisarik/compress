"""Vseobecne index-plus-diff anchor modely pre vacsie bloky."""

from __future__ import annotations

from dataclasses import dataclass

from .huge_blocks import SUPPORTED_HUGE_WIDTHS
from .prime_bigint import prev_prime_64
from .residual_codecs import unsigned_width_for_max, zigzag_encode

SUPPORTED_HUGE_ANCHOR_FAMILIES = (
    "linear_shift",
    "affine_shift",
    "multiple",
    "square",
    "scaled_prime",
)
_FIXED_MODEL_BITS = 12
_FAMILY_BITS = unsigned_width_for_max(len(SUPPORTED_HUGE_ANCHOR_FAMILIES) - 1)
_MAX_UINT64 = 1 << 64


@dataclass(frozen=True, order=True)
class HugeAnchorModel:
    """Popis jednej anchor family a jej parametrov."""

    family: str
    params: dict[str, int]


def huge_anchor_model_to_dict(model: HugeAnchorModel) -> dict:
    """Vrati stabilny serializovatelny slovnik modelu."""

    normalized = _normalize_model(model)
    return {
        "family": normalized.family,
        "params": dict(normalized.params),
    }


def huge_anchor_model_from_dict(data: dict) -> HugeAnchorModel:
    """Vytvori a znormalizuje model zo slovnikovej reprezentacie."""

    if not isinstance(data, dict):
        raise ValueError("model data must be a dict")

    family = data.get("family")
    params = data.get("params")
    if not isinstance(family, str):
        raise ValueError("model data must contain string family")
    if not isinstance(params, dict):
        raise ValueError("model data must contain dict params")

    normalized_params: dict[str, int] = {}
    for key, value in params.items():
        normalized_params[str(key)] = int(value)
    return _normalize_model(HugeAnchorModel(family=family, params=normalized_params))


def render_huge_anchor_model(model: HugeAnchorModel) -> str:
    """Vrati stabilnu textualnu reprezentaciu anchor modelu."""

    normalized = _normalize_model(model)
    if not normalized.params:
        return normalized.family
    rendered_params = ", ".join(f"{key}={normalized.params[key]}" for key in sorted(normalized.params))
    return f"{normalized.family}({rendered_params})"


def huge_anchor_model_bits(model: HugeAnchorModel) -> int:
    """Vrati fixnu cenu identifikacie vseobecnej huge-anchor vetvy."""

    _normalize_model(model)
    return _FIXED_MODEL_BITS


def huge_anchor_parameter_bits(model: HugeAnchorModel) -> int:
    """Vrati cenu family taga a jej ciselnych parametrov."""

    normalized = _normalize_model(model)
    parameter_bits = _FAMILY_BITS
    for key, value in normalized.params.items():
        if _is_signed_param(normalized.family, key):
            parameter_bits += unsigned_width_for_max(zigzag_encode(value))
        else:
            parameter_bits += unsigned_width_for_max(value)
    return parameter_bits


def anchor_from_index(index: int, model: HugeAnchorModel, width_bits: int) -> int | None:
    """Vrati deterministicky anchor pre dany index alebo None."""

    normalized = _normalize_model(model)
    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")
    if index < 0:
        return None

    anchor: int | None
    if normalized.family == "linear_shift":
        anchor = index << normalized.params["shift"]
    elif normalized.family == "affine_shift":
        anchor = (index << normalized.params["shift"]) + normalized.params["bias"]
    elif normalized.family == "multiple":
        anchor = index * normalized.params["step"]
    elif normalized.family == "square":
        anchor = index * index
    elif normalized.family == "scaled_prime":
        if width_bits > 64:
            return None
        base = index << normalized.params["shift"]
        if base >= _MAX_UINT64:
            return None
        anchor = prev_prime_64(base)
    else:
        raise ValueError(f"Unsupported huge anchor family: {normalized.family}")

    if anchor is None or anchor < 0 or anchor >= (1 << width_bits):
        return None
    return int(anchor)


def _normalize_model(model: HugeAnchorModel) -> HugeAnchorModel:
    """Overi family a vrati normalizovanu kopiu s ocakavanymi parametrami."""

    if model.family not in SUPPORTED_HUGE_ANCHOR_FAMILIES:
        raise ValueError(f"Unsupported huge anchor family: {model.family}")

    raw_params = dict(model.params)

    if model.family == "linear_shift":
        shift = _require_non_negative_int(raw_params, "shift")
        _reject_extra_params(model.family, raw_params, {"shift"})
        return HugeAnchorModel(model.family, {"shift": shift})

    if model.family == "affine_shift":
        shift = _require_non_negative_int(raw_params, "shift")
        bias = _require_int(raw_params, "bias")
        _reject_extra_params(model.family, raw_params, {"shift", "bias"})
        return HugeAnchorModel(model.family, {"shift": shift, "bias": bias})

    if model.family == "multiple":
        step = _require_positive_int(raw_params, "step")
        _reject_extra_params(model.family, raw_params, {"step"})
        return HugeAnchorModel(model.family, {"step": step})

    if model.family == "square":
        _reject_extra_params(model.family, raw_params, set())
        return HugeAnchorModel(model.family, {})

    shift = _require_positive_int(raw_params, "shift")
    search_radius = int(raw_params.pop("search_radius", 0))
    if search_radius < 0:
        raise ValueError("search_radius must be non-negative")
    _reject_extra_params(model.family, raw_params, {"shift", "search_radius"})
    return HugeAnchorModel(model.family, {"shift": shift, "search_radius": search_radius})


def _require_int(params: dict[str, int], key: str) -> int:
    """Vrati integer parameter alebo vyhodi chybu."""

    if key not in params or not isinstance(params[key], int):
        raise ValueError(f"Missing or invalid integer parameter: {key}")
    return int(params[key])


def _require_non_negative_int(params: dict[str, int], key: str) -> int:
    """Vrati nezaporny integer parameter alebo vyhodi chybu."""

    value = _require_int(params, key)
    if value < 0:
        raise ValueError(f"{key} must be non-negative")
    return value


def _require_positive_int(params: dict[str, int], key: str) -> int:
    """Vrati kladny integer parameter alebo vyhodi chybu."""

    value = _require_int(params, key)
    if value <= 0:
        raise ValueError(f"{key} must be positive")
    return value


def _reject_extra_params(family: str, params: dict[str, int], expected: set[str]) -> None:
    """Overi, ze family nedostala necakane parametre."""

    unknown = set(params) - expected
    if unknown:
        raise ValueError(f"Unexpected parameters for {family}: {sorted(unknown)}")


def _is_signed_param(family: str, key: str) -> bool:
    """Vrati pravdu pre parametre, ktore mozu byt podpisane."""

    return family == "affine_shift" and key == "bias"
