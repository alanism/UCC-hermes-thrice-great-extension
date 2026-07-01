import json
import hashlib
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = REPO_ROOT / "fixtures" / "synthetic"
DIRECT_IDENTITY_FIELDS = {"email", "family_name", "learner_name", "real_name", "school_id", "discord_id"}
sys.path.insert(0, str(REPO_ROOT / "plugins" / "hermes-thrice-great"))


def load(relative):
    return json.loads((FIXTURE_ROOT / relative).read_text(encoding="utf-8"))


def walk(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def scalar_values(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from scalar_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from scalar_values(item)
    else:
        yield value


def test_valid_week_manifest_is_complete_offline_and_synthetic():
    week = load("valid/week.json")
    assert week["fixture_schema_version"] == "ucc.synthetic_week_fixture.v1.0.0"
    assert week["synthetic"] is week["offline"] is True
    assert week["week_id"].startswith("synthetic-")
    assert set(week["inputs"]) == {
        "smc", "calm_receipt", "pressure_receipt", "pairing", "proposal",
        "approval", "ledger", "workflow"
    }
    for relative in week["inputs"].values():
        path = REPO_ROOT / relative
        assert path.is_file()
        assert path.resolve().is_relative_to(REPO_ROOT.resolve())
    learner_ids = {
        load("valid/smc.json")["learner_id"],
        load("valid/calm-receipt.json")["learner_id"],
        load("valid/pressure-receipt.json")["learner_id"],
        load("valid/proposal.json")["ucc_parent_proposal"]["learner_id"],
        load("valid/approval.json")["ucc_parent_approval_event"]["scope"]["learner_id"],
        load("valid/workflow.json")["learner_id"],
    }
    assert len(learner_ids) == 1


def test_smc_is_active_pseudonymous_and_contains_no_direct_identity():
    smc = load("valid/smc.json")
    assert smc["contract_version"] == "ucc.smc.v1.0.0"
    assert smc["lifecycle_status"] == "active"
    assert smc["learner_id"].startswith("lrn_")
    assert smc["display_name"] is None
    for mapping in walk(smc):
        assert not (DIRECT_IDENTITY_FIELDS & set(mapping))


def test_adversarial_set_is_closed_synthetic_and_noncommitting():
    fixture = load("adversarial/week-cases.json")
    assert fixture["synthetic"] is True
    assert fixture["base_week"] == "fixtures/synthetic/valid/week.json"
    assert len(fixture["cases"]) == 5
    assert all(case["ledger_commits"] == 0 for case in fixture["cases"])
    assert {case["mutation"] for case in fixture["cases"]} == {
        "remove_approval", "change_approval_payload", "invalidate_receipt_total",
        "inject_temp_write_fault", "attempt_network",
    }
    assert all(case["expected_issue"].startswith(("APPROVAL_", "IDEMPOTENCY_", "RECEIPT_", "LEDGER_", "OFFLINE_")) for case in fixture["cases"])


def test_every_materialized_json_is_parseable_and_contains_no_outbound_identity_shape():
    files = sorted(FIXTURE_ROOT.rglob("*.json"))
    assert len(files) == 10
    for path in files:
        document = json.loads(path.read_text(encoding="utf-8"))
        for mapping in walk(document):
            assert not (DIRECT_IDENTITY_FIELDS & set(mapping))
            if "display_name" in mapping:
                assert mapping["display_name"] is None
        for value in scalar_values(document):
            if isinstance(value, str):
                assert re.search(r"[^\s@]+@[^\s@]+\.[^\s@]+", value) is None
                assert re.match(r"^[A-Za-z]:\\", value) is None
                assert not value.startswith("\\\\")


def test_materialized_contract_inputs_pass_the_deterministic_validators():
    from hermes_thrice_great.contracts import approval, ledger, pairing, receipts

    calm = load("valid/calm-receipt.json")
    pressure = load("valid/pressure-receipt.json")
    pair_config = load("valid/pairing.json")
    form_registry = {
        key: {"level_order": [value["level_band"]]}
        for key, value in pair_config["form_manifests"].items()
    }
    for receipt in (calm, pressure):
        result = receipts.validate_receipt(
            receipt,
            form_registry=form_registry,
            validated_at="2026-06-30T04:00:00.000Z",
        )
        assert result["quality"]["status"] == "clean"
    pair_result = pairing.evaluate_pair(
        [calm, pressure],
        form_manifests=pair_config["form_manifests"],
        pairing_policy=pair_config["pairing_policy"],
        registry_snapshot_sha256=pair_config["registry_snapshot_sha256"],
        pair_result_id="pres_01J00000000000000000000061",
        evaluated_at="2026-06-30T04:00:00.000Z",
    )
    assert pair_result["status"] == "valid"
    assert pair_result["metrics"] == pair_config["expected_metrics"]
    smc = load("valid/smc.json")
    smc_hash = hashlib.sha256(
        json.dumps(smc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    proposal = load("valid/proposal.json")
    approval_event = load("valid/approval.json")
    assert approval.validate_proposal(
        proposal,
        smc_registry={smc["smc_id"]: {"canonical_hash": smc_hash, "active": True}},
    ) == []
    authority = {
        "ledger_namespace": "synthetic-test",
        "actors": {"parent": ["act_01J0000000000000000000001A"]},
    }
    assert approval.validate_approval_event(
        approval_event, proposal=proposal, authority_config=authority
    ) == []
    assert ledger.validate_ledger(load("valid/ledger.json")) == []
