from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest

from primesymbolicmdl.ap_rpc import build_request, handle_request, validate_repo_relative_path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_build_request_contains_required_metadata() -> None:
    request = build_request("repo.get_file", {"path": "AP.md", "max_bytes": 1234})

    assert request["id"]
    assert request["type"] == "rpc_request"
    assert request["from"] == "ORCHESTRATOR"
    assert request["to"] == "WORKER"
    assert request["method"] == "repo.get_file"
    assert request["params"] == {"path": "AP.md", "max_bytes": 1234}
    assert request["created_at"]


def test_validate_repo_relative_path_allows_safe_relative_file() -> None:
    validate_repo_relative_path("AP.md")


@pytest.mark.parametrize(
    "bad_path",
    [
        "/etc/passwd",
        "../secret.txt",
        ".git/config",
        ".venv/bin/python",
        "image.png",
        "cache/module.pyc",
    ],
)
def test_validate_repo_relative_path_rejects_forbidden_inputs(bad_path: str) -> None:
    with pytest.raises(ValueError):
        validate_repo_relative_path(bad_path)


def test_repo_get_file_returns_sha_and_truncation(tmp_path: Path) -> None:
    sample = tmp_path / "notes.txt"
    content = "alpha-beta-gamma-delta"
    sample.write_text(content, encoding="utf-8")
    request = {
        "id": "demo-request",
        "type": "rpc_request",
        "from": "ORCHESTRATOR",
        "to": "WORKER",
        "method": "repo.get_file",
        "params": {"path": "notes.txt", "max_bytes": 5},
        "created_at": "2026-06-11T20:00:00+02:00",
    }

    response = handle_request(request, tmp_path)

    assert response["status"] == "ok"
    assert response["result"] == {
        "path": "notes.txt",
        "content": "alpha",
        "size_bytes": len(content.encode("utf-8")),
        "truncated": True,
        "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
    }


def test_unknown_method_returns_error_response(tmp_path: Path) -> None:
    request = {
        "id": "unknown-request",
        "type": "rpc_request",
        "from": "ORCHESTRATOR",
        "to": "WORKER",
        "method": "repo.unknown",
        "params": {},
        "created_at": "2026-06-11T20:00:00+02:00",
    }

    response = handle_request(request, tmp_path)

    assert response["status"] == "error"
    assert "Unknown RPC method" in response["error"]


def test_ap_rpc_call_fish_smoke() -> None:
    if shutil.which("fish") is None:
        pytest.skip("fish is not available")

    completed = subprocess.run(
        ["fish", "scripts/ap_rpc_call.fish", "--method", "repo.status"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "RESPONSE_STATUS=ok" in completed.stdout
    assert "RESPONSE_PATH=" in completed.stdout
