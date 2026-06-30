import copy
import json
from datetime import datetime
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = REPO_ROOT / "fixtures" / "red" / "t4_3"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def set_pointer(document, pointer, value):
    tokens = pointer.lstrip("/").split("/")
    parent = document
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
    key = int(tokens[-1]) if isinstance(parent, list) else tokens[-1]
    parent[key] = copy.deepcopy(value)


def materialize_pair():
    case = load_json(FIXTURE_ROOT / "positive_pair.json")
    calm = load_json(REPO_ROOT / case["calm_receipt_fixture"])
    pressure = copy.deepcopy(calm)
    for override in case["pressure_overrides"]:
        set_pointer(pressure, override["path"], override["value"])
    return calm, pressure, case


def materialize_negative(case):
    calm, pressure, pair = materialize_pair()
    policy = copy.deepcopy(pair["pairing_policy"])
    for operation in case["operations"]:
        target = pressure if operation["target"] == "pressure" else policy
        set_pointer(target, operation["path"], operation["value"])
    return calm, pressure, policy, pair


def pairing_api():
    return require_product_module(
        "hermes_thrice_great.contracts.pairing",
        "PAIRING_EVALUATOR_IMPLEMENTATION_MISSING",
    )


def test_positive_pair_fixture_is_coherent_and_metrics_are_unambiguous():
    calm, pressure, case = materialize_pair()
    assert calm["paired_run_id"] == pressure["paired_run_id"]
    assert calm["learner_id"] == pressure["learner_id"]
    assert {calm["assessment"]["mode"], pressure["assessment"]["mode"]} == {"calm", "pressure"}
    calm_completed = datetime.fromisoformat(calm["session"]["completed_at"].replace("Z", "+00:00"))
    pressure_started = datetime.fromisoformat(pressure["session"]["started_at"].replace("Z", "+00:00"))
    assert calm_completed < pressure_started
    policy = case["pairing_policy"]
    assert policy["minimum_answered_per_mode"] == 1
    calm_answered = calm["summary"]["correct"] / calm["summary"]["items_answered"]
    pressure_answered = pressure["summary"]["correct"] / pressure["summary"]["items_answered"]
    calm_presented = calm["summary"]["correct"] / calm["summary"]["items_presented"]
    pressure_presented = pressure["summary"]["correct"] / pressure["summary"]["items_presented"]
    assert case["expected_metrics"]["pressure_delta_answered"] == calm_answered - pressure_answered
    assert case["expected_metrics"]["pressure_delta"] == calm_presented - pressure_presented


def test_negative_pair_fixtures_materialize_with_locked_outcomes():
    cases = load_json(FIXTURE_ROOT / "negative_pair_mutations.json")
    assert len(cases) == 10
    for case in cases:
        calm, pressure, policy, _ = materialize_negative(case)
        assert calm["contract_version"] == pressure["contract_version"] == "ucc.assessment_receipt.v2.0.0"
        assert policy["minimum_presented_per_mode"] >= policy["minimum_answered_per_mode"]
        assert case["expected_issue"].startswith("PAIR_")
        assert case["expected_status"] in {"incomparable", "insufficient_evidence", "void"}


def test_pairing_mutation_probe_obeys_r4_contract():
    probe = load_json(FIXTURE_ROOT / "mutation_probe.json")
    assert probe["killable"]["expected_outcome"] == "KILLED"
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


def evaluate(api, calm, pressure, policy, pair):
    return api.evaluate_pair(
        [calm, pressure],
        form_manifests=pair["form_manifests"],
        pairing_policy=policy,
        registry_snapshot_sha256=pair["registry_snapshot_sha256"],
        pair_result_id="pres_01J0000000000000000000000A",
        evaluated_at="2026-06-30T00:16:00.000Z",
    )


def test_positive_pair_produces_locked_pressure_metrics():
    api = pairing_api()
    calm, pressure, case = materialize_pair()
    result = evaluate(api, calm, pressure, case["pairing_policy"], case)
    assert result["status"] == "valid"
    assert result["metrics"] == case["expected_metrics"]


@pytest.mark.parametrize("case", load_json(FIXTURE_ROOT / "negative_pair_mutations.json"), ids=lambda item: item["case_id"])
def test_negative_pairs_fail_closed_without_metrics(case):
    api = pairing_api()
    calm, pressure, policy, pair = materialize_negative(case)
    result = evaluate(api, calm, pressure, policy, pair)
    assert result["status"] == case["expected_status"]
    assert case["expected_issue"] in [issue["code"] for issue in result["issues"]]
    assert "metrics" not in result


def test_pairing_is_deterministic_and_not_diagnostic():
    api = pairing_api()
    calm, pressure, case = materialize_pair()
    first = evaluate(api, calm, pressure, case["pairing_policy"], case)
    second = evaluate(api, calm, pressure, case["pairing_policy"], case)
    assert first == second
    serialized = json.dumps(first).lower()
    assert "diagnosis" not in serialized
    assert "mastery_established" not in serialized
    assert "cheating" not in serialized


def test_pressure_delta_mutation_probe_uses_r4_outcomes():
    api = pairing_api()
    calm, pressure, case = materialize_pair()
    outcomes = api.run_mutation_probe(calm, pressure, case["pairing_policy"], load_json(FIXTURE_ROOT / "mutation_probe.json"))
    assert outcomes["canonical-delta-uses-answered-denominator"] == "KILLED"
    assert outcomes["skill-iteration-order-only"] in {"SURVIVED", "SKIPPED"}
