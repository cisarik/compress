"""Lossless 2D image-law branch nad decoder-znamym pixel kontextom."""

from __future__ import annotations

import math

from .image_context_laws import (
    ImageLawNode,
    deserialize_image_law,
    evaluate_image_law,
    image_law_model_bits,
    image_law_parameter_bits,
    render_image_law,
    serialize_image_law,
)
from .image_datasets import GrayImage
from .residual_codecs import (
    choose_best_residual_codec,
    decode_fixed_signed_residual_payload,
    decode_zero_rle_residual_payload,
    signed_width_for_range,
)

_HEADER_BITS = 64


def estimate_image_law_cost(image: GrayImage, law: ImageLawNode) -> dict:
    """Odhadne cenu image-law vetvy pre konkretny grayscale obrazok."""

    trace = build_image_law_trace(image, law)
    raw_bits = image.width * image.height * 8
    model_bits = image_law_model_bits(law)
    parameter_bits = image_law_parameter_bits(law)
    residual_codec = choose_best_residual_codec(trace["residuals"])
    residual_bits = residual_codec.bits
    residual_width = signed_width_for_range(trace["min_residual"], trace["max_residual"])
    total_bits = _HEADER_BITS + model_bits + parameter_bits + residual_bits
    saving_bits = raw_bits - total_bits
    return {
        "raw_bits": raw_bits,
        "model_bits": model_bits,
        "parameter_bits": parameter_bits,
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
        "model": law,
    }


def encode_image_law_payload(image: GrayImage, law: ImageLawNode) -> dict:
    """Zakoduje obrazok cez 2D expression-law prediktor."""

    trace = build_image_law_trace(image, law)
    residual_codec = choose_best_residual_codec(trace["residuals"])
    return {
        "codec": "image_law",
        "width": image.width,
        "height": image.height,
        "law": serialize_image_law(law),
        "residual_codec": residual_codec.codec_name,
        "residual_payload": residual_codec.payload,
        "metadata": {
            "estimated_costs": estimate_image_law_cost(image, law),
            "model_string": render_image_law(law),
            "experimental": True,
        },
    }


def decode_image_law_payload(payload: dict) -> bytes:
    """Dekoduje payload iba z law modelu, rozmerov a residual streamu."""

    width = payload.get("width")
    height = payload.get("height")
    law_payload = payload.get("law")
    residual_codec = payload.get("residual_codec")
    residual_payload = payload.get("residual_payload")
    explicit_residuals = payload.get("residuals")

    if payload.get("codec") not in {None, "image_law"}:
        raise ValueError("Unsupported image law codec")
    if not isinstance(width, int) or width <= 0:
        raise ValueError("width must be a positive integer")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("height must be a positive integer")

    law = deserialize_image_law(law_payload)
    residuals = _decode_residual_stream(residual_codec, residual_payload, explicit_residuals)
    if len(residuals) != width * height:
        raise ValueError("residual count does not match image size")

    decoded: list[int] = []
    for index, residual in enumerate(residuals):
        if not isinstance(residual, int):
            raise ValueError("residuals must contain integers")
        row = index // width
        col = index % width
        context = _build_context(decoded, col, row, width, height)
        prediction = evaluate_image_law(law, context)
        value = prediction + residual
        if value < 0 or value > 255:
            raise ValueError("Decoded pixel is out of grayscale range")
        decoded.append(value)

    return bytes(decoded)


def roundtrip_image_law(image: GrayImage, law: ImageLawNode) -> bytes:
    """Zakoduje a spatne dekoduje obrazok bez straty informacie."""

    return decode_image_law_payload(encode_image_law_payload(image, law))


def build_image_law_trace(image: GrayImage, law: ImageLawNode) -> dict:
    """Vrati predikovane pixely, rezidua a decoded kontrolu pre obrazok."""

    predicted: list[int] = []
    residuals: list[int] = []
    decoded: list[int] = []

    for index, original in enumerate(image.pixels):
        row = index // image.width
        col = index % image.width
        context = _build_context(decoded, col, row, image.width, image.height)
        prediction = evaluate_image_law(law, context)
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
        "model_string": render_image_law(law),
    }


def _build_context(decoded: list[int], col: int, row: int, width: int, height: int) -> dict[str, int]:
    """Posklada decoder-znamy 2D kontext bez pristupu k aktualnemu pixelu."""

    left = decoded[-1] if col > 0 else 0
    up = decoded[(row - 1) * width + col] if row > 0 else 0
    up_left = decoded[(row - 1) * width + col - 1] if row > 0 and col > 0 else 0
    return {
        "col": col,
        "row": row,
        "width": width,
        "height": height,
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


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer total_bits voci raw_bits."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else math.inf
    return total_bits / raw_bits
