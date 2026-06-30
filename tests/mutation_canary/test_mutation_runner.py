import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_meta_canaries_classify_behavior_and_infrastructure_distinctly():
    completed = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "run_mutation_checks.py"), "--self-test"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report["killable"]["outcome"] == "KILLED"
    assert report["equivalent"]["outcome"] == "SURVIVED"
    assert report["crash"]["outcome"] == "ERROR"
    assert report["setup_error"]["outcome"] == "ERROR"
    assert report["timeout"]["outcome"] == "ERROR"
