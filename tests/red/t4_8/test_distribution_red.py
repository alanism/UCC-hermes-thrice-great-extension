import json
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES = REPO_ROOT / "fixtures" / "red" / "t4_8"


def load_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def profile_api():
    return require_product_module("hermes_thrice_great.packaging.profile", "PROFILE_DISTRIBUTION_IMPLEMENTATION_MISSING")


def test_install_contract_locks_pin_isolation_names_and_offline_smoke():
    contract = load_json("install_contract.json")
    assert contract["hermes_pin"] == {"package":"hermes-agent==0.16.0","head":"2a5dc0ef3df433a36abed9ee544ea067d807c438"}
    assert contract["source_root_never_installable"] is True
    assert contract["staging_tree"] == "dist/hermes-thrice-great-profile"
    assert contract["profile_names"] == ["ucc", "thoth", "synthetic-arbitrary-name"]
    assert contract["offline"] is contract["isolated_home_required"] is True


def test_mutation_probe_obeys_r4_outcome_contract():
    probe = load_json("mutation_probe.json")
    assert all(case["expected_outcome"] == "KILLED" for case in probe["killable"])
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


@pytest.mark.parametrize("relative", load_json("install_contract.json")["required_source_files"])
def test_required_distribution_and_plugin_sources_exist(relative):
    assert (REPO_ROOT / relative).is_file(), f"PROFILE_SOURCE_MISSING: {relative}"


@pytest.mark.parametrize("profile_name", load_json("install_contract.json")["profile_names"])
def test_generated_staging_tree_installs_in_isolated_home_under_arbitrary_name(tmp_path, profile_name):
    api = profile_api()
    result = api.build_and_install_isolated(
        source_root=REPO_ROOT,
        staging_root=tmp_path / "staging",
        hermes_home=tmp_path / "hermes-home",
        profile_name=profile_name,
        offline=True,
    )
    assert result["installed_from"] == str(tmp_path / "staging")
    assert result["repository_root_installed"] is False
    assert result["profile_name"] == profile_name


def test_installed_payload_delivers_opt_in_plugin_without_loading_it(tmp_path):
    api = profile_api()
    result = api.build_and_install_isolated(REPO_ROOT, tmp_path / "staging", tmp_path / "home", "ucc", offline=True)
    assert result["plugin"]["id"] == "hermes-thrice-great"
    assert result["plugin"]["delivered"] is True
    assert result["plugin"]["loaded"] is False


def test_stock_offline_smoke_is_unchanged_before_and_after_install(tmp_path):
    api = profile_api()
    result = api.stock_smoke_around_isolated_install(REPO_ROOT, tmp_path, load_json("install_contract.json"))
    assert result["before"] == result["after"]
    assert all(item["exit_code"] == 0 for item in result["after"])
    assert result["network_attempts"] == 0
    assert result["hermes_head_after"] == "2a5dc0ef3df433a36abed9ee544ea067d807c438"


def test_distribution_mutation_probe_uses_r4_outcomes():
    api = profile_api()
    outcomes = api.run_mutation_probe(REPO_ROOT, load_json("install_contract.json"), load_json("mutation_probe.json"))
    for mutant in load_json("mutation_probe.json")["killable"]:
        assert outcomes[mutant["mutant_id"]] == "KILLED"
    assert outcomes["inventory-key-order-only"] in {"SURVIVED", "SKIPPED"}
