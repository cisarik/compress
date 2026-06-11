"""Headless simulacia optimizerov nad malymi grayscale datasetmi."""

from __future__ import annotations

from .image_datasets import GrayImage, make_gray_image, make_image_dataset
from .image_law_branch import build_image_law_trace, decode_image_law_payload
from .image_predictor_branch import build_image_predictor_trace, decode_image_predictor_payload
from .index_branch import encode_block_with_law, roundtrip_law_payload
from .optimizers import OptimizerRequest, run_optimizer
from .optimizers.image_soma import build_image_soma_trace, decode_image_soma_payload
from .residual_codecs import choose_best_byte_codec


def bits_to_bytes_ceil(bit_count: int) -> int:
    """Prevedie bitovy odhad na konzervativny pocet bajtov."""

    if bit_count < 0:
        raise ValueError("bit_count must be non-negative")
    return (bit_count + 7) // 8


def run_gray_image_simulation(
    optimizer_name: str,
    image: GrayImage,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 20,
    max_index: int | None = None,
    strict_lower: bool = False,
    image_gplite_primitive_set: str | None = None,
) -> dict:
    """Spusti vybrany optimizer nad konkretnym grayscale obrazkom."""

    metadata = {
        "image_width": image.width,
        "image_height": image.height,
        "dataset_name": image.name,
    }
    if image_gplite_primitive_set is not None:
        metadata["image_gplite_primitive_set"] = image_gplite_primitive_set

    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=seed,
        population_size=population_size,
        generations=generations,
        max_index=max_index,
        strict_lower=strict_lower,
        metadata=metadata,
    )
    result = run_optimizer(optimizer_name, request)
    details = dict(result.details)
    best_cost = details.get("best_cost")
    if isinstance(best_cost, dict):
        for key in ("residual_bits", "residual_codec", "residual_codec_details"):
            if key not in details and key in best_cost:
                details[key] = best_cost[key]
    raw_byte_codec = choose_best_byte_codec(image.pixels)
    details["raw_byte_codec"] = raw_byte_codec.codec_name
    details["raw_byte_codec_bits"] = raw_byte_codec.bits
    details["raw_byte_codec_ratio_vs_raw"] = _ratio(raw_byte_codec.bits, result.raw_bits)
    details["raw_byte_codec_details"] = dict(raw_byte_codec.details)
    preview = build_result_preview(image, details)
    raw_bytes = len(image.pixels)
    total_bytes_estimate = bits_to_bytes_ceil(result.total_bits)
    saving_bytes_estimate = raw_bytes - total_bytes_estimate
    payload = {
        "optimizer_name": result.optimizer_name,
        "status": result.status,
        "dataset_name": image.name,
        "image_width": image.width,
        "image_height": image.height,
        "raw_bits": result.raw_bits,
        "total_bits": result.total_bits,
        "saving_bits": result.saving_bits,
        "ratio_vs_raw": result.ratio_vs_raw,
        "raw_bytes": raw_bytes,
        "total_bytes_estimate": total_bytes_estimate,
        "saving_bytes_estimate": saving_bytes_estimate,
        "best_model": result.best_model,
        "history": result.history,
        "details": details,
    }
    if preview is not None:
        payload["preview"] = preview
    return payload


def run_image_simulation(
    optimizer_name: str,
    dataset_name: str = "gradient",
    image_width: int = 32,
    image_height: int = 32,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 20,
    max_index: int | None = None,
    strict_lower: bool = False,
    image_gplite_primitive_set: str | None = None,
) -> dict:
    """Spusti vybrany optimizer nad generovanym grayscale datasetom."""

    image = make_image_dataset(dataset_name, image_width, image_height, seed)
    return run_gray_image_simulation(
        optimizer_name,
        image,
        seed=seed,
        population_size=population_size,
        generations=generations,
        max_index=max_index,
        strict_lower=strict_lower,
        image_gplite_primitive_set=image_gplite_primitive_set,
    )


def build_result_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati preview pre law-based alebo image-predictor branch."""

    preview = build_law_image_preview(image, details)
    if preview is not None:
        return preview
    preview = build_image_law_preview(image, details)
    if preview is not None:
        return preview
    preview = build_image_soma_preview(image, details)
    if preview is not None:
        return preview
    return build_image_predictor_preview(image, details)


def build_law_image_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati anchor, residual a decoded preview pre law-based vysledok."""

    decoder_model = details.get("decoder_model")
    max_index = details.get("max_index")
    if decoder_model is None or not isinstance(max_index, int):
        return None

    strict_lower = bool(details.get("strict_lower", False))
    encoded = [
        encode_block_with_law(pixel, decoder_model, max_index, strict_lower)
        for pixel in image.pixels
    ]
    anchor_pixels = bytes(entry["anchor"] for entry in encoded)
    residual_pixels = bytes(entry["residual"] for entry in encoded)
    decoded_pixels = roundtrip_law_payload(image.pixels, 8, decoder_model, max_index, strict_lower)
    return {
        "anchor_image": make_gray_image(f"{image.name}:anchors", image.width, image.height, anchor_pixels),
        "residual_image": make_gray_image(f"{image.name}:residuals", image.width, image.height, residual_pixels),
        "decoded_image": make_gray_image(f"{image.name}:decoded", image.width, image.height, decoded_pixels),
        "anchor_label": "Anchors",
        "residual_label": "Residuals",
        "escaped_count": sum(1 for entry in encoded if entry["escaped"]),
        "min_residual": min(residual_pixels, default=0),
        "max_residual": max(residual_pixels, default=0),
        "roundtrip_ok": decoded_pixels == image.pixels,
    }


def build_image_predictor_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati predictor, residual a decoded preview pre image predictor."""

    model = details.get("predictor_model")
    if model is None:
        return None

    trace = build_image_predictor_trace(image, model)
    payload = details.get("payload")
    if isinstance(payload, dict):
        decoded_pixels = decode_image_predictor_payload(payload)
    else:
        decoded_pixels = trace["decoded_pixels"]

    residual_visual = bytes(_signed_residual_to_visual(value) for value in trace["residuals"])
    return {
        "anchor_image": make_gray_image(f"{image.name}:predictor", image.width, image.height, trace["predicted_pixels"]),
        "residual_image": make_gray_image(f"{image.name}:residuals", image.width, image.height, residual_visual),
        "decoded_image": make_gray_image(f"{image.name}:decoded", image.width, image.height, decoded_pixels),
        "anchor_label": "Predictor",
        "residual_label": "Residuals+128",
        "escaped_count": 0,
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "roundtrip_ok": decoded_pixels == image.pixels,
    }


def build_image_law_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati predictor, residual a decoded preview pre image-law branch."""

    law = details.get("image_law_model")
    if law is None:
        return None

    trace = build_image_law_trace(image, law)
    payload = details.get("payload")
    if isinstance(payload, dict):
        decoded_pixels = decode_image_law_payload(payload)
    else:
        decoded_pixels = trace["decoded_pixels"]

    residual_visual = bytes(_signed_residual_to_visual(value) for value in trace["residuals"])
    return {
        "anchor_image": make_gray_image(f"{image.name}:predictor_law", image.width, image.height, trace["predicted_pixels"]),
        "residual_image": make_gray_image(f"{image.name}:residuals", image.width, image.height, residual_visual),
        "decoded_image": make_gray_image(f"{image.name}:decoded", image.width, image.height, decoded_pixels),
        "anchor_label": "Predictor law",
        "residual_label": "Residuals+128",
        "escaped_count": 0,
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "roundtrip_ok": decoded_pixels == image.pixels,
    }


def build_image_soma_preview(image: GrayImage, details: dict) -> dict | None:
    """Vrati predictor, residual a decoded preview pre fixed-point Image-SOMA."""

    model = details.get("image_soma_model")
    if model is None:
        return None

    trace = build_image_soma_trace(image, model)
    payload = details.get("payload")
    if isinstance(payload, dict):
        decoded_pixels = decode_image_soma_payload(payload)
    else:
        decoded_pixels = trace["decoded_pixels"]

    residual_visual = bytes(_signed_residual_to_visual(value) for value in trace["residuals"])
    return {
        "anchor_image": make_gray_image(f"{image.name}:predictor_soma", image.width, image.height, trace["predicted_pixels"]),
        "residual_image": make_gray_image(f"{image.name}:residuals", image.width, image.height, residual_visual),
        "decoded_image": make_gray_image(f"{image.name}:decoded", image.width, image.height, decoded_pixels),
        "anchor_label": "Predictor soma",
        "residual_label": "Residuals+128",
        "escaped_count": 0,
        "min_residual": trace["min_residual"],
        "max_residual": trace["max_residual"],
        "roundtrip_ok": decoded_pixels == image.pixels,
    }


def format_simulation_report(result: dict) -> str:
    """Vrati citatelny textovy report pre CLI alebo GUI."""

    details = result.get("details", {})
    lines = [
        f"optimizer: {result['optimizer_name']}",
        f"status: {result['status']}",
        f"dataset: {result['dataset_name']} ({result['image_width']}x{result['image_height']})",
        f"raw_bits: {result['raw_bits']}",
        f"total_bits: {result['total_bits']}",
        f"saving_bits: {result['saving_bits']}",
        f"raw_bytes: {result.get('raw_bytes', bits_to_bytes_ceil(result['raw_bits']))}",
        f"total_bytes_estimate: {result.get('total_bytes_estimate', bits_to_bytes_ceil(result['total_bits']))}",
        f"saving_bytes_estimate: {result.get('saving_bytes_estimate', 0)}",
        f"ratio_vs_raw: {result['ratio_vs_raw']:.3f}",
        f"best_model: {result['best_model']}",
    ]
    if result["total_bits"] < result["raw_bits"]:
        lines.append("decision: WIN beats raw under current accounting")
    else:
        lines.append("decision: use raw fallback; current model loses to raw")
    would_use_fallback = details.get("would_use_fallback")
    if not isinstance(would_use_fallback, bool):
        would_use_fallback = result["total_bits"] >= result["raw_bits"]
    lines.append(
        "fallback_recommendation: "
        + ("use_raw_fallback" if would_use_fallback else "use_model_under_current_accounting")
    )
    history = result.get("history", [])
    if history:
        lines.append("history:")
        for item in history[:5]:
            best_label = item.get("best_law") or item.get("best_model") or "n/a"
            lines.append(
                f"  gen={item.get('generation', '?')} total_bits={item.get('total_bits', '?')} "
                f"saving_bits={item.get('saving_bits', '?')} best={best_label}"
            )
    if details.get("message"):
        lines.append(f"note: {details['message']}")
    if details.get("note"):
        lines.append(f"note: {details['note']}")
    if details.get("primitive_set"):
        primitive_label = str(details["primitive_set"])
        resolved = details.get("resolved_primitive_set")
        if isinstance(resolved, str) and resolved != primitive_label:
            primitive_label = f"{primitive_label} -> {resolved}"
        lines.append(f"primitive_set: {primitive_label}")
    if details.get("residual_codec"):
        lines.append(f"residual_codec: {details['residual_codec']}")
    if details.get("residual_bits") is not None:
        lines.append(f"residual_bits: {details['residual_bits']}")
    if details.get("raw_byte_codec"):
        lines.append(f"raw_byte_codec: {details['raw_byte_codec']}")
        lines.append(f"raw_byte_codec_bits: {details['raw_byte_codec_bits']}")
        lines.append(f"raw_byte_codec_ratio_vs_raw: {details['raw_byte_codec_ratio_vs_raw']:.3f}")
    preview = result.get("preview")
    if isinstance(preview, dict):
        lines.append(f"roundtrip_preview_ok: {preview.get('roundtrip_ok', False)}")
        lines.append(f"escaped_pixels: {preview.get('escaped_count', 0)}")
        lines.append(f"min_residual: {preview.get('min_residual', 0)}")
        lines.append(f"max_residual: {preview.get('max_residual', 0)}")
    return "\n".join(lines)


def _signed_residual_to_visual(value: int) -> int:
    """Prevedie signed residual na zobrazitelny grayscale proxy."""

    return max(0, min(255, int(value) + 128))


def _ratio(total_bits: int, raw_bits: int) -> float:
    """Vrati pomer bitovej ceny voci raw baseline."""

    if raw_bits == 0:
        return 0.0 if total_bits == 0 else float("inf")
    return total_bits / raw_bits
