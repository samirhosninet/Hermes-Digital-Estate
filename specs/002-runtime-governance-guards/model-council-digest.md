# Model Council Digest: Runtime Governance Guards

Task: Review feature 002 for Hermes Agent runtime-governance-guards.

Scope:
- Design-only feature.
- No runtime implementation yet.
- No dependency or lockfile changes.
- No external concept-folder dependency.
- Goal is to design future guards for terminal/file/package/git/network/credentials/model-routing/gateway/cron side effects.

Current proposed architecture:
1. Policy artifacts.
2. Action classifier.
3. Decision engine returning allow, deny, escalate, or fail_closed.
4. Audit writer that avoids secrets.

Key requirements:
- fail closed on missing/malformed policy in strict mode.
- tests before implementation.
- integrate with existing Hermes approvals rather than bypassing them.
- preserve portability across machines.
- record decisions without leaking secrets.

Please return:
- top risks in this design
- missing acceptance criteria
- recommended first implementation slice if later approved
- no-go warnings
- whether this feature should remain design-only now
