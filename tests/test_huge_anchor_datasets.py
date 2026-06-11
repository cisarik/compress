from primesymbolicmdl.huge_anchor_datasets import get_huge_anchor_dataset_names, make_huge_anchor_dataset


def test_huge_anchor_dataset_names_are_stable() -> None:
    assert get_huge_anchor_dataset_names() == [
        "linear_shift_generated",
        "square_generated",
        "multiple_generated",
        "random_bytes",
        "ascii_small",
        "repeating_pattern",
    ]


def test_huge_anchor_datasets_are_deterministic_for_same_seed() -> None:
    left = make_huge_anchor_dataset("random_bytes", 32, count=16, seed=1234)
    right = make_huge_anchor_dataset("random_bytes", 32, count=16, seed=1234)

    assert left == right


def test_generated_dataset_respects_requested_size() -> None:
    data = make_huge_anchor_dataset("square_generated", 64, count=10, seed=1234)

    assert len(data) == 10 * (64 // 8)
