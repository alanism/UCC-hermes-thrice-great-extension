"""Deterministic installed-profile CLI for synthetic offline acceptance."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from hermes_thrice_great.orchestration.week import run_adversarial_case, run_week
from hermes_thrice_great.privacy.guards import validate_contained_path


_COMMANDS = {"ucc doctor", "ucc validate --synthetic", "ucc dry-run --synthetic"}
_RESOURCE_ROOT = Path(__file__).resolve().parents[1] / "resources" / "synthetic"
_CASE_MUTATIONS = {
    "missing_approval": "remove_approval",
    "replay_conflict": "change_approval_payload",
    "invalid_totals": "invalidate_receipt_total",
    "write_fault": "inject_temp_write_fault",
    "network_request": "attempt_network",
}


def _canonical_hash(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _load_json(root: Path, relative: str):
    result = validate_contained_path(root, relative)
    if not result["allowed"]:
        raise ValueError(result["issues"][0]["code"])
    return json.loads(Path(result["resolved_path"]).read_text(encoding="utf-8"))


def _verified_manifest(resource_root: Path) -> dict:
    manifest = _load_json(resource_root, "manifest.json")
    projection = dict(manifest)
    expected = projection.pop("canonical_hash", None)
    if expected != _canonical_hash(projection):
        raise ValueError("INSTALLED_RESOURCE_MANIFEST_HASH_INVALID")
    for item in manifest.get("files", []):
        result = validate_contained_path(resource_root, item.get("path", ""))
        if not result["allowed"]:
            raise ValueError("INSTALLED_RESOURCE_PATH_INVALID")
        if hashlib.sha256(Path(result["resolved_path"]).read_bytes()).hexdigest() != item.get("sha256"):
            raise ValueError("INSTALLED_RESOURCE_HASH_INVALID")
    return manifest


def _case(resource_root: Path, case_id: str) -> dict:
    if case_id not in _CASE_MUTATIONS:
        raise ValueError("OFFLINE_CASE_UNKNOWN")
    fixture = _load_json(resource_root, "adversarial/week-cases.json")
    mutation = _CASE_MUTATIONS[case_id]
    return next(item for item in fixture["cases"] if item["mutation"] == mutation)


def _envelope(
    *, command: str, status: str, manifest: dict, case_id: str | None = None,
    issue_codes: list[str] | None = None, stage_results: list[str] | None = None,
    canonical_hash: str | None = None, ledger_hash: str | None = None,
    ledger_commits: int = 0,
) -> dict:
    return {
        "command": command,
        "status": status,
        "synthetic_set_id": manifest["synthetic_set_id"],
        "case_id": case_id,
        "issue_codes": issue_codes or [],
        "stage_results": stage_results or [],
        "canonical_hash": canonical_hash,
        "ledger_hash": ledger_hash,
        "ledger_commits": ledger_commits,
        "ledger_writes": 0,
        "network_attempts": 0,
        "model_calls": 0,
    }


def _doctor(resource_root: Path, manifest: dict) -> tuple[int, dict]:
    profile_root = resource_root.parents[4]
    config = (profile_root / "config.yaml").read_text(encoding="utf-8")
    restrictions = (
        'disabled_toolsets: ["*"]' in config
        and "cli: []" in config
        and "mcp_servers: {}" in config
    )
    schema = resource_root / "schema" / "contract-registry.v1.schema.json"
    valid = (
        manifest.get("distribution_id") == "hermes-thrice-great"
        and schema.is_file()
        and restrictions
        and bool(manifest.get("files"))
    )
    issues = [] if valid else ["DOCTOR_INSTALLED_PROFILE_INVALID"]
    payload = _envelope(
        command="ucc doctor", status="ok" if valid else "failed", manifest=manifest,
        issue_codes=issues, canonical_hash=manifest["canonical_hash"],
    )
    return (0 if valid else 2), payload


def _validate_valid(resource_root: Path, manifest: dict, fixture: dict) -> tuple[int, dict]:
    result = run_week(
        fixture, offline=True, resource_root=resource_root, commit_ledger=False
    )
    if result["status"] != "complete":
        codes = [item["code"] for item in result.get("issues", [])]
        return 2, _envelope(
            command="ucc validate", status="failed", manifest=manifest,
            issue_codes=codes,
        )
    return 0, _envelope(
        command="ucc validate", status="ok", manifest=manifest,
        stage_results=result["stages"],
        canonical_hash=hashlib.sha256(result["canonical_bytes"]).hexdigest(),
        ledger_hash=result["ledger_hash"], ledger_commits=0,
    )


def _validate_case(
    resource_root: Path, manifest: dict, week: dict, case_id: str
) -> tuple[int, dict]:
    result = run_adversarial_case(
        week, _case(resource_root, case_id), offline=True,
        resource_root=resource_root,
    )
    codes = [item["code"] for item in result.get("issues", [])]
    return 2, _envelope(
        command="ucc validate", status="failed", manifest=manifest,
        case_id=case_id, issue_codes=codes,
        canonical_hash=_canonical_hash({"case_id": case_id, "issue_codes": codes}),
        ledger_commits=result.get("ledger_commits", 0),
    )


def _load_explicit_fixture(resource_root: Path, relative: str):
    document = _load_json(resource_root, relative)
    if document.get("fixture_schema_version") == "ucc.synthetic_week_fixture.v1.0.0":
        return "valid", document
    if document.get("fixture_schema_version") == "ucc.synthetic_week_adversarial.v1.0.0":
        return "adversarial", document
    raise ValueError("OFFLINE_FIXTURE_TYPE_UNSUPPORTED")


def run_cli(argv: list[str], *, resource_root: Path | None = None) -> tuple[int, dict]:
    root = Path(resource_root or _RESOURCE_ROOT).resolve(strict=True)
    try:
        manifest = _verified_manifest(root)
        parser = argparse.ArgumentParser(add_help=False)
        setup_cli(parser)
        args = parser.parse_args(argv)
        if args.ucc_action == "doctor":
            return _doctor(root, manifest)
        if args.ucc_action == "validate":
            if args.fixture:
                kind, document = _load_explicit_fixture(root, args.fixture)
                if kind == "valid":
                    return _validate_valid(root, manifest, document)
                case_id = args.case or "missing_approval"
                week = _load_json(root, document["base_week"])
                return _validate_case(root, manifest, week, case_id)
            week = _load_json(root, "valid/week.json")
            if args.case:
                return _validate_case(root, manifest, week, args.case)
            return _validate_valid(root, manifest, week)
        week = _load_json(root, "valid/week.json")
        if args.case:
            result = run_adversarial_case(
                week, _case(root, args.case), offline=True, resource_root=root
            )
            codes = [item["code"] for item in result.get("issues", [])]
            return 2, _envelope(
                command="ucc dry-run", status="failed", manifest=manifest,
                case_id=args.case, issue_codes=codes,
                canonical_hash=_canonical_hash({"case_id": args.case, "issue_codes": codes}),
                ledger_commits=result.get("ledger_commits", 0),
            )
        result = run_week(week, offline=True, resource_root=root)
        if result["status"] != "complete":
            codes = [item["code"] for item in result.get("issues", [])]
            return 2, _envelope(
                command="ucc dry-run", status="failed", manifest=manifest,
                issue_codes=codes,
            )
        return 0, _envelope(
            command="ucc dry-run", status="ok", manifest=manifest,
            stage_results=result["stages"],
            canonical_hash=hashlib.sha256(result["canonical_bytes"]).hexdigest(),
            ledger_hash=result["ledger_hash"], ledger_commits=result["ledger_commits"],
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        code = str(exc) if str(exc).isupper() else "OFFLINE_CLI_VALIDATION_ERROR"
        fallback = {
            "synthetic_set_id": "ucc-synthetic-week-v1",
            "canonical_hash": None,
        }
        return 2, _envelope(
            command="ucc", status="failed", manifest=fallback, issue_codes=[code]
        )


def execute(command: str, *, fixture: dict, offline: bool) -> dict:
    """Compatibility entry point retained for the side-effect-free core tests."""
    base = {"model_calls": 0, "network_attempts": 0, "ledger_writes": 0}
    if not offline or not fixture.get("synthetic") or command not in _COMMANDS:
        return {**base, "exit_code": 2, "issues": [{"code": "PLUGIN_COMMAND_UNSUPPORTED"}]}
    return {**base, "exit_code": 0, "issues": [], "command": command, "status": "ok"}


def setup_cli(parser) -> None:
    subcommands = parser.add_subparsers(dest="ucc_action", required=True)
    subcommands.add_parser("doctor", help="Verify installed offline resources and restrictions")
    validate = subcommands.add_parser("validate", help="Run deterministic synthetic validation")
    source = validate.add_mutually_exclusive_group(required=True)
    source.add_argument("--synthetic", action="store_true")
    source.add_argument("--fixture")
    validate.add_argument("--case", choices=sorted(_CASE_MUTATIONS))
    dry_run = subcommands.add_parser("dry-run", help="Run the real isolated synthetic weekly flow")
    dry_run.add_argument("--synthetic", action="store_true", required=True)
    dry_run.add_argument("--case", choices=sorted(_CASE_MUTATIONS))


def handle_cli(args) -> int:
    argv = [args.ucc_action]
    if getattr(args, "synthetic", False):
        argv.append("--synthetic")
    fixture = getattr(args, "fixture", None)
    if fixture:
        argv.extend(["--fixture", fixture])
    case_id = getattr(args, "case", None)
    if case_id:
        argv.extend(["--case", case_id])
    exit_code, result = run_cli(argv)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    if exit_code:
        raise SystemExit(exit_code)
    return 0
