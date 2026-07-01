import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "plugins" / "hermes-thrice-great"))


def test_canonical_week_composes_every_deterministic_stage_once():
    from hermes_thrice_great.orchestration.week import run_week

    week = json.loads(
        (REPO_ROOT / "fixtures" / "synthetic" / "valid" / "week.json").read_text(encoding="utf-8")
    )
    result = run_week(week, offline=True)
    assert result["status"] == "complete"
    assert result["stages"] == [
        "smc_loaded", "receipts_validated", "pair_evaluated",
        "review_generated", "approval_wait", "approval_applied", "ledger_committed",
    ]
    assert result["approval_wait_observed"] is True
    assert result["ledger_commits"] == 1
    assert result["model_calls"] == result["network_attempts"] == 0
