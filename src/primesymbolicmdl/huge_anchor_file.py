"""Súborový `.psmdl` wrapper pre huge-anchor binárnu kompresiu."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .bitstream import decode_unsigned_varint, encode_unsigned_varint
from .huge_anchor_binary import (
    _MAGIC as _HUGE_ANCHOR_MAGIC,
    compress_best_huge_anchor_binary,
    decode_huge_anchor_binary,
)

_RAW_MAGIC = b"PSMDLRAW1"
_RAW_VERSION = 1
_RAW2_MAGIC = b"PSMDLR2"
_MAX_UINT16_PAYLOAD = 65535
_LARGE_SIZE_MARKER = 0xFF


class PsmdlCompressionRefusedError(RuntimeError):
    """Vznika, ked CLI odmietne zapis, lebo kompresia nie je mensia ako raw."""


@dataclass(frozen=True)
class PsmdlCompressResult:
    """Vysledok kompresie pred zapisom do suboru."""

    file_bytes: bytes
    width_bits: int
    raw_bytes: int
    compressed_bytes: int
    decision: str
    file_format: str
    roundtrip_ok: bool
    best_model_string: str
    search_radius: int
    estimated_best_model_string: str
    actual_rerank_changed_winner: bool


def encode_raw_psmdl(data: bytes) -> bytes:
    """Zabali povodne bajty do kompaktneho raw-fallback `.psmdl` kontajnera."""

    payload = bytes(data)
    original_size = len(payload)
    output = bytearray()
    output.extend(_RAW2_MAGIC)
    if original_size <= _MAX_UINT16_PAYLOAD:
        output.extend(original_size.to_bytes(2, "big"))
    else:
        output.append(_LARGE_SIZE_MARKER)
        output.extend(original_size.to_bytes(4, "big"))
    output.extend(payload)
    return bytes(output)


def decode_raw_psmdl_v1(blob: bytes) -> bytes:
    """Dekoduje legacy `PSMDLRAW1` raw-fallback kontajner."""

    payload = bytes(blob)
    if not payload.startswith(_RAW_MAGIC):
        raise ValueError("Unsupported raw .psmdl magic")
    if len(payload) <= len(_RAW_MAGIC):
        raise ValueError("Raw .psmdl payload is truncated")

    version = payload[len(_RAW_MAGIC)]
    if version != _RAW_VERSION:
        raise ValueError(f"Unsupported raw .psmdl version: {version}")

    offset = len(_RAW_MAGIC) + 1
    original_size, offset = decode_unsigned_varint(payload, offset)
    if offset + original_size > len(payload):
        raise ValueError("Truncated raw .psmdl payload")
    if offset + original_size < len(payload):
        raise ValueError("Raw .psmdl payload has trailing bytes")

    return payload[offset : offset + original_size]


def decode_raw_psmdl_v2(blob: bytes) -> bytes:
    """Dekoduje kompaktny `PSMDLR2` raw-fallback kontajner."""

    payload = bytes(blob)
    if not payload.startswith(_RAW2_MAGIC):
        raise ValueError("Unsupported compact raw .psmdl magic")
    if len(payload) <= len(_RAW2_MAGIC):
        raise ValueError("Compact raw .psmdl payload is truncated")

    offset = len(_RAW2_MAGIC)
    if offset + 2 > len(payload):
        raise ValueError("Truncated compact raw .psmdl size field")

    if payload[offset] == _LARGE_SIZE_MARKER:
        offset += 1
        if offset + 4 > len(payload):
            raise ValueError("Truncated compact raw .psmdl large size field")
        original_size = int.from_bytes(payload[offset : offset + 4], "big")
        offset += 4
    else:
        original_size = int.from_bytes(payload[offset : offset + 2], "big")
        offset += 2

    if offset + original_size > len(payload):
        raise ValueError("Truncated compact raw .psmdl payload")
    if offset + original_size < len(payload):
        raise ValueError("Compact raw .psmdl payload has trailing bytes")

    return payload[offset : offset + original_size]


def decode_raw_psmdl(blob: bytes) -> bytes:
    """Dekoduje raw-fallback `.psmdl` kontajner (legacy alebo kompaktny)."""

    payload = bytes(blob)
    if payload.startswith(_RAW2_MAGIC):
        return decode_raw_psmdl_v2(payload)
    if payload.startswith(_RAW_MAGIC):
        return decode_raw_psmdl_v1(payload)
    raise ValueError("Unsupported raw .psmdl magic")


def raw_psmdl_container_overhead(raw_bytes: int) -> int:
    """Vrati pocet bajtov naviac oproti raw payloadu pre aktualny raw kontajner."""

    if raw_bytes <= _MAX_UINT16_PAYLOAD:
        return len(_RAW2_MAGIC) + 2
    return len(_RAW2_MAGIC) + 1 + 4


def decode_psmdl_bytes(blob: bytes) -> bytes:
    """Dekoduje `.psmdl` subor bez ohladu na to, ci ide o huge-anchor alebo raw fallback."""

    payload = bytes(blob)
    if payload.startswith(_HUGE_ANCHOR_MAGIC):
        return decode_huge_anchor_binary(payload)
    if payload.startswith(_RAW2_MAGIC) or payload.startswith(_RAW_MAGIC):
        return decode_raw_psmdl(payload)
    raise ValueError("Unsupported .psmdl file magic")


def compress_to_psmdl_bytes(
    data: bytes,
    width_bits: int = 32,
    *,
    require_compression: bool = False,
    actual_rerank_top_n: int = 16,
) -> PsmdlCompressResult:
    """Skomprimuje bajty do `.psmdl` reprezentacie s uctivym raw fallbackom."""

    payload = bytes(data)
    search_result = compress_best_huge_anchor_binary(
        payload,
        width_bits=width_bits,
        allow_raw_fallback=True,
        actual_rerank_top_n=actual_rerank_top_n,
    )

    if search_result["decision"] == "compressed":
        file_bytes = bytes(search_result["binary_blob"])
        file_format = "huge_anchor"
        decision = "compressed"
    elif require_compression:
        raise PsmdlCompressionRefusedError(
            "Huge-anchor binary blob is not smaller than raw input; refusing to write output"
        )
    else:
        file_bytes = encode_raw_psmdl(payload)
        file_format = "raw_fallback"
        decision = "raw_fallback"

    roundtrip_ok = decode_psmdl_bytes(file_bytes) == payload
    if not roundtrip_ok:
        raise RuntimeError("PSMDL compress roundtrip verification failed")

    return PsmdlCompressResult(
        file_bytes=file_bytes,
        width_bits=width_bits,
        raw_bytes=len(payload),
        compressed_bytes=len(file_bytes),
        decision=decision,
        file_format=file_format,
        roundtrip_ok=roundtrip_ok,
        best_model_string=str(search_result["best_model_string"]),
        search_radius=int(search_result["search_radius"]),
        estimated_best_model_string=str(search_result["estimated_best_model_string"]),
        actual_rerank_changed_winner=bool(search_result["actual_rerank_changed_winner"]),
    )


def compress_file(
    input_path: str | Path,
    output_path: str | Path,
    *,
    width_bits: int = 32,
    require_compression: bool = False,
    actual_rerank_top_n: int = 16,
) -> PsmdlCompressResult:
    """Precita vstupny subor, zapise `.psmdl` vystup a overi presny roundtrip."""

    source = Path(input_path)
    destination = Path(output_path)
    payload = source.read_bytes()
    result = compress_to_psmdl_bytes(
        payload,
        width_bits=width_bits,
        require_compression=require_compression,
        actual_rerank_top_n=actual_rerank_top_n,
    )
    destination.write_bytes(result.file_bytes)
    return result


def decompress_file(input_path: str | Path, output_path: str | Path) -> bytes:
    """Dekoduje `.psmdl` subor a zapise obnovene bajty."""

    source = Path(input_path)
    destination = Path(output_path)
    restored = decode_psmdl_bytes(source.read_bytes())
    destination.write_bytes(restored)
    return restored
