import json
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES = REPO_ROOT / "fixtures" / "red" / "t4_10"


def load_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def orchestrator_api():
    return require_product_module("hermes_thrice_great.orchestration.week", "WEEK_ORCHESTRATOR_IMPLEMENTATION_MISSING")


def test_week_fixture_is_synthetic_offline_and_composed_from_validated_red_fixtures():
    week = load_json("synthetic_week.json")
    assert week["synthetic"] is week["offline"] is True
    assert all((REPO_ROOT / path).is_file() for path in week["inputs"].values())
    assert week["expected"]["model_calls"] == week["expected"]["network_attempts"] == 0
    assert week["expected"]["approval_wait_observed"] is True


def test_adversarial_week_cases_are_closed_and_side_effect_free():
    cases = load_json("adversarial_week_cases.json")
    assert len(cases) == 5
    assert all(case["ledger_commits"] == 0 for case in cases)
    assert all(case["expected_issue"].startswith(("APPROVAL_", "IDEMPOTENCY_", "RECEIPT_", "LEDGER_", "OFFLINE_")) for case in cases)


def test_valid_synthetic_week_waits_for_approval_then_commits_once_offline():
    api = orchestrator_api()
    result = api.run_week(load_json("synthetic_week.json"), offline=True)
    assert result["status"] == "complete"
    assert result["approval_wait_observed"] is True
    assert result["approval_applied_after_wait"] is True
    assert result["ledger_commits"] == 1
    assert result["model_calls"] == result["network_attempts"] == 0


def test_two_runs_with_same_injected_dependencies_are_byte_identical():
    api = orchestrator_api()
    week = load_json("synthetic_week.json")
    first = api.run_week(week, offline=True)
    second = api.run_week(week, offline=True)
    assert first["canonical_bytes"] == second["canonical_bytes"]
    assert first["ledger_hash"] == second["ledger_hash"]


@pytest.mark.parametrize("case", load_json("adversarial_week_cases.json"), ids=lambda value: value["case_id"])
def test_adversarial_week_fails_closed_without_ledger_commit(case):
    api = orchestrator_api()
    result = api.run_adversarial_case(load_json("synthetic_week.json"), case, offline=True)
    assert case["expected_issue"] in [issue["code"] for issue in result["issues"]]
    assert result["ledger_commits"] == 0
    assert result["model_calls"] == result["network_attempts"] == 0


def test_week_runner_has_no_live_adapter_surface():
    api = orchestrator_api()
    assert api.available_adapters() == []
    assert api.mock_adapters_included() is False
