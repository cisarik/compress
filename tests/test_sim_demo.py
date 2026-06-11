import io
from contextlib import redirect_stdout

from primesymbolicmdl import sim_demo


def test_sim_demo_runs_and_prints_reports() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        sim_demo.main()

    output = stdout.getvalue()
    assert "optimizer: Image-predictor" in output
    assert "optimizer: Image-GP-lite" in output
    assert "optimizer: Image-SOMA" in output
    assert "optimizer: GP-lite" in output
    assert "optimizer: SOMA" in output
    assert "residual_codec:" in output
    assert "raw_byte_codec:" in output
    assert "## Image-GP-lite primitive ablation summary: gradient" in output
    assert "primitive_set" in output
