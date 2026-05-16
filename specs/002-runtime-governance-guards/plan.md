# Plan: Runtime Governance Guards

## Status

Minimal non-integrated guard core implemented. No Hermes runtime hook or live enforcement is active.

## Architecture Concept

Future runtime guards should have four layers:

1. Policy artifacts
   - repo-relative policy files
   - versioned schemas
   - action classes and risk taxonomy

2. Classifier
   - maps a proposed action to risk class and boundary
   - detects destructive commands, secret paths, package changes, git remotes, deployment operations, and gateway side effects

3. Decision engine
   - returns allow, deny, escalate, or fail_closed
   - never fails open on missing or malformed policy

4. Audit writer
   - records decision, actor, boundary, action summary, policy version, outcome, and timestamp
   - avoids storing secrets or raw sensitive payloads

## Implemented Non-Integrated Core

The current implementation is pure Python and test-only from a runtime perspective:

- `agent/runtime_governance.py`
- `tests/agent/test_runtime_governance.py`
- `schemas/runtime-guard-policy-v1.json`
- `schemas/runtime-guard-decision-v1.json`
- `schemas/runtime-guard-audit-record-v1.json`
- `specs/002-runtime-governance-guards/fixtures/dry-run-*.json`
- `scripts/governance/check_runtime_guard_schema.py`

Implemented behavior:

- strict-mode fail-closed for missing/malformed policies
- rules-based policy shape with `allow`, `deny`, `escalate`, and `fail_closed`
- terminal dry-run action classifier via `build_terminal_dry_run_action()`
- dry-run action fixtures for read-only terminal, package mutation, and destructive git classifications
- schema checker support for dry-run action fixture validation
- package mutation escalation
- credential path denial
- redacted audit records using `runtime-guard-audit-record-v1`

This core is not connected to terminal/file/gateway/model routing. Existing Hermes runtime behavior is unchanged.

## Candidate Files for Future Runtime Hooking

Do not edit these until a hook-specific task is approved:

- `tools/terminal_tool.py`
- `tools/code_execution_tool.py`
- `tools/file_safety.py`
- `tools/path_security.py`
- `tools/approval.py`
- `model_tools.py`
- `gateway/`
- `cron/`
- `hermes_cli/config.py`

## Policy Inputs

Potential future portable inputs:

- `config/governance/policy.yaml` or equivalent repo policy
- `specs/*/schemas/runtime-guard-policy-v1.json`
- operator-local overrides outside the repo for deployment-specific constraints

No policy file is added yet because policy grammar needs final review before runtime implementation.

## Model Council Design Review

Feature 002 Model Council results are recorded in:

- `model-council-results.json`
- `model-council-results.md`

Returned reviewers agreed the feature should remain design-only now. The main design gaps identified were escalation criteria, portability verification, secret definition for audit records, and the need to avoid conflicts with the existing Hermes approvals flow.

## Design Schemas Added Before Runtime Implementation

The design now includes portable, repo-relative schema drafts and fixtures under:

- `schemas/runtime-guard-policy-v1.json`
- `schemas/runtime-guard-decision-v1.json`
- `schemas/runtime-guard-audit-record-v1.json`
- `fixtures/valid-policy.json`
- `fixtures/valid-decision.json`
- `fixtures/valid-audit-record.json`

These schemas are not runtime enforcement. They define the contract that a later implementation must satisfy before any terminal/file/gateway/model-routing hook is added. The validator `scripts/governance/check_runtime_guard_schema.py` is read-only and stdlib-only.

## Runtime Guard Design Document

The future policy, classifier, decision, approval-handoff, audit, and outcome lifecycle is documented in:

- `docs/governance/runtime-guard-design.md`

This document is intentionally design-only. It is the operator-readable bridge between Feature 001 governance posture and Feature 002 future implementation.

## First Implementation Slice If Later Approved

If the operator explicitly approves implementation later, the first slice should not hook every Hermes tool. Start with a minimal, test-first guard core:

1. policy schema/parser with strict-mode fail-closed behavior
2. action classifier for one low-blast-radius boundary
3. decision object: allow, deny, escalate, fail_closed
4. redacted audit-record builder
5. unit tests for missing/malformed policy, safe read-only actions, escalation, and secret redaction
6. dry-run/log-only mode before enforcement

Only after that should any terminal/file/gateway/model runtime hook be designed or implemented.

## Testing Strategy Required Before Implementation

Tests must cover:

- malformed policy -> fail_closed
- missing policy in strict mode -> fail_closed
- destructive command -> deny or escalate
- safe read-only command -> allow
- credential path access -> deny or escalate
- package/lockfile mutation -> escalate
- git reset/push -> escalate or deny
- gateway broadcast/deployment -> escalate
- audit record emitted for each decision
- no secrets leaked into audit output

## Rollout Strategy

1. Design-only Spec Kit feature.
2. Model Council review.
3. Schema drafts, fixtures, and read-only validator.
4. Operator-readable runtime guard design document.
5. Human approval to implement a minimal policy parser and tests.
6. Implement guard in dry-run/log-only mode.
7. Implement fail-closed enforcement for highest-risk actions.
8. Expand boundaries one at a time.

## Risks

- False sense of safety if docs imply enforcement before tests.
- Breaking existing Hermes tools if hooks are inserted too broadly.
- Secret leakage if audit records capture raw payloads.
- Operator frustration if benign actions are over-blocked.
- Portability loss if policies use machine-specific paths.

## Terminal Hook Dry-Run Contract

T019 now has a design-only terminal hook contract:

- `docs/governance/terminal-hook-dry-run-design.md`
- `schemas/terminal-hook-dry-run-contract-v1.json`
- `fixtures/terminal-hook-dry-run-contract.json`
- `fixtures/terminal-hook-dry-run-audit-sample.json`
- `tests/scripts/test_terminal_hook_contract.py`

The contract explicitly requires `dry_run_log_only`, `runtime_enforcement_enabled=false`, `changes_terminal_execution_flow=false`, and `may_block_commands=false`. It also requires evidence before integration: unit tests, a dry-run audit sample, operator approval matrix, portability check, and secret-redaction test.

This is still not a runtime hook. It is the acceptance contract for a future hook implementation.

## Approval Flow Interaction Contract

T020 now has a design-only approval-flow interaction contract:

- `docs/governance/approval-flow-interaction.md`
- `schemas/approval-flow-interaction-contract-v1.json`
- `fixtures/approval-flow-interaction-contract.json`
- `fixtures/approval-flow-dry-run-audit-sample.json`
- `tests/scripts/test_approval_flow_interaction.py`

The contract explicitly requires `dry_run_log_only`, `runtime_enforcement_enabled=false`, `duplicates_approval_prompt=false`, `bypasses_existing_approval=false`, `changes_terminal_execution_flow=false`, and `may_block_commands=false`. It also defines disable and failure behavior: audit failures must not stop terminal flow, and approval failures must defer to the existing approval flow.

This is still not a runtime hook. It is the acceptance contract for a future dry-run/log-only approval interaction.

## Log-Only Implementation Gate

T021A adds the explicit gate that must pass before any future terminal runtime touchpoint is allowed:

- `docs/governance/log-only-implementation-gate.md`
- `schemas/log-only-implementation-gate-v1.json`
- `fixtures/log-only-implementation-gate.json`
- `tests/scripts/test_log_only_implementation_gate.py`

The gate requires `mode=log_only`, `runtime_enforcement_enabled=false`, `may_block_commands=false`, and `changes_terminal_execution_flow=false`. It also requires explicit operator approval, passing terminal-hook and approval-flow contracts, unit tests, portability checks, and a rollback plan before any runtime file is touched.

This is still not a runtime hook. It is the approval gate for a future log-only implementation slice.

## Operator Approval Record Gate

T021B adds the explicit operator approval record required before any future runtime touchpoint can be edited:

- `docs/governance/operator-approval-record.md`
- `schemas/operator-approval-record-v1.json`
- `fixtures/operator-approval-record.json`
- `tests/scripts/test_operator_approval_record.py`

The current record deliberately sets `approval_status=not_granted`, `runtime_scope=none`, `runtime_touchpoint_allowed=false`, and `enforcement_allowed=false`. It keeps terminal, file, gateway, model routing, cron, and approvals runtime out of scope. A later approval must name the exact touchpoint, mode, validation commands, audit behavior, and rollback path.

This is still not a runtime hook. It is a conservative approval record proving that no runtime integration is currently authorized.

## Current Decision

Feature 002 now has a tested pure decision core, terminal dry-run classifier, terminal hook dry-run contract, approval-flow interaction contract, log-only implementation gate, and operator approval record. It remains non-enforcing until a separate runtime-hook implementation phase is explicitly approved and tested.

## Added Evidence Layer

A portable model benchmark utility now exists as read-only governance evidence:

- `scripts/governance/model_benchmark.py`
- `tests/scripts/test_model_benchmark.py`
- `docs/governance/model-benchmarking.md`
- `specs/001-hyperagent-governance-integration/schemas/model-benchmark-v1.json`
- `specs/001-hyperagent-governance-integration/model-benchmark-smoke-results.json`

This does not change runtime routing. It only records current provider/model health so Model Council decisions and timeout settings are evidence-based.

## Dry-Run Scenario Fixtures

Feature 002 now includes design-time decision examples under:

- `fixtures/scenarios/dry-run-safe-read-allow.json`
- `fixtures/scenarios/dry-run-package-escalate.json`
- `fixtures/scenarios/dry-run-secret-path-deny.json`
- `fixtures/scenarios/dry-run-policy-missing-fail-closed.json`

These fixtures demonstrate the intended allow/escalate/deny/fail_closed outcomes before any runtime hook exists. They are validated by `tests/scripts/test_runtime_guard_scenarios.py` and `scripts/governance/check_runtime_guard_schema.py`.

They are still evidence and contract artifacts only. They do not intercept terminal, file, gateway, cron, or model-routing calls.

