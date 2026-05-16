# Approval Flow Interaction

No runtime integration is active.

This document defines the future interaction contract between runtime governance dry-run logging and the existing Hermes approval flow. It is a design artifact only. It does not install a terminal hook, does not change approvals, and does not alter command execution.

## Purpose

A future terminal dry-run hook may classify a proposed command and produce a governance decision for audit/provenance. In its first approved implementation it must remain dry-run/log-only. It must not create a second approval prompt, must not bypass the existing approval flow, and must not change terminal execution order or outcome.

## Required Interaction Sequence

1. Proposed terminal action is received by the existing terminal path.
2. A governance dry-run action is built from the command text.
3. The governance core produces a dry-run decision.
4. The existing approval flow remains authoritative.
5. The terminal execution flow continues unchanged.
6. A redacted audit record is written or buffered.

## Non-Negotiable Rules

- The first integration must be dry-run/log-only.
- It must not create a second approval prompt.
- It must not bypass the existing approval flow.
- It must not block, mutate, or reorder terminal execution.
- It must not store raw secrets in logs or audit records.
- If audit writing fails, terminal flow must continue and the audit failure must be recorded locally when possible.
- If approval handling fails, behavior must defer to the existing approval flow rather than governance code.

## Disable / Rollback

The design contract reserves this future disable flag:

`governance.terminal_dry_run_enabled=false`

A future implementation must be removable by deleting the hook call or disabling the flag. Until implementation is explicitly approved, this flag is only a documented contract value and not active configuration.

## Evidence Required Before Runtime Integration

Before touching terminal runtime files, the repository must contain:

- terminal hook dry-run contract
- approval interaction contract
- unit tests for interaction guarantees
- redacted audit samples
- portability check
- secret redaction tests
- operator approval matrix reference

## Current Status

The current repository has a non-integrated governance core and dry-run classifier. No runtime integration is active.
