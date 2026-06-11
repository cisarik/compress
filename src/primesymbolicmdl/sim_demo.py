"""Krátke CLI demo simulacie optimizerov nad obrazkami."""

from __future__ import annotations

from .simulation import format_simulation_report, run_image_simulation


def run_demo() -> list[dict]:
    """Spusti dva male demo behy nad gradientom."""

    shared = {
        "dataset_name": "gradient",
        "image_width": 16,
        "image_height": 16,
        "seed": 1234,
        "population_size": 12,
        "generations": 8,
        "max_index": 15,
        "strict_lower": False,
    }
    return [
        run_image_simulation("GP-lite", **shared),
        run_image_simulation("SOMA", **shared),
    ]


def main() -> None:
    """Vypise reporty pre GP-lite a SOMA."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_simulation_report(result))


if __name__ == "__main__":
    main()
