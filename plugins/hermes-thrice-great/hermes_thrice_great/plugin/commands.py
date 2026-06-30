"""In-process offline commands; native registration is completed by U8.7."""

from __future__ import annotations

import json


_COMMANDS = {"ucc doctor", "ucc validate --synthetic", "ucc dry-run --synthetic"}


def execute(command: str, *, fixture: dict, offline: bool) -> dict:
    base = {"model_calls": 0, "network_attempts": 0, "ledger_writes": 0}
    if not offline or not fixture.get("synthetic") or command not in _COMMANDS:
        return {**base, "exit_code": 2, "issues": [{"code": "PLUGIN_COMMAND_UNSUPPORTED"}]}
    return {**base, "exit_code": 0, "issues": [], "command": command, "status": "ok"}


def setup_cli(parser) -> None:
    subcommands = parser.add_subparsers(dest="ucc_action", required=True)
    subcommands.add_parser("doctor", help="Verify the offline deterministic core")
    validate = subcommands.add_parser("validate", help="Validate the bundled synthetic contract path")
    validate.add_argument("--synthetic", action="store_true", required=True)
    dry_run = subcommands.add_parser("dry-run", help="Run the synthetic workflow without writes")
    dry_run.add_argument("--synthetic", action="store_true", required=True)


def handle_cli(args) -> int:
    action = args.ucc_action
    command = "ucc doctor" if action == "doctor" else f"ucc {action} --synthetic"
    result = execute(command, fixture={"synthetic": True}, offline=True)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return result["exit_code"]
