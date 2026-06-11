"""Rychle ablation benchmarky pre Image-GP-lite primitive sety."""

from __future__ import annotations

from .simulation import run_image_simulation

_ABLATION_PRIMITIVE_SETS = ("local", "ramp", "structure")


def run_image_gplite_ablation(
    dataset_name: str,
    width: int = 16,
    height: int = 16,
    seed: int = 1234,
    population_size: int = 32,
    generations: int = 10,
) -> list[dict]:
    """Spusti Image-GP-lite nad vsetkymi hlavnymi primitive setmi."""

    rows = []
    for primitive_set in _ABLATION_PRIMITIVE_SETS:
        result = run_image_simulation(
            "Image-GP-lite",
            dataset_name=dataset_name,
            image_width=width,
            image_height=height,
            seed=seed,
            population_size=population_size,
            generations=generations,
            max_index=31,
            strict_lower=False,
            image_gplite_primitive_set=primitive_set,
        )
        preview = result.get("preview", {})
        details = result.get("details", {})
        rows.append(
            {
                "dataset_name": dataset_name,
                "primitive_set": primitive_set,
                "raw_bits": result["raw_bits"],
                "total_bits": result["total_bits"],
                "saving_bits": result["saving_bits"],
                "ratio_vs_raw": result["ratio_vs_raw"],
                "best_model": result["best_model"],
                "residual_codec": details.get("residual_codec", "n/a"),
                "roundtrip_preview_ok": bool(preview.get("roundtrip_ok", False)),
            }
        )
    return rows


def format_image_ablation_table(rows: list[dict]) -> str:
    """Vrati markdown tabulku s vysledkami primitive-set ablationu."""

    header = (
        "| dataset | primitive_set | raw_bits | total_bits | saving_bits | ratio_vs_raw | "
        "best_model | residual_codec | roundtrip_preview_ok |"
    )
    divider = "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |"
    body = [header, divider]
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                [
                    str(row["dataset_name"]),
                    str(row["primitive_set"]),
                    str(row["raw_bits"]),
                    str(row["total_bits"]),
                    str(row["saving_bits"]),
                    f"{float(row['ratio_vs_raw']):.3f}",
                    str(row["best_model"]),
                    str(row["residual_codec"]),
                    str(bool(row["roundtrip_preview_ok"])),
                ]
            )
            + " |"
        )
    return "\n".join(body)


def main() -> None:
    """Vypise rychle markdown tabuľky pre hlavne synteticke datasety."""

    for index, dataset_name in enumerate(("gradient", "diagonal_ramp", "checker")):
        if index:
            print()
        print(f"## Image-GP-lite ablation: {dataset_name}")
        rows = run_image_gplite_ablation(dataset_name, width=16, height=16, seed=1234, population_size=16, generations=8)
        print(format_image_ablation_table(rows))


if __name__ == "__main__":
    main()
