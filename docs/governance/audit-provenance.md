# Hermes Digital State Audit and Provenance Runbook

This runbook defines what the portable Hermes digital state should record for traceability. In feature 001 this is documentation and read-only validation guidance only; no runtime audit enforcement is active.

## Goals

- Make decisions reproducible across machines.
- Separate returned model reviews from timed-out or errored attempts.
- Preserve operator sovereignty: humans approve irreversible or external side effects.
- Keep secrets and machine-local state out of portable artifacts.
- Provide a path toward future fail-closed enforcement without claiming it exists today.

## Provenance sources

Spec Kit artifacts
- constitution.md: principles and no-go gates.
- spec.md: user-visible intent and acceptance criteria.
- plan.md: architecture, roadmap, model-council synthesis, risks.
- tasks.md: executable task list and verification steps.
- analyze.md: consistency and gap analysis.

Model Council records
- model-council-digest.md: compact prompt sent to models.
- model-council-results.md: human-readable review record.
- model-council-results.json: machine-checkable status record.

Governance schemas
- governance-status-v1.json: posture/status contract.
- model-review-v1.json: per-model review contract.
- audit-record-v1.json: event provenance contract.
- portability-check-v1.json: bootstrap/portability check contract.

Validation records
- outputs from scripts/governance/*.py.
- test results from unittest/pytest.
- hermes config check summary.
- model smoke-test summaries when relevant.

## Required event types

model_review_requested
- Record model id, provider, digest hash or path, timeout seconds, prompt sensitivity level.

model_review_returned
- Record model id, provider, elapsed seconds, content hash, status returned.

model_review_failed
- Record timeout/error/empty/skipped and reason. Do not synthesize from failed reviews.

decision_made
- Record decision, inputs used, models that influenced it, models excluded due to timeout/error, and operator assumptions.

artifact_changed
- Record path, task id, change purpose, before/after checksum if available.

approval_requested
- Record action, approval level, target, blast radius, rollback plan.

approval_granted_or_denied
- Record operator decision and constraints.

validation_run
- Record command, exit code, key output, files checked.

bootstrap_check
- Record machine-independent readiness: repo files present, local secrets absent from repo, config check result, tool availability, model smoke status.

incident_or_blocked_action
- Record what was blocked or failed, why, severity, and recovery steps.

## Integrity guidance

Checksums
- Use SHA-256 for important artifacts when a durable record is needed.
- Hash content outputs rather than storing large model responses in every audit entry.

Append-only posture
- Prefer append-only records for audit logs.
- If a correction is needed, add a correction entry rather than silently rewriting history.

Secret hygiene
- Never store raw API keys, OAuth tokens, cookies, SSH keys, or gateway tokens in audit artifacts.
- Store provider names and credential source class only, for example: NVIDIA_API_KEY present in operator env, not the value.

Machine portability
- Use repo-relative paths in portable audit records.
- Use placeholders for operator-local paths: HERMES_HOME, PROFILE_HOME, ENV_FILE.
- Do not make X:, /mnt/d, /mock/user/, or ~/.hermes paths required by the repo.

## Model Council provenance rules

1. Every requested model must have a record.
2. Valid statuses are returned, timeout, error, empty, skipped.
3. Returned reviews may influence synthesis.
4. Timeout/error/empty/skipped records may influence risk assessment, but not substantive plan agreement.
5. The final synthesis must state which returned models were used.
6. A quorum is preferred, but no false consensus is allowed.

## Institution/government/space-grade notes

Hermes governance artifacts are foundations for auditability, not legal or mission certification.

For critical deployments, add external controls:
- named accountable owner,
- change advisory process,
- independent review,
- retention period,
- incident response procedure,
- disaster recovery test,
- supply-chain review,
- offline operating mode,
- physical and network security controls.

## Minimum audit record example

{
  "schema_version": "audit-record-v1",
  "timestamp_utc": "2026-05-14T00:00:00Z",
  "actor": "hermes-agent:gpt-5.5",
  "event_type": "artifact_changed",
  "artifact_path": "docs/governance/approval-matrix.md",
  "outcome": "success",
  "checksum_sha256": "optional",
  "notes": "Created approval guidance for portable digital-state governance."
}

## Current feature boundary

Feature 001 creates the audit language and validation surface. It does not hook audit recording into Hermes runtime. Runtime audit capture belongs in a separate future Spec Kit feature with tests and explicit operator approval.
