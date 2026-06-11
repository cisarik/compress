from primesymbolicmdl.image_datasets import make_checker_image, make_diagonal_ramp_image, make_gradient_image, make_noise_image
from primesymbolicmdl.image_datasets import make_gray_image
from primesymbolicmdl.image_predictor_branch import (
    decode_image_predictor_payload,
    encode_image_predictor_payload,
    estimate_image_predictor_cost,
    roundtrip_image_predictor,
)
from primesymbolicmdl.image_predictors import ImagePredictorModel


def test_x_ramp_predictor_can_exactly_match_gradient_image() -> None:
    image = make_gradient_image(8, 8)
    cost = estimate_image_predictor_cost(image, ImagePredictorModel("x_ramp"))

    assert cost["residual_width"] == 0
    assert cost["residual_codec"] == "fixed_signed"
    assert cost["total_bits"] < cost["raw_bits"]


def test_diagonal_ramp_predictor_roundtrips_diagonal_ramp() -> None:
    image = make_diagonal_ramp_image(8, 8)
    model = ImagePredictorModel("diagonal_ramp")

    assert roundtrip_image_predictor(image, model) == image.pixels


def test_checker_predictor_roundtrips_checker_image() -> None:
    image = make_checker_image(8, 8, 4)
    payload = encode_image_predictor_payload(image, ImagePredictorModel("checker", {"block": 4}))

    assert decode_image_predictor_payload(payload) == image.pixels


def test_zero_predictor_roundtrips_noise_even_without_compression_win() -> None:
    image = make_noise_image(8, 8, 1234)
    model = ImagePredictorModel("zero")
    cost = estimate_image_predictor_cost(image, model)

    assert roundtrip_image_predictor(image, model) == image.pixels
    assert isinstance(cost["ratio_vs_raw"], float)


def test_cost_report_contains_required_fields() -> None:
    image = make_gradient_image(4, 4)
    cost = estimate_image_predictor_cost(image, ImagePredictorModel("x_ramp"))

    required = {
        "raw_bits",
        "model_bits",
        "parameter_bits",
        "header_bits",
        "residual_bits",
        "residual_codec",
        "residual_codec_details",
        "total_bits",
        "saving_bits",
        "ratio_vs_raw",
        "min_residual",
        "max_residual",
        "residual_width",
        "pixel_count",
        "model",
    }

    assert required.issubset(cost)


def test_nonzero_constant_residuals_still_need_positive_width() -> None:
    image = make_gray_image("constant", 4, 4, bytes([5] * 16))
    cost = estimate_image_predictor_cost(image, ImagePredictorModel("zero"))

    assert cost["min_residual"] == 5
    assert cost["max_residual"] == 5
    assert cost["residual_width"] > 0


def test_predictor_payload_carries_residual_codec_metadata() -> None:
    image = make_gradient_image(8, 8)
    payload = encode_image_predictor_payload(image, ImagePredictorModel("x_ramp"))

    assert payload["residual_codec"] == "fixed_signed"
    assert isinstance(payload["residual_payload"], dict)
