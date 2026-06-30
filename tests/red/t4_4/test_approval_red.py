import copy
import hashlib
import json
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = REPO_ROOT / "fixtures" / "red" / "t4_4"


def load_json(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def clean_extensions(value):
    if isinstance(value, dict):
        return {key: clean_extensions(item) for key, item in value.items() if key != "extensions"}
    if isinstance(value, list):
        return [clean_extensions(item) for item in value]
    return value


def canonical_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def recompute_proposal(document):
    proposal = document["ucc_parent_proposal"]
    projection = clean_extensions(proposal)
    projection.pop("canonical_hash")
    projection.pop("proposal_status")
    proposal["canonical_hash"] = canonical_hash(projection)
    return document


def recompute_event(document):
    event = document["ucc_parent_approval_event"]
    projection = clean_extensions(event)
    projection.pop("canonical_hash")
    event["canonical_hash"] = canonical_hash(projection)
    return document


def pointer_parent(document, pointer):
    tokens = pointer.lstrip("/").split("/")
    parent = document
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
    key = int(tokens[-1]) if isinstance(parent, list) else tokens[-1]
    return parent, key


def apply_operations(document, operations):
    result = copy.deepcopy(document)
    for operation in operations:
        parent, key = pointer_parent(result, operation["path"])
        if operation["op"] == "remove":
            parent.pop(key)
        elif operation["op"] in {"replace", "add"}:
            parent[key] = copy.deepcopy(operation["value"])
        else:
            raise AssertionError(operation["op"])
    return result


def approval_api():
    return require_product_module(
        "hermes_thrice_great.contracts.approval",
        "APPROVAL_EVALUATOR_IMPLEMENTATION_MISSING",
    )


def authority_config():
    return {
        "ledger_namespace": "synthetic-test",
        "actors": {
            role: ["act_01J0000000000000000000001A"]
            for role in load_json("valid_actor_roles.json")
        },
        "allow_synthetic_capture": True,
    }


def smc_registry():
    return {"smc_01J00000000000000000000015": {"canonical_hash": "1" * 64, "active": True}}


def test_positive_proposal_and_event_fixtures_have_exact_hashes_and_separated_authorship():
    proposal_doc = load_json("positive_proposal.json")
    event_doc = load_json("positive_approval_event.json")
    proposal = proposal_doc["ucc_parent_proposal"]
    event = event_doc["ucc_parent_approval_event"]
    projection = clean_extensions(proposal)
    projection.pop("canonical_hash")
    projection.pop("proposal_status")
    assert proposal["canonical_hash"] == canonical_hash(projection)
    event_projection = clean_extensions(event)
    event_projection.pop("canonical_hash")
    assert event["canonical_hash"] == canonical_hash(event_projection)
    assert event["proposal_hash"] == proposal["canonical_hash"]
    assert proposal["authorship"]["proposal_author"]["actor_role"] == "ai"
    assert proposal["authorship"]["evidence_producers"][0]["producer_role"] == "system"
    assert event["actor"]["actor_role"] == "parent"
    assert "approval_actor" not in proposal["authorship"]


def test_negative_and_replay_fixtures_materialize_with_locked_issue_codes():
    proposal = load_json("positive_proposal.json")
    event = load_json("positive_approval_event.json")
    cases = load_json("negative_mutations.json")
    assert len(cases) == 13
    for case in cases:
        source = proposal if case["document"] == "proposal" else event
        mutated = apply_operations(source, case["operations"])
        assert set(mutated) == ({"ucc_parent_proposal"} if case["document"] == "proposal" else {"ucc_parent_approval_event"})
        assert case["expected_issue"].startswith(("PROPOSAL_", "APPROVAL_", "IDEMPOTENCY_"))
    replay = load_json("replay_cases.json")
    assert {case["expected_issue"] for case in replay if "expected_issue" in case} == {
        "IDEMPOTENCY_CONFLICT",
        "APPROVAL_DECISION_CONFLICT",
    }


def test_mutation_probe_obeys_r4_outcome_contract():
    probe = load_json("mutation_probe.json")
    assert all(item["expected_outcome"] == "KILLED" for item in probe["killable"])
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


def test_positive_proposal_and_approval_event_validate():
    api = approval_api()
    proposal = load_json("positive_proposal.json")
    event = load_json("positive_approval_event.json")
    assert api.validate_proposal(proposal, smc_registry=smc_registry()) == []
    assert api.validate_approval_event(event, proposal=proposal, authority_config=authority_config()) == []


@pytest.mark.parametrize("role", load_json("valid_actor_roles.json"))
def test_all_three_human_actor_roles_are_valid(role):
    api = approval_api()
    proposal = load_json("positive_proposal.json")
    event = load_json("positive_approval_event.json")
    event["ucc_parent_approval_event"]["actor"]["actor_role"] = role
    recompute_event(event)
    assert api.validate_approval_event(event, proposal=proposal, authority_config=authority_config()) == []


@pytest.mark.parametrize("case", load_json("negative_mutations.json"), ids=lambda item: item["case_id"])
def test_invalid_proposal_and_approval_documents_return_stable_issue(case):
    api = approval_api()
    proposal = load_json("positive_proposal.json")
    event = load_json("positive_approval_event.json")
    source = proposal if case["document"] == "proposal" else event
    mutated = apply_operations(source, case["operations"])
    if case["document"] == "proposal":
        issues = api.validate_proposal(mutated, smc_registry=smc_registry())
    else:
        issues = api.validate_approval_event(mutated, proposal=proposal, authority_config=authority_config())
    assert case["expected_issue"] in [issue["code"] for issue in issues]


def test_identical_replay_is_idempotent_and_does_not_append_twice():
    api = approval_api()
    proposal = load_json("positive_proposal.json")
    event = load_json("positive_approval_event.json")
    first = api.evaluate_transition(proposal, event, accepted_events=[], idempotency_bindings={}, authority_config=authority_config(), execution_state="not_started")
    second = api.evaluate_transition(proposal, event, accepted_events=[event], idempotency_bindings={event["ucc_parent_approval_event"]["approval_key"]: event}, authority_config=authority_config(), execution_state="not_started")
    assert first["next_proposal_status"] == "approved"
    assert second["replayed"] is True
    assert second["append_event"] is False


@pytest.mark.parametrize("case", load_json("replay_cases.json")[1:], ids=lambda item: item["case_id"])
def test_changed_payload_cross_revision_and_decision_conflicts(case):
    api = approval_api()
    proposal = load_json("positive_proposal.json")
    event = load_json("positive_approval_event.json")
    prior = copy.deepcopy(event)
    candidate = copy.deepcopy(event)
    inner = candidate["ucc_parent_approval_event"]
    if case["case_id"] == "changed-payload-same-key":
        set_parent, key = pointer_parent(candidate, case["mutation"]["path"])
        set_parent[key] = case["mutation"]["value"]
    elif case["case_id"] == "r1-to-r2-same-key":
        proposal = copy.deepcopy(proposal)
        proposal_inner = proposal["ucc_parent_proposal"]
        proposal_inner["proposal_revision"] = 2
        proposal_inner["supersedes_revision"] = 1
        proposal_inner["proposal_payload"]["rationale"] = "Synthetic revision two rationale."
        recompute_proposal(proposal)
        inner["proposal_revision"] = case["proposal_revision"]
        inner["proposal_hash"] = proposal_inner["canonical_hash"]
        inner["scope"]["proposal_revision"] = 2
    else:
        inner["approval_key"] = case["approval_key"]
        inner["approval_action"] = case["approval_action"]
        inner["approval_event_id"] = "appr_01J0000000000000000000001C"
        inner["scope"]["decision_effect"] = case["approval_action"]
    recompute_event(candidate)
    result = api.evaluate_transition(proposal, candidate, accepted_events=[prior], idempotency_bindings={prior["ucc_parent_approval_event"]["approval_key"]: prior}, authority_config=authority_config(), execution_state="not_started")
    assert case["expected_issue"] in [issue["code"] for issue in result["issues"]]


def test_namespaced_extensions_are_inert_but_unknown_fields_fail():
    api = approval_api()
    proposal = load_json("positive_proposal.json")
    proposal["ucc_parent_proposal"]["extensions"] = {"org.example.note": {"synthetic": True}}
    assert api.validate_proposal(proposal, smc_registry=smc_registry()) == []
    proposal["ucc_parent_proposal"]["outside_extensions"] = True
    issues = api.validate_proposal(proposal, smc_registry=smc_registry())
    assert "PROPOSAL_UNKNOWN_FIELD" in [issue["code"] for issue in issues]


def test_approval_mutation_probe_uses_r4_outcomes():
    api = approval_api()
    outcomes = api.run_mutation_probe(
        load_json("positive_proposal.json"),
        load_json("positive_approval_event.json"),
        load_json("mutation_probe.json"),
    )
    for mutant in load_json("mutation_probe.json")["killable"]:
        assert outcomes[mutant["mutant_id"]] == "KILLED"
    assert outcomes["canonical-object-key-order-only"] in {"SURVIVED", "SKIPPED"}
