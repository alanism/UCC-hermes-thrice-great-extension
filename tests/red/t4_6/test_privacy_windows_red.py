import json
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = REPO_ROOT / "fixtures" / "red" / "t4_6"


def load_json(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def privacy_api():
    return require_product_module(
        "hermes_thrice_great.privacy.guards",
        "PRIVACY_GUARDS_IMPLEMENTATION_MISSING",
    )


def test_windows_cases_are_bound_to_r4_host_capabilities():
    fixture = load_json("windows_path_cases.json")
    assert fixture["host_canary"] == {
        "long_path": "PASS_FAIL_CLOSED",
        "drive_case": "PASS_SUPPORTED",
        "reserved_name": "PASS_SUPPORTED",
        "junction_reparse": "PASS_SUPPORTED",
    }
    assert len(fixture["cases"]) == 9
    assert all(case["expected_issue"].startswith("PRIVACY_") for case in fixture["cases"] if not case["expected_allowed"])


def test_redaction_retention_and_commit_fixtures_are_synthetic_and_complete():
    fixture = load_json("redaction_retention_cases.json")
    assert len(fixture["redaction"]) == 4
    assert len(fixture["retention"]) == 4
    assert len(fixture["commit_eligibility"]) == 5
    assert all(case["synthetic"] for case in fixture["commit_eligibility"])
    assert all("SYNTHETIC" in case["input"] or "synthetic" in case["input"] for case in fixture["redaction"])


def test_mutation_probe_obeys_r4_outcome_contract():
    probe = load_json("mutation_probe.json")
    assert all(case["expected_outcome"] == "KILLED" for case in probe["killable"])
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


@pytest.mark.parametrize("case", load_json("windows_path_cases.json")["cases"], ids=lambda value: value["case_id"])
def test_windows_containment_traversal_reserved_and_reparse_cases(tmp_path, case):
    api = privacy_api()
    root = tmp_path / "private-root"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    resolver = None
    if case["case_id"] == "junction-escape":
        resolver = lambda _candidate: outside / "synthetic.json"
    if case["case_id"] == "long-path-host-rejected":
        resolver = lambda _candidate: (_ for _ in ()).throw(OSError(206, "synthetic long path rejection"))
    result = api.validate_contained_path(root, case["relative"], injected_resolver=resolver)
    assert result["allowed"] is case["expected_allowed"]
    if case["expected_issue"]:
        assert case["expected_issue"] in [issue["code"] for issue in result["issues"]]


@pytest.mark.parametrize("case", load_json("redaction_retention_cases.json")["redaction"], ids=lambda value: value["case_id"])
def test_logs_redact_private_values_and_paths(case):
    api = privacy_api()
    output = api.redact_log(case["input"])
    assert case["forbidden"] not in output
    assert case["expected_marker"] in output


@pytest.mark.parametrize("case", load_json("redaction_retention_cases.json")["retention"], ids=lambda value: value["case_id"])
def test_retention_is_deterministic_and_holds_fail_closed(case):
    api = privacy_api()
    assert api.evaluate_retention(case) == case["expected_action"]


@pytest.mark.parametrize("case", load_json("redaction_retention_cases.json")["commit_eligibility"], ids=lambda value: value["path"])
def test_commit_eligibility_rejects_private_roots_even_for_synthetic_files(case):
    api = privacy_api()
    result = api.evaluate_commit_eligibility(case["path"], synthetic=case["synthetic"])
    assert result["allowed"] is case["expected_allowed"]
    if case.get("expected_issue"):
        assert case["expected_issue"] in [issue["code"] for issue in result["issues"]]


def test_privacy_mutation_probe_uses_r4_outcomes():
    api = privacy_api()
    outcomes = api.run_mutation_probe(
        load_json("windows_path_cases.json"),
        load_json("redaction_retention_cases.json"),
        load_json("mutation_probe.json"),
    )
    for mutant in load_json("mutation_probe.json")["killable"]:
        assert outcomes[mutant["mutant_id"]] == "KILLED"
    assert outcomes["case-normalization-order-only"] in {"SURVIVED", "SKIPPED"}
