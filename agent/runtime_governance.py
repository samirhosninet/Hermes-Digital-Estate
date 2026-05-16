"""Pure runtime governance decision core for Hermes digital-state planning.

This module is intentionally not wired into Hermes tool dispatch yet. It gives
Feature 002 a small, testable policy/parser/classifier/audit core that future
runtime hooks can call only after a separate approval and integration pass.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import shlex
from pathlib import Path
import re
from typing import Any, Mapping


_ALLOWED_DECISIONS = {"allow", "deny", "escalate", "fail_closed"}
_SECRET_PATH_MARKERS = (
    ".env",
    "auth.json",
    "credential",
    "credentials",
    "token",
    "tokens",
    "cookie",
    "cookies",
    "private_key",
    "id_rsa",
    "id_ed25519",
)
_SECRET_TEXT_PATTERNS = (
    re.compile(r"Bearer\s+\S+", re.IGNORECASE),
    re.compile(r"sk-[A-Za-z0-9._-]+"),
    re.compile(r"(?i)(api[_-]?key|token|password|secret)=([^\s'\"]+)"),
)
_BOUNDARY_RISK = {
    "terminal": "R0",
    "file": "R1",
    "package": "R2",
    "git_destructive": "R3",
    "network_deployment": "R3",
    "gateway": "R3",
    "cron_webhook": "R3",
    "model_routing": "R2",
    "credential": "R4",
}


@dataclass(frozen=True)
class GuardDecision:
    decision: str
    reason: str
    risk_class: str
    boundary: str
    policy_loaded: bool
    policy_version: str | None
    action_summary: str
    action_hash: str


class RuntimeGovernanceGuard:
    """Evaluate proposed actions against a portable dry-run governance policy."""

    def __init__(
        self,
        policy: Mapping[str, Any] | None,
        *,
        policy_loaded: bool,
        load_error: str | None = None,
        strict: bool = True,
    ) -> None:
        self.policy = dict(policy or {})
        self.policy_loaded = policy_loaded
        self.load_error = load_error
        self.strict = strict

    @classmethod
    def from_policy_file(cls, path: str | Path, *, strict: bool = True) -> "RuntimeGovernanceGuard":
        policy_path = Path(path)
        if not policy_path.exists():
            return cls(None, policy_loaded=False, load_error="policy_missing", strict=strict)
        try:
            raw = policy_path.read_text(encoding="utf-8")
            policy = json.loads(raw)
        except json.JSONDecodeError:
            return cls(None, policy_loaded=False, load_error="policy_malformed", strict=strict)
        except OSError:
            return cls(None, policy_loaded=False, load_error="policy_unreadable", strict=strict)

        if not isinstance(policy, dict):
            return cls(None, policy_loaded=False, load_error="policy_malformed", strict=strict)
        if policy.get("schema_version") != "runtime-guard-policy-v1":
            return cls(None, policy_loaded=False, load_error="policy_unsupported_schema", strict=strict)
        default_decision = policy.get("default_decision", "escalate")
        if default_decision not in _ALLOWED_DECISIONS - {"fail_closed"}:
            return cls(None, policy_loaded=False, load_error="policy_malformed", strict=strict)
        rules = policy.get("rules")
        if not isinstance(rules, list) or not rules:
            return cls(None, policy_loaded=False, load_error="policy_malformed", strict=strict)
        return cls(policy, policy_loaded=True, strict=strict)

    def evaluate(self, action: Mapping[str, Any]) -> GuardDecision:
        boundary = str(action.get("boundary") or "unknown")
        summary = _summarize_action(action)
        action_hash = hashlib.sha256(summary.encode("utf-8")).hexdigest()

        if not self.policy_loaded and self.strict:
            return GuardDecision(
                decision="fail_closed",
                reason=self.load_error or "policy_unavailable",
                risk_class="R5",
                boundary=boundary,
                policy_loaded=False,
                policy_version=None,
                action_summary=_redact(summary),
                action_hash=action_hash,
            )

        path = str(action.get("path") or "")
        if _is_secret_path(path) or boundary in {"credential", "credentials"}:
            return self._decision("deny", "secret_path", "R4", boundary, summary, action_hash)

        command = str(action.get("command") or "")
        normalized_command = command.lower()
        if _looks_destructive_git(normalized_command):
            return self._decision("escalate", "git_destructive", "R3", "git_destructive", summary, action_hash)

        matched = self._match_rule(action, boundary)
        if matched is not None and matched.get("decision") == "allow":
            return self._decision(
                "allow",
                "read_only_allowed",
                str(matched.get("risk_class", "R0")),
                boundary,
                summary,
                action_hash,
            )
        if matched is not None and matched.get("decision") == "escalate":
            return self._decision(
                "escalate",
                "boundary_requires_approval",
                str(matched.get("risk_class", _BOUNDARY_RISK.get(boundary, "R2"))),
                boundary,
                summary,
                action_hash,
            )

        escalate_boundaries = set(self.policy.get("escalate_boundaries", [])) | {"package"}
        if boundary in escalate_boundaries:
            return self._decision(
                "escalate",
                "boundary_requires_approval",
                _BOUNDARY_RISK.get(boundary, "R2"),
                boundary,
                summary,
                action_hash,
            )

        if bool(action.get("read_only")) and bool(self.policy.get("allow_read_only", False)):
            return self._decision("allow", "read_only_allowed", "R0", boundary, summary, action_hash)

        default_decision = str(self.policy.get("default_decision", "escalate"))
        if default_decision not in _ALLOWED_DECISIONS:
            default_decision = "fail_closed"
        risk = _BOUNDARY_RISK.get(boundary, "R2")
        return self._decision(default_decision, "default_policy", risk, boundary, summary, action_hash)

    def build_audit_record(self, decision: GuardDecision, *, actor: str = "assistant") -> dict[str, Any]:
        return {
            "schema_version": "runtime-guard-audit-record-v1",
            "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "actor": actor,
            "policy_version": decision.policy_version or "unknown",
            "policy_loaded": decision.policy_loaded,
            "boundary": decision.boundary,
            "risk_class": decision.risk_class,
            "decision": decision.decision,
            "reason": decision.reason,
            "redacted_action_summary": decision.action_summary,
            "action_hash": decision.action_hash,
            "secret_redaction_applied": "[REDACTED]" in decision.action_summary,
            "approval_reference": None,
        }

    def _match_rule(self, action: Mapping[str, Any], boundary: str) -> Mapping[str, Any] | None:
        for rule in self.policy.get("rules", []):
            if not isinstance(rule, Mapping):
                continue
            if str(rule.get("boundary")) != boundary:
                continue
            match = rule.get("match")
            if not isinstance(match, Mapping):
                continue
            if match.get("command_class") == "read_only" and bool(action.get("read_only")):
                return rule
            if bool(match.get("changes_lockfile")) and boundary == "package":
                return rule
            if bool(match.get("secret_path")) and _is_secret_path(str(action.get("path") or "")):
                return rule
        return None

    def _decision(
        self,
        decision: str,
        reason: str,
        risk_class: str,
        boundary: str,
        summary: str,
        action_hash: str,
    ) -> GuardDecision:
        return GuardDecision(
            decision=decision,
            reason=reason,
            risk_class=risk_class,
            boundary=boundary,
            policy_loaded=self.policy_loaded,
            policy_version=self.policy.get("policy_version") or self.policy.get("policy_id"),
            action_summary=_redact(summary),
            action_hash=action_hash,
        )


def build_terminal_dry_run_action(command: str) -> dict[str, Any]:
    """Classify a proposed terminal command without executing it.

    This is a dry-run adapter for Feature 002. It returns the action shape that
    RuntimeGovernanceGuard.evaluate can consume later, but it is intentionally
    not wired into tools/terminal execution.
    """
    command_text = str(command).strip()
    lowered = command_text.lower()
    command_class = _classify_terminal_command(lowered)
    boundary = {
        "git_destructive": "git_destructive",
        "package_mutation": "package",
    }.get(command_class, "terminal")
    return {
        "boundary": boundary,
        "operation": "dry_run_terminal_classification",
        "command": command_text,
        "read_only": command_class == "read_only",
        "command_class": command_class,
    }


def _classify_terminal_command(lowered_command: str) -> str:
    if _looks_destructive_git(lowered_command):
        return "git_destructive"
    try:
        parts = shlex.split(lowered_command)
    except ValueError:
        parts = lowered_command.split()
    if not parts:
        return "unknown"
    if _looks_package_mutation(parts):
        return "package_mutation"
    if _looks_read_only_command(parts):
        return "read_only"
    return "unknown"


def _looks_package_mutation(parts: list[str]) -> bool:
    if parts[:2] in (["pip", "install"], ["pip", "uninstall"], ["uv", "add"], ["uv", "remove"], ["poetry", "add"], ["poetry", "remove"]):
        return True
    if parts[:2] in (["npm", "install"], ["npm", "uninstall"], ["pnpm", "add"], ["pnpm", "remove"], ["yarn", "add"], ["yarn", "remove"]):
        return True
    return False


def _looks_read_only_command(parts: list[str]) -> bool:
    read_only_commands = {
        "pwd",
        "ls",
        "find",
        "grep",
        "rg",
        "git",
        "python",
        "python3",
        "date",
        "whoami",
        "uname",
        "df",
        "du",
        "ps",
    }
    if parts[0] not in read_only_commands:
        return False
    if parts[0] == "git" and len(parts) > 1:
        return parts[1] in {"status", "diff", "log", "show", "branch"}
    if parts[0] in {"python", "python3"}:
        return "-m" in parts or "--version" in parts or "-V" in parts
    return True


def _summarize_action(action: Mapping[str, Any]) -> str:
    parts = []
    for key in ("boundary", "operation", "path", "command"):
        if action.get(key) is not None:
            parts.append(f"{key}={action[key]}")
    return "; ".join(parts) or "action=unspecified"


def _is_secret_path(path: str) -> bool:
    normalized = path.lower().replace("\\", "/")
    return any(marker in normalized for marker in _SECRET_PATH_MARKERS)


def _looks_destructive_git(command: str) -> bool:
    return any(
        marker in command
        for marker in (
            "git reset --hard",
            "git push --force",
            "git push -f",
            "git rebase",
            "git remote add",
            "git remote set-url",
        )
    )


def _reason_for_rule(rule: Mapping[str, Any]) -> str:
    rule_id = str(rule.get("id") or "")
    if rule_id.startswith("allow-read-only"):
        return "read_only_allowed"
    if rule_id.startswith("escalate-package"):
        return "boundary_requires_approval"
    if rule_id.startswith("deny-credential"):
        return "secret_path"
    decision = str(rule.get("decision") or "")
    return f"rule_{decision}" if decision else "rule_matched"


def _redact(text: str) -> str:
    redacted = text
    for pattern in _SECRET_TEXT_PATTERNS:
        redacted = pattern.sub(lambda match: match.group(0).split()[0] + " [REDACTED]" if "Bearer" in match.group(0) else "[REDACTED]", redacted)
    return redacted
