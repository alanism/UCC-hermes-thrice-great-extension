import json
import re
from pathlib import Path

import pytest

from tests.red_support import require_product_module


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS = REPO_ROOT / "skills"
FIXTURES = REPO_ROOT / "fixtures" / "red" / "t4_7"


def load_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def packaging_api():
    return require_product_module(
        "hermes_thrice_great.packaging.skills",
        "SKILL_PACKAGING_IMPLEMENTATION_MISSING",
    )


def test_skill_fixture_preserves_source_authority_and_exclusions():
    fixture = load_json("skill_candidates.json")
    assert fixture["native_layout"] == "skills/<slug>/SKILL.md"
    assert fixture["source_authority"] == "legacy_repo_export_non_authoritative"
    assert fixture["sanitized_release_candidate"] is None
    assert set(fixture["explicitly_excluded"]) == {
        "ghostwriting_integrity_gate", "aria_workflow", "parent_workflow", "thoth_ucc_workflows"
    }
    assert "ghostwriting_integrity_gate" not in fixture["candidates"]


def test_mutation_probe_obeys_r4_outcome_contract():
    probe = load_json("mutation_probe.json")
    assert all(case["expected_outcome"] == "KILLED" for case in probe["killable"])
    assert probe["equivalent_control"]["expected_outcome"] in {"SURVIVED", "SKIPPED"}
    assert probe["infrastructure_failures"]["expected_outcome"] == "ERROR"


@pytest.mark.parametrize("slug", load_json("skill_candidates.json")["candidates"])
def test_each_candidate_uses_native_directory_layout_and_required_frontmatter(slug):
    target = SKILLS / slug / "SKILL.md"
    assert target.is_file(), f"SKILL_LAYOUT_NOT_NATIVE: missing {slug}/SKILL.md"
    text = target.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"SKILL_FRONTMATTER_INVALID: {slug}"
    for key in load_json("skill_candidates.json")["required_frontmatter"]:
        assert re.search(rf"(?m)^{re.escape(key)}:\s*\S", text), f"SKILL_FRONTMATTER_INVALID: {slug}:{key}"
    assert re.search(rf"(?m)^name:\s*{re.escape(slug)}\s*$", text), f"SKILL_NAME_MISMATCH: {slug}"


def test_flat_legacy_exports_are_not_installable_native_skills():
    flat = sorted(path.name for path in SKILLS.glob("*.SKILL.md"))
    assert flat == [], f"SKILL_LAYOUT_NOT_NATIVE: flat legacy exports remain: {flat}"


def test_every_declared_reference_resolves_inside_its_native_skill_directory():
    missing = []
    for source in SKILLS.glob("*.SKILL.md"):
        text = source.read_text(encoding="utf-8")
        for reference in re.findall(r"(?m)^\s+-\s+(references/[^\s]+)\s*$", text):
            expected = SKILLS / source.name.removesuffix(".SKILL.md") / reference
            if not expected.is_file():
                missing.append(f"{source.name}:{reference}")
    assert not missing, f"SKILL_REFERENCE_MISSING: {missing}"


def test_native_discovery_finds_only_allowlisted_candidate_skills(tmp_path):
    api = packaging_api()
    staged = api.stage_candidate_skills(SKILLS, tmp_path, load_json("skill_candidates.json"))
    discovered = api.discover_native_skills(staged, platform="windows")
    assert sorted(discovered) == sorted(load_json("skill_candidates.json")["candidates"])
    assert set(discovered).isdisjoint(load_json("skill_candidates.json")["explicitly_excluded"])


def test_skill_mutation_probe_uses_r4_outcomes():
    api = packaging_api()
    outcomes = api.run_mutation_probe(SKILLS, load_json("skill_candidates.json"), load_json("mutation_probe.json"))
    for mutant in load_json("mutation_probe.json")["killable"]:
        assert outcomes[mutant["mutant_id"]] == "KILLED"
    assert outcomes["frontmatter-key-order-only"] in {"SURVIVED", "SKIPPED"}
