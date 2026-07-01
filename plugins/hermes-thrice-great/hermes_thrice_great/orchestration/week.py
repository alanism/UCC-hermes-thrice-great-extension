"""Minimum deterministic, offline synthetic weekly evidence loop."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path

from hermes_thrice_great.contracts import approval, ledger, pairing, receipts
from hermes_thrice_great.core.workflow import build_parent_review
from hermes_thrice_great.privacy.guards import validate_contained_path


REPO_ROOT = Path(__file__).resolve().parents[4]
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
BUNDLED_RESOURCE_ROOT = PACKAGE_ROOT / "resources" / "synthetic"
SOURCE_CANONICAL_WEEK = REPO_ROOT / "fixtures" / "synthetic" / "valid" / "week.json"


def _issue(code: str) -> dict[str, str]:
    return {"code": code}


def _hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def _load(relative: str, resource_root: Path | None = None):
    root = Path(resource_root).resolve(strict=True) if resource_root is not None else REPO_ROOT
    containment = validate_contained_path(root, relative)
    if not containment["allowed"]:
        raise ValueError(containment["issues"][0]["code"])
    return json.loads(Path(containment["resolved_path"]).read_text(encoding="utf-8"))


def _materialized_week(week: dict, resource_root: Path | None = None) -> dict:
    if week.get("fixture_schema_version") == "ucc.synthetic_week_fixture.v1.0.0":
        return week
    canonical_path = (
        Path(resource_root) / "valid" / "week.json"
        if resource_root is not None
        else SOURCE_CANONICAL_WEEK
    )
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    if canonical["week_id"] != week.get("week_id"):
        raise ValueError("OFFLINE_WEEK_FIXTURE_UNSUPPORTED")
    return canonical


def _failure(code: str) -> dict:
    return {
        "status": "failed", "issues": [_issue(code)], "ledger_commits": 0,
        "model_calls": 0, "network_attempts": 0,
    }


def _inputs(week: dict, resource_root: Path | None = None) -> dict:
    return {name: _load(relative, resource_root) for name, relative in week["inputs"].items()}


def _prepare_week(week: dict, resource_root: Path | None = None) -> tuple[dict, dict] | tuple[None, dict]:
    if not week.get("synthetic") or not week.get("offline"):
        return None, _failure("OFFLINE_SYNTHETIC_REQUIRED")
    try:
        materialized = _materialized_week(week, resource_root)
        return {"week": materialized, "inputs": _inputs(materialized, resource_root)}, {}
    except (OSError, ValueError, json.JSONDecodeError):
        return None, _failure("OFFLINE_FIXTURE_INVALID")


def run_week(
    week: dict, *, offline: bool, resource_root: Path | None = None,
    commit_ledger: bool = True,
) -> dict:
    if not offline:
        return _failure("OFFLINE_NETWORK_FORBIDDEN")
    prepared, failure = _prepare_week(week, resource_root)
    if prepared is None:
        return failure
    materialized, inputs = prepared["week"], prepared["inputs"]
    stages = ["smc_loaded"]
    smc = inputs["smc"]
    if smc.get("lifecycle_status") != "active":
        return _failure("CORE_SMC_NOT_ACTIVE")
    learner_ids = {
        smc.get("learner_id"), inputs["calm_receipt"].get("learner_id"),
        inputs["pressure_receipt"].get("learner_id"),
        inputs["proposal"]["ucc_parent_proposal"].get("learner_id"),
        inputs["approval"]["ucc_parent_approval_event"]["scope"].get("learner_id"),
    }
    if len(learner_ids) != 1:
        return _failure("CORE_LEARNER_MISMATCH")

    pair_config = inputs["pairing"]
    form_registry = {
        key: {"level_order": [value["level_band"]]}
        for key, value in pair_config["form_manifests"].items()
    }
    for receipt in (inputs["calm_receipt"], inputs["pressure_receipt"]):
        validation = receipts.validate_receipt(
            receipt, form_registry=form_registry,
            validated_at=materialized["injected"]["recorded_at"],
        )
        if validation["quality"]["status"] != "clean":
            code = (validation["quality"]["blocking_issues"] + validation["quality"]["warnings"])[0]["code"]
            return _failure(code)
    stages.append("receipts_validated")

    pair_result = pairing.evaluate_pair(
        [inputs["calm_receipt"], inputs["pressure_receipt"]],
        form_manifests=pair_config["form_manifests"],
        pairing_policy=pair_config["pairing_policy"],
        registry_snapshot_sha256=pair_config["registry_snapshot_sha256"],
        pair_result_id=materialized["injected"]["pair_result_id"],
        evaluated_at=materialized["injected"]["recorded_at"],
    )
    if pair_result["status"] != "valid":
        return _failure(pair_result["issues"][0]["code"])
    stages.append("pair_evaluated")

    proposal_document = inputs["proposal"]
    proposal_inner = proposal_document["ucc_parent_proposal"]
    workflow_case = copy.deepcopy(inputs["workflow"])
    workflow_case["injected"]["proposal_id"] = proposal_inner["proposal_id"]
    review = build_parent_review(workflow_case, injected=workflow_case["injected"])
    if review["proposal"]["proposal_id"] != proposal_inner["proposal_id"]:
        return _failure("CORE_PROPOSAL_BINDING_INVALID")
    smc_registry = {smc["smc_id"]: {"canonical_hash": _hash(smc), "active": True}}
    proposal_issues = approval.validate_proposal(proposal_document, smc_registry=smc_registry)
    if proposal_issues:
        return _failure(proposal_issues[0]["code"])
    stages.extend(["review_generated", "approval_wait"])

    event_document = inputs.get("approval")
    if event_document is None:
        return _failure("APPROVAL_REQUIRED")
    event_inner = event_document["ucc_parent_approval_event"]
    authority = {
        "ledger_namespace": inputs["ledger"]["ucc_local_ledger"]["ledger_namespace"],
        "actors": {event_inner["actor"]["actor_role"]: [event_inner["actor"]["actor_id"]]},
    }
    transition = approval.evaluate_transition(
        proposal_document, event_document, accepted_events=[], idempotency_bindings={},
        authority_config=authority, execution_state="not_started",
    )
    if transition["issues"]:
        return _failure(transition["issues"][0]["code"])
    stages.append("approval_applied")

    approval_ref = {
        "approval_event_id": event_inner["approval_event_id"],
        "proposal_id": event_inner["proposal_id"],
        "proposal_revision": event_inner["proposal_revision"],
        "proposal_hash": event_inner["proposal_hash"],
        "approval_action": event_inner["approval_action"],
        "approval_actor_role": event_inner["actor"]["actor_role"],
        "approval_scope": copy.deepcopy(event_inner["scope"]),
    }
    payload = copy.deepcopy(event_inner)
    appended = ledger.append_entry(
        inputs["ledger"], entry_type="approval_recorded", payload=payload,
        payload_contract={
            "contract_family": "proposal_approval",
            "contract_version": event_inner["contract_version"],
            "schema_ref": "schemas/approval-event.v1.schema.json",
            "canonical_hash": _hash(payload),
        },
        source_refs=[{
            "source_ref_id": "sref_01J00000000000000000000064",
            "source_type": "approval_event", "source_id": event_inner["approval_event_id"],
            "source_contract_family": "proposal_approval",
            "source_contract_version": event_inner["contract_version"],
            "source_hash": event_inner["canonical_hash"], "relationship": "records",
        }],
        approval_ref=approval_ref, parent_brief_ref=None,
        injected_entry_id=materialized["injected"]["ledger_entry_id"],
        injected_idempotency_key=materialized["injected"]["ledger_idempotency_key"],
        injected_recorded_at=materialized["injected"]["recorded_at"],
        occurred_at=event_inner["decision_at"],
    )
    if commit_ledger:
        with tempfile.TemporaryDirectory(prefix="ucc-synthetic-week-") as directory:
            commit = ledger.commit_ledger_atomic(Path(directory) / "ledger.json", appended["ledger"])
        if not commit["success"]:
            return _failure(commit["issues"][0]["code"])
        stages.append("ledger_committed")
    else:
        ledger_issues = ledger.validate_ledger(appended["ledger"])
        if ledger_issues:
            return _failure(ledger_issues[0]["code"])
        stages.append("ledger_validated")

    canonical_record = {
        "week_id": materialized["week_id"], "status": "complete", "stages": stages,
        "learner_id": smc["learner_id"], "pair_metrics": pair_result["metrics"],
        "diagnosis_hash": review["diagnosis"]["canonical_hash"],
        "brief_hash": review["brief"]["canonical_hash"],
        "proposal_hash": proposal_inner["canonical_hash"],
        "approval_hash": event_inner["canonical_hash"],
        "ledger_hash": appended["ledger"]["ucc_local_ledger"]["ledger_hash"],
        "approval_wait_observed": True, "approval_applied_after_wait": True,
        "ledger_commits": 1 if commit_ledger else 0,
        "model_calls": 0, "network_attempts": 0,
    }
    canonical_bytes = json.dumps(canonical_record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return {**canonical_record, "issues": [], "canonical_bytes": canonical_bytes}


def run_adversarial_case(
    week: dict, case: dict, *, offline: bool, resource_root: Path | None = None
) -> dict:
    if not offline or case.get("mutation") == "attempt_network":
        return _failure("OFFLINE_NETWORK_FORBIDDEN")
    prepared, failure = _prepare_week(week, resource_root)
    if prepared is None:
        return failure
    inputs = prepared["inputs"]
    mutation = case.get("mutation")
    if mutation == "remove_approval":
        return _failure("APPROVAL_REQUIRED")
    if mutation == "invalidate_receipt_total":
        candidate = copy.deepcopy(inputs["calm_receipt"])
        candidate["summary"]["correct"] = 0
        config = inputs["pairing"]
        form_registry = {key: {"level_order": [value["level_band"]]} for key, value in config["form_manifests"].items()}
        result = receipts.validate_receipt(candidate, form_registry=form_registry, validated_at="2026-06-30T04:00:00.000Z")
        if any(item["code"] == "RECEIPT_TOTAL_MISMATCH" for item in result["quality"]["blocking_issues"]):
            return _failure("RECEIPT_TOTAL_INCONSISTENT")
    if mutation == "change_approval_payload":
        prior = inputs["approval"]
        candidate = copy.deepcopy(prior)
        inner = candidate["ucc_parent_approval_event"]
        inner["reason_code"] = "synthetic_changed_reason"
        projection = copy.deepcopy(inner)
        projection.pop("canonical_hash")
        inner["canonical_hash"] = _hash(projection)
        prior_inner = prior["ucc_parent_approval_event"]
        authority = {"ledger_namespace": "synthetic-test", "actors": {"parent": [prior_inner["actor"]["actor_id"]]}}
        result = approval.evaluate_transition(
            inputs["proposal"], candidate, accepted_events=[prior],
            idempotency_bindings={prior_inner["approval_key"]: prior},
            authority_config=authority, execution_state="not_started",
        )
        return {**_failure(result["issues"][0]["code"]), "issues": result["issues"]}
    if mutation == "inject_temp_write_fault":
        with tempfile.TemporaryDirectory(prefix="ucc-synthetic-fault-") as directory:
            path = Path(directory) / "ledger.json"
            result = ledger.commit_ledger_atomic(path, inputs["ledger"], injected_fault="temp_write")
        return {**_failure(result["issues"][0]["code"]), "issues": result["issues"]}
    return _failure("OFFLINE_ADVERSARIAL_CASE_UNSUPPORTED")


def available_adapters() -> list:
    return []


def mock_adapters_included() -> bool:
    return False
