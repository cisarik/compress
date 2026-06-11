from primesymbolicmdl.image_datasets import make_checker_image, make_gradient_image, make_noise_image
from primesymbolicmdl.optimizers import OptimizerRequest, run_optimizer


def test_image_gplite_runs_on_tiny_gradient_image() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    result = run_optimizer("Image-GP-lite", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-GP-lite"
    assert result.total_bits < result.raw_bits
    assert result.details["residual_codec"] == "fixed_signed"
    assert isinstance(result.details["would_use_fallback"], bool)


def test_image_gplite_is_deterministic_for_same_seed() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=2024,
        population_size=10,
        generations=5,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    left = run_optimizer("Image-GP-lite", request)
    right = run_optimizer("Image-GP-lite", request)

    assert left.best_model == right.best_model
    assert left.total_bits == right.total_bits


def test_image_gplite_accepts_named_primitive_sets() -> None:
    image = make_gradient_image(8, 8)
    for primitive_set in ("local", "ramp", "structure", "full"):
        request = OptimizerRequest(
            data=image.pixels,
            width_bits=8,
            seed=1234,
            population_size=8,
            generations=4,
            max_index=7,
            strict_lower=False,
            metadata={
                "image_width": image.width,
                "image_height": image.height,
                "dataset_name": image.name,
                "image_gplite_primitive_set": primitive_set,
            },
        )
        result = run_optimizer("Image-GP-lite", request)
        assert result.status == "ok"


def test_image_gplite_rejects_unknown_primitive_set() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=7,
        strict_lower=False,
        metadata={
            "image_width": image.width,
            "image_height": image.height,
            "dataset_name": image.name,
            "image_gplite_primitive_set": "mystery",
        },
    )

    try:
        run_optimizer("Image-GP-lite", request)
    except ValueError as exc:
        assert "primitive set" in str(exc)
    else:
        raise AssertionError("Unknown primitive set should raise ValueError")


def test_structure_primitive_set_finds_checker_like_model() -> None:
    image = make_checker_image(8, 8, 4)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=12,
        generations=6,
        max_index=7,
        strict_lower=False,
        metadata={
            "image_width": image.width,
            "image_height": image.height,
            "dataset_name": image.name,
            "image_gplite_primitive_set": "structure",
        },
    )

    result = run_optimizer("Image-GP-lite", request)

    assert result.status == "ok"
    assert "checker_parity" in result.best_model
    assert result.total_bits < result.raw_bits


def test_image_gplite_runs_on_noise_without_promising_a_win() -> None:
    image = make_noise_image(8, 8, 1234)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=1234,
        population_size=10,
        generations=5,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    result = run_optimizer("Image-GP-lite", request)

    assert result.status == "ok"
    assert isinstance(result.best_model, str)
    assert isinstance(result.total_bits, int)
