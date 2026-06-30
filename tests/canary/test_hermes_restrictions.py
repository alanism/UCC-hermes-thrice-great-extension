import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
HERMES_SOURCE = Path(r"C:\Users\alani\AppData\Local\hermes\hermes-agent")
PINNED_HEAD = "2a5dc0ef3df433a36abed9ee544ea067d807c438"


def test_deny_all_baseline_is_mechanically_enforced(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "verify_hermes_restrictions.py"),
            "--hermes-source",
            str(HERMES_SOURCE),
            "--temp-home",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report["hermes_head"] == PINNED_HEAD
    assert report["hermes_clean"] is True
    assert report["unrestricted_tool_count"] > 0
    assert report["restricted_tool_count"] == 0
    assert report["restricted_tool_names"] == []
    assert report["plugin_count"] == 0
    assert report["mcp_server_count"] == 0
    assert report["network_attempts"] == 0


def test_distribution_config_enforces_zero_tool_surface(tmp_path):
    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "verify_hermes_restrictions.py"),
            "--hermes-source", str(HERMES_SOURCE),
            "--temp-home", str(tmp_path),
            "--config-source", str(REPO_ROOT / "config.yaml"),
        ],
        check=False, capture_output=True, text=True,
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report["configured_disabled_toolsets"] == ["*"]
    assert set(report["configured_enabled_toolsets"]).isdisjoint(
        {"terminal", "browser", "web", "discord", "messaging", "send_message", "mcp"}
    )
    assert report["restricted_tool_count"] == 0
    assert report["plugin_count"] == 0
    assert report["mcp_server_count"] == 0
    assert report["network_attempts"] == 0
