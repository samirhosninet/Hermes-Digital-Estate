# Phase 5 Model Council Digest

Review these new Hermes Agent portable digital-state governance docs.
Goal: Hermes Agent as independent portable digital-state for users, institutions, governments, and space-grade organizations.
Constraints: no external folder dependency, no runtime enforcement claim, no certification claim, docs/read-only only in feature 001.
Return concise review: (1) strongest point, (2) missing risk/control, (3) wording that must be conservative, (4) go/no-go for docs-only phase.

FILE: docs/governance/compliance-mapping.md
# Compliance Mapping for the Hermes Portable Digital State
It is not a certification claim. It is a planning and evidence map that helps operators decide what is already documented, what can be validated read-only, and what still requires future runtime enforcement, organizational controls, or third-party assessment.
## Scope
- `specs/001-hyperagent-governance-integration/`
- `docs/governance/`
- `skills/devops/governance-status/`
- `scripts/governance/`
- `tests/scripts/`
- `tests/fixtures/governance/`
- API keys and OAuth tokens
- `~/.hermes/config.yaml`
- `~/.hermes/.env`
- Hermes profiles and auth stores
- gateway tokens and platform credentials
- machine-specific paths and service units
## Control Families
### Governance and policy
- Spec Kit constitution, spec, plan, tasks, and analysis
- approval matrix
- bootstrap readiness checklist
- governance-status skill
- clear authority for changes
- phase separation between planning, read-only validation, and enforcement
- explicit no-go gates
- operator sign-off for irreversible actions
- policies are documented and validated as artifacts; they are not runtime-enforced yet.
- approved runtime-governance-guards Spec Kit feature
- tests proving fail-closed behavior
- signed release or change approval records
### Auditability and provenance
- audit/provenance runbook
- model-council result records
- audit-record schema
- validator outputs
- who/what proposed a change
- which model reviews returned or failed
- what validators ran
- what approvals were required
- which artifacts changed
- records are file-based and operator-managed; immutable storage is not implemented.
- append-only audit backend
- checksums/signatures for critical records
- retention policy and export format
### Security and least privilege
- approval matrix
- portability guide
- best settings guide
- portability validator scanning for forbidden paths and secret-like content
- no committed credentials
- separation of repo artifacts from local secrets
- manual approval default for high-risk operations
- explicit stop conditions for destructive actions
- runtime command blocking is not active in this feature.
- tool-dispatch guards for terminal/file/package/git/network/model actions
- tests for blocked commands and denied writes
- policy parser with fail-closed behavior
### Portability and reproducibility
- portable digital-state guide
- bootstrap readiness checklist
- portability-check schema
- check_portability.py validator
- move the digital-state repo to another machine
- restore local config through Hermes-native mechanisms
- run checks after bootstrap
- operate in degraded/offline mode when models are unavailable
- provider credentials, OAuth, and gateway bindings remain local and must be restored by the operator.
- profile export/import runbooks tested across machines
- model smoke-test script with recorded results
- optional offline bundle checklist
### Model governance
- model council digest
- model council results JSON/Markdown
- model-review schema
- plan rules for returned/timeout/error handling
- no false consensus
- timeout/error models are not counted as reviewers
- synthesis only uses returned reviews
- provider/model provenance is recorded
- model quality is not certified; availability changes over time.
- repeatable model benchmark/smoke-test tool
- per-model timeout recommendations backed by measurements
- model risk tiers for production, advisory, and experimental use
### Safety-critical and mission-grade use
- approval matrix critical-grade section
- bootstrap readiness levels
- audit/provenance runbook
- manual approval over automation
- deterministic bootstrap checks
- offline-readable operating manuals
- no untested runtime enforcement claims
- Hermes is not certified for safety-critical, classified, export-controlled, or mission-critical use by these docs alone.
- formal hazard analysis
- security assessment
- independent review
- operational continuity plan
- incident response exercises
- organization-specific legal and compliance review
## Readiness Levels
- Spec Kit artifacts exist.
- No validators or docs beyond the plan.
- governance docs exist.
- approval matrix and portability guide exist.
- no runtime enforcement claims.
- schemas exist.
- validators run successfully.
- model council records are valid.
- portability checks pass for selected artifacts.
- profile/config/secrets restoration is documented.
- bootstrap readiness checks are repeatable.
- approval records are kept.
- model smoke tests are recorded.
- runtime guards exist and are tested.
- policies fail closed.
- audit records are append-only or tamper-evident.
- package/git/network operations are governed.
- independent security/compliance review is complete.
- mission-specific requirements are mapped.
- incident response and continuity procedures are exercised.
- legal, procurement, and safety authorities approve operation.
Current feature target: Level 2 with foundations for Level 3.
## Evidence Checklist
- current git diff summary
- validator outputs
- `hermes config check` output
- model council result file
- bootstrap readiness record
- approval record for any write/runtime change
- secret scan results
- test command outputs
Do not claim certification, accreditation, airworthiness, government approval, or mission authorization unless a qualified external process has granted it.

FILE: docs/governance/institutional-operating-model.md
# Institutional Operating Model for the Hermes Portable Digital State
It is Hermes-native and does not depend on any external project folder.
## Operating Principles
## Roles
### Sovereign Operator
- approve bootstrap and local profile restoration
- decide which providers and models are allowed
- approve irreversible actions
- maintain secrets outside the repo
- decide whether a deployment is personal, institutional, government, or mission-grade
### Strategy Ministry
- maintain constitution/spec/plan/tasks/analyze
- decide scope boundaries
- prevent runtime enforcement from entering docs-only features
- request Model Council review for major changes
### Operations Ministry
- maintain bootstrap checklists
- run validation commands
- record environment readiness
- keep runtime changes behind approved future features
### Signals Ministry
- scan for secrets, forbidden paths, dependency drift, and scope creep
- identify readiness gaps
- warn before high-risk operations
### Audit Office
- maintain model council records
- track validations and approvals
- preserve decision context
- prepare evidence bundles for review
### Model Council
- review compact digests
- return structured advice
- record timeout/error honestly
- never create false consensus from failed reviews
## Deployment Classes
### Personal
- manual approvals
- secret redaction enabled
- local docs and validators
- model council optional for major changes
### Team or institution
- shared approval matrix
- documented bootstrap
- recorded validators
- explicit provider/model allowlist
- audit records for runtime-impacting changes
### Government or regulated organization
- local legal/security review
- strict separation of secrets and repo artifacts
- explicit data classification rules
- restricted model/provider policy
- offline-readable procedures
- change control and retention policy
### Space-grade or mission-critical organization
- no autonomous destructive actions
- deterministic bootstrap checks
- independent hazard/security analysis
- tamper-evident audit trail
- model outputs treated as advisory only
- fail-closed runtime guards only after separate tested feature
## Change Classes
### Class A: Read-only
- reading docs/specs
- running validators
- generating reports
- model council reviews
- generally allowed unless sensitive data is involved.
### Class B: Safe repo writes
- docs updates
- Spec Kit updates
- schema drafts
- tests for read-only scripts
- allowed when within current feature scope.
### Class C: Runtime-impacting changes
- tool dispatch changes
- gateway changes
- provider routing changes
- model fallback changes
- config defaults
- requires explicit operator approval and a Spec Kit task.
### Class D: Destructive or irreversible
- deleting files
- `git reset --hard`
- changing credentials
- deployment operations
- package/lockfile churn
- explicit approval, audit record, and rollback plan required.
### Class E: Critical-grade mission impact
- safety-critical automation
- government classified handling
- spacecraft/mission command contexts
- medical/legal/financial irreversible actions
- out of scope for repository docs alone; requires qualified authority and independent assessment.
## Portable Bootstrap Process
## Non-Goals
This operating model does not:
- certify Hermes for regulated use
- activate runtime enforcement
- replace organizational policy
- store secrets in the repo
- depend on external prototype folders
- guarantee model availability or quality
## Minimum Evidence for Institutional Use
- approved operating class
- bootstrap readiness result
- current model allowlist
- current provider/credential owner
- latest validator outputs
- audit/provenance policy
- incident contact and escalation path
- explicit statement of what is not enforced yet

FILE: docs/governance/space-grade-readiness.md
# Space-Grade Readiness Notes for the Hermes Portable Digital State
## Core Position
- constitution and governance docs
- read-only schemas and validators
- model provenance records
- approval matrix
- bootstrap readiness guidance
- audit/provenance runbooks
It does not provide:
- certified runtime enforcement
- formal verification
- tamper-proof audit storage
- classified data handling approval
- mission command authority
- safety-critical autonomy
## Mission-Grade Rules
## Readiness Domains
### Configuration
- config check output
- provider/model allowlist
- redaction settings
- approval mode
- profile restoration record
- unreviewed model/provider use
- accidental secret exposure
- inconsistent operator posture
### Portability
- clone/copy steps
- local secrets restoration steps
- validator outputs
- bootstrap readiness level
- no required external paths
- deployment cannot be reproduced on another machine
- hidden dependency on operator workstation
### Model governance
- model council records
- model status: returned, timeout, error, empty, skipped
- synthesis record showing only returned reviews influenced decisions
- per-model smoke-test or benchmark records when available
- false consensus
- dependence on unavailable or unstable models
### Audit and provenance
- decision records
- validation run records
- approval records
- artifact checksums where practical
- incident records for blocked or failed actions
- inability to reconstruct why a decision was made
- weak change accountability
### Runtime enforcement
- separate Spec Kit feature
- tests before implementation
- policy parser
- fail-closed behavior
- deny/allow decisions logged
- rollback plan
- not implemented in this feature.
- operators may believe Hermes blocks unsafe actions when it only documents policy.
## Mission Readiness Levels
- Ideas are documented.
- No repeatable checks.
- Spec Kit and governance docs exist.
- No enforcement claims.
- schemas and validators exist.
- portability and model council records validate.
- bootstrap process is repeatable.
- local config/secrets restoration is documented.
- approvals and audit records are maintained.
- runtime guards are implemented in a separate feature.
- policy failures fail closed.
- tests cover deny/allow paths.
- external security/safety assessment completed.
- organization-specific compliance mapping completed.
- continuity and incident procedures exercised.
- qualified authority grants explicit authorization.
- operational constraints are documented and enforced.
- monitoring, rollback, and accountability are active.
Current feature target: MRL-2 foundations, with documentation supporting future MRL-3.
## Prohibited Claims Without External Approval
Do not claim:
- flight ready
- safety certified
- government accredited
- classified data approved
- ITAR/EAR compliant
- mission command approved
- autonomous mission operations ready
- tamper-proof audit trail
- governance foundations
- portable digital-state artifacts
- read-only validators
- advisory model council
- bootstrap readiness checklist
- future enforcement candidate
## Next Safe Improvements