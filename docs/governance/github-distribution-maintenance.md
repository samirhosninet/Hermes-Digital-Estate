# GitHub Distribution Maintenance

Digital State should be maintained as a GitHub-hosted Hermes Profile Distribution.

## Repository model

Recommended repository:

```text
github.com/YOUR-ORG/hermes-digital-state
```

The repository contains profile distribution artifacts only. It does not replace official Hermes Agent.

## Required release assets

A release must include:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml` with non-secret defaults
- `.env.EXAMPLE`
- `digital-state.manifest.json`
- `docs/governance/`
- `skills/`
- `scripts/governance/`
- `specs/003-portable-digital-state-distribution/`

## Release process

1. Update the version in `digital-state.manifest.json`.
2. Update changelog or release notes.
3. Run validation locally.
4. Open a pull request.
5. Run CI checks.
6. Tag the release.
7. Ask users to update through Hermes profile commands.

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

## Compatibility policy

Digital State versions should state the expected Hermes compatibility range in the manifest. If Hermes changes profile behavior, ship a new Digital State version with migration notes instead of patching user installations manually.

## CI expectations

Every pull request should run:

```bash
python3 -m unittest tests.scripts.test_digital_state_distribution -v
python3 scripts/governance/bootstrap_digital_state.py --json
python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution scripts/governance
hermes config check
```
