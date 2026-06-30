import json
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES = REPO_ROOT / "fixtures" / "red" / "t4_12"


def load_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def branding_api():
    return require_product_module("hermes_thrice_great.packaging.branding", "BRANDING_IMPLEMENTATION_MISSING")


def test_branding_contract_separates_semantic_identity_from_presentation():
    contract = load_json("branding_contract.json")
    assert contract["install_names"] == ["ucc", "hermes-thrice-great", "thoth"]
    assert contract["optional_alias"] == "thoth"
    assert set(contract["semantic_identity_fields"]).isdisjoint(contract["presentation_only_fields"])
    assert contract["stock_identity"]["must_remain_unmodified"] is True
    assert contract["repository_root_install_forbidden"] is True


def test_mutation_probe_obeys_r4_outcome_contract():
    probe = load_json("mutation_probe.json")
    assert all(case["expected_outcome"] == "KILLED" for case in probe["killable"])
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


@pytest.mark.parametrize("relative", ["distribution.yaml", "SOUL.md"])
def test_branding_presentation_sources_exist(relative):
    assert (REPO_ROOT / relative).is_file(), f"BRANDING_SOURCE_MISSING: {relative}"


def test_all_install_names_have_identical_semantic_identity(tmp_path):
    api = branding_api()
    contract = load_json("branding_contract.json")
    identities = [api.install_identity(REPO_ROOT, tmp_path / name, name) for name in contract["install_names"]]
    baseline = {key: identities[0][key] for key in contract["semantic_identity_fields"]}
    assert all({key: identity[key] for key in contract["semantic_identity_fields"]} == baseline for identity in identities)


def test_aliases_differ_only_in_presentation_fields(tmp_path):
    api = branding_api()
    contract = load_json("branding_contract.json")
    records = [api.install_identity(REPO_ROOT, tmp_path / name, name) for name in contract["install_names"]]
    differing = {key for key in records[0] if any(record.get(key) != records[0].get(key) for record in records[1:])}
    assert differing <= set(contract["presentation_only_fields"])


def test_stock_hermes_identity_and_checkout_remain_unmodified(tmp_path):
    api = branding_api()
    result = api.verify_stock_identity_around_install(REPO_ROOT, tmp_path, load_json("branding_contract.json"))
    assert result["before"] == result["after"] == load_json("branding_contract.json")["stock_identity"]
    assert result["checkout_dirty"] is False
    assert result["repository_root_installed"] is False


def test_branding_mutation_probe_uses_r4_outcomes():
    api = branding_api()
    outcomes = api.run_mutation_probe(REPO_ROOT, load_json("branding_contract.json"), load_json("mutation_probe.json"))
    for mutant in load_json("mutation_probe.json")["killable"]:
        assert outcomes[mutant["mutant_id"]] == "KILLED"
    assert outcomes["display-label-only"] in {"SURVIVED", "SKIPPED"}
