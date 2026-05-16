
Project: Hermes Agent portable digital-state governance system.
User requirement in Arabic: Build Hermes Agent as an independent digital-state system portable to any machine and suitable for users, institutions, governments, and space agencies. Do NOT link to <external-concept-source>; transfer ideas only into Hermes-native architecture. Use Spec Kit and multi-model planning for maximum quality.

Current constraints:
- Hermes Agent repo path: <repo-root>.
- <external-concept-source> is concept inspiration only, never runtime dependency.
- Portable by design: repo-relative specs/skills/docs/scripts/tests; secrets and machine config stay in Hermes profiles, ~/.hermes/config.yaml, ~/.hermes/.env, OAuth flows.
- Phase 1/2 must be artifact/docs/skill/read-only only. Runtime enforcement/tool guards require separate future Spec Kit feature.
- Avoid dependency manifests, lockfiles, gateway/runtime/tool changes in the first feature.

Ask to model council:
Review and improve the plan for enterprise/government/space-grade portability and governance. Return concise recommendations under these headings:
1. Missing principles
2. Architecture changes
3. Phasing and tasks
4. Security/compliance/audit requirements
5. Portability/installation requirements
6. Risks and no-go gates
7. What should NOT be implemented yet

Existing Spec Kit artifacts:
--- constitution.md ---
     1|# Digital State Governance Constitution
     2|
     3|Feature: 001-hyperagent-governance-integration
     4|Status: planning-only
     5|Intent source: concepts inspired by prior digital-state/governance exploration
     6|Target: Hermes Agent (<repo-root>)
     7|
     8|Portability target: the digital-state system must be self-contained in Hermes Agent artifacts and portable to another machine without any dependency on <external-concept-source> or machine-specific absolute paths.
     9|
    10|## Principles
    11|
    12|1. Ideas, not linkage
    13|The goal is to transfer useful ideas into Hermes Agent as Hermes-native design. Do not create runtime links, imports, dependencies, watchers, sync jobs, or operational coupling to <external-concept-source> or any external folder.
    14|
    15|2. Hermes is the state
    16|Hermes Agent is the runtime and control plane. The "digital state" must be represented through Hermes-native artifacts: Spec Kit files, skills, docs, validators, audit schemas, model-review records, and later separately-approved tool guards.
    17|
    18|3. Read-only first
    19|The first implementation phase must only add documentation, skill guidance, and read-only validators/parsers. It must not execute external code, open gates, start services, modify dependencies, or enforce new command/tool policies at runtime.
    20|
    21|4. Hermes-native integration
    22|Any eventual code must follow Hermes conventions: use get_hermes_home() for Hermes state paths, return JSON strings for tools, keep tool availability gated by check_fn where applicable, and add tests before behavior changes.
    23|
    24|5. Fail-closed design
    25|Any future governance enforcement must default to deny/blocked when policy state is missing, malformed, or ambiguous. Phase 1 may describe this behavior but must not wire enforcement into terminal/file/tool execution.
    26|
    27|6. Spec Kit source of truth
    28|Decisions live in this feature directory: constitution.md, spec.md, plan.md, tasks.md, and analyze.md. Chat transcripts and external reports are not the source of truth.
    29|
    30|7. No dependency churn in Phase 1
    31|Do not edit pyproject.toml, package.json, package-lock.json, pnpm/yarn locks, requirements files, or generated dependency metadata in the first phase.
    32|
    33|8. Portable by design
    34|Every digital-state artifact must be relocatable. Use repository-relative paths for source artifacts and Hermes profile/home mechanisms for operator state. Do not hardcode [windows-drive-mount], [windows-absolute-path], <user-home>, usernames, machine IDs, API keys, tokens, or external drive locations into portable artifacts. Anything secret or machine-local belongs in ~/.hermes/.env, profile config, or operator setup notes, not in repo code/specs.
    35|
--- spec.md ---
     1|# Feature Spec: Hermes Digital State Governance
     2|
     3|## User Story
     4|
     5|As a Hermes Agent operator, I want Hermes to adopt the useful digital-state ideas: constitution, ministries/roles, model council, governance status, audit trail, risk signals, and staged enforcement, so Hermes can become an independent native control plane that can be moved to another machine without linking to or depending on <external-concept-source>.
     6|
     7|## Scope
     8|
     9|In scope for Phase 1:
    10|- Keep Spec Kit artifacts as the source of truth for the digital-state design.
    11|- Add or plan a Hermes-native governance status skill/documentation entry.
    12|- Define the digital-state vocabulary in Hermes terms: constitution, ministries, model council, status, audit, signals, approvals, and no-go gates.
    13|- Define a read-only status/validator design that summarizes Hermes-owned governance artifacts only.
    14|- Define a portability contract so the system can be cloned/exported/imported on another machine using Hermes-native repo files, skills, docs, tests, profiles, and config/env separation.
    15|- Identify exact exclusions and safety gates before implementation.
    16|
    17|Out of scope for Phase 1:
    18|- Linking to <external-concept-source> at runtime.
    19|- Importing modules, configs, AGENTS.md, SOUL.md, .specify, or .agents from any external folder.
    20|- Running external dashboards, executors, agents, ministries, or runtime services.
    21|- Copying package/lock/pyproject files.
    22|- Adding npm/pip dependencies.
    23|- Adding runtime hooks to terminal, patch, write_file, model routing, gateway, or tool dispatch.
    24|- Implementing AG-UI/CopilotKit or dashboard work.
    25|
    26|## Acceptance Criteria
    27|
    28|AC1. The integration has Spec Kit artifacts in specs/001-hyperagent-governance-integration/.
    29|AC2. The plan states that the goal is idea transfer into Hermes-native artifacts, not linking or direct project coupling.
    30|AC3. The first executable work item is read-only and has tests.
    31|AC4. Any future validator works only on Hermes-owned files or explicit test fixtures and does not import from <external-concept-source>.
    32|AC5. The plan records model-review results, including model timeouts, so claims about “all models” are accurate.
    33|AC6. No Phase 1 task edits dependency manifests or starts runtime services.
    34|AC7. The design avoids machine-specific absolute paths and documents how the digital-state artifacts move with Hermes Agent while secrets/config remain outside the repo.
    35|
    36|## Portability Requirements
    37|
    38|- Repo-portable artifacts: specs/, skills/, docs/, scripts/, and tests created for the digital state must use repository-relative paths.
    39|- Operator-local artifacts: API keys, OAuth tokens, provider credentials, platform tokens, and machine-specific config stay in ~/.hermes/.env, ~/.hermes/config.yaml, or exported Hermes profiles, not in committed files.
    40|- Profile portability: the recommended move path is either git clone/pull for source artifacts plus `hermes profile export/import` for operator state, or a documented bootstrap script later if approved.
    41|- No hardcoded external paths: portable artifacts must not require <external-concept-source>, <external-concept-source>, <user-home>, or this specific Windows/WSL mount layout.
    42|
    43|## Digital-State Concepts to Adapt
    44|
    45|Useful concepts to convert into Hermes-native form:
    46|- Constitution: Spec Kit principles and acceptance gates.
    47|- Ministries: role vocabulary for skills, not independent runtime agents.
    48|  - Strategy Ministry: planning, priorities, model council synthesis.
    49|  - Operations Ministry: safe execution readiness and operator runbooks.
    50|  - Signals Ministry: read-only risk scanning and premortem checks.
    51|  - Audit Office: append-only records and decision provenance.
    52|- Model Council: explicit per-model reviews with returned/timeout/error status.
    53|- Governance status: a readable posture summary from Hermes-owned artifacts.
    54|- Sandbox vocabulary: read-only/writable/denied paths, network/process deny-by-default, fail-closed decisions.
    55|- Audit/status JSON schemas.
    56|- Premortem/signals scanner concepts.
    57|
    58|Do not directly transfer as code or behavior in Phase 1:
    59|- dashboards or UI runtimes
    60|- sandbox executor/integration/rollback runtime
    61|- external AGENTS.md/SOUL.md as root instructions
    62|- generated reports wholesale
    63|- external .specify or .agents directories
    64|- dependency manifests/lockfiles
    65|
--- plan.md ---
     1|# Hermes Digital State Governance Plan
     2|
     3|> For Hermes: implement only after this feature's tasks.md and analyze.md are accepted. Use test-driven development and do not skip verification.
     4|
     5|## Clarified Direction
     6|
     7|The goal is not to link Hermes Agent with <external-concept-source>. The goal is to transfer the ideas into Hermes Agent as independent, Hermes-native, portable artifacts and later Hermes-native code. <external-concept-source> is not a dependency, runtime source, import path, sync target, or control plane.
     8|
     9|The target operating model is a portable "digital state" inside Hermes Agent: clone or move the Hermes Agent repo/artifacts to another machine, restore the Hermes profile/config/secrets through Hermes-native mechanisms, and the governance system should still work without any absolute path dependency on this workstation.
    10|
    11|## Model Review Record
    12|
    13|Requested model set:
    14|- gpt-5.5 via openai-codex: returned a usable plan.
    15|- meta/llama-4-maverick-17b-128e-instruct via NVIDIA: returned a usable plan.
    16|- z-ai/glm-5.1 via NVIDIA: attempted; timed out.
    17|- deepseek-ai/deepseek-v4-pro via NVIDIA: attempted; timed out.
    18|- deepseek-ai/deepseek-v4-flash via NVIDIA: attempted; timed out.
    19|- mistralai/mistral-large-3-675b-instruct-2512 via NVIDIA: attempted; timed out in this planning run.
    20|- minimaxai/minimax-m2.7 via NVIDIA: attempted; timed out.
    21|- moonshotai/kimi-k2.6 via NVIDIA: attempted; timed out.
    22|
    23|Only returned outputs are used as recommendations. Timed-out models are recorded as attempted, not as reviewers.
    24|
    25|## Architecture
    26|
    27|Phase 1 is artifact-only/read-only:
    28|1. Spec Kit artifacts define the digital-state constitution, vocabulary, boundaries, and tasks.
    29|2. A Hermes-native governance skill/docs page explains posture from Hermes-owned files.
    30|3. A future optional read-only script parses a Hermes-owned governance status fixture/file and emits JSON.
    31|4. Portability rules separate repo artifacts from local operator state and secrets.
    32|5. Runtime enforcement is postponed until a later feature with separate tests and approval.
    33|
    34|## Target Areas
    35|
    36|Likely files/directories after approval:
    37|- specs/001-hyperagent-governance-integration/: source of truth for this feature.
    38|- skills/devops/governance-status/SKILL.md or skills/software-development/governance-status/SKILL.md: optional read-only skill.
    39|- docs/governance/digital-state-governance.md: operator-facing docs for the adapted concepts.
    40|- docs/governance/portable-digital-state.md: optional move/bootstrap guide for repo artifacts vs Hermes profile/config/secrets.
    41|- scripts/governance/read_governance_status.py: optional read-only parser, no external imports.
    42|- tests/scripts/test_read_governance_status.py or similar: tests for parser output.
    43|
    44|Avoid in Phase 1:
    45|- run_agent.py, model_tools.py, tools/terminal_tool.py, tools/file tools, gateway runtime, TUI, pyproject/package/lockfiles.
    46|- Any import, path dependency, or runtime call to <external-concept-source>.
    47|
    48|## Phases
    49|
    50|Phase 0: Baseline and safety
    51|- Verify current git status before changes.
    52|- Confirm no existing specs directory conflicts.
    53|- Treat all prior/external material as concept inspiration only.
    54|
    55|Phase 1: Spec Kit artifacts
    56|- Create/update constitution.md, spec.md, plan.md, tasks.md, analyze.md.
    57|- Record model-review results honestly.
    58|- Validate that no dependency/runtime files were changed.
    59|
    60|Phase 2: Governance skill/docs only
    61|- Draft a Hermes-native read-only governance-status skill or doc.
    62|- It should explain posture, blocked actions, allowed read-only checks, model-council records, and next safe actions.
    63|- It should include a portability section: repository-relative artifacts move with the repo; secrets/config move through Hermes profile/config/env mechanisms.
    64|- It must not claim enforcement exists.
    65|
    66|Phase 3: Read-only validator script
    67|- If needed, create scripts/governance/read_governance_status.py.
    68|- It reads a provided path or Hermes-owned fixture/status JSON/Markdown.
    69|- It emits stable JSON and exits non-zero for malformed input.
    70|- It imports only Python standard library.
    71|
    72|Phase 4: Tests
    73|- Add tests for parser success, malformed input, missing file, and no external-folder import/path dependency.
    74|- Run targeted tests first, then broader relevant tests.
    75|
    76|Phase 5: Later enforcement design, separate feature
    77|- Only after Phase 1-4 are stable, design runtime guards for terminal/file/package operations.
    78|- This must be a separate Spec Kit feature because it changes tool behavior.
    79|
    80|## Verification Commands
    81|
    82|Before implementation:
    83|- git status --short
    84|- python3 -m compileall scripts/governance tests/scripts if those paths are created
    85|
    86|After adding parser/tests:
    87|- python3 -m pytest tests/scripts/test_read_governance_status.py -q -o 'addopts='
    88|- hermes config check
    89|
    90|## Risks
    91|
    92|- Accidentally treating an external folder as a live dependency instead of concept inspiration.
    93|- Accidentally importing external project instructions into Hermes root behavior.
    94|- Accidentally hardcoding this machine's absolute paths into portable governance artifacts.
    95|- Adding enforcement too early and breaking normal Hermes tool use.
    96|- Copying generated reports or stale governance state as if active.
    97|- Claiming all models reviewed when some timed out.
    98|
--- tasks.md ---
     1|# Tasks: Hermes Digital State Governance
     2|
     3|## Phase 1: Planning artifacts
     4|
     5|T001. Confirm repository baseline
     6|Files: none
     7|Command: git status --short
     8|Expected: record existing dirty state; do not overwrite unrelated user changes.
     9|
    10|T002. Keep this Spec Kit feature directory as source of truth
    11|Files: specs/001-hyperagent-governance-integration/*
    12|Verification: all five artifacts exist: constitution.md, spec.md, plan.md, tasks.md, analyze.md.
    13|
    14|T003. Record model-review status
    15|Files: specs/001-hyperagent-governance-integration/plan.md
    16|Verification: every requested model is listed as either returned, timed out, errored, or skipped.
    17|
    18|T003A. Confirm no-linkage rule
    19|Files: specs/001-hyperagent-governance-integration/*
    20|Verification: artifacts state idea transfer only; no runtime link/import/sync/dependency to <external-concept-source>.
    21|
    22|T003B. Confirm portability rule
    23|Files: specs/001-hyperagent-governance-integration/*
    24|Verification: artifacts state that the digital-state system must be portable through repository-relative files plus Hermes profile/config/env mechanisms, with no machine-specific absolute paths in portable artifacts.
    25|
    26|## Phase 2: Read-only skill/docs
    27|
    28|T004. Draft governance-status skill
    29|Create: skills/devops/governance-status/SKILL.md
    30|Objective: Provide operator guidance for reading Hermes-native governance posture without executing runtime.
    31|Test: validate SKILL.md has YAML frontmatter and does not mention active enforcement.
    32|
    33|T005. Draft governance docs
    34|Create: docs/governance/digital-state-governance.md
    35|Objective: Explain adapted concepts: constitution, ministries as skills/roles, model council, audit trail, signals, no-go gates, and staged enforcement.
    36|Test: grep/check that it labels external digital-state material as concept-only and not a runtime dependency.
    37|
    38|T005A. Draft portability guide
    39|Create: docs/governance/portable-digital-state.md
    40|Objective: Explain how to move the digital state to another machine: clone/copy repo artifacts, install Hermes, restore profile/config via Hermes-native commands, restore secrets via .env/auth flows, run checks, and never rely on absolute workstation paths.
    41|Test: verify the guide does not contain <external-concept-source> as a required path and separates secrets from committed artifacts.
    42|
    43|## Phase 3: Optional read-only validator
    44|
    45|T006. Write failing parser tests
    46|Create: tests/scripts/test_read_governance_status.py
    47|Cases: valid fixture, malformed JSON, missing file, and no external-folder imports/path dependencies.
    48|
    49|T007. Implement parser
    50|Create: scripts/governance/read_governance_status.py
    51|Rules: Python stdlib only; read-only; stable JSON output; non-zero on malformed input.
    52|
    53|T008. Run targeted tests
    54|Command: python3 -m pytest tests/scripts/test_read_governance_status.py -q -o 'addopts='
    55|Expected: pass.
    56|
    57|## Phase 4: Review gates
    58|
    59|T009. Analyze spec/plan/tasks consistency
    60|Files: specs/001-hyperagent-governance-integration/analyze.md
    61|Expected: no unresolved contradictions.
    62|
    63|T010. Stop before runtime enforcement
    64|Objective: Do not edit terminal/file/model/gateway runtime in this feature.
    65|Verification: git diff --name-only contains no runtime enforcement files unless a new approved Spec Kit feature exists.
    66|
--- analyze.md ---
     1|# Analysis: Hermes Digital State Governance
     2|
     3|## Consistency Check
     4|
     5|Constitution vs Spec: aligned. Both require idea transfer only, no runtime linkage, read-only first, no dependency churn, Hermes-native artifacts, and portability across machines without external folder dependencies.
     6|
     7|Spec vs Plan: aligned. The plan starts with Spec Kit artifacts/skill/docs and postpones any enforcement to a later feature.
     8|
     9|Plan vs Tasks: aligned. Tasks include a no-linkage rule, stop before runtime enforcement, and include tests before parser implementation.
    10|
    11|## Clarified User Direction
    12|
    13|The user does not want to connect Hermes Agent to <external-concept-source>. The requested outcome is to move the ideas into Hermes Agent: digital-state governance, ministries as roles/skills, model council, audit/status records, risk signals, staged enforcement, and a portable system that can be moved to another machine.
    14|
    15|## Open Questions
    16|
    17|1. Should the first user-visible artifact be a bundled skill under skills/devops or documentation under docs/governance?
    18|Default: start with docs plus optional skill only if the user wants it available to Hermes sessions.
    19|
    20|2. Should governance status read from a fixed Hermes-owned file or an explicit path argument?
    21|Default: explicit path argument for tests and safety; no global state dependency in Phase 1.
    22|
    23|3. Should model timeouts block the plan?
    24|Default: no. Record timeouts honestly and use only returned recommendations.
    25|
    26|4. Should portability be implemented as a script now?
    27|Default: no for Phase 1. First document the portability contract. A bootstrap/export helper can be a later task after docs and read-only validation exist.
    28|
    29|## No-Go Conditions
    30|
    31|Do not implement if the requested next step requires:
    32|- linking Hermes to <external-concept-source> at runtime
    33|- running external runtime/dashboard/executors
    34|- copying external AGENTS.md into Hermes root behavior
    35|- importing modules/config from external folders
    36|- modifying dependency manifests
    37|- wiring guards into terminal/file tools before a separate enforcement spec exists
    38|- hardcoding this workstation's absolute paths into portable governance artifacts
    39|
    40|## Ready for Implementation?
    41|
    42|Ready for Phase 2 only after user approval. Phase 2 may create docs and/or a governance-status skill. Runtime enforcement is not approved by this feature.
    43|
