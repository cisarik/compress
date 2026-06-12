from primesymbolicmdl.huge_anchor_file_benchmark import format_benchmark_table, run_benchmark


def test_huge_anchor_file_benchmark_runs_and_reports_honest_sizes() -> None:
  rows = run_benchmark()
  table = format_benchmark_table(rows)

  assert len(rows) >= 5
  assert all(row.roundtrip_ok for row in rows)
  assert any(row.decision == "raw_fallback" for row in rows)
  assert any(row.decision == "compressed" for row in rows)
  assert "random_bytes_128" in table
  assert "square_generated_64" in table
  assert "README.md" in table

  random_row = next(row for row in rows if row.name == "random_bytes_128")
  assert random_row.decision == "raw_fallback"
  assert random_row.psmdl_bytes >= random_row.raw_bytes
  assert random_row.require_compression == "refused"

  square_row = next(row for row in rows if row.name == "square_generated_64")
  assert square_row.decision == "compressed"
  assert square_row.psmdl_bytes < square_row.raw_bytes
  assert square_row.require_compression == "ok"
