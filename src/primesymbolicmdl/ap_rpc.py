"""File-based Coordinator Protocol RPC helpers."""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

DEFAULT_MAX_BYTES = 40_000
FORBIDDEN_BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".mp4",
    ".mov",
    ".zip",
    ".db",
    ".sqlite",
    ".pyc",
}
FORBIDDEN_PATH_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache"}
LISTING_SKIP_PARTS = FORBIDDEN_PATH_PARTS | {".ap"}


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _new_request_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}_{secrets.token_hex(4)}"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def ensure_rpc_directories(repo_root: Path) -> dict[str, Path]:
    rpc_root = repo_root / ".ap" / "rpc"
    inbox = rpc_root / "inbox"
    outbox = rpc_root / "outbox"
    archive = rpc_root / "archive"
    for path in (inbox, outbox, archive):
        path.mkdir(parents=True, exist_ok=True)
    return {"rpc_root": rpc_root, "inbox": inbox, "outbox": outbox, "archive": archive}


def is_forbidden_file_path(path: str) -> bool:
    pure_path = PurePosixPath(path)
    lower_parts = {part.lower() for part in pure_path.parts}
    if lower_parts & FORBIDDEN_PATH_PARTS:
        return True
    return pure_path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES


def validate_repo_relative_path(path: str) -> None:
    if not path or path in {".", "./"}:
        raise ValueError("Path must point to a repository file.")
    pure_path = PurePosixPath(path)
    if pure_path.is_absolute():
        raise ValueError("Absolute paths are forbidden.")
    if any(part == ".." for part in pure_path.parts):
        raise ValueError("Parent path traversal is forbidden.")
    if is_forbidden_file_path(path):
        raise ValueError(f"Forbidden file path: {path}")


def build_request(
    method: str,
    params: dict[str, Any] | None = None,
    *,
    from_role: str = "ORCHESTRATOR",
    to_role: str = "WORKER",
    request_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    if not method:
        raise ValueError("RPC method is required.")
    request_params = dict(params or {})
    if method == "repo.get_file":
        if "path" not in request_params:
            raise ValueError("repo.get_file requires a path parameter.")
        validate_repo_relative_path(str(request_params["path"]))
        if "max_bytes" in request_params:
            request_params["max_bytes"] = _normalize_max_bytes(request_params["max_bytes"])
    return {
        "id": request_id or _new_request_id(),
        "type": "rpc_request",
        "from": from_role,
        "to": to_role,
        "method": method,
        "params": request_params,
        "created_at": created_at or _now_iso(),
    }


def build_response(
    request_id: str,
    method: str,
    *,
    status: str,
    result: dict[str, Any] | None = None,
    error: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    return {
        "id": request_id,
        "type": "rpc_response",
        "status": status,
        "method": method,
        "result": result if status == "ok" else None,
        "error": error if status == "error" else None,
        "created_at": created_at or _now_iso(),
    }


def _normalize_max_bytes(raw_value: Any) -> int:
    try:
        max_bytes = int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("max_bytes must be an integer.") from exc
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive.")
    return max_bytes


def _run_git_command(repo_root: Path, *args: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("git is not available in PATH.") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or f"git {' '.join(args)} failed."
        raise RuntimeError(message) from exc
    return completed.stdout.rstrip("\n")


def _is_hidden_from_listing(path: str) -> bool:
    parts = {part.lower() for part in PurePosixPath(path).parts}
    return bool(parts & LISTING_SKIP_PARTS)


def _fallback_list_files(repo_root: Path) -> list[str]:
    files: list[str] = []
    for candidate in repo_root.rglob("*"):
        if not candidate.is_file():
            continue
        relative = candidate.relative_to(repo_root).as_posix()
        if _is_hidden_from_listing(relative):
            continue
        files.append(relative)
    return sorted(set(files))


def _repo_status(repo_root: Path) -> dict[str, Any]:
    return {
        "branch": _run_git_command(repo_root, "branch", "--show-current"),
        "head": _run_git_command(repo_root, "rev-parse", "HEAD"),
        "status_short": _run_git_command(repo_root, "status", "--short"),
    }


def _repo_diff_stat(repo_root: Path) -> dict[str, Any]:
    return {"diff_stat": _run_git_command(repo_root, "diff", "--stat")}


def _repo_list_files(repo_root: Path) -> dict[str, Any]:
    try:
        tracked = _run_git_command(repo_root, "ls-files").splitlines()
        untracked = _run_git_command(repo_root, "ls-files", "--others", "--exclude-standard").splitlines()
        files = sorted(
            {
                path
                for path in tracked + untracked
                if path and not _is_hidden_from_listing(path)
            }
        )
    except RuntimeError:
        files = _fallback_list_files(repo_root)
    return {"files": files}


def _resolve_repo_path(repo_root: Path, relative_path: str) -> Path:
    validate_repo_relative_path(relative_path)
    candidate = (repo_root / PurePosixPath(relative_path)).resolve(strict=False)
    resolved_root = repo_root.resolve()
    if not candidate.is_relative_to(resolved_root):
        raise ValueError("Resolved path escapes the repository root.")
    return candidate


def _repo_get_file(repo_root: Path, params: dict[str, Any]) -> dict[str, Any]:
    path = str(params.get("path") or "")
    max_bytes = _normalize_max_bytes(params.get("max_bytes", DEFAULT_MAX_BYTES))
    candidate = _resolve_repo_path(repo_root, path)
    if not candidate.exists():
        raise FileNotFoundError(f"Repository file does not exist: {path}")
    if not candidate.is_file():
        raise ValueError(f"Repository path is not a file: {path}")
    data = candidate.read_bytes()
    excerpt = data[:max_bytes].decode("utf-8", errors="replace")
    return {
        "path": path,
        "content": excerpt,
        "size_bytes": len(data),
        "truncated": len(data) > max_bytes,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def handle_request(request: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    request_id = str(request.get("id") or "unknown_request")
    method = str(request.get("method") or "")
    try:
        if request.get("type") != "rpc_request":
            raise ValueError('Request type must be "rpc_request".')
        params = request.get("params") or {}
        if not isinstance(params, dict):
            raise ValueError("Request params must be a JSON object.")
        if method == "repo.status":
            result = _repo_status(repo_root)
        elif method == "repo.diff_stat":
            result = _repo_diff_stat(repo_root)
        elif method == "repo.list_files":
            result = _repo_list_files(repo_root)
        elif method == "repo.get_file":
            result = _repo_get_file(repo_root, params)
        else:
            raise ValueError(f"Unknown RPC method: {method}")
        return build_response(request_id, method, status="ok", result=result)
    except Exception as exc:
        return build_response(request_id, method, status="error", error=str(exc))


def _load_request_file(request_path: Path) -> dict[str, Any]:
    raw_payload = json.loads(request_path.read_text(encoding="utf-8"))
    if not isinstance(raw_payload, dict):
        raise ValueError("Request JSON root must be an object.")
    return raw_payload


def _pick_oldest_request(inbox_dir: Path) -> Path | None:
    candidates = list(inbox_dir.glob("*.json"))
    if not candidates:
        return None
    return sorted(candidates, key=lambda path: (path.stat().st_mtime, path.name))[0]


def create_request_file(
    repo_root: Path,
    method: str,
    *,
    path: str | None = None,
    max_bytes: int | None = None,
) -> dict[str, Any]:
    directories = ensure_rpc_directories(repo_root)
    params: dict[str, Any] = {}
    if path is not None:
        params["path"] = path
    if max_bytes is not None:
        params["max_bytes"] = max_bytes
    request = build_request(method, params)
    request_path = directories["inbox"] / f"{request['id']}.json"
    _write_json(request_path, request)
    return {
        "request_id": request["id"],
        "request_path": str(request_path.resolve()),
    }


def handle_request_file(repo_root: Path, request_path: Path | None = None) -> dict[str, Any]:
    directories = ensure_rpc_directories(repo_root)
    selected_request = request_path or _pick_oldest_request(directories["inbox"])
    if selected_request is None:
        raise FileNotFoundError("No RPC request file found in .ap/rpc/inbox.")

    selected_request = selected_request.resolve(strict=False)
    request_id = selected_request.stem
    method = ""

    try:
        request = _load_request_file(selected_request)
        request.setdefault("id", request_id)
        method = str(request.get("method") or "")
        response = handle_request(request, repo_root)
    except Exception as exc:
        response = build_response(
            request_id,
            method,
            status="error",
            error=f"Invalid request file: {exc}",
        )

    response_path = directories["outbox"] / f"{request_id}.json"
    _write_json(response_path, response)

    archive_path: Path | None = None
    if selected_request.exists():
        archive_path = directories["archive"] / f"{request_id}.json"
        if selected_request != archive_path:
            shutil.move(str(selected_request), str(archive_path))
        else:
            archive_path = selected_request

    return {
        "request_id": request_id,
        "request_path": str(selected_request),
        "response_path": str(response_path.resolve()),
        "archive_path": str(archive_path.resolve()) if archive_path is not None else None,
        "response_status": str(response["status"]),
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Coordinator Protocol RPC helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    request_parser = subparsers.add_parser("request", help="Create an RPC request file.")
    request_parser.add_argument("--repo-root", default=".", help="Repository root directory.")
    request_parser.add_argument("--method", required=True, help="RPC method name.")
    request_parser.add_argument("--path", help="Repository-relative file path.")
    request_parser.add_argument("--max-bytes", type=int, help="Optional truncation limit.")

    handle_parser = subparsers.add_parser("handle", help="Handle one RPC request file.")
    handle_parser.add_argument("--repo-root", default=".", help="Repository root directory.")
    handle_parser.add_argument("--request", help="Explicit request file path.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        if args.command == "request":
            payload = create_request_file(
                repo_root,
                args.method,
                path=args.path,
                max_bytes=args.max_bytes,
            )
        else:
            request_path = Path(args.request) if args.request else None
            payload = handle_request_file(repo_root, request_path)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
