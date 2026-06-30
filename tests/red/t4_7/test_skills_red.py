import json
import re
import shutil
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS = REPO_ROOT / "skills"
FIXTURES = REPO_ROOT / "fixtures" / "red" / "t4_7"


def load_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


HERMES_SOURCE = Path.home() / "AppData" / "Local" / "hermes" / "hermes-agent"
HERMES_SITE_PACKAGES = HERMES_SOURCE / "venv" / "Lib" / "site-packages"


def hermes_skill_api(monkeypatch):
    monkeypatch.syspath_prepend(str(HERMES_SITE_PACKAGES))
    monkeypatch.syspath_prepend(str(HERMES_SOURCE))
    from agent.skill_utils import iter_skill_index_files, parse_frontmatter, skill_matches_platform

    return iter_skill_index_files, parse_frontmatter, skill_matches_platform


def copy_skills(target):
    shutil.copytree(SKILLS, target)
    return target


def native_inventory(skills_root, api):
    iter_files, parse_frontmatter, skill_matches_platform = api
    inventory = []
    missing_refs = []
    for skill_md in iter_files(skills_root, "SKILL.md"):
        frontmatter, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        references = frontmatter.get("linked", {}).get("references", [])
        for reference in references:
            target = skill_md.parent / reference
            if not target.is_file():
                missing_refs.append(f"{frontmatter.get('name')}:{reference}")
            else:
                assert target.read_text(encoding="utf-8").strip()
        inventory.append({
            "directory": skill_md.parent.name,
            "name": frontmatter.get("name"),
            "description": frontmatter.get("description"),
            "platform_match": skill_matches_platform(frontmatter),
            "body_loaded": bool(body.strip()),
        })
    return inventory, missing_refs


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
    for source in SKILLS.glob("*/SKILL.md"):
        text = source.read_text(encoding="utf-8")
        for reference in re.findall(r"(?m)^\s+-\s+(references/[^\s]+)\s*$", text):
            expected = source.parent / reference
            if not expected.is_file():
                missing.append(f"{source.parent.name}:{reference}")
    assert not missing, f"SKILL_REFERENCE_MISSING: {missing}"


def test_native_discovery_finds_and_loads_only_allowlisted_candidate_skills(tmp_path, monkeypatch):
    api = hermes_skill_api(monkeypatch)
    staged = copy_skills(tmp_path / "isolated-profile" / "skills")
    inventory, missing_refs = native_inventory(staged, api)
    discovered = [item["name"] for item in inventory]
    assert sorted(discovered) == sorted(load_json("skill_candidates.json")["candidates"])
    assert all(item["directory"] == item["name"] for item in inventory)
    assert all(item["description"] and item["platform_match"] and item["body_loaded"] for item in inventory)
    assert missing_refs == []
    assert set(discovered).isdisjoint(load_json("skill_candidates.json")["explicitly_excluded"])


def test_skill_mutation_probe_kills_layout_reference_name_and_exclusion_faults(tmp_path, monkeypatch):
    api = hermes_skill_api(monkeypatch)
    expected = set(load_json("skill_candidates.json")["candidates"])

    def passes(root):
        inventory, missing_refs = native_inventory(root, api)
        names = {item["name"] for item in inventory}
        return (
            names == expected
            and not missing_refs
            and all(item["directory"] == item["name"] for item in inventory)
            and names.isdisjoint(load_json("skill_candidates.json")["explicitly_excluded"])
        )

    baseline = copy_skills(tmp_path / "baseline")
    assert passes(baseline)

    flat = copy_skills(tmp_path / "flat")
    source = flat / "assessment_app_reviewer" / "SKILL.md"
    source.replace(flat / "assessment_app_reviewer.SKILL.md")
    assert not passes(flat)

    missing_reference = copy_skills(tmp_path / "missing-reference")
    (missing_reference / "assessment_app_reviewer" / "references" / "app-update-verification-example.md").unlink()
    assert not passes(missing_reference)

    wrong_name = copy_skills(tmp_path / "wrong-name")
    target = wrong_name / "ucc_ontology_mapper" / "SKILL.md"
    target.write_text(target.read_text(encoding="utf-8").replace("name: ucc_ontology_mapper", "name: wrong_name", 1), encoding="utf-8")
    assert not passes(wrong_name)

    excluded = copy_skills(tmp_path / "excluded")
    excluded_skill = excluded / "ghostwriting_integrity_gate"
    excluded_skill.mkdir()
    (excluded_skill / "SKILL.md").write_text("---\nname: ghostwriting_integrity_gate\ndescription: synthetic excluded sentinel\nplatforms: [windows]\n---\nSentinel.\n", encoding="utf-8")
    assert not passes(excluded)

    equivalent = copy_skills(tmp_path / "equivalent")
    assert passes(equivalent)
