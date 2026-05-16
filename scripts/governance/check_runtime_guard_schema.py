#!/usr/bin/env python3
"""Lightweight stdlib validator for Feature 002 runtime guard design fixtures.

This is intentionally not runtime enforcement. It only checks the design-time
schemas/fixtures are internally consistent and fail closed on malformed inputs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BOUNDARIES = {"terminal", "file", "package", "git", "git_destructive", "network", "credentials", "model_routing", "gateway", "cron_webhook", "unknown"}
RISK_CLASSES = {"R0", "R1", "R2", "R3", "R4", "R5", "unknown"}
DECISIONS = {"allow", "deny", "escalate", "fail_closed"}
POLICY_MODES = {"design_only", "dry_run", "strict"}
COMMAND_CLASSES = {"read_only", "package_mutation", "git_destructive", "unknown"}


def fail(message: str) -> int:
    print(json.dumps({"ok": False, "error": message}, indent=2, sort_keys=True))
    return 2


def ok(kind: str, path: Path) -> int:
    print(json.dumps({"ok": True, "kind": kind, "path": str(path)}, indent=2, sort_keys=True))
    return 0


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed JSON: {exc.msg}")


def require(data: dict, fields: set[str]) -> None:
    missing = sorted(fields - set(data))
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")


def validate_policy(data: dict) -> None:
    require(data, {"schema_version", "mode", "default_decision", "rules"})
    if data["schema_version"] != "runtime-guard-policy-v1":
        raise ValueError("schema_version must be runtime-guard-policy-v1")
    if data["mode"] not in POLICY_MODES:
        raise ValueError("mode is invalid")
    if data["default_decision"] not in {"deny", "escalate", "fail_closed"}:
        raise ValueError("default_decision must be deny, escalate, or fail_closed")
    rules = data["rules"]
    if not isinstance(rules, list) or not rules:
        raise ValueError("rules must be a non-empty list")
    for idx, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError(f"rules[{idx}] must be object")
        require(rule, {"id", "boundary", "risk_class", "decision"})
        if rule["boundary"] not in BOUNDARIES - {"unknown"}:
            raise ValueError(f"rules[{idx}].boundary is invalid")
        if rule["risk_class"] not in RISK_CLASSES - {"unknown"}:
            raise ValueError(f"rules[{idx}].risk_class is invalid")
        if rule["decision"] not in DECISIONS:
            raise ValueError(f"rules[{idx}].decision is invalid")


def validate_decision(data: dict) -> None:
    require(data, {"schema_version", "decision", "boundary", "risk_class", "reason", "policy_version"})
    if data["schema_version"] != "runtime-guard-decision-v1":
        raise ValueError("schema_version must be runtime-guard-decision-v1")
    if data["decision"] not in DECISIONS:
        raise ValueError("decision is invalid")
    if data["boundary"] not in BOUNDARIES:
        raise ValueError("boundary is invalid")
    if data["risk_class"] not in RISK_CLASSES:
        raise ValueError("risk_class is invalid")
    if not str(data["reason"]).strip():
        raise ValueError("reason must be non-empty")


def validate_audit(data: dict) -> None:
    require(data, {"schema_version", "timestamp_utc", "boundary", "risk_class", "decision", "actor", "policy_version", "action_hash", "redacted_action_summary"})
    if data["schema_version"] != "runtime-guard-audit-record-v1":
        raise ValueError("schema_version must be runtime-guard-audit-record-v1")
    if data["decision"] not in DECISIONS:
        raise ValueError("decision is invalid")
    if data["boundary"] not in BOUNDARIES:
        raise ValueError("boundary is invalid")
    if data["risk_class"] not in RISK_CLASSES:
        raise ValueError("risk_class is invalid")
    summary = str(data["redacted_action_summary"])
    lowered = summary.lower()
    if any(token in lowered for token in ("api_key", "bearer ", "password", "private key", "oauth")):
        raise ValueError("redacted_action_summary appears to contain secret material")


def validate_action(data: dict) -> None:
    require(data, {"boundary", "operation", "command", "read_only", "command_class"})
    if data["operation"] != "dry_run_terminal_classification":
        raise ValueError("operation must be dry_run_terminal_classification")
    if data["boundary"] not in BOUNDARIES:
        raise ValueError("boundary is invalid")
    if data["command_class"] not in COMMAND_CLASSES:
        raise ValueError("command_class is invalid")
    if not isinstance(data["read_only"], bool):
        raise ValueError("read_only must be boolean")
    if data["command_class"] == "read_only" and data["read_only"] is not True:
        raise ValueError("read_only command_class must set read_only true")
    if data["command_class"] != "read_only" and data["read_only"] is not False:
        raise ValueError("mutating or unknown command_class must set read_only false")
    if not str(data["command"]).strip():
        raise ValueError("command must be non-empty")


def validate_terminal_hook_contract(data: dict) -> None:
    require(data, {
        "schema_version",
        "mode",
        "runtime_enforcement_enabled",
        "changes_terminal_execution_flow",
        "may_block_commands",
        "requires_existing_approval_flow",
        "required_evidence_before_integration",
        "rollback",
    })
    if data["schema_version"] != "terminal-hook-dry-run-contract-v1":
        raise ValueError("schema_version must be terminal-hook-dry-run-contract-v1")
    if data["mode"] != "dry_run_log_only":
        raise ValueError("mode must be dry_run_log_only")
    if data["runtime_enforcement_enabled"] is not False:
        raise ValueError("runtime_enforcement_enabled must be false")
    if data["changes_terminal_execution_flow"] is not False:
        raise ValueError("changes_terminal_execution_flow must be false")
    if data["may_block_commands"] is not False:
        raise ValueError("may_block_commands must be false")
    if data["requires_existing_approval_flow"] is not True:
        raise ValueError("requires_existing_approval_flow must be true")
    evidence = data["required_evidence_before_integration"]
    if not isinstance(evidence, list) or len(set(evidence)) != len(evidence):
        raise ValueError("required_evidence_before_integration must be a unique list")
    required = {"unit_tests", "dry_run_audit_sample", "operator_approval_matrix", "portability_check", "secret_redaction_test"}
    if not required.issubset(set(evidence)):
        raise ValueError("required_evidence_before_integration is incomplete")
    if data["rollback"] != "remove_hook_call_or_disable_config_flag":
        raise ValueError("rollback is invalid")


def validate_approval_flow_contract(data: dict) -> None:
    require(data, {
        "schema_version",
        "mode",
        "runtime_enforcement_enabled",
        "duplicates_approval_prompt",
        "bypasses_existing_approval",
        "changes_terminal_execution_flow",
        "may_block_commands",
        "required_interaction_events",
        "disable_flag",
        "audit_failure_behavior",
        "approval_failure_behavior",
    })
    if data["schema_version"] != "approval-flow-interaction-contract-v1":
        raise ValueError("schema_version must be approval-flow-interaction-contract-v1")
    if data["mode"] != "dry_run_log_only":
        raise ValueError("mode must be dry_run_log_only")
    for field in ("runtime_enforcement_enabled", "duplicates_approval_prompt", "bypasses_existing_approval", "changes_terminal_execution_flow", "may_block_commands"):
        if data[field] is not False:
            raise ValueError(f"{field} must be false")
    events = data["required_interaction_events"]
    if not isinstance(events, list) or len(set(events)) != len(events):
        raise ValueError("required_interaction_events must be a unique list")
    required_events = {
        "proposed_terminal_action",
        "governance_dry_run_decision",
        "existing_approval_flow_observed",
        "terminal_execution_continues_unchanged",
        "redacted_audit_record_written_or_buffered",
    }
    if not required_events.issubset(set(events)):
        raise ValueError("required_interaction_events is incomplete")
    if data["disable_flag"] != "governance.terminal_dry_run_enabled=false":
        raise ValueError("disable_flag is invalid")
    if data["audit_failure_behavior"] != "continue_terminal_flow_and_record_local_error":
        raise ValueError("audit_failure_behavior is invalid")
    if data["approval_failure_behavior"] != "defer_to_existing_approval_flow":
        raise ValueError("approval_failure_behavior is invalid")


def validate_log_only_implementation_gate(data: dict) -> None:
    require(data, {
        "schema_version",
        "mode",
        "runtime_enforcement_enabled",
        "may_block_commands",
        "changes_terminal_execution_flow",
        "default_failure_behavior",
        "required_evidence_before_runtime_touchpoint",
        "runtime_touchpoint_constraints",
        "rollback",
    })
    if data["schema_version"] != "log-only-implementation-gate-v1":
        raise ValueError("schema_version must be log-only-implementation-gate-v1")
    if data["mode"] != "log_only":
        raise ValueError("mode must be log_only")
    for field in ("runtime_enforcement_enabled", "may_block_commands", "changes_terminal_execution_flow"):
        if data[field] is not False:
            raise ValueError(f"{field} must be false")
    if data["default_failure_behavior"] != "continue_without_governance_block":
        raise ValueError("default_failure_behavior is invalid")
    evidence = data["required_evidence_before_runtime_touchpoint"]
    if not isinstance(evidence, list) or len(set(evidence)) != len(evidence):
        raise ValueError("required_evidence_before_runtime_touchpoint must be a unique list")
    required_evidence = {
        "explicit_operator_approval",
        "terminal_hook_contract_passed",
        "approval_flow_contract_passed",
        "unit_tests_passed",
        "portability_check_passed",
        "rollback_plan_documented",
    }
    if not required_evidence.issubset(set(evidence)):
        raise ValueError("required_evidence_before_runtime_touchpoint is incomplete")
    constraints = data["runtime_touchpoint_constraints"]
    if not isinstance(constraints, list) or len(set(constraints)) != len(constraints):
        raise ValueError("runtime_touchpoint_constraints must be a unique list")
    required_constraints = {
        "one_small_hook_only",
        "no_command_mutation",
        "no_additional_approval_prompt",
        "audit_write_failure_non_blocking",
        "feature_flag_disable_path",
    }
    if not required_constraints.issubset(set(constraints)):
        raise ValueError("runtime_touchpoint_constraints is incomplete")
    if data["rollback"] != "disable_governance_terminal_dry_run_or_remove_single_hook":
        raise ValueError("rollback is invalid")


def validate_operator_approval_record(data: dict) -> None:
    require(data, {
        "schema_version",
        "record_id",
        "approval_status",
        "runtime_scope",
        "runtime_touchpoint_allowed",
        "enforcement_allowed",
        "maximum_mode",
        "operator_identity",
        "approved_touchpoints",
        "explicitly_out_of_scope",
        "required_validation",
        "rollback_plan",
        "operator_reapproval_required_for",
        "notes",
    })
    if data["schema_version"] != "operator-approval-record-v1":
        raise ValueError("schema_version must be operator-approval-record-v1")
    if data["approval_status"] not in {"not_granted", "granted", "revoked", "expired"}:
        raise ValueError("approval_status is invalid")
    if data["runtime_scope"] not in {"none", "terminal_log_only", "file_log_only", "gateway_log_only", "model_routing_log_only"}:
        raise ValueError("runtime_scope is invalid")
    if data["maximum_mode"] not in {"design_only", "log_only"}:
        raise ValueError("maximum_mode is invalid")
    for field in ("runtime_touchpoint_allowed", "enforcement_allowed"):
        if not isinstance(data[field], bool):
            raise ValueError(f"{field} must be boolean")
    if data["approval_status"] == "not_granted":
        if data["runtime_scope"] != "none":
            raise ValueError("not_granted records must set runtime_scope to none")
        if data["runtime_touchpoint_allowed"] is not False:
            raise ValueError("not_granted records must not allow runtime touchpoints")
        if data["enforcement_allowed"] is not False:
            raise ValueError("not_granted records must not allow enforcement")
    if data["enforcement_allowed"] is True:
        raise ValueError("Feature 002 operator approval records cannot approve enforcement yet")
    approved = data["approved_touchpoints"]
    out_of_scope = data["explicitly_out_of_scope"]
    validation = data["required_validation"]
    reapproval = data["operator_reapproval_required_for"]
    for name, value in (
        ("approved_touchpoints", approved),
        ("explicitly_out_of_scope", out_of_scope),
        ("required_validation", validation),
        ("operator_reapproval_required_for", reapproval),
    ):
        if not isinstance(value, list) or len(set(value)) != len(value):
            raise ValueError(f"{name} must be a unique list")
    required_out_of_scope = {"tools/terminal", "tools/file", "gateway", "model_routing"}
    if data["approval_status"] == "not_granted" and not required_out_of_scope.issubset(set(out_of_scope)):
        raise ValueError("not_granted records must explicitly keep runtime touchpoints out of scope")
    required_validation = {
        "operator_approval_record_validator_passed",
        "terminal_hook_contract_passed",
        "approval_flow_contract_passed",
        "log_only_implementation_gate_passed",
        "unit_tests_passed",
        "portability_check_passed",
        "rollback_plan_documented",
    }
    if not required_validation.issubset(set(validation)):
        raise ValueError("required_validation is incomplete")
    required_reapproval = {
        "any_runtime_file_edit",
        "any_command_blocking_behavior",
        "any_terminal_execution_flow_change",
        "any_new_approval_prompt",
        "any_scope_beyond_log_only",
    }
    if not required_reapproval.issubset(set(reapproval)):
        raise ValueError("operator_reapproval_required_for is incomplete")
    if not str(data["rollback_plan"]).strip():
        raise ValueError("rollback_plan must be non-empty")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return fail("usage: check_runtime_guard_schema.py <policy|decision|audit json>")
    path = Path(argv[1])
    try:
        data = load(path)
        if not isinstance(data, dict):
            raise ValueError("top-level JSON must be object")
        version = data.get("schema_version")
        if version == "runtime-guard-policy-v1":
            validate_policy(data)
            return ok("policy", path)
        if version == "runtime-guard-decision-v1":
            validate_decision(data)
            return ok("decision", path)
        if version == "runtime-guard-audit-record-v1":
            validate_audit(data)
            return ok("audit", path)
        if version == "terminal-hook-dry-run-contract-v1":
            validate_terminal_hook_contract(data)
            return ok("terminal_hook_contract", path)
        if version == "approval-flow-interaction-contract-v1":
            validate_approval_flow_contract(data)
            return ok("approval_flow_contract", path)
        if version == "log-only-implementation-gate-v1":
            validate_log_only_implementation_gate(data)
            return ok("log_only_implementation_gate", path)
        if version == "operator-approval-record-v1":
            validate_operator_approval_record(data)
            return ok("operator_approval_record", path)
        if data.get("operation") == "dry_run_terminal_classification":
            validate_action(data)
            return ok("action", path)
        raise ValueError("unknown schema_version")
    except ValueError as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
