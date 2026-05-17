#!/usr/bin/env python3
"""Validate the portable Hermes Digital State profile distribution.

This script is intentionally read-only and stdlib-only. It validates the
Digital State manifest and Hermes profile distribution metadata without
reading or printing secrets.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "digital-state.manifest.json"
DISTRIBUTION_PATH = REPO_ROOT / "distribution.yaml"

WINDOWS_PATH_RE = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:\\\\|(?<![A-Za-z0-9_])[A-Za-z]:/")
ABSOLUTE_POSIX_RE = re.compile(r"^/(?:home|mnt|Users|var|etc|tmp|opt)/")
SECRET_VALUE_RE = re.compile(
    r"(?i)(api[_-]?key|token|secret|password)[ \t]*[:=][ \t]*['\"]?[A-Za-z0-9_\-]{16,}"
)
FORBIDDEN_REAL_ENV = {".env", "auth.json"}


def _simple_yaml_load(path: Path) -> dict[str, Any]:
    """Parse the small distribution.yaml subset used by Hermes docs.

    This avoids a PyYAML dependency. It supports top-level scalars and lists
    of strings or mappings with scalar values.
    """
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            return loaded
    except Exception:
        pass

    data: dict[str, Any] = {}
    current_key: str | None = None
    current_item: dict[str, Any] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            current_item = None
            if value:
                data[key] = _parse_scalar(value)
            else:
                data[key] = []
            continue
        if current_key is None:
            raise ValueError(f"Cannot parse YAML line: {raw_line}")
        stripped = line.strip()
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if ":" in item:
                k, v = item.split(":", 1)
                current_item = {k.strip(): _parse_scalar(v.strip())}
                data[current_key].append(current_item)
            else:
                current_item = None
                data[current_key].append(_parse_scalar(item))
            continue
        if current_item is not None and ":" in stripped:
            k, v = stripped.split(":", 1)
            current_item[k.strip()] = _parse_scalar(v.strip())
            continue
        raise ValueError(f"Cannot parse YAML line: {raw_line}")
    return data


def _parse_scalar(value: str) -> Any:
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def _is_repo_relative(path: str) -> bool:
    return not (
        path.startswith("/")
        or path.startswith("~")
        or ".." in Path(path).parts
        or WINDOWS_PATH_RE.search(path)
    )


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_manifest(manifest: dict[str, Any], root: Path = REPO_ROOT) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    required_keys = {
        "schema_version",
        "name",
        "version",
        "distribution",
        "compatible_hermes",
        "allowed_roots",
        "forbidden_paths",
        "required_files",
        "required_checks",
        "supported_modes",
        "local_credentials",
        "secrets_policy",
        "update_policy",
    }
    missing = sorted(required_keys - set(manifest))
    for key in missing:
        findings.append({"severity": "error", "code": "manifest_missing_key", "detail": key})

    if manifest.get("schema_version") != "digital-state-manifest-v1":
        findings.append({"severity": "error", "code": "manifest_schema_version", "detail": str(manifest.get("schema_version"))})

    distribution = manifest.get("distribution", {})
    if distribution.get("type") != "hermes_profile_distribution":
        findings.append({"severity": "error", "code": "manifest_distribution_type", "detail": str(distribution.get("type"))})
    for field in ("install_command", "update_command", "run_command"):
        value = distribution.get(field, "")
        if not isinstance(value, str) or not value:
            findings.append({"severity": "error", "code": "manifest_distribution_command", "detail": field})

    for collection_name in ("allowed_roots", "forbidden_paths", "required_files"):
        for entry in manifest.get(collection_name, []):
            if not isinstance(entry, str) or not _is_repo_relative(entry):
                findings.append({"severity": "error", "code": "non_portable_path", "detail": f"{collection_name}:{entry}"})

    for forbidden in manifest.get("forbidden_paths", []):
        if forbidden in manifest.get("allowed_roots", []):
            findings.append({"severity": "error", "code": "forbidden_allowed_overlap", "detail": forbidden})

    for required_file in manifest.get("required_files", []):
        if not (root / required_file).exists():
            findings.append({"severity": "error", "code": "required_file_missing", "detail": required_file})

    policy = manifest.get("secrets_policy", {})
    for key in ("ships_secrets", "ships_oauth_tokens", "ships_sessions", "ships_logs", "ships_memories"):
        if policy.get(key) is not False:
            findings.append({"severity": "error", "code": "secrets_policy_not_false", "detail": key})
    return findings


def validate_distribution(
    distribution: dict[str, Any],
    manifest: dict[str, Any],
    installed_profile_name: str | None = None,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for key in ("name", "version", "description", "hermes_requires", "env_requires", "distribution_owned"):
        if key not in distribution:
            findings.append({"severity": "error", "code": "distribution_missing_key", "detail": key})

    accepted_names = {manifest.get("name")}
    if installed_profile_name:
        accepted_names.add(installed_profile_name)
    if distribution.get("name") not in accepted_names:
        findings.append({"severity": "error", "code": "distribution_name_mismatch", "detail": str(distribution.get("name"))})
    if distribution.get("version") != manifest.get("version"):
        findings.append({"severity": "error", "code": "distribution_version_mismatch", "detail": str(distribution.get("version"))})

    env_requires = distribution.get("env_requires", [])
    for item in env_requires:
        if not isinstance(item, dict) or not {"name", "description", "required"}.issubset(item):
            findings.append({"severity": "error", "code": "distribution_env_requires_shape", "detail": str(item)})
            continue
        if not re.match(r"^[A-Z0-9_]+$", str(item.get("name", ""))):
            findings.append({"severity": "error", "code": "distribution_env_name", "detail": str(item.get("name"))})

    local_credentials = set(manifest.get("local_credentials", []))
    distribution_env = {item.get("name") for item in env_requires if isinstance(item, dict)}
    for env_name in distribution_env:
        if env_name not in local_credentials:
            findings.append({"severity": "warning", "code": "env_not_listed_in_manifest", "detail": str(env_name)})

    for owned in distribution.get("distribution_owned", []):
        if not isinstance(owned, str) or not _is_repo_relative(owned):
            findings.append({"severity": "error", "code": "distribution_non_portable_owned_path", "detail": str(owned)})
        if owned in FORBIDDEN_REAL_ENV:
            findings.append({"severity": "error", "code": "distribution_forbidden_owned_path", "detail": owned})
    return findings


def scan_portable_files(root: Path, manifest: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    allowed_roots = manifest.get("allowed_roots", [])
    for rel in allowed_roots:
        path = root / rel
        if not path.exists():
            continue
        files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()]
        for file_path in files:
            if file_path.suffix in {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".gz"}:
                continue
            if file_path.name == ".env.EXAMPLE":
                continue
            try:
                text = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            rel_path = file_path.relative_to(root).as_posix()
            if WINDOWS_PATH_RE.search(text) or any(ABSOLUTE_POSIX_RE.search(line.strip()) for line in text.splitlines()):
                findings.append({"severity": "error", "code": "non_portable_content", "detail": rel_path})
            if SECRET_VALUE_RE.search(text):
                findings.append({"severity": "error", "code": "secret_like_content", "detail": rel_path})
    return findings


def run(root: Path = REPO_ROOT) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    manifest_path = root / "digital-state.manifest.json"
    distribution_path = root / "distribution.yaml"

    if not manifest_path.exists():
        findings.append({"severity": "error", "code": "manifest_missing", "detail": str(manifest_path)})
        manifest: dict[str, Any] = {}
    else:
        try:
            manifest = _read_json(manifest_path)
        except Exception as exc:
            manifest = {}
            findings.append({"severity": "error", "code": "manifest_parse_error", "detail": str(exc)})

    if not distribution_path.exists():
        findings.append({"severity": "error", "code": "distribution_missing", "detail": str(distribution_path)})
        distribution: dict[str, Any] = {}
    else:
        try:
            distribution = _simple_yaml_load(distribution_path)
        except Exception as exc:
            distribution = {}
            findings.append({"severity": "error", "code": "distribution_parse_error", "detail": str(exc)})

    if manifest:
        findings.extend(validate_manifest(manifest, root=root))
        findings.extend(scan_portable_files(root, manifest))
    if manifest and distribution:
        findings.extend(validate_distribution(distribution, manifest, installed_profile_name=root.name))

    ok = not any(item["severity"] == "error" for item in findings)
    return {
        "ok": ok,
        "profile_distribution": distribution.get("name") if distribution else None,
        "manifest": manifest.get("name") if manifest else None,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Hermes Digital State distribution readiness")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument("--root", default=str(REPO_ROOT), help="Workspace root to validate")
    args = parser.parse_args(argv)

    result = run(Path(args.root).resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "OK" if result["ok"] else "FAILED"
        print(f"Digital State bootstrap: {status}")
        for finding in result["findings"]:
            print(f"- {finding['severity']}: {finding['code']}: {finding['detail']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
