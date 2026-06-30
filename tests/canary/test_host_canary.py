import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_pytest_executes_on_native_windows():
    assert sys.platform == "win32"


def test_host_canary_reports_all_required_windows_probes(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "run_host_canary.py"), "--root", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report["platform"] == "win32"
    assert set(report["probes"]) == {
        "long_path",
        "drive_case",
        "reserved_name",
        "junction_reparse",
    }
    assert all(item["outcome"].startswith("PASS_") for item in report["probes"].values())
