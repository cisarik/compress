"""External-corpus benchmark pre actual `.psmdl` velkosti bez univerzalnych tvrdeni."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from .huge_anchor_file import compress_to_psmdl_bytes, decode_psmdl_bytes
from .huge_blocks import SUPPORTED_HUGE_WIDTHS

_SKIP_DIR_NAMES = {".git", ".venv", "__pycache__", ".pytest_cache", ".ap"}


@dataclass(frozen=True)
class CorpusRow:
    """Vysledok jedneho suboru v external-corpus benchmarke."""

    path: str
    raw_bytes: int
    psmdl_bytes: int
    decision: str
    file_format: str
    roundtrip_ok: bool
    error: str | None = None


@dataclass(frozen=True)
class CorpusSummary:
    """Agregovany honest suhrn external-corpus benchmarku."""

    file_count: int
    total_raw_bytes: int
    total_psmdl_bytes: int
    total_delta_bytes: int
    compressed_count: int
    raw_fallback_count: int
    roundtrip_failure_count: int
    error_count: int


@dataclass(frozen=True)
class CorpusBenchmarkResult:
    """Kompletny vysledok benchmarku."""

    rows: tuple[CorpusRow, ...]
    summary: CorpusSummary


def discover_corpus_files(
    *,
    input_paths: list[Path] | None = None,
    input_dir: Path | None = None,
    recursive: bool = False,
    max_files: int | None = None,
) -> list[Path]:
    """Deterministicky najde subory pre benchmark."""

    if input_paths is None:
        input_paths = []
    if not input_paths and input_dir is None:
        raise ValueError("Provide at least one --file path or --input-dir")

    discovered: list[Path] = []
    seen: set[Path] = set()

    def add_file(path: Path) -> None:
        resolved = path.resolve()
        if not resolved.is_file():
            raise ValueError(f"Not a regular file: {path}")
        if resolved in seen:
            return
        seen.add(resolved)
        discovered.append(resolved)

    for path in input_paths:
        add_file(Path(path))

    if input_dir is not None:
        root = Path(input_dir).resolve()
        if not root.is_dir():
            raise ValueError(f"Not a directory: {input_dir}")

        iterator = root.rglob("*") if recursive else root.glob("*")
        for candidate in sorted(iterator):
            if not candidate.is_file():
                continue
            if any(part in _SKIP_DIR_NAMES for part in candidate.parts):
                continue
            if candidate in seen:
                continue
            seen.add(candidate)
            discovered.append(candidate)

    discovered.sort(key=lambda path: str(path))
    if max_files is not None:
        if max_files <= 0:
            raise ValueError("max_files must be positive")
        discovered = discovered[:max_files]
    return discovered


def benchmark_file(path: Path, *, width_bits: int = 32) -> CorpusRow:
    """Skomprimuje jeden subor a overi exact roundtrip."""

    display_path = str(path)
    try:
        payload = path.read_bytes()
        result = compress_to_psmdl_bytes(payload, width_bits=width_bits)
        restored = decode_psmdl_bytes(result.file_bytes)
        roundtrip_ok = restored == payload
        return CorpusRow(
            path=display_path,
            raw_bytes=result.raw_bytes,
            psmdl_bytes=result.compressed_bytes,
            decision=result.decision,
            file_format=result.file_format,
            roundtrip_ok=roundtrip_ok,
            error=None if roundtrip_ok else "roundtrip mismatch",
        )
    except Exception as error:  # pragma: no cover - exercised via tests indirectly
        raw_size = 0
        try:
            raw_size = path.stat().st_size
        except OSError:
            pass
        return CorpusRow(
            path=display_path,
            raw_bytes=raw_size,
            psmdl_bytes=0,
            decision="error",
            file_format="error",
            roundtrip_ok=False,
            error=str(error),
        )


def run_corpus_benchmark(
    *,
    input_paths: list[Path] | None = None,
    input_dir: Path | None = None,
    recursive: bool = False,
    max_files: int | None = None,
    width_bits: int = 32,
) -> CorpusBenchmarkResult:
    """Spusti external-corpus benchmark nad explicitnymi cestami alebo adresarom."""

    files = discover_corpus_files(
        input_paths=input_paths,
        input_dir=input_dir,
        recursive=recursive,
        max_files=max_files,
    )
    rows = tuple(benchmark_file(path, width_bits=width_bits) for path in files)
    return CorpusBenchmarkResult(rows=rows, summary=summarize_corpus_rows(rows))


def summarize_corpus_rows(rows: tuple[CorpusRow, ...] | list[CorpusRow]) -> CorpusSummary:
    """Vypocita agregovany honest suhrn."""

    total_raw = 0
    total_psmdl = 0
    compressed_count = 0
    raw_fallback_count = 0
    roundtrip_failure_count = 0
    error_count = 0

    for row in rows:
        if row.error is not None and row.decision == "error":
            error_count += 1
        if not row.roundtrip_ok:
            roundtrip_failure_count += 1
        total_raw += row.raw_bytes
        total_psmdl += row.psmdl_bytes
        if row.decision == "compressed":
            compressed_count += 1
        elif row.decision == "raw_fallback":
            raw_fallback_count += 1

    return CorpusSummary(
        file_count=len(rows),
        total_raw_bytes=total_raw,
        total_psmdl_bytes=total_psmdl,
        total_delta_bytes=total_psmdl - total_raw,
        compressed_count=compressed_count,
        raw_fallback_count=raw_fallback_count,
        roundtrip_failure_count=roundtrip_failure_count,
        error_count=error_count,
    )


def format_corpus_table(result: CorpusBenchmarkResult) -> str:
    """Vrati citatelnu tabulku a agregovany suhrn."""

    header = "path | raw_bytes | psmdl_bytes | delta | decision | file_format | roundtrip_ok | error"
    lines = [header, "-" * len(header)]
    for row in result.rows:
        delta = row.psmdl_bytes - row.raw_bytes
        error = row.error or ""
        lines.append(
            f"{row.path} | {row.raw_bytes} | {row.psmdl_bytes} | {delta} | {row.decision} | "
            f"{row.file_format} | {row.roundtrip_ok} | {error}"
        )

    summary = result.summary
    lines.extend(
        [
            "",
            "aggregate_summary:",
            f"file_count={summary.file_count}",
            f"total_raw_bytes={summary.total_raw_bytes}",
            f"total_psmdl_bytes={summary.total_psmdl_bytes}",
            f"total_delta_bytes={summary.total_delta_bytes}",
            f"compressed_count={summary.compressed_count}",
            f"raw_fallback_count={summary.raw_fallback_count}",
            f"roundtrip_failure_count={summary.roundtrip_failure_count}",
            f"error_count={summary.error_count}",
        ]
    )
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark actual .psmdl sizes on an external file corpus.",
    )
    parser.add_argument("--input-dir", help="Directory containing files to benchmark")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        dest="files",
        help="Explicit file path to benchmark; may be repeated",
    )
    parser.add_argument("--recursive", action="store_true", help="Walk --input-dir recursively")
    parser.add_argument("--max-files", type=int, help="Limit number of discovered files")
    parser.add_argument(
        "--width-bits",
        type=int,
        default=32,
        choices=sorted(SUPPORTED_HUGE_WIDTHS),
        help="Huge block width in bits",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Spusti external-corpus benchmark CLI."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        result = run_corpus_benchmark(
            input_paths=[Path(path) for path in args.files],
            input_dir=Path(args.input_dir) if args.input_dir else None,
            recursive=args.recursive,
            max_files=args.max_files,
            width_bits=args.width_bits,
        )
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1

    print(format_corpus_table(result))
    if result.summary.roundtrip_failure_count or result.summary.error_count:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
