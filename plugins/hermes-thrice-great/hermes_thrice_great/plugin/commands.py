"""In-process offline commands; native registration is completed by U8.7."""

from __future__ import annotations


_COMMANDS = {"ucc doctor", "ucc validate --synthetic", "ucc dry-run --synthetic"}


def execute(command: str, *, fixture: dict, offline: bool) -> dict:
    base = {"model_calls": 0, "network_attempts": 0, "ledger_writes": 0}
    if not offline or not fixture.get("synthetic") or command not in _COMMANDS:
        return {**base, "exit_code": 2, "issues": [{"code": "PLUGIN_COMMAND_UNSUPPORTED"}]}
    return {**base, "exit_code": 0, "issues": [], "command": command, "status": "ok"}
