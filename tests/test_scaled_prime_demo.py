import io
from contextlib import redirect_stdout

from primesymbolicmdl import scaled_prime_demo


def test_scaled_prime_demo_runs_and_prints_reports() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        scaled_prime_demo.main()

    output = stdout.getvalue()
    assert "dataset: ascii_small" in output
    assert "dataset: random_bytes" in output
    assert "best_model:" in output
    assert "residual_codec:" in output
    assert "roundtrip_ok: True" in output
    assert "decision:" in output


def test_scaled_prime_demo_results_are_exact_roundtrips() -> None:
    results = scaled_prime_demo.run_demo()

    assert results
    assert all(result["roundtrip_ok"] for result in results)
