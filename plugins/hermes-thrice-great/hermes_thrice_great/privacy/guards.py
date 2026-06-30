"""Deterministic local privacy guards with no model or network dependency."""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path, PureWindowsPath
from typing import Callable


_RESERVED_WINDOWS_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
_PRIVATE_VALUE = re.compile(
    r"(?i)\b(learner_display_name|learner_id|answer|token|secret|email|profile_name)\s*=\s*([^\s,;]+)"
)
_PRIVATE_PATH = re.compile(r"(?i)\b(path\s*=\s*)(?:[a-z]:\\[^\s,;]+|\\\\[^\s,;]+)")


def _issue(code: str) -> dict[str, str]:
    return {"code": code}


def _is_reserved(part: str) -> bool:
    normalized = part.rstrip(" .").split(".", 1)[0].upper()
    return normalized in _RESERVED_WINDOWS_NAMES


def _is_reparse(path: Path) -> bool:
    try:
        metadata = os.lstat(path)
    except OSError:
        return False
    attributes = getattr(metadata, "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _inside(candidate: Path, root: Path) -> bool:
    try:
        return os.path.commonpath((os.path.normcase(str(candidate)), os.path.normcase(str(root)))) == os.path.normcase(str(root))
    except ValueError:
        return False


def validate_contained_path(
    root: Path,
    relative: str,
    *,
    injected_resolver: Callable[[Path], Path] | None = None,
) -> dict:
    """Validate a Windows-relative path against a resolved private root."""
    root = Path(root).resolve(strict=True)
    windows_path = PureWindowsPath(relative)
    if windows_path.is_absolute() or windows_path.drive or windows_path.root:
        return {"allowed": False, "issues": [_issue("PRIVACY_PATH_ESCAPE")]}
    parts = windows_path.parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        return {"allowed": False, "issues": [_issue("PRIVACY_PATH_ESCAPE")]}
    if any(_is_reserved(part) for part in parts):
        return {"allowed": False, "issues": [_issue("PRIVACY_RESERVED_NAME")]}

    candidate = root.joinpath(*parts)
    try:
        resolved = Path(injected_resolver(candidate) if injected_resolver else candidate.resolve(strict=False))
    except OSError as exc:
        if getattr(exc, "winerror", None) == 206 or exc.errno == 206:
            return {"allowed": False, "issues": [_issue("PRIVACY_HOST_PATH_UNSUPPORTED")]}
        return {"allowed": False, "issues": [_issue("PRIVACY_PATH_INSPECTION_FAILED")]}

    current = root
    saw_reparse = injected_resolver is not None
    for part in parts:
        current = current / part
        if current.exists() and _is_reparse(current):
            saw_reparse = True
    if not _inside(resolved, root):
        code = "PRIVACY_REPARSE_ESCAPE" if saw_reparse else "PRIVACY_PATH_ESCAPE"
        return {"allowed": False, "issues": [_issue(code)]}
    return {"allowed": True, "issues": [], "resolved_path": resolved}


def redact_log(value: str) -> str:
    """Remove private identifiers, secrets, emails, profile names, and paths."""
    redacted = _PRIVATE_PATH.sub(lambda match: f"{match.group(1)}[PRIVATE_PATH]", value)
    return _PRIVATE_VALUE.sub(lambda match: f"{match.group(1)}=[REDACTED]", redacted)
