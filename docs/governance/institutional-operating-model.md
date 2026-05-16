# Institutional Operating Model

Purpose: define how a portable Hermes digital state can be operated by individuals, teams, institutions, governments, and high-assurance agencies without turning documentation into unapproved runtime services.

## Roles

| Role | Responsibility | Current implementation level |
| --- | --- | --- |
| Sovereign Operator | Final authority for local configuration, credentials, and irreversible actions | Human/process role |
| Strategy Ministry | Maintains roadmap, Spec Kit plans, and Model Council synthesis | Docs/skill role |
| Operations Ministry | Owns bootstrap, readiness checks, environment runbooks, and safe execution posture | Docs/skill role |
| Signals Ministry | Maintains risk taxonomy, premortems, dependency/secret/path checks | Docs/validator role |
| Audit Office | Maintains model review records, decision records, hashes, and validation logs | Docs/schema role |
| Security Reviewer | Reviews credentials, network, dependency, and runtime-guard changes | Human/process role |
| Mission Authority | Approves mission-impacting or public-sector critical operations | Human/process role |

## Deployment classes

Class A: Individual portable state
- Local Hermes install.
- Manual config restoration.
- Read-only governance checks.
- No organizational approval workflow required.

Class B: Team or enterprise workspace
- Shared repo governance artifacts.
- Operator-local credentials per user/profile.
- Approval matrix adopted by team policy.
- Model Council records required for major architecture changes.

Class C: Government or regulated environment
- Offline-readable docs and deterministic bootstrap checks.
- Restricted network/tooling policy.
- Explicit change-control records.
- No claims of authorization without local authority approval.

Class D: Space-grade or mission-critical evaluation
- All Class C controls.
- Fail-closed defaults.
- Human authority over irreversible or mission-impacting actions.
- Formal safety/security case required outside this repo.

## Operating ceremonies

1. Bootstrap review: run config, portability, model-council, and governance-status checks before using a moved installation.
2. Model Council review: run a compact digest through configured models for major plans; record returned/timeouts honestly.
3. Approval review: classify proposed action using approval-matrix.md before execution.
4. Audit review: record decisions, validations, and blocked actions using audit-provenance.md vocabulary.
5. Incident review: when a no-go condition appears, stop escalation and document the blocked condition.

## Break-glass and emergency override

This feature does not implement a runtime break-glass mechanism. For institutional, government, or space-grade deployments, the operating organization must define any emergency override process before production use.

Minimum evidence to define:

- who can declare an emergency override
- what actions and systems the override covers
- how the override is time-limited
- how the action is recorded for audit
- who reviews the action after the emergency
- how credentials are rotated or revoked after suspected compromise
- how normal approval gates are restored

Until a separate tested runtime-governance-guards feature exists, Hermes can document break-glass expectations but must not be represented as technically enforcing them.

## Supply-chain and validator integrity

Before relying on governance validators in institutional settings, operators should confirm:

- scripts are from the expected repository revision
- scripts are reviewed before execution in regulated environments
- outputs are recorded with command, timestamp, and git revision
- standard-library validators are preferred for bootstrap checks
- any future third-party validator or dependency requires explicit approval

## Boundaries

This operating model creates names, responsibilities, and evidence expectations. It does not create autonomous ministries, daemons, dashboards, hidden agents, access-control systems, or runtime enforcement by itself.
