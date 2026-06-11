"""Prvy skutocny binarny container pre huge-anchor payloady.

Format je deterministicky a repo-friendly:

- magic `PSMDLHA1`
- 1 bajt version
- unsigned varint `width_bits`
- unsigned varint `original_size`
- unsigned varint `block_count`
- model family id a family-specific parametre
- unsigned varint `search_radius`
- unsigned varint `flag_blob_length` + MSB-first flag bity
- unsigned varint `index_width`
- unsigned varint `index_count`
- unsigned varint `index_blob_length` + MSB-first packed indices
- unsigned varint `residual_count`
- unsigned varint `residual_blob_length` + residual binary blob
- unsigned varint `raw_escape_count`
- unsigned varint `raw_blob_length` + big-endian raw escape bloky
"""

from __future__ import annotations

from .bitstream import BitReader, BitWriter, decode_unsigned_varint, encode_unsigned_varint, zigzag_decode, zigzag_encode
from .huge_anchor_branch import encode_block_huge_anchor
from .huge_anchor_models import (
    HugeAnchorModel,
    SUPPORTED_HUGE_ANCHOR_FAMILIES,
    anchor_from_index,
    huge_anchor_model_from_dict,
    huge_anchor_model_bits,
    huge_anchor_parameter_bits,
)
from .huge_anchor_search import search_best_huge_anchor_model
from .huge_blocks import SUPPORTED_HUGE_WIDTHS, bytes_to_huge_blocks, huge_blocks_to_bytes
from .residual_binary import decode_residuals_binary, encode_residuals_binary
from .residual_codecs import choose_best_residual_codec, unsigned_width_for_max

_MAGIC = b"PSMDLHA1"
_VERSION = 1
_FAMILY_TO_ID = {family: index for index, family in enumerate(SUPPORTED_HUGE_ANCHOR_FAMILIES)}
_ID_TO_FAMILY = {value: key for key, value in _FAMILY_TO_ID.items()}


def encode_huge_anchor_binary(
    data: bytes,
    width_bits: int,
    model: HugeAnchorModel,
    search_radius: int = 0,
) -> bytes:
    """Zakoduje data do skutocneho huge-anchor binarneho blobu."""

    _validate_width_bits(width_bits)
    if not isinstance(search_radius, int) or search_radius < 0:
        raise ValueError("search_radius must be a non-negative integer")

    payload = bytes(data)
    blocks = bytes_to_huge_blocks(payload, width_bits)
    encoded_blocks = [encode_block_huge_anchor(block, width_bits, model, search_radius=search_radius) for block in blocks]

    flags = [bool(entry["escaped"]) for entry in encoded_blocks]
    indices = [int(entry["index"]) for entry in encoded_blocks if not entry["escaped"] and entry["index"] is not None]
    residuals = [int(entry["diff"]) for entry in encoded_blocks if not entry["escaped"]]
    raw_blocks = [int(block) for block, entry in zip(blocks, encoded_blocks) if entry["escaped"]]

    residual_codec = choose_best_residual_codec(residuals)
    residual_blob = encode_residuals_binary(residuals, codec_name=residual_codec.codec_name)
    flag_blob = _pack_flags(flags)
    index_width = unsigned_width_for_max(max(indices)) if indices else 0
    index_blob = _pack_fixed_width_values(indices, index_width, "indices")
    raw_blob = _encode_raw_blocks(raw_blocks, width_bits)

    output = bytearray()
    output.extend(_MAGIC)
    output.append(_VERSION)
    output.extend(encode_unsigned_varint(width_bits))
    output.extend(encode_unsigned_varint(len(payload)))
    output.extend(encode_unsigned_varint(len(blocks)))
    output.extend(_encode_model(model))
    output.extend(encode_unsigned_varint(search_radius))
    output.extend(encode_unsigned_varint(len(flag_blob)))
    output.extend(flag_blob)
    output.extend(encode_unsigned_varint(index_width))
    output.extend(encode_unsigned_varint(len(indices)))
    output.extend(encode_unsigned_varint(len(index_blob)))
    output.extend(index_blob)
    output.extend(encode_unsigned_varint(len(residuals)))
    output.extend(encode_unsigned_varint(len(residual_blob)))
    output.extend(residual_blob)
    output.extend(encode_unsigned_varint(len(raw_blocks)))
    output.extend(encode_unsigned_varint(len(raw_blob)))
    output.extend(raw_blob)
    return bytes(output)


def decode_huge_anchor_binary(blob: bytes) -> bytes:
    """Dekoduje huge-anchor binarny blob spat na povodne bajty."""

    payload = bytes(blob)
    if not payload.startswith(_MAGIC):
        raise ValueError("Unsupported huge-anchor binary magic")
    if len(payload) <= len(_MAGIC):
        raise ValueError("Huge-anchor binary payload is truncated")

    version = payload[len(_MAGIC)]
    if version != _VERSION:
        raise ValueError(f"Unsupported huge-anchor binary version: {version}")

    offset = len(_MAGIC) + 1
    width_bits, offset = decode_unsigned_varint(payload, offset)
    original_size, offset = decode_unsigned_varint(payload, offset)
    block_count, offset = decode_unsigned_varint(payload, offset)
    model, offset = _decode_model(payload, offset)
    search_radius, offset = decode_unsigned_varint(payload, offset)
    del search_radius

    flag_blob_length, offset = decode_unsigned_varint(payload, offset)
    flag_blob, offset = _take_bytes(payload, offset, flag_blob_length, "flag blob")
    flags = _unpack_flags(flag_blob, block_count)

    index_width, offset = decode_unsigned_varint(payload, offset)
    index_count, offset = decode_unsigned_varint(payload, offset)
    index_blob_length, offset = decode_unsigned_varint(payload, offset)
    index_blob, offset = _take_bytes(payload, offset, index_blob_length, "index blob")
    indices = _unpack_fixed_width_values(index_blob, index_count, index_width, "indices")

    residual_count, offset = decode_unsigned_varint(payload, offset)
    residual_blob_length, offset = decode_unsigned_varint(payload, offset)
    residual_blob, offset = _take_bytes(payload, offset, residual_blob_length, "residual blob")
    residuals = decode_residuals_binary(residual_blob, residual_count)

    raw_escape_count, offset = decode_unsigned_varint(payload, offset)
    raw_blob_length, offset = decode_unsigned_varint(payload, offset)
    raw_blob, offset = _take_bytes(payload, offset, raw_blob_length, "raw escape blob")
    raw_blocks = _decode_raw_blocks(raw_blob, raw_escape_count, width_bits)

    if offset != len(payload):
        raise ValueError("Huge-anchor binary payload has trailing bytes")

    escape_count = sum(1 for flag in flags if flag)
    non_escape_count = block_count - escape_count
    if escape_count != raw_escape_count:
        raise ValueError("raw escape count does not match flag stream")
    if non_escape_count != index_count:
        raise ValueError("index count does not match non-escape blocks")
    if non_escape_count != residual_count:
        raise ValueError("residual count does not match non-escape blocks")

    index_position = 0
    residual_position = 0
    raw_position = 0
    decoded_blocks: list[int] = []

    for escaped in flags:
        if escaped:
            decoded_blocks.append(raw_blocks[raw_position])
            raw_position += 1
            continue

        index = indices[index_position]
        residual = residuals[residual_position]
        index_position += 1
        residual_position += 1

        anchor = anchor_from_index(index, model, width_bits)
        if anchor is None:
            raise ValueError("Stored index cannot reconstruct a valid anchor")
        block_value = anchor + residual
        if block_value < 0 or block_value >= (1 << width_bits):
            raise ValueError("Decoded block falls outside the declared width")
        decoded_blocks.append(block_value)

    return huge_blocks_to_bytes(decoded_blocks, width_bits, original_size)


def compress_best_huge_anchor_binary(
    data: bytes,
    width_bits: int = 32,
    allow_raw_fallback: bool = True,
    actual_rerank_top_n: int = 16,
) -> dict:
    """Najde najmensi skutocny binarny blob medzi top estimated kandidatmi."""

    payload = bytes(data)
    search_result = search_best_huge_anchor_model(payload, width_bits=width_bits)
    actual_rerank_candidates = rerank_huge_anchor_candidates_by_actual_size(
        payload,
        width_bits,
        search_result,
        top_n=actual_rerank_top_n,
    )

    successful_candidates = [candidate for candidate in actual_rerank_candidates if candidate["status"] == "ok"]
    if not successful_candidates:
        raise RuntimeError("Actual-size reranking did not produce any decodable huge-anchor candidate")

    actual_winner = successful_candidates[0]
    best_model = huge_anchor_model_from_dict(actual_winner["model_dict"])
    search_radius = int(actual_winner["search_radius"])
    binary_blob = encode_huge_anchor_binary(payload, width_bits, best_model, search_radius=search_radius)
    roundtrip_ok = decode_huge_anchor_binary(binary_blob) == payload

    raw_bytes = len(payload)
    compressed_bytes = int(actual_winner["compressed_bytes"])
    raw_bits = raw_bytes * 8
    actual_bits = int(actual_winner["actual_bits"])
    decision = "compressed" if compressed_bytes < raw_bytes else "raw_fallback"
    if not allow_raw_fallback and decision == "raw_fallback":
        decision = "model_blob"

    estimated_best_key = (search_result["best_model_string"], int(search_result["search_radius"]))
    actual_best_key = (actual_winner["model"], search_radius)

    return {
        "best_model": best_model,
        "best_model_string": actual_winner["model"],
        "width_bits": width_bits,
        "search_radius": search_radius,
        "estimated_best_model": search_result["best_model"],
        "estimated_best_model_dict": dict(search_result["best_model_dict"]),
        "estimated_best_model_string": search_result["best_model_string"],
        "estimated_best_search_radius": search_result["search_radius"],
        "estimated_best_total_bits": search_result["total_bits"],
        "actual_rerank_top_n": actual_rerank_top_n,
        "actual_rerank_candidates": actual_rerank_candidates,
        "actual_rerank_changed_winner": actual_best_key != estimated_best_key,
        "raw_bytes": raw_bytes,
        "compressed_bytes": compressed_bytes,
        "raw_bits": raw_bits,
        "actual_bits": actual_bits,
        "estimated_total_bits": actual_winner["estimated_total_bits"],
        "estimated_saving_bits": actual_winner["estimated_saving_bits"],
        "actual_saving_bytes": actual_winner["actual_saving_bytes"],
        "actual_saving_bits": actual_winner["actual_saving_bits"],
        "roundtrip_ok": roundtrip_ok,
        "decision": decision,
        "estimated_decision": search_result["decision"],
        "residual_codec": actual_winner["residual_codec"],
        "escape_count": actual_winner["escape_count"],
        "binary_blob": binary_blob,
    }


def rerank_huge_anchor_candidates_by_actual_size(
    data: bytes,
    width_bits: int,
    search_result: dict,
    top_n: int = 16,
) -> list[dict]:
    """Zoradi top estimated kandidatov podla skutocnej serializovanej velkosti."""

    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("top_n must be a positive integer")

    payload = bytes(data)
    history = search_result.get("history")
    if not isinstance(history, list) or not history:
        raise ValueError("search_result must contain non-empty history")

    raw_bytes = len(payload)
    raw_bits = raw_bytes * 8
    selected_rows: list[dict] = []
    seen_identities: set[tuple[str, tuple[tuple[str, int], ...], int]] = set()

    for row in history:
        model_dict = row.get("model_dict")
        if not isinstance(model_dict, dict):
            raise ValueError("search history row is missing model_dict")
        search_radius = row.get("search_radius")
        if not isinstance(search_radius, int):
            raise ValueError("search history row has invalid search_radius")

        identity = _candidate_identity_key(model_dict, search_radius)
        if identity in seen_identities:
            continue
        seen_identities.add(identity)
        selected_rows.append(row)
        if len(selected_rows) >= top_n:
            break

    reranked: list[dict] = []
    for estimated_rank, row in enumerate(selected_rows, start=1):
        model_dict = dict(row["model_dict"])
        candidate = {
            "status": "error",
            "estimated_rank": estimated_rank,
            "model": row["model"],
            "model_dict": model_dict,
            "search_radius": int(row["search_radius"]),
            "estimated_total_bits": int(row["total_bits"]),
            "estimated_saving_bits": int(row["saving_bits"]),
            "residual_codec": row["residual_codec"],
            "escape_count": int(row["escape_count"]),
            "raw_bytes": raw_bytes,
            "raw_bits": raw_bits,
            "roundtrip_ok": False,
            "decision": "error",
        }
        try:
            model = huge_anchor_model_from_dict(model_dict)
            blob = encode_huge_anchor_binary(payload, width_bits, model, search_radius=candidate["search_radius"])
            roundtrip_ok = decode_huge_anchor_binary(blob) == payload
            if not roundtrip_ok:
                raise ValueError("Binary rerank roundtrip failed")

            compressed_bytes = len(blob)
            actual_bits = compressed_bytes * 8
            candidate.update(
                {
                    "status": "ok",
                    "compressed_bytes": compressed_bytes,
                    "actual_bits": actual_bits,
                    "actual_saving_bytes": raw_bytes - compressed_bytes,
                    "actual_saving_bits": raw_bits - actual_bits,
                    "roundtrip_ok": True,
                    "decision": "compressed" if compressed_bytes < raw_bytes else "raw_fallback",
                }
            )
        except Exception as error:  # pragma: no cover - defensive path exercised indirectly
            candidate["error"] = str(error)
        reranked.append(candidate)

    reranked.sort(
        key=lambda row: (
            0 if row["status"] == "ok" else 1,
            row.get("compressed_bytes", float("inf")),
            row["estimated_total_bits"],
            row["model"],
            row["search_radius"],
        )
    )
    return reranked


def _validate_width_bits(width_bits: int) -> None:
    """Overi, ze huge-block sirka patri medzi podporovane hodnoty."""

    if width_bits not in SUPPORTED_HUGE_WIDTHS:
        raise ValueError(f"Unsupported huge block width: {width_bits}")


def _encode_model(model: HugeAnchorModel) -> bytes:
    """Zakoduje family identifikator a jej parametre."""

    huge_anchor_model_bits(model)
    huge_anchor_parameter_bits(model)

    family = model.family
    params = dict(model.params)
    output = bytearray()
    try:
        family_id = _FAMILY_TO_ID[family]
    except KeyError as error:
        raise ValueError(f"Unsupported huge anchor family: {family}") from error

    output.extend(encode_unsigned_varint(family_id))
    if family == "linear_shift":
        output.extend(encode_unsigned_varint(int(params["shift"])))
    elif family == "affine_shift":
        output.extend(encode_unsigned_varint(int(params["shift"])))
        output.extend(encode_unsigned_varint(zigzag_encode(int(params["bias"]))))
    elif family == "multiple":
        output.extend(encode_unsigned_varint(int(params["step"])))
    elif family == "square":
        pass
    elif family == "scaled_prime":
        output.extend(encode_unsigned_varint(int(params["shift"])))
        output.extend(encode_unsigned_varint(int(params.get("search_radius", 0))))
    else:
        raise ValueError(f"Unsupported huge anchor family: {family}")
    return bytes(output)


def _decode_model(payload: bytes, offset: int) -> tuple[HugeAnchorModel, int]:
    """Dekoduje family identifikator a family-specific parametre."""

    family_id, offset = decode_unsigned_varint(payload, offset)
    family = _ID_TO_FAMILY.get(family_id)
    if family is None:
        raise ValueError(f"Unsupported huge anchor family id: {family_id}")

    if family == "linear_shift":
        shift, offset = decode_unsigned_varint(payload, offset)
        return HugeAnchorModel(family, {"shift": shift}), offset
    if family == "affine_shift":
        shift, offset = decode_unsigned_varint(payload, offset)
        bias_encoded, offset = decode_unsigned_varint(payload, offset)
        return HugeAnchorModel(family, {"shift": shift, "bias": zigzag_decode(bias_encoded)}), offset
    if family == "multiple":
        step, offset = decode_unsigned_varint(payload, offset)
        return HugeAnchorModel(family, {"step": step}), offset
    if family == "square":
        return HugeAnchorModel(family, {}), offset

    shift, offset = decode_unsigned_varint(payload, offset)
    model_search_radius, offset = decode_unsigned_varint(payload, offset)
    return HugeAnchorModel(family, {"shift": shift, "search_radius": model_search_radius}), offset


def _candidate_identity_key(model_dict: dict, search_radius: int) -> tuple[str, tuple[tuple[str, int], ...], int]:
    """Vrati hashovatelny identifikator modelu a search radiusu."""

    normalized = huge_anchor_model_from_dict(model_dict)
    return (
        normalized.family,
        tuple(sorted(normalized.params.items())),
        search_radius,
    )


def _pack_flags(flags: list[bool]) -> bytes:
    """Zabali escape flagy do MSB-first bitstreamu."""

    writer = BitWriter()
    for flag in flags:
        writer.write_bool(flag)
    return writer.to_bytes()


def _unpack_flags(blob: bytes, count: int) -> list[bool]:
    """Rozbali escape flagy z bitstreamu."""

    reader = BitReader(blob)
    flags = [reader.read_bool() for _ in range(count)]
    _validate_zero_padding(blob, count, "flag stream")
    return flags


def _pack_fixed_width_values(values: list[int], width: int, label: str) -> bytes:
    """Zabali zoznam nezapornych hodnot s fixnou bitovou sirkou."""

    if width == 0:
        if any(value != 0 for value in values):
            raise ValueError(f"{label} require non-zero width")
        return b""

    writer = BitWriter()
    for value in values:
        if value < 0:
            raise ValueError(f"{label} must be non-negative")
        writer.write_bits(value, width)
    return writer.to_bytes()


def _unpack_fixed_width_values(blob: bytes, count: int, width: int, label: str) -> list[int]:
    """Rozbali zoznam hodnot s fixnou bitovou sirkou."""

    if width == 0:
        if blob:
            raise ValueError(f"{label} with zero width must not contain bytes")
        return [0] * count

    reader = BitReader(blob)
    values = [reader.read_bits(width) for _ in range(count)]
    _validate_zero_padding(blob, count * width, label)
    return values


def _encode_raw_blocks(raw_blocks: list[int], width_bits: int) -> bytes:
    """Zakoduje raw escape bloky ako big-endian bajty."""

    width_bytes = width_bits // 8
    output = bytearray()
    for block in raw_blocks:
        if block < 0 or block >= (1 << width_bits):
            raise ValueError(f"Raw block out of range for {width_bits} bits: {block}")
        output.extend(int(block).to_bytes(width_bytes, "big"))
    return bytes(output)


def _decode_raw_blocks(blob: bytes, raw_escape_count: int, width_bits: int) -> list[int]:
    """Dekoduje raw escape bloky z big-endian bajtov."""

    width_bytes = width_bits // 8
    expected_length = raw_escape_count * width_bytes
    if len(blob) != expected_length:
        raise ValueError("raw escape blob length does not match raw_escape_count")

    blocks: list[int] = []
    for start in range(0, len(blob), width_bytes):
        blocks.append(int.from_bytes(blob[start : start + width_bytes], "big"))
    return blocks


def _take_bytes(payload: bytes, offset: int, length: int, label: str) -> tuple[bytes, int]:
    """Vrati rez `length` bajtov alebo vyhodi chybu pri orezani."""

    if offset + length > len(payload):
        raise ValueError(f"Truncated {label}")
    return payload[offset : offset + length], offset + length


def _validate_zero_padding(payload: bytes, used_bits: int, label: str) -> None:
    """Overi, ze padding za skutocnymi bitmi je nulovy."""

    total_bits = len(payload) * 8
    if used_bits > total_bits:
        raise ValueError(f"{label} is shorter than declared")
    if used_bits == total_bits:
        return

    full_bytes, used_tail_bits = divmod(used_bits, 8)
    if used_tail_bits:
        mask = (1 << (8 - used_tail_bits)) - 1
        if payload[full_bytes] & mask:
            raise ValueError(f"{label} contains non-zero padding bits")
        full_bytes += 1

    for byte_value in payload[full_bytes:]:
        if byte_value:
            raise ValueError(f"{label} contains non-zero trailing bytes")
