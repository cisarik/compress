import io
from contextlib import redirect_stdout

from primesymbolicmdl import huge_anchor_binary_demo


def test_huge_anchor_binary_demo_runs_and_prints_actual_fields() -> None:
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        huge_anchor_binary_demo.main()

    output = stdout.getvalue()
    assert "dataset: linear_shift_generated" in output
    assert "actual_bits:" in output
    assert "decision:" in output
    assert "estimated_best_model:" in output
    assert "actual_best_model:" in output
    assert "actual_top_3_candidates:" in output


def test_huge_anchor_binary_demo_results_include_actual_compression_or_honest_fallback() -> None:
    results = huge_anchor_binary_demo.run_demo()

    assert results
    assert all(result["roundtrip_ok"] for result in results)
    assert any(result["decision"] == "compressed" for result in results if result["dataset"].endswith("_generated"))
    assert all(result["actual_rerank_candidates"] for result in results)
