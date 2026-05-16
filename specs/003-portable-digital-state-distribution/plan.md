# Plan: Portable Digital-State Distribution

## Goal

Turn the Hermes digital-state layer into an upstream-safe, GitHub-hosted Hermes Profile Distribution that users can install, update, bootstrap-check, and operate through official Hermes Workspace without forking or breaking upstream Hermes Agent.

The primary user path is:

1. Install official Hermes Agent from NousResearch.
2. Install the Digital State Distribution from GitHub using Hermes profile distribution commands.
3. Run bootstrap checks.
4. Add local credentials/config/profile state.
5. Use Hermes Workspace, CLI, skills, docs, scripts, and future Hermes-native commands.
6. Receive updates through the Digital State distribution repository without modifying Hermes core.

## Current Decision

Focus on Hermes Workspace and official Hermes Agent. Do not create a separate UI and do not fork Hermes core. Feature 003 is a GitHub distribution and onboarding layer built on Hermes Profile Distributions.

The Digital State model architecture is fixed ministry-model routing, not fallback routing. Each ministry has one assigned model, and readiness tests must evaluate that ministry model directly. If a ministry model times out, the failure is recorded for that ministry; another model is not substituted.

`import_digital_state.py` and `export_digital_state.py`, if implemented, are support/backup tools only. The canonical installation and update path should be Hermes profile distribution:

- `hermes profile install <github-or-local-distribution> --alias <name>`
- `hermes profile update <name>`
- `hermes profile info <name>`
- `hermes -p <name> chat` or distribution alias wrappers

## Architecture

### Layer 1: Official Hermes Agent

Installed and updated by the user through official Hermes installation/update flows. Hermes core remains upstream-owned and updateable.

### Layer 2: Digital State GitHub Repository

A separate GitHub project/repository containing the portable distribution source. It should be versioned, tagged, reviewed, and updated independently from official Hermes Agent.

Recommended repository contents:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml` with non-secret defaults only
- `.env.EXAMPLE` with required variable names only
- `README.md`
- `CHANGELOG.md`
- `docs/governance/`
- `skills/`
- `specs/`
- `scripts/governance/`
- `tests/`
- `digital-state.manifest.json`

### Layer 3: Hermes Profile Distribution

The Digital State project is installed into Hermes as a profile distribution. This gives users a clean profile boundary and an update path managed by Hermes profile commands instead of ad-hoc copying.

The distribution profile should carry:

- governance skills as ministries
- SOUL/instructions for the digital-state persona
- non-secret config defaults
- docs and bootstrap scripts
- optional cron/MCP templates only if disabled or clearly opt-in

### Layer 4: Operator Local State

Not part of the distribution repository and not part of shipped archives:

- API keys
- OAuth/auth stores
- gateway tokens
- `.env` real values
- local `~/.hermes/config.yaml`
- sessions
- logs
- memories
- unsanitized profile archives
- machine-specific paths

Each user/institution creates this state locally after installation.

### Layer 5: Bootstrap and Evidence

Bootstrap scripts validate readiness but do not mutate runtime. Evidence artifacts prove distribution contents, validation outcomes, model readiness, and portability posture.

### Layer 6: Future Hermes-Native UX

Later feature may add:

- `hermes digital-state status`
- `hermes digital-state bootstrap`
- `hermes digital-state export`
- `hermes digital-state import`
- slash commands such as `/digital-state status`

This is not part of Feature 003 unless explicitly approved later.

## Implementation Phases

### Phase 0: Spec Kit planning

Create this feature directory and artifacts:

- constitution
- spec
- plan
- tasks
- analyze
- model-council digest

Status: completed.

### Phase 1: Distribution contract

Create:

- `distribution.yaml` for Hermes Profile Distribution
- `SOUL.md` for profile identity and operating principles
- `.env.EXAMPLE` with optional credential names only
- `config.yaml` with safe non-secret profile defaults
- `digital-state.manifest.json`
- schema `specs/003-portable-digital-state-distribution/schemas/digital-state-manifest-v1.json`
- schema `specs/003-portable-digital-state-distribution/schemas/profile-distribution-contract-v1.json`
- `scripts/governance/bootstrap_digital_state.py`
- `tests/scripts/test_digital_state_distribution.py`

Required distribution fields/concerns:

- profile/distribution name
- version
- compatible Hermes notes
- included skills/docs/scripts/specs/003
- non-secret config defaults
- required environment variables as names only
- update policy
- forbidden paths and secrets
- supported deployment modes
- GitHub source metadata

Status: completed.

Verification completed:

- `python3 -m unittest tests.scripts.test_digital_state_distribution -v`
- `python3 scripts/governance/bootstrap_digital_state.py --json`
- `hermes config check`

Design note: the initial installable profile distribution deliberately ships current operational governance artifacts and Feature 003 distribution artifacts. Older development histories/model-council records from Feature 001/002 are not included as core distribution-owned paths because they can contain historical, non-portable examples and are not required for non-technical user onboarding.

### Phase 2: Bootstrap checker

Create:

- `scripts/governance/bootstrap_digital_state.py`
- tests for success/failure modes

Behavior:

- read manifest and distribution metadata
- verify required files exist
- verify no forbidden paths/secrets in portable artifacts
- verify validators are present
- optionally run selected validators
- output JSON and human summary
- read-only

### Phase 3: GitHub release/update workflow documentation

Create docs and checks for:

- repository layout
- semantic versioning or date/version tags
- changelog entries
- release checklist
- compatibility notes
- `hermes profile update` path
- rollback/reinstall guidance

### Phase 4: Optional support export/import tools

Optional, not canonical:

- `scripts/governance/export_digital_state.py`
- `scripts/governance/import_digital_state.py`

Use cases:

- offline transfer
- institutional review bundle
- backup of distribution artifacts

Rules:

- official Hermes profile distribution remains primary
- export includes only manifest-allowed paths
- import defaults to dry-run and requires explicit apply
- never import secrets automatically

### Phase 5: User and institution documentation

Create:

- `docs/governance/start-here.md`
- `docs/governance/user-quickstart.md`
- `docs/governance/institution-installation.md`
- `docs/governance/update-and-recovery.md`
- `docs/governance/github-distribution-maintenance.md`

Status: user-facing non-technical start docs are implemented and included in the manifest required files.

Documentation must show the official Hermes-first flow:

1. install official Hermes
2. install Digital State profile distribution from GitHub
3. bootstrap
4. add local credentials
5. run checks
6. use workspace/profile
7. update via Hermes profile update

### Phase 6: Model Council review

Create:

- `model-council-digest.md`
- `model-council-results.md`
- `model-council-results.json`

Record each requested model as returned, timeout, error, empty, or skipped. Use only returned reviews in synthesis.

### Phase 7: Validation

Run:

- `python3 -m compileall scripts/governance tests/scripts tests/agent agent`
- targeted unittest or pytest tests available in this environment
- `python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs scripts/governance tests/scripts tests/fixtures`
- distribution/manifest/bootstrap validators after they exist
- `hermes config check`

## File Targets

Feature source of truth:

- `specs/003-portable-digital-state-distribution/constitution.md`
- `specs/003-portable-digital-state-distribution/spec.md`
- `specs/003-portable-digital-state-distribution/plan.md`
- `specs/003-portable-digital-state-distribution/tasks.md`
- `specs/003-portable-digital-state-distribution/analyze.md`
- `specs/003-portable-digital-state-distribution/model-council-digest.md`

Planned implementation artifacts:

- `distribution.yaml`
- `SOUL.md` for the distribution profile, or a repo-local equivalent if the distribution repository is separate
- `.env.EXAMPLE`
- `digital-state.manifest.json`
- `specs/003-portable-digital-state-distribution/schemas/digital-state-manifest-v1.json`
- `specs/003-portable-digital-state-distribution/schemas/profile-distribution-contract-v1.json`
- `scripts/governance/bootstrap_digital_state.py`
- `docs/governance/start-here.md`
- `docs/governance/user-quickstart.md`
- `docs/governance/institution-installation.md`
- `docs/governance/update-and-recovery.md`
- `docs/governance/github-distribution-maintenance.md`
- optional support `export_digital_state.py` / `import_digital_state.py`
- tests under `tests/scripts/`

## Update-Safety Rules

- Prefer Hermes Profile Distributions over custom install/update mechanisms.
- Keep the Digital State repository independent from official Hermes core.
- Do not vendor official Hermes Agent source into the distribution repository.
- Do not edit runtime files for this feature.
- Do not add dependencies or lockfile changes.
- Use Python standard library first.
- Use repo-relative paths in manifests and docs.
- Treat local config/profiles/secrets as operator-local state.
- Use releases/tags/changelog for Digital State updates.
- Use `hermes profile update` as the normal update path for users.

## GitHub distribution maintenance

Completed additions:

- `docs/governance/github-distribution-maintenance.md` defines release discipline for the GitHub distribution repository.
- `docs/governance/e2e-fullstack-release.md` defines the full local-to-GitHub pipeline: workspace validation, staging distribution, temporary profile install, local chat smoke test, GitHub publish, GitHub install, update, rollback, and CI gates.
- `digital-state.manifest.json` requires the E2E runbook so it ships with the profile distribution.

These artifacts keep the workspace as a development factory and the GitHub repo as a small Hermes Profile Distribution, not a fork of Hermes Agent.

## Risks

- Accidentally packaging secrets.
- Creating a custom import script that competes with official Hermes profile distribution support.
- Hardcoding the current workstation path.
- Making users believe the distribution replaces official Hermes installation.
- Building a dashboard before core distribution workflows are stable.
- Drifting from Hermes upstream because of unnecessary core edits.
- Updating Digital State in a way that assumes a newer Hermes feature without documenting compatibility.

## Open Questions

- Should the distribution repository live inside this workspace first, or be extracted to a separate GitHub repository after manifest/bootstrap stabilize?
- What exact `distribution.yaml` fields are required by the current Hermes Profile Distribution docs and CLI?
- Should we create one distribution profile or multiple distributions such as personal/team/enterprise/government?
- Should optional offline export/import support `.tar.gz`, `.zip`, or both?
- Should the manifest include a minimum Hermes version after a version check mechanism is confirmed?

## Update-Safe Architecture Contract

Feature 003 now carries an explicit update-safety contract:

- Digital State is a Hermes Profile Distribution, not a Hermes core fork.
- Hermes Agent updates and Digital State updates are separate flows.
- The canonical Digital State update command is `hermes profile update digital-state`.
- Post-update validation requires bootstrap, portability, and Hermes config checks.
- Rollback uses versioned GitHub tags instead of patching Hermes core.
- Feature 003 does not permit runtime/core modifications.

Artifacts:

- `docs/governance/update-and-recovery.md`
- `docs/governance/github-distribution-maintenance.md`
- `specs/003-portable-digital-state-distribution/schemas/update-safety-contract-v1.json`
- `specs/003-portable-digital-state-distribution/fixtures/update-safety-contract.json`
