# Feature Spec: Hermes Portable Digital State

## User Story

As a Hermes Agent operator, institution, government team, or space-grade mission team, I want Hermes Agent to become an independent portable digital-state system so I can move it to another machine, restore operator state safely, and keep governance, model review, audit, risk signals, and staged enforcement consistent without depending on any external workstation folder or project.

## What the Feature Builds

This feature defines the plan and first safe artifacts for a Hermes-native digital state:
- Spec Kit constitution and source-of-truth artifacts
- a model council process that records returned, timed-out, errored, and skipped models
- a portability contract for moving the state between machines
- governance vocabulary: constitution, ministries, model council, audit office, signals office, operations office, strategy office, no-go gates
- future schemas for governance status, model review, audit records, and portability checks
- read-only skill/docs/validator phases before any runtime enforcement

## Personas and Operating Environments

1. Individual operator
Needs simple bootstrap, local profile restore, safe defaults, and visible model health.

2. Institution or enterprise
Needs repeatable setup, role separation, audit records, compliance-ready documentation, and secrets/config separation.

3. Government environment
Needs least privilege, offline-ready documentation, deterministic validation, explicit approvals, model provenance, and no hidden remote dependencies.

4. Space or mission-critical agency
Needs fail-closed design, unreliable-network tolerance, reproducible installation, immutable decision records, strict no-go gates, and human authority over irreversible actions.

## Scope

In scope for the current Spec Kit feature:
- Update and maintain specs/001-hyperagent-governance-integration as the source of truth.
- Record actual Model Council results in model-council-results.md/json and summarize them in plan.md.
- Define a Hermes-native portable-state architecture.
- Plan docs and skills that explain the state without claiming enforcement exists.
- Plan read-only schemas/validators using standard library only.
- Define future phases for ministries, signals, audit, bootstrap, and runtime guards.

Out of scope for this feature:
- linking to or importing from external concept folders
- copying external runtime, dashboards, executors, package manifests, lockfiles, or root instructions
- modifying terminal, file, patch, model routing, gateway, cron, or TUI behavior
- adding dependencies
- implementing AG-UI, CopilotKit, or any dashboard
- claiming production/critical certification

## Acceptance Criteria

AC1. Spec Kit artifacts define Hermes as an independent portable digital state.
AC2. The plan distinguishes portable repo artifacts from operator-local secrets/config/profile state.
AC3. Model Council records every requested model as returned, timeout/error, empty, or skipped.
AC4. Only returned model outputs influence recommendations; timed-out models are not counted as reviewers.
AC5. Current phases remain read-only/artifact-only until a later enforcement feature is approved.
AC6. First validator tasks are standard-library, read-only, and tested with fixtures.
AC7. Portability checks reject required workstation-specific paths and required external project paths.
AC8. Plans address individual, enterprise, government, and mission-critical/space-grade use cases.
AC9. No task in this feature modifies dependency manifests, lockfiles, runtime tool dispatch, or gateway behavior.
AC10. Bootstrap documentation clearly states that secrets and OAuth credentials are restored through Hermes-native auth/profile/env flows, not committed files.

## Digital-State Concepts

- Constitution: immutable principles and no-go gates.
- Strategy Ministry: planning, prioritization, roadmap synthesis, model council synthesis.
- Operations Ministry: bootstrap, environment readiness, runbooks, safe execution posture.
- Signals Ministry: read-only risk scanning, premortems, dependency and secret heuristics.
- Audit Office: provenance records, model review records, decision logs, hashes, timestamps.
- Model Council: explicit fan-out to models with status tracking and quorum rules.
- Governance Status: a readable summary of posture, gates, artifacts, model health, portability state.
- Portability Contract: what moves with the repo vs what must be restored locally.
- Runtime Guards: future separate feature for terminal/file/package/model/gateway enforcement.

## Portability Contract

Portable with the repository:
- specs/
- skills/ created for governance
- docs/governance/
- scripts/governance/ read-only validators
- tests for schemas and validators
- schemas/ or spec-local schema files
- model council records without secrets

Operator-local, not committed:
- API keys and provider tokens
- OAuth/auth stores
- gateway/platform tokens
- local model credentials
- machine-specific config
- local logs containing sensitive data
- profile exports unless explicitly sanitized

Bootstrap must verify:
- Hermes is installed and compatible
- config validates
- required skills/docs/scripts exist
- provider keys are present where needed
- model smoke tests pass or failures are recorded
- no required external path is present
- no secrets are committed in portable artifacts

## Model Council Quorum

For ordinary planning, at least three usable reviewers are preferred, including the active synthesis model if it produced the final plan. For high-risk/government/space-grade phases, the plan should seek at least three returned model reviews from different model families/providers or record why quorum was not possible. Timeout does not block artifact drafting, but it blocks claims of full model consensus.
