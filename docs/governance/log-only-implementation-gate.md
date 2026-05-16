# Log-Only Implementation Gate

This is not runtime enforcement. It is a design gate that must be satisfied before Hermes Agent is allowed to add any future terminal runtime touchpoint for governance logging.

The current allowed mode is log-only. A future hook, if explicitly approved later, must not block terminal execution, must not mutate commands, must not add a second approval prompt, and must not change terminal execution order.

## Required evidence before runtime touchpoint

A future implementation slice may touch terminal runtime only after all of these are true:

- explicit operator approval is recorded for the specific runtime touchpoint
- terminal-hook dry-run contract passes validation
- approval-flow interaction contract passes validation
- unit tests pass
- portability check passes for governance artifacts
- rollback plan is documented and executable

## Runtime touchpoint constraints

If approved later, the first runtime touchpoint must be:

- one small hook only
- log-only, not enforcement
- no command mutation
- no additional approval prompt
- audit write failure is non-blocking
- feature flag disable path exists before activation

## Failure posture

The default failure behavior is continue_without_governance_block. In log-only mode, governance logging failure must not become a hidden denial path. If a later enforcement feature is desired, it must be a separate Spec Kit feature with its own Model Council review and explicit approval.

## Current status

No runtime touchpoint is authorized by this document. This document only defines the gate for a later operator-approved log-only implementation.
