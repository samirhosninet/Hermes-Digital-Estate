# Tasks: Runtime Governance Guards

## Phase 0: Design Baseline

T001. Record design-only boundary
Files: constitution.md, spec.md, plan.md
Verification: all files state no runtime enforcement is implemented yet.
Status: completed.

T002. Identify candidate enforcement boundaries
Files: spec.md, plan.md
Verification: terminal, file, package, git, credential, network/deployment, model routing, gateway, cron/webhook are listed as candidates.
Status: completed.

T003. Define decision vocabulary
Files: spec.md
Verification: allow, deny, escalate, and fail_closed are defined.
Status: completed.

## Phase 1: Review Before Implementation

T004. Create Model Council digest for feature 002
Create: model-council-digest.md
Verification: digest summarizes design-only scope and asks for no-go warnings.
Status: completed.

T005. Run Model Council for feature 002
Create: model-council-results.json and model-council-results.md
Verification: every requested model is marked returned, timeout/error, empty, or skipped.
Status: completed.

T006. Analyze gaps
Modify: analyze.md
Verification: contradictions, missing tests, and risky enforcement assumptions are listed.
Status: completed.

T006A. Add missing design criteria from Model Council
Modify: spec.md, plan.md, analyze.md
Verification: escalation criteria, portability criteria, secret/sensitive payload definition, and first implementation slice are documented.
Status: completed.

## Phase 2A: Design Schemas, Still No Runtime Hooks

T010. Draft portable runtime guard policy schema
Files: schemas/runtime-guard-policy-v1.json, fixtures/valid-policy.json
Verification: check_runtime_guard_schema.py accepts valid policy and fails closed on missing rules.
Status: completed.

T011. Draft decision and audit record schemas
Files: schemas/runtime-guard-decision-v1.json, schemas/runtime-guard-audit-record-v1.json, fixtures/valid-decision.json, fixtures/valid-audit-record.json
Verification: checker accepts valid fixtures and rejects secret-like audit summaries.
Status: completed.

T012. Add read-only schema validator and tests
Files: scripts/governance/check_runtime_guard_schema.py, tests/scripts/test_runtime_guard_schema.py
Verification: unittest passes without adding dependencies.
Status: completed.

## Phase 2B: Operator-Readable Design, Still No Runtime Hooks

T013. Add runtime guard design document
Files: docs/governance/runtime-guard-design.md
Verification: document explains proposed action -> classification -> policy load -> decision -> approval handoff -> audit -> outcome.
Status: completed.

T014. Clean Feature 002 Spec Kit artifacts
Files: spec.md, plan.md, tasks.md, analyze.md
Verification: artifacts are readable markdown without accidental line-number prefixes and still state design-only boundary.
Status: completed.

T015. Update governance-status skill source list
Files: skills/devops/governance-status/SKILL.md
Verification: skill points to runtime-guard-design.md and the runtime guard schema validator.
Status: completed.

## Phase 2C: Model Benchmark Evidence, Still No Runtime Hooks

T015A. Add portable model benchmark utility
Files: scripts/governance/model_benchmark.py, tests/scripts/test_model_benchmark.py
Verification: unittest covers timeout recommendation, summaries, and secret-free reports.
Status: completed.

T015B. Add benchmark documentation and schema
Files: docs/governance/model-benchmarking.md, specs/001-hyperagent-governance-integration/schemas/model-benchmark-v1.json
Verification: docs define readiness classes and benchmark reports remain portable evidence.
Status: completed.

T015C. Run smoke benchmark for current NVIDIA council models
Files: specs/001-hyperagent-governance-integration/model-benchmark-smoke-results.json
Verification: report records returned models and timeout/error models without secrets.
Status: completed.


## Phase 2D: Dry-Run Decision Scenarios, Still No Runtime Hooks

T015D. Add dry-run decision scenario fixtures
Files: specs/002-runtime-governance-guards/fixtures/scenarios/*.json
Verification: scenarios cover allow, escalate, deny, and fail_closed outcomes.
Status: completed.

T015E. Add scenario fixture tests
Files: tests/scripts/test_runtime_guard_scenarios.py
Verification: unittest validates all scenario fixtures with the runtime guard schema checker.
Status: completed.

## Phase 3: Minimal Non-Integrated Core, No Runtime Hooks

T016. Treat operator continuation as approval for pure core only
Files: constitution.md, spec.md, plan.md, tasks.md, analyze.md
Verification: artifacts distinguish pure core from runtime enforcement.
Status: completed.

T017. Write tests before guard core implementation
Files: tests/agent/test_runtime_governance.py
Verification: tests failed before missing APIs were implemented.
Status: completed.

T018. Implement minimal dry-run guard core
Files: agent/runtime_governance.py, tests/agent/test_runtime_governance.py, specs/002-runtime-governance-guards/fixtures/dry-run-*.json
Verification: policy parser, decision engine, terminal dry-run classifier, action fixtures, and audit builder pass tests without hooking runtime tools.
Status: completed.

T018A. Validate dry-run action fixtures
Files: scripts/governance/check_runtime_guard_schema.py, tests/scripts/test_runtime_guard_schema.py
Verification: schema checker accepts dry_run_terminal_classification action fixtures and rejects malformed governance records.
Status: completed.

## Phase 4: Runtime Hook Gate, Not Yet Approved

T019. Design terminal hook dry-run integration
Files: docs/governance/terminal-hook-dry-run-design.md, schemas/terminal-hook-dry-run-contract-v1.json, fixtures/terminal-hook-dry-run-contract.json, fixtures/terminal-hook-dry-run-audit-sample.json, tests/scripts/test_terminal_hook_contract.py
Verification: contract has hook-specific tests, validator support, and proves no execution-flow change.
Status: completed.

T020. Design approval-flow interaction for dry-run/log-only mode
Files: docs/governance/approval-flow-interaction.md, schemas/approval-flow-interaction-contract-v1.json, fixtures/approval-flow-interaction-contract.json, fixtures/approval-flow-dry-run-audit-sample.json, tests/scripts/test_approval_flow_interaction.py
Verification: contract proves no duplicate approval prompt, no approval bypass, no command blocking, no execution-flow change, and explicit disable/failure behavior.
Status: completed.

T021A. Design log-only implementation gate before any runtime touchpoint
Files: docs/governance/log-only-implementation-gate.md, schemas/log-only-implementation-gate-v1.json, fixtures/log-only-implementation-gate.json, tests/scripts/test_log_only_implementation_gate.py
Verification: contract proves log-only mode cannot block commands, cannot change terminal execution flow, requires explicit operator approval, and defines rollback before any runtime file is touched.
Status: completed.

T021B. Add operator approval record gate
Files: docs/governance/operator-approval-record.md, schemas/operator-approval-record-v1.json, fixtures/operator-approval-record.json, tests/scripts/test_operator_approval_record.py
Verification: record explicitly grants no current runtime touchpoint, keeps terminal/file/gateway/model routing out of scope, and requires reapproval before any runtime file edit or scope expansion.
Status: completed.

T021. Enforce high-risk actions
Files: future runtime files only after explicit approval
Verification: fail-closed and deny/escalate behavior proven at real hook boundaries.
Status: blocked.
