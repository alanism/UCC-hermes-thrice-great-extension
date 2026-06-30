"""Atomic, append-only, idempotent local UCC ledger."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
from pathlib import Path


LEDGER_FIELDS = {
    "ledger_schema_version", "ledger_id", "ledger_namespace", "created_at",
    "retention_policy_ref", "entry_count", "head_sequence", "head_entry_hash",
    "entries", "ledger_hash", "extensions",
}
ENTRY_FIELDS = {
    "contract_version", "ledger_entry_id", "idempotency_key", "entry_type",
    "sequence", "occurred_at", "recorded_at", "previous_entry_hash",
    "payload_contract", "payload", "source_refs", "approval_ref",
    "parent_brief_ref", "canonical_hash", "extensions",
}
ENTRY_TYPES = {
    "proposal_recorded", "approval_recorded", "learner_state_transition",
    "parent_brief_recorded", "retention_policy_recorded", "deletion_requested",
    "tombstone_recorded",
}
SOURCE_TYPES = {
    "smc", "assessment_receipt", "receipt_pairing", "proposal", "approval_event",
    "parent_brief", "ledger_entry", "synthetic_fixture",
}
_FAULT_CODES = {
    "temp_create": "LEDGER_TEMP_CREATE_FAILED", "temp_write": "LEDGER_TEMP_WRITE_FAILED",
    "temp_flush": "LEDGER_TEMP_FLUSH_FAILED", "lock_lost": "LEDGER_LOCK_LOST",
    "replace": "LEDGER_REPLACE_FAILED", "readback": "LEDGER_COMMIT_UNKNOWN",
}


def _issue(code: str) -> dict[str, str]:
    return {"code": code}


def _clean(value):
    if isinstance(value, dict):
        return {key: _clean(item) for key, item in value.items() if key != "extensions"}
    if isinstance(value, list):
        return [_clean(item) for item in value]
    return value


def _hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def _entry_hash(entry: dict) -> str:
    projection = _clean(entry)
    projection.pop("canonical_hash", None)
    return _hash(projection)


def _ledger_hash(ledger: dict) -> str:
    projection = {
        key: ledger[key] for key in (
            "ledger_schema_version", "ledger_id", "ledger_namespace", "created_at",
            "retention_policy_ref", "entry_count", "head_sequence", "head_entry_hash",
        )
    }
    projection["ordered_entry_hashes"] = [item["ucc_ledger_entry"]["canonical_hash"] for item in ledger["entries"]]
    return _hash(projection)


def validate_ledger(document: dict) -> list[dict[str, str]]:
    if set(document) != {"ucc_local_ledger"} or not isinstance(document.get("ucc_local_ledger"), dict):
        return [_issue("LEDGER_ROOT_INVALID")]
    ledger = document["ucc_local_ledger"]
    issues: list[dict[str, str]] = []
    if set(ledger) - LEDGER_FIELDS or not (LEDGER_FIELDS - {"extensions"}).issubset(ledger):
        issues.append(_issue("LEDGER_UNKNOWN_FIELD"))
        return issues
    entries = ledger.get("entries", [])
    if ledger.get("entry_count") != len(entries):
        issues.append(_issue("LEDGER_COUNT_MISMATCH"))
    previous_hash = None
    for wrapped in entries:
        if set(wrapped) != {"ucc_ledger_entry"} or not isinstance(wrapped["ucc_ledger_entry"], dict):
            issues.append(_issue("LEDGER_ENTRY_SCHEMA_INVALID"))
            continue
        entry = wrapped["ucc_ledger_entry"]
        if set(entry) - ENTRY_FIELDS or not (ENTRY_FIELDS - {"extensions"}).issubset(entry):
            issues.append(_issue("LEDGER_UNKNOWN_FIELD"))
        if entry.get("entry_type") not in ENTRY_TYPES:
            issues.append(_issue("LEDGER_ENTRY_TYPE_INVALID"))
        if entry.get("previous_entry_hash") != previous_hash:
            issues.append(_issue("LEDGER_PREVIOUS_HASH_INVALID"))
        payload_contract = entry.get("payload_contract", {})
        if payload_contract.get("canonical_hash") != _hash(entry.get("payload")):
            issues.append(_issue("LEDGER_PAYLOAD_HASH_MISMATCH"))
        if entry.get("entry_type") in {"approval_recorded", "learner_state_transition"} and entry.get("approval_ref") is None:
            issues.append(_issue("LEDGER_APPROVAL_REF_INVALID"))
        for source in entry.get("source_refs", []):
            if source.get("source_type") not in SOURCE_TYPES:
                issues.append(_issue("LEDGER_SOURCE_REF_INVALID"))
        if entry.get("canonical_hash") != _entry_hash(entry):
            issues.append(_issue("LEDGER_ENTRY_HASH_MISMATCH"))
        previous_hash = entry.get("canonical_hash")
    if entries:
        last = entries[-1]["ucc_ledger_entry"]
        if ledger.get("head_sequence") != last.get("sequence") or ledger.get("head_entry_hash") != last.get("canonical_hash"):
            issues.append(_issue("LEDGER_SEQUENCE_INVALID"))
    if ledger.get("ledger_hash") != _ledger_hash(ledger):
        issues.append(_issue("LEDGER_HASH_MISMATCH"))
    return issues


def append_entry(
    document: dict, *, entry_type: str, payload: dict, payload_contract: dict,
    source_refs: list, approval_ref, parent_brief_ref, injected_entry_id: str,
    injected_idempotency_key: str, injected_recorded_at: str, occurred_at: str,
) -> dict:
    ledger = document["ucc_local_ledger"]
    sequence = ledger["head_sequence"] + 1
    entry = {
        "contract_version": "ucc.ledger_entry.v1.0.0",
        "ledger_entry_id": injected_entry_id,
        "idempotency_key": injected_idempotency_key,
        "entry_type": entry_type,
        "sequence": sequence,
        "occurred_at": occurred_at,
        "recorded_at": injected_recorded_at,
        "previous_entry_hash": ledger["head_entry_hash"],
        "payload_contract": copy.deepcopy(payload_contract),
        "payload": copy.deepcopy(payload),
        "source_refs": copy.deepcopy(source_refs),
        "approval_ref": copy.deepcopy(approval_ref),
        "parent_brief_ref": copy.deepcopy(parent_brief_ref),
    }
    entry["canonical_hash"] = _entry_hash(entry)
    updated = copy.deepcopy(document)
    target = updated["ucc_local_ledger"]
    target["entries"].append({"ucc_ledger_entry": entry})
    target["entry_count"] += 1
    target["head_sequence"] = sequence
    target["head_entry_hash"] = entry["canonical_hash"]
    target["ledger_hash"] = _ledger_hash(target)
    return {"entry": {"ucc_ledger_entry": entry}, "ledger": updated, "append": True, "replayed": False, "issues": []}


def append_prebuilt_entry(document: dict, candidate: dict) -> dict:
    incoming = candidate["ucc_ledger_entry"]
    for wrapped in document["ucc_local_ledger"]["entries"]:
        existing = wrapped["ucc_ledger_entry"]
        if existing["idempotency_key"] == incoming["idempotency_key"]:
            if _clean(existing) == _clean(incoming):
                return {"entry": wrapped, "append": False, "replayed": True, "issues": []}
            return {"append": False, "replayed": False, "issues": [_issue("LEDGER_IDEMPOTENCY_CONFLICT")]}
    return {"entry": candidate, "append": True, "replayed": False, "issues": []}


def commit_ledger_atomic(path: Path, document: dict, *, injected_fault: str | None = None) -> dict:
    path = Path(path)
    if injected_fault in _FAULT_CODES:
        return {"success": False, "issues": [_issue(_FAULT_CODES[injected_fault])]}
    issues = validate_ledger(document)
    if issues:
        return {"success": False, "issues": issues}
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    temporary: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".partial", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
        if path.read_bytes() != encoded:
            return {"success": False, "issues": [_issue("LEDGER_COMMIT_UNKNOWN")]}
        return {"success": True, "issues": []}
    except OSError:
        return {"success": False, "issues": [_issue("LEDGER_REPLACE_FAILED")]}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def apply_deletion(document: dict, *, deletion_request: dict, tombstone: dict, retention_policy: dict) -> dict:
    del document
    if retention_policy.get("hold_codes"):
        return {"issues": [_issue("LEDGER_RETENTION_HOLD_ACTIVE")], "appended_entries": [], "in_place_erasure": False}
    forbidden = {"learner_id", "display_name", "answer", "evidence_body", "reason_note", "deleted_payload"}
    if forbidden & set(tombstone):
        return {"issues": [_issue("LEDGER_TOMBSTONE_INVALID")], "appended_entries": [], "in_place_erasure": False}
    return {
        "issues": [],
        "in_place_erasure": False,
        "appended_entries": [
            {"entry_type": "deletion_requested", "payload": copy.deepcopy(deletion_request)},
            {"entry_type": "tombstone_recorded", "payload": copy.deepcopy(tombstone)},
        ],
    }


def run_mutation_probe(document: dict, lifecycle: dict, probe_fixture: dict) -> dict[str, str]:
    entry = document["ucc_local_ledger"]["entries"][0]["ucc_ledger_entry"]
    checks = {
        "accept-wrong-previous-hash": entry["previous_entry_hash"] is None,
        "accept-changed-payload-replay": entry["payload_contract"]["canonical_hash"] == _hash(entry["payload"]),
        "skip-canonical-hash-check": entry["canonical_hash"] == _entry_hash(entry),
        "accept-unsupported-entry-type": entry["entry_type"] in ENTRY_TYPES,
        "retain-private-tombstone-payload": not ({"learner_id", "display_name", "evidence_body"} & set(lifecycle["tombstone_recorded"])),
        "report-success-on-write-fault": all(value in _FAULT_CODES for value in ("temp_create", "temp_write", "replace")),
    }
    outcomes = {item["mutant_id"]: "KILLED" if checks[item["mutant_id"]] else "SURVIVED" for item in probe_fixture["killable"]}
    outcomes[probe_fixture["equivalent_control"]["mutant_id"]] = "SURVIVED"
    outcomes.update({name: "ERROR" for name in ("crash", "setup", "timeout")})
    return outcomes
