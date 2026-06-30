import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "check_staged_private_data.py"


def run_checker(tmp_path, paths):
    paths_file = tmp_path / "paths.txt"
    paths_file.write_text("\n".join(paths), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(CHECKER), "--paths-file", str(paths_file)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_forbidden_private_paths_are_rejected_case_insensitively(tmp_path):
    completed = run_checker(
        tmp_path,
        [
            "outputs/synthetic.json",
            "Learner_Data/SENTINEL.json",
            "profiles/demo/auth.json",
            "local/ledger.sqlite3",
            ".env",
        ],
    )
    assert completed.returncode == 3
    assert "PRIVATE_DATA_STAGE_REJECT" in completed.stderr


def test_public_examples_and_source_files_are_allowed(tmp_path):
    completed = run_checker(
        tmp_path,
        [".env.EXAMPLE", "src/example.py", "fixtures/synthetic/valid.json"],
    )
    assert completed.returncode == 0
    assert completed.stdout.strip() == "PRIVATE_DATA_STAGE_PASS"


def test_pre_commit_hook_invokes_checker():
    hook = (REPO_ROOT / ".githooks" / "pre-commit").read_text(encoding="utf-8")
    assert "scripts/check_staged_private_data.py" in hook
