# Tasks: Hermes Portable Digital State

## Phase 0: Baseline and Model Council

T001. Record repository baseline
Files: none
Command: git status --short
Expected: existing dirty state is recorded; unrelated user changes are not overwritten.

T002. Maintain Spec Kit source of truth
Files: specs/001-hyperagent-governance-integration/*
Verification: constitution.md, spec.md, plan.md, tasks.md, analyze.md exist and describe Hermes-native portable digital state.

T003. Generate model council digest
Create/update: specs/001-hyperagent-governance-integration/model-council-digest.md
Verification: digest is compact enough to send to models and contains constraints, current plan, and requested review headings.

T004. Run requested model council
Create/update: model-council-results.md and model-council-results.json
Verification: every requested model is marked returned, timeout/error, empty, or skipped with provider and timing where available.

T005. Synthesize only returned reviews
Modify: plan.md, spec.md, constitution.md, analyze.md
Verification: recommendations from timed-out/error models are not used as if reviewed.

## Phase 1: Constitution, Contract, and Schemas

T006. Finalize portability contract
Modify: spec.md and plan.md
Verification: repo artifacts vs operator-local state are explicitly separated.

T007. Add Model Council quorum rules
Modify: constitution.md, spec.md, plan.md
Verification: plan states minimum preferred reviewers, timeout handling, and no false consensus.

T008. Draft governance-status schema
Create: specs/001-hyperagent-governance-integration/schemas/governance-status-v1.json
Verification: schema describes posture, phase, gates, artifacts, model council summary, and warnings.

T009. Draft model-review schema
Create: specs/001-hyperagent-governance-integration/schemas/model-review-v1.json
Verification: schema supports model, provider, timestamp, status, seconds, error, content_hash, and notes.

T010. Draft audit-record schema
Create: specs/001-hyperagent-governance-integration/schemas/audit-record-v1.json
Verification: schema supports timestamp_utc, actor, artifact_path, event_type, outcome, checksum fields, and notes.

T011. Draft portability-check schema
Create: specs/001-hyperagent-governance-integration/schemas/portability-check-v1.json
Verification: schema supports allowed repo paths, operator-local exclusions, forbidden required paths, and check results.

## Phase 2: Docs and Skill, Read-Only

T012. Create digital-state governance docs
Create: docs/governance/digital-state-governance.md
Verification: explains constitution, ministries, model council, audit office, signals office, no-go gates, and staged enforcement.

T013. Create portable-state guide
Create: docs/governance/portable-digital-state.md
Verification: explains moving to another machine through clone/copy, Hermes install, profile/config/env restoration, checks, and model smoke tests.

T014. Create governance-status skill
Create: skills/devops/governance-status/SKILL.md
Verification: valid YAML frontmatter; says read-only guidance; does not claim runtime enforcement.

T015. Review docs for forbidden dependency claims
Files: docs/governance/*, skills/devops/governance-status/SKILL.md
Verification: docs may mention external inspiration as non-dependency only, never as a required runtime path.

## Phase 3: Read-Only Validators and Tests

T016. Add governance fixture files
Create: tests/fixtures/governance/valid-status.json and invalid fixtures
Verification: fixtures contain no secrets and no machine-specific required paths.

T017. Write failing governance status tests
Create: tests/scripts/test_governance_status.py
Cases: valid status, missing required fields, malformed JSON, model timeout record, stale phase.

T018. Implement read_governance_status.py
Create: scripts/governance/read_governance_status.py
Rules: standard library only; read-only; explicit input path; stable JSON output; non-zero on malformed input.

T019. Write failing portability tests
Create: tests/scripts/test_governance_portability.py
Cases: no required external paths, no committed secret patterns, repo-relative artifact paths, operator-local exclusions.

T020. Implement check_portability.py
Create: scripts/governance/check_portability.py
Rules: standard library only; scans selected repo artifacts; reports JSON; non-zero on required forbidden paths/secrets.

T021. Implement check_model_council_record.py
Create: scripts/governance/check_model_council_record.py
Rules: validates model-council-results.json against model-review expectations and statuses.

T022. Run targeted tests
Command: python3 -m pytest tests/scripts/test_governance_status.py tests/scripts/test_governance_portability.py -q -o 'addopts='
Expected: pass.

## Completed Tasks in Current Pass

Completed:
- T008 through T011: schema drafts created.
- T012 through T015: governance docs and governance-status skill created and checked for portability.
- T016 through T021: fixtures, unittest-compatible tests, and read-only validators created.
- T022: targeted verification passed with unittest because pytest is not installed in this environment.
- T023 through T025: enterprise/government/space-grade planning docs created: approval matrix, audit/provenance runbook, and bootstrap readiness checklist.
- T026 through T028: compliance mapping, institutional operating model, and space-grade readiness docs created as read-only governance artifacts.

Passed commands:
- python3 -m compileall scripts/governance tests/scripts
- python3 -m unittest tests.scripts.test_governance_status tests.scripts.test_governance_portability
- python3 scripts/governance/check_model_council_record.py specs/001-hyperagent-governance-integration/model-council-results.json
- python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/001-hyperagent-governance-integration/schemas
- hermes config check
- Phase 4 verification commands are listed after re-run in the current implementation summary.
- Phase 5 Model Council digest/results created.
- Phase 5 additional hardening docs created: compliance mapping, institutional operating model, space-grade readiness, risk taxonomy, maturity model, and evidence bundle guide.
- Future feature 002 opened as design-only under specs/002-runtime-governance-guards/.

## Phase 4: Enterprise, Government, and Space-Grade Planning

T023. Add approval matrix doc
Create: docs/governance/approval-matrix.md
Status: completed.
Verification: distinguishes read-only, write, destructive, network, package, credential, deployment, and critical-grade actions.

T024. Add audit and provenance runbook
Create: docs/governance/audit-provenance.md
Status: completed.
Verification: defines what must be recorded for model reviews, decisions, approvals, validation runs, incidents, and bootstrap checks.

T025. Add offline/bootstrap readiness checklist
Create: docs/governance/bootstrap-readiness.md
Status: completed.
Verification: supports new machine setup, model readiness classes, readiness levels, and degraded/offline environments without claiming full runtime enforcement.

## Phase 5: Compliance Mapping and Critical-Grade Docs, Read-Only

T026. Add compliance mapping doc
Create: docs/governance/compliance-mapping.md
Status: completed.
Verification: maps governance artifacts to control families without claiming certification or runtime enforcement.

T027. Add institutional operating model
Create: docs/governance/institutional-operating-model.md
Status: completed.
Verification: defines operator, ministries, audit office, model council, deployment classes, and change classes.

T028. Add space-grade readiness notes
Create: docs/governance/space-grade-readiness.md
Status: completed.
Verification: defines conservative mission-readiness levels and prohibited claims without external approval.

## Phase 6: Stop Before Runtime Enforcement

T029. Confirm no runtime files changed
Command: git diff --name-only
Expected: no terminal/file/tool/model/gateway/runtime enforcement files are changed in this feature.

T030. Create future enforcement proposal only if requested
Create: specs/002-runtime-governance-guards/ only after explicit approval
Status: completed as design-only.
Expected: runtime guards are not implemented under feature 001.

T031. Record Phase 5 Model Council
Create: specs/001-hyperagent-governance-integration/phase5-model-council-digest.md, phase5-model-council-results.md, phase5-model-council-results.json
Status: completed.
Verification: returned and timeout models are recorded separately; only returned Kimi K2.6 and Llama 4 Maverick NVIDIA reviews were counted, with gpt-5.5 active synthesis.

T032. Apply returned Phase 5 review fixes
Modify: docs/governance/compliance-mapping.md, docs/governance/institutional-operating-model.md, docs/governance/space-grade-readiness.md, analyze.md
Status: completed.
Verification: added break-glass notes, validator integrity notes, and reduced readiness/certification implication language.

T033. Add final hardening docs and feature 002 design skeleton
Create: docs/governance/risk-taxonomy.md, docs/governance/maturity-model.md, docs/governance/evidence-bundle.md, specs/002-runtime-governance-guards/*
Status: completed.
Verification: docs remain read-only; feature 002 states design-only and no runtime enforcement implemented.

T034. Add model benchmark evidence layer
Create: scripts/governance/model_benchmark.py, tests/scripts/test_model_benchmark.py, docs/governance/model-benchmarking.md, specs/001-hyperagent-governance-integration/schemas/model-benchmark-v1.json, specs/001-hyperagent-governance-integration/model-benchmark-smoke-results.json
Status: completed.
Verification: smoke run records current NVIDIA health; tests validate timeout recommendation and secret-free reports.

T035. Add deep benchmark evidence for healthy NVIDIA models
Create: specs/001-hyperagent-governance-integration/model-benchmark-deep-results.json
Modify: docs/governance/model-benchmarking.md, plan.md, analyze.md, skills/devops/governance-status/SKILL.md
Status: completed.
Verification: deep run used suite all, repeat 3, timeout 180 for Mistral Large 3 and Llama 4 Maverick; results recorded without secrets.
