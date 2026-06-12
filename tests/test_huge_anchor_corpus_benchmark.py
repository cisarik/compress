from pathlib import Path

import pytest

from primesymbolicmdl.huge_anchor_corpus_benchmark import (
    discover_corpus_files,
    format_corpus_table,
    run_corpus_benchmark,
    summarize_corpus_rows,
)
from primesymbolicmdl.huge_anchor_datasets import make_huge_anchor_dataset


def test_discover_corpus_files_is_deterministic(tmp_path: Path) -> None:
    (tmp_path / "b.bin").write_bytes(b"b")
    (tmp_path / "a.bin").write_bytes(b"a")
    (tmp_path / "skip").mkdir()
    (tmp_path / "skip" / "hidden.bin").write_bytes(b"x")

    files = discover_corpus_files(input_dir=tmp_path, recursive=False)
    assert [path.name for path in files] == ["a.bin", "b.bin"]


def test_run_corpus_benchmark_reports_aggregate_summary(tmp_path: Path) -> None:
    random_bytes = make_huge_anchor_dataset("random_bytes", 32, count=16, seed=99)
    square_bytes = make_huge_anchor_dataset("square_generated", 64, count=16, seed=99)
    (tmp_path / "random.bin").write_bytes(random_bytes)
    (tmp_path / "square.bin").write_bytes(square_bytes)

    result = run_corpus_benchmark(input_dir=tmp_path, width_bits=32)
    table = format_corpus_table(result)

    assert result.summary.file_count == 2
    assert result.summary.total_raw_bytes == sum(row.raw_bytes for row in result.rows)
    assert result.summary.total_psmdl_bytes == sum(row.psmdl_bytes for row in result.rows)
    assert result.summary.raw_fallback_count >= 1
    assert "aggregate_summary:" in table
    assert all(row.roundtrip_ok for row in result.rows)


def test_random_like_temp_file_does_not_claim_misleading_compression_win(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=16, seed=4242)
    file_path = tmp_path / "random.bin"
    file_path.write_bytes(data)

    result = run_corpus_benchmark(input_paths=[file_path], width_bits=32)
    row = result.rows[0]

    assert row.roundtrip_ok is True
    assert row.decision == "raw_fallback"
    assert row.psmdl_bytes >= row.raw_bytes


def test_square_generated_file_may_compress_on_64_bit_width(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("square_generated", 64, count=16, seed=4242)
    file_path = tmp_path / "square.bin"
    file_path.write_bytes(data)

    result = run_corpus_benchmark(input_paths=[file_path], width_bits=64)
    row = result.rows[0]

    assert row.roundtrip_ok is True
    assert row.decision == "compressed"
    assert row.psmdl_bytes < row.raw_bytes


def test_max_files_limits_discovery(tmp_path: Path) -> None:
    for index in range(5):
        (tmp_path / f"f{index}.bin").write_bytes(bytes([index]))

    files = discover_corpus_files(input_dir=tmp_path, max_files=2)
    assert len(files) == 2


def test_discover_requires_input() -> None:
    with pytest.raises(ValueError, match="Provide at least one"):
        discover_corpus_files()
