"""Run mutation probes with strict behavioral/infrastructure classification."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = REPO_ROOT / "tests" / "mutation_canary" / "mutation_cases.py"


def run(command: list[str], *, mutation: str | None, timeout: float) -> dict:
    environment = os.environ.copy()
    if mutation is None:
        environment.pop("HTG_MUTATION_CASE", None)
    else:
        environment["HTG_MUTATION_CASE"] = mutation
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"kind": "timeout"}
    return {
        "kind": "exit",
        "returncode": completed.returncode,
        "stdout": completed.stdout[-1000:],
        "stderr": completed.stderr[-1000:],
    }


def classify(
    baseline_command: list[str],
    mutant_command: list[str],
    *,
    mutation: str,
    timeout: float = 3.0,
) -> dict[str, str | int | None]:
    baseline = run(baseline_command, mutation=None, timeout=3.0)
    if baseline["kind"] != "exit" or baseline.get("returncode") != 0:
        return {"outcome": "ERROR", "reason": "baseline_failed"}

    mutant = run(mutant_command, mutation=mutation, timeout=timeout)
    if mutant["kind"] == "timeout":
        return {"outcome": "ERROR", "reason": "timeout"}
    returncode = int(mutant["returncode"])
    if returncode == 0:
        return {"outcome": "SURVIVED", "reason": "tests_passed", "returncode": 0}
    if returncode == 1:
        return {"outcome": "KILLED", "reason": "test_failure", "returncode": 1}
    return {"outcome": "ERROR", "reason": f"infrastructure_exit_{returncode}", "returncode": returncode}


def meta_canaries() -> dict[str, dict]:
    pytest_case = [sys.executable, "-m", "pytest", "-q", str(CASE_FILE)]
    missing_case = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        str(CASE_FILE.with_name("missing_setup_case.py")),
    ]
    return {
        "killable": classify(pytest_case, pytest_case, mutation="killable"),
        "equivalent": classify(pytest_case, pytest_case, mutation="equivalent"),
        "crash": classify(pytest_case, pytest_case, mutation="crash"),
        "setup_error": classify(pytest_case, missing_case, mutation="setup_error"),
        "timeout": classify(pytest_case, pytest_case, mutation="timeout", timeout=0.2),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--all", action="store_true")
    args = parser.parse_args()
    report = meta_canaries()
    print(json.dumps(report, sort_keys=True))
    expected = {
        "killable": "KILLED",
        "equivalent": "SURVIVED",
        "crash": "ERROR",
        "setup_error": "ERROR",
        "timeout": "ERROR",
    }
    passed = all(report[name]["outcome"] == outcome for name, outcome in expected.items())
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
