"""Deterministic contract-registry validation and exact-version resolution."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath


FAMILIES = {"smc", "assessment_receipt", "receipt_pairing", "proposal_approval", "parent_brief_ledger"}
LIFECYCLES = {"draft", "locked", "active", "deprecated", "retired"}
ENVELOPE_FIELDS = {
    "registry_schema_version", "registry_id", "generated_at", "approved_at",
    "canonicalization_id", "families", "extensions",
}
VERSION_FIELDS = {
    "version", "lifecycle_state", "schema_ref", "contract_ref", "canonical_hash",
    "semantic_validator_ref", "semantic_projection_ref", "introduced_at", "replaces",
    "compatible_with", "migration", "fixture_sets", "approval_ref",
}
_NAMESPACE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)+$")


def _issue(code: str, path: str = "") -> dict[str, str]:
    return {"code": code, "path": path}


def _jcs(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def compute_registry_snapshot_hash(document: dict) -> str:
    return hashlib.sha256(_jcs(document)).hexdigest()


def compute_version_canonical_hash(version: dict, canonicalization_id: str) -> str:
    schema = version.get("schema_ref") or {}
    contract = version.get("contract_ref") or {}
    excerpt = contract.get("canonical_excerpt")
    projection = {
        "version": version.get("version"),
        "schema_id": schema.get("schema_id"),
        "schema_artifact_sha256": schema.get("artifact_sha256"),
        "contract_artifact_sha256": contract.get("artifact_sha256"),
        "canonical_excerpt_sha256": hashlib.sha256(excerpt.encode("utf-8")).hexdigest() if excerpt is not None else None,
        "semantic_validator_sha256": (version.get("semantic_validator_ref") or {}).get("artifact_sha256"),
        "semantic_projection_sha256": (version.get("semantic_projection_ref") or {}).get("artifact_sha256"),
        "canonicalization_id": canonicalization_id,
    }
    return hashlib.sha256(_jcs(projection)).hexdigest()


def _safe_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


def _artifact(root: Path, relative: str) -> bytes | None:
    if not _safe_path(relative):
        return None
    target = (root / relative).resolve(strict=False)
    try:
        target.relative_to(root.resolve(strict=True))
        return target.read_bytes()
    except (OSError, ValueError):
        return None


def _validate_fixture_set(item: object) -> bool:
    required = {"fixture_set_id", "path", "purpose", "expected_hash", "coverage_labels"}
    return (
        isinstance(item, dict) and set(item) == required and _safe_path(item.get("path"))
        and isinstance(item.get("expected_hash"), str) and len(item["expected_hash"]) == 64
        and isinstance(item.get("coverage_labels"), list)
    )


def _validate_approval(value: object) -> bool:
    required = {"actor_role", "approval_event_id", "decision_id", "timestamp", "source_document", "scope"}
    return isinstance(value, dict) and set(value) == required and bool(value.get("actor_role")) and isinstance(value.get("scope"), dict)


def _fixture_hash(root: Path, relative: str) -> str | None:
    directory = root / relative
    if not directory.is_dir():
        return None
    entries = []
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        entries.append({"path": path.relative_to(directory).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return hashlib.sha256(_jcs(entries)).hexdigest() if entries else None


def validate_registry(document: dict, artifact_root: Path, snapshot_hash: str) -> list[dict[str, str]]:
    if set(document) != {"ucc_contract_registry"} or not isinstance(document.get("ucc_contract_registry"), dict):
        return [_issue("REGISTRY_ROOT_INVALID")]
    envelope = document["ucc_contract_registry"]
    if set(envelope) - ENVELOPE_FIELDS:
        return [_issue("REGISTRY_UNKNOWN_FIELD")]
    extensions = envelope.get("extensions")
    if extensions is not None and (
        not isinstance(extensions, dict) or any(not _NAMESPACE.fullmatch(key) for key in extensions)
    ):
        return [_issue("REGISTRY_EXTENSION_INVALID")]
    required_envelope = ENVELOPE_FIELDS - {"extensions"}
    if not required_envelope.issubset(envelope) or envelope.get("registry_schema_version") != "ucc.contract_registry.v1.0.0":
        return [_issue("REGISTRY_SCHEMA_INVALID")]
    families = envelope.get("families")
    if not isinstance(families, dict) or set(families) != FAMILIES:
        return [_issue("REGISTRY_SCHEMA_INVALID")]
    for family_key, family in families.items():
        if not isinstance(family, dict) or "family_id" not in family:
            return [_issue("REGISTRY_FAMILY_ID_MISSING", family_key)]
        if family.get("family_id") != family_key or set(family) != {"family_id", "versions"} or not isinstance(family.get("versions"), list):
            return [_issue("REGISTRY_SCHEMA_INVALID", family_key)]
        for index, version in enumerate(family["versions"]):
            at = f"{family_key}/versions/{index}"
            if not isinstance(version, dict):
                return [_issue("REGISTRY_SCHEMA_INVALID", at)]
            lifecycle = version.get("lifecycle_state")
            if lifecycle not in LIFECYCLES:
                return [_issue("REGISTRY_LIFECYCLE_UNKNOWN", at)]
            missing = VERSION_FIELDS - set(version)
            if missing or set(version) - VERSION_FIELDS:
                return [_issue("REGISTRY_SCHEMA_INVALID", at)]
            if lifecycle != "draft" and any(version.get(name) is None for name in ("schema_ref", "canonical_hash", "approval_ref")):
                return [_issue("REGISTRY_SCHEMA_INVALID", at)]
            compatibility = version.get("compatible_with")
            if not isinstance(compatibility, dict) or set(compatibility) != {"readers", "writers", "unknown_version_behavior"}:
                return [_issue("REGISTRY_COMPATIBILITY_INVALID", at)]
            fixtures = version.get("fixture_sets")
            if not isinstance(fixtures, list) or any(not _validate_fixture_set(item) for item in fixtures):
                return [_issue("REGISTRY_FIXTURE_SET_INVALID", at)]
            if version.get("approval_ref") is not None and not _validate_approval(version["approval_ref"]):
                return [_issue("REGISTRY_APPROVAL_REF_INVALID", at)]
            for ref_name in ("schema_ref", "contract_ref", "semantic_validator_ref", "semantic_projection_ref"):
                ref = version.get(ref_name)
                if ref is not None and (not isinstance(ref, dict) or not _safe_path(ref.get("path"))):
                    return [_issue("REGISTRY_PATH_INVALID", f"{at}/{ref_name}")]
            if lifecycle != "draft":
                schema_ref = version["schema_ref"]
                schema_bytes = _artifact(Path(artifact_root), schema_ref["path"])
                if schema_bytes is None or hashlib.sha256(schema_bytes).hexdigest() != schema_ref.get("artifact_sha256"):
                    return [_issue("REGISTRY_ARTIFACT_HASH_MISMATCH", f"{at}/schema_ref")]
                if compute_version_canonical_hash(version, envelope["canonicalization_id"]) != version["canonical_hash"]:
                    return [_issue("REGISTRY_CANONICAL_HASH_MISMATCH", at)]
            contract_ref = version["contract_ref"]
            contract_bytes = _artifact(Path(artifact_root), contract_ref["path"])
            if contract_bytes is None:
                return [_issue("REGISTRY_PATH_INVALID", f"{at}/contract_ref")]
            normalized = contract_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
            if hashlib.sha256(normalized).hexdigest() != contract_ref.get("artifact_sha256"):
                return [_issue("REGISTRY_ARTIFACT_HASH_MISMATCH", f"{at}/contract_ref")]
            for fixture in fixtures:
                if _fixture_hash(Path(artifact_root), fixture["path"]) != fixture["expected_hash"]:
                    return [_issue("REGISTRY_FIXTURE_HASH_MISMATCH", at)]
    if compute_registry_snapshot_hash(document) != snapshot_hash:
        return [_issue("REGISTRY_SNAPSHOT_HASH_MISMATCH")]
    return []


def resolve_version(
    document: dict, snapshot_hash: str, family_id: str, version: str, *, purpose: str,
    allow_locked: bool, artifact_root: Path,
) -> dict:
    issues = validate_registry(document, artifact_root, snapshot_hash)
    if issues:
        return {"record": None, "issues": issues}
    family = document["ucc_contract_registry"]["families"].get(family_id)
    record = next((item for item in family["versions"] if item["version"] == version), None) if family else None
    if record is None:
        return {"record": None, "issues": [_issue("REGISTRY_VERSION_UNSUPPORTED")]}
    usable = record["lifecycle_state"] == "active" or (
        record["lifecycle_state"] == "locked" and allow_locked and purpose in {"test", "contract_lock"}
    )
    if not usable:
        return {"record": None, "issues": [_issue("REGISTRY_LIFECYCLE_UNUSABLE")]}
    return {"record": record, "issues": []}


def plan_migration(document: dict, source_version: str, target_version: str) -> dict:
    for family in document.get("ucc_contract_registry", {}).get("families", {}).values():
        target = next((item for item in family.get("versions", []) if item.get("version") == target_version), None)
        if target:
            adapters = target.get("migration", {}).get("adapters", [])
            adapter = next((item for item in adapters if item.get("source_version") == source_version), None)
            if adapter:
                return {"record": adapter, "issues": []}
    return {"record": None, "issues": [_issue("MIGRATION_ADAPTER_UNAVAILABLE")]}
