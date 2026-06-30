import copy
import hashlib
import json
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = REPO_ROOT / "fixtures" / "red" / "t4_5"


def load_json(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def canonical_hash(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def clean_extensions(value):
    if isinstance(value, dict):
        return {key: clean_extensions(item) for key, item in value.items() if key != "extensions"}
    if isinstance(value, list):
        return [clean_extensions(item) for item in value]
    return value


def pointer_parent(document, pointer):
    tokens = pointer.lstrip("/").split("/")
    parent = document
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
    key = int(tokens[-1]) if isinstance(parent, list) else tokens[-1]
    return parent, key


def apply_mutation(document, case):
    result = copy.deepcopy(document)
    if case["operation"] == "rename_root":
        result[case["value"]] = result.pop("ucc_local_ledger")
        return result
    parent, key = pointer_parent(result, case["path"])
    parent[key] = copy.deepcopy(case["value"])
    return result


def ledger_api():
    return require_product_module(
        "hermes_thrice_great.contracts.ledger",
        "LEDGER_IMPLEMENTATION_MISSING",
    )


def entry(document):
    return document["ucc_local_ledger"]["entries"][0]["ucc_ledger_entry"]


def test_positive_ledger_fixture_has_exact_closed_envelopes_and_hashes():
    document = load_json("positive_ledger.json")
    assert set(document) == {"ucc_local_ledger"}
    ledger = document["ucc_local_ledger"]
    assert set(ledger) == {
        "ledger_schema_version", "ledger_id", "ledger_namespace", "created_at",
        "retention_policy_ref", "entry_count", "head_sequence", "head_entry_hash",
        "entries", "ledger_hash",
    }
    item = entry(document)
    assert set(item) == {
        "contract_version", "ledger_entry_id", "idempotency_key", "entry_type",
        "sequence", "occurred_at", "recorded_at", "previous_entry_hash",
        "payload_contract", "payload", "source_refs", "approval_ref",
        "parent_brief_ref", "canonical_hash",
    }
    assert item["previous_entry_hash"] is None
    assert canonical_hash(item["payload"]) == item["payload_contract"]["canonical_hash"]
    projection = clean_extensions(item)
    projection.pop("canonical_hash")
    assert canonical_hash(projection) == item["canonical_hash"]
    ledger_projection = {
        key: ledger[key]
        for key in (
            "ledger_schema_version", "ledger_id", "ledger_namespace", "created_at",
            "retention_policy_ref", "entry_count", "head_sequence", "head_entry_hash",
        )
    }
    ledger_projection["ordered_entry_hashes"] = [item["canonical_hash"]]
    assert canonical_hash(ledger_projection) == ledger["ledger_hash"]


def test_nested_reference_and_lifecycle_fixtures_match_locked_shapes():
    item = entry(load_json("positive_ledger.json"))
    assert set(item["payload_contract"]) == {
        "contract_family", "contract_version", "schema_ref", "canonical_hash"
    }
    assert set(item["source_refs"][0]) == {
        "source_ref_id", "source_type", "source_id", "source_contract_family",
        "source_contract_version", "source_hash", "relationship",
    }
    assert set(item["approval_ref"]) == {
        "approval_event_id", "proposal_id", "proposal_revision", "proposal_hash",
        "approval_action", "approval_actor_role", "approval_scope",
    }
    assert item["parent_brief_ref"] is None
    lifecycle = load_json("lifecycle_payloads.json")
    assert set(lifecycle["retention_policy_recorded"]) == {
        "retention_policy_id", "policy_version", "recorded_by_actor_role",
        "effective_at", "entry_type_rules", "hold_codes",
    }
    assert set(lifecycle["deletion_requested"]) == {
        "deletion_request_id", "target_entry_ids", "policy_id", "reason_code",
        "requested_by_actor_role", "requested_by_actor_id", "requested_at",
        "redaction_scope", "request_key",
    }
    tombstone = lifecycle["tombstone_recorded"]
    assert set(tombstone) == {
        "tombstone_id", "target_entry_id", "reason_code", "requested_by_actor_role",
        "requested_at", "redaction_scope", "retained_audit_hashes",
    }
    forbidden = {"learner_id", "display_name", "answer", "evidence_body", "reason_note"}
    assert forbidden.isdisjoint(tombstone)


def test_negative_and_fault_fixtures_use_stable_issue_and_r4_outcome_codes():
    cases = load_json("negative_mutations.json")
    assert len(cases) == 10
    assert all(case["expected_issue"].startswith("LEDGER_") for case in cases)
    for case in cases:
        assert set(apply_mutation(load_json("positive_ledger.json"), case))
    faults = load_json("replay_fault_cases.json")
    assert all(case["expected_issue"].startswith("LEDGER_") for case in faults["faults"])
    probe = load_json("mutation_probe.json")
    assert all(item["expected_outcome"] == "KILLED" for item in probe["killable"])
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


def test_positive_ledger_and_entry_envelopes_validate():
    api = ledger_api()
    assert api.validate_ledger(load_json("positive_ledger.json")) == []


@pytest.mark.parametrize("case", load_json("negative_mutations.json"), ids=lambda value: value["case_id"])
def test_invalid_ledgers_return_locked_primary_issue(case):
    api = ledger_api()
    candidate = apply_mutation(load_json("positive_ledger.json"), case)
    issues = api.validate_ledger(candidate)
    assert case["expected_issue"] in [issue["code"] for issue in issues]


def test_entry_identity_is_injected_and_append_order_hash_chain_is_exact():
    api = ledger_api()
    document = load_json("positive_ledger.json")
    candidate_payload = {"proposal_id": "prop_01J00000000000000000000010", "proposal_revision": 2}
    result = api.append_entry(
        document,
        entry_type="proposal_recorded",
        payload=candidate_payload,
        payload_contract={
            "contract_family": "proposal_approval",
            "contract_version": "ucc.proposal.v1.0.0",
            "schema_ref": "schemas/proposal.v1.schema.json",
            "canonical_hash": canonical_hash(candidate_payload),
        },
        source_refs=[], approval_ref=None, parent_brief_ref=None,
        injected_entry_id="ldgr_01J00000000000000000000040",
        injected_idempotency_key="idem_01J00000000000000000000041",
        injected_recorded_at="2026-06-30T01:00:03.000Z",
        occurred_at="2026-06-30T01:00:03.000Z",
    )
    appended = result["entry"]["ucc_ledger_entry"]
    assert appended["ledger_entry_id"] == "ldgr_01J00000000000000000000040"
    assert appended["sequence"] == 2
    assert appended["previous_entry_hash"] == entry(document)["canonical_hash"]


def test_identical_replay_is_idempotent_and_changed_payload_conflicts():
    api = ledger_api()
    document = load_json("positive_ledger.json")
    original = entry(document)
    replay = api.append_prebuilt_entry(document, {"ucc_ledger_entry": copy.deepcopy(original)})
    assert replay["replayed"] is True
    assert replay["append"] is False
    changed = copy.deepcopy(original)
    changed["payload"]["approval_action"] = "reject"
    conflict = api.append_prebuilt_entry(document, {"ucc_ledger_entry": changed})
    assert "LEDGER_IDEMPOTENCY_CONFLICT" in [issue["code"] for issue in conflict["issues"]]


@pytest.mark.parametrize("fault", load_json("replay_fault_cases.json")["faults"], ids=lambda value: value["fault"])
def test_injected_write_fault_preserves_prior_valid_ledger_and_never_commits_partial(tmp_path, fault):
    api = ledger_api()
    ledger_path = tmp_path / "ledger.json"
    prior = json.dumps(load_json("positive_ledger.json"), sort_keys=True, separators=(",", ":")).encode()
    ledger_path.write_bytes(prior)
    result = api.commit_ledger_atomic(
        ledger_path,
        load_json("positive_ledger.json"),
        injected_fault=fault["fault"],
    )
    if fault.get("prior_bytes_unchanged"):
        assert ledger_path.read_bytes() == prior
    assert result.get("success") is not True
    assert fault["expected_issue"] in [issue["code"] for issue in result["issues"]]
    assert not list(tmp_path.glob("*.partial.committed"))


def test_retention_deletion_and_tombstone_are_two_event_atomic_history():
    api = ledger_api()
    lifecycle = load_json("lifecycle_payloads.json")
    result = api.apply_deletion(
        load_json("positive_ledger.json"),
        deletion_request=lifecycle["deletion_requested"],
        tombstone=lifecycle["tombstone_recorded"],
        retention_policy=lifecycle["retention_policy_recorded"],
    )
    assert [item["entry_type"] for item in result["appended_entries"]] == [
        "deletion_requested", "tombstone_recorded"
    ]
    assert result["in_place_erasure"] is False
    serialized_tombstone = json.dumps(result["appended_entries"][1], sort_keys=True)
    assert all(term not in serialized_tombstone for term in ("learner_id", "display_name", "evidence_body"))


def test_namespaced_extensions_are_inert_and_unknown_fields_fail():
    api = ledger_api()
    document = load_json("positive_ledger.json")
    document["ucc_local_ledger"]["extensions"] = {"org.example.note": {"synthetic": True}}
    assert api.validate_ledger(document) == []
    document["ucc_local_ledger"]["outside_extensions"] = True
    assert "LEDGER_UNKNOWN_FIELD" in [issue["code"] for issue in api.validate_ledger(document)]


def test_ledger_mutation_probe_uses_r4_outcomes():
    api = ledger_api()
    outcomes = api.run_mutation_probe(
        load_json("positive_ledger.json"),
        load_json("lifecycle_payloads.json"),
        load_json("mutation_probe.json"),
    )
    for mutant in load_json("mutation_probe.json")["killable"]:
        assert outcomes[mutant["mutant_id"]] == "KILLED"
    assert outcomes["canonical-object-key-order-only"] in {"SURVIVED", "SKIPPED"}
