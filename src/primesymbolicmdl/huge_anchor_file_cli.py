"""CLI pre huge-anchor `.psmdl` kompresiu a dekompresiu suborov."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .huge_anchor_file import PsmdlCompressionRefusedError, compress_file, decompress_file
from .huge_blocks import SUPPORTED_HUGE_WIDTHS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PrimeSymbolicMDL huge-anchor file compression and decompression.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    compress_parser = subparsers.add_parser("compress", help="Compress an input file to .psmdl")
    compress_parser.add_argument("--input", required=True, help="Path to the raw input file")
    compress_parser.add_argument("--output", required=True, help="Path to the output .psmdl file")
    compress_parser.add_argument(
        "--width-bits",
        type=int,
        default=32,
        choices=sorted(SUPPORTED_HUGE_WIDTHS),
        help="Huge block width in bits",
    )
    compress_parser.add_argument(
        "--require-compression",
        action="store_true",
        help="Refuse to write output when the huge-anchor blob is not smaller than raw",
    )
    compress_parser.add_argument(
        "--actual-rerank-top-n",
        type=int,
        default=16,
        help="How many estimated candidates to rerank by actual serialized size",
    )

    decompress_parser = subparsers.add_parser("decompress", help="Decompress a .psmdl file")
    decompress_parser.add_argument("--input", required=True, help="Path to the input .psmdl file")
    decompress_parser.add_argument("--output", required=True, help="Path to the restored output file")
    return parser


def _format_compress_summary(result) -> str:
    return (
        f"decision={result.decision} "
        f"file_format={result.file_format} "
        f"width_bits={result.width_bits} "
        f"raw_bytes={result.raw_bytes} "
        f"compressed_bytes={result.compressed_bytes} "
        f"roundtrip_ok={result.roundtrip_ok} "
        f"best_model={result.best_model_string} "
        f"search_radius={result.search_radius}"
    )


def main(argv: list[str] | None = None) -> int:
    """Spusti CLI pre compress alebo decompress."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "compress":
            result = compress_file(
                args.input,
                args.output,
                width_bits=args.width_bits,
                require_compression=args.require_compression,
                actual_rerank_top_n=args.actual_rerank_top_n,
            )
            print(_format_compress_summary(result))
            return 0

        decompress_file(args.input, args.output)
        print(f"restored_bytes={Path(args.output).stat().st_size}")
        return 0
    except PsmdlCompressionRefusedError as error:
        print(str(error), file=sys.stderr)
        return 2
    except (ValueError, RuntimeError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
