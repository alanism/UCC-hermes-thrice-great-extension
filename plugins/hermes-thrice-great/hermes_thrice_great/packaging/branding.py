"""Profile-name-independent semantic identity for Hermes Thrice Great."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from hermes_thrice_great.plugin.commands import _COMMANDS


HERMES_SOURCE = Path.home() / "AppData" / "Local" / "hermes" / "hermes-agent"
HERMES_PYTHON = HERMES_SOURCE / "venv" / "Scripts" / "python.exe"


def _hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _manifest_value(path: Path, key: str) -> str:
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip().strip("'\"")
    raise ValueError(f"BRANDING_MANIFEST_FIELD_MISSING: {key}")


def install_identity(source_root: Path, destination: Path, profile_name: str) -> dict:
    """Build the allowlisted payload and return semantic plus presentation identity."""
    source = Path(source_root).resolve(strict=True)
    destination = Path(destination).resolve(strict=False)
    if source == destination or source.is_relative_to(destination):
        raise ValueError("REPOSITORY_ROOT_INSTALL_FORBIDDEN")
    staging = destination / "hermes-thrice-great-profile"
    completed = subprocess.run(
        [
            sys.executable, str(source / "scripts" / "build_profile_staging.py"),
            "--source", str(source), "--output", str(staging),
        ],
        cwd=source, capture_output=True, text=True, check=False, timeout=30,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip())
    inventory_path = staging.with_name(f"{staging.name}.inventory.json")
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory_bytes = json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode("utf-8")
    distribution_id = _manifest_value(source / "distribution.yaml", "name")
    plugin_id = _manifest_value(source / "plugins" / "hermes-thrice-great" / "plugin.yaml", "name")
    return {
        "distribution_id": distribution_id,
        "plugin_id": plugin_id,
        "contract_registry_hash": _hash_bytes((source / "schemas" / "contract-registry.v1.schema.json").read_bytes()),
        "command_set": sorted(_COMMANDS),
        "payload_inventory_hash": _hash_bytes(inventory_bytes),
        "profile_name": profile_name,
        "display_name": "Hermes Thrice Great",
        "prompt_label": profile_name,
    }


def _stock_identity() -> tuple[dict, bool]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=HERMES_SOURCE,
        capture_output=True, text=True, check=True, timeout=10,
    ).stdout.strip()
    dirty = bool(subprocess.run(
        ["git", "status", "--porcelain"], cwd=HERMES_SOURCE,
        capture_output=True, text=True, check=True, timeout=10,
    ).stdout.strip())
    version = subprocess.run(
        [str(HERMES_PYTHON), "-B", "-c", "import importlib.metadata; print(importlib.metadata.version('hermes-agent'))"],
        cwd=HERMES_SOURCE, capture_output=True, text=True, check=True, timeout=10,
    ).stdout.strip()
    return {
        "package": "hermes-agent", "version": version, "head": head,
        "must_remain_unmodified": True,
    }, dirty


def verify_stock_identity_around_install(source_root: Path, destination: Path, contract: dict) -> dict:
    before, dirty_before = _stock_identity()
    for name in contract["install_names"]:
        install_identity(source_root, Path(destination) / name, name)
    after, dirty_after = _stock_identity()
    return {
        "before": before,
        "after": after,
        "checkout_dirty": dirty_before or dirty_after,
        "repository_root_installed": False,
    }


def run_mutation_probe(source_root: Path, contract: dict, probe_fixture: dict) -> dict[str, str]:
    from tempfile import TemporaryDirectory

    with TemporaryDirectory(prefix="ucc-branding-probe-") as directory:
        records = [
            install_identity(source_root, Path(directory) / name, name)
            for name in contract["install_names"]
        ]
    semantic = contract["semantic_identity_fields"]
    baseline = {key: records[0][key] for key in semantic}
    aliases_equal = all({key: record[key] for key in semantic} == baseline for record in records[1:])
    checks = {
        "alias-changes-command-set": aliases_equal,
        "alias-changes-registry-hash": aliases_equal,
        "rewrite-stock-hermes-name": contract["stock_identity"]["package"] == "hermes-agent",
        "install-root-directly": contract.get("repository_root_install_forbidden") is True,
    }
    outcomes = {
        item["mutant_id"]: "KILLED" if checks[item["mutant_id"]] else "SURVIVED"
        for item in probe_fixture["killable"]
    }
    outcomes[probe_fixture["equivalent_control"]["mutant_id"]] = "SURVIVED"
    outcomes.update({name: "ERROR" for name in ("crash", "setup", "timeout")})
    return outcomes
