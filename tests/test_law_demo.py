import importlib
import io
from contextlib import redirect_stdout

from primesymbolicmdl import law_demo


def test_law_demo_module_is_importable() -> None:
    module = importlib.import_module("primesymbolicmdl.law_demo")

    assert hasattr(module, "main")


def test_law_demo_runs_and_prints_summary() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        law_demo.main()

    output = stdout.getvalue()
    assert "dataset:" in output
    assert "best_law:" in output
