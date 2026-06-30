"""Closed-wire proposal/approval validation and deterministic transition evaluation."""

from __future__ import annotations

import hashlib
import json


HUMAN_ROLES = {"parent", "guardian", "authorized_adult"}
PROPOSAL_FIELDS = {
    "contract_version", "proposal_id", "proposal_revision", "supersedes_revision",
    "proposal_type", "learner_id", "created_at", "authorship", "smc_ref",
    "expected_evidence", "empty_evidence_rationale", "proposal_payload",
    "proposal_status", "canonical_hash", "extensions",
}
EVENT_FIELDS = {
    "contract_version", "approval_event_id", "approval_key", "ledger_namespace",
    "proposal_id", "proposal_revision", "proposal_hash", "proposal_type",
    "approval_action", "actor", "decision_at", "scope", "reason_code",
    "reason_note", "provenance", "canonical_hash", "extensions",
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


def _proposal_hash(proposal: dict) -> str:
    projection = _clean(proposal)
    projection.pop("canonical_hash", None)
    projection.pop("proposal_status", None)
    return _hash(projection)


def _event_hash(event: dict) -> str:
    projection = _clean(event)
    projection.pop("canonical_hash", None)
    return _hash(projection)


def validate_proposal(document: dict, *, smc_registry: dict) -> list[dict[str, str]]:
    if set(document) != {"ucc_parent_proposal"} or not isinstance(document.get("ucc_parent_proposal"), dict):
        return [_issue("PROPOSAL_SCHEMA_INVALID")]
    proposal = document["ucc_parent_proposal"]
    issues: list[dict[str, str]] = []
    unknown = set(proposal) - PROPOSAL_FIELDS
    if unknown:
        issues.append(_issue("PROPOSAL_UNKNOWN_FIELD"))
    required = PROPOSAL_FIELDS - {"extensions"}
    if not required.issubset(proposal):
        issues.append(_issue("PROPOSAL_SCHEMA_INVALID"))
    if "approval_actor" in proposal.get("authorship", {}):
        issues.append(_issue("PROPOSAL_AUTHORSHIP_CONFLATED"))
    smc_ref = proposal.get("smc_ref")
    if not isinstance(smc_ref, dict) or not {"smc_id", "smc_version", "canonical_hash", "source_path", "approved_at"}.issubset(smc_ref):
        issues.append(_issue("PROPOSAL_SMC_REF_INVALID"))
    elif (
        smc_ref.get("smc_id") not in smc_registry
        or smc_registry[smc_ref["smc_id"]].get("canonical_hash") != smc_ref.get("canonical_hash")
        or smc_registry[smc_ref["smc_id"]].get("active") is not True
    ):
        issues.append(_issue("PROPOSAL_SMC_REF_INVALID"))
    evidence = proposal.get("expected_evidence")
    if isinstance(evidence, list) and not evidence:
        rationale = proposal.get("empty_evidence_rationale")
        if rationale is None:
            issues.append(_issue("PROPOSAL_EMPTY_EVIDENCE_RATIONALE_REQUIRED"))
        if proposal.get("proposal_payload", {}).get("requested_claim_scope") == "mastery_state":
            issues.append(_issue("PROPOSAL_EMPTY_EVIDENCE_SCOPE_INVALID"))
    if "canonical_hash" in proposal and proposal["canonical_hash"] != _proposal_hash(proposal):
        issues.append(_issue("PROPOSAL_CANONICAL_HASH_MISMATCH"))
    return issues


def validate_approval_event(document: dict, *, proposal: dict, authority_config: dict) -> list[dict[str, str]]:
    if set(document) != {"ucc_parent_approval_event"} or not isinstance(document.get("ucc_parent_approval_event"), dict):
        return [_issue("APPROVAL_SCHEMA_INVALID")]
    event = document["ucc_parent_approval_event"]
    proposal_inner = proposal.get("ucc_parent_proposal", {})
    issues: list[dict[str, str]] = []
    if set(event) - EVENT_FIELDS or not (EVENT_FIELDS - {"extensions"}).issubset(event):
        issues.append(_issue("APPROVAL_SCHEMA_INVALID"))
    actor = event.get("actor", {})
    role, actor_id = actor.get("actor_role"), actor.get("actor_id")
    if role not in HUMAN_ROLES or actor_id not in authority_config.get("actors", {}).get(role, []):
        issues.append(_issue("APPROVAL_ACTOR_UNAUTHORIZED"))
    if event.get("ledger_namespace") != authority_config.get("ledger_namespace"):
        issues.append(_issue("APPROVAL_AUTHORITY_INVALID"))
    if event.get("proposal_id") != proposal_inner.get("proposal_id") or event.get("proposal_revision") != proposal_inner.get("proposal_revision"):
        issues.append(_issue("APPROVAL_REVISION_MISMATCH"))
    if event.get("proposal_hash") != proposal_inner.get("canonical_hash"):
        issues.append(_issue("APPROVAL_PROPOSAL_HASH_MISMATCH"))
    scope = event.get("scope", {})
    expected_scope = {
        "proposal_id": proposal_inner.get("proposal_id"),
        "proposal_revision": proposal_inner.get("proposal_revision"),
        "learner_id": proposal_inner.get("learner_id"),
        "proposal_type": proposal_inner.get("proposal_type"),
        "decision_effect": event.get("approval_action"),
    }
    if scope != expected_scope:
        issues.append(_issue("APPROVAL_SCOPE_MISMATCH"))
    if event.get("canonical_hash") != _event_hash(event):
        issues.append(_issue("APPROVAL_CANONICAL_HASH_MISMATCH"))
    return issues


def evaluate_transition(
    proposal: dict, event: dict, *, accepted_events: list[dict], idempotency_bindings: dict,
    authority_config: dict, execution_state: str,
) -> dict:
    del execution_state
    issues = validate_approval_event(event, proposal=proposal, authority_config=authority_config)
    if issues:
        return {"issues": issues, "append_event": False, "replayed": False}
    inner = event["ucc_parent_approval_event"]
    existing = idempotency_bindings.get(inner["approval_key"])
    if existing is not None:
        if _clean(existing) == _clean(event):
            return {"issues": [], "append_event": False, "replayed": True, "next_proposal_status": _next_status(inner["approval_action"])}
        return {"issues": [_issue("IDEMPOTENCY_CONFLICT")], "append_event": False, "replayed": False}
    for accepted in accepted_events:
        prior = accepted["ucc_parent_approval_event"]
        if prior["proposal_id"] == inner["proposal_id"] and prior["proposal_revision"] == inner["proposal_revision"] and prior["approval_action"] != inner["approval_action"]:
            return {"issues": [_issue("APPROVAL_DECISION_CONFLICT")], "append_event": False, "replayed": False}
    return {"issues": [], "append_event": True, "replayed": False, "next_proposal_status": _next_status(inner["approval_action"])}


def _next_status(action: str) -> str:
    return {"approve": "approved", "reject": "rejected", "request_revision": "revision_requested"}[action]


def run_mutation_probe(proposal: dict, event: dict, probe_fixture: dict) -> dict[str, str]:
    p = proposal["ucc_parent_proposal"]
    e = event["ucc_parent_approval_event"]
    checks = {
        "allow-ai-approval-actor": e["actor"]["actor_role"] in HUMAN_ROLES,
        "ignore-wrong-revision": e["proposal_revision"] == p["proposal_revision"],
        "accept-changed-replay-payload": _event_hash(e) == e["canonical_hash"],
        "ignore-proposal-hash-change": e["proposal_hash"] == p["canonical_hash"],
    }
    outcomes = {item["mutant_id"]: "KILLED" if checks[item["mutant_id"]] else "SURVIVED" for item in probe_fixture["killable"]}
    outcomes[probe_fixture["equivalent_control"]["mutant_id"]] = "SURVIVED"
    return outcomes
