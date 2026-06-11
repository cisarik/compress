"""Kratke CLI demo pre scaled prime-index branch."""

from __future__ import annotations

from .experiments import dataset_random
from .scaled_prime_search import search_best_scaled_prime_model


def run_demo() -> list[dict]:
    """Spusti malu deterministicku sadu scaled-prime experimentov."""

    datasets = [
        ("ascii_small", b"prime-index-demo", (16, 24, 32, 64)),
        ("ramp_bytes", bytes(range(24)), (16, 24, 32)),
        ("random_bytes", dataset_random(24, seed=1234), (16, 24, 32)),
        ("repeating_pattern", b"ABCDABCDABCDABCD", (16, 24, 32, 64)),
    ]

    results: list[dict] = []
    for dataset_name, data, widths in datasets:
        for width_bits in widths:
            search = search_best_scaled_prime_model(data, width_bits=width_bits)
            results.append(
                {
                    "dataset": dataset_name,
                    "size_bytes": len(data),
                    "width_bits": width_bits,
                    "best_model": search["best_model"],
                    "best_model_string": search["best_model_string"],
                    "raw_bits": search["raw_bits"],
                    "total_bits": search["total_bits"],
                    "saving_bits": search["saving_bits"],
                    "ratio_vs_raw": search["ratio_vs_raw"],
                    "residual_codec": search["residual_codec"],
                    "escape_count": search["escape_count"],
                    "roundtrip_ok": search["roundtrip_ok"],
                    "decision": "win" if search["total_bits"] < search["raw_bits"] else "raw_fallback",
                }
            )
    return results


def format_scaled_prime_result(result: dict) -> str:
    """Vrati stabilny textovy report jedneho demo vysledku."""

    lines = [
        f"dataset: {result['dataset']}",
        f"size_bytes: {result['size_bytes']}",
        f"width_bits: {result['width_bits']}",
        f"best_model: {result['best_model_string']}",
        f"raw_bits: {result['raw_bits']}",
        f"total_bits: {result['total_bits']}",
        f"saving_bits: {result['saving_bits']}",
        f"ratio_vs_raw: {result['ratio_vs_raw']:.3f}" if result["ratio_vs_raw"] != float("inf") else "ratio_vs_raw: inf",
        f"residual_codec: {result['residual_codec']}",
        f"escape_count: {result['escape_count']}",
        f"roundtrip_ok: {result['roundtrip_ok']}",
        f"decision: {result['decision']}",
    ]
    return "\n".join(lines)


def main() -> None:
    """Vypise scaled-prime demo reporty do stdout."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_scaled_prime_result(result))


if __name__ == "__main__":
    main()
