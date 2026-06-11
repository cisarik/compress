"""Deterministicky fixed-point Image-SOMA search nad 2D pixel kontextom."""

from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random

from .base import OptimizerRequest, OptimizerResult
from ..bitcost import bits_unsigned_range
from ..image_datasets import GrayImage, make_gray_image
from ..residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    signed_width_for_range,
)

_HEADER_BITS = 64
_MODEL_BITS = 16
_SCALE = 256
_WEIGHT_BOUNDS = (-512, 512)
_BIAS_BOUNDS = (-65536, 65536)
_PATH_STEPS = ((1, 2), (1, 1), (3, 2))
_PRT = 0.6
_DIMENSION_NAMES = ("w_left", "w_up", "w_up_left", "w_x", "w_y", "w_diag", "bias")


@dataclass(frozen=True)
class ImageSomaModel:
    """Malý fixed-point linear predictor pre grayscale obrazky."""

    w_left: int
    w_up: int
    w_up_left: int
    w_x: int
    w_y: int
    w_diag: int
    bias: int

    def predict(self, context: dict[str, int]) -> int:
        """Vrati clampnutu predikciu iba z decoder-znameho kontextu."""

        total = (
            (self.w_left * context["left"])
            + (self.w_up * context["up"])
            + (self.w_up_left * context["up_left"])
            + (self.w_x * context["x_ramp"])
            + (self.w_y * context["y_ramp"])
            + (self.w_diag * context["diag_ramp"])
            + self.bias
        )
        return _clamp_byte(total // _SCALE)

    def parameter_bits(self) -> int:
        """Vrati konzervativnu cenu vsetkych integer parametrov modelu."""

        values = (
            self.w_left,
            self.w_up,
            self.w_up_left,
            self.w_x,
            self.w_y,
            self.w_diag,
            self.bias,
        )
        return sum(_signed_parameter_bits(value) for value in values)

    def render(self) -> str:
        """Vrati stabilnu textualnu podobu fixed-point modelu."""

        return (
            "image_soma("
            f"w_left={self.w_left}, "
            f"w_up={self.w_up}, "
            f"w_up_left={self.w_up_left}, "
            f"w_x={self.w_x}, "
            f"w_y={self.w_y}, "
            f"w_diag={self.w_diag}, "
            f"bias={self.bias}, "
            f"scale={_SCALE})"
        )

    def as_tuple(self) -> tuple[int, int, int, int, int, int, int]:
        """Vrati model ako stabilny integer vektor."""

        return (
            self.w_left,
            self.w_up,
            self.w_up_left,
            self.w_x,
            self.w_y,
            self.w_diag,
            self.bias,
        )


class ImageSomaOptimizer:
    """Registry adapter pre image-aware fixed-point SOMA search."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "Image-SOMA"

    def available(self) -> bool:
        """Image-SOMA je plne implementovany v tomto repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti maly deterministicky fixed-point SOMA search."""

        width = request.metadata.get("image_width")
        height = request.metadata.get("image_height")
        dataset_name = request.metadata.get("dataset_name", "external")

        if not isinstance(width, int) or width <= 0:
            raise ValueError("Image-SOMA requires positive metadata['image_width']")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Image-SOMA requires positive metadata['image_height']")

        image_name = str(dataset_name) if isinstance(dataset_name, str) else "external"
        image = make_gray_image(image_name, width, height, bytes(request.data))
        search = search_best_image_soma_model(
            image,
            seed=request.seed,
            population_size=request.population_size,
            generations=request.generations,
        )
        best_model = search["best_model"]
        best_cost = search["best_cost"]
        payload = encode_image_soma_payload(image, best_model)
        return OptimizerResult(
            optimizer_name=self.name(),
            status="ok",
            best_model=best_model.render(),
            raw_bits=best_cost["raw_bits"],
            total_bits=best_cost["total_bits"],
            saving_bits=best_cost["saving_bits"],
            ratio_vs_raw=best_cost["ratio_vs_raw"],
            history=search["history"],
            details={
                "image_soma_model": best_model,
                "payload": payload,
                "residual_bits": best_cost["residual_bits"],
                "residual_codec": best_cost["residual_codec"],
                "residual_codec_details": best_cost["residual_codec_details"],
                "min_residual": best_cost["min_residual"],
                "max_residual": best_cost["max_residual"],
                "would_use_fallback": best_cost["total_bits"] >= best_cost["raw_bits"],
                "best_cost": best_cost,
                "scale": _SCALE,
                "search_seed": request.seed,
            },
        )


def estimate_image_soma_cost(image: GrayImage, model: ImageSomaModel) -> dict:
    """Odhadne cenu fixed-point Image-SOMA vetvy pre obrazok."""

    trace = build_image_soma_trace(image, model)
    raw_bits = image.width * image.height * 8
    residual_codec = choose_best_residual_codec(trace["residuals"])
    residual_bits = residual_codec.bits
    residual_width = signed_width_for_range(trace["min_residual"], trace["max_residual"])
    total_bits = _HEADER_BITS + _MODEL_BITS + model.parameter_bits() + residual_bits
    saving_bits = raw_bits - total_bits
    return {
        "raw_bits": raw_bits,
        "model_bits": _MODEL_BITS,
        "parameter_bits": model.parameter_bits(),
        "header_bits": _HEADER_BITS,
        "residual_bits": residual_bits,
        "residual_width": residual_width,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "pixel_count": trace["pixel_count"],
        "model": model,
    }


def encode_image_soma_payload(image: GrayImage, model: ImageSomaModel) -> dict:
    """Zakoduje obrazok cez fixed-point Image-SOMA model."""

    trace = build_image_soma_trace(image, model)
    residual_codec = choose_best_residual_codec(trace["residuals"])
    return {
        "codec": "image_soma",
        "width": image.width,
        "height": image.height,
        "model": {
            "w_left": model.w_left,
            "w_up": model.w_up,
            "w_up_left": model.w_up_left,
            "w_x": model.w_x,
            "w_y": model.w_y,
            "w_diag": model.w_diag,
            "bias": model.bias,
            "scale": _SCALE,
        },
        "residual_codec": residual_codec.codec_name,
        "residual_payload": residual_codec.payload,
        "metadata": {
            "estimated_costs": estimate_image_soma_cost(image, model),
            "model_string": model.render(),
            "experimental": True,
        },
    }


def decode_image_soma_payload(payload: dict) -> bytes:
    """Dekoduje exact-lossless fixed-point Image-SOMA payload."""

    width = payload.get("width")
    height = payload.get("height")
    model_payload = payload.get("model")
    residual_codec = payload.get("residual_codec")
    residual_payload = payload.get("residual_payload")
    explicit_residuals = payload.get("residuals")

    if payload.get("codec") not in {None, "image_soma"}:
        raise ValueError("Unsupported image soma codec")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("height must be a positive integer")
    if not isinstance(model_payload, dict):
        raise ValueError("model must be a dict")

    model = ImageSomaModel(
        w_left=int(model_payload.get("w_left", 0)),
        w_up=int(model_payload.get("w_up", 0)),
        w_up_left=int(model_payload.get("w_up_left", 0)),
        w_x=int(model_payload.get("w_x", 0)),
        w_y=int(model_payload.get("w_y", 0)),
        w_diag=int(model_payload.get("w_diag", 0)),
        bias=int(model_payload.get("bias", 0)),
    )
    residuals = _decode_residual_stream(residual_codec, residual_payload, explicit_residuals)
    if len(residuals) != width * height:
        raise ValueError("residual count does not match image size")

    decoded: list[int] = []
    for index, residual in enumerate(residuals):
        row = index // width
        col = index % width
        context = _build_context(decoded, col, row, width, height)
        prediction = model.predict(context)
        value = prediction + int(residual)
        if value < 0 or value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        decoded.append(value)
    return bytes(decoded)


def roundtrip_image_soma(image: GrayImage, model: ImageSomaModel) -> bytes:
    """Zakoduje a spatne dekoduje obrazok bez straty informacie."""

    return decode_image_soma_payload(encode_image_soma_payload(image, model))


def build_image_soma_trace(image: GrayImage, model: ImageSomaModel) -> dict:
    """Vrati predikcie, rezidua a decoded kontrolu pre dany model."""

    predicted: list[int] = []
    residuals: list[int] = []
    decoded: list[int] = []

    for index, original in enumerate(image.pixels):
        row = index // image.width
        col = index % image.width
        context = _build_context(decoded, col, row, image.width, image.height)
        prediction = model.predict(context)
        residual = int(original) - prediction
        decoded_value = prediction + residual
        if decoded_value < 0 or decoded_value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        predicted.append(prediction)
        residuals.append(residual)
        decoded.append(decoded_value)

    min_residual = min(residuals, default=0)
    max_residual = max(residuals, default=0)
    return {
        "predicted_pixels": bytes(predicted),
        "residuals": residuals,
        "decoded_pixels": bytes(decoded),
        "min_residual": min_residual,
        "max_residual": max_residual,
        "pixel_count": len(image.pixels),
        "model_string": model.render(),
    }


def search_best_image_soma_model(
    image: GrayImage,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 20,
) -> dict:
    """Spusti malu deterministicku fixed-point SOMA search smycku."""

    rng = Random(seed)
    resolved_population = max(1, population_size)
    resolved_generations = max(1, generations)

    population = _initial_population(rng, resolved_population)
    history: list[dict] = []
    best_model: ImageSomaModel | None = None
    best_cost: dict | None = None

    for generation in range(resolved_generations):
        scored = _score_population(population, image)
        leader = scored[0]
        best_model = leader["model"]
        best_cost = leader["cost"]
        history.append(
            {
                "generation": generation,
                "best_model": best_model.render(),
                "total_bits": best_cost["total_bits"],
                "saving_bits": best_cost["saving_bits"],
            }
        )

        elite_count = max(2, min(len(scored), resolved_population // 8 or 1))
        next_population = [item["model"] for item in scored[:elite_count]]
        for item in scored[elite_count:]:
            next_population.append(_migrate_individual(item["model"], best_model, image, rng))

        while len(next_population) < resolved_population:
            next_population.append(_random_model(rng))
        population = next_population[:resolved_population]

    if best_model is None or best_cost is None:
        raise RuntimeError("Image-SOMA did not produce a best candidate")

    return {
        "best_model": best_model,
        "best_cost": best_cost,
        "history": history,
        "generations": resolved_generations,
        "population_size": resolved_population,
        "seed": seed,
    }


def _initial_population(rng: Random, population_size: int) -> list[ImageSomaModel]:
    """Vytvori uvodnu populaciu s rozumnymi fixed-point baseline modelmi."""

    population = [
        ImageSomaModel(0, 0, 0, _SCALE, 0, 0, 0),
        ImageSomaModel(0, 0, 0, 0, _SCALE, 0, 0),
        ImageSomaModel(0, 0, 0, 0, 0, _SCALE, 0),
        ImageSomaModel(_SCALE, 0, 0, 0, 0, 0, 0),
        ImageSomaModel(0, _SCALE, 0, 0, 0, 0, 0),
        ImageSomaModel(_SCALE // 2, _SCALE // 2, 0, 0, 0, 0, 0),
        ImageSomaModel(_SCALE, _SCALE, -_SCALE, 0, 0, 0, 0),
        ImageSomaModel(0, 0, 0, 0, 0, 0, 128 * _SCALE),
    ]
    while len(population) < max(1, population_size):
        population.append(_random_model(rng))
    return population[: max(1, population_size)]


def _score_population(population: list[ImageSomaModel], image: GrayImage) -> list[dict]:
    """Ohodnoti populaciu a utriedi ju podla total_bits."""

    scored = []
    for model in population:
        cost = estimate_image_soma_cost(image, model)
        scored.append({"model": model, "cost": cost})
    scored.sort(key=lambda item: (item["cost"]["total_bits"], -item["cost"]["saving_bits"], item["model"].render()))
    return scored


def _migrate_individual(current: ImageSomaModel, leader: ImageSomaModel, image: GrayImage, rng: Random) -> ImageSomaModel:
    """Presunie jedinca po ceste smerom k liderovi a ponecha najlepsi bod."""

    best_model = current
    best_cost = estimate_image_soma_cost(image, current)
    current_values = list(current.as_tuple())
    leader_values = list(leader.as_tuple())

    for numerator, denominator in _PATH_STEPS:
        mask = _prt_mask(rng, len(current_values))
        candidate_values = []
        for index, (value, target) in enumerate(zip(current_values, leader_values)):
            if mask[index] == 0:
                candidate_values.append(value)
                continue
            delta = target - value
            migrated = value + _round_div(delta * numerator, denominator)
            candidate_values.append(_clip_dimension(index, migrated))
        candidate = _model_from_values(candidate_values)
        candidate_cost = estimate_image_soma_cost(image, candidate)
        if (candidate_cost["total_bits"], candidate.render()) < (best_cost["total_bits"], best_model.render()):
            best_model = candidate
            best_cost = candidate_cost

    if rng.random() < 0.2:
        mutated = _random_perturbation(best_model, rng)
        mutated_cost = estimate_image_soma_cost(image, mutated)
        if (mutated_cost["total_bits"], mutated.render()) < (best_cost["total_bits"], best_model.render()):
            best_model = mutated

    return best_model


def _prt_mask(rng: Random, dimensions: int) -> list[int]:
    """Vrati PRT masku a zaruci aspon jednu aktivnu dimenziu."""

    mask = [1 if rng.random() < _PRT else 0 for _ in range(dimensions)]
    if any(mask):
        return mask
    mask[rng.randrange(dimensions)] = 1
    return mask


def _random_model(rng: Random) -> ImageSomaModel:
    """Vrati nahodny model v povolenych integer hraniciach."""

    return ImageSomaModel(
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_WEIGHT_BOUNDS),
        rng.randint(*_BIAS_BOUNDS),
    )


def _random_perturbation(model: ImageSomaModel, rng: Random) -> ImageSomaModel:
    """Vykona malu lokalnu mutaciu jedneho integer parametra."""

    values = list(model.as_tuple())
    index = rng.randrange(len(values))
    if index < 6:
        values[index] = _clip_dimension(index, values[index] + rng.choice((-64, -32, -16, 16, 32, 64)))
    else:
        values[index] = _clip_dimension(index, values[index] + rng.choice((-4096, -1024, -256, 256, 1024, 4096)))
    return _model_from_values(values)


def _build_context(decoded: list[int], col: int, row: int, width: int, height: int) -> dict[str, int]:
    """Posklada decoder-znamy 2D kontext bez pristupu k aktualnemu pixelu."""

    left = decoded[-1] if col > 0 else 0
    up = decoded[(row - 1) * width + col] if row > 0 else 0
    up_left = decoded[(row - 1) * width + col - 1] if row > 0 and col > 0 else 0
    return {
        "left": left,
        "up": up,
        "up_left": up_left,
        "x_ramp": (255 * col) // max(1, width - 1),
        "y_ramp": (255 * row) // max(1, height - 1),
        "diag_ramp": (255 * (col + row)) // max(1, width + height - 2),
    }


def _decode_residual_stream(
    residual_codec: object,
    residual_payload: object,
    explicit_residuals: object,
) -> list[int]:
    """Dekoduje residual stream z codec payloadu alebo zo starsieho fallback pola."""

    if isinstance(explicit_residuals, list):
        if not all(isinstance(value, int) for value in explicit_residuals):
            raise ValueError("residuals must contain integers")
        return [int(value) for value in explicit_residuals]

    if not isinstance(residual_codec, str):
        raise ValueError("residual_codec must be a string")
    if not isinstance(residual_payload, dict):
        raise ValueError("residual_payload must be a dict")
    if residual_codec == "fixed_signed":
        return decode_fixed_signed_residual_payload(residual_payload)
    if residual_codec == "zero_rle":
        return decode_zero_rle_residual_payload(residual_payload)
    raise ValueError(f"Unsupported residual codec: {residual_codec}")


def _model_from_values(values: list[int]) -> ImageSomaModel:
    """Posklada immutable model z integer zoznamu."""

    return ImageSomaModel(*[int(value) for value in values])


def _clip_dimension(index: int, value: int) -> int:
    """Oreze jednu dimenziu vektora na jej povoleny rozsah."""

    if index < 6:
        return max(_WEIGHT_BOUNDS[0], min(_WEIGHT_BOUNDS[1], int(value)))
    return max(_BIAS_BOUNDS[0], min(_BIAS_BOUNDS[1], int(value)))


def _round_div(value: int, divisor: int) -> int:
    """Zaokruhli integer po deleni smerom k najblizsiemu celemu."""

    if divisor <= 0:
        raise ValueError("divisor must be positive")
    if value >= 0:
        return (value + (divisor // 2)) // divisor
    return -(((-value) + (divisor // 2)) // divisor)


def _signed_parameter_bits(value: int) -> int:
    """Vrati konzervativnu bitovu cenu jedneho podpisaneho parametra."""

    if value == 0:
        return 1
    return 1 + bits_unsigned_range(abs(int(value)))


def _clamp_byte(value: int) -> int:
    """Oreze lubovolne cele cislo na grayscale rozsah."""

    return max(0, min(255, int(value)))


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer total_bits voci raw_bits."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
