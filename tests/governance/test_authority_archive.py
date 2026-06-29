import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AUTHORITY_CHECKER = REPO_ROOT / "scripts" / "validate_authority.py"
ARCHIVE_CHECKER = REPO_ROOT / "scripts" / "check_archive_hygiene.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AuthorityArchiveTests(unittest.TestCase):
    def run_checker(self, checker: Path, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(checker), "--root", str(root)],
            capture_output=True,
            text=True,
            check=False,
        )

    def seed_authority(self, root: Path) -> Path:
        active = root / "docs" / "active"
        active.mkdir(parents=True)
        artifacts = {
            "BUILD_PLAN.md": "# Build Plan\n",
            "PROJECT_TASKS.md": "# Tasks\n",
            "architecture.mmd": "flowchart LR\n",
        }
        for name, content in artifacts.items():
            (active / name).write_text(content, encoding="utf-8")
        authority = {
            "schema_version": "acdf.authority.v1",
            "status": "planning_active",
            "implementation_authorized": False,
            "active_plan_hash": f"sha256:{sha256(active / 'BUILD_PLAN.md')}",
            "binding_artifacts": {
                "build_plan": {
                    "path": "docs/active/BUILD_PLAN.md",
                    "sha256": sha256(active / "BUILD_PLAN.md"),
                },
                "task_board": {
                    "path": "docs/active/PROJECT_TASKS.md",
                    "sha256": sha256(active / "PROJECT_TASKS.md"),
                },
                "architecture": {
                    "path": "docs/active/architecture.mmd",
                    "sha256": sha256(active / "architecture.mmd"),
                },
            },
            "archive_policy": {
                "archive_path": "docs/archive/",
                "archive_is_authority": False,
                "current_state": "initialized",
            },
        }
        path = active / "authority.json"
        path.write_text(json.dumps(authority, indent=2) + "\n", encoding="utf-8")
        return path

    def test_valid_authority_hashes_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_authority(root)
            result = self.run_checker(AUTHORITY_CHECKER, root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_tampered_binding_hash_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_authority(root)
            (root / "docs" / "active" / "BUILD_PLAN.md").write_text(
                "# Tampered\n", encoding="utf-8"
            )
            result = self.run_checker(AUTHORITY_CHECKER, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("HASH_MISMATCH", result.stdout + result.stderr)

    def test_duplicate_active_build_plan_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_authority(root)
            (root / "docs" / "active" / "BUILD_PLAN_COPY.md").write_text(
                "# Competing Plan\n", encoding="utf-8"
            )
            result = self.run_checker(AUTHORITY_CHECKER, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ACTIVE_PLAN_COUNT", result.stdout + result.stderr)

    def test_initialized_ignored_archive_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_authority(root)
            (root / "docs" / "archive").mkdir(parents=True)
            (root / ".agentignore").write_text("docs/archive/**\n", encoding="utf-8")
            result = self.run_checker(ARCHIVE_CHECKER, root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unignored_archive_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_authority(root)
            (root / "docs" / "archive").mkdir(parents=True)
            (root / ".agentignore").write_text("tmp/**\n", encoding="utf-8")
            result = self.run_checker(ARCHIVE_CHECKER, root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ARCHIVE_NOT_IGNORED", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
