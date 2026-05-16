#!/usr/bin/env python3
"""Read-only portability scanner for Hermes digital-state artifacts."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FORBIDDEN_PATTERNS = [
    ("windows_drive_path", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:\\(?![nrt])")),
    ("wsl_drive_mount", re.compile(r"/mnt/[a-zA-Z]/")),
    ("external_concept_folder", re.compile(r"hermes_hyperagent", re.IGNORECASE)),
    ("api_key_assignment", re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{20,}[\"']")),
]
TEXT_EXTENSIONS = {".md", ".json", ".yaml", ".yml", ".py", ".txt"}
SKIP_FILE_NAMES = {
    "check_portability.py",  # contains the forbidden regex patterns by definition
    "test_governance_portability.py",  # contains intentionally forbidden fixture strings
}


def should_scan(path: Path) -> bool:
    return path.name not in SKIP_FILE_NAMES


def iter_files(paths: list[Path]):
    for path in paths:
        if path.is_file():
            if should_scan(path):
                yield path
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix.lower() in TEXT_EXTENSIONS and should_scan(child):
                    yield child


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(json.dumps({"ok": False, "error": "usage: check_portability.py <file-or-dir> [...]"}, sort_keys=True))
        return 2
    paths = [Path(item) for item in argv[1:]]
    findings = []
    scanned = 0
    for file_path in iter_files(paths):
        scanned += 1
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append({"file": str(file_path), "line": line, "pattern": name})
    payload = {
        "schema_version": "portability-check-v1",
        "checked_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "portable": not findings,
        "scanned_files": scanned,
        "findings": findings,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
