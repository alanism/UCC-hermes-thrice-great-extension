"""Validate ACDF authority bindings without third-party dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _contained_path(root: Path, relative: object) -> Path | None:
    if not isinstance(relative, str):
        return None
    candidate = Path(relative)
    if candidate.is_absolute():
        return None
    resolved = (root / candidate).resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError:
        return None
    return resolved


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

    bindings = authority.get("binding_artifacts")
    if not isinstance(bindings, dict) or not bindings:
        return ["BINDINGS_INVALID: binding_artifacts must be a non-empty object"]

    build_plan_hash: str | None = None
    for name, binding in bindings.items():
        if not isinstance(binding, dict):
            errors.append(f"BINDING_INVALID: {name}")
            continue
        path = _contained_path(root, binding.get("path"))
        if path is None:
            errors.append(f"PATH_ESCAPE: {name}")
            continue
        if not path.is_file():
            errors.append(f"BINDING_MISSING: {name} path={binding.get('path')}")
            continue
        expected = binding.get("sha256")
        actual = _sha256(path)
        if not isinstance(expected, str) or expected.lower() != actual:
            errors.append(
                f"HASH_MISMATCH: {name} expected={expected} actual={actual}"
            )
        if name == "build_plan":
            build_plan_hash = actual

    if build_plan_hash is None:
        errors.append("BUILD_PLAN_BINDING_MISSING")
    else:
        expected_active = f"sha256:{build_plan_hash}"
        if authority.get("active_plan_hash") != expected_active:
            errors.append(
                "ACTIVE_PLAN_HASH_MISMATCH: "
                f"expected={expected_active} actual={authority.get('active_plan_hash')}"
            )

    active_dir = root / "docs" / "active"
    active_plans = sorted(active_dir.glob("BUILD_PLAN*.md")) if active_dir.is_dir() else []
    if len(active_plans) != 1:
        errors.append(
            "ACTIVE_PLAN_COUNT: "
            f"expected=1 actual={len(active_plans)} "
            f"paths={[path.name for path in active_plans]}"
        )
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
    print("AUTHORITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
