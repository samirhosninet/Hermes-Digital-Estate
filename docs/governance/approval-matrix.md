# Hermes Digital State Approval Matrix

This runbook defines approval expectations for a portable Hermes digital state. It is policy guidance only in feature 001; it does not implement runtime enforcement.

## Approval levels

Level 0: Read-only
- Examples: read files, inspect git status, run validators that only read inputs, review docs, query model catalogs, smoke-test models with harmless prompts.
- Default: allowed during planning and audit work.
- Record: optional for routine inspection, required when used for Model Council or compliance evidence.

Level 1: Safe repo writes
- Examples: create or edit specs, docs, skills, schemas, fixtures, and read-only scripts inside the approved feature scope.
- Default: allowed after Spec Kit task exists.
- Record: artifact path, reason, linked task ID, verification command.

Level 2: Behavioral code changes
- Examples: changing Hermes runtime behavior, model routing, tool dispatch, gateway processing, approvals, file/terminal tools, memory, cron, kanban, or provider code.
- Default: blocked in feature 001.
- Requirement: separate Spec Kit feature, tests first, explicit operator approval.

Level 3: Destructive/local irreversible operations
- Examples: rm -rf, git reset --hard, database deletion, credential deletion, key rotation, profile deletion, force push, uninstall, service removal.
- Default: manual approval required every time.
- Requirement: explain target, backup/rollback status, blast radius, and verification plan.

Level 4: Network, deployment, and external side effects
- Examples: deploy, publish packages, push to remote, call production APIs, send messages, create cloud resources, subscribe webhooks, run gateway against live platforms.
- Default: manual approval required.
- Requirement: environment name, credentials used, expected external effect, rollback/disable plan.

Level 5: Credential and secret handling
- Examples: reading, moving, exporting, rotating, or transmitting API keys, OAuth tokens, auth stores, .env files, gateway tokens.
- Default: do not expose secrets to model context; use Hermes-native auth/profile/env flows.
- Requirement: operator confirmation, redaction enabled where possible, no committed secrets.

Level 6: Institution/government/space-grade critical actions
- Examples: policies that affect safety, legal compliance, public service operation, operational command systems, or mission-critical workflows.
- Default: advisory only unless formally governed outside Hermes.
- Requirement: human accountable owner, external review, audit retention policy, incident process, and explicit non-certification notice.

## Action categories

Read-only inspection
- Approval: Level 0.
- Allowed paths: repo-relative artifacts, configured logs, non-secret config summaries.
- Not allowed: secret dumps, private keys, token stores.

Documentation/specification updates
- Approval: Level 1 when scoped by Spec Kit.
- Required evidence: changed file list and validation results.

Validator/script creation
- Approval: Level 1 if read-only and standard-library only.
- Escalate to Level 2 if the script changes files, starts services, or calls external APIs.

Package and dependency changes
- Approval: Level 2 minimum.
- Feature 001 status: blocked.
- Required evidence: dependency rationale, lockfile diff, security review, rollback.

Runtime enforcement
- Approval: Level 2 minimum.
- Feature 001 status: blocked.
- Required evidence: tests, fail-closed behavior, migration notes, opt-in/opt-out semantics.

Git operations
- git status/diff/log: Level 0.
- commit local changes: Level 1 or 2 depending on touched files.
- push/force-push/reset/clean: Level 3 or 4 depending on effect.

Model Council calls
- Smoke tests: Level 0 if prompts contain no secrets.
- Code/spec review: Level 0 or 1 depending on content sensitivity.
- Production/private data review: Level 5 and institution policy required.
- Record every model as returned, timeout/error, empty, or skipped.

## No-go gates for feature 001

Stop and create a new Spec Kit feature if a task requires:
- runtime guard implementation,
- terminal/file/gateway/model-routing changes,
- dependency or lockfile edits,
- external service deployment,
- committed secrets,
- coupling to a local machine path,
- claiming certification or active enforcement that does not exist.

## Minimum audit fields

For any Level 1+ action, record:
- timestamp UTC,
- actor or model,
- task/spec reference,
- action category and approval level,
- files or systems affected,
- outcome,
- verification command/result,
- rollback or follow-up note when relevant.
