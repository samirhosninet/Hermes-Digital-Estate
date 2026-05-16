# Tasks: Portable Digital-State Distribution

## Phase 0: Spec Kit Planning

T001. Create Feature 003 Spec Kit directory
Files: `specs/003-portable-digital-state-distribution/`
Status: completed.
Verification: directory contains constitution/spec/plan/tasks/analyze/model-council-digest.

T002. Capture upstream-safe workspace decision
Files: constitution.md, spec.md, plan.md
Status: completed.
Verification: artifacts state official Hermes Agent remains base; Digital State is installed as a Hermes Profile Distribution and operated through Hermes Workspace.

T003. Define no-go gates
Files: constitution.md, plan.md
Status: completed.
Verification: no core runtime, no separate UI, no dependencies, no secrets, no machine-specific paths.

T003A. Align Feature 003 with Hermes Profile Distributions
Files: spec.md, plan.md, tasks.md, analyze.md, model-council-digest.md
Status: completed.
Verification: canonical path is `hermes profile install/update`; custom import/export is secondary only.

## Phase 1: Distribution and Manifest Contract

T004. Draft profile distribution contract schema
Create: `specs/003-portable-digital-state-distribution/schemas/profile-distribution-contract-v1.json`
Status: completed.
Expected: defines required `distribution.yaml` fields, source metadata, included assets, required env var names, update policy, and no-secret constraints.
Verification: schema file exists and is used by distribution/bootstrap tests.

T005. Draft manifest schema
Create: `specs/003-portable-digital-state-distribution/schemas/digital-state-manifest-v1.json`
Status: completed.
Expected: defines pack metadata, allowed artifact roots, excluded paths, checks, modes, local credentials names, GitHub source metadata, and compatibility notes.
Verification: schema file exists and manifest validates through `bootstrap_digital_state.py`.

T006. Create initial distribution files
Create: `distribution.yaml`, `.env.EXAMPLE`, `SOUL.md`, and profile `config.yaml`.
Status: completed.
Expected: profile distribution can be inspected without secrets and points users to official Hermes install first.
Verification: `distribution.yaml` is parsed by tests; `.env.EXAMPLE` contains names only; `config.yaml` has safe profile defaults.

T007. Create initial manifest
Create: `digital-state.manifest.json`
Status: completed.
Expected: lists current portable profile artifacts and excludes secrets/config/logs/sessions/auth/profile archives.
Verification: `python3 scripts/governance/bootstrap_digital_state.py --json` returns ok true.

T008. Add distribution/manifest tests
Create: `tests/scripts/test_digital_state_distribution.py`
Status: completed.
Expected cases: valid distribution, missing required fields, forbidden absolute path, forbidden secret-bearing path, real `.env` rejection.
Verification: `python3 -m unittest tests.scripts.test_digital_state_distribution -v` passes.

T009. Add distribution/manifest validator or integrate with bootstrap
Create or modify: `scripts/governance/bootstrap_digital_state.py`
Status: completed.
Expected: validates manifest/distribution shape using stdlib only.
Verification: bootstrap validates manifest, distribution metadata, required files, no-secret policy, and portable content scan.

## Phase 2: Bootstrap Checker

T010. Write bootstrap checker tests first
Create: `tests/scripts/test_bootstrap_digital_state.py`
Cases: clean workspace/profile, missing required artifact, forbidden local path, secret-like content, JSON output.

T011. Implement bootstrap checker
Create: `scripts/governance/bootstrap_digital_state.py`
Rules: read-only; repo-relative; stdlib-only; JSON output; non-zero on failed required checks.

T012. Wire existing validators into bootstrap
Modify: `bootstrap_digital_state.py`
Expected: can call or reuse portability/model-council/runtime-schema checks without exposing secrets.

## Phase 3: GitHub Distribution Maintenance

T013. Create GitHub distribution maintenance guide
Create: `docs/governance/github-distribution-maintenance.md`
Expected: repository layout, release tags, changelog, compatibility notes, update flow, rollback guidance.

T014. Add release checklist
Create or modify: `docs/governance/github-distribution-maintenance.md`, `digital-state.manifest.json`
Status: completed.
Expected: maintainers can release updates without changing Hermes core.
Verification: `docs/governance/e2e-fullstack-release.md` is required by manifest and covered by distribution tests.

T014A. Add end-to-end full-stack release runbook
Create: `docs/governance/e2e-fullstack-release.md`
Status: completed.
Expected: documents workspace development, staging distribution, local profile install, chat smoke test, GitHub publish, GitHub install, update, rollback, and CI gates.
Verification: `tests/scripts/test_digital_state_distribution.py` asserts the runbook is required and contains the profile install/staging/GitHub flow.

T015. Add update path validation notes
Create or modify: `docs/governance/update-and-recovery.md`
Expected: users update Digital State via `hermes profile update <name>` and update Hermes separately via official Hermes update flow.

## Phase 4: Optional Support Export/Import Tools

T016. Decide whether offline export/import is needed for Phase 003
Files: plan.md, analyze.md
Expected: if implemented, mark as optional support/evidence bundle tooling only.

T017. Write export tests first if approved
Create: `tests/scripts/test_export_digital_state.py`
Cases: allowed files included, excluded paths excluded, secrets excluded, unsafe output path refused, archive contains manifest.

T018. Implement export tool if approved
Create: `scripts/governance/export_digital_state.py`
Rules: explicit output path; include only manifest allowlist; refuse path traversal; no secrets; deterministic enough for repeatable validation.

T019. Write import tests first if approved
Create: `tests/scripts/test_import_digital_state.py`
Cases: dry-run import, safe extraction, path traversal rejected, absolute paths rejected, overwrite policy respected, secrets not imported.

T020. Implement import tool if approved
Create: `scripts/governance/import_digital_state.py`
Rules: default dry-run or explicit `--apply`; explicit destination; inspect manifest before extract; no secrets import.

## Phase 5: User and Institution Documentation

T021. Create user quickstart
Create: `docs/governance/start-here.md`, `docs/governance/user-quickstart.md`
Status: completed.
Expected: official Hermes install -> `hermes profile install` Digital State -> bootstrap -> add credentials -> use workspace/profile.
Verification: docs are listed in `digital-state.manifest.json` required files and covered by `tests/scripts/test_digital_state_distribution.py`.

T022. Create institution installation guide
Create: `docs/governance/institution-installation.md`
Expected: roles, profiles, local secrets, audit/evidence bundle, model readiness, no certification claims.

T023. Create update and recovery guide
Create: `docs/governance/update-and-recovery.md`
Expected: update Hermes, update Digital State profile distribution, rerun checks, recover after deletion, migrate machine, troubleshoot failed bootstrap.

## Phase 5A: Fixed Model Ministry Routing

T023A. Add no-fallback model ministry routing contract
Files: `docs/governance/model-ministry-routing.md`, `specs/003-portable-digital-state-distribution/schemas/model-ministry-routing-v1.json`, `specs/003-portable-digital-state-distribution/fixtures/model-ministry-routing.json`, `config.yaml`, `tests/scripts/test_model_ministry_routing.py`
Status: completed.
Verification: each ministry has one assigned model, `fallback_enabled` is false, profile config declares `digital_state.model_ministries`, and `deepseek-ai/deepseek-v4-pro` is reserve/not_launch_ready rather than launch-critical.

T023B. Run no-fallback ministry readiness test before GitHub
Files: `specs/003-portable-digital-state-distribution/model-ministry-readiness.md`, `model-ministry-readiness-results.json`, `model-ministry-readiness-glm-retry.json`
Status: completed.
Verification: launch-critical ministries returned without fallback substitution; non-critical slow/experimental ministries are documented honestly.

## Phase 6: Model Council Review

T024. Create model council digest
Create: `specs/003-portable-digital-state-distribution/model-council-digest.md`
Status: completed initial digest; updated for Profile Distribution decision.
Expected: compact prompt for review of GitHub profile distribution design.

T025. Run Model Council when requested
Create: `model-council-results.md`, `model-council-results.json`
Expected: every model marked returned, timeout, error, empty, or skipped; only returned reviews influence plan.

T026. Synthesize returned reviews
Modify: plan.md, spec.md, analyze.md, tasks.md
Expected: no recommendations from timed-out/error models are treated as reviewed.

## Phase 7: Validation and Update-Safety

T027. Run targeted tests
Commands:
- `python3 -m unittest tests.scripts.test_digital_state_distribution tests.scripts.test_bootstrap_digital_state`
Expected: pass after implementation.

T028. Run portability check
Command:
- `python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs scripts/governance tests/scripts tests/fixtures`
Expected: portable true; no required forbidden paths/secrets.

T029. Run config check
Command:
- `hermes config check`
Expected: config ok.

T030. Confirm no Hermes core runtime changes
Command:
- `git diff --name-only`
Expected: Feature 003 changes remain in distribution/docs/specs/scripts/tests; no terminal/file/gateway/model-routing runtime edits.

## Explicitly Out of Scope

- Standalone UI/dashboard.
- Runtime enforcement.
- Terminal/file/gateway/model-routing hooks.
- Package dependency changes.
- Lockfile changes.
- Shipping credentials or local profiles inside the distribution.
- Custom install/update mechanism as the primary path when Hermes Profile Distributions can handle it.

T015A. Add update-safety contract
Files: `docs/governance/update-and-recovery.md`, `docs/governance/github-distribution-maintenance.md`, `specs/003-portable-digital-state-distribution/schemas/update-safety-contract-v1.json`, `specs/003-portable-digital-state-distribution/fixtures/update-safety-contract.json`, `digital-state.manifest.json`, `tests/scripts/test_digital_state_distribution.py`
Status: completed.
Verification: targeted distribution tests assert that Digital State updates use `hermes profile update digital-state`, runtime/core changes are forbidden in Feature 003, update docs are required files, and rollback uses versioned GitHub tags.
