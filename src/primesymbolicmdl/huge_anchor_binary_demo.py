"""CLI demo pre skutocne huge-anchor binarne payloady."""

from __future__ import annotations

from .huge_anchor_binary import compress_best_huge_anchor_binary
from .huge_anchor_datasets import make_huge_anchor_dataset


def run_demo() -> list[dict]:
    """Spusti malu deterministicku sadu benchmarkov nad binarnym kontajnerom."""

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
            result = compress_best_huge_anchor_binary(data, width_bits=width_bits, allow_raw_fallback=True)
            results.append(
                {
                    "dataset": dataset_name,
                    **result,
                }
            )
    return results


def format_huge_anchor_binary_result(result: dict) -> str:
    """Vrati stabilny textovy report jedneho binarneho benchmarku."""

    lines = [
        f"dataset: {result['dataset']}",
        f"width_bits: {result['width_bits']}",
        f"estimated_best_model: {result['estimated_best_model_string']} radius={result['estimated_best_search_radius']}",
        f"actual_best_model: {result['best_model_string']} radius={result['search_radius']}",
        f"actual_rerank_changed_winner: {result['actual_rerank_changed_winner']}",
        f"actual_rerank_top_n: {result['actual_rerank_top_n']}",
        f"raw_bytes: {result['raw_bytes']}",
        f"compressed_bytes: {result['compressed_bytes']}",
        f"raw_bits: {result['raw_bits']}",
        f"actual_bits: {result['actual_bits']}",
        f"actual_best_estimated_total_bits: {result['estimated_total_bits']}",
        f"estimated_best_total_bits: {result['estimated_best_total_bits']}",
        f"actual_saving_bytes: {result['actual_saving_bytes']}",
        f"actual_saving_bits: {result['actual_saving_bits']}",
        f"roundtrip_ok: {result['roundtrip_ok']}",
        f"decision: {result['decision']}",
        f"estimated_decision: {result['estimated_decision']}",
        f"residual_codec: {result['residual_codec']}",
        f"escape_count: {result['escape_count']}",
        "actual_top_3_candidates:",
    ]
    for index, candidate in enumerate(result["actual_rerank_candidates"][:3], start=1):
        if candidate["status"] == "ok":
            lines.append(
                f"{index}. {candidate['model']} radius={candidate['search_radius']} compressed_bytes={candidate['compressed_bytes']} "
                f"actual_bits={candidate['actual_bits']} estimated_total_bits={candidate['estimated_total_bits']} decision={candidate['decision']}"
            )
            continue
        lines.append(
            f"{index}. {candidate['model']} radius={candidate['search_radius']} status=error error={candidate.get('error', 'unknown')}"
        )
    return "\n".join(lines)


def main() -> None:
    """Vypise binarny huge-anchor report do stdout."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_huge_anchor_binary_result(result))


if __name__ == "__main__":
    main()
