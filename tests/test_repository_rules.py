from pathlib import Path


def test_no_local_pytest_shim_exists() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    assert not (repo_root / "pytest").exists()
