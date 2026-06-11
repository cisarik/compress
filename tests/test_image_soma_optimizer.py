from primesymbolicmdl.image_datasets import make_gradient_image, make_noise_image
from primesymbolicmdl.optimizers import OptimizerRequest, run_optimizer
from primesymbolicmdl.optimizers.image_soma import ImageSomaModel


def test_image_soma_runs_on_tiny_gradient_image() -> None:
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

    result = run_optimizer("Image-SOMA", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-SOMA"
    assert result.total_bits < result.raw_bits
    assert result.details["residual_codec"] == "fixed_signed"
    assert isinstance(result.details["would_use_fallback"], bool)


def test_image_soma_is_deterministic_for_same_seed() -> None:
    image = make_gradient_image(8, 8)
    request = OptimizerRequest(
        data=image.pixels,
        width_bits=8,
        seed=2025,
        population_size=10,
        generations=5,
        max_index=7,
        strict_lower=False,
        metadata={"image_width": image.width, "image_height": image.height, "dataset_name": image.name},
    )

    left = run_optimizer("Image-SOMA", request)
    right = run_optimizer("Image-SOMA", request)

    assert left.best_model == right.best_model
    assert left.total_bits == right.total_bits


def test_image_soma_rendering_is_stable() -> None:
    model = ImageSomaModel(256, 0, 0, 256, 0, 0, 0)

    assert (
        model.render()
        == "image_soma(w_left=256, w_up=0, w_up_left=0, w_x=256, w_y=0, w_diag=0, bias=0, scale=256)"
    )


def test_image_soma_runs_on_noise_without_promising_a_win() -> None:
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

    result = run_optimizer("Image-SOMA", request)

    assert result.status == "ok"
    assert isinstance(result.best_model, str)
    assert isinstance(result.total_bits, int)
