"""Lossless 2D predictor branch pre grayscale obrazky."""

from __future__ import annotations

import math

from .image_datasets import GrayImage
from .image_predictors import (
    ImagePredictorModel,
    image_predictor_model_bits,
    image_predictor_parameter_bits,
    predict_pixel,
    render_image_predictor,
)
from .residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    signed_width_for_range,
)

_HEADER_BITS = 64


def estimate_image_predictor_cost(image: GrayImage, model: ImagePredictorModel) -> dict:
    """Odhadne cenu 2D predictor vetvy pre konkretny grayscale obrazok."""

    trace = build_image_predictor_trace(image, model)
    raw_bits = image.width * image.height * 8
    model_bits = image_predictor_model_bits(model)
    parameter_bits = image_predictor_parameter_bits(model)
    residual_width = signed_width_for_range(trace["min_residual"], trace["max_residual"])
    residual_codec = choose_best_residual_codec(trace["residuals"])
    residual_bits = residual_codec.bits
    total_bits = _HEADER_BITS + model_bits + parameter_bits + residual_bits
    saving_bits = raw_bits - total_bits
    return {
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "parameter_bits": parameter_bits,
        "header_bits": _HEADER_BITS,
        "residual_bits": residual_bits,
        "total_bits": total_bits,
        "saving_bits": saving_bits,
        "ratio_vs_raw": _ratio(total_bits, raw_bits),
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "residual_width": residual_width,
        "residual_codec": residual_codec.codec_name,
        "residual_codec_details": dict(residual_codec.details),
        "pixel_count": trace["pixel_count"],
        "model": model,
    }


def encode_image_predictor_payload(image: GrayImage, model: ImagePredictorModel) -> dict:
    """Zakoduje obrazok cez 2D prediktor a ulozi rezidua."""

    trace = build_image_predictor_trace(image, model)
    residual_codec = choose_best_residual_codec(trace["residuals"])
    return {
        "codec": "image_predictor",
        "width": image.width,
        "height": image.height,
        "model_name": model.name,
        "model_params": dict(model.params),
        "residual_codec": residual_codec.codec_name,
        "residual_payload": residual_codec.payload,
        "metadata": {
            "estimated_costs": estimate_image_predictor_cost(image, model),
            "experimental": True,
        },
    }


def decode_image_predictor_payload(payload: dict) -> bytes:
    """Dekoduje lossless payload iba z modelu, rozmerov a rezidui."""

    width = payload.get("width")
    height = payload.get("height")
    model_name = payload.get("model_name")
    model_params = payload.get("model_params", {})
    residual_codec = payload.get("residual_codec")
    residual_payload = payload.get("residual_payload")
    explicit_residuals = payload.get("residuals")

    if payload.get("codec") not in {None, "image_predictor"}:
        raise ValueError("Unsupported image predictor codec")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("height must be a positive integer")
    if not isinstance(model_name, str):
        raise ValueError("model_name must be a string")
    if not isinstance(model_params, dict):
        raise ValueError("model_params must be a dict")

    model = ImagePredictorModel(model_name, {str(key): int(value) for key, value in model_params.items()})
    residuals = _decode_residual_stream(residual_codec, residual_payload, explicit_residuals)
    if len(residuals) != width * height:
        raise ValueError("residual count does not match image size")
    decoded: list[int] = []

    for index, residual in enumerate(residuals):
        if not isinstance(residual, int):
            raise ValueError("residuals must contain integers")
        row = index // width
        col = index % width
        left = decoded[index - 1] if col > 0 else 0
        up = decoded[index - width] if row > 0 else 0
        up_left = decoded[index - width - 1] if row > 0 and col > 0 else 0
        prediction = predict_pixel(model, col, row, width, height, left, up, up_left)
        value = prediction + residual
        if value < 0 or value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        decoded.append(value)

    return bytes(decoded)


def roundtrip_image_predictor(image: GrayImage, model: ImagePredictorModel) -> bytes:
    """Zakoduje a spatne dekoduje obrazok bez straty informacie."""

    return decode_image_predictor_payload(encode_image_predictor_payload(image, model))


def build_image_predictor_trace(image: GrayImage, model: ImagePredictorModel) -> dict:
    """Vrati predikovane pixely, rezidua a decoded kontrolu pre obrazok."""

    predicted: list[int] = []
    residuals: list[int] = []
    decoded: list[int] = []

    for index, original in enumerate(image.pixels):
        row = index // image.width
        col = index % image.width
        left = decoded[index - 1] if col > 0 else 0
        up = decoded[index - image.width] if row > 0 else 0
        up_left = decoded[index - image.width - 1] if row > 0 and col > 0 else 0
        prediction = predict_pixel(model, col, row, image.width, image.height, left, up, up_left)
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
        "model_string": render_image_predictor(model),
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


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer total_bits voci raw_bits."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
