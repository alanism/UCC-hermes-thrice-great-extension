import json
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES = REPO_ROOT / "fixtures" / "red" / "t4_9"


def load_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def core_api():
    return require_product_module("hermes_thrice_great.core.workflow", "CORE_IMPLEMENTATION_MISSING")


def command_api():
    return require_product_module("hermes_thrice_great.plugin.commands", "PLUGIN_COMMAND_IMPLEMENTATION_MISSING")


def test_workflow_fixture_is_synthetic_offline_and_authority_separated():
    case = load_json("workflow_case.json")
    assert case["synthetic"] is True
    assert case["expected"]["approval_status"] == "not_decided"
    assert case["expected"]["ledger_writes"] == case["expected"]["model_calls"] == case["expected"]["network_attempts"] == 0
    assert all((REPO_ROOT / path).is_file() for path in case["inputs"].values())


def test_negative_and_mutation_fixtures_use_stable_contract_codes():
    cases = load_json("negative_cases.json")
    assert len(cases) == 6
    assert all(case["expected_issue"].startswith(("CORE_", "BRIEF_", "APPROVAL_", "PLUGIN_")) for case in cases)
    probe = load_json("mutation_probe.json")
    assert all(item["expected_outcome"] == "KILLED" for item in probe["killable"])
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


def test_diagnosis_brief_and_proposal_are_byte_repeatable_with_injected_dependencies():
    api = core_api()
    case = load_json("workflow_case.json")
    first = api.build_parent_review(case, injected=case["injected"])
    second = api.build_parent_review(case, injected=case["injected"])
    assert first == second
    assert first["diagnosis"]["kind"] == case["expected"]["diagnosis_kind"]
    assert set(first["brief"]["claim_labels"]) <= set(case["expected"]["brief_claim_labels"])
    assert first["proposal"]["proposal_status"] == "ready_for_parent"
    assert first["approval_status"] == "not_decided"
    assert first["ledger_writes"] == first["model_calls"] == first["network_attempts"] == 0


@pytest.mark.parametrize("case", load_json("negative_cases.json")[:-1], ids=lambda value: value["case_id"])
def test_invalid_core_inputs_return_stable_issue_without_side_effects(case):
    api = core_api()
    result = api.evaluate_negative_case(load_json("workflow_case.json"), case)
    assert case["expected_issue"] in [issue["code"] for issue in result["issues"]]
    assert result["ledger_writes"] == result["model_calls"] == result["network_attempts"] == 0


@pytest.mark.parametrize("command", load_json("workflow_case.json")["commands"])
def test_offline_plugin_commands_are_registered_and_side_effect_free(command):
    api = command_api()
    result = api.execute(command, fixture=load_json("workflow_case.json"), offline=True)
    assert result["exit_code"] == 0
    assert result["model_calls"] == result["network_attempts"] == result["ledger_writes"] == 0


def test_unknown_or_outbound_command_is_rejected():
    api = command_api()
    result = api.execute("ucc send", fixture=load_json("workflow_case.json"), offline=True)
    assert "PLUGIN_COMMAND_UNSUPPORTED" in [issue["code"] for issue in result["issues"]]


def test_core_mutation_probe_uses_r4_outcomes():
    api = core_api()
    outcomes = api.run_mutation_probe(load_json("workflow_case.json"), load_json("mutation_probe.json"))
    for mutant in load_json("mutation_probe.json")["killable"]:
        assert outcomes[mutant["mutant_id"]] == "KILLED"
    assert outcomes["diagnosis-fact-key-order-only"] in {"SURVIVED", "SKIPPED"}
