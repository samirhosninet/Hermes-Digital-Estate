#!/usr/bin/env python3
"""Eight-layer preflight check engine for Hermes Digital State.

Every function returns a dict with at least:
    {"status": "pass"|"warn"|"fail", "label": str, "detail": str}

Stdlib-only — no pip dependencies.
"""
from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(cmd: list[str], timeout: int = 15) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except FileNotFoundError:
        return -1, ""
    except subprocess.TimeoutExpired:
        return -2, "timeout"


def _version_tuple(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3])


def _check(status: str, label: str, detail: str = "", fix: str = "") -> dict:
    d: dict[str, str] = {"status": status, "label": label, "detail": detail}
    if fix:
        d["fix"] = fix
    return d

# ---------------------------------------------------------------------------
# Layer 1 — System Tools
# ---------------------------------------------------------------------------

def check_system() -> list[dict]:
    results: list[dict] = []
    os_name = platform.system()

    # Python
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 10):
        results.append(_check("pass", "Python", py_ver))
    else:
        results.append(_check("fail", "Python", py_ver, "https://python.org/downloads/"))

    # Git
    rc, out = _run(["git", "--version"])
    if rc == 0:
        ver = re.search(r"(\d+\.\d+[\.\d]*)", out)
        results.append(_check("pass", "Git", ver.group(1) if ver else out))
    else:
        fix = "https://git-scm.com/downloads"
        results.append(_check("fail", "Git", "not found", fix))

    # Node.js (optional)
    rc, out = _run(["node", "--version"])
    if rc == 0:
        results.append(_check("pass", "Node.js", out.strip().lstrip("v") + " (optional)"))
    else:
        results.append(_check("warn", "Node.js", "not found (optional — for Workspace)", "https://nodejs.org/"))

    # pnpm (optional)
    rc, out = _run(["pnpm", "--version"])
    if rc == 0:
        results.append(_check("pass", "pnpm", out.strip() + " (optional)"))
    else:
        results.append(_check("warn", "pnpm", "not found (optional)", "npm install -g pnpm"))

    return results

# ---------------------------------------------------------------------------
# Layer 2 — Hermes Agent
# ---------------------------------------------------------------------------

def _hermes_home() -> Path | None:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env)
    if platform.system() == "Windows":
        local = os.environ.get("LOCALAPPDATA", "")
        p = Path(local) / "hermes"
        if p.is_dir():
            return p
    home = Path.home() / ".hermes"
    return home if home.is_dir() else None


def check_hermes() -> list[dict]:
    results: list[dict] = []
    hermes_bin = shutil.which("hermes")

    if hermes_bin:
        results.append(_check("pass", "hermes CLI", str(hermes_bin)))
    else:
        install = ("curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
                    if platform.system() != "Windows" else
                    "irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex")
        results.append(_check("fail", "hermes CLI", "not found", install))
        return results

    # Version
    rc, out = _run(["hermes", "--version"])
    if rc == 0:
        ver_match = re.search(r"(\d+\.\d+[\.\d]*)", out)
        if ver_match:
            ver = ver_match.group(1)
            req = "0.12.0"
            if _version_tuple(ver) >= _version_tuple(req):
                results.append(_check("pass", "Hermes version", f"{ver} (requires >={req})"))
            else:
                results.append(_check("fail", "Hermes version", f"{ver} (requires >={req})", "hermes self-update"))
        else:
            results.append(_check("warn", "Hermes version", f"could not parse: {out}"))
    else:
        results.append(_check("warn", "Hermes version", "could not determine"))

    # Home directory
    home = _hermes_home()
    if home:
        results.append(_check("pass", "HERMES_HOME", str(home)))
    else:
        results.append(_check("warn", "HERMES_HOME", "not found"))

    return results

# ---------------------------------------------------------------------------
# Layer 3 — Digital State Files
# ---------------------------------------------------------------------------

def check_governance() -> list[dict]:
    results: list[dict] = []

    # Manifest
    manifest_path = REPO_ROOT / "digital-state.manifest.json"
    if not manifest_path.exists():
        results.append(_check("fail", "manifest.json", "MISSING"))
        return results

    try:
        manifest = json.loads(manifest_path.read_text("utf-8"))
    except Exception as e:
        results.append(_check("fail", "manifest.json", f"parse error: {e}"))
        return results

    # Required files
    req_files = manifest.get("required_files", [])
    present = sum(1 for f in req_files if (REPO_ROOT / f).exists())
    if present == len(req_files):
        results.append(_check("pass", "Required files", f"{present}/{len(req_files)}"))
    else:
        missing = [f for f in req_files if not (REPO_ROOT / f).exists()]
        results.append(_check("fail", "Required files", f"{present}/{len(req_files)} — missing: {', '.join(missing[:3])}"))

    # SOUL.md
    soul_path = REPO_ROOT / "SOUL.md"
    if soul_path.exists():
        soul = soul_path.read_text("utf-8")
        keywords = ["portable", "governance", "official Hermes Agent", "Secrets are local", "evidence-oriented", "Spec Kit"]
        found = sum(1 for kw in keywords if kw in soul)
        if found == len(keywords):
            results.append(_check("pass", "SOUL.md integrity", f"{found}/{len(keywords)} principles"))
        else:
            results.append(_check("fail", "SOUL.md integrity", f"{found}/{len(keywords)} principles"))
    else:
        results.append(_check("fail", "SOUL.md", "MISSING"))

    # config.yaml — count ministries
    cfg_path = REPO_ROOT / "config.yaml"
    if cfg_path.exists():
        cfg = cfg_path.read_text("utf-8")
        ministries = re.findall(r"^\s{4,}\w.*-(?:ministry|office|services|planning):", cfg, re.MULTILINE)
        results.append(_check("pass", "config.yaml", f"{len(ministries)} ministries"))
    else:
        results.append(_check("fail", "config.yaml", "MISSING"))

    # distribution.yaml consistency
    dist_path = REPO_ROOT / "distribution.yaml"
    if dist_path.exists():
        dist = dist_path.read_text("utf-8")
        dist_ver = re.search(r"version:\s*(.+)", dist)
        manifest_ver = manifest.get("version", "")
        dv = dist_ver.group(1).strip().strip("\"'") if dist_ver else ""
        if dv == manifest_ver:
            results.append(_check("pass", "distribution.yaml", f"v{dv} matches manifest"))
        else:
            results.append(_check("fail", "distribution.yaml", f"version mismatch: dist={dv} manifest={manifest_ver}"))
    else:
        results.append(_check("fail", "distribution.yaml", "MISSING"))

    # Count governance docs, specs, scripts, skills, tests
    gov_docs = list((REPO_ROOT / "docs" / "governance").glob("*.md")) if (REPO_ROOT / "docs" / "governance").is_dir() else []
    results.append(_check("pass", "docs/governance/", f"{len(gov_docs)} documents"))

    spec_dirs = [d for d in (REPO_ROOT / "specs").iterdir() if d.is_dir()] if (REPO_ROOT / "specs").is_dir() else []
    results.append(_check("pass", "specs/", f"{len(spec_dirs)} specifications"))

    gov_scripts = list((REPO_ROOT / "scripts" / "governance").glob("*.py")) if (REPO_ROOT / "scripts" / "governance").is_dir() else []
    results.append(_check("pass", "scripts/governance/", f"{len(gov_scripts)} scripts"))

    import glob
    test_files = glob.glob(str(REPO_ROOT / "tests" / "**" / "test_*.py"), recursive=True)
    results.append(_check("pass", "tests/", f"{len(test_files)} test files"))

    return results

# ---------------------------------------------------------------------------
# Layer 4 — Credentials
# ---------------------------------------------------------------------------

def check_credentials() -> list[dict]:
    results: list[dict] = []

    dist_path = REPO_ROOT / "distribution.yaml"
    if not dist_path.exists():
        results.append(_check("fail", ".env check", "distribution.yaml missing"))
        return results

    # Parse env_requires from distribution.yaml
    env_requires: list[dict[str, Any]] = []
    dist_text = dist_path.read_text("utf-8")
    current_item: dict[str, Any] | None = None
    in_env = False
    for line in dist_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("env_requires"):
            in_env = True
            continue
        if in_env and not line.startswith(" "):
            break
        if in_env and stripped.startswith("- name:"):
            if current_item:
                env_requires.append(current_item)
            current_item = {"name": stripped.split(":", 1)[1].strip()}
        elif in_env and current_item and stripped.startswith("required:"):
            val = stripped.split(":", 1)[1].strip()
            current_item["required"] = val.lower() == "true"
    if current_item:
        env_requires.append(current_item)

    # Check .env in multiple locations
    env_paths = [
        REPO_ROOT / ".env",
        Path.home() / ".hermes" / ".env",
    ]
    hermes_home = _hermes_home()
    if hermes_home:
        env_paths.append(hermes_home / ".env")

    env_vars: dict[str, str] = {}
    env_file_found = None
    for ep in env_paths:
        if ep.exists():
            env_file_found = ep
            for line in ep.read_text("utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
            break

    if env_file_found:
        results.append(_check("pass", ".env file", str(env_file_found)))
    else:
        results.append(_check("warn", ".env file", "not found — credentials not configured yet"))

    for item in env_requires:
        name = item.get("name", "")
        required = item.get("required", False)
        val = env_vars.get(name, "")
        placeholder_patterns = ["your-", "your_", "xxx", "placeholder"]
        is_placeholder = any(p in val.lower() for p in placeholder_patterns) if val else False

        if val and not is_placeholder:
            results.append(_check("pass", name, f"set ({len(val)} chars)"))
        elif required:
            results.append(_check("fail", name, "required but not set"))
        else:
            results.append(_check("warn", name, "not set (optional)"))

    return results

# ---------------------------------------------------------------------------
# Layer 5 — Network & Services
# ---------------------------------------------------------------------------

def _http_ok(url: str, timeout: int = 5) -> tuple[bool, str]:
    try:
        req = Request(url, headers={"User-Agent": "HermesWizard/1.0"})
        resp = urlopen(req, timeout=timeout)
        return True, str(resp.status)
    except URLError as e:
        return False, str(e.reason)
    except Exception as e:
        return False, str(e)


def check_network(offline: bool = False) -> list[dict]:
    results: list[dict] = []

    if offline:
        results.append(_check("warn", "Network", "offline mode — skipped"))
        return results

    github_repos = [
        ("NousResearch/hermes-agent", "https://github.com/NousResearch/hermes-agent"),
        ("outsourc-e/hermes-workspace", "https://github.com/outsourc-e/hermes-workspace"),
        ("samirhosninet/Hermes-Digital-Estate", "https://github.com/samirhosninet/Hermes-Digital-Estate"),
    ]
    for name, url in github_repos:
        ok, detail = _http_ok(url, timeout=8)
        if ok:
            results.append(_check("pass", f"GitHub: {name}", "reachable"))
        else:
            results.append(_check("warn", f"GitHub: {name}", detail))

    # Local services
    gw_ok, gw_d = _http_ok("http://127.0.0.1:8642/health", timeout=3)
    if gw_ok:
        results.append(_check("pass", "Hermes Gateway", "responding"))
    else:
        results.append(_check("warn", "Hermes Gateway (:8642)", "not responding", "hermes gateway run"))

    db_ok, db_d = _http_ok("http://127.0.0.1:9119/api/status", timeout=3)
    if db_ok:
        results.append(_check("pass", "Hermes Dashboard", "responding"))
    else:
        results.append(_check("warn", "Hermes Dashboard (:9119)", "not responding", "hermes dashboard"))

    return results

# ---------------------------------------------------------------------------
# Layer 6 — Deep Audit
# ---------------------------------------------------------------------------

def check_audit() -> list[dict]:
    results: list[dict] = []

    # audit.py
    audit_path = REPO_ROOT / "audit.py"
    if audit_path.exists():
        rc, out = _run([sys.executable, str(audit_path)], timeout=60)
        pass_m = re.search(r"\[PASS\]\s*:\s*(\d+)", out)
        fail_m = re.search(r"\[FAIL\]\s*:\s*(\d+)", out)
        p = int(pass_m.group(1)) if pass_m else 0
        f = int(fail_m.group(1)) if fail_m else -1
        if f == 0:
            results.append(_check("pass", "audit.py", f"{p} PASS / {f} FAIL"))
        else:
            results.append(_check("fail", "audit.py", f"{p} PASS / {f} FAIL"))
    else:
        results.append(_check("fail", "audit.py", "MISSING"))

    # Unit tests
    test_cmd = [
        sys.executable, "-m", "unittest",
        "tests.scripts.test_digital_state_distribution",
        "tests.scripts.test_governance_portability",
        "tests.scripts.test_governance_status",
        "tests.agent.test_runtime_governance",
        "tests.scripts.test_runtime_guard_schema",
        "tests.scripts.test_model_benchmark",
        "tests.scripts.test_approval_flow_interaction",
        "tests.scripts.test_log_only_implementation_gate",
        "tests.scripts.test_model_ministry_routing",
        "tests.scripts.test_operator_approval_record",
        "tests.scripts.test_runtime_guard_scenarios",
        "tests.scripts.test_terminal_hook_contract",
    ]
    rc, out = _run(test_cmd, timeout=120)
    ran_m = re.search(r"Ran (\d+) tests?", out)
    count = int(ran_m.group(1)) if ran_m else 0
    if rc == 0 and count > 0:
        results.append(_check("pass", "Test Suite", f"{count} tests OK"))
    else:
        results.append(_check("fail", "Test Suite", f"exit={rc}, ran={count}"))

    # Portability
    port_script = REPO_ROOT / "scripts" / "governance" / "check_portability.py"
    if port_script.exists():
        targets = "docs specs scripts tests agent skills SOUL.md config.yaml distribution.yaml"
        rc, out = _run([sys.executable, str(port_script)] + targets.split(), timeout=30)
        try:
            data = json.loads(out)
            scanned = data.get("scanned_files", "?")
            portable = data.get("portable", False)
            if portable:
                results.append(_check("pass", "Portability", f"{scanned} files — portable"))
            else:
                results.append(_check("fail", "Portability", f"{scanned} files — violations found"))
        except json.JSONDecodeError:
            results.append(_check("warn", "Portability", "could not parse output"))
    else:
        results.append(_check("fail", "Portability scanner", "MISSING"))

    return results

# ---------------------------------------------------------------------------
# Layer 7 — Cross-Repo Consistency (renamed from Layer 8)
# ---------------------------------------------------------------------------

def check_consistency() -> list[dict]:
    results: list[dict] = []

    # Git remote
    rc, out = _run(["git", "-C", str(REPO_ROOT), "remote", "get-url", "origin"])
    if rc == 0 and out:
        results.append(_check("pass", "Git remote origin", out.strip()))
    else:
        results.append(_check("warn", "Git remote origin", "not configured"))

    # Tags
    rc, out = _run(["git", "-C", str(REPO_ROOT), "tag", "--list"])
    tags = [t.strip() for t in out.splitlines() if t.strip()]
    if tags:
        results.append(_check("pass", "Git tags", ", ".join(tags[-3:])))
    else:
        results.append(_check("warn", "Git tags", "none"))

    return results

# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------

ALL_LAYERS = [
    ("System Tools", check_system),
    ("Hermes Agent", check_hermes),
    ("Digital State Files", check_governance),
    ("Credentials", check_credentials),
    ("Network & Services", lambda: check_network(offline=False)),
    ("Deep Audit", check_audit),
    ("Consistency", check_consistency),
]


def run_all(*, offline: bool = False) -> dict[str, Any]:
    layers = list(ALL_LAYERS)
    if offline:
        layers[4] = ("Network & Services", lambda: check_network(offline=True))

    report: dict[str, Any] = {"layers": [], "summary": {"pass": 0, "warn": 0, "fail": 0}}
    for name, fn in layers:
        items = fn()
        for item in items:
            report["summary"][item["status"]] += 1
        report["layers"].append({"name": name, "checks": items})

    report["summary"]["total"] = sum(report["summary"].values())
    report["summary"]["ready"] = report["summary"]["fail"] == 0
    return report
