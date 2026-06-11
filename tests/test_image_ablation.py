import io
from contextlib import redirect_stdout

from primesymbolicmdl import image_ablation


def test_run_image_gplite_ablation_returns_all_primitive_sets() -> None:
    rows = image_ablation.run_image_gplite_ablation("gradient", width=8, height=8, population_size=8, generations=4)

    assert [row["primitive_set"] for row in rows] == ["local", "ramp", "structure"]
    assert all("residual_codec" in row for row in rows)


def test_format_image_ablation_table_returns_markdown_header() -> None:
    rows = image_ablation.run_image_gplite_ablation("checker", width=8, height=8, population_size=8, generations=4)
    table = image_ablation.format_image_ablation_table(rows)

    assert "| dataset | primitive_set |" in table
    assert "structure" in table


def test_image_ablation_cli_main_runs() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        image_ablation.main()

    output = stdout.getvalue()
    assert "## Image-GP-lite ablation: gradient" in output
    assert "## Image-GP-lite ablation: checker" in output
    assert "| dataset | primitive_set |" in output
