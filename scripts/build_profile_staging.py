"""Build the deny-by-default Hermes profile staging payload."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path


ALLOWLIST_FILES = (
    "distribution.yaml",
    "SOUL.md",
    "config.yaml",
    ".env.EXAMPLE",
)
ALLOWLIST_DIRS = (
    "skills",
    "plugins/hermes-thrice-great",
    "schemas",
    "benchmarks",
)
INVENTORY_NAME = "payload-inventory.json"


class StagingError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _is_reparse_point(path: Path) -> bool:
    try:
        metadata = os.lstat(path)
    except OSError as exc:
        raise StagingError("PATH_INSPECTION_FAILED", f"cannot inspect {path}: {exc}") from exc
    attributes = getattr(metadata, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return path.is_symlink() or bool(attributes & reparse_flag)


def _assert_safe_selected_tree(path: Path, source: Path) -> None:
    if _is_reparse_point(path):
        raise StagingError("REPARSE_POINT_REJECTED", f"selected path is a link/reparse point: {path}")
    resolved = path.resolve()
    if not _is_relative_to(resolved, source):
        raise StagingError("SOURCE_PATH_ESCAPE", f"selected path escapes source root: {path}")
    if path.is_dir():
        for child in path.rglob("*"):
            if _is_reparse_point(child):
                raise StagingError(
                    "REPARSE_POINT_REJECTED",
                    f"selected payload contains a link/reparse point: {child}",
                )


def _copy_selected(source: Path, staging: Path) -> None:
    for relative in ALLOWLIST_FILES:
        item = source / relative
        if not item.exists():
            continue
        _assert_safe_selected_tree(item, source)
        if not item.is_file():
            raise StagingError("EXPECTED_FILE", f"allowlisted file is not a file: {relative}")
        destination = staging / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, destination)

    for relative in ALLOWLIST_DIRS:
        item = source / relative
        if not item.exists():
            continue
        _assert_safe_selected_tree(item, source)
        if not item.is_dir():
            raise StagingError("EXPECTED_DIRECTORY", f"allowlisted directory is not a directory: {relative}")
        destination = staging / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(item, destination)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_inventory(staging: Path) -> None:
    files = [
        {"path": path.relative_to(staging).as_posix(), "sha256": _sha256(path)}
        for path in sorted(staging.rglob("*"))
        if path.is_file() and path.name != INVENTORY_NAME
    ]
    (staging / INVENTORY_NAME).write_text(
        json.dumps({"schema_version": "ucc.profile_payload_inventory.v1", "files": files}, indent=2)
        + "\n",
        encoding="utf-8",
    )


def build(source_arg: Path, output_arg: Path) -> Path:
    source = source_arg.resolve(strict=True)
    output = output_arg.resolve(strict=False)
    if source == output or _is_relative_to(output, source) or _is_relative_to(source, output):
        raise StagingError("SOURCE_OUTPUT_OVERLAP", "source and output trees must not overlap")
    if not source.is_dir():
        raise StagingError("SOURCE_NOT_DIRECTORY", f"source is not a directory: {source}")
    if not (source / "distribution.yaml").is_file():
        raise StagingError("MISSING_MANIFEST", "distribution.yaml is required at the source root")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        _copy_selected(source, temporary)
        _write_inventory(temporary)
        if output.exists():
            if _is_reparse_point(output):
                raise StagingError("OUTPUT_REPARSE_POINT", f"refusing to replace reparse-point output: {output}")
            shutil.rmtree(output)
        temporary.replace(output)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        output = build(args.source, args.output)
    except StagingError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
