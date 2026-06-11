from primesymbolicmdl.anchor_laws import (
    add_law,
    anchor_value,
    clamp_nonnegative_law,
    const_law,
    floordiv_pow2_law,
    idx_law,
    law_model_bits,
    law_parameter_bits,
    mul_small_law,
    render_law,
    square_law,
    sub_law,
)


def test_idx_terminal_evaluates_to_index() -> None:
    assert anchor_value(idx_law(), 7) == 7


def test_constant_terminal_evaluates() -> None:
    assert anchor_value(const_law(5), 12) == 5


def test_add_and_sub_evaluate() -> None:
    law = sub_law(add_law(idx_law(), const_law(3)), const_law(1))

    assert anchor_value(law, 4) == 6


def test_mul_small_evaluates() -> None:
    assert anchor_value(mul_small_law(idx_law(), 3), 5) == 15


def test_floordiv_pow2_evaluates() -> None:
    assert anchor_value(floordiv_pow2_law(mul_small_law(idx_law(), 3), 2), 5) == 3


def test_square_evaluates() -> None:
    assert anchor_value(square_law(idx_law()), 6) == 36


def test_clamp_nonnegative_evaluates() -> None:
    law = clamp_nonnegative_law(sub_law(idx_law(), const_law(5)))

    assert anchor_value(law, 2) == 0
    assert anchor_value(law, 9) == 4


def test_render_is_deterministic_and_readable() -> None:
    law = clamp_nonnegative_law(add_law(idx_law(), const_law(2)))

    assert render_law(law) == "clamp_nonnegative(add(idx, 2))"
    assert render_law(law) == render_law(law)


def test_model_and_parameter_bits_are_reported() -> None:
    law = mul_small_law(add_law(idx_law(), const_law(2)), 3)

    assert law_model_bits(law) > 0
    assert law_parameter_bits(law) > 0
