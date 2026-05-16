# Hermes Digital State Bootstrap Readiness

This checklist helps move the Hermes digital state to a new machine and verify it without depending on any external concept folder. It is designed for users, institutions, governments, and space-grade operators who need repeatable setup and degraded-mode awareness.

## Portability contract

Portable repo artifacts
- specs/
- docs/governance/
- skills/
- scripts/governance/
- tests/fixtures/governance/
- tests/scripts/

Operator-local state
- ~/.hermes/config.yaml
- ~/.hermes/.env
- ~/.hermes/auth.json or provider auth stores
- Hermes profiles
- gateway tokens
- OAuth sessions
- local logs and sessions
- machine-specific paths

Rule: portable artifacts must not require operator-local paths or secrets to exist in the repository.

## New machine bootstrap

1. Install Hermes Agent using the normal Hermes installer or project-specific setup.
2. Clone or copy the Hermes Agent repository.
3. Restore operator-local state through Hermes-native mechanisms:
   - hermes profile import when a profile archive is intentionally exported,
   - hermes setup for interactive configuration,
   - hermes login for OAuth providers,
   - ~/.hermes/.env or secret manager for API keys.
4. Run config and health checks:
   - hermes config check
   - hermes doctor
5. Verify governance artifacts:
   - python3 scripts/governance/read_governance_status.py tests/fixtures/governance/valid-status.json
   - python3 scripts/governance/check_model_council_record.py specs/001-hyperagent-governance-integration/model-council-results.json
   - python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/001-hyperagent-governance-integration/schemas
6. Run tests:
   - python3 -m unittest tests.scripts.test_governance_status tests.scripts.test_governance_portability
   - or pytest equivalent if pytest is installed.
7. Smoke-test models with tiny prompts before using them for planning or execution.
8. Restart gateway/API sessions after config, skill, or system-prompt changes.

## Model readiness classes

Ready
- Model returns a tiny chat completion within the configured timeout.
- It can be used for chat or model council work depending on quality.

Slow
- Model returns but approaches timeout.
- Use for analysis only; avoid default chat.

Unstable
- Model sometimes returns and sometimes times out or emits non-standard content.
- Record attempts; do not rely on it for quorum.

Unavailable
- Model is catalog-listed but completion calls fail or time out.
- Keep as optional, not required for bootstrap success.

## Degraded/offline mode

The digital state remains partially useful without model/API access if:
- docs are available offline,
- specs and schemas are present,
- validators run with standard library only,
- tests for governance scripts pass,
- operator can inspect policies and approval matrix manually.

Unavailable features in degraded mode:
- remote model council calls,
- provider smoke tests,
- gateway platform operations that require network,
- OAuth login refresh,
- external deployments.

## Readiness levels

Level A: Documentation portable
- Specs, docs, skills, and schemas are present.
- No secrets or required machine paths are committed.

Level B: Validation portable
- Governance scripts run successfully with standard library.
- Fixtures/tests pass.

Level C: Operator configured
- Hermes config check passes.
- Required provider credentials are restored locally.
- Gateway/API sessions can restart cleanly if needed.

Level D: Model council ready
- At least the primary model and one fallback model pass smoke tests.
- Timed-out models are recorded honestly and not required for quorum.

Level E: Runtime governed
- Future state only.
- Requires separate Spec Kit feature implementing and testing runtime enforcement.

## Critical deployment caution

For institution, government, or space-grade use, do not treat successful bootstrap as certification. Add external governance:
- change control,
- independent review,
- supply-chain review,
- secure key management,
- incident response,
- disaster recovery test,
- legal/compliance assessment,
- human accountability.

## Bootstrap failure handling

Config check fails
- Inspect config with hermes config path and hermes config check.
- Do not commit local config secrets to the repo.

Model smoke tests fail
- Verify provider credential presence.
- Check whether other models on the same provider work.
- Mark failing model unavailable or unstable for the current run.

Portability check fails
- Remove required absolute paths or secrets from portable artifacts.
- Replace machine paths with placeholders.
- Re-run check_portability.py.

Tests fail
- Fix governance scripts or fixtures first.
- Do not proceed to runtime enforcement until tests pass.
