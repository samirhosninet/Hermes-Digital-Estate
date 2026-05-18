# GitHub Distribution Maintenance

Digital State should be maintained as a GitHub-hosted Hermes Profile Distribution.

## Repository model

Recommended repository:

```text
github.com/samirhosninet/Hermes-Digital-Estate
```

The repository contains profile distribution artifacts only. It does not replace official Hermes Agent.

The GitHub repository must be populated from a staging output built with `scripts/governance/build_staging_distribution.py`. Do not push the development workspace directly.

## Required release assets

A release must include:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml` with non-secret defaults
- `.env.EXAMPLE`
- `START.bat`
- `START.sh`
- `wizard.py`
- `digital-state.manifest.json`
- `docs/governance/`
- `docs/governance/digital-state-runbook-ar.md`
- `preflight/`
- `skills/`
- `scripts/bootstrap/`
- `scripts/governance/`
- `specs/003-portable-digital-state-distribution/`
- `specs/004-setup-wizard-hardening/`

The public Windows bootstrap command depends on `scripts/bootstrap/install-windows.ps1` being present on the `main` branch:

```powershell
irm https://raw.githubusercontent.com/samirhosninet/Hermes-Digital-Estate/main/scripts/bootstrap/install-windows.ps1 | iex
```

That script must download the distribution package, launch `START.bat`, and let the local installer install Hermes Agent before checking Git, Node.js, or Workspace dependencies.

## Release process

1. Update the version in `digital-state.manifest.json`.
2. Update `docs/governance/release-notes.md`.
3. Run validation locally.
4. Build staging with `scripts/governance/build_staging_distribution.py`.
5. Run bootstrap and portability inside the staging output.
6. Publish only the staging output to the GitHub distribution repo.
7. Open a pull request.
8. Run CI checks.
9. Tag the release.
10. Ask users to update through Hermes profile commands.

User update command:

```bash
hermes profile update digital-state
```

## Maintainer no-go gates

Do not ship:

- real `.env`
- OAuth/auth tokens
- logs or sessions
- machine-specific paths
- Hermes core runtime modifications as part of this distribution
- a standalone UI as the primary onboarding path
- `agent/` or `tests/` as product artifacts unless explicitly allowed by the manifest

## Compatibility policy

Digital State versions should state the expected Hermes compatibility range in the manifest. If Hermes changes profile behavior, ship a new Digital State version with migration notes instead of patching user installations manually.

## CI expectations

Every pull request should run:

```bash
python3 -m unittest tests.scripts.test_staging_distribution tests.scripts.test_digital_state_distribution tests.scripts.test_preflight -v
python3 scripts/governance/bootstrap_digital_state.py --json
python3 scripts/governance/build_staging_distribution.py --output /path/to/empty-staging-dir --json
python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution specs/004-setup-wizard-hardening scripts/bootstrap scripts/governance wizard.py preflight START.bat START.sh
hermes config check
```
