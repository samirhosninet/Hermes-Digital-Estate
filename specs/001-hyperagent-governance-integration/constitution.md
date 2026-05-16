# Constitution: Hermes Portable Digital State

Feature: 001-hyperagent-governance-integration
Status: planning-only
Version: 1.0.0-draft
Intent: Build Hermes Agent as an independent, portable digital-state system for individual users, institutions, governments, and space-grade operating environments.

## Core Definition

The digital state is Hermes-native. It is not a link to any external project or workstation folder. It is represented by repository-relative Spec Kit artifacts, skills, docs, schemas, read-only validators, tests, model-review records, and later separately approved runtime guards.

## Constitutional Principles

1. Hermes is the state
Hermes Agent is the runtime and control plane. The state must live in Hermes-native artifacts and Hermes-native operator mechanisms, not in external folders, dashboards, or copied runtime systems.

2. Portable by design
Every portable artifact must be repository-relative and relocatable across Linux, macOS, Windows, and WSL. Machine-local state, credentials, OAuth tokens, platform secrets, provider keys, and local config stay outside committed artifacts and move only through Hermes profile/config/env mechanisms.

3. Ideas, not linkage
External digital-state research may inspire vocabulary and design, but there must be no runtime import, sync job, watcher, service dependency, path dependency, or operational coupling to any external concept source.

4. Policy and mechanism are separate
Spec Kit artifacts define policy: what the state believes, allows, blocks, audits, and reviews. Runtime code, if later approved, implements mechanisms. No executable code should hardcode governance policy when a schema or artifact can define it.

5. Read-only first
The first implementation phases may add docs, skills, schemas, fixtures, and read-only validators only. They must not modify tool dispatch, terminal/file tools, model routing, gateway behavior, dependency manifests, package locks, or long-running services.

6. Fail-closed future enforcement
Future enforcement must deny or require operator approval when policy is missing, malformed, stale, ambiguous, or incompatible. This constitution describes the rule now; runtime enforcement requires a separate Spec Kit feature later.

7. Model Council honesty
A model only counts as a reviewer if it returned usable output for that review. Timeouts, empty responses, and errors must be recorded separately. Synthesis may proceed with quorum, but claims must distinguish returned recommendations from attempted models.

8. Auditability and provenance
Major decisions need provenance: artifact path, timestamp, actor, model/provider when applicable, outcome, and a content hash or durable reference. Phase 1 may store this as files in the feature directory; later phases may add append-only audit storage.

9. Operator sovereignty
The operator, institution, or agency owns its state. No forced cloud sync, no hidden remote dependency, no implicit external control plane, and no secret committed into portable artifacts.

10. Zero-trust bootstrap
A copied or cloned state is not considered operational until bootstrap checks pass: Hermes version, profile/config presence, provider health, skills/docs availability, schema validation, and no forbidden path/secret leakage.

11. Minimal viable governance
Start with the smallest useful state: constitution, vocabulary, model council, portability contract, governance status, audit schema, and read-only validation. Add ministries, scanners, and guards in staged, tested increments.

12. Space/critical-grade restraint
For government or space-agency use, planning must assume unreliable networks, strict audit requirements, least privilege, reproducibility, offline documentation, deterministic bootstrap checks, and human approval for irreversible actions.

## Non-Negotiable No-Go Gates

Stop immediately if a task requires any of the following without a new approved Spec Kit feature:
- runtime coupling to an external folder or project
- importing external AGENTS/SOUL/specify/agent files as active Hermes instructions
- modifying dependency manifests or lockfiles
- editing terminal/file/model/gateway enforcement code
- starting dashboards, daemons, executors, or autonomous ministries
- committing secrets, tokens, OAuth state, machine IDs, or workstation-specific paths as required configuration
- claiming a model reviewed the plan when it timed out or errored
