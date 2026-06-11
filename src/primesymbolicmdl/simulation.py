"""Headless simulacia optimizerov nad malymi grayscale datasetmi."""

from __future__ import annotations

from .image_datasets import make_image_dataset
from .optimizers import OptimizerRequest, run_optimizer


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
) -> dict:
    """Spusti vybrany optimizer nad generovanym grayscale datasetom."""

    image = make_image_dataset(dataset_name, image_width, image_height, seed)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=seed,
        population_size=population_size,
        generations=generations,
        max_index=max_index,
        strict_lower=strict_lower,
    )
    result = run_optimizer(optimizer_name, request)
    return {
        "optimizer_name": result.optimizer_name,
        "status": result.status,
        "dataset_name": image.name,
        "image_width": image.width,
        "image_height": image.height,
        "raw_bits": result.raw_bits,
        "total_bits": result.total_bits,
        "saving_bits": result.saving_bits,
        "ratio_vs_raw": result.ratio_vs_raw,
        "best_model": result.best_model,
        "history": result.history,
        "details": dict(result.details),
    }


def format_simulation_report(result: dict) -> str:
    """Vrati citatelny textovy report pre CLI alebo GUI."""

    lines = [
        f"optimizer: {result['optimizer_name']}",
        f"status: {result['status']}",
        f"dataset: {result['dataset_name']} ({result['image_width']}x{result['image_height']})",
        f"raw_bits: {result['raw_bits']}",
        f"total_bits: {result['total_bits']}",
        f"saving_bits: {result['saving_bits']}",
        f"ratio_vs_raw: {result['ratio_vs_raw']:.3f}",
        f"best_model: {result['best_model']}",
    ]
    history = result.get("history", [])
    if history:
        lines.append("history:")
        for item in history[:5]:
            best_label = item.get("best_law") or item.get("best_model") or "n/a"
            lines.append(
                f"  gen={item.get('generation', '?')} total_bits={item.get('total_bits', '?')} "
                f"saving_bits={item.get('saving_bits', '?')} best={best_label}"
            )
    details = result.get("details", {})
    if details.get("message"):
        lines.append(f"note: {details['message']}")
    if details.get("note"):
        lines.append(f"note: {details['note']}")
    return "\n".join(lines)
