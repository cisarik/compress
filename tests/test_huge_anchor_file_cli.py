import subprocess
import sys
from pathlib import Path

import pytest

from primesymbolicmdl.huge_anchor_datasets import make_huge_anchor_dataset
from primesymbolicmdl.huge_anchor_file import (
    PsmdlCompressionRefusedError,
    compress_file,
    compress_to_psmdl_bytes,
    decode_psmdl_bytes,
    decompress_file,
    encode_raw_psmdl,
)
from primesymbolicmdl.huge_anchor_file_cli import main as cli_main


def test_compress_to_psmdl_bytes_roundtrips_square_generated() -> None:
    data = make_huge_anchor_dataset("square_generated", 64, count=32, seed=1234)
    result = compress_to_psmdl_bytes(data, width_bits=64)

    assert result.roundtrip_ok is True
    assert decode_psmdl_bytes(result.file_bytes) == data
    assert result.decision == "compressed"
    assert result.file_format == "huge_anchor"
    assert result.compressed_bytes < result.raw_bytes


def test_compress_to_psmdl_bytes_uses_raw_fallback_for_random_data() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    result = compress_to_psmdl_bytes(data, width_bits=32)

    assert result.roundtrip_ok is True
    assert decode_psmdl_bytes(result.file_bytes) == data
    assert result.decision == "raw_fallback"
    assert result.file_format == "raw_fallback"
    assert result.compressed_bytes >= result.raw_bytes


def test_compress_to_psmdl_bytes_can_refuse_non_winning_compression() -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)

    with pytest.raises(PsmdlCompressionRefusedError, match="not smaller than raw"):
        compress_to_psmdl_bytes(data, width_bits=32, require_compression=True)


def test_encode_raw_psmdl_roundtrips() -> None:
    data = b"hello-psmdl-raw-fallback"

    assert decode_psmdl_bytes(encode_raw_psmdl(data)) == data


def test_temp_file_cli_roundtrip_for_square_generated(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("square_generated", 32, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    restored_path = tmp_path / "restored.bin"
    input_path.write_bytes(data)

    result = compress_file(input_path, psmdl_path, width_bits=32)
    assert result.roundtrip_ok is True
    assert psmdl_path.exists()

    restored = decompress_file(psmdl_path, restored_path)
    assert restored == data
    assert restored_path.read_bytes() == data


def test_temp_file_cli_roundtrip_for_random_bytes_with_raw_fallback(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    restored_path = tmp_path / "restored.bin"
    input_path.write_bytes(data)

    result = compress_file(input_path, psmdl_path, width_bits=32)
    assert result.decision == "raw_fallback"
    assert result.file_format == "raw_fallback"

    restored = decompress_file(psmdl_path, restored_path)
    assert restored == data


def test_cli_module_compress_and_decompress_roundtrip(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("linear_shift_generated", 16, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    restored_path = tmp_path / "restored.bin"
    input_path.write_bytes(data)

    exit_code = cli_main(
        [
            "compress",
            "--input",
            str(input_path),
            "--output",
            str(psmdl_path),
            "--width-bits",
            "16",
        ]
    )
    assert exit_code == 0
    assert psmdl_path.exists()

    exit_code = cli_main(
        [
            "decompress",
            "--input",
            str(psmdl_path),
            "--output",
            str(restored_path),
        ]
    )
    assert exit_code == 0
    assert restored_path.read_bytes() == data


def test_cli_refuses_compression_when_required_and_no_win(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("random_bytes", 32, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    input_path.write_bytes(data)

    exit_code = cli_main(
        [
            "compress",
            "--input",
            str(input_path),
            "--output",
            str(psmdl_path),
            "--width-bits",
            "32",
            "--require-compression",
        ]
    )
    assert exit_code == 2
    assert not psmdl_path.exists()


def test_subprocess_cli_roundtrip(tmp_path: Path) -> None:
    data = make_huge_anchor_dataset("multiple_generated", 32, count=32, seed=1234)
    input_path = tmp_path / "input.bin"
    psmdl_path = tmp_path / "output.psmdl"
    restored_path = tmp_path / "restored.bin"
    input_path.write_bytes(data)

    compress = subprocess.run(
        [
            sys.executable,
            "-m",
            "primesymbolicmdl.huge_anchor_file_cli",
            "compress",
            "--input",
            str(input_path),
            "--output",
            str(psmdl_path),
            "--width-bits",
            "32",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert compress.returncode == 0, compress.stderr

    decompress = subprocess.run(
        [
            sys.executable,
            "-m",
            "primesymbolicmdl.huge_anchor_file_cli",
            "decompress",
            "--input",
            str(psmdl_path),
            "--output",
            str(restored_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert decompress.returncode == 0, decompress.stderr
    assert restored_path.read_bytes() == data
