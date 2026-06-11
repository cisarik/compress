import importlib
import io
from contextlib import redirect_stdout

from primesymbolicmdl.experiments import (
    default_datasets,
    format_markdown_table,
    run_prime_anchor_matrix,
)


def test_default_experiment_matrix_produces_rows() -> None:
    rows = run_prime_anchor_matrix(
        datasets=default_datasets(),
        widths=(8, 16, 24, 32),
        modes=("lower", "upper", "nearest"),
    )

    assert rows


def test_all_requested_widths_and_modes_appear() -> None:
    rows = run_prime_anchor_matrix(
        datasets={"tiny": b"\x00\x01\x02"},
        widths=(8, 16, 24, 32),
        modes=("lower", "upper", "nearest"),
    )

    assert {row["width_bits"] for row in rows} == {8, 16, 24, 32}
    assert {row["mode"] for row in rows} == {"lower", "upper", "nearest"}


def test_markdown_table_contains_header() -> None:
    table = format_markdown_table(
        [
            {
                "dataset": "tiny",
                "size_bytes": 3,
                "width_bits": 8,
                "mode": "nearest",
                "raw_bits": 24,
                "total_bits": 40,
                "ratio_vs_raw": 1.5,
                "escape_count": 0,
                "block_count": 3,
            }
        ]
    )

    assert "| dataset " in table
    assert "| ratio_vs_raw " in table


def test_cli_module_is_importable_and_prints_table() -> None:
    module = importlib.import_module("primesymbolicmdl.experiments")
    assert hasattr(module, "run_prime_anchor_matrix")

    stdout = io.StringIO()
    with redirect_stdout(stdout):
        module.main()

    output = stdout.getvalue()
    assert "| dataset " in output
