import io
from contextlib import redirect_stdout

from primesymbolicmdl import huge_anchor_demo


def test_huge_anchor_demo_runs_and_prints_reports() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        huge_anchor_demo.main()

    output = stdout.getvalue()
    assert "dataset: linear_shift_generated" in output
    assert "dataset: random_bytes" in output
    assert "best_model:" in output
    assert "top_3_candidates:" in output
    assert "scaled_prime_baseline:" in output


def test_huge_anchor_demo_results_include_at_least_one_win() -> None:
    results = huge_anchor_demo.run_demo()

    assert results
    assert all(result["roundtrip_ok"] for result in results)
    assert any(result["decision"] == "win" for result in results if result["dataset"].endswith("_generated"))
