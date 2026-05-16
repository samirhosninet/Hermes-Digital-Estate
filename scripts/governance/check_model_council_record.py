#!/usr/bin/env python3
"""Validate a Hermes Model Council result JSON file."""
from __future__ import annotations

import json
import sys
from pathlib import Path

VALID_STATUSES = {"returned", "timeout_or_error", "empty", "skipped"}


def emit(ok: bool, **kwargs) -> None:
    payload = {"ok": ok, **kwargs}
    print(json.dumps(payload, indent=2, sort_keys=True))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        emit(False, error="usage: check_model_council_record.py <model-council-results.json>")
        return 2
    path = Path(argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        emit(False, error=f"file not found: {path}")
        return 2
    except json.JSONDecodeError as exc:
        emit(False, error=f"malformed JSON: {exc.msg}")
        return 2

    results = data.get("results")
    if not isinstance(results, list):
        emit(False, error="results must be a list")
        return 2

    errors: list[str] = []
    counts = {status: 0 for status in VALID_STATUSES}
    for idx, record in enumerate(results):
        if not isinstance(record, dict):
            errors.append(f"results[{idx}] must be object")
            continue
        model = record.get("model")
        status = record.get("status")
        if not isinstance(model, str) or not model:
            errors.append(f"results[{idx}].model must be non-empty string")
        if status not in VALID_STATUSES:
            errors.append(f"results[{idx}].status must be one of {sorted(VALID_STATUSES)}")
        else:
            counts[status] += 1
        if status == "returned" and not record.get("content"):
            errors.append(f"returned model {model!r} must include content")
        if status == "timeout_or_error" and not record.get("error"):
            errors.append(f"timeout/error model {model!r} must include error")

    if errors:
        emit(False, errors=errors, counts=counts)
        return 2
    emit(True, counts=counts, total=len(results), quorum_met=counts["returned"] >= 3)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
