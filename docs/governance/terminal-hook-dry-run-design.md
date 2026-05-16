# Terminal Hook Dry-Run Design

No current terminal runtime hook is active.

This document defines the future dry-run/log-only terminal hook contract for Feature 002. It is a design and evidence artifact only. It does not modify terminal execution, approvals, process management, shell invocation, or command output handling.

## Purpose

The future hook should let Hermes classify a proposed terminal command, build a governance decision, and write a redacted audit record before command execution. In the first integration slice it must be dry-run/log-only and must not block, mutate, or reorder terminal execution.

## Required Future Flow

1. Receive the proposed terminal command text.
2. Build a dry-run action with `build_terminal_dry_run_action(command)`.
3. Evaluate the action with the runtime governance core.
4. Build a redacted audit record.
5. Continue the existing terminal execution flow unchanged.
6. Never replace the existing approval mechanism.

## Non-Negotiable Guardrails

- The first hook must be dry-run/log-only.
- It must not block, mutate, or reorder terminal execution.
- It must not bypass existing approvals.
- It must not capture raw secrets in audit records.
- It must fail safely if policy/audit writing is unavailable.
- It must have an explicit disable/rollback path.

## Evidence Required Before Integration

The following evidence must exist before any runtime file is touched:

- unit tests for allow/escalate/deny/fail_closed decisions
- dry-run audit sample
- operator approval matrix
- portability check
- secret redaction test

## Current Status

The current repository has a non-integrated classifier and decision core. The terminal hook itself is not connected. Any future edit to terminal dispatch must be a separate approved implementation step.
