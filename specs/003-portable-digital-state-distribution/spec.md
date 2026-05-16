# Spec: Portable Digital-State Distribution

## Summary

Create a safe GitHub-hosted Hermes Profile Distribution for the Hermes Digital State layer so users can install official Hermes Agent, install the Digital State profile distribution, run bootstrap checks, add their own credentials, update the distribution from GitHub, and keep working through Hermes Workspace without breaking upstream updates.

This feature is a planning and packaging feature. It does not activate runtime guards and does not create a separate UI.

## Users

### Individual user

Wants to install Hermes, install the Digital State profile distribution, and start using governance skills/docs/checks without understanding the internal repository structure.

### Team or institution operator

Wants a repeatable GitHub-backed distribution that can be reviewed, installed, validated, updated, and rolled back across machines without leaking secrets or depending on one workstation.

### Government or critical-grade operator

Wants an evidence-oriented installation path with clear separation between portable artifacts and local secrets, plus update/recovery guidance and no false certification claims.

### Distribution maintainer

Wants to publish Digital State updates without modifying official Hermes core and without forcing users to reinstall Hermes.

## User Stories

### US1: Install on a clean machine

Given a new machine with official Hermes Agent installed, when the user installs the Digital State Profile Distribution from GitHub and runs bootstrap checks, then the system reports whether the distribution is installed, portable, and ready for local credentials.

### US2: Update Digital State independently

Given Hermes Agent remains installed from upstream, when the Digital State repository releases an update, then the user can update the profile distribution without patching Hermes core.

### US3: Recover after deletion

Given Hermes Agent was deleted or reinstalled, when the user reinstalls official Hermes and reinstalls the profile distribution, then the digital-state artifacts are restored and bootstrap tells the user which local credentials/configuration must be recreated.

### US4: Update upstream Hermes safely

Given Hermes Agent receives upstream updates, when the operator updates Hermes and runs the digital-state bootstrap checks, then compatibility issues are reported without modifying core runtime files.

### US5: Institutional rollout

Given an institution wants to deploy the digital-state layer, when it follows the institutional installation guide, then the process distinguishes distribution artifacts, local secrets, profiles, approvals, evidence bundles, update policy, and operator responsibilities.

## Functional Requirements

FR1. Define a Hermes Profile Distribution contract using `distribution.yaml`, profile metadata, non-secret config defaults, skills, docs, scripts, and required environment variable names.

FR2. Define a `digital-state.manifest.json` contract listing pack metadata, supported artifact paths, excluded paths, required checks, supported modes, GitHub source metadata, and compatibility notes.

FR3. Define a read-only bootstrap checker that validates the workspace/profile contains required artifacts, no forbidden paths/secrets are present, schemas are readable, and expected validators/tests can run.

FR4. Document GitHub install/update flow using Hermes profile distribution commands rather than a custom installer as the primary path.

FR5. Keep optional export/import tooling as secondary support for offline transfer/evidence bundles only, never as the canonical update mechanism.

FR6. Add user quickstart documentation for personal usage.

FR7. Add institution installation documentation for teams, institutions, governments, and critical-grade environments.

FR8. Add update and recovery documentation for Hermes updates, Digital State distribution updates, deletion, migration, and rollback.

FR9. Add tests for distribution/manifest validation, bootstrap behavior, forbidden paths, secret exclusions, and portability.

FR10. Run or prepare a Model Council review record for the distribution design, recording returned/timeouts honestly.

FR11. Keep all artifacts repo-relative and avoid machine-specific required paths.

## Non-Goals

- Building a standalone UI/dashboard.
- Replacing official Hermes installation.
- Vendoring or forking official Hermes Agent core.
- Distributing API keys or OAuth credentials.
- Enabling runtime enforcement.
- Modifying terminal/file/gateway/model-routing core behavior.
- Claiming compliance certification or mission approval.

## Acceptance Criteria

AC1. `specs/003-portable-digital-state-distribution/` contains constitution, spec, plan, tasks, analyze, and model-council digest artifacts.

AC2. The plan clearly states that official Hermes Agent remains the base and Digital State is installed/updated as a Hermes Profile Distribution from a GitHub project.

AC3. The planned `distribution.yaml` and manifest exclude secrets, auth stores, logs, sessions, and machine-specific paths.

AC4. The planned bootstrap and distribution checks are stdlib-first and update-safe.

AC5. The planned documentation explains personal, institutional, GitHub update, and recovery workflows.

AC6. Runtime changes remain blocked unless Feature 002 approval gates are separately satisfied.

AC7. Verification commands include portability checks, schema checks, tests, and `hermes config check`.

AC8. Optional export/import tooling is documented as support/offline tooling, not the primary distribution mechanism.
