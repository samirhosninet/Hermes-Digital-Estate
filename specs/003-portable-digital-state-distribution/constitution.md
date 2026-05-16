# Constitution: Portable Digital-State Distribution

## Purpose

Feature 003 defines how the Hermes digital-state layer is packaged, installed, bootstrapped, updated, and recovered without forking or breaking upstream Hermes Agent.

Hermes Agent remains the official upstream runtime. The digital state is a portable Hermes-native layer distributed primarily as a GitHub-hosted Hermes Profile Distribution for users, teams, institutions, governments, or critical-grade operators.

## Core Principles

### 1. Upstream Hermes First

The user installs and updates the official Hermes Agent first. This feature must not require a custom fork, patched installer, or external prototype folder.

### 2. Profile Distribution First

The canonical distribution mechanism is Hermes Profile Distributions, preferably installed from a GitHub repository and updated with Hermes profile update flows. Custom import/export scripts are secondary support tools only.

### 3. Portable Layer, Not Core Replacement

Digital-state artifacts are distributed as repository-relative files: distribution metadata, SOUL/profile guidance, specs, docs, skills, schemas, validators, fixtures, and tests. They do not replace Hermes runtime internals.

### 4. No Secrets in the Distribution

The distribution must never include API keys, OAuth tokens, auth stores, gateway tokens, real `.env`, logs, session transcripts, memories, unsanitized profile archives, or machine-specific absolute paths.

### 5. Easy for New Users

A new user should be able to:

1. Install official Hermes Agent.
2. Install the Digital State Profile Distribution from GitHub or a local distribution path.
3. Run bootstrap checks.
4. Add their own credentials locally.
5. Use the layer through Hermes workspace, profile, CLI, skills, docs, and scripts.
6. Update Digital State separately from Hermes core.

### 6. Update-Safe by Default

The distribution must survive Hermes upstream updates by minimizing core changes, using repo-relative artifacts, and providing update/recovery checks.

### 7. Workspace-Native UX First

Do not create a separate dashboard or UI in this feature. Use Hermes workspace, profile distribution, CLI scripts, skills, docs, and future Hermes-native commands/slash commands. A separate UI is out of scope.

### 8. Read-Only Bootstrap Before Mutation

Bootstrap checks must be read-only. Any optional import/export support may write only within an explicit destination or archive path and must refuse unsafe paths.

### 9. Institutional Without False Certification

The distribution may support evidence, auditability, readiness levels, and operating models for institutions/governments/space-grade agencies. It must not claim certification, accreditation, or mission approval.

### 10. Runtime Enforcement Remains Separate

Runtime hooks, blocking behavior, terminal/file enforcement, gateway enforcement, or model-routing enforcement remain governed by Feature 002 and require explicit approval records. Feature 003 only distributes the layer.

## No-Go Gates

Feature 003 must not:

- Modify Hermes core runtime files.
- Change terminal/file/gateway/model routing behavior.
- Add package dependencies or lockfile changes.
- Include secrets or unsanitized local config in exported or installed distributions.
- Depend on Windows drive paths, mounted-drive paths, home-directory paths, or any local absolute path.
- Create a standalone UI/dashboard.
- Claim regulatory or space-flight certification.
- Replace Hermes Profile Distribution with a competing primary installer.
