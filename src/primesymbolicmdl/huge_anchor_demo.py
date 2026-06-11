"""Sirsie CLI porovnanie huge-anchor portfolia a scaled-prime baseline."""

from __future__ import annotations

from .huge_anchor_datasets import make_huge_anchor_dataset
from .huge_anchor_search import search_best_huge_anchor_model
from .scaled_prime_search import search_best_scaled_prime_model


def run_demo() -> list[dict]:
    """Spusti malu deterministicku benchmark sadu nad portfolio branchom."""

    datasets = (
        "linear_shift_generated",
        "square_generated",
        "multiple_generated",
        "random_bytes",
        "ascii_small",
        "repeating_pattern",
    )
    widths = (16, 32, 64)

    results: list[dict] = []
    for dataset_name in datasets:
        for width_bits in widths:
            data = make_huge_anchor_dataset(dataset_name, width_bits, count=32, seed=1234)
            portfolio = search_best_huge_anchor_model(data, width_bits=width_bits)
            scaled_prime = search_best_scaled_prime_model(data, width_bits=width_bits) if width_bits <= 64 else None
            results.append(
                {
                    "dataset": dataset_name,
                    "width_bits": width_bits,
                    "best_model": portfolio["best_model"],
                    "best_model_string": portfolio["best_model_string"],
                    "raw_bits": portfolio["raw_bits"],
                    "total_bits": portfolio["total_bits"],
                    "saving_bits": portfolio["saving_bits"],
                    "ratio_vs_raw": portfolio["ratio_vs_raw"],
                    "residual_codec": portfolio["residual_codec"],
                    "escape_count": portfolio["escape_count"],
                    "roundtrip_ok": portfolio["roundtrip_ok"],
                    "decision": portfolio["decision"],
                    "search_radius": portfolio["search_radius"],
                    "top_candidates": portfolio["top_candidates"],
                    "scaled_prime_baseline": scaled_prime,
                }
            )
    return results


def format_huge_anchor_result(result: dict) -> str:
    """Vrati stabilny textovy report jedneho benchmark behu."""

    ratio = result["ratio_vs_raw"]
    lines = [
        f"dataset: {result['dataset']}",
        f"width_bits: {result['width_bits']}",
        f"best_model: {result['best_model_string']}",
        f"raw_bits: {result['raw_bits']}",
        f"total_bits: {result['total_bits']}",
        f"saving_bits: {result['saving_bits']}",
        f"ratio_vs_raw: {ratio:.3f}" if ratio != float("inf") else "ratio_vs_raw: inf",
        f"residual_codec: {result['residual_codec']}",
        f"escape_count: {result['escape_count']}",
        f"roundtrip_ok: {result['roundtrip_ok']}",
        f"decision: {result['decision']}",
        f"search_radius: {result['search_radius']}",
        "top_3_candidates:",
    ]
    for index, candidate in enumerate(result["top_candidates"], start=1):
        lines.append(
            f"{index}. {candidate['model']} radius={candidate['search_radius']} total_bits={candidate['total_bits']} "
            f"saving_bits={candidate['saving_bits']} residual_codec={candidate['residual_codec']} escapes={candidate['escape_count']}"
        )

    scaled_prime = result.get("scaled_prime_baseline")
    if scaled_prime is None:
        lines.append("scaled_prime_baseline: n/a")
    else:
        lines.append(
            "scaled_prime_baseline: "
            f"{scaled_prime['best_model_string']} total_bits={scaled_prime['total_bits']} "
            f"saving_bits={scaled_prime['saving_bits']} residual_codec={scaled_prime['residual_codec']} "
            f"decision={'win' if scaled_prime['total_bits'] < scaled_prime['raw_bits'] else 'raw_fallback'}"
        )
    return "\n".join(lines)


def main() -> None:
    """Vypise portfolio benchmark reporty do stdout."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_huge_anchor_result(result))


if __name__ == "__main__":
    main()
