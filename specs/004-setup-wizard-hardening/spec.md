# Spec: Setup Wizard Hardening

## Summary

Harden the Hermes Digital State Setup Wizard as an onboarding helper without changing the canonical Hermes Profile Distribution install and update path.

## Requirements

- The wizard remains stdlib-only and must not add package dependencies, lockfiles, `keyring`, or `PyInstaller`.
- `wizard.py --port <PORT>` treats the port as the first preferred localhost port and may bind to the next available port in a bounded range.
- The local HTTP server binds only to `127.0.0.1`, handles concurrent requests, and rejects non-local Host headers.
- Credential saving writes only operator-local `.env` state, never returns credential values in JSON, and uses locked atomic writes.
- Windows one-click startup performs visible prerequisite diagnostics, then runs the server in the background with a log and opens the browser only after a health check succeeds.
- macOS/Linux startup follows the same readiness model as Windows: visible prerequisite diagnostics, background server, health check, browser open after readiness, and log output on failure.
- Audit and portability checks should scan wizard implementation files when practical; any remaining skips must be for scanner source or intentional fixtures.

## Non-Goals

- Replacing Hermes Profile Distribution as the primary install/update mechanism.
- Adding runtime governance enforcement.
- Adding new dependencies, executable bundling, or OS credential-store integration.

## Acceptance Checks

- `python -m unittest tests.scripts.test_preflight`
- `python audit.py`
- `python scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution scripts/governance tests/scripts tests/fixtures`
