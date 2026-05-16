# Constitution: Runtime Governance Guards

This feature has moved from design-only into a minimal approved core slice. The implemented slice is not wired into Hermes runtime dispatch and does not enforce terminal/file/gateway/model actions yet.

## Principles

1. Fail closed: missing, malformed, or ambiguous policy must not silently allow risky action.
2. Human authority: operators remain final authority for destructive, credential, deployment, and critical-grade actions.
3. Policy/mechanism separation: policy artifacts define intent; runtime hook mechanisms are separate and require tests plus approval.
4. Auditability: every allow, deny, escalation, and policy error must be recordable without leaking secrets.
5. Portability: policy files and schemas must be repo-relative and machine-independent; secrets and local config remain operator-local.
6. Minimal blast radius: implementation must be staged by action class and tool boundary.
7. No false enforcement claims: the current implementation is a pure decision core only; docs must not claim active runtime protection.

## No-Go Gates

The design and first slice must not:
- depend on external concept folders or local paths
- copy runtime from unrelated projects
- change package/dependency/lockfiles without separate approval
- bypass existing Hermes approval controls
- hide model timeout/error results
- claim government, safety, space, or mission certification
- hook terminal/file/gateway/model routing before a separate hook-specific Spec Kit task and tests

## Action Classes

R0-R1: read-only/advisory actions.
R2: safe repo writes or model-routing/package changes requiring approval.
R3: runtime-impacting changes, deployments, gateway fanout, cron/webhook side effects, or destructive git operations.
R4: credential/auth/secret boundary access or destructive irreversible actions.
R5: critical-grade/mission-impacting contexts or fail-closed policy errors.

Runtime guard integration, if later approved, must first cover R4/R5 denial/escalation paths before claiming broad protection.
