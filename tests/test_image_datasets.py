from primesymbolicmdl.image_datasets import (
    get_image_dataset_names,
    make_checker_image,
    make_diagonal_ramp_image,
    make_gradient_image,
    make_image_dataset,
    make_noise_image,
)


def test_generated_images_have_expected_pixel_length() -> None:
    for image in (
        make_gradient_image(8, 8),
        make_checker_image(8, 8, 2),
        make_diagonal_ramp_image(8, 8),
        make_noise_image(8, 8, 1234),
    ):
        assert len(image.pixels) == image.width * image.height


def test_generated_pixels_are_bytes() -> None:
    image = make_gradient_image(4, 4)

    assert isinstance(image.pixels, bytes)


def test_dataset_names_are_stable() -> None:
    assert get_image_dataset_names() == ["gradient", "checker", "diagonal_ramp", "noise"]


def test_make_image_dataset_dispatches() -> None:
    image = make_image_dataset("noise", 8, 8, 1234)

    assert image.name == "noise"
