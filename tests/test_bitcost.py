from primesymbolicmdl.bitcost import estimate_prime_anchor_cost
from primesymbolicmdl.blocks import bytes_to_uint_blocks


def test_cost_accounting_uses_original_size_bits() -> None:
    data = b"\x00\x01\x02"
    blocks = bytes_to_uint_blocks(data, 16)
    costs = estimate_prime_anchor_cost(blocks, 16, len(data), "nearest")

    assert costs["raw_bits"] == len(data) * 8
    assert costs["width_bits"] == 16
    assert isinstance(costs["ratio_vs_raw"], (int, float))


def test_cost_accounting_handles_empty_data() -> None:
    costs = estimate_prime_anchor_cost([], 8, 0, "nearest")

    assert costs["raw_bits"] == 0
    assert costs["block_count"] == 0
    assert costs["escape_count"] == 0


def test_lower_mode_counts_escaped_blocks_below_two() -> None:
    data = b"\x00\x01\x02\x03"
    blocks = bytes_to_uint_blocks(data, 8)
    costs = estimate_prime_anchor_cost(blocks, 8, len(data), "lower")

    assert costs["escape_count"] == 2
    assert costs["escape_bits"] == 16
    assert costs["block_count"] == 4
