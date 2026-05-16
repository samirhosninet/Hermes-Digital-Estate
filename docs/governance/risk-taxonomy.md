# Risk Taxonomy for the Hermes Portable Digital State

This taxonomy gives Hermes operators a shared vocabulary for planning, review, audit, and future enforcement work.

It is not a runtime security control and it is not a certification claim. It is a portable governance artifact that can travel with the repository.

## Risk Classes

### R0: Informational

Examples:
- reading public docs
- summarizing repo files
- generating non-sensitive plans

Expected control:
- normal agent use
- no special approval unless sensitive context is present

### R1: Advisory governance

Examples:
- updating Spec Kit plans
- writing governance docs
- running read-only validators
- requesting Model Council review

Expected control:
- repo-local changes only
- record meaningful decisions in specs/docs

### R2: Safe repository writes

Examples:
- adding tests for read-only validators
- creating schemas
- updating skills/docs

Expected control:
- keep writes in approved paths
- avoid dependencies and runtime code unless specifically approved
- run targeted tests

### R3: Runtime-impacting change

Examples:
- changing model routing
- changing terminal/file/gateway behavior
- changing config defaults
- adding runtime policy checks

Expected control:
- separate Spec Kit feature
- tests before implementation
- approval record
- rollback plan

### R4: Destructive or irreversible action

Examples:
- deleting files or repositories
- `git reset --hard`
- changing credentials
- deployment operations
- package/lockfile churn

Expected control:
- explicit operator approval
- audit/provenance record
- clear rollback or mitigation plan
- fail-closed if policy is unclear

### R5: Critical-grade / mission-impacting

Examples:
- government classified handling
- spacecraft or mission command contexts
- medical/legal/financial irreversible actions
- safety-critical automation

Expected control:
- outside repository docs alone
- qualified authority approval
- independent security/safety assessment
- formal operating constraints

## Cross-Cutting Risks

### Portability risk

A feature creates hidden dependency on local paths, local credentials, or a specific operator workstation.

Signals:
- hardcoded absolute Linux mount paths, Windows drive paths, user-home paths, or Hermes home paths as required portable paths
- docs saying external folders are required
- committed env/auth material

### False-consensus model risk

A timed-out or errored model is counted as if it reviewed a plan.

Signals:
- Model Council result lacks status per model
- synthesis cites a model that did not return
- timeout/error results are omitted

### False-enforcement risk

Docs imply Hermes blocks unsafe actions when only documentation exists.

Signals:
- wording such as "enforced" without runtime tests
- missing fail-closed tests
- missing policy parser or audit path

### Supply-chain risk

A governance feature adds dependencies, lockfile churn, or package changes before requirements are stable.

Signals:
- package/lockfile modifications in docs-only phases
- unpinned third-party tools
- validators requiring non-stdlib packages unnecessarily

### Secret and data-boundary risk

Sensitive data is copied into portable repo artifacts or model prompts.

Signals:
- API keys or tokens in fixtures/results
- local auth files referenced as portable evidence
- model digests containing secrets or regulated data

## Minimum Handling Rules

1. R0-R1 may proceed with normal documentation discipline.
2. R2 must stay inside approved artifact paths and run checks.
3. R3 requires a separate Spec Kit feature and tests.
4. R4 requires explicit approval and audit evidence.
5. R5 is not authorized by these docs alone.

## Relationship to Other Governance Docs

- `approval-matrix.md` defines approval expectations.
- `audit-provenance.md` defines evidence records.
- `maturity-model.md` defines adoption levels.
- `space-grade-readiness.md` defines conservative mission-grade language.
