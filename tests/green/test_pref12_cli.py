import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SOURCE = REPO_ROOT / "plugins" / "hermes-thrice-great"
RESOURCE_SOURCE = PLUGIN_SOURCE / "hermes_thrice_great" / "resources" / "synthetic"
HERMES_SOURCE = Path.home() / "AppData" / "Local" / "hermes" / "hermes-agent"
HERMES_PYTHON = HERMES_SOURCE / "venv" / "Scripts" / "python.exe"
HERMES_EXE = HERMES_SOURCE / "venv" / "Scripts" / "hermes.exe"
EXPECTED_CASES = {
    "missing_approval": "APPROVAL_REQUIRED",
    "replay_conflict": "IDEMPOTENCY_CONFLICT",
    "invalid_totals": "RECEIPT_TOTAL_INCONSISTENT",
    "write_fault": "LEDGER_TEMP_WRITE_FAILED",
    "network_request": "OFFLINE_NETWORK_FORBIDDEN",
}


def test_command_engine_runs_installed_resources_and_real_orchestrator():
    sys.path.insert(0, str(PLUGIN_SOURCE))
    from hermes_thrice_great.plugin.commands import run_cli

    code, valid = run_cli(["validate", "--synthetic"], resource_root=RESOURCE_SOURCE)
    assert code == 0
    assert valid["status"] == "ok"
    assert valid["synthetic_set_id"] == "ucc-synthetic-week-v1"
    assert valid["canonical_hash"]
    for case_id, issue_code in EXPECTED_CASES.items():
        code, invalid = run_cli(
            ["validate", "--synthetic", "--case", case_id],
            resource_root=RESOURCE_SOURCE,
        )
        assert code != 0
        assert invalid["issue_codes"] == [issue_code]
        assert invalid["ledger_commits"] == 0
    code, explicit_valid = run_cli(
        ["validate", "--fixture", "valid/week.json"], resource_root=RESOURCE_SOURCE
    )
    assert code == 0 and explicit_valid["status"] == "ok"
    code, explicit_invalid = run_cli(
        ["validate", "--fixture", "adversarial/week-cases.json"], resource_root=RESOURCE_SOURCE
    )
    assert code != 0 and explicit_invalid["issue_codes"] == ["APPROVAL_REQUIRED"]
    code, dry_run = run_cli(["dry-run", "--synthetic"], resource_root=RESOURCE_SOURCE)
    assert code == 0
    assert dry_run["stage_results"] == [
        "smc_loaded", "receipts_validated", "pair_evaluated", "review_generated",
        "approval_wait", "approval_applied", "ledger_committed",
    ]
    assert dry_run["ledger_commits"] == 1
    assert dry_run["ledger_hash"]
    code, dry_invalid = run_cli(
        ["dry-run", "--synthetic", "--case", "missing_approval"],
        resource_root=RESOURCE_SOURCE,
    )
    assert code != 0
    assert dry_invalid["issue_codes"] == ["APPROVAL_REQUIRED"]
    assert dry_invalid["ledger_commits"] == 0


def test_installed_profile_loads_bundled_resources_with_zero_socket_attempts(tmp_path):
    staging = tmp_path / "hermes-thrice-great-profile"
    built = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build_profile_staging.py"), "--source", str(REPO_ROOT), "--output", str(staging)],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    assert built.returncode == 0, built.stderr
    assert (staging / "plugins" / "hermes-thrice-great" / "hermes_thrice_great" / "resources" / "synthetic" / "manifest.json").is_file()
    home = tmp_path / "home"
    env = os.environ.copy()
    env.update({"HERMES_HOME": str(home), "HERMES_SAFE_MODE": "1", "HERMES_ENABLE_PROJECT_PLUGINS": "0"})
    install_code = (
        "import json,sys; from hermes_cli.profile_distribution import install_distribution; "
        "p=install_distribution(sys.argv[1],name='ucc'); print(json.dumps({'target':str(p.target_dir)}))"
    )
    installed = subprocess.run(
        [str(HERMES_PYTHON), "-B", "-c", install_code, str(staging)],
        cwd=HERMES_SOURCE, env=env, capture_output=True, text=True, check=False,
    )
    assert installed.returncode == 0, installed.stderr
    profile = Path(json.loads(installed.stdout.strip().splitlines()[-1])["target"])
    (profile / "config.yaml").write_text(
        'agent:\n  disabled_toolsets: ["*"]\nplatform_toolsets:\n  cli: []\nplugins:\n  enabled: [hermes-thrice-great]\n  disabled: []\nmcp_servers: {}\n',
        encoding="utf-8",
    )
    sentinel = tmp_path / "sentinel"
    sentinel.mkdir()
    marker = sentinel / "network.txt"
    (sentinel / "sitecustomize.py").write_text(
        "import os,socket\n"
        "def blocked(self,address):\n"
        " open(os.environ['HTG_NETWORK_MARKER'],'a').write('attempt\\n'); raise RuntimeError('network blocked')\n"
        "socket.socket.connect=blocked\n",
        encoding="utf-8",
    )
    run_env = os.environ.copy()
    run_env.update({
        "HERMES_HOME": str(profile), "HERMES_ENABLE_PROJECT_PLUGINS": "0",
        "PYTHONPATH": str(sentinel), "PYTHONDONTWRITEBYTECODE": "1",
        "HTG_NETWORK_MARKER": str(marker),
    })

    def invoke(*args):
        result = subprocess.run(
            [str(HERMES_EXE), "ucc", *args], cwd=HERMES_SOURCE, env=run_env,
            capture_output=True, text=True, check=False, timeout=20,
        )
        payload = json.loads(result.stdout.strip().splitlines()[-1])
        return result.returncode, payload

    assert invoke("doctor")[0] == 0
    assert invoke("validate", "--synthetic")[0] == 0
    assert invoke("validate", "--fixture", "valid/week.json")[0] == 0
    explicit_code, explicit = invoke(
        "validate", "--fixture", "adversarial/week-cases.json"
    )
    assert explicit_code != 0 and explicit["issue_codes"] == ["APPROVAL_REQUIRED"]
    invalid_code, invalid = invoke("validate", "--synthetic", "--case", "invalid_totals")
    assert invalid_code != 0 and invalid["issue_codes"] == ["RECEIPT_TOTAL_INCONSISTENT"]
    dry_code, dry = invoke("dry-run", "--synthetic")
    assert dry_code == 0 and dry["ledger_commits"] == 1 and len(dry["stage_results"]) == 7
    rejected_code, rejected = invoke("dry-run", "--synthetic", "--case", "missing_approval")
    assert rejected_code != 0 and rejected["ledger_commits"] == 0
    assert not marker.exists()
    assert all(
        payload["network_attempts"] == payload["model_calls"] == 0
        for payload in (explicit, invalid, dry, rejected)
    )
