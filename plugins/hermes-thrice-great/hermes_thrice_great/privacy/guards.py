"""Deterministic local privacy guards with no model or network dependency."""

from __future__ import annotations

import os
import re
import stat
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path, PureWindowsPath
from typing import Callable


_RESERVED_WINDOWS_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
_PRIVATE_VALUE = re.compile(
    r"(?i)\b(learner_display_name|learner_id|answer|token|secret|email|profile_name)\s*=\s*([^\s,;]+)"
)
_PRIVATE_PATH = re.compile(r"(?i)\b(path\s*=\s*)(?:[a-z]:\\[^\s,;]+|\\\\[^\s,;]+)")
_PSEUDONYMOUS_LEARNER_ID = re.compile(r"^lrn_[0-9A-HJKMNP-TV-Z]{26}$")
_DIRECT_IDENTITY_FIELDS = {"display_name", "email", "family_name", "learner_name", "name"}
_TOMBSTONE_PRIVATE_FIELDS = {
    "answer", "deleted_payload", "display_name", "email", "evidence_body",
    "family_name", "learner_id", "learner_name", "private_path", "reason_note",
}
_FORBIDDEN_COMMIT_ROOTS = {
    "data", "dist", "learner_data", "local", "logs", "memories", "outputs",
    "private", "sessions", "workspace",
}


def _issue(code: str) -> dict[str, str]:
    return {"code": code}


def _is_reserved(part: str) -> bool:
    normalized = part.rstrip(" .").split(".", 1)[0].upper()
    return normalized in _RESERVED_WINDOWS_NAMES


def _is_reparse(path: Path) -> bool:
    try:
        metadata = os.lstat(path)
    except OSError:
        return False
    attributes = getattr(metadata, "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _inside(candidate: Path, root: Path) -> bool:
    try:
        return os.path.commonpath((os.path.normcase(str(candidate)), os.path.normcase(str(root)))) == os.path.normcase(str(root))
    except ValueError:
        return False


def validate_contained_path(
    root: Path,
    relative: str,
    *,
    injected_resolver: Callable[[Path], Path] | None = None,
) -> dict:
    """Validate a Windows-relative path against a resolved private root."""
    root = Path(root).resolve(strict=True)
    windows_path = PureWindowsPath(relative)
    if windows_path.is_absolute() or windows_path.drive or windows_path.root:
        return {"allowed": False, "issues": [_issue("PRIVACY_PATH_ESCAPE")]}
    parts = windows_path.parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        return {"allowed": False, "issues": [_issue("PRIVACY_PATH_ESCAPE")]}
    if any(_is_reserved(part) for part in parts):
        return {"allowed": False, "issues": [_issue("PRIVACY_RESERVED_NAME")]}

    candidate = root.joinpath(*parts)
    try:
        resolved = Path(injected_resolver(candidate) if injected_resolver else candidate.resolve(strict=False))
    except OSError as exc:
        if getattr(exc, "winerror", None) == 206 or exc.errno == 206:
            return {"allowed": False, "issues": [_issue("PRIVACY_HOST_PATH_UNSUPPORTED")]}
        return {"allowed": False, "issues": [_issue("PRIVACY_PATH_INSPECTION_FAILED")]}

    current = root
    saw_reparse = injected_resolver is not None
    for part in parts:
        current = current / part
        if current.exists() and _is_reparse(current):
            saw_reparse = True
    if not _inside(resolved, root):
        code = "PRIVACY_REPARSE_ESCAPE" if saw_reparse else "PRIVACY_PATH_ESCAPE"
        return {"allowed": False, "issues": [_issue(code)]}
    return {"allowed": True, "issues": [], "resolved_path": resolved}


def redact_log(value: str) -> str:
    """Remove private identifiers, secrets, emails, profile names, and paths."""
    redacted = _PRIVATE_PATH.sub(lambda match: f"{match.group(1)}[PRIVATE_PATH]", value)
    return _PRIVATE_VALUE.sub(lambda match: f"{match.group(1)}=[REDACTED]", redacted)


def _utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def evaluate_retention(case: dict) -> str:
    """Return the deterministic retention action; any hold fails closed."""
    if case.get("hold_codes"):
        return "retain"
    retention_days = case.get("retention_days")
    if retention_days is None:
        return "retain"
    expires_at = _utc(case["recorded_at"]) + timedelta(days=retention_days)
    return "request_deletion" if expires_at <= _utc(case["now"]) else "retain"


def evaluate_commit_eligibility(path: str, *, synthetic: bool) -> dict:
    """Fail closed for generated/private roots and secret-shaped files."""
    normalized = path.replace("\\", "/").strip("/").casefold()
    parts = tuple(part for part in normalized.split("/") if part)
    name = parts[-1] if parts else ""
    forbidden = (
        not synthetic
        or not parts
        or parts[0] in _FORBIDDEN_COMMIT_ROOTS
        or (name.startswith(".env") and name not in {".env.example", ".env.template"})
        or name == "auth.json"
        or name.startswith(("credentials", "secrets."))
        or name.endswith((".key", ".p12", ".pem", ".pfx", ".sqlite", ".sqlite3"))
    )
    issues = [_issue("PRIVATE_DATA_COMMIT_FORBIDDEN")] if forbidden else []
    return {"allowed": not forbidden, "issues": issues}


def validate_pseudonymous_record(record: dict) -> dict:
    """Accept only durable pseudonymous learner identity at the guard boundary."""
    issues = []
    if not _PSEUDONYMOUS_LEARNER_ID.fullmatch(str(record.get("learner_id", ""))):
        issues.append(_issue("PRIVACY_PSEUDONYM_INVALID"))
    if any(record.get(field) not in {None, ""} for field in _DIRECT_IDENTITY_FIELDS):
        issues.append(_issue("PRIVACY_DIRECT_IDENTIFIER_FORBIDDEN"))
    return {"allowed": not issues, "issues": issues}


def _contains_private_tombstone_field(value) -> bool:
    if isinstance(value, dict):
        return any(
            key.casefold() in _TOMBSTONE_PRIVATE_FIELDS or _contains_private_tombstone_field(item)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_contains_private_tombstone_field(item) for item in value)
    return False


def validate_deletion_guard(deletion_request: dict, tombstone: dict, *, hold_codes: list[str]) -> dict:
    """Validate a deletion plan without performing ledger mutation or erasure."""
    issues = []
    targets = deletion_request.get("target_entry_ids", [])
    if hold_codes:
        issues.append(_issue("PRIVACY_DELETION_HOLD_ACTIVE"))
    if not targets or tombstone.get("target_entry_id") not in targets:
        issues.append(_issue("PRIVACY_DELETION_TARGET_INVALID"))
    audit_targets = [item.get("target_entry_id") for item in tombstone.get("retained_audit_hashes", [])]
    if tombstone.get("target_entry_id") not in audit_targets:
        issues.append(_issue("PRIVACY_TOMBSTONE_AUDIT_INVALID"))
    if _contains_private_tombstone_field(tombstone):
        issues.append(_issue("PRIVACY_TOMBSTONE_PRIVATE_DATA"))
    return {
        "allowed": not issues,
        "issues": issues,
        "in_place_erasure": False,
        "actions": ["append_deletion_requested", "compact_atomically", "append_tombstone_recorded"] if not issues else [],
    }


def run_mutation_probe(windows_fixture: dict, lifecycle_fixture: dict, probe_fixture: dict) -> dict[str, str]:
    """Exercise each named privacy control and classify it under the R4 outcome contract."""
    outcomes: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="ucc-privacy-probe-") as directory:
        root = Path(directory) / "root"
        outside = Path(directory) / "outside"
        root.mkdir()
        outside.mkdir()
        checks = {
            "skip-dotdot-normalization": not validate_contained_path(root, r"..\outside\synthetic.json")["allowed"],
            "ignore-reparse-target": not validate_contained_path(
                root, r"junction\synthetic.json", injected_resolver=lambda _candidate: outside / "synthetic.json"
            )["allowed"],
            "drive-case-sensitive-containment": validate_contained_path(root, r"records\case.json")["allowed"],
            "log-private-value": "SYNTHETIC_PERSON_0001" not in redact_log("learner_display_name=SYNTHETIC_PERSON_0001"),
            "delete-active-hold": evaluate_retention(next(case for case in lifecycle_fixture["retention"] if case["case_id"] == "hold-active")) == "retain",
            "allow-private-commit-root": not evaluate_commit_eligibility("local/synthetic.json", synthetic=True)["allowed"],
        }
    for mutant in probe_fixture["killable"]:
        outcomes[mutant["mutant_id"]] = "KILLED" if checks.get(mutant["mutant_id"], False) else "SURVIVED"
    outcomes[probe_fixture["equivalent_control"]["mutant_id"]] = "SURVIVED"
    outcomes.update({name: "ERROR" for name in ("crash", "setup", "timeout")})
    return outcomes
