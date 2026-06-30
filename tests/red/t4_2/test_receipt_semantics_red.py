import copy
import json
from datetime import datetime
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = REPO_ROOT / "fixtures" / "red" / "t4_2"


def load_json(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def pointer_parent(document, pointer):
    tokens = pointer.lstrip("/").split("/")
    parent = document
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
    key = int(tokens[-1]) if isinstance(parent, list) else tokens[-1]
    return parent, key


def mutate(document, operations):
    result = copy.deepcopy(document)
    for operation in operations:
        parent, key = pointer_parent(result, operation["path"])
        if operation["op"] == "replace":
            parent[key] = operation["value"]
        else:
            raise AssertionError(f"unsupported operation {operation['op']}")
    return result


def receipt_api():
    return require_product_module(
        "hermes_thrice_great.contracts.receipts",
        "RECEIPT_VALIDATOR_IMPLEMENTATION_MISSING",
    )


def test_positive_receipt_fixture_has_valid_arithmetic_chronology_and_timer():
    receipt = load_json("positive_receipt.json")
    events = receipt["events"]
    summary = receipt["summary"]
    answered = [event for event in events if event["response_status"] == "answered"]
    assert summary["items_presented"] == len(events)
    assert summary["items_answered"] == len(answered)
    assert summary["correct"] == sum(event["is_correct"] is True for event in answered)
    assert summary["incorrect"] == sum(event["is_correct"] is False for event in answered)
    assert summary["timeouts"] == sum(event["response_status"] == "timeout" for event in events)
    assert summary["skipped"] == sum(event["response_status"] == "skipped" for event in events)
    started = datetime.fromisoformat(receipt["session"]["started_at"].replace("Z", "+00:00"))
    completed = datetime.fromisoformat(receipt["session"]["completed_at"].replace("Z", "+00:00"))
    assert started <= completed
    assert receipt["assessment"]["mode"] == "calm"
    assert receipt["assessment"]["timer_policy"] == {
        "timer_visible": False,
        "time_limit_seconds": None,
        "timeout_behavior": "none",
        "policy_id": "calm-no-timer-v1",
    }


def test_negative_receipt_mutations_are_complete_and_use_locked_issue_codes():
    positive = load_json("positive_receipt.json")
    cases = load_json("negative_mutations.json")
    assert len(cases) == 9
    for case in cases:
        mutated = mutate(positive, case["operations"])
        assert mutated["contract_version"] == "ucc.assessment_receipt.v2.0.0"
        assert case["expected_issue"].startswith("RECEIPT_")
        assert case["expected_quality"] in {"limited", "degraded", "void"}


def test_mutation_probe_obeys_r4_outcome_contract():
    probe = load_json("mutation_probe.json")
    assert probe["killable"]["expected_outcome"] == "KILLED"
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


def test_positive_receipt_is_accepted_with_recomputed_clean_quality():
    api = receipt_api()
    result = api.validate_receipt(
        load_json("positive_receipt.json"),
        form_registry={"synthetic-math-form-a@1": {"level_order": ["grade-3"]}},
        validated_at="2026-06-30T00:06:00.000Z",
    )
    assert result["quality"]["status"] == "clean"
    assert result["accepted_for_storage"] is True
    assert result["accepted_for_pairing"] is True


@pytest.mark.parametrize("case", load_json("negative_mutations.json"), ids=lambda item: item["case_id"])
def test_negative_receipts_return_locked_issue_and_quality(case):
    api = receipt_api()
    receipt = mutate(load_json("positive_receipt.json"), case["operations"])
    result = api.validate_receipt(
        receipt,
        form_registry={"synthetic-math-form-a@1": {"level_order": ["grade-3"]}},
        validated_at="2026-06-30T00:06:00.000Z",
    )
    codes = [issue["code"] for issue in result["quality"]["blocking_issues"] + result["quality"]["warnings"]]
    assert case["expected_issue"] in codes
    assert result["quality"]["status"] == case["expected_quality"]


def test_same_receipt_and_injected_context_are_deterministic():
    api = receipt_api()
    kwargs = {
        "form_registry": {"synthetic-math-form-a@1": {"level_order": ["grade-3"]}},
        "validated_at": "2026-06-30T00:06:00.000Z",
    }
    first = api.validate_receipt(load_json("positive_receipt.json"), **kwargs)
    second = api.validate_receipt(load_json("positive_receipt.json"), **kwargs)
    assert first == second


def test_receipt_mutation_probe_kills_denominator_change_and_preserves_key_order_control():
    api = receipt_api()
    outcomes = api.run_mutation_probe(
        load_json("positive_receipt.json"),
        load_json("mutation_probe.json"),
    )
    assert outcomes["accuracy-denominator-includes-timeouts"] == "KILLED"
    assert outcomes["canonical-object-key-order-only"] in {"SURVIVED", "SKIPPED"}
