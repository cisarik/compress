"""Deterministicke 2D prediktory pre grayscale obrazky."""

from __future__ import annotations

from dataclasses import dataclass, field

from .bitcost import bits_unsigned_range

_CHECKER_BLOCKS = (1, 2, 4, 8, 16)
_MODEL_NAMES = (
    "zero",
    "left",
    "up",
    "avg_left_up",
    "gradient",
    "x_ramp",
    "y_ramp",
    "diagonal_ramp",
    "checker",
)
_MODEL_BITS = bits_unsigned_range(len(_MODEL_NAMES) - 1)


@dataclass(frozen=True)
class ImagePredictorModel:
    """Malý nemenny popis jedneho obrazkoveho prediktora."""

    name: str
    params: dict[str, int] = field(default_factory=dict)


def predict_pixel(
    model: ImagePredictorModel,
    col: int,
    row: int,
    width: int,
    height: int,
    left: int,
    up: int,
    up_left: int,
) -> int:
    """Vrati predikovanu hodnotu pixelu iba z decoder-znameho kontextu."""

    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")

    _validate_model(model)

    if model.name == "zero":
        value = 0
    elif model.name == "left":
        value = left
    elif model.name == "up":
        value = up
    elif model.name == "avg_left_up":
        value = (left + up) // 2
    elif model.name == "gradient":
        value = left + up - up_left
    elif model.name == "x_ramp":
        value = (255 * col) // max(1, width - 1)
    elif model.name == "y_ramp":
        value = (255 * row) // max(1, height - 1)
    elif model.name == "diagonal_ramp":
        value = (255 * (col + row)) // max(1, width + height - 2)
    elif model.name == "checker":
        block = int(model.params["block"])
        value = 255 if ((col // block) + (row // block)) % 2 else 0
    else:
        raise ValueError(f"Unknown image predictor: {model.name}")

    return _clamp_byte(value)


def default_image_predictor_models() -> list[ImagePredictorModel]:
    """Vrati stabilny zoznam malych baseline obrazkovych prediktorov."""

    models = [
        ImagePredictorModel("zero"),
        ImagePredictorModel("left"),
        ImagePredictorModel("up"),
        ImagePredictorModel("avg_left_up"),
        ImagePredictorModel("gradient"),
        ImagePredictorModel("x_ramp"),
        ImagePredictorModel("y_ramp"),
        ImagePredictorModel("diagonal_ramp"),
    ]
    models.extend(ImagePredictorModel("checker", {"block": block}) for block in _CHECKER_BLOCKS)
    return models


def render_image_predictor(model: ImagePredictorModel) -> str:
    """Vrati stabilnu textualnu reprezentaciu modelu."""

    _validate_model(model)
    if not model.params:
        return model.name
    params = ", ".join(f"{key}={model.params[key]}" for key in sorted(model.params))
    return f"{model.name}({params})"


def image_predictor_model_bits(model: ImagePredictorModel) -> int:
    """Vrati konzervativnu cenu identifikatora rodiny modelu."""

    _validate_model(model)
    return _MODEL_BITS


def image_predictor_parameter_bits(model: ImagePredictorModel) -> int:
    """Vrati konzervativnu cenu ciselnych parametrov modelu."""

    _validate_model(model)
    total = 0
    for key in sorted(model.params):
        value = int(model.params[key])
        if value < 0:
            total += 1 + bits_unsigned_range(abs(value))
        else:
            total += bits_unsigned_range(value)
    return total


def _validate_model(model: ImagePredictorModel) -> None:
    """Overi, ze model patri medzi podporovane prediktory."""

    if model.name not in _MODEL_NAMES:
        raise ValueError(f"Unknown image predictor: {model.name}")

    params = dict(model.params)
    if model.name == "checker":
        if set(params) != {"block"}:
            raise ValueError("checker predictor requires exactly one 'block' parameter")
        block = int(params["block"])
        if block not in _CHECKER_BLOCKS:
            raise ValueError(f"Unsupported checker block: {block}")
        return

    if params:
        raise ValueError(f"Predictor {model.name} does not accept parameters")


def _clamp_byte(value: int) -> int:
    """Oreze hodnotu na 8-bitovy grayscale rozsah."""

    return max(0, min(255, int(value)))
