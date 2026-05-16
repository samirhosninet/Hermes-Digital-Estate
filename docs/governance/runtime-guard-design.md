# Runtime Guard Design

Status: design-only. This document does not enable runtime enforcement.

## Purpose

Runtime governance guards are the future protection layer for a portable Hermes digital state. They are intended to classify proposed actions, decide whether they are allowed, denied, escalated, or failed closed, and produce redacted audit records.

This design exists so implementation can be reviewed before any Hermes tool, gateway, model routing, cron, or file runtime is changed.

## Non-enforcement boundary

The current repository state may include schemas, fixtures, validators, tests, and docs. These are not guards by themselves.

Do not claim Hermes is enforcing runtime governance until a later Spec Kit implementation feature adds tested runtime hooks.

## Lifecycle

1. Proposed action
   - A tool, gateway adapter, cron job, model router, or file operation prepares an action.
   - Future guard code receives a summarized action object, not raw secret-bearing content.

2. Classification
   - The classifier assigns boundary and risk class.
   - Boundaries include terminal, file, package, git, network/deployment, credentials, model routing, gateway, cron, and webhook.
   - Risk classes align with `docs/governance/risk-taxonomy.md`.

3. Policy load
   - Policy is loaded from portable repo-relative policy artifacts and optional operator-local overlays.
   - Missing, malformed, ambiguous, or incompatible policy must fail closed in strict mode.

4. Decision
   - The decision engine returns one of: allow, deny, escalate, fail_closed.
   - A decision must include policy version, boundary, risk class, reason, and redacted action summary.

5. Approval handoff
   - Escalation should integrate with existing Hermes approval flows instead of bypassing or duplicating them unsafely.
   - Operator approval is an authorization event, not a reason to skip audit.

6. Audit record
   - Every decision should be audit-recordable.
   - Audit records store redacted summaries and hashes, not raw secrets, OAuth tokens, cookies, private keys, or credential material.

7. Outcome
   - Allowed actions proceed.
   - Denied and fail-closed actions stop.
   - Escalated actions wait for operator approval and then record the outcome.

## Decision vocabulary

allow: the action is within policy and low enough risk to proceed.

deny: the action violates a no-go rule or is too risky for the current mode.

escalate: explicit operator approval is required before proceeding.

fail_closed: policy, schema, classifier, or guard state is unsafe or unreadable, so the action must not proceed silently.

## First safe implementation slice, if later approved

The first implementation should not hook every Hermes tool. It should be a small guard core with tests first:

1. policy parser for the existing schema drafts
2. decision object builder
3. redacted audit-record builder
4. classifier for one low-blast-radius boundary
5. dry-run/log-only mode
6. unit tests for allow, deny, escalate, fail_closed, missing policy, malformed policy, and secret redaction

Only after this works should terminal, file, gateway, cron, or model-routing hooks be considered.

## Current non-integrated core

The repository now includes a pure, unhooked dry-run classifier in `agent/runtime_governance.py`. It can turn proposed terminal command text into action records for tests and design review, but it does not execute commands and is not connected to `tools/terminal_tool.py`.

Current examples:

- `pwd` -> terminal/read_only
- `pip install requests` -> package/package_mutation
- `git reset --hard HEAD~1` -> git_destructive/git_destructive

The matching dry-run action fixtures live under `specs/002-runtime-governance-guards/fixtures/dry-run-*.json` and are validated by `scripts/governance/check_runtime_guard_schema.py`.

## No-go gates

Do not implement runtime hooks before tests.
Do not store raw secrets in audit records.
Do not change dependencies or lockfiles for the first slice.
Do not bypass current Hermes approvals.
Do not use machine-specific absolute paths in portable policy.
Do not claim certification, accreditation, mission authorization, or safety-critical readiness from this design.

## Portability requirements

Portable artifacts may live in:

- `specs/`
- `docs/`
- `skills/`
- `scripts/`
- `tests/`
- future repo-relative policy files

Operator-local state must stay outside portable artifacts:

- API keys
- OAuth tokens
- gateway tokens
- local profiles
- machine-specific paths
- private audit exports
- deployment credentials

## Related artifacts

- `specs/002-runtime-governance-guards/constitution.md`
- `specs/002-runtime-governance-guards/spec.md`
- `specs/002-runtime-governance-guards/plan.md`
- `specs/002-runtime-governance-guards/tasks.md`
- `specs/002-runtime-governance-guards/analyze.md`
- `specs/002-runtime-governance-guards/schemas/runtime-guard-policy-v1.json`
- `specs/002-runtime-governance-guards/schemas/runtime-guard-decision-v1.json`
- `specs/002-runtime-governance-guards/schemas/runtime-guard-audit-record-v1.json`
- `specs/002-runtime-governance-guards/fixtures/dry-run-terminal-read-only-action.json`
- `specs/002-runtime-governance-guards/fixtures/dry-run-package-mutation-action.json`
- `specs/002-runtime-governance-guards/fixtures/dry-run-git-destructive-action.json`
- `scripts/governance/check_runtime_guard_schema.py`
