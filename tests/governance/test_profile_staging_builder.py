import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BUILDER = REPO_ROOT / "scripts" / "build_profile_staging.py"


class ProfileStagingBuilderTests(unittest.TestCase):
    def run_builder(self, source: Path, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BUILDER), "--source", str(source), "--output", str(output)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def seed_source(self, root: Path) -> None:
        files = {
            "distribution.yaml": "name: synthetic-stage\nversion: 0.0.1\ndistribution_owned:\n  - skills\n  - plugins/hermes-thrice-great\n  - schemas\n  - benchmarks\n",
            "SOUL.md": "# Synthetic\n",
            "config.yaml": "plugins:\n  enabled: []\n",
            ".env.EXAMPLE": "SYNTHETIC=\n",
            "skills/probe/SKILL.md": "---\nname: probe\ndescription: synthetic\n---\n",
            "plugins/hermes-thrice-great/plugin.yaml": "name: hermes-thrice-great\nversion: 0.0.1\n",
            "schemas/probe.json": "{}\n",
            "benchmarks/probe.txt": "synthetic\n",
            ".agent/state.log": "must-not-copy\n",
            "docs/active/authority.json": "{}\n",
            ".env": "MUST_NOT_COPY=true\n",
            "auth.json": "{}\n",
            "local/private.txt": "must-not-copy\n",
            "README.md": "must-not-copy\n",
        }
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def test_copies_only_allowlisted_payload_and_emits_sibling_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source"
            output = base / "dist" / "hermes-thrice-great-profile"
            self.seed_source(source)

            result = self.run_builder(source, output)
            self.assertEqual(result.returncode, 0, result.stderr)

            actual = {
                path.relative_to(output).as_posix()
                for path in output.rglob("*")
                if path.is_file()
            }
            expected_payload = {
                "distribution.yaml",
                "SOUL.md",
                "config.yaml",
                ".env.EXAMPLE",
                "skills/probe/SKILL.md",
                "plugins/hermes-thrice-great/plugin.yaml",
                "schemas/probe.json",
                "benchmarks/probe.txt",
            }
            self.assertEqual(expected_payload, actual)
            self.assertFalse(any(name.startswith((".agent/", "docs/", "local/")) for name in actual))
            self.assertNotIn(".env", actual)
            self.assertNotIn("auth.json", actual)
            self.assertNotIn("README.md", actual)

            inventory_path = output.with_name(f"{output.name}.inventory.json")
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
            self.assertEqual(sorted(expected_payload), sorted(item["path"] for item in inventory["files"]))

    def test_rebuild_removes_stale_non_allowlisted_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source"
            output = base / "dist" / "hermes-thrice-great-profile"
            self.seed_source(source)
            first = self.run_builder(source, output)
            self.assertEqual(first.returncode, 0, first.stderr)
            (output / "stale-private.txt").write_text("stale\n", encoding="utf-8")

            second = self.run_builder(source, output)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertFalse((output / "stale-private.txt").exists())

    def test_rejects_source_output_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source"
            self.seed_source(source)
            result = self.run_builder(source, source / "dist")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("SOURCE_OUTPUT_OVERLAP", result.stderr)

    def test_allows_only_canonical_in_repo_distribution_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source"
            self.seed_source(source)
            output = source / "dist" / "hermes-thrice-great-profile"
            result = self.run_builder(source, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "distribution.yaml").is_file())
            self.assertTrue(output.with_name(f"{output.name}.inventory.json").is_file())

    def test_optional_directories_require_manifest_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source"
            output = base / "output"
            self.seed_source(source)
            (source / "distribution.yaml").write_text(
                "name: minimal\nversion: 0.0.1\ndistribution_owned:\n  - skills\n",
                encoding="utf-8",
            )
            result = self.run_builder(source, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "skills" / "probe" / "SKILL.md").is_file())
            self.assertFalse((output / "plugins").exists())
            self.assertFalse((output / "schemas").exists())
            self.assertFalse((output / "benchmarks").exists())


if __name__ == "__main__":
    unittest.main()
