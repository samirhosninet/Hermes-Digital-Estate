---
name: governance-status
description: "Read-only guidance for Hermes portable digital-state governance posture."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [governance, portability, audit, digital-state, read-only]
---

# Governance Status

Use this skill when working on Hermes Agent digital-state governance, portability, model council records, audit posture, bootstrap readiness, or institution/government/space-grade operating rules.

## Operating rule

This skill is read-only guidance. It does not mean runtime enforcement is active. Do not claim terminal/file/model/gateway guards exist unless a later Spec Kit feature implements and tests them.

## Source of truth

Read these repo-relative artifacts first:

1. `specs/001-hyperagent-governance-integration/constitution.md`
2. `specs/001-hyperagent-governance-integration/spec.md`
3. `specs/001-hyperagent-governance-integration/plan.md`
4. `specs/001-hyperagent-governance-integration/tasks.md`
5. `specs/001-hyperagent-governance-integration/analyze.md`
6. `docs/governance/digital-state-governance.md`
7. `docs/governance/portable-digital-state.md`
8. `docs/governance/approval-matrix.md`
9. `docs/governance/audit-provenance.md`
10. `docs/governance/bootstrap-readiness.md`
11. `docs/governance/compliance-mapping.md`
12. `docs/governance/institutional-operating-model.md`
13. `docs/governance/space-grade-readiness.md`
14. `docs/governance/risk-taxonomy.md`
15. `docs/governance/maturity-model.md`
16. `docs/governance/evidence-bundle.md`
17. `docs/governance/model-benchmarking.md`
18. `specs/001-hyperagent-governance-integration/model-benchmark-deep-results.json`
19. `docs/governance/runtime-guard-design.md`
20. `docs/governance/terminal-hook-dry-run-design.md`
21. `docs/governance/approval-flow-interaction.md`
22. `docs/governance/log-only-implementation-gate.md`
23. `docs/governance/operator-approval-record.md`
24. `specs/002-runtime-governance-guards/` when discussing future runtime enforcement design

## Posture checklist

- Confirm whether the current phase is planning-only, docs-only, read-only validation, enforcement design, or runtime enforcement.
- Separate portable repo artifacts from operator-local secrets/config/profile state.
- Record model council results honestly: returned, timeout/error, empty, or skipped.
- Use only returned model outputs for synthesis.
- Stop before runtime enforcement unless a separate approved Spec Kit feature exists.
- Reject plans that require external-folder linkage, committed secrets, dependency churn, or untested runtime guards.
- Do not claim certification, accreditation, mission authorization, or safety-critical readiness from docs-only artifacts.

## Recommended commands

- `git status --short`
- `hermes config check`
- `python3 scripts/governance/read_governance_status.py tests/fixtures/governance/valid-status.json`
- `python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/001-hyperagent-governance-integration/schemas`
- `python3 scripts/governance/check_model_council_record.py specs/001-hyperagent-governance-integration/model-council-results.json`
- `python3 scripts/governance/model_benchmark.py --suite smoke --repeat 1 --timeout 60 --max-tokens 32 --output specs/001-hyperagent-governance-integration/model-benchmark-smoke-results.json`
- `python3 scripts/governance/model_benchmark.py --suite all --repeat 3 --timeout 180 --max-tokens 128 --models 'mistralai/mistral-large-3-675b-instruct-2512,meta/llama-4-maverick-17b-128e-instruct' --output specs/001-hyperagent-governance-integration/model-benchmark-deep-results.json`
- `python3 scripts/governance/check_runtime_guard_schema.py specs/002-runtime-governance-guards/fixtures/valid-policy.json`
- `python3 scripts/governance/check_runtime_guard_schema.py specs/002-runtime-governance-guards/fixtures/terminal-hook-dry-run-contract.json`
- `python3 scripts/governance/check_runtime_guard_schema.py specs/002-runtime-governance-guards/fixtures/approval-flow-interaction-contract.json`
- `python3 scripts/governance/check_runtime_guard_schema.py specs/002-runtime-governance-guards/fixtures/log-only-implementation-gate.json`
- `python3 scripts/governance/check_runtime_guard_schema.py specs/002-runtime-governance-guards/fixtures/operator-approval-record.json`
- `python3 -m unittest tests.scripts.test_runtime_guard_scenarios -v`
- `python3 -m unittest tests.scripts.test_terminal_hook_contract -v`
- `python3 -m unittest tests.scripts.test_approval_flow_interaction -v`
- `python3 -m unittest tests.scripts.test_log_only_implementation_gate -v`
- `python3 -m unittest tests.scripts.test_operator_approval_record -v`

## Critical-grade note

For institutions, governments, and space agencies, prefer manual approval gates, least privilege, offline-readable documentation, deterministic bootstrap checks, and explicit operator sign-off for irreversible actions.
