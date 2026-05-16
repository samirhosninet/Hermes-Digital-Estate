# Analyze: Runtime Governance Guards

## Design Consistency Check

The feature has advanced from design-only into a minimal, non-integrated guard core:

- no tool dispatch hooks are changed
- no gateway/model-routing hooks are changed
- no dependencies are added
- no lockfiles are modified
- no external folder dependency exists
- no live enforcement claim is made

## Open Questions Before Implementation

1. Where should portable policy live?
   - Candidate: repo policy under `config/governance/`
   - Concern: local deployments may need stricter operator-local overlays.

2. Which mode should exist first?
   - Candidate: dry-run/log-only before enforcement.
   - Concern: high-risk actions should not be described as protected until fail-closed tests exist.

3. How should policy interact with existing Hermes approvals?
   - Candidate: governance guard classifies/escalates; existing approval UI collects confirmation.
   - Concern: duplicate prompts or bypasses.

4. What should audit records store?
   - Candidate: summarized action, boundary, risk class, decision, policy version, timestamp.
   - Concern: raw command/output may contain secrets.

5. What should trigger escalation?
   - Candidate: any durable-state, external-system, credential, billing, deployment, model-routing, gateway, cron/webhook, or ambiguous side effect.
   - Concern: over-escalation can frustrate operators, while under-escalation can bypass governance.

6. How is portability verified?
   - Candidate: reject required absolute paths and ensure repo artifacts remain portable while operator-local overlays stay optional.
   - Concern: strict policies may accidentally encode one workstation's paths.

## Required Tests Before Any Runtime Code

- missing policy in strict mode fails closed
- malformed policy fails closed
- destructive shell commands escalate or deny
- credential paths escalate or deny
- safe read-only commands allow
- package/lockfile changes escalate
- git reset/push escalate or deny
- deployment/gateway fanout escalates
- audit records are emitted without secrets

## No-Go Findings

Do not:

- implement hooks before tests
- treat docs as enforcement
- store secrets in audit records
- modify package files as part of the first guard pass
- make mission-grade claims without independent assessment

## Model Council Synthesis

Feature 002 Model Council was attempted against the configured model set and recorded in `model-council-results.json`. Returned reviews supported caution, a narrow slice, and no broad runtime hooks. The usable review highlighted these gaps:

- escalation criteria must be specific before implementation
- portability verification must be testable
- secret/sensitive payload definitions must be explicit before audit logging
- future guards must integrate with existing Hermes approvals rather than bypass or duplicate them unsafely
- the first implementation slice should be narrow and test-first, not a broad hook across every tool

## Phase 2A Schema Analysis

The schemas reduce ambiguity before implementation by making policy, decision, and audit contracts explicit. Remaining constraints:

- the schemas are design contracts only; no runtime guard hook is active
- policy grammar is intentionally small until implementation is approved
- audit records require redacted summaries and action hashes, not raw payloads
- any future strict mode must fail closed when policy is missing, malformed, or ambiguous
- validator coverage is stdlib-only so the portable digital state does not gain dependencies

## Phase 2B Design Document Analysis

`docs/governance/runtime-guard-design.md` fills the operator-facing gap between schemas and future implementation. It documents the lifecycle in plain language:

- proposed action
- classification
- policy load
- decision
- approval handoff
- audit record
- outcome

The document remains explicitly non-enforcing and keeps runtime hooks behind a future approval gate.

## Phase 2C Model Benchmark Analysis

`docs/governance/model-benchmarking.md` and `scripts/governance/model_benchmark.py` add an evidence layer for Model Council readiness and timeout decisions. The current smoke report shows that, at a 60 second timeout, `mistralai/mistral-large-3-675b-instruct-2512` and `meta/llama-4-maverick-17b-128e-instruct` returned quickly, while GLM, DeepSeek Pro, DeepSeek Flash, MiniMax, and Kimi timed out in this point-in-time run.

This must not be interpreted as permanent model quality. It only means current provider health did not support counting those timeout models as reviewers for that run. The next benchmark step should be `--suite all --repeat 3` for the returned models, and longer isolated tests for the timeout-heavy models only if their expected value justifies the wait.

## Phase 3 Non-Integrated Core Analysis

The pure core now includes a terminal dry-run action classifier that converts proposed command text into a portable action record without executing anything. Covered examples are:

- `pwd` -> terminal/read_only
- `pip install requests` -> package/package_mutation
- `git reset --hard HEAD~1` -> git_destructive/git_destructive

The classifier is intentionally not a terminal hook. It is evidence for future hook design only. The schema checker now validates dry-run action fixtures as portable evidence, while runtime behavior remains unchanged.

## Current Recommendation

Keep the current core unhooked. T019 and T020 are now complete as dry-run/log-only design contracts, not runtime implementations. The next safe step is to design the first log-only implementation gate and operator approval criteria before editing any runtime terminal dispatch file.

## Phase 4 Terminal Hook Contract Analysis

T019 added a contract and operator-facing design for a future terminal hook:

- `docs/governance/terminal-hook-dry-run-design.md`
- `schemas/terminal-hook-dry-run-contract-v1.json`
- `fixtures/terminal-hook-dry-run-contract.json`
- `fixtures/terminal-hook-dry-run-audit-sample.json`
- `tests/scripts/test_terminal_hook_contract.py`

The contract deliberately proves what must not happen in the first integration slice: no runtime enforcement, no command blocking, no mutation or reordering of terminal execution, and no bypass of existing approvals. This keeps the digital-state guard architecture evidence-oriented while avoiding a false claim that terminal protection is already active.

Before T020 could edit any runtime terminal file, the plan needed approval-flow interaction tests that prove dry-run logging coexists with Hermes approvals and has an explicit rollback/disable path. T020 now provides those tests and contracts without runtime integration.

## Phase 4 Approval Flow Interaction Analysis

T020 added a design-only approval-flow interaction contract:

- `docs/governance/approval-flow-interaction.md`
- `schemas/approval-flow-interaction-contract-v1.json`
- `fixtures/approval-flow-interaction-contract.json`
- `fixtures/approval-flow-dry-run-audit-sample.json`
- `tests/scripts/test_approval_flow_interaction.py`

The contract prevents the most dangerous integration mistakes before any hook is written: duplicate approval prompts, bypassing existing approvals, blocking commands in dry-run mode, changing terminal execution flow, and failing closed incorrectly on audit-write errors. It also defines a future disable flag and requires approval failures to defer to the existing approval flow.

## Phase 4 Log-Only Implementation Gate Analysis

T021A adds the final design gate before any runtime terminal touchpoint can be considered:

- `docs/governance/log-only-implementation-gate.md`
- `schemas/log-only-implementation-gate-v1.json`
- `fixtures/log-only-implementation-gate.json`
- `tests/scripts/test_log_only_implementation_gate.py`

The gate prevents accidental enforcement creep by requiring log-only mode, no command blocking, no execution-flow changes, explicit operator approval, passing terminal-hook and approval-flow contracts, portability verification, and a documented rollback path. It also states that governance logging failure must continue without governance blocking in this phase.

This keeps the next possible implementation slice narrow and reversible: one log-only touchpoint, no command mutation, no duplicate approval prompt, and a feature-flag disable path before activation.

## Phase 4 Operator Approval Record Analysis

T021B adds the explicit operator approval record gate:

- `docs/governance/operator-approval-record.md`
- `schemas/operator-approval-record-v1.json`
- `fixtures/operator-approval-record.json`
- `tests/scripts/test_operator_approval_record.py`

The current record intentionally grants no runtime approval. It keeps terminal, file, gateway, model routing, cron, and approvals runtime out of scope and requires reapproval for any runtime file edit, command-blocking behavior, terminal execution-flow change, new approval prompt, audit storage change, or expansion beyond log-only scope.

This closes a governance gap: the system can now distinguish “design artifacts exist” from “operator approved a runtime touchpoint.” Until a future operator approval record changes scope from `none` to a named log-only touchpoint, runtime integration remains blocked.

## Phase 2D Dry-Run Scenario Fixture Analysis

The scenario fixtures make expected decisions concrete before any runtime hook is allowed:

- safe read-only terminal inspection -> allow
- package mutation -> escalate
- credential/secret path access -> deny
- missing policy in strict mode -> fail_closed

This improves reviewability for institutions/governments/space-grade operators because the decision vocabulary is now backed by portable examples and tests, not only prose. The fixtures remain design evidence only and must not be presented as active protection.

