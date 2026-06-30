"""Probe Windows filesystem behavior required by the production harness."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def result(outcome: str, detail: str) -> dict[str, str]:
    return {"outcome": outcome, "detail": detail}


def probe_long_path(root: Path) -> dict[str, str]:
    path = root / "long-path"
    while len(str(path / "sentinel.txt")) <= 280:
        path /= "segment_" + ("x" * 32)
    sentinel = path / "sentinel.txt"
    try:
        path.mkdir(parents=True)
        sentinel.write_text("synthetic-host-canary", encoding="utf-8")
        if sentinel.read_text(encoding="utf-8") != "synthetic-host-canary":
            return result("ERROR", "long-path round trip changed content")
        return result("PASS_SUPPORTED", f"round trip succeeded at {len(str(sentinel))} characters")
    except OSError as exc:
        return result("PASS_FAIL_CLOSED", f"OS rejected {len(str(sentinel))}-character path: winerror={exc.winerror}")


def probe_drive_case(root: Path) -> dict[str, str]:
    sentinel = root / "drive-case.txt"
    sentinel.write_text("synthetic-host-canary", encoding="utf-8")
    drive = sentinel.drive
    if not drive:
        return result("ERROR", "temporary root has no Windows drive")
    alternate = Path((drive.swapcase() + str(sentinel)[len(drive) :]))
    try:
        if not os.path.samefile(sentinel, alternate):
            return result("ERROR", "drive-letter case aliases did not identify the same file")
        return result("PASS_SUPPORTED", f"{drive} and {drive.swapcase()} resolve to the same file")
    except OSError as exc:
        return result("ERROR", f"drive-case comparison failed: winerror={exc.winerror}")


def probe_reserved_name(root: Path) -> dict[str, str]:
    reserved = root / "CON"
    try:
        reserved.mkdir()
    except OSError as exc:
        return result("PASS_FAIL_CLOSED", f"reserved name rejected: winerror={exc.winerror}")
    return result("PASS_SUPPORTED", "reserved device name CON was creatable; product guards must reject it")


def probe_junction_reparse(root: Path) -> dict[str, str]:
    containment = root / "containment"
    target = root / "outside-target"
    link = containment / "escape-junction"
    containment.mkdir()
    target.mkdir()
    (target / "sentinel.txt").write_text("synthetic-host-canary", encoding="utf-8")
    completed = subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return result("PASS_FAIL_CLOSED", f"junction creation rejected with exit {completed.returncode}")
    try:
        resolved = (link / "sentinel.txt").resolve(strict=True)
        contained = os.path.commonpath([str(containment.resolve()), str(resolved)]) == str(containment.resolve())
        if contained:
            return result("ERROR", "junction target was incorrectly classified as contained")
        return result("PASS_SUPPORTED", "junction is traversable and canonical resolution exposes escape")
    finally:
        os.rmdir(link)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    if sys.platform != "win32":
        print(json.dumps({"platform": sys.platform, "probes": {}, "error": "native Windows required"}))
        return 2

    root = args.root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    probes = {
        "long_path": probe_long_path(root),
        "drive_case": probe_drive_case(root),
        "reserved_name": probe_reserved_name(root),
        "junction_reparse": probe_junction_reparse(root),
    }
    print(json.dumps({"platform": sys.platform, "probes": probes}, sort_keys=True))
    return 2 if any(item["outcome"] == "ERROR" for item in probes.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
