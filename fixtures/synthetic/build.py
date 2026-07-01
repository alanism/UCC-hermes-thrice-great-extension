"""Materialize the closed, coherent synthetic weekly fixture set."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
LEARNER_ID = "lrn_01J00000000000000000000020"


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write(relative: str, value) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def clean_extensions(value):
    if isinstance(value, dict):
        return {key: clean_extensions(item) for key, item in value.items() if key != "extensions"}
    if isinstance(value, list):
        return [clean_extensions(item) for item in value]
    return value


def canonical_hash(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def set_pointer(document, pointer, value) -> None:
    tokens = pointer.lstrip("/").split("/")
    parent = document
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
    key = int(tokens[-1]) if isinstance(parent, list) else tokens[-1]
    parent[key] = copy.deepcopy(value)


smc = {
    "contract_version": "ucc.smc.v1.0.0",
    "smc_id": "smc_01J00000000000000000000015",
    "revision": 1,
    "lifecycle_status": "active",
    "learner_id": LEARNER_ID,
    "display_name": None,
    "created_at": "2026-06-30T00:00:00.000Z",
    "effective_at": "2026-06-30T00:00:00.000Z",
    "source": {"format": "synthetic_json", "source_hash": "1" * 64, "local_source_label": "synthetic-week-smc"},
    "authorship": {"actor_type": "parent_guardian", "actor_id": "act_01J0000000000000000000001A", "authored_at": "2026-06-30T00:00:00.000Z"},
    "supersedes_revision": None,
    "amendment_decision": None,
    "canvas": {
        "learner_context": {"age_years": None, "grade_stage": "synthetic-grade-3", "schooling_context": "other", "schooling_context_other_label": "synthetic-context", "exported_date": "2026-06-30"},
        "educational_vision": {"vision": "Synthetic evidence-led learning."},
        "teaching_approach": {"style": "collaborative", "pacing": "cyclic", "evaluation_methods": ["demonstration", "testing"], "other_labels": None},
        "learning_preferences": {"modalities": ["mixed"], "environments": ["structured"], "scope": "mixed", "other_labels": None},
        "communication_authority": {"communication_mode": "discussion", "adult_role": "guide", "other_labels": None},
        "physical_activity": {"frequency": None, "activity_types": [], "goals": []},
        "socializing": {"peer_interaction": None, "group_learning_enabled": False, "group_learning_notes": None, "community_involvement": []},
        "technology": {"available_devices": ["synthetic-device"], "screen_time_policy": "synthetic-policy", "digital_literacy_goals": []},
        "enrichment": {"extracurriculars": [], "special_interests": [], "field_experiences": []},
        "confidence_building": {"strategies": [], "known_challenges": [], "support_resources": []},
        "family_values": {"educational_philosophies": ["synthetic-evidence-first"], "cultural_religious_considerations": [], "long_term_vision": "Synthetic fixture vision."},
        "learning_environment": {"learning_spaces": ["synthetic-space"], "distractions_and_mitigations": [], "schedule_flexibility": "mixed", "schedule_flexibility_other_label": None},
        "resources_budget": {"curriculum_materials": [], "budget_note": None, "support_network": []},
        "guardian_expectations": {"weekly_time_commitment": "synthetic-weekly", "co_learning": "sometimes", "adaptability": "synthetic-adaptability"},
    },
}

calm = load("fixtures/red/t4_2/positive_receipt.json")
calm["learner_id"] = LEARNER_ID

pair_recipe = load("fixtures/red/t4_3/positive_pair.json")
pressure = copy.deepcopy(calm)
for override in pair_recipe["pressure_overrides"]:
    set_pointer(pressure, override["path"], override["value"])
pressure["learner_id"] = LEARNER_ID

proposal = load("fixtures/red/t4_4/positive_proposal.json")
proposal_inner = proposal["ucc_parent_proposal"]
proposal_inner["learner_id"] = LEARNER_ID
proposal_inner["smc_ref"]["canonical_hash"] = canonical_hash(smc)
proposal_inner["smc_ref"]["source_path"] = "fixtures/synthetic/valid/smc.json"
proposal_projection = clean_extensions(proposal_inner)
proposal_projection.pop("canonical_hash")
proposal_projection.pop("proposal_status")
proposal_inner["canonical_hash"] = canonical_hash(proposal_projection)

approval = load("fixtures/red/t4_4/positive_approval_event.json")
approval_inner = approval["ucc_parent_approval_event"]
approval_inner["proposal_hash"] = proposal_inner["canonical_hash"]
approval_inner["scope"]["learner_id"] = LEARNER_ID
approval_projection = clean_extensions(approval_inner)
approval_projection.pop("canonical_hash")
approval_inner["canonical_hash"] = canonical_hash(approval_projection)

retention = load("fixtures/red/t4_5/positive_ledger.json")["ucc_local_ledger"]["retention_policy_ref"]
ledger = {
    "ucc_local_ledger": {
        "ledger_schema_version": "ucc.ledger_file.v1.0.0",
        "ledger_id": "ledg_01J00000000000000000000060",
        "ledger_namespace": "synthetic-test",
        "created_at": "2026-06-30T03:59:59.000Z",
        "retention_policy_ref": retention,
        "entry_count": 0,
        "head_sequence": 0,
        "head_entry_hash": None,
        "entries": [],
        "ledger_hash": "",
    }
}
ledger_projection = {key: ledger["ucc_local_ledger"][key] for key in (
    "ledger_schema_version", "ledger_id", "ledger_namespace", "created_at",
    "retention_policy_ref", "entry_count", "head_sequence", "head_entry_hash",
)}
ledger_projection["ordered_entry_hashes"] = []
ledger["ucc_local_ledger"]["ledger_hash"] = canonical_hash(ledger_projection)

workflow = load("fixtures/red/t4_9/workflow_case.json")
workflow["learner_id"] = LEARNER_ID
workflow["inputs"] = {
    "receipt": "fixtures/synthetic/valid/calm-receipt.json",
    "pair": "fixtures/synthetic/valid/pairing.json",
    "proposal": "fixtures/synthetic/valid/proposal.json",
}

pairing = {
    "calm_receipt": "fixtures/synthetic/valid/calm-receipt.json",
    "pressure_receipt": "fixtures/synthetic/valid/pressure-receipt.json",
    "form_manifests": pair_recipe["form_manifests"],
    "pairing_policy": pair_recipe["pairing_policy"],
    "registry_snapshot_sha256": pair_recipe["registry_snapshot_sha256"],
    "expected_metrics": pair_recipe["expected_metrics"],
}

week = {
    "fixture_schema_version": "ucc.synthetic_week_fixture.v1.0.0",
    "week_id": "synthetic-week-0001",
    "synthetic": True,
    "offline": True,
    "inputs": {
        "smc": "fixtures/synthetic/valid/smc.json",
        "calm_receipt": "fixtures/synthetic/valid/calm-receipt.json",
        "pressure_receipt": "fixtures/synthetic/valid/pressure-receipt.json",
        "pairing": "fixtures/synthetic/valid/pairing.json",
        "proposal": "fixtures/synthetic/valid/proposal.json",
        "approval": "fixtures/synthetic/valid/approval.json",
        "ledger": "fixtures/synthetic/valid/ledger.json",
        "workflow": "fixtures/synthetic/valid/workflow.json",
    },
    "injected": {
        "week_start": "2026-06-30T00:00:00.000Z",
        "week_end": "2026-07-06T23:59:59.999Z",
        "pair_result_id": "pres_01J00000000000000000000061",
        "ledger_entry_id": "ldgr_01J00000000000000000000062",
        "ledger_idempotency_key": "idem_01J00000000000000000000063",
        "recorded_at": "2026-06-30T04:00:01.000Z",
        "id_seed": "synthetic-week-0001",
    },
}

adversarial = {
    "fixture_schema_version": "ucc.synthetic_week_adversarial.v1.0.0",
    "synthetic": True,
    "base_week": "fixtures/synthetic/valid/week.json",
    "cases": load("fixtures/red/t4_10/adversarial_week_cases.json"),
}

for name, value in {
    "valid/smc.json": smc,
    "valid/calm-receipt.json": calm,
    "valid/pressure-receipt.json": pressure,
    "valid/pairing.json": pairing,
    "valid/proposal.json": proposal,
    "valid/approval.json": approval,
    "valid/ledger.json": ledger,
    "valid/workflow.json": workflow,
    "valid/week.json": week,
    "adversarial/week-cases.json": adversarial,
}.items():
    write(name, value)
