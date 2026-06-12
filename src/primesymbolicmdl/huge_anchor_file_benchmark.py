"""Deterministicky benchmark pre `.psmdl` file CLI bez univerzalnych tvrdeni."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

from .huge_anchor_datasets import make_huge_anchor_dataset
from .huge_anchor_file import PsmdlCompressionRefusedError, compress_file, decompress_file


@dataclass(frozen=True)
class BenchmarkRow:
    """Jeden riadok honest actual-size benchmarku."""

    name: str
    raw_bytes: int
    psmdl_bytes: int
    decision: str
    file_format: str
    roundtrip_ok: bool
    require_compression: str
    note: str = ""


def _benchmark_one(
    name: str,
    data: bytes,
    *,
    width_bits: int = 32,
    note: str = "",
) -> BenchmarkRow:
    """Skomprimuje jeden vstup do docasneho suboru a overi roundtrip."""

    with tempfile.TemporaryDirectory(prefix="psmdl-bench-") as tmp_dir:
        tmp = Path(tmp_dir)
        input_path = tmp / "input.bin"
        psmdl_path = tmp / "output.psmdl"
        restored_path = tmp / "restored.bin"
        input_path.write_bytes(data)

        result = compress_file(input_path, psmdl_path, width_bits=width_bits)
        restored = decompress_file(psmdl_path, restored_path)
        roundtrip_ok = restored == data

        require_status = "ok"
        try:
            refused_path = tmp / "refused.psmdl"
            compress_file(input_path, refused_path, width_bits=width_bits, require_compression=True)
            if result.decision != "compressed":
                require_status = "unexpected_ok"
        except PsmdlCompressionRefusedError:
            if result.decision == "compressed":
                require_status = "unexpected_refused"
            else:
                require_status = "refused"
        except Exception as error:  # pragma: no cover - defensive
            require_status = f"error:{error}"

        return BenchmarkRow(
            name=name,
            raw_bytes=len(data),
            psmdl_bytes=result.compressed_bytes,
            decision=result.decision,
            file_format=result.file_format,
            roundtrip_ok=roundtrip_ok,
            require_compression=require_status,
            note=note,
        )


def run_benchmark() -> list[BenchmarkRow]:
    """Spusti maly deterministicky benchmark nad repozitarnymi a syntetickymi vstupmi."""

    repo_root = Path(__file__).resolve().parents[2]
    rows: list[BenchmarkRow] = []

    rows.append(
        _benchmark_one(
            "random_bytes_128",
            make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234),
            note="deterministic random sanity",
        )
    )
    rows.append(
        _benchmark_one(
            "repeating_pattern",
            make_huge_anchor_dataset("repeating_pattern", 32, count=32, seed=1234),
            note="ABCD repeat",
        )
    )

    for rel_path in ("README.md", "AGENTS.md"):
        source = repo_root / rel_path
        rows.append(
            _benchmark_one(
                rel_path,
                source.read_bytes(),
                note="repo text file",
            )
        )

    py_source = repo_root / "src" / "primesymbolicmdl" / "huge_anchor_file.py"
    rows.append(
        _benchmark_one(
            "src/primesymbolicmdl/huge_anchor_file.py",
            py_source.read_bytes(),
            note="repo python source",
        )
    )
    rows.append(
        _benchmark_one(
            "square_generated_64",
            make_huge_anchor_dataset("square_generated", 64, count=32, seed=1234),
            width_bits=64,
            note="synthetic structure-compatible dataset",
        )
    )
    return rows


def format_benchmark_table(rows: list[BenchmarkRow]) -> str:
    """Vrati citatelnu tabulku actual byte sizes."""

    header = (
        "name | raw_bytes | psmdl_bytes | decision | file_format | roundtrip_ok | require_compression | note"
    )
    lines = [header, "-" * len(header)]
    for row in rows:
        lines.append(
            f"{row.name} | {row.raw_bytes} | {row.psmdl_bytes} | {row.decision} | "
            f"{row.file_format} | {row.roundtrip_ok} | {row.require_compression} | {row.note}"
        )
    return "\n".join(lines)


def main() -> None:
    """Vypise honest benchmark tabulku do stdout."""

    print(format_benchmark_table(run_benchmark()))


if __name__ == "__main__":
    main()
