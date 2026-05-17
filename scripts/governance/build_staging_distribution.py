#!/usr/bin/env python3
"""Build a local staging copy of the Digital State distribution.

The staging directory is built from manifest-approved roots only. It must
look like the future GitHub distribution repo, not like the full workspace.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_SUFFIXES = {".pyc", ".pyo"}
SKIP_DIR_NAMES = {"__pycache__"}


def _read_manifest(root: Path) -> dict[str, Any]:
    with (root / "digital-state.manifest.json").open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _is_relative_path(value: str) -> bool:
    path = Path(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and not value.startswith("~")


def _resolve_output(root: Path, output: str) -> Path:
    return Path(output).expanduser().resolve()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _is_forbidden(rel_path: str, forbidden_paths: list[str]) -> bool:
    normalized = rel_path.replace("\\", "/").strip("/")
    for forbidden in forbidden_paths:
        item = forbidden.replace("\\", "/").strip("/")
        if not item:
            continue
        if normalized == item or normalized.startswith(item.rstrip("/") + "/"):
            return True
    return False


def _should_skip_file(path: Path) -> bool:
    return path.suffix in SKIP_SUFFIXES or any(part in SKIP_DIR_NAMES for part in path.parts)


def _iter_allowed_files(root: Path, allowed_root: str) -> list[Path]:
    source = root / allowed_root
    if not source.exists():
        return []
    if source.is_file():
        return [source]
    return [item for item in source.rglob("*") if item.is_file()]


def validate_output_path(root: Path, output: Path, forbidden_paths: list[str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if output == root or _is_within(output, root):
        findings.append({
            "severity": "error",
            "code": "output_inside_source",
            "detail": str(output),
        })
    for part in output.parts:
        if _is_forbidden(part, forbidden_paths):
            findings.append({
                "severity": "error",
                "code": "output_forbidden_path",
                "detail": str(output),
            })
            break
    if output.exists() and any(output.iterdir()):
        findings.append({
            "severity": "error",
            "code": "output_not_empty",
            "detail": str(output),
        })
    return findings


def build_staging(root: Path, output: Path) -> dict[str, Any]:
    root = root.resolve()
    output = output.resolve()
    manifest = _read_manifest(root)
    allowed_roots = manifest.get("allowed_roots", [])
    forbidden_paths = manifest.get("forbidden_paths", [])
    findings = validate_output_path(root, output, forbidden_paths)
    copied: list[str] = []
    skipped: list[str] = []

    for allowed in allowed_roots:
        if not isinstance(allowed, str) or not _is_relative_path(allowed):
            findings.append({
                "severity": "error",
                "code": "invalid_allowed_root",
                "detail": str(allowed),
            })
            continue
        if _is_forbidden(allowed, forbidden_paths):
            findings.append({
                "severity": "error",
                "code": "allowed_root_forbidden",
                "detail": allowed,
            })

    if any(item["severity"] == "error" for item in findings):
        return {
            "ok": False,
            "output": str(output),
            "copied_count": 0,
            "copied": copied,
            "skipped": skipped,
            "findings": findings,
        }

    output.mkdir(parents=True, exist_ok=True)

    for allowed in allowed_roots:
        for source_file in _iter_allowed_files(root, allowed):
            rel = source_file.relative_to(root).as_posix()
            if _is_forbidden(rel, forbidden_paths):
                skipped.append(rel)
                findings.append({
                    "severity": "warning",
                    "code": "skipped_forbidden_file",
                    "detail": rel,
                })
                continue
            if _should_skip_file(source_file):
                skipped.append(rel)
                continue
            target = output / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target)
            copied.append(rel)

    return {
        "ok": not any(item["severity"] == "error" for item in findings),
        "output": str(output),
        "copied_count": len(copied),
        "copied": copied,
        "skipped": skipped,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a local Digital State staging distribution")
    parser.add_argument("--output", required=True, help="Empty output directory outside the source repository")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Source repository root")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args(argv)

    result = build_staging(Path(args.root), _resolve_output(Path(args.root), args.output))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        status = "OK" if result["ok"] else "FAILED"
        print(f"Staging distribution build: {status}")
        print(f"Output: {result['output']}")
        print(f"Copied files: {result['copied_count']}")
        for finding in result["findings"]:
            print(f"- {finding['severity']}: {finding['code']}: {finding['detail']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
