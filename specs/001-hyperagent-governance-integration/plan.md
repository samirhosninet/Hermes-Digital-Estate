# Plan: Hermes Portable Digital State

> For Hermes: this is a Spec Kit planning artifact. Do not implement runtime enforcement from this file. Execute only the read-only/docs/schema tasks unless a later Spec Kit feature approves runtime changes.

## Goal

Build Hermes Agent into an independent, portable digital-state system that can be moved to another machine and adapted for individual users, institutions, governments, and space-grade agencies while staying Hermes-native and avoiding external project coupling.

## Current Model Council Run

Digest file: specs/001-hyperagent-governance-integration/model-council-digest.md
Results file: specs/001-hyperagent-governance-integration/model-council-results.md
JSON record: specs/001-hyperagent-governance-integration/model-council-results.json

Returned usable reviews in this run:
- gpt-5.5: active Hermes synthesis and final planning integration.
- z-ai/glm-5.1 via NVIDIA: returned in 140.86 seconds.
- mistralai/mistral-large-3-675b-instruct-2512 via NVIDIA: returned in 128.49 seconds.
- moonshotai/kimi-k2.6 via NVIDIA: returned in 73.85 seconds.
- meta/llama-4-maverick-17b-128e-instruct via NVIDIA: returned in 15.42 seconds.

Attempted but not usable in this run:
- deepseek-ai/deepseek-v4-pro via NVIDIA: timeout/error at 180.41 seconds.
- deepseek-ai/deepseek-v4-flash via NVIDIA: timeout/error at 180.41 seconds.
- minimaxai/minimax-m2.7 via NVIDIA: timeout/error at 180.44 seconds.

Model Council synthesis:
- Add a formal portability/bootstrap contract.
- Add schemas for governance status, model reviews, audit records, and portability checks.
- Keep ministries as skills/roles/tags first, not autonomous runtime agents.
- Separate digital-state artifacts from operator-local state.
- Add model review quorum and timeout rules.
- Add read-only checks for forbidden required paths and secret leakage.
- Do not implement runtime guards, dashboards, package changes, or dependency changes yet.

## Architecture

Layer 1: Constitution and policy
Files under specs/ define principles, no-go gates, model council quorum, portability, and safety posture.

Layer 2: Digital-state artifacts
Repository-relative skills, docs, schemas, fixtures, and read-only scripts. These move with the repo.

Layer 3: Operator state
Hermes profiles, ~/.hermes/config.yaml, ~/.hermes/.env, OAuth/auth stores, gateway tokens, and provider credentials. These do not live in repo artifacts and must be restored through Hermes-native flows.

Layer 4: Model Council
A repeatable process that sends compact digests to configured models, records returned/timeouts/errors, and allows synthesis only from returned reviews.

Layer 5: Ministries as roles/skills
Strategy, Operations, Signals, and Audit begin as docs/skills and metadata. They do not spawn autonomous processes in this feature.

Layer 6: Read-only validators
Standard-library scripts validate schemas, portability rules, model review records, and governance status fixtures. They do not enforce runtime actions.

Layer 7: Future runtime enforcement
A later feature may add tool guards, approval policies, package-change gates, and fail-closed enforcement after tests and operator approval.

## Roadmap

Phase 0: Baseline and model-council planning
- Confirm current dirty git state.
- Create model council digest.
- Run all configured/requested models that can be called.
- Record returned/timeouts/errors honestly.
- Update Spec Kit artifacts from returned recommendations.

Phase 1: Portable constitution and schemas
- Finalize constitution/spec/plan/tasks/analyze.
- Add schema drafts under specs/001-hyperagent-governance-integration/schemas/ or docs-governance schema location.
- Define governance-status-v1, model-review-v1, audit-record-v1, portability-check-v1.
- Add fixtures for valid and invalid records.

Phase 2: Docs and governance skill, read-only
- Create docs/governance/digital-state-governance.md.
- Create docs/governance/portable-digital-state.md.
- Create governance-status skill as operator guidance only.
- State clearly that enforcement is not active.

Phase 3: Read-only validators and tests
- Add scripts/governance/read_governance_status.py.
- Add scripts/governance/check_portability.py.
- Add scripts/governance/check_model_council_record.py.
- Add tests for valid/invalid fixtures, forbidden required paths, secret-pattern detection, and model status parsing.

Phase 4: Bootstrap and migration runbook
- Document clone/copy, install Hermes, import/restore profile, restore secrets, run config check, run model smoke tests, run governance validators.
- Optional later script may automate checks, but must remain read-only first.

Phase 5: Enterprise/government hardening
- Add role vocabulary, approval matrix, audit retention guidance, offline mode guidance, model provenance requirements, and incident response runbooks.
- Add compliance mapping docs without claiming certification.
- Current status: initial approval matrix, audit/provenance runbook, bootstrap readiness checklist, compliance mapping, institutional operating model, and space-grade readiness notes are created as docs-only artifacts. They provide critical-grade foundations but do not certify Hermes for regulated or mission-critical use.

Phase 6: Future runtime enforcement feature
- Separate Spec Kit feature only.
- Design guards for terminal/file/package/git/network/model operations.
- Add tests before any enforcement code.
- Fail closed on missing/malformed policy.

## File Targets

Current feature source of truth:
- specs/001-hyperagent-governance-integration/constitution.md
- specs/001-hyperagent-governance-integration/spec.md
- specs/001-hyperagent-governance-integration/plan.md
- specs/001-hyperagent-governance-integration/tasks.md
- specs/001-hyperagent-governance-integration/analyze.md
- specs/001-hyperagent-governance-integration/model-council-digest.md
- specs/001-hyperagent-governance-integration/model-council-results.md
- specs/001-hyperagent-governance-integration/model-council-results.json

Planned portable artifacts:
- docs/governance/digital-state-governance.md
- docs/governance/portable-digital-state.md
- docs/governance/approval-matrix.md
- docs/governance/audit-provenance.md
- docs/governance/bootstrap-readiness.md
- docs/governance/compliance-mapping.md
- docs/governance/institutional-operating-model.md
- docs/governance/space-grade-readiness.md
- skills/devops/governance-status/SKILL.md
- scripts/governance/read_governance_status.py
- scripts/governance/check_portability.py
- scripts/governance/check_model_council_record.py
- tests/scripts/test_governance_status.py
- tests/scripts/test_governance_portability.py

Additional Model Council records:
- specs/001-hyperagent-governance-integration/model-council-phase5-digest.md
- specs/001-hyperagent-governance-integration/model-council-phase5-results.md
- specs/001-hyperagent-governance-integration/model-council-phase5-results.json

Separate future design-only feature:
- specs/002-runtime-governance-guards/ defines guard concepts and required tests but does not authorize runtime code changes.

Do not touch in this feature:
- pyproject.toml
- package.json/package-lock/pnpm/yarn locks
- run_agent.py
- model_tools.py
- terminal/file/patch tool implementations
- gateway runtime
- TUI runtime
- provider runtime code


## Model Benchmark Evidence

Smoke benchmark record:
- specs/001-hyperagent-governance-integration/model-benchmark-smoke-results.json

Deep benchmark record:
- specs/001-hyperagent-governance-integration/model-benchmark-deep-results.json

Latest deep benchmark summary:
- meta/llama-4-maverick-17b-128e-instruct returned 9/9 attempts, averaged about 1.754 seconds, maxed about 3.05 seconds, and remains the best NVIDIA chat/fallback model from current evidence.
- mistralai/mistral-large-3-675b-instruct-2512 returned 8/9 attempts, averaged about 27.949 seconds, had one 180 second timeout, and is better treated as an analysis/council reviewer than first chat fallback.

Operational implication:
- Keep gpt-5.5 as primary chat model.
- Keep Llama 4 Maverick as first NVIDIA fallback.
- Keep Mistral Large 3 as a strong but slower analysis fallback.
- Do not promote timeout-heavy NVIDIA models to default/fallback priority until future benchmark evidence improves.

## Verification Commands

Planning verification:
- git status --short
- python3 -m json.tool specs/001-hyperagent-governance-integration/model-council-results.json

Future validator verification:
- python3 -m compileall scripts/governance tests/scripts
- python3 -m pytest tests/scripts/test_governance_status.py tests/scripts/test_governance_portability.py -q -o 'addopts='
- hermes config check

## Risks

- Over-scoping into runtime enforcement too early.
- Treating timed-out models as reviewers.
- Hardcoding local paths or secrets into portable artifacts.
- Creating ministries as autonomous services before governance is validated.
- Adding dependency churn for schema validation when standard library is enough for the first version.
- Claiming government/space compliance rather than providing auditable foundations.
