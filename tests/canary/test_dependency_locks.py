import sys
import tomllib
from importlib.metadata import version
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_DEV = {
    "colorama==0.4.6",
    "iniconfig==2.3.0",
    "packaging==26.0",
    "pluggy==1.6.0",
    "Pygments==2.19.2",
    "pytest==9.0.2",
    "pytest-asyncio==1.3.0",
    "typing-extensions==4.15.0",
}


def locked_lines(name):
    return {
        line.strip()
        for line in (REPO_ROOT / name).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def test_packaging_manifest_and_locks_are_exact():
    manifest = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert manifest["project"]["requires-python"] == ">=3.11,<3.14"
    assert set(manifest["project"]["optional-dependencies"]["dev"]) == EXPECTED_DEV
    assert locked_lines("requirements-dev.lock") == EXPECTED_DEV
    assert locked_lines("requirements-runtime.lock") == {"hermes-agent==0.16.0"}


def test_current_runtime_matches_matrix_pin():
    assert sys.platform == "win32"
    assert (3, 11) <= sys.version_info[:2] < (3, 14)
    assert version("hermes-agent") == "0.16.0"
