# Governance Compliance Mapping

Purpose: provide an evidence map for organizations that want to evaluate Hermes Agent as a portable digital-state control plane. This document is not a certification, accreditation, legal opinion, export-control review, safety case, or mission authorization.

## Mapping principles

1. Evidence over claims: every maturity or compliance statement must point to a repo artifact, validator, test, approval record, or operator runbook.
2. Local-state separation: credentials, OAuth stores, platform tokens, and machine-specific profiles are operator-local and must not be committed.
3. Human authority: irreversible, destructive, credential, deployment, and mission-impacting actions require explicit human approval until a later audited runtime-guards feature exists.
4. Fail closed: missing governance status, malformed policies, or absent approval evidence must prevent escalation to higher readiness levels.
5. No false consensus: model reviews are counted only when the model returned usable output.

## Evidence map

| Governance concern | Current artifact | Evidence status | Gap before regulated use |
| --- | --- | --- | --- |
| Source of truth | specs/001-hyperagent-governance-integration/ | Present | External review and signed change-control process |
| Portability | docs/governance/portable-digital-state.md | Present | Automated bootstrap report and profile sanitization workflow |
| Approval boundaries | docs/governance/approval-matrix.md | Present | Runtime enforcement and signed approvals |
| Audit/provenance | docs/governance/audit-provenance.md | Present | Append-only storage and tamper-evident record hashes |
| Model review provenance | model-council-results*.json/md | Present | Automated per-review signatures and provider health evidence |
| Secret hygiene | scripts/governance/check_portability.py | Initial | Full secret scanning policy and CI gate |
| Bootstrap readiness | docs/governance/bootstrap-readiness.md | Present | Deterministic machine-readable readiness bundle |
| Institutional roles | docs/governance/institutional-operating-model.md | Present | Organization-specific role binding and access control |
| Mission/space posture | docs/governance/space-grade-readiness.md | Present | Formal safety case, hazard analysis, and independent verification |
| Validator integrity | scripts/governance/ | Initial | Script review, trusted revision pinning, checksums, and recorded command provenance |

## Alignment vocabulary

For enterprises, map artifacts to internal controls such as change management, access control, audit logging, data protection, incident response, and third-party/model risk management.

For governments, map artifacts to authority-to-operate preparation, least privilege, traceability, records management, offline operation, supply-chain review, and explicit human authorization.

For space or mission-critical agencies, map artifacts to configuration control, hazard analysis inputs, fail-safe/fail-closed principles, verification evidence, operator authority, and communications-degraded operation.

## Readiness wording

Current feature target: Level 2 documentation and read-only validation only. Level 3 requires separate implementation, operator adoption, and environment-specific validation.

Do not describe current artifacts as certified, accredited, mission-authorized, flight-ready, or runtime-enforced. Acceptable wording is: documented governance foundation, read-only validation, advisory model review, and future enforcement may be proposed in a separate feature.

## Non-claims

These artifacts do not certify Hermes Agent for regulated production, classified environments, safety-critical systems, spacecraft operations, medical use, weapons systems, or autonomous irreversible control. They provide a portable governance foundation that can be reviewed, extended, and independently assessed.
