from primesymbolicmdl.image_datasets import make_gray_image, make_image_dataset
from primesymbolicmdl.simulation import bits_to_bytes_ceil, format_simulation_report, run_gray_image_simulation, run_image_simulation


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
        "raw_bytes",
        "total_bytes_estimate",
        "saving_bytes_estimate",
        "best_model",
        "history",
        "details",
    }

    assert required.issubset(result)


def test_format_simulation_report_returns_readable_text() -> None:
    result = run_image_simulation(
        "Image-predictor",
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
    assert "raw_bytes:" in report
    assert "total_bytes_estimate:" in report
    assert "decision:" in report
    assert "fallback_recommendation:" in report
    assert "residual_codec:" in report
    assert "raw_byte_codec:" in report


def test_gplite_and_soma_both_run_on_tiny_gradient() -> None:
    left = run_image_simulation("GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    right = run_image_simulation("SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert left["status"] == "ok"
    assert right["status"] == "ok"


def test_image_gplite_and_image_soma_run_on_tiny_gradient() -> None:
    left = run_image_simulation("Image-GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    right = run_image_simulation("Image-SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert left["status"] == "ok"
    assert right["status"] == "ok"
    assert left["details"]["residual_codec"] == "fixed_signed"
    assert right["details"]["residual_codec"] == "fixed_signed"


def test_image_gplite_simulation_accepts_primitive_set_metadata() -> None:
    result = run_image_simulation(
        "Image-GP-lite",
        "checker",
        8,
        8,
        population_size=8,
        generations=4,
        max_index=7,
        image_gplite_primitive_set="structure",
    )

    assert result["status"] == "ok"
    assert result["details"]["resolved_primitive_set"] == "structure"
    assert "primitive_set:" in format_simulation_report(result)


def test_image_predictor_runs_on_tiny_gradient() -> None:
    result = run_image_simulation("Image-predictor", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert result["status"] == "ok"
    assert result["best_model"] == "x_ramp"
    assert result["details"]["residual_codec"] == "fixed_signed"
    assert result["details"]["raw_byte_codec"] in {"raw_bytes", "byte_rle"}
    assert result["preview"]["roundtrip_ok"] is True


def test_gp_placeholder_returns_not_implemented() -> None:
    result = run_image_simulation("GP", "gradient", 8, 8, population_size=8, generations=4, max_index=7)

    assert result["status"] == "not_implemented"


def test_bits_to_bytes_ceil_rounds_up() -> None:
    assert bits_to_bytes_ceil(0) == 0
    assert bits_to_bytes_ceil(8) == 1
    assert bits_to_bytes_ceil(9) == 2


def test_run_gray_image_simulation_accepts_external_image() -> None:
    image = make_gray_image("external", 4, 4, bytes(range(16)))
    result = run_gray_image_simulation(
        "GP-lite",
        image,
        population_size=8,
        generations=4,
        max_index=7,
    )

    assert result["dataset_name"] == "external"
    assert result["image_width"] == 4
    assert result["image_height"] == 4
    assert result["details"]["raw_byte_codec"] in {"raw_bytes", "byte_rle"}


def test_law_based_preview_roundtrips_for_gplite_and_soma() -> None:
    gplite_result = run_image_simulation("GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    soma_result = run_image_simulation("SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    original = make_image_dataset("gradient", 8, 8, 1234)

    for result in (gplite_result, soma_result):
        preview = result["preview"]
        assert preview["roundtrip_ok"] is True
        assert preview["decoded_image"].pixels == original.pixels
        assert len(preview["residual_image"].pixels) == 64


def test_image_predictor_preview_roundtrips_for_gradient() -> None:
    result = run_image_simulation("Image-predictor", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    original = make_image_dataset("gradient", 8, 8, 1234)
    preview = result["preview"]

    assert preview["anchor_label"] == "Predictor"
    assert preview["residual_label"] == "Residuals+128"
    assert preview["decoded_image"].pixels == original.pixels


def test_image_gplite_preview_roundtrips_for_gradient() -> None:
    result = run_image_simulation("Image-GP-lite", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    original = make_image_dataset("gradient", 8, 8, 1234)
    preview = result["preview"]

    assert preview["roundtrip_ok"] is True
    assert preview["decoded_image"].pixels == original.pixels


def test_image_soma_preview_roundtrips_for_gradient() -> None:
    result = run_image_simulation("Image-SOMA", "gradient", 8, 8, population_size=8, generations=4, max_index=7)
    original = make_image_dataset("gradient", 8, 8, 1234)
    preview = result["preview"]

    assert preview["roundtrip_ok"] is True
    assert preview["decoded_image"].pixels == original.pixels
