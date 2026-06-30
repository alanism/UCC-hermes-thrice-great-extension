import copy
import hashlib
import json
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = REPO_ROOT / "fixtures" / "red" / "t4_1"
FAMILIES = {
    "smc",
    "assessment_receipt",
    "receipt_pairing",
    "proposal_approval",
    "parent_brief_ledger",
}
VERSION_FIELDS = {
    "version",
    "lifecycle_state",
    "schema_ref",
    "contract_ref",
    "canonical_hash",
    "semantic_validator_ref",
    "semantic_projection_ref",
    "introduced_at",
    "replaces",
    "compatible_with",
    "migration",
    "fixture_sets",
    "approval_ref",
}


def load_json(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def jcs_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def materialize_artifacts(root):
    artifact_map = load_json("artifact_map.json")
    for relative, content in artifact_map.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode("utf-8"))


def pointer_parent(document, pointer):
    tokens = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
    parent = document
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
    final = int(tokens[-1]) if isinstance(parent, list) else tokens[-1]
    return parent, final


def apply_operations(document, operations):
    result = copy.deepcopy(document)
    for operation in operations:
        parent, key = pointer_parent(result, operation["path"])
        if operation["op"] == "remove":
            parent.pop(key)
        elif operation["op"] == "replace":
            parent[key] = operation["value"]
        else:
            raise AssertionError(f"unsupported fixture operation: {operation['op']}")
    return result


def registry_api():
    return require_product_module(
        "hermes_thrice_great.contracts.registry",
        "REGISTRY_IMPLEMENTATION_MISSING",
    )


def assert_fixture_set_hashes(version, artifact_map):
    for fixture_set in version["fixture_sets"]:
        prefix = fixture_set["path"] + "/"
        entries = []
        for path, content in artifact_map.items():
            if path.startswith(prefix):
                entries.append({
                    "path": path[len(prefix):],
                    "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                })
        assert entries
        assert fixture_set["expected_hash"] == jcs_hash(sorted(entries, key=lambda item: item["path"]))


def test_positive_fixture_is_internally_valid_and_hash_complete(tmp_path):
    registry = load_json("positive_registry.json")
    artifact_map = load_json("artifact_map.json")
    materialize_artifacts(tmp_path)
    assert set(registry) == {"ucc_contract_registry"}
    envelope = registry["ucc_contract_registry"]
    assert envelope["registry_schema_version"] == "ucc.contract_registry.v1.0.0"
    assert set(envelope["families"]) == FAMILIES
    for family_key, family in envelope["families"].items():
        assert family["family_id"] == family_key
        assert family["versions"]
        for version in family["versions"]:
            assert set(version) == VERSION_FIELDS
            contract_ref = version["contract_ref"]
            content = artifact_map[contract_ref["path"]].replace("\r\n", "\n").replace("\r", "\n")
            assert contract_ref["artifact_sha256"] == hashlib.sha256(content.encode()).hexdigest()
    smc = envelope["families"]["smc"]["versions"][0]
    schema = artifact_map[smc["schema_ref"]["path"]].encode()
    assert smc["schema_ref"]["artifact_sha256"] == hashlib.sha256(schema).hexdigest()
    projection = {
        "version": smc["version"],
        "schema_id": smc["schema_ref"]["schema_id"],
        "schema_artifact_sha256": smc["schema_ref"]["artifact_sha256"],
        "contract_artifact_sha256": smc["contract_ref"]["artifact_sha256"],
        "canonical_excerpt_sha256": None,
        "semantic_validator_sha256": None,
        "semantic_projection_sha256": None,
        "canonicalization_id": envelope["canonicalization_id"],
    }
    assert smc["canonical_hash"] == jcs_hash(projection)
    assert_fixture_set_hashes(smc, artifact_map)


def test_negative_mutations_materialize_complete_documents():
    positive = load_json("positive_registry.json")
    cases = load_json("negative_mutations.json")
    assert len(cases) == 10
    for case in cases:
        document = apply_operations(positive, case["operations"])
        assert "ucc_contract_registry" in document
        assert case["expected_issue"].startswith(("REGISTRY_", "MIGRATION_"))


def test_positive_registry_requires_absent_registry_validator(tmp_path):
    api = registry_api()
    materialize_artifacts(tmp_path)
    document = load_json("positive_registry.json")
    snapshot = jcs_hash(document)
    assert api.validate_registry(document, tmp_path, snapshot) == []


@pytest.mark.parametrize("case", load_json("negative_mutations.json"), ids=lambda item: item["case_id"])
def test_negative_registry_cases_return_stable_primary_issue(tmp_path, case):
    api = registry_api()
    materialize_artifacts(tmp_path)
    document = apply_operations(load_json("positive_registry.json"), case["operations"])
    issues = api.validate_registry(document, tmp_path, jcs_hash(document))
    assert issues[0]["code"] == case["expected_issue"]


def test_unknown_fields_rejected_but_namespaced_extensions_allowed(tmp_path):
    api = registry_api()
    materialize_artifacts(tmp_path)
    positive = load_json("positive_registry.json")
    with_extension = copy.deepcopy(positive)
    with_extension["ucc_contract_registry"]["extensions"] = {"org.example.note": {"synthetic": True}}
    assert api.validate_registry(with_extension, tmp_path, jcs_hash(with_extension)) == []
    unknown = copy.deepcopy(positive)
    unknown["ucc_contract_registry"]["unregistered_field"] = True
    issues = api.validate_registry(unknown, tmp_path, jcs_hash(unknown))
    assert issues[0]["code"] == "REGISTRY_UNKNOWN_FIELD"


def test_registry_and_version_canonical_hash_recomputation():
    api = registry_api()
    document = load_json("positive_registry.json")
    envelope = document["ucc_contract_registry"]
    smc = envelope["families"]["smc"]["versions"][0]
    assert api.compute_registry_snapshot_hash(document) == jcs_hash(document)
    assert api.compute_version_canonical_hash(smc, envelope["canonicalization_id"]) == smc["canonical_hash"]


@pytest.mark.parametrize("case", load_json("resolution_cases.json"), ids=lambda item: item["case_id"])
def test_exact_version_lifecycle_and_migration_resolution(tmp_path, case):
    api = registry_api()
    materialize_artifacts(tmp_path)
    document = load_json("positive_registry.json")
    snapshot = jcs_hash(document)
    if "source_version" in case:
        result = api.plan_migration(document, case["source_version"], case["target_version"])
    else:
        result = api.resolve_version(
            document,
            snapshot,
            case["family_id"],
            case["version"],
            purpose=case["purpose"],
            allow_locked=case["allow_locked"],
            artifact_root=tmp_path,
        )
    if "expected_issue" in case:
        assert result["issues"][0]["code"] == case["expected_issue"]
    else:
        assert result["record"]["version"] == case["expected_version"]
