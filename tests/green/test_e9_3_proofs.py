import json
import socket
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "plugins" / "hermes-thrice-great"))
WEEK_PATH = REPO_ROOT / "fixtures" / "synthetic" / "valid" / "week.json"
ADVERSARIAL_PATH = REPO_ROOT / "fixtures" / "synthetic" / "adversarial" / "week-cases.json"
LEDGER_PATH = REPO_ROOT / "fixtures" / "synthetic" / "valid" / "ledger.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_two_canonical_runs_are_byte_identical_and_do_not_mutate_baseline():
    from hermes_thrice_great.orchestration.week import run_week

    week_bytes = WEEK_PATH.read_bytes()
    ledger_bytes = LEDGER_PATH.read_bytes()
    first = run_week(load(WEEK_PATH), offline=True)
    second = run_week(load(WEEK_PATH), offline=True)
    assert first["canonical_bytes"] == second["canonical_bytes"]
    assert first["ledger_hash"] == second["ledger_hash"]
    assert WEEK_PATH.read_bytes() == week_bytes
    assert LEDGER_PATH.read_bytes() == ledger_bytes


def test_approval_wait_precedes_apply_and_missing_approval_never_commits():
    from hermes_thrice_great.orchestration.week import run_adversarial_case, run_week

    week = load(WEEK_PATH)
    result = run_week(week, offline=True)
    assert result["stages"].index("approval_wait") < result["stages"].index("approval_applied")
    missing = next(case for case in load(ADVERSARIAL_PATH)["cases"] if case["mutation"] == "remove_approval")
    rejected = run_adversarial_case(week, missing, offline=True)
    assert rejected["issues"] == [{"code": "APPROVAL_REQUIRED"}]
    assert rejected["ledger_commits"] == 0


def test_replay_and_write_fault_leave_baseline_ledger_unchanged():
    from hermes_thrice_great.orchestration.week import run_adversarial_case

    before = LEDGER_PATH.read_bytes()
    cases = load(ADVERSARIAL_PATH)["cases"]
    for mutation in ("change_approval_payload", "inject_temp_write_fault"):
        case = next(item for item in cases if item["mutation"] == mutation)
        result = run_adversarial_case(load(WEEK_PATH), case, offline=True)
        assert result["ledger_commits"] == 0
    assert LEDGER_PATH.read_bytes() == before


def test_valid_and_adversarial_runs_make_zero_socket_connections(monkeypatch):
    from hermes_thrice_great.orchestration.week import run_adversarial_case, run_week

    attempts = []

    def blocked_connect(_socket, address):
        attempts.append(address)
        raise AssertionError("socket connection attempted")

    monkeypatch.setattr(socket.socket, "connect", blocked_connect)
    week = load(WEEK_PATH)
    assert run_week(week, offline=True)["status"] == "complete"
    for case in load(ADVERSARIAL_PATH)["cases"]:
        run_adversarial_case(week, case, offline=True)
    assert attempts == []
