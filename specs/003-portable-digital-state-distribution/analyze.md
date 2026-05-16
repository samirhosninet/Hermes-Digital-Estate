# Analysis: Portable Digital-State Distribution

## Summary

Feature 003 defines Digital State as a portable Hermes Profile Distribution, not a Hermes Agent fork.

The development workspace is a factory for building and validating distribution artifacts. The user-facing product is a small GitHub repository containing only manifest-approved Digital State files.

## Architecture decision

- Official Hermes Agent remains the upstream runtime.
- Digital State is installed with `hermes profile install` and updated with `hermes profile update`.
- Secrets, sessions, logs, OAuth tokens, memories, and local profile state never ship in the distribution.
- Runtime hooks, terminal/file/gateway/model-routing changes, dependencies, lockfiles, and standalone UI are out of scope for Feature 003.

## Risks and mitigations

### Risk: Publishing the full Hermes Agent workspace

Mitigation: use a staging distribution directory built from `digital-state.manifest.json` required/allowed files only. Publish that staging content to the GitHub distribution repo, not the full workspace.

### Risk: Secrets in GitHub

Mitigation: `.env` and auth/session/log/memory files are forbidden. Only `.env.EXAMPLE` ships. Bootstrap and portability checks scan shipping files.

### Risk: Breaking Hermes updates

Mitigation: Digital State is a profile distribution. Hermes core updates and Digital State updates are separate. Feature 003 forbids Hermes core runtime changes.

### Risk: Model fallback hiding ministry failures

Mitigation: ministry routing is fixed and `fallback_enabled` is false. Every ministry is tested with its assigned model. Failures are recorded as ministry failures, not substituted silently.

### Risk: Non-technical users cannot operate it

Mitigation: `start-here.md`, `user-quickstart.md`, and the E2E release runbook define the official-Hermes-first installation path and simple usage commands.

## Current status

Phase 1 is implemented and validated. The workspace now has initial Hermes Profile Distribution files:

- `distribution.yaml`
- `SOUL.md`
- `.env.EXAMPLE`
- profile `config.yaml`
- `digital-state.manifest.json`
- distribution/manifest schemas
- `scripts/governance/bootstrap_digital_state.py`
- `tests/scripts/test_digital_state_distribution.py`

Phase 5 user onboarding has started. `docs/governance/start-here.md` and `docs/governance/user-quickstart.md` provide a non-technical official-Hermes-first install/use/update path and are required by the manifest.

## Update-safety analysis

The update-safety design is explicit and test-backed.

Decision:

- Official Hermes Agent remains the upstream-owned core.
- Digital State remains a GitHub-hosted Hermes Profile Distribution.
- Users update Digital State through `hermes profile update digital-state`.
- Users update Hermes Agent separately through official Hermes update flows.
- Feature 003 cannot ship Hermes core runtime changes.

Validation:

- `digital-state.manifest.json` requires update/recovery and GitHub maintenance docs.
- `update-safety-contract.json` forbids Digital State from modifying Hermes core in Feature 003.
- Tests assert the update command, no-core-modification policy, and required docs.

## End-to-end full-stack release analysis

Added `docs/governance/e2e-fullstack-release.md` as the operational bridge between local development and GitHub release.

The runbook defines:

1. Workspace development.
2. Workspace validation.
3. Staging distribution build.
4. Local staging profile install as `digital-state-test`.
5. Local chat smoke test with credentials added locally only.
6. Temporary profile cleanup.
7. GitHub distribution publish.
8. GitHub install test.
9. Update and rollback flow.
10. GitHub CI requirements.

Verification added:

- `digital-state.manifest.json` requires the E2E runbook.
- `tests/scripts/test_digital_state_distribution.py` checks that the E2E runbook is required and contains the staging/GitHub install path.

Remaining future hardening:

- Add GitHub Actions workflow once the distribution repository is created.
- Add changelog and release-tag policy when the external GitHub repository exists.
- Add an automated staging builder script if manual staging becomes error-prone.
