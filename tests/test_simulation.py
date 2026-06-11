from primesymbolicmdl.simulation import format_simulation_report, run_image_simulation


def test_run_image_simulation_returns_required_fields() -> None:
    result = run_image_simulation(
        "GP-lite",
        dataset_name="gradient",
        image_width=8,
        image_height=8,
        population_size=8,
        generations=4,
        max_index=7,
    )
    required = {
        "optimizer_name",
        "status",
        "dataset_name",
        "image_width",
        "image_height",
        "raw_bits",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "best_model",
        "history",
        "details",
    }

    assert required.issubset(result)


def test_format_simulation_report_returns_readable_text() -> None:
    result = run_image_simulation(
        "GP-lite",
        dataset_name="gradient",
        image_width=8,
        image_height=8,
        population_size=8,
        generations=4,
        max_index=7,
    )
    report = format_simulation_report(result)

    assert "optimizer:" in report
    assert "raw_bits:" in report


def test_gplite_and_soma_both_run_on_tiny_gradient() -> None:
    left = run_image_simulation("GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    right = run_image_simulation("SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert left["status"] == "ok"
    assert right["status"] == "ok"


def test_gp_placeholder_returns_not_implemented() -> None:
    result = run_image_simulation("GP", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert result["status"] == "not_implemented"
