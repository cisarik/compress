import pytest

from primesymbolicmdl.huge_anchor_models import (
    HugeAnchorModel,
    anchor_from_index,
    huge_anchor_model_bits,
    huge_anchor_parameter_bits,
    render_huge_anchor_model,
)


def test_render_huge_anchor_model_is_stable() -> None:
    model = HugeAnchorModel("affine_shift", {"shift": 4, "bias": -1})

    assert render_huge_anchor_model(model) == "affine_shift(bias=-1, shift=4)"


def test_huge_anchor_model_bits_and_parameters_are_positive() -> None:
    model = HugeAnchorModel("linear_shift", {"shift": 3})

    assert huge_anchor_model_bits(model) > 0
    assert huge_anchor_parameter_bits(model) > 0


@pytest.mark.parametrize(
    ("model", "index", "width_bits", "expected"),
    [
        (HugeAnchorModel("linear_shift", {"shift": 3}), 5, 16, 40),
        (HugeAnchorModel("affine_shift", {"shift": 2, "bias": 3}), 4, 16, 19),
        (HugeAnchorModel("multiple", {"step": 7}), 6, 16, 42),
        (HugeAnchorModel("square", {}), 9, 16, 81),
        (HugeAnchorModel("scaled_prime", {"shift": 4, "search_radius": 0}), 3, 16, 47),
    ],
)
def test_anchor_from_index_returns_expected_values(
    model: HugeAnchorModel,
    index: int,
    width_bits: int,
    expected: int,
) -> None:
    assert anchor_from_index(index, model, width_bits) == expected


def test_scaled_prime_anchor_returns_none_above_64_bits() -> None:
    model = HugeAnchorModel("scaled_prime", {"shift": 4, "search_radius": 0})

    assert anchor_from_index(3, model, 96) is None


def test_unknown_family_raises() -> None:
    model = HugeAnchorModel("unknown_family", {})

    with pytest.raises(ValueError):
        render_huge_anchor_model(model)
