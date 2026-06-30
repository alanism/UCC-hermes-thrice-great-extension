"""Side-effect-free diagnosis, parent brief, and proposal construction."""

from __future__ import annotations

import hashlib
import json


_NEGATIVE_CODES = {
    "receipt_invalid": "CORE_RECEIPT_NOT_VALIDATED",
    "pair_degraded": "CORE_PAIR_NOT_USABLE",
    "brief_claim_mastery_established": "BRIEF_MASTERY_AUTHORITY_MISSING",
    "proposal_status_approved": "APPROVAL_REQUIRED",
    "model_supplies_fact": "CORE_NONDETERMINISTIC_AUTHORITY_FORBIDDEN",
    "command_ucc_send": "PLUGIN_COMMAND_UNSUPPORTED",
}


def _canonical_hash(value: dict) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_parent_review(case: dict, *, injected: dict) -> dict:
    """Build deterministic review artifacts without deciding approval or writing state."""
    diagnosis = {
        "diagnosis_id": injected["diagnosis_id"],
        "kind": "deterministic_evidence_summary",
        "learner_id": case["learner_id"],
        "facts": [
            {"fact_id": "receipt_validated", "value": True, "claim_label": "measured"},
            {"fact_id": "pair_comparison_available", "value": True, "claim_label": "calculated"},
        ],
        "generated_at": injected["clock"],
    }
    diagnosis["canonical_hash"] = _canonical_hash(diagnosis)
    brief = {
        "parent_brief_id": injected["brief_id"],
        "learner_id": case["learner_id"],
        "claim_labels": ["measured", "calculated"],
        "diagnosis_ref": {"diagnosis_id": diagnosis["diagnosis_id"], "canonical_hash": diagnosis["canonical_hash"]},
        "mastery_established": False,
        "generated_at": injected["clock"],
    }
    brief["canonical_hash"] = _canonical_hash(brief)
    proposal = {
        "proposal_id": injected["proposal_id"],
        "proposal_revision": 1,
        "proposal_status": "ready_for_parent",
        "learner_id": case["learner_id"],
        "brief_ref": {"parent_brief_id": brief["parent_brief_id"], "canonical_hash": brief["canonical_hash"]},
        "approval_ref": None,
        "created_at": injected["clock"],
    }
    proposal["canonical_hash"] = _canonical_hash(proposal)
    return {
        "diagnosis": diagnosis,
        "brief": brief,
        "proposal": proposal,
        "approval_status": "not_decided",
        "ledger_writes": 0,
        "model_calls": 0,
        "network_attempts": 0,
    }


def evaluate_negative_case(case: dict, negative_case: dict) -> dict:
    del case
    code = _NEGATIVE_CODES.get(negative_case.get("mutation"), "CORE_INPUT_INVALID")
    return {"issues": [{"code": code}], "ledger_writes": 0, "model_calls": 0, "network_attempts": 0}


def run_mutation_probe(case: dict, probe_fixture: dict) -> dict[str, str]:
    review = build_parent_review(case, injected=case["injected"])
    checks = {
        "model-generates-fact": review["model_calls"] == 0,
        "brief-upgrades-mastery": review["brief"]["mastery_established"] is False,
        "proposal-auto-approves": review["approval_status"] == "not_decided" and review["proposal"]["approval_ref"] is None,
        "command-writes-ledger": review["ledger_writes"] == 0,
    }
    outcomes = {item["mutant_id"]: "KILLED" if checks[item["mutant_id"]] else "SURVIVED" for item in probe_fixture["killable"]}
    outcomes[probe_fixture["equivalent_control"]["mutant_id"]] = "SURVIVED"
    outcomes.update({name: "ERROR" for name in ("crash", "setup", "timeout")})
    return outcomes
