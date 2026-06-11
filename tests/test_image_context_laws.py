from primesymbolicmdl.image_context_laws import (
    add_law,
    avg_law,
    checker_parity_law,
    clamp_byte_law,
    const_law,
    eq_const_law,
    evaluate_image_law,
    floordiv_const_law,
    floordiv_pow2_law,
    gradient_law,
    image_law_model_bits,
    image_law_parameter_bits,
    mod_const_law,
    mul_small_law,
    parity_byte_law,
    render_image_law,
    sub_law,
    terminal_law,
)
from primesymbolicmdl.image_datasets import make_checker_image


def _context() -> dict[str, int]:
    return {
        "col": 3,
        "row": 2,
        "width": 8,
        "height": 8,
        "left": 50,
        "up": 70,
        "up_left": 20,
        "x_ramp": 109,
        "y_ramp": 72,
        "diag_ramp": 91,
    }


def test_terminals_return_decoder_known_context() -> None:
    context = _context()

    assert evaluate_image_law(terminal_law("left"), context) == 50
    assert evaluate_image_law(terminal_law("up"), context) == 70
    assert evaluate_image_law(terminal_law("x_ramp"), context) == 109


def test_basic_image_law_operators_work() -> None:
    context = _context()

    assert evaluate_image_law(add_law(terminal_law("left"), const_law(5)), context) == 55
    assert evaluate_image_law(sub_law(terminal_law("up"), terminal_law("left")), context) == 20
    assert evaluate_image_law(avg_law(terminal_law("left"), terminal_law("up")), context) == 60
    assert evaluate_image_law(
        gradient_law(terminal_law("left"), terminal_law("up"), terminal_law("up_left")),
        context,
    ) == 100
    assert evaluate_image_law(mul_small_law(terminal_law("row"), 3), context) == 6
    assert evaluate_image_law(floordiv_pow2_law(const_law(40), 3), context) == 5


def test_clamp_byte_keeps_prediction_in_byte_range() -> None:
    context = _context()

    assert evaluate_image_law(clamp_byte_law(const_law(999)), context) == 255
    assert evaluate_image_law(sub_law(const_law(0), const_law(999)), context) == 0


def test_render_and_bit_helpers_are_stable() -> None:
    law = clamp_byte_law(
        gradient_law(
            terminal_law("left"),
            terminal_law("up"),
            floordiv_pow2_law(terminal_law("up_left"), 1),
        )
    )

    assert render_image_law(law) == "clamp_byte(gradient(left, up, floordiv_pow2(up_left, 1)))"
    assert isinstance(image_law_model_bits(law), int)
    assert isinstance(image_law_parameter_bits(law), int)
    assert image_law_model_bits(law) > 0


def test_structure_primitives_are_deterministic() -> None:
    context = _context()

    assert evaluate_image_law(mod_const_law(terminal_law("col"), 4), context) == 3
    assert evaluate_image_law(floordiv_const_law(terminal_law("left"), 4), context) == 12
    assert evaluate_image_law(eq_const_law(terminal_law("row"), 2), context) == 255
    assert evaluate_image_law(eq_const_law(terminal_law("row"), 3), context) == 0
    assert evaluate_image_law(parity_byte_law(terminal_law("col")), context) == 255


def test_checker_parity_matches_checker_dataset_for_block_four() -> None:
    image = make_checker_image(8, 8, 4)
    law = checker_parity_law(4)
    predicted = bytes(
        evaluate_image_law(
            law,
            {
                "col": col,
                "row": row,
                "width": image.width,
                "height": image.height,
                "left": 0,
                "up": 0,
                "up_left": 0,
                "x_ramp": (255 * col) // max(1, image.width - 1),
                "y_ramp": (255 * row) // max(1, image.height - 1),
                "diag_ramp": (255 * (col + row)) // max(1, image.width + image.height - 2),
            },
        )
        for row in range(image.height)
        for col in range(image.width)
    )

    assert predicted == image.pixels


def test_structure_primitive_render_strings_are_stable() -> None:
    law = clamp_byte_law(
        add_law(
            checker_parity_law(4),
            parity_byte_law(floordiv_const_law(terminal_law("col"), 2)),
        )
    )

    assert (
        render_image_law(law)
        == "clamp_byte(add(checker_parity(block=4), parity_byte(floordiv_const(col, 2))))"
    )
    assert isinstance(image_law_model_bits(law), int)
    assert isinstance(image_law_parameter_bits(law), int)
