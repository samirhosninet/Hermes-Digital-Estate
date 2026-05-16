#!/usr/bin/env python3
"""Read and validate a Hermes digital-state governance status JSON file.

Read-only, standard-library-only. This script validates the minimal v1 shape and
prints a stable JSON summary. It does not inspect secrets, mutate files, or enable
runtime enforcement.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "state_name",
    "phase",
    "posture",
    "portable",
    "artifacts",
    "model_council",
    "warnings",
}
VALID_PHASES = {
    "planning",
    "docs-only",
    "read-only-validation",
    "enforcement-design",
    "runtime-enforcement",
}
VALID_POSTURES = {
    "planning-only",
    "read-only",
    "approval-required",
    "enforcement-active",
    "blocked",
}


def fail(message: str) -> int:
    print(json.dumps({"ok": False, "error": message}, sort_keys=True), file=sys.stderr)
    return 2


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_status(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["status must be a JSON object"]

    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    if data.get("schema_version") != "governance-status-v1":
        errors.append("schema_version must be governance-status-v1")
    if data.get("phase") not in VALID_PHASES:
        errors.append("phase is not valid")
    if data.get("posture") not in VALID_POSTURES:
        errors.append("posture is not valid")
    if not isinstance(data.get("portable"), bool):
        errors.append("portable must be boolean")
    if not isinstance(data.get("artifacts"), list) or not all(isinstance(item, str) for item in data.get("artifacts", [])):
        errors.append("artifacts must be a list of strings")

    council = data.get("model_council")
    if not isinstance(council, dict):
        errors.append("model_council must be an object")
    else:
        for key in ("returned", "timeout_or_error"):
            if not isinstance(council.get(key), list) or not all(isinstance(item, str) for item in council.get(key, [])):
                errors.append(f"model_council.{key} must be a list of strings")
        if not isinstance(council.get("quorum_met"), bool):
            errors.append("model_council.quorum_met must be boolean")

    if not isinstance(data.get("warnings"), list) or not all(isinstance(item, str) for item in data.get("warnings", [])):
        errors.append("warnings must be a list of strings")
    return errors


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    council = data["model_council"]
    return {
        "ok": True,
        "schema_version": data["schema_version"],
        "state_name": data["state_name"],
        "phase": data["phase"],
        "posture": data["posture"],
        "portable": data["portable"],
        "artifact_count": len(data["artifacts"]),
        "model_council": {
            "returned_count": len(council["returned"]),
            "timeout_or_error_count": len(council["timeout_or_error"]),
            "quorum_met": council["quorum_met"],
        },
        "warnings": data["warnings"],
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return fail("usage: read_governance_status.py <status.json>")
    path = Path(argv[1])
    if not path.exists():
        return fail(f"file not found: {path}")
    try:
        data = load_json(path)
    except json.JSONDecodeError as exc:
        return fail(f"malformed JSON: {exc.msg}")
    errors = validate_status(data)
    if errors:
        return fail("; ".join(errors))
    print(json.dumps(summarize(data), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
