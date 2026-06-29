"""Validate the non-authoritative, agent-ignored ACDF archive boundary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _is_archive_ignored(agentignore: Path, archive_relative: str) -> bool:
    normalized_archive = archive_relative.replace("\\", "/").strip("/")
    for raw in agentignore.read_text(encoding="utf-8").splitlines():
        pattern = raw.strip().lstrip("/")
        if not pattern or pattern.startswith("#") or pattern.startswith("!"):
            continue
        normalized_pattern = pattern.replace("\\", "/").rstrip("/")
        if normalized_pattern == normalized_archive or normalized_pattern.startswith(
            f"{normalized_archive}/"
        ):
            return True
    return False


def validate(root_arg: Path) -> list[str]:
    errors: list[str] = []
    root = root_arg.resolve(strict=True)
    authority_path = root / "docs" / "active" / "authority.json"
    if not authority_path.is_file():
        return [f"AUTHORITY_MISSING: {authority_path}"]
    try:
        authority = json.loads(authority_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"AUTHORITY_PARSE: {exc}"]

    policy = authority.get("archive_policy")
    if not isinstance(policy, dict):
        return ["ARCHIVE_POLICY_MISSING"]
    archive_raw = policy.get("archive_path")
    if not isinstance(archive_raw, str) or not archive_raw.strip():
        return ["ARCHIVE_PATH_INVALID"]
    archive_relative = archive_raw.replace("\\", "/").strip("/")
    archive_path = (root / archive_relative).resolve(strict=False)
    try:
        archive_path.relative_to(root)
    except ValueError:
        return [f"ARCHIVE_PATH_ESCAPE: {archive_raw}"]

    if not archive_path.is_dir():
        errors.append(f"ARCHIVE_MISSING: {archive_relative}")
    if policy.get("archive_is_authority") is not False:
        errors.append("ARCHIVE_AUTHORITY_INVALID: archive_is_authority must be false")
    if policy.get("current_state") not in {"initialized", "operational"}:
        errors.append(
            f"ARCHIVE_STATE_INVALID: {policy.get('current_state')}"
        )

    agentignore = root / ".agentignore"
    if not agentignore.is_file():
        errors.append("AGENTIGNORE_MISSING")
    else:
        try:
            ignored = _is_archive_ignored(agentignore, archive_relative)
        except (OSError, UnicodeError) as exc:
            errors.append(f"AGENTIGNORE_READ_ERROR: {exc}")
        else:
            if not ignored:
                errors.append(f"ARCHIVE_NOT_IGNORED: {archive_relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        errors = validate(args.root)
    except (OSError, RuntimeError) as exc:
        errors = [f"CHECKER_ERROR: {exc}"]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("ARCHIVE_HYGIENE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
