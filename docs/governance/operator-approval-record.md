# Operator Approval Record

This document defines the approval record required before Feature 002 may touch any Hermes runtime file.

No runtime touchpoint is approved by this record.

## Purpose

Runtime governance is intentionally staged. Design artifacts, schemas, fixtures, validators, and the non-integrated decision core may exist without changing live Hermes behavior. Any future runtime touchpoint must have explicit operator approval recorded in a repo-relative artifact before implementation starts.

## Current status

- Approval status: not granted
- Runtime scope: none
- Enforcement allowed: false
- Maximum future mode without a new approval: log-only
- Blocking behavior allowed: false
- Terminal execution flow changes allowed: false
- Duplicate approval prompts allowed: false

## Required approval record

The canonical fixture is:

`specs/002-runtime-governance-guards/fixtures/operator-approval-record.json`

It must remain conservative until the operator explicitly approves a named runtime touchpoint.

A valid future approval must include:

1. Operator identity or role.
2. Exact runtime file or hook location.
3. Explicit scope, limited to log-only unless a later Spec Kit feature authorizes enforcement.
4. Required validation commands.
5. Rollback path.
6. Audit storage behavior.
7. Reapproval triggers.

## Mandatory constraints

A future log-only approval must not:

- Block commands.
- Mutate terminal commands.
- Bypass existing approvals.
- Add duplicate approval prompts.
- Store raw secrets.
- Depend on machine-specific paths.
- Expand beyond the named touchpoint.

## Rollback

The rollback must be simple and operator-readable. At minimum it must identify the config flag or single hook call to remove/disable.

## Reapproval triggers

Explicit operator approval is required again for:

- Any runtime file edit not named in the approval record.
- Any change from log-only toward enforcement.
- Any command-blocking behavior.
- Any terminal execution flow change.
- Any new approval prompt.
- Any audit storage location change.
- Any scope expansion beyond the approved touchpoint.

## Verification

Run:

`python3 scripts/governance/check_runtime_guard_schema.py specs/002-runtime-governance-guards/fixtures/operator-approval-record.json`

A passing validator only means the approval record is structurally valid. It does not mean runtime approval has been granted.
