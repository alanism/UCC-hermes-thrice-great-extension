import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES = REPO_ROOT / "fixtures" / "red" / "t4_8"
BUILDER = REPO_ROOT / "scripts" / "build_profile_staging.py"
HERMES_SOURCE = Path.home() / "AppData" / "Local" / "hermes" / "hermes-agent"
HERMES_PYTHON = HERMES_SOURCE / "venv" / "Scripts" / "python.exe"
HERMES_EXE = HERMES_SOURCE / "venv" / "Scripts" / "hermes.exe"


def load_json(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def build_staging(staging_root):
    completed = subprocess.run(
        [sys.executable, str(BUILDER), "--source", str(REPO_ROOT), "--output", str(staging_root)],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    inventory_path = staging_root.with_name(f"{staging_root.name}.inventory.json")
    assert inventory_path.is_file()
    return json.loads(inventory_path.read_text(encoding="utf-8"))


def install_isolated(source, hermes_home, profile_name):
    if Path(source).resolve() == REPO_ROOT.resolve():
        raise ValueError("REPOSITORY_ROOT_INSTALL_FORBIDDEN")
    if Path(source).name != "hermes-thrice-great-profile":
        raise ValueError("GENERATED_STAGING_SOURCE_REQUIRED")
    code = (
        "import json,sys; "
        "from hermes_cli.profile_distribution import install_distribution; "
        "p=install_distribution(sys.argv[1],name=sys.argv[2]); "
        "print(json.dumps({'profile_name':p.manifest.name,'target':str(p.target_dir),"
        "'source':p.provenance,'has_skills':p.has_skills}))"
    )
    env = os.environ.copy()
    env.update({"HERMES_HOME": str(hermes_home), "HERMES_SAFE_MODE": "1", "HERMES_ENABLE_PROJECT_PLUGINS": "0"})
    completed = subprocess.run(
        [str(HERMES_PYTHON), "-B", "-c", code, str(source), profile_name],
        cwd=HERMES_SOURCE, env=env, capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout.strip().splitlines()[-1])


def build_and_install_isolated(staging_root, hermes_home, profile_name):
    inventory = build_staging(staging_root)
    installed = install_isolated(staging_root, hermes_home, profile_name)
    target = Path(installed["target"])
    return {
        "installed_from": str(staging_root),
        "repository_root_installed": False,
        "profile_name": installed["profile_name"],
        "target": target,
        "inventory": inventory,
        "plugin": {
            "id": "hermes-thrice-great",
            "delivered": (target / "plugins" / "hermes-thrice-great" / "plugin.yaml").is_file(),
            "loaded": False,
        },
    }


def discover_installed_plugins(profile_root):
    code = (
        "import json; from hermes_cli.plugins import PluginManager; "
        "m=PluginManager(); m.discover_and_load(); print(json.dumps(m.list_plugins()))"
    )
    env = os.environ.copy()
    env.pop("HERMES_SAFE_MODE", None)
    env.update({"HERMES_HOME": str(profile_root), "HERMES_ENABLE_PROJECT_PLUGINS": "0"})
    completed = subprocess.run(
        [str(HERMES_PYTHON), "-B", "-c", code], cwd=HERMES_SOURCE, env=env,
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout.strip().splitlines()[-1])


def update_isolated(hermes_home, profile_name):
    code = (
        "import json,sys; from hermes_cli.profile_distribution import update_distribution; "
        "p=update_distribution(sys.argv[1]); "
        "print(json.dumps({'profile_name':p.manifest.name,'target':str(p.target_dir),'preserves_config':p.preserves_config}))"
    )
    env = os.environ.copy()
    env.update({"HERMES_HOME": str(hermes_home), "HERMES_SAFE_MODE": "1", "HERMES_ENABLE_PROJECT_PLUGINS": "0"})
    completed = subprocess.run(
        [str(HERMES_PYTHON), "-B", "-c", code, profile_name], cwd=HERMES_SOURCE, env=env,
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads(completed.stdout.strip().splitlines()[-1])


def hermes_checkout_identity():
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=HERMES_SOURCE, capture_output=True, text=True, check=True
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], cwd=HERMES_SOURCE, capture_output=True, text=True, check=True
    ).stdout.strip()
    return {"head": head, "dirty": bool(dirty)}


def run_stock_smoke(hermes_home, sentinel_root):
    sentinel_root.mkdir(parents=True, exist_ok=True)
    marker = sentinel_root / "network-attempts.txt"
    sentinel = sentinel_root / "sitecustomize.py"
    sentinel.write_text(
        "import os,socket\n"
        "_original_connect=socket.socket.connect\n"
        "def _blocked(self,address):\n"
        "    with open(os.environ['HTG_NETWORK_MARKER'],'a',encoding='utf-8') as handle: handle.write(repr(address)+'\\n')\n"
        "    raise RuntimeError('offline smoke network blocked')\n"
        "socket.socket.connect=_blocked\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env.update({
        "HERMES_HOME": str(hermes_home), "HERMES_SAFE_MODE": "1",
        "HERMES_ENABLE_PROJECT_PLUGINS": "0", "HTG_NETWORK_MARKER": str(marker),
        "PYTHONPATH": str(sentinel_root),
    })
    commands = [
        ("hermes --version", [str(HERMES_EXE), "--version"]),
        ("hermes profile list", [str(HERMES_EXE), "profile", "list"]),
        ("hermes --help", [str(HERMES_EXE), "--help"]),
    ]
    results = []
    for label, command in commands:
        completed = subprocess.run(command, cwd=HERMES_SOURCE, env=env, capture_output=True, text=True, check=False)
        results.append({"command": label, "exit_code": completed.returncode})
        assert completed.returncode == 0, completed.stderr
    attempts = marker.read_text(encoding="utf-8").splitlines() if marker.exists() else []
    return results, attempts


def stock_smoke_around_isolated_install(tmp_path):
    hermes_home = tmp_path / "home"
    before_identity = hermes_checkout_identity()
    before, before_attempts = run_stock_smoke(hermes_home, tmp_path / "sentinel-before")
    result = build_and_install_isolated(tmp_path / "hermes-thrice-great-profile", hermes_home, "ucc")
    after, after_attempts = run_stock_smoke(hermes_home, tmp_path / "sentinel-after")
    after_identity = hermes_checkout_identity()
    return {
        "before": before, "after": after,
        "network_attempts": len(before_attempts) + len(after_attempts),
        "hermes_head_after": after_identity["head"],
        "checkout_before": before_identity, "checkout_after": after_identity,
        "install": result,
    }


def semantic_payload_hashes(profile_root):
    selected = ["SOUL.md", "config.yaml", "skills", "plugins"]
    result = {}
    for relative in selected:
        path = profile_root / relative
        files = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
        for item in files:
            result[item.relative_to(profile_root).as_posix()] = __import__("hashlib").sha256(item.read_bytes()).hexdigest()
    return result


def distribution_policy_passes(staging, *, checkout_dirty=False, network_attempts=0):
    manifest = (staging / "distribution.yaml").read_text(encoding="utf-8")
    paths = {item.relative_to(staging).as_posix() for item in staging.rglob("*") if item.is_file()}
    forbidden_prefixes = (".git/", ".agent/", "docs/", "local/", "memories/", "sessions/", "logs/", "schemas/", "benchmarks/")
    return (
        "name: hermes-thrice-great" in manifest
        and "plugins/hermes-thrice-great/plugin.yaml" in paths
        and not any(path == ".env" or path.startswith(forbidden_prefixes) for path in paths)
        and not checkout_dirty
        and network_attempts == 0
    )


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


@pytest.mark.parametrize("relative", load_json("install_contract.json")["required_profile_sources"])
def test_required_profile_sources_exist(relative):
    assert (REPO_ROOT / relative).is_file(), f"PROFILE_SOURCE_MISSING: {relative}"


def test_required_plugin_source_and_inert_skeleton_exist():
    manifest = REPO_ROOT / load_json("install_contract.json")["required_plugin_source"]
    module = manifest.with_name("__init__.py")
    assert manifest.is_file() and module.is_file()
    text = module.read_text(encoding="utf-8")
    assert "def register(ctx):" in text
    assert all(token not in text for token in ("register_command", "register_tool", "register_hook", "register_middleware"))


def test_repository_root_install_is_rejected_before_hermes():
    with pytest.raises(ValueError, match="REPOSITORY_ROOT_INSTALL_FORBIDDEN"):
        install_isolated(REPO_ROOT, REPO_ROOT / "tmp" / "forbidden-home", "forbidden")


def test_generated_payload_is_exactly_allowlisted_and_contains_eight_public_skills(tmp_path):
    staging = tmp_path / "hermes-thrice-great-profile"
    inventory = build_staging(staging)
    paths = {item["path"] for item in inventory["files"]}
    assert set(load_json("install_contract.json")["required_profile_sources"]) <= paths
    assert len([path for path in paths if path.endswith("/SKILL.md")]) == 8
    forbidden = (".git/", ".agent/", "docs/", "local/", "memories/", "sessions/", "logs/", ".env")
    assert not any(path == ".env" or path.startswith(forbidden[:-1]) for path in paths)


@pytest.mark.parametrize("profile_name", load_json("install_contract.json")["profile_names"])
def test_generated_staging_tree_installs_in_isolated_home_under_arbitrary_name(tmp_path, profile_name):
    staging = tmp_path / "hermes-thrice-great-profile"
    result = build_and_install_isolated(staging, tmp_path / "hermes-home", profile_name)
    assert result["installed_from"] == str(staging)
    assert result["repository_root_installed"] is False
    assert result["profile_name"] == profile_name
    assert result["target"].resolve().is_relative_to((tmp_path / "hermes-home").resolve())


def test_installed_payload_delivers_opt_in_plugin_without_loading_it(tmp_path):
    result = build_and_install_isolated(tmp_path / "hermes-thrice-great-profile", tmp_path / "home", "ucc")
    assert result["plugin"]["id"] == "hermes-thrice-great"
    assert result["plugin"]["delivered"] is True
    plugins = discover_installed_plugins(result["target"])
    plugin = next(item for item in plugins if item["name"] == "hermes-thrice-great")
    assert plugin["kind"] == "standalone"
    assert plugin["enabled"] is False
    assert plugin["tools"] == plugin["hooks"] == plugin["middleware"] == plugin["commands"] == 0
    assert "not enabled in config" in plugin["error"]


def test_ucc_and_optional_thoth_are_config_isolated_but_semantically_equivalent(tmp_path):
    staging = tmp_path / "hermes-thrice-great-profile"
    build_staging(staging)
    hermes_home = tmp_path / "home"
    ucc = install_isolated(staging, hermes_home, "ucc")
    thoth = install_isolated(staging, hermes_home, "thoth")
    ucc_root, thoth_root = Path(ucc["target"]), Path(thoth["target"])
    assert ucc_root != thoth_root
    assert semantic_payload_hashes(ucc_root) == semantic_payload_hashes(thoth_root)
    ucc_config = ucc_root / "config.yaml"
    original_thoth_config = (thoth_root / "config.yaml").read_bytes()
    ucc_config.write_text(ucc_config.read_text(encoding="utf-8") + "\n# synthetic ucc-only override\n", encoding="utf-8")
    assert (thoth_root / "config.yaml").read_bytes() == original_thoth_config


def test_update_restores_distribution_files_and_preserves_config_and_user_state(tmp_path):
    staging = tmp_path / "hermes-thrice-great-profile"
    build_staging(staging)
    hermes_home = tmp_path / "home"
    installed = install_isolated(staging, hermes_home, "ucc")
    target = Path(installed["target"])
    custom_config = (target / "config.yaml").read_text(encoding="utf-8") + "\n# synthetic user override\n"
    (target / "config.yaml").write_text(custom_config, encoding="utf-8")
    memory = target / "memories" / "synthetic-preserve.txt"
    memory.write_text("synthetic user-owned sentinel\n", encoding="utf-8")
    (target / "SOUL.md").write_text("tampered distribution file\n", encoding="utf-8")
    (target / "plugins" / "hermes-thrice-great" / "plugin.yaml").write_text("tampered\n", encoding="utf-8")
    result = update_isolated(hermes_home, "ucc")
    assert result["preserves_config"] is True
    assert (target / "config.yaml").read_text(encoding="utf-8") == custom_config
    assert memory.read_text(encoding="utf-8") == "synthetic user-owned sentinel\n"
    assert (target / "SOUL.md").read_bytes() == (staging / "SOUL.md").read_bytes()
    assert (target / "plugins" / "hermes-thrice-great" / "plugin.yaml").read_bytes() == (staging / "plugins" / "hermes-thrice-great" / "plugin.yaml").read_bytes()


def test_stock_offline_smoke_is_unchanged_before_and_after_install(tmp_path):
    result = stock_smoke_around_isolated_install(tmp_path)
    assert result["before"] == result["after"]
    assert all(item["exit_code"] == 0 for item in result["after"])
    assert result["network_attempts"] == 0
    assert result["hermes_head_after"] == "2a5dc0ef3df433a36abed9ee544ea067d807c438"
    assert result["checkout_before"] == result["checkout_after"] == {
        "head": "2a5dc0ef3df433a36abed9ee544ea067d807c438", "dirty": False
    }


def test_distribution_mutation_probe_uses_r4_outcomes(tmp_path):
    baseline = tmp_path / "baseline" / "hermes-thrice-great-profile"
    build_staging(baseline)
    assert distribution_policy_passes(baseline)
    outcomes = {}
    try:
        install_isolated(REPO_ROOT, tmp_path / "forbidden", "forbidden")
    except ValueError:
        outcomes["install-repository-root"] = "KILLED"

    no_plugin = tmp_path / "no-plugin"
    shutil.copytree(baseline, no_plugin)
    shutil.rmtree(no_plugin / "plugins")
    outcomes["omit-plugin-payload"] = "SURVIVED" if distribution_policy_passes(no_plugin) else "KILLED"

    hardcoded = tmp_path / "hardcoded-thoth"
    shutil.copytree(baseline, hardcoded)
    manifest = hardcoded / "distribution.yaml"
    manifest.write_text(manifest.read_text(encoding="utf-8").replace("name: hermes-thrice-great", "name: thoth", 1), encoding="utf-8")
    outcomes["hardcode-thoth-name"] = "SURVIVED" if distribution_policy_passes(hardcoded) else "KILLED"
    outcomes["dirty-stock-hermes"] = "SURVIVED" if distribution_policy_passes(baseline, checkout_dirty=True) else "KILLED"
    outcomes["allow-network-smoke"] = "SURVIVED" if distribution_policy_passes(baseline, network_attempts=1) else "KILLED"
    outcomes["inventory-key-order-only"] = "SURVIVED" if distribution_policy_passes(baseline) else "KILLED"
    for mutant in load_json("mutation_probe.json")["killable"]:
        assert outcomes[mutant["mutant_id"]] == "KILLED"
    assert outcomes["inventory-key-order-only"] in {"SURVIVED", "SKIPPED"}
