# Maturity Model for the Hermes Portable Digital State

This maturity model helps individuals, institutions, governments, and mission-grade organizations adopt Hermes Agent as a portable digital-state system without overstating current capabilities.

It is an adoption model, not a certification model.

## Level 0: Concept

State:
- ideas are discussed
- no durable Spec Kit source of truth
- no repeatable checks

Exit criteria:
- Spec Kit feature exists
- scope and non-goals are written

## Level 1: Documented Portable State

State:
- constitution/spec/plan/tasks/analyze exist
- repo-portable artifacts are separated from operator-local state
- no external concept folder is required

Evidence:
- `specs/001-hyperagent-governance-integration/`
- `docs/governance/portable-digital-state.md`

Exit criteria:
- governance docs and approval matrix exist
- model council process is documented

## Level 2: Read-Only Validated Governance

State:
- schemas exist
- read-only validators exist
- tests verify validators
- model council records distinguish returned, timeout, error, empty, and skipped

Evidence:
- `scripts/governance/`
- `tests/scripts/`
- `specs/001-hyperagent-governance-integration/schemas/`
- model council result files

Exit criteria:
- targeted tests pass
- portability check passes
- governance-status skill exists

## Level 3: Operator-Ready Deployment

State:
- another machine can bootstrap the repo
- local secrets/config/profile restoration is documented
- approval and audit runbooks are usable by a team

Evidence:
- `bootstrap-readiness.md`
- `audit-provenance.md`
- `institutional-operating-model.md`
- local operator records outside the repo

Exit criteria:
- bootstrap has been tested on at least one clean machine or profile
- model/provider readiness has been smoke-tested
- evidence bundle can be generated or assembled

## Level 4: Designed Runtime Enforcement

State:
- runtime governance guards are specified but not necessarily implemented
- enforcement points, policy grammar, fail-closed behavior, audit records, and tests are designed

Evidence:
- `specs/002-runtime-governance-guards/`

Exit criteria:
- feature 002 design passes analysis
- no runtime implementation begins until operator approves

## Level 5: Tested Runtime Enforcement

State:
- runtime guards are implemented and tested
- unsafe terminal/file/package/git/network/model actions can be denied by policy
- deny/allow decisions are auditable

Evidence:
- tests covering allow/deny/fail-closed paths
- runtime implementation PR/change set
- rollback plan

Exit criteria:
- independent review for institutional or government deployment
- documented incident procedure

## Level 6: Independently Assessed Deployment

State:
- organization-specific security, legal, safety, and compliance review completed
- continuity and incident exercises performed
- deployment boundaries are formally approved

Evidence:
- external assessment reports
- organization-specific authority-to-operate or equivalent approval
- retention and audit policies

## Level 7: Mission-Authorized Operation

State:
- qualified authority approves a specific mission or critical use
- operational constraints are enforced and monitored
- models remain advisory unless explicitly authorized

Evidence:
- mission authorization
- operational monitoring records
- rollback/abort procedures
- formal hazard analysis

## Current Target

The current feature targets Level 2 foundations and prepares for Level 3 documentation.

Feature 002 should target Level 4 design only unless the operator explicitly approves implementation later.
