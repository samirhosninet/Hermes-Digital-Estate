# Model Council Digest: Portable Digital-State Distribution

## Review Target

Feature 003: `portable-digital-state-distribution`

Goal: make the Hermes digital-state layer easy to install, update, bootstrap, recover, and operate while keeping official Hermes Agent as the base and avoiding conflicts with upstream updates.

## Updated Distribution Decision

The primary distribution path should use Hermes Profile Distributions from a GitHub project/repository, not a custom installer as the canonical path.

Expected user path:

1. Install official Hermes Agent from NousResearch.
2. Install Digital State as a Hermes Profile Distribution from GitHub or a local distribution path.
3. Add local credentials from `.env.EXAMPLE`.
4. Run bootstrap checks.
5. Use `hermes -p <profile> chat` or the distribution alias.
6. Update Digital State with Hermes profile update flow.
7. Update official Hermes separately with official Hermes update flow.

## Hard Constraints

- Official Hermes Agent remains the base installation.
- Digital State is a profile distribution, not a fork.
- No dependency on external prototype folders.
- No hardcoded local paths.
- No secrets, auth stores, sessions, logs, gateway tokens, memories, or unsanitized profiles in the distribution.
- No standalone UI/dashboard in this feature.
- No runtime enforcement or hooks in this feature.
- No terminal/file/gateway/model-routing core changes.
- No package dependency or lockfile changes.
- Prefer Python standard library for scripts.
- Keep all artifacts repo-relative and update-safe.

## Planned Artifacts

- `distribution.yaml`
- `SOUL.md`
- `.env.EXAMPLE`
- `README.md`
- `CHANGELOG.md`
- `digital-state.manifest.json`
- `specs/003-portable-digital-state-distribution/schemas/profile-distribution-contract-v1.json`
- `specs/003-portable-digital-state-distribution/schemas/digital-state-manifest-v1.json`
- `scripts/governance/bootstrap_digital_state.py`
- `docs/governance/user-quickstart.md`
- `docs/governance/institution-installation.md`
- `docs/governance/update-and-recovery.md`
- `docs/governance/github-distribution-maintenance.md`
- tests under `tests/scripts/`
- optional support-only export/import scripts for offline/evidence use

## Requested Review Questions

1. Does using Hermes Profile Distribution keep Hermes upstream-update-safe better than custom import/export?
2. What must be present in `distribution.yaml`, manifest, and `.env.EXAMPLE` for user simplicity?
3. What is the biggest portability or security risk?
4. Should optional import/export exist at all, or only after profile distribution is stable?
5. How should GitHub releases/tags/changelog be structured for institutions?
6. What evidence should institutions/governments/critical-grade operators require before use?
7. What should be explicitly out of scope to avoid overbuilding?

## Desired Output Format

Return concise recommendations under:

- Upstream safety
- Profile distribution design
- Manifest/bootstrap risks
- GitHub update/release workflow
- User onboarding
- Institution/critical-grade evidence
- No-go warnings
