# Update and Recovery for Digital State

This document explains how to update the Digital State without breaking official Hermes Agent.

## Core rule

Digital State is a Hermes Profile Distribution. It is not a fork of Hermes Agent and must not require edits to Hermes core.

Users update two things separately:

1. Official Hermes Agent, using official Hermes update flows.
2. Digital State, using Hermes profile distribution update flows.

## Normal update

```bash
hermes profile update digital-state
```

Then run:

```bash
python3 scripts/governance/bootstrap_digital_state.py --json
hermes config check
```

If both checks pass, the update is ready.

## If an update fails

Do not edit Hermes core to work around a failed Digital State update. Instead:

1. Stop and record the error.
2. Run the bootstrap check.
3. Review the release notes for the Digital State version.
4. Reinstall or roll back the Digital State profile from a known-good GitHub tag.

Example rollback pattern:

```bash
hermes profile install github.com/samirhosninet/Hermes-Digital-Estate@v0.1.1 --alias digital-state
```

## What stays local

Never publish or restore these through the Digital State GitHub repository:

- real `.env` files
- API keys
- OAuth tokens
- auth stores
- sessions
- logs
- memories
- machine-specific paths

## Update readiness checklist

Before marking a release stable:

- `digital-state.manifest.json` validates.
- `distribution.yaml` validates.
- Bootstrap returns `ok: true`.
- Portability checks pass.
- Unit tests pass.
- No Hermes core files are required for the Digital State update.
- Recovery instructions reference a versioned GitHub tag.
