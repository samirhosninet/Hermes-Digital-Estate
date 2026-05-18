# End-to-End Full-Stack Release Runbook

This runbook explains how to develop, test, stage, publish, update, and recover the Digital State Profile Distribution without modifying Hermes Agent core.

## Core rule

Hermes Agent remains the official upstream runtime. Digital State ships as a Hermes Profile Distribution.

Do not publish the full `hermes-agent` workspace as the Digital State product. The workspace is the local factory. The GitHub product is a small profile distribution repo that contains only manifest-approved portable files.

## Actors and locations

1. Development workspace
   - Purpose: local development and validation.
   - Example: current Hermes workspace.
   - Contains the full Hermes Agent checkout plus Digital State source files.

2. Staging distribution directory
   - Purpose: simulate the future GitHub repo locally.
   - Example: a temporary directory created from manifest-required files.
   - Contains only Digital State shipping artifacts.

3. GitHub distribution repo
   - Purpose: the user-installable product.
   - Canonical source: `github.com/samirhosninet/Hermes-Digital-Estate`.
   - Installed with `hermes profile install` and updated with `hermes profile update`.

4. Installed user profile
   - Purpose: what the end user actually runs.
   - Created by Hermes under the user's Hermes home.
   - Contains no bundled secrets, sessions, logs, OAuth tokens, or memories.

## Release pipeline

### Stage 0: workspace development

Work only on distribution-owned or governance-owned files:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml`
- `.env.EXAMPLE`
- `START.bat`
- `START.sh`
- `wizard.py`
- `digital-state.manifest.json`
- `preflight/`
- `docs/governance/`
- `skills/devops/governance-status/`
- `scripts/bootstrap/`
- `scripts/governance/`
- `specs/003-portable-digital-state-distribution/`
- `specs/004-setup-wizard-hardening/`
- relevant distribution tests

Do not modify Hermes core runtime for Feature 003:

- terminal tools
- file tools
- gateway runtime
- model routing runtime
- approvals runtime
- cron runtime
- provider implementation
- package files or lockfiles

### Stage 1: workspace validation

Run from the workspace root:

```bash
python3 -m unittest tests.scripts.test_staging_distribution tests.scripts.test_digital_state_distribution tests.scripts.test_preflight tests.scripts.test_model_ministry_routing -v
python3 scripts/governance/bootstrap_digital_state.py --json
python3 scripts/governance/check_portability.py distribution.yaml SOUL.md config.yaml .env.EXAMPLE digital-state.manifest.json docs/governance skills/devops/governance-status scripts/bootstrap scripts/governance specs/003-portable-digital-state-distribution specs/004-setup-wizard-hardening wizard.py preflight START.bat START.sh tests/scripts tests/fixtures
hermes config check
```

Required outcome:

- tests pass
- bootstrap returns `ok: true`
- portability returns `portable: true`
- Hermes config check passes

### Stage 2: build a local staging distribution

Create a clean staging directory from the manifest-approved files only. The staging directory should look like the future GitHub repo, not like the full Hermes Agent checkout.

Build it with the repository staging builder:

```bash
python3 scripts/governance/build_staging_distribution.py --output /path/to/empty-staging-dir --json
```

Minimum staging contents:

- `distribution.yaml`
- `SOUL.md`
- `config.yaml`
- `.env.EXAMPLE`
- `START.bat`
- `START.sh`
- `wizard.py`
- `digital-state.manifest.json`
- `preflight/`
- `docs/governance/`
- `docs/governance/digital-state-runbook-ar.md`
- `skills/devops/governance-status/`
- `scripts/bootstrap/`
- `scripts/governance/`
- `specs/003-portable-digital-state-distribution/`
- `specs/004-setup-wizard-hardening/`

`tests/` and `agent/` are validation-only workspace inputs. They are not part of the GitHub distribution product unless the manifest explicitly allows them.

Run the distribution checks again from inside the staging directory:

```bash
python3 scripts/governance/bootstrap_digital_state.py --json
python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution specs/004-setup-wizard-hardening scripts/bootstrap scripts/governance wizard.py preflight START.bat START.sh
```

Do not include:

- `.env`
- `auth.json`
- sessions
- logs
- memories
- local profile exports
- machine-specific paths
- `agent/`
- `tests/`
- the full Hermes Agent source tree

### Stage 3: install staging as a temporary profile

Install the staging directory as a temporary profile:

```bash
hermes profile install /path/to/staging-digital-state --name digital-state-test -y
hermes profile show digital-state-test
hermes -p digital-state-test config check
```

Then run bootstrap inside the installed profile directory:

```bash
cd ~/.hermes/profiles/digital-state-test
python3 scripts/governance/bootstrap_digital_state.py --json
```

Required outcome:

- profile installs successfully
- `SOUL.md` and `config.yaml` are present
- bootstrap returns `ok: true`

### Stage 4: local end-to-end chat smoke test

Secrets are never committed. For testing only, add credentials locally to the temporary profile or use the normal Hermes local auth flow.

Smoke test the profile:

```bash
hermes -p digital-state-test chat -q "Reply with OK only."
```

For ministry accountability, do not use fallback substitution. Test each ministry with its assigned model and record the result:

- Strategy Ministry: `openai-codex:gpt-5.5`
- Operations Ministry: `nvidia:meta/llama-4-maverick-17b-128e-instruct`
- Signals Ministry: `nvidia:mistralai/mistral-large-3-675b-instruct-2512`
- Audit Office: `nvidia:z-ai/glm-5.1`
- Governance Office: `nvidia:deepseek-ai/deepseek-v4-flash`
- Citizen Services: `nvidia:minimaxai/minimax-m2.7`
- Research and Space Planning: `nvidia:moonshotai/kimi-k2.6`

If a ministry model fails, mark that ministry unavailable or experimental. Do not replace it silently with another model.

### Stage 5: cleanup local test credentials

After testing, delete the temporary profile or remove local credentials from it:

```bash
hermes profile delete digital-state-test
```

Never copy temporary `.env`, auth files, sessions, logs, or memories into the GitHub distribution repo.

### Stage 6: publish to GitHub

Use the canonical GitHub repo for the distribution:

```bash
git remote -v
```

The remote must point to `https://github.com/samirhosninet/Hermes-Digital-Estate.git`.

Push only the staging distribution contents, not the full Hermes Agent workspace. The staging output is the only allowed source for the GitHub distribution repo.

Tag the current tested version:

```bash
git tag v0.1.1
git push origin main --tags
```

### Stage 7: test from GitHub like a real user

Install from GitHub into a fresh profile:

```bash
hermes profile install github.com/samirhosninet/Hermes-Digital-Estate --alias
hermes profile show digital-state
hermes -p digital-state config check
```

Run bootstrap inside the installed profile:

```bash
cd ~/.hermes/profiles/digital-state
python3 scripts/governance/bootstrap_digital_state.py --json
```

Run a chat smoke test after adding local credentials:

```bash
hermes -p digital-state chat -q "Reply with OK only."
```

### Stage 8: update flow

Users update Digital State with:

```bash
hermes profile update digital-state
```

After every update:

```bash
hermes -p digital-state config check
cd ~/.hermes/profiles/digital-state
python3 scripts/governance/bootstrap_digital_state.py --json
```

Hermes Agent itself is updated separately through the official Hermes update flow. Digital State updates must not patch Hermes core.

### Stage 9: rollback

If a release breaks, reinstall or update from a known-good GitHub tag.

Example policy:

- keep versioned tags such as `v0.1.1`
- publish release notes
- document compatibility changes
- never require users to patch Hermes core manually

## GitHub CI requirement

Before release, the GitHub repo should run these checks on pull requests and tags:

```bash
python3 -m unittest tests.scripts.test_staging_distribution tests.scripts.test_digital_state_distribution tests.scripts.test_preflight tests.scripts.test_model_ministry_routing -v
python3 scripts/governance/bootstrap_digital_state.py --json
python3 scripts/governance/build_staging_distribution.py --output /path/to/empty-staging-dir --json
python3 scripts/governance/check_portability.py distribution.yaml SOUL.md config.yaml .env.EXAMPLE digital-state.manifest.json docs/governance skills/devops/governance-status scripts/bootstrap scripts/governance specs/003-portable-digital-state-distribution specs/004-setup-wizard-hardening wizard.py preflight START.bat START.sh tests/scripts tests/fixtures
```

CI must fail if:

- required files are missing
- secrets are present
- local paths are present
- the distribution claims to modify Hermes core
- model-ministry routing enables fallback
- bootstrap fails

## Non-technical user path

The final Windows user experience should be:

1. Open PowerShell on a fresh Windows machine.
2. Run:

```powershell
irm https://raw.githubusercontent.com/samirhosninet/Hermes-Digital-Estate/main/scripts/bootstrap/install-windows.ps1 | iex
```

3. Use the local **Install Digital State Stack** UI.

The Windows bootstrapper downloads this distribution, launches `START.bat`, installs Hermes Agent first, and then uses `%LOCALAPPDATA%\hermes\bin\hermes.cmd` directly because the current shell may not have refreshed PATH after the official Hermes installer.

The advanced terminal experience should be:

1. Install official Hermes Agent.
2. Run one install command:

```bash
hermes profile install github.com/samirhosninet/Hermes-Digital-Estate --alias
```

3. Start the profile:

```bash
hermes -p digital-state chat
```

4. Follow the profile's first-run guidance to add local keys and run readiness checks.

The user should not need to understand the development workspace, staging directory, or GitHub release pipeline.
