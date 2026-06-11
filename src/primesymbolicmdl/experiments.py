"""Deterministicke experimenty pre prime-anchor maticu."""

from __future__ import annotations

import math
import random

from .bitcost import estimate_prime_anchor_cost
from .blocks import bytes_to_uint_blocks


def dataset_empty() -> bytes:
    """Vrati prazdnu testovaciu vzorku."""

    return b""


def dataset_ascii_small() -> bytes:
    """Vrati malu ASCII vzorku s citatelnym obsahom."""

    return b"PrimeSymbolicMDL experimental harness"


def dataset_zeros(size: int = 1024) -> bytes:
    """Vrati nulovy dataset pevnej dlzky."""

    if size < 0:
        raise ValueError("size must be non-negative")
    return b"\x00" * size


def dataset_ramp_u16(count: int = 512) -> bytes:
    """Vrati rastucu rampu 16-bitovych hodnot v big-endian tvare."""

    if count < 0:
        raise ValueError("count must be non-negative")
    return b"".join((value % (1 << 16)).to_bytes(2, "big") for value in range(count))


def dataset_random(size: int = 1024, seed: int = 1234) -> bytes:
    """Vrati deterministicke pseudo-nahodne byty."""

    if size < 0:
        raise ValueError("size must be non-negative")
    rng = random.Random(seed)
    return bytes(rng.randrange(256) for _ in range(size))


def default_datasets() -> dict[str, bytes]:
    """Vrati malu deterministicku sadu datasetov pre rychle lokalne porovnanie."""

    return {
        "empty": dataset_empty(),
        "zeros_256": dataset_zeros(256),
        "ramp_u16_64": dataset_ramp_u16(64),
    }


def run_prime_anchor_matrix(
    datasets: dict[str, bytes],
    widths: tuple[int, ...],
    modes: tuple[str, ...],
) -> list[dict]:
    """Spusti deterministicku maticu sirka x mod nad zadanou sadou datasetov."""

    rows: list[dict] = []

    for dataset_name, data in datasets.items():
        for width_bits in widths:
            blocks = bytes_to_uint_blocks(data, width_bits)
            for mode in modes:
                costs = estimate_prime_anchor_cost(blocks, width_bits, len(data), mode)
                rows.append(
                    {
                        "dataset": dataset_name,
                        "size_bytes": len(data),
                        "width_bits": width_bits,
                        "mode": mode,
                        "raw_bits": costs["raw_bits"],
                        "total_bits": costs["total_bits"],
                        "ratio_vs_raw": costs["ratio_vs_raw"],
                        "escape_count": costs["escape_count"],
                        "block_count": costs["block_count"],
                    }
                )

    return rows


def _format_cell(column: str, value) -> str:
    """Zjednoti formatovanie buniek pre terminalovy markdown."""

    if column == "ratio_vs_raw" and isinstance(value, (int, float)):
        if math.isinf(value):
            return "inf"
        return f"{float(value):.3f}"
    return str(value)


def format_markdown_table(rows: list[dict]) -> str:
    """Vrati maticu ako jednoduchu markdown tabulku."""

    columns = [
        "dataset",
        "size_bytes",
        "width_bits",
        "mode",
        "raw_bits",
        "total_bits",
        "ratio_vs_raw",
        "escape_count",
        "block_count",
    ]
    headers = {
        "dataset": "dataset",
        "size_bytes": "size_bytes",
        "width_bits": "width_bits",
        "mode": "mode",
        "raw_bits": "raw_bits",
        "total_bits": "total_bits",
        "ratio_vs_raw": "ratio_vs_raw",
        "escape_count": "escape_count",
        "block_count": "block_count",
    }

    rendered_rows = []
    for row in rows:
        rendered_rows.append([_format_cell(column, row.get(column, "")) for column in columns])

    widths = []
    for index, column in enumerate(columns):
        cell_width = len(headers[column])
        for rendered_row in rendered_rows:
            cell_width = max(cell_width, len(rendered_row[index]))
        widths.append(cell_width)

    header_line = "| " + " | ".join(headers[column].ljust(widths[index]) for index, column in enumerate(columns)) + " |"
    separator_line = "| " + " | ".join("-" * widths[index] for index, _ in enumerate(columns)) + " |"
    body_lines = [
        "| " + " | ".join(row[index].ljust(widths[index]) for index in range(len(columns))) + " |"
        for row in rendered_rows
    ]

    return "\n".join([header_line, separator_line, *body_lines])


def main() -> None:
    """Vypise predvolenu markdown tabulku experimentov."""

    rows = run_prime_anchor_matrix(
        datasets=default_datasets(),
        widths=(8, 16, 24, 32),
        modes=("lower", "upper", "nearest"),
    )
    print(format_markdown_table(rows))


if __name__ == "__main__":
    main()
