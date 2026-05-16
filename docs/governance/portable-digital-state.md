# Portable Hermes Digital State

Goal: move Hermes Agent's digital-state artifacts to another machine without depending on this workstation.

## Portable with the repo

- `specs/`
- governance skills under `skills/`
- `docs/governance/`
- read-only validators under `scripts/governance/`
- tests and fixtures for governance validators
- model council records without secrets

## Not committed / restored locally

- API keys and provider tokens
- OAuth/auth stores
- gateway/platform tokens
- machine-specific config
- local logs that may contain sensitive data
- unsanitized profile archives

## Bootstrap checklist on a new machine

1. Install Hermes Agent for the target OS.
2. Clone or copy the Hermes Agent repo.
3. Restore Hermes profile/config through Hermes-native commands when available:
   - `hermes profile export <name>` on source machine after sanitization.
   - `hermes profile import <archive>` on target machine.
4. Restore secrets through `~/.hermes/.env`, auth/login flows, or provider-specific setup. Do not commit them.
5. Run `hermes config check`.
6. Run governance validators, for example:
   - `python3 scripts/governance/read_governance_status.py tests/fixtures/governance/valid-status.json`
   - `python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/001-hyperagent-governance-integration/schemas`
   - `python3 scripts/governance/check_model_council_record.py specs/001-hyperagent-governance-integration/model-council-results.json`
7. Run model smoke tests and record timeouts honestly.

## Portability rules

Use repository-relative paths in committed governance artifacts. Keep absolute local paths, drive letters, usernames, and secrets out of portable artifacts. If a deployment needs a local path, document it as operator-local setup, not as a repo requirement.
