"""Maly CLI demo beh GP-lite searchu nad zakonmi A(i)."""

from __future__ import annotations

from .experiments import dataset_ramp_u16
from .law_search import search_best_law_for_bytes


def run_demo() -> dict:
    """Spusti maly deterministicky demo search a vrati vysledok."""

    data = dataset_ramp_u16(32)
    result = search_best_law_for_bytes(
        data,
        width_bits=16,
        seed=1234,
        population_size=24,
        generations=10,
        max_depth=4,
        max_index=31,
        strict_lower=False,
    )
    return {
        "dataset_name": "ramp_u16_32",
        "result": result,
    }


def main() -> None:
    """Vypise kratke zhrnutie demo behu."""

    demo = run_demo()
    result = demo["result"]
    print(f"dataset: {demo['dataset_name']}")
    print(f"raw_bits: {result['raw_bits']}")
    print(f"best_total_bits: {result['total_bits']}")
    print(f"saving_bits: {result['saving_bits']}")
    print(f"ratio_vs_raw: {result['ratio_vs_raw']:.3f}")
    print(f"best_law: {result['best_law_string']}")
    print(f"max_index: {result['max_index']}")
    print("history:")
    for item in result["history"][:5]:
        print(
            f"  gen={item['generation']} total_bits={item['total_bits']} "
            f"saving_bits={item['saving_bits']} law={item['best_law']}"
        )


if __name__ == "__main__":
    main()
