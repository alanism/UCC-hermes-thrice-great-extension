import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "check_claim_state.py"
PLAN_HASH = "sha256:" + "a" * 64


class ClaimStateTests(unittest.TestCase):
    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(root)],
            capture_output=True,
            text=True,
            check=False,
        )

    def seed_root(self, root: Path) -> None:
        active = root / "docs" / "active"
        claims = root / ".agent" / "claims"
        receipts = active / "receipts"
        active.mkdir(parents=True)
        claims.mkdir(parents=True)
        receipts.mkdir(parents=True)
        (active / "authority.json").write_text(
            json.dumps({"active_plan_hash": PLAN_HASH}) + "\n", encoding="utf-8"
        )
        (active / "PROJECT_TASKS.md").write_text(
            "| ID | Task |\n|---|---|\n| X1 | Synthetic task |\n", encoding="utf-8"
        )
        schema = {
            "required": [
                "task_id",
                "agent_id",
                "claimed_at",
                "active_plan_hash",
                "allowed_files",
                "forbidden_files",
                "status",
            ],
            "properties": {
                "status": {"enum": ["IN_PROGRESS", "DONE", "BLOCKED", "FAILED"]}
            },
        }
        (root / ".agent" / "claim.schema.json").write_text(
            json.dumps(schema) + "\n", encoding="utf-8"
        )

    def write_claim(
        self,
        root: Path,
        *,
        task_id: str = "X1",
        agent_id: str = "agent-one",
        plan_hash: str = PLAN_HASH,
        status: str = "IN_PROGRESS",
    ) -> Path:
        claim = {
            "task_id": task_id,
            "agent_id": agent_id,
            "claimed_at": "2026-06-29T00:00:00Z",
            "active_plan_hash": plan_hash,
            "allowed_files": ["tests/**"],
            "forbidden_files": ["plugins/**"],
            "status": status,
        }
        if status == "DONE":
            claim.update(
                {
                    "completed_at": "2026-06-29T00:01:00Z",
                    "receipt": "docs/active/receipts/X1.md",
                }
            )
            (root / "docs" / "active" / "receipts" / "X1.md").write_text(
                "# Receipt\n", encoding="utf-8"
            )
        path = root / ".agent" / "claims" / f"{task_id}.{agent_id}.json"
        path.write_text(json.dumps(claim, indent=2) + "\n", encoding="utf-8")
        return path

    def write_state(self, root: Path, lines: list[str]) -> None:
        (root / ".agent" / "state.log").write_text(
            "\n".join(lines) + "\n", encoding="utf-8"
        )

    def test_valid_active_claim_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_root(root)
            self.write_claim(root)
            self.write_state(
                root,
                [
                    "2026-06-29T00:00:00Z CLAIM_CREATED task=X1 agent=agent-one",
                    "2026-06-29T00:00:01Z TASK_IN_PROGRESS task=X1 agent=agent-one",
                ],
            )
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_required_claim_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_root(root)
            path = self.write_claim(root)
            claim = json.loads(path.read_text(encoding="utf-8"))
            del claim["allowed_files"]
            path.write_text(json.dumps(claim) + "\n", encoding="utf-8")
            self.write_state(root, [])
            result = self.run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CLAIM_FIELD_MISSING", result.stdout + result.stderr)

    def test_stale_active_plan_hash_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_root(root)
            self.write_claim(root, plan_hash="sha256:" + "b" * 64)
            self.write_state(
                root,
                [
                    "2026-06-29T00:00:00Z CLAIM_CREATED task=X1 agent=agent-one",
                    "2026-06-29T00:00:01Z TASK_IN_PROGRESS task=X1 agent=agent-one",
                ],
            )
            result = self.run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ACTIVE_PLAN_HASH_MISMATCH", result.stdout + result.stderr)

    def test_unknown_task_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_root(root)
            self.write_claim(root, task_id="UNKNOWN")
            self.write_state(root, [])
            result = self.run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("TASK_NOT_FOUND", result.stdout + result.stderr)

    def test_done_claim_requires_done_event(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_root(root)
            self.write_claim(root, status="DONE")
            self.write_state(
                root,
                [
                    "2026-06-29T00:00:00Z CLAIM_CREATED task=X1 agent=agent-one",
                    "2026-06-29T00:00:01Z TASK_IN_PROGRESS task=X1 agent=agent-one",
                ],
            )
            result = self.run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("STATE_EVENT_MISSING", result.stdout + result.stderr)

    def test_duplicate_active_claims_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.seed_root(root)
            self.write_claim(root, agent_id="agent-one")
            self.write_claim(root, agent_id="agent-two")
            self.write_state(
                root,
                [
                    "2026-06-29T00:00:00Z CLAIM_CREATED task=X1 agent=agent-one",
                    "2026-06-29T00:00:01Z TASK_IN_PROGRESS task=X1 agent=agent-one",
                    "2026-06-29T00:00:02Z CLAIM_CREATED task=X1 agent=agent-two",
                    "2026-06-29T00:00:03Z TASK_IN_PROGRESS task=X1 agent=agent-two",
                ],
            )
            result = self.run_checker(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CLAIM_COLLISION", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
