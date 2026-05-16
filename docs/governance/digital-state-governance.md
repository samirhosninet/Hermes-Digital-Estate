# Hermes Digital State Governance

Hermes Agent is treated as the portable digital state: the repo carries the constitution, skills, docs, schemas, validators, tests, and model-review records; the operator restores local profile/config/secrets through Hermes-native mechanisms.

This document transfers ideas only. It does not create a runtime dependency on any external folder, dashboard, executor, or project.

## Layers

1. Constitution: Spec Kit principles and no-go gates in `specs/001-hyperagent-governance-integration/`.
2. Ministries: role vocabulary implemented first as skills/docs, not autonomous services.
3. Model Council: per-model reviews with returned/timeout/error status; only returned outputs affect decisions.
4. Audit Office: JSON records for decisions, validations, approvals, and blocked actions.
5. Signals Office: read-only risk signals such as secrets, absolute paths, unsafe dependency changes, and scope creep.
6. Operations Office: bootstrap, health checks, model smoke tests, and operator runbooks.
7. Runtime Guards: future separate Spec Kit feature only; not active in this phase.

## No-go gates in the current phase

Stop if a task requires dependency changes, lockfile edits, gateway/runtime/tool-dispatch changes, autonomous dashboards, external-folder coupling, or committed secrets.

## Critical-grade posture

For institutions, governments, and space-grade environments, the default posture is conservative: least privilege, offline-readable docs, reproducible bootstrap, explicit operator approval for irreversible actions, and honest model provenance.

## Current status

This phase is docs/read-only governance. It does not enforce command blocking at runtime. Runtime enforcement requires a new approved Spec Kit feature and tests.
