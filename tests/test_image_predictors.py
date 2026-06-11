from primesymbolicmdl.image_predictors import (
    ImagePredictorModel,
    default_image_predictor_models,
    image_predictor_model_bits,
    image_predictor_parameter_bits,
    predict_pixel,
    render_image_predictor,
)


def test_default_image_predictor_models_are_stable() -> None:
    models = default_image_predictor_models()

    assert [render_image_predictor(model) for model in models] == [
        "zero",
        "left",
        "up",
        "avg_left_up",
        "gradient",
        "x_ramp",
        "y_ramp",
        "diagonal_ramp",
        "checker(block=1)",
        "checker(block=2)",
        "checker(block=4)",
        "checker(block=8)",
        "checker(block=16)",
    ]


def test_predict_pixel_supports_context_predictors() -> None:
    assert predict_pixel(ImagePredictorModel("zero"), 2, 3, 8, 8, 11, 22, 33) == 0
    assert predict_pixel(ImagePredictorModel("left"), 2, 3, 8, 8, 11, 22, 33) == 11
    assert predict_pixel(ImagePredictorModel("up"), 2, 3, 8, 8, 11, 22, 33) == 22
    assert predict_pixel(ImagePredictorModel("avg_left_up"), 2, 3, 8, 8, 11, 22, 33) == 16
    assert predict_pixel(ImagePredictorModel("gradient"), 2, 3, 8, 8, 11, 22, 33) == 0


def test_predict_pixel_supports_geometric_predictors() -> None:
    assert predict_pixel(ImagePredictorModel("x_ramp"), 7, 0, 8, 8, 0, 0, 0) == 255
    assert predict_pixel(ImagePredictorModel("y_ramp"), 0, 7, 8, 8, 0, 0, 0) == 255
    assert predict_pixel(ImagePredictorModel("diagonal_ramp"), 7, 7, 8, 8, 0, 0, 0) == 255
    assert predict_pixel(ImagePredictorModel("checker", {"block": 2}), 3, 0, 8, 8, 0, 0, 0) == 255


def test_predict_pixel_clamps_gradient_to_byte_range() -> None:
    assert predict_pixel(ImagePredictorModel("gradient"), 1, 1, 8, 8, 255, 255, 0) == 255


def test_image_predictor_bit_helpers_are_deterministic() -> None:
    assert image_predictor_model_bits(ImagePredictorModel("zero")) == 4
    assert image_predictor_parameter_bits(ImagePredictorModel("zero")) == 0
    assert image_predictor_parameter_bits(ImagePredictorModel("checker", {"block": 16})) > 0
