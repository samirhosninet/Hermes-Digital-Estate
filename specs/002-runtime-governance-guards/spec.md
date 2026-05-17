# Spec: Runtime Governance Guards

## Purpose

Design a Hermes-native runtime governance guard system that can later protect high-risk actions across terminal, file, package, git, network/deployment, credential, model-routing, gateway, cron, and webhook boundaries.

The current approved slice implements a pure, non-integrated guard core. No runtime enforcement is active.

## Users

- Individual operators who want safer autonomous work.
- Teams and institutions that need approval and audit boundaries.
- Government or regulated environments that need strict separation of advisory AI from authorized action.
- Space-grade or mission-grade organizations that need conservative fail-closed design before any operational use.

## Required Outcomes

1. Define policy inputs and action classes.
2. Define enforcement points in Hermes without implementing them yet.
3. Define allow, deny, escalate, and fail_closed decisions.
4. Define audit records for guard decisions.
5. Implement a minimal non-integrated guard core before any runtime hook.
6. Preserve portability across machines.
7. Keep Model Council review records honest.
8. Provide a design document that explains the future policy/decision/audit lifecycle.

## Non-Goals

- No terminal/file/gateway/model-routing runtime hooks in this slice.
- No package/dependency/lockfile changes.
- No dashboard or daemon.
- No external folder dependency.
- No certification or mission-authorization claim.

## Candidate Enforcement Boundaries

- terminal command dispatch
- file write/patch/delete operations
- package manager and lockfile changes
- git destructive operations and remote pushes
- network/deployment operations
- credential and auth-file access
- model/provider routing changes
- gateway platform operations
- cron/webhook scheduling with side effects

## Decision Types

- allow: action is within current policy and risk class.
- deny: action violates policy or no-go gates.
- escalate: operator approval required before proceeding.
- fail_closed: policy cannot be loaded or interpreted safely.

## Escalation Criteria

Future runtime guards should escalate rather than silently allow when an action crosses a boundary that may affect durable state, other users, external systems, credentials, model routing, billing, deployment, or irreversible git history. Escalation should also be required when the classifier cannot prove an action is read-only.

Examples that should escalate in a future implementation:

- package installation, dependency edits, or lockfile mutation
- git push, force-push, reset, rebase, or remote changes
- deployment, gateway fanout, webhook publication, or cron side effects
- reads from credential/auth paths or writes near config/secrets
- model/provider routing changes that affect future sessions
- ambiguous shell commands whose side effects cannot be classified safely

## Secret and Sensitive Payload Definition

Future audit writers must avoid storing raw values for secrets or sensitive payloads. At minimum, treat these as sensitive:

- API keys, OAuth tokens, bearer tokens, cookies, passwords, private keys, SSH keys, gateway tokens, and credential-pool material
- `.env`, auth stores, provider config, browser/session cookies, and local profile state
- raw command arguments or file excerpts that contain high-entropy tokens, account identifiers, phone numbers, or deployment credentials

Audit records should store summaries, hashes, policy version, boundary, decision, and redacted paths instead of raw secret-bearing content.

## Portability Criteria

Future policy artifacts must be repo-relative by default and must not require machine-specific absolute paths. Operator-local overlays may exist outside the repo, but they must be optional, explicitly declared, and excluded from the portable evidence bundle.

A future portability check should fail if the guard policy requires Windows absolute paths, `/mock/user/...`, `/mock_mnt/<drive>/...`, or untracked secret/config paths to function.

## Design-Time Schemas

The design phase defines schema drafts for the future guard core without enabling enforcement:

- runtime guard policy: version, mode, default decision, portable flag, and rules
- runtime guard decision: allow/deny/escalate/fail_closed result, boundary, risk class, reason, policy version, and redacted action summary
- runtime guard audit record: timestamp, actor, boundary, risk class, decision, action hash, redacted summary, and optional approval reference

These schema drafts are portable artifacts and must not contain local absolute paths, secrets, OAuth material, or machine-specific state.

## Current Implemented Core

Implemented files:

- `agent/runtime_governance.py`
- `tests/agent/test_runtime_governance.py`
- `specs/002-runtime-governance-guards/schemas/runtime-guard-policy-v1.json`
- `specs/002-runtime-governance-guards/schemas/runtime-guard-decision-v1.json`
- `specs/002-runtime-governance-guards/schemas/runtime-guard-audit-record-v1.json`
- `specs/002-runtime-governance-guards/fixtures/dry-run-*.json`
- `scripts/governance/check_runtime_guard_schema.py`

Current behavior:

- missing/malformed policy fails closed
- rules-based policy decisions can allow, deny, escalate, or fail closed
- terminal commands can be classified in dry-run form without execution
- dry-run action fixtures document read-only terminal, package mutation, and destructive git classifications
- schema validator accepts dry-run action fixtures as portable evidence
- package mutation escalates
- credential path access denies
- audit records redact secret-bearing action summaries and store hashes

This is not wired into live Hermes tool dispatch.

## Runtime Guard Design Document

The lifecycle and no-go gates are documented in:

- `docs/governance/runtime-guard-design.md`

This document is also design-only and does not enable enforcement.

## Acceptance Criteria for Current Slice

- guard artifacts exist under `specs/002-runtime-governance-guards/`
- enforcement points are listed without live runtime hooks
- pure guard core has tests before any runtime integration
- audit schema exists and audit builder avoids raw secret-bearing payloads
- no terminal/file/gateway/model-routing dispatch files are modified
- escalation criteria are documented before enforcement
- secret/sensitive payload handling is documented before audit implementation
- portability criteria are documented before policy grammar is finalized
- policy, decision, and audit schema drafts exist before runtime hook implementation
- schema fixtures validate with a stdlib-only read-only checker
- `docs/governance/runtime-guard-design.md` documents the future policy/decision/audit lifecycle
- `docs/governance/terminal-hook-dry-run-design.md` and `terminal-hook-dry-run-contract-v1` define the future terminal hook as dry-run/log-only, non-blocking, and non-reordering before any runtime file is edited
- `docs/governance/approval-flow-interaction.md` and `approval-flow-interaction-contract-v1` prove the future dry-run hook must not duplicate prompts, bypass existing approvals, block commands, or change terminal execution flow
- `docs/governance/log-only-implementation-gate.md` and `log-only-implementation-gate-v1` define the evidence and operator-approval gate required before any runtime terminal touchpoint is edited
- `docs/governance/operator-approval-record.md` and `operator-approval-record-v1` prove that no runtime touchpoint is currently approved and define the exact evidence, scope, rollback, and reapproval requirements for any future runtime edit
