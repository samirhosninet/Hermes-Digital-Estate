# Evidence Bundle Guide for the Hermes Portable Digital State

An evidence bundle is a portable collection of governance records that lets an operator, reviewer, institution, government team, or mission-assurance group understand what Hermes Agent is configured to claim and what has actually been validated.

This guide defines what to include. It does not create tamper-proof storage or certification by itself.

## Bundle Goals

1. Make governance state reviewable offline.
2. Separate portable repo evidence from operator-local secrets/config.
3. Preserve Model Council provenance honestly.
4. Show which validators and tests passed.
5. Avoid false claims about runtime enforcement.

## Recommended Bundle Contents

### 1. Spec Kit source of truth

Include:
- `specs/001-hyperagent-governance-integration/constitution.md`
- `specs/001-hyperagent-governance-integration/spec.md`
- `specs/001-hyperagent-governance-integration/plan.md`
- `specs/001-hyperagent-governance-integration/tasks.md`
- `specs/001-hyperagent-governance-integration/analyze.md`

If runtime guard design exists, include:
- `specs/002-runtime-governance-guards/`

### 2. Governance docs

Include:
- `docs/governance/digital-state-governance.md`
- `docs/governance/portable-digital-state.md`
- `docs/governance/best-settings.md`
- `docs/governance/approval-matrix.md`
- `docs/governance/audit-provenance.md`
- `docs/governance/bootstrap-readiness.md`
- `docs/governance/compliance-mapping.md`
- `docs/governance/institutional-operating-model.md`
- `docs/governance/space-grade-readiness.md`
- `docs/governance/risk-taxonomy.md`
- `docs/governance/maturity-model.md`

### 3. Schemas and validators

Include:
- `specs/001-hyperagent-governance-integration/schemas/`
- `scripts/governance/`
- `tests/scripts/`
- `tests/fixtures/governance/`

### 4. Model Council records

Include:
- model council digest files
- model council results JSON/Markdown
- synthesis notes in plan/analyze

Requirement:
- returned, timeout, error, empty, and skipped statuses must remain visible.

### 5. Validation outputs

Include command outputs from:
- `python3 -m compileall scripts/governance tests/scripts`
- `python3 -m unittest tests.scripts.test_governance_status tests.scripts.test_governance_portability`
- `python3 scripts/governance/check_model_council_record.py <results.json>`
- `python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/001-hyperagent-governance-integration/schemas`
- `hermes config check`

Do not include secrets printed by accidental commands.

## Exclusions

Never include:
- API keys
- OAuth tokens
- `~/.hermes/auth.json`
- `.env` files containing secrets
- gateway tokens
- private user messages unless explicitly approved
- classified, export-controlled, or regulated data without local authority

## Optional Local Appendix

Operators may keep a separate local appendix outside the repo with:
- provider/model allowlist
- redacted config summary
- profile restoration notes
- machine bootstrap log
- internal approval records

This appendix should not be committed unless reviewed and sanitized.

## Future Automation

A future read-only script may generate an evidence bundle manifest with file hashes. That script should remain stdlib-only initially and must not collect secrets by default.
