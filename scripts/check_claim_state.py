"""Validate ACDF claims, task-board synchronization, receipts, and state events."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
BOARD_TASK_RE = re.compile(r"^\|\s*([A-Z][A-Z0-9]*(?:\.[0-9]+[A-Z]?)?)\s*\|")


def _read_json(path: Path, code: str, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{code}: {path} {exc}")
        return None


def _has_event(lines: list[str], event: str, task: str, agent: str) -> bool:
    return any(
        f" {event} " in f" {line} "
        and f"task={task}" in line
        and f"agent={agent}" in line
        for line in lines
    )


def _receipt_path(root: Path, raw: object) -> Path | None:
    if not isinstance(raw, str) or not raw:
        return None
    candidate = Path(raw)
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
    authority = _read_json(
        root / "docs" / "active" / "authority.json", "AUTHORITY_PARSE", errors
    )
    schema = _read_json(root / ".agent" / "claim.schema.json", "SCHEMA_PARSE", errors)
    if not isinstance(authority, dict) or not isinstance(schema, dict):
        return errors
    active_plan_hash = authority.get("active_plan_hash")
    required = schema.get("required")
    status_schema = schema.get("properties", {}).get("status", {})
    statuses = status_schema.get("enum") if isinstance(status_schema, dict) else None
    task_schema = schema.get("properties", {}).get("task_id", {})
    task_pattern = task_schema.get("pattern") if isinstance(task_schema, dict) else None
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        errors.append("SCHEMA_REQUIRED_INVALID")
        return errors
    if not isinstance(statuses, list):
        errors.append("SCHEMA_STATUS_INVALID")
        return errors

    task_board = root / "docs" / "active" / "PROJECT_TASKS.md"
    try:
        task_ids = {
            match.group(1)
            for line in task_board.read_text(encoding="utf-8").splitlines()
            if (match := BOARD_TASK_RE.match(line))
        }
    except (OSError, UnicodeError) as exc:
        return errors + [f"TASK_BOARD_READ: {exc}"]

    state_path = root / ".agent" / "state.log"
    try:
        state_lines = state_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return errors + [f"STATE_LOG_READ: {exc}"]

    claims_dir = root / ".agent" / "claims"
    if not claims_dir.is_dir():
        return errors + ["CLAIMS_DIR_MISSING"]

    active_by_task: dict[str, list[str]] = defaultdict(list)
    active_claims: list[str] = []
    for path in sorted(claims_dir.glob("*.json")):
        claim = _read_json(path, "CLAIM_PARSE", errors)
        if not isinstance(claim, dict):
            continue
        missing = [field for field in required if field not in claim]
        for field in missing:
            errors.append(f"CLAIM_FIELD_MISSING: {path.name} field={field}")
        if missing:
            continue

        task = claim.get("task_id")
        agent = claim.get("agent_id")
        status = claim.get("status")
        if (
            not isinstance(task, str)
            or not task
            or (isinstance(task_pattern, str) and re.fullmatch(task_pattern, task) is None)
        ):
            errors.append(f"CLAIM_TASK_INVALID: {path.name}")
            continue
        if not isinstance(agent, str) or not agent:
            errors.append(f"CLAIM_AGENT_INVALID: {path.name}")
            continue
        if path.name != f"{task}.{agent}.json":
            errors.append(f"CLAIM_FILENAME_MISMATCH: {path.name}")
        if task not in task_ids:
            errors.append(f"TASK_NOT_FOUND: {task}")
        if status not in statuses:
            errors.append(f"CLAIM_STATUS_INVALID: {path.name} status={status}")
        if not HASH_RE.fullmatch(str(claim.get("active_plan_hash", ""))):
            errors.append(f"CLAIM_PLAN_HASH_INVALID: {path.name}")
        for field in ("allowed_files", "forbidden_files"):
            value = claim.get(field)
            if (
                not isinstance(value, list)
                or not value
                or not all(isinstance(item, str) and item for item in value)
            ):
                errors.append(f"CLAIM_SCOPE_INVALID: {path.name} field={field}")

        if not _has_event(state_lines, "CLAIM_CREATED", task, agent):
            errors.append(f"STATE_EVENT_MISSING: {task} agent={agent} event=CLAIM_CREATED")
        if not _has_event(state_lines, "TASK_IN_PROGRESS", task, agent):
            errors.append(f"STATE_EVENT_MISSING: {task} agent={agent} event=TASK_IN_PROGRESS")

        if status == "IN_PROGRESS":
            effective_plan = claim.get("revalidated_plan_hash", claim.get("active_plan_hash"))
            if effective_plan != active_plan_hash:
                errors.append(
                    "ACTIVE_PLAN_HASH_MISMATCH: "
                    f"{path.name} expected={active_plan_hash} actual={effective_plan}"
                )
            active_by_task[task].append(path.name)
            active_claims.append(path.name)
        elif status == "DONE":
            if not _has_event(state_lines, "TASK_DONE", task, agent):
                errors.append(f"STATE_EVENT_MISSING: {task} agent={agent} event=TASK_DONE")
            receipt = _receipt_path(root, claim.get("receipt"))
            if receipt is None or not receipt.is_file():
                errors.append(f"RECEIPT_MISSING: {path.name}")
            if not isinstance(claim.get("completed_at"), str):
                errors.append(f"CLAIM_FIELD_MISSING: {path.name} field=completed_at")
        elif status == "BLOCKED" and not _has_event(
            state_lines, "TASK_BLOCKED", task, agent
        ):
            errors.append(f"STATE_EVENT_MISSING: {task} agent={agent} event=TASK_BLOCKED")
        elif status == "FAILED" and not _has_event(
            state_lines, "TASK_FAILED", task, agent
        ):
            errors.append(f"STATE_EVENT_MISSING: {task} agent={agent} event=TASK_FAILED")

    for task, paths in active_by_task.items():
        if len(paths) > 1:
            errors.append(f"CLAIM_COLLISION: task={task} claims={paths}")
    if len(active_claims) > 1:
        errors.append(f"ACTIVE_TASK_COUNT: expected<=1 actual={len(active_claims)}")
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
    print("CLAIM_STATE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
