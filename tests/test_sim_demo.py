import io
from contextlib import redirect_stdout

from primesymbolicmdl import sim_demo


def test_sim_demo_runs_and_prints_reports() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        sim_demo.main()

    output = stdout.getvalue()
    assert "optimizer: GP-lite" in output
    assert "optimizer: SOMA" in output
