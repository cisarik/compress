"""Krátke CLI demo simulacie optimizerov nad obrazkami."""

from __future__ import annotations

from .image_ablation import format_image_ablation_table, run_image_gplite_ablation
from .simulation import format_simulation_report, run_image_simulation


def run_demo() -> list[dict]:
    """Spusti malu sadu rychlych demo behov nad obrazkami."""

    shared = {
        "image_width": 16,
        "image_height": 16,
        "seed": 1234,
        "population_size": 12,
        "generations": 8,
        "max_index": 15,
        "strict_lower": False,
    }
    return [
        run_image_simulation("Image-predictor", dataset_name="gradient", **shared),
        run_image_simulation("Image-GP-lite", dataset_name="gradient", **shared),
        run_image_simulation("Image-SOMA", dataset_name="gradient", **shared),
        run_image_simulation("Image-predictor", dataset_name="checker", **shared),
        run_image_simulation("Image-GP-lite", dataset_name="checker", **shared),
        run_image_simulation("GP-lite", dataset_name="gradient", **shared),
        run_image_simulation("SOMA", dataset_name="gradient", **shared),
    ]


def main() -> None:
    """Vypise reporty pre rychlu sadu obrazkovych demo behov."""

    for index, result in enumerate(run_demo()):
        if index:
            print()
        print(format_simulation_report(result))

    print()
    print("## Image-GP-lite primitive ablation summary: gradient")
    print(format_image_ablation_table(run_image_gplite_ablation("gradient", width=16, height=16, seed=1234, population_size=16, generations=8)))
    print()
    print("## Image-GP-lite primitive ablation summary: checker")
    print(format_image_ablation_table(run_image_gplite_ablation("checker", width=16, height=16, seed=1234, population_size=16, generations=8)))


if __name__ == "__main__":
    main()
