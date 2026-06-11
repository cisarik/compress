from primesymbolicmdl.image_context_laws import terminal_law
from primesymbolicmdl.image_datasets import make_checker_image, make_diagonal_ramp_image, make_gradient_image
from primesymbolicmdl.image_law_branch import (
    decode_image_law_payload,
    encode_image_law_payload,
    estimate_image_law_cost,
    roundtrip_image_law,
)


def test_x_ramp_law_can_exactly_match_gradient_image() -> None:
    image = make_gradient_image(8, 8)
    law = terminal_law("x_ramp")
    cost = estimate_image_law_cost(image, law)

    assert roundtrip_image_law(image, law) == image.pixels
    assert cost["residual_codec"] == "fixed_signed"
    assert cost["raw_bits"] == image.width * image.height * 8
    assert cost["total_bits"] < cost["raw_bits"]


def test_diagonal_ramp_law_roundtrips_diagonal_image() -> None:
    image = make_diagonal_ramp_image(8, 8)
    law = terminal_law("diag_ramp")

    assert roundtrip_image_law(image, law) == image.pixels


def test_image_law_payload_roundtrips_checker_even_without_win() -> None:
    image = make_checker_image(8, 8, 4)
    payload = encode_image_law_payload(image, terminal_law("x_ramp"))

    assert decode_image_law_payload(payload) == image.pixels


def test_image_law_cost_report_contains_required_fields() -> None:
    image = make_gradient_image(4, 4)
    cost = estimate_image_law_cost(image, terminal_law("x_ramp"))

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
        "pixel_count",
        "model",
    }

    assert required.issubset(cost)
