"""Reject staged paths reserved for secrets or generated private data."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys
from pathlib import PurePosixPath


FORBIDDEN_ROOTS = {
    "outputs",
    "data",
    "learner_data",
    "private",
    "local",
    "sessions",
    "memories",
    "workspace",
    "logs",
    "dist",
}
ALLOWED_ENV_NAMES = {".env.example", ".env.template"}


def normalize(path: str) -> str:
    return path.replace("\\", "/").strip("/").lower()


def forbidden_reason(path: str) -> str | None:
    normalized = normalize(path)
    if not normalized:
        return None
    parts = PurePosixPath(normalized).parts
    name = parts[-1]

    if parts[0] in FORBIDDEN_ROOTS:
        return f"private/generated root: {parts[0]}"
    if name.startswith(".env") and name not in ALLOWED_ENV_NAMES:
        return "local environment file"
    if name == "auth.json":
        return "authentication state"
    if fnmatch.fnmatch(name, "credentials*.json") or fnmatch.fnmatch(name, "secrets.*"):
        return "credential/secret file"
    if any(name.endswith(extension) for extension in (".pem", ".key", ".p12", ".pfx")):
        return "private key material"
    if name.startswith(("state.db", "hermes_state.db", "response_store.db")):
        return "runtime database"
    if name.endswith((".sqlite", ".sqlite3")):
        return "runtime database"
    if parts[0] == "profiles" and any(
        part in {"sessions", "memories", "logs"} for part in parts[2:-1]
    ):
        return "profile runtime state"
    return None


def staged_paths() -> list[str]:
    completed = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
        check=True,
        capture_output=True,
    )
    return [item.decode("utf-8", errors="surrogateescape") for item in completed.stdout.split(b"\0") if item]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths-file")
    args = parser.parse_args()
    if args.paths_file:
        with open(args.paths_file, encoding="utf-8") as handle:
            paths = [line.strip() for line in handle if line.strip()]
    else:
        paths = staged_paths()

    rejected = [(path, forbidden_reason(path)) for path in paths]
    rejected = [(path, reason) for path, reason in rejected if reason]
    if rejected:
        for path, reason in rejected:
            print(f"PRIVATE_DATA_STAGE_REJECT {path}: {reason}", file=sys.stderr)
        return 3
    print("PRIVATE_DATA_STAGE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
