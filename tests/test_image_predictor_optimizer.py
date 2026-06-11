from primesymbolicmdl.optimizers import OptimizerRequest, run_optimizer


def test_image_predictor_optimizer_runs_on_gradient_image() -> None:
    width = 8
    height = 8
    pixels = bytes((255 * col) // max(1, width - 1) for _row in range(height) for col in range(width))
    request = OptimizerRequest(
        data=pixels,
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": width, "image_height": height, "dataset_name": "gradient"},
    )

    result = run_optimizer("Image-predictor", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-predictor"
    assert result.best_model == "x_ramp"
    assert result.total_bits < result.raw_bits
    assert result.details["would_use_fallback"] is False
    assert result.details["residual_codec"] == "fixed_signed"


def test_image_predictor_requires_image_metadata() -> None:
    request = OptimizerRequest(
        data=b"\x00\x01\x02\x03",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
    )

    try:
        run_optimizer("Image-predictor", request)
    except ValueError as exc:
        assert "image_width" in str(exc)
    else:
        raise AssertionError("Image-predictor should require image metadata")
