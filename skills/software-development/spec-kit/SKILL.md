---
name: spec-kit
description: "Use when bootstrapping or operating GitHub Spec Kit / Specify CLI workflows for spec-driven development: install Specify, initialize a project, create constitution/spec/plan/tasks artifacts, run implementation, and work around integration limitations from Hermes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [spec-kit, specify-cli, spec-driven-development, planning, requirements, implementation]
    homepage: https://github.com/github/spec-kit
    related_skills: [writing-plans, test-driven-development, github-issues, github-pr-workflow]
---

# GitHub Spec Kit

## Overview

Spec Kit is GitHub's open-source toolkit for Spec-Driven Development (SDD). It makes specifications first-class development artifacts: a project constitution defines governing principles, a feature spec captures the what and why, a plan captures technical decisions, tasks break the plan into implementable work, and implementation follows those artifacts instead of free-form prompting.

The `specify` CLI bootstraps projects with Spec Kit templates and AI-agent integrations. Most supported agents receive `/speckit.*` slash commands. Some agents install these workflows as skills instead. Hermes may not be a built-in Spec Kit integration in the installed version, so use this skill to operate the same process directly and, when useful, initialize an adjacent supported integration such as `codex`, `claude`, or `copilot` to get the generated artifacts and templates.

Official source: https://github.com/github/spec-kit
Docs: https://github.github.io/spec-kit/

## When to Use

Use this skill when the user asks to:

- Add or use GitHub Spec Kit, Specify CLI, or Spec-Driven Development.
- Turn an idea into a constitution, feature spec, implementation plan, task list, or implementation run.
- Initialize an existing or new project with `.specify/` artifacts.
- Convert Spec Kit tasks into GitHub issues.
- Validate consistency across spec, plan, and tasks before coding.
- Work with `/speckit.constitution`, `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.analyze`, `/speckit.taskstoissues`, or `/speckit.implement` workflows.

Do not use this skill for small one-off code edits where the user explicitly wants a quick direct patch and no specification process.

## Prerequisites

Spec Kit requires:

- Python 3.11+
- Git
- `uv` recommended, or `pipx` as an alternative
- A target project directory

Check prerequisites before installing or initializing:

```bash
python3 --version
python --version
uv --version || true
pipx --version || true
git --version
```

If `uv` is missing, install it from the official uv installer or use `pipx`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

## Install Specify CLI

Important: Spec Kit's maintainers warn that the official maintained packages are installed directly from the GitHub repository. Do not install an unrelated PyPI package with the same name.

Recommended persistent install, pinned to a release tag when possible:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
specify version
```

Install latest from `main` if the user accepts unreleased changes:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify version
```

`pipx` alternative:

```bash
pipx install git+https://github.com/github/spec-kit.git@vX.Y.Z
# or latest main
pipx install git+https://github.com/github/spec-kit.git
specify version
```

One-time use without persistent install:

```bash
uvx --from git+https://github.com/github/spec-kit.git@vX.Y.Z specify init <PROJECT_NAME>
```

Upgrade:

```bash
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git@vX.Y.Z
# pipx users:
pipx install --force git+https://github.com/github/spec-kit.git@vX.Y.Z
```

## Initialize a Project

For a new project:

```bash
specify init <PROJECT_NAME> --integration copilot
```

For an existing project:

```bash
cd <PROJECT_DIR>
specify init . --integration copilot
# or
specify init --here --integration copilot
```

For a non-empty directory where merging is intentional:

```bash
specify init . --force --integration copilot
# or
specify init --here --force --integration copilot
```

If agent CLI checks block initialization or the target integration's tool is not installed, use:

```bash
specify init . --integration copilot --ignore-agent-tools
```

For integrations that support skills mode, use:

```bash
specify init . --integration codex --integration-options="--skills"
```

List integrations supported by the installed Specify version:

```bash
specify integration list
```

## Hermes Usage Pattern

Hermes does not need Spec Kit slash commands to follow the workflow. When the user asks Hermes to run Spec Kit, do this:

1. Verify the project root and inspect existing `.specify/`, `specs/`, and agent command files.
2. If the project is not initialized, install Specify if needed and run `specify init` with an appropriate integration. Prefer `--ignore-agent-tools` when only templates are needed.
3. Treat the Spec Kit phases as explicit Hermes tasks:
   - Constitution: write or update `.specify/memory/constitution.md`.
   - Specify: create or update a feature specification under `specs/<feature>/spec.md`.
   - Clarify: list open questions and resolve them with the user before planning if requirements are ambiguous.
   - Plan: create or update the technical plan, research notes, data model, contracts, and quickstart files expected by the project's templates.
   - Tasks: create an ordered `tasks.md` with dependencies, parallelizable tasks, and acceptance criteria.
   - Analyze: check consistency and coverage across spec, plan, and tasks.
   - Implement: execute tasks, run tests, and update artifacts when implementation reveals legitimate changes.
4. Preserve the distinction between requirements and implementation choices: specs describe what and why; plans describe how.
5. Do not skip verification. Run project tests and perform an artifact consistency check before reporting completion.

When Spec Kit generated slash-command prompt files are present, read the relevant command file before reproducing that phase in Hermes. Typical locations vary by integration, for example `.claude/commands/`, `.github/prompts/`, `.gemini/commands/`, `.agents/skills/`, or another agent-specific directory.

## Core Workflow

### 1. Constitution

Purpose: define non-negotiable project principles and governance. This usually writes `.specify/memory/constitution.md`.

Prompt pattern:

```text
Create principles focused on code quality, testing standards, user experience consistency, security, performance requirements, and governance for technical decisions.
```

Hermes action:

- Inspect existing docs, tests, package files, and architecture notes.
- Draft principles that are specific enough to guide tradeoffs.
- Include governance: how principles are amended, versioned, and enforced.
- Avoid vague principles such as “write clean code” unless paired with measurable rules.

### 2. Specify

Purpose: capture what to build and why without prematurely choosing the stack.

Prompt pattern:

```text
Build <product/feature>. It should allow <users> to <capabilities>. Include <constraints>, <edge cases>, and <success criteria>. Do not choose implementation technology yet.
```

Hermes action:

- Create user stories, functional requirements, assumptions, edge cases, and measurable success criteria.
- Mark ambiguities explicitly. If they block planning, ask concise clarification questions.
- Keep implementation details out unless the user provided them as hard constraints.

### 3. Clarify

Purpose: resolve underspecified areas before planning.

Hermes action:

- Identify gaps that would materially change data model, UX, architecture, security, or scope.
- Ask the smallest set of questions needed.
- Record answers in the spec or a checklist.
- Do not ask about details that can be decided safely during planning.

### 4. Plan

Purpose: choose implementation approach, architecture, technology, and validation strategy.

Prompt pattern:

```text
Use <stack>. Store data in <database>. Follow <architecture constraints>. Include test strategy, security considerations, and deployment assumptions.
```

Hermes action:

- Read the constitution and spec first.
- Produce plan artifacts using project templates when available.
- Include technical context, constraints, structure, risks, test strategy, and acceptance checks.
- Flag constitution violations and either revise the plan or ask the user to approve a principle change.

### 5. Tasks

Purpose: generate an actionable, ordered task list from the spec and plan.

Hermes action:

- Break work into small tasks with clear file targets and acceptance criteria.
- Separate setup, tests, implementation, integration, polish, and documentation.
- Mark dependencies and tasks that can run in parallel.
- Prefer test-first tasks when the project has a test framework.
- Avoid tasks that are too broad, such as “build the backend.”

### 6. Analyze

Purpose: check artifact consistency and coverage after task generation and before implementation.

Hermes action:

- Verify every functional requirement maps to one or more tasks.
- Verify every planned component has implementation and test tasks.
- Check for contradictions between constitution, spec, plan, and tasks.
- Check edge cases and non-functional requirements are covered.
- Produce a short findings list and fix artifacts before coding when possible.

### 7. Taskstoissues

Purpose: convert tasks into GitHub issues for tracking.

Hermes action:

- Load the `github-issues` skill before creating issues.
- Confirm repository target and labels if not obvious.
- Preserve task dependencies and acceptance criteria in issue bodies.
- Avoid creating duplicate issues; search existing open issues first.

### 8. Implement

Purpose: execute the tasks and build the feature according to the plan.

Hermes action:

- Read constitution, spec, plan, and tasks before editing code.
- Follow task order unless a dependency requires adjustment.
- Update task status as work progresses.
- Run tests and linters relevant to changed files.
- If implementation reveals a spec or plan issue, update the artifact and note why.
- Keep changes scoped to the feature.

## Artifact Checklist

After initialization or a workflow phase, inspect these common paths:

```bash
find . -maxdepth 4 -type f \( -path './.specify/*' -o -path './specs/*' \) | sort
```

Common artifacts:

- `.specify/memory/constitution.md`
- `.specify/templates/`
- `.specify/scripts/`
- `specs/<feature>/spec.md`
- `specs/<feature>/plan.md`
- `specs/<feature>/tasks.md`
- `specs/<feature>/research.md`
- `specs/<feature>/data-model.md`
- `specs/<feature>/contracts/`
- `specs/<feature>/quickstart.md`

Exact paths may vary by Spec Kit version, installed preset, or project-local override. Prefer discovering files over assuming fixed paths.

## Extensions and Presets

Spec Kit customization has four priority layers, highest first:

1. Project-local overrides: `.specify/templates/overrides/`
2. Presets: `.specify/presets/templates/`
3. Extensions: `.specify/extensions/templates/`
4. Core templates: `.specify/templates/`

Use extensions to add new commands, external integrations, or new phases:

```bash
specify extension search
specify extension add <extension-name>
```

Use presets to customize formats, terminology, standards, or methodology without adding a new capability:

```bash
specify preset search
specify preset add <preset-name>
```

When changing templates for one project only, prefer project-local overrides over editing core templates.

## Good Hermes Prompts for Spec Kit

Constitution:

```text
Use Spec Kit to create a constitution for this project. Inspect the repo first, then write principles for testing, architecture boundaries, security, performance, UX consistency, and governance.
```

Specify:

```text
Use Spec Kit to draft a feature spec for: <feature idea>. Focus on user outcomes, functional requirements, edge cases, assumptions, and measurable success criteria. Do not choose a tech stack yet.
```

Plan:

```text
Use Spec Kit to create the technical plan for the current feature. Stack constraints: <stack>. Include architecture, data model, contracts, tests, risks, and constitution compliance.
```

Tasks:

```text
Use Spec Kit to generate tasks from the spec and plan. Make tasks small, ordered, dependency-aware, test-first where possible, and include file paths and acceptance criteria.
```

Analyze:

```text
Use Spec Kit to analyze consistency across constitution, spec, plan, and tasks. Report gaps, contradictions, uncovered requirements, and fixes needed before implementation.
```

Implement:

```text
Use Spec Kit to implement the current feature from tasks.md. Follow task order, keep changes scoped, update artifacts if needed, and run tests before reporting completion.
```

## Common Pitfalls

1. Installing the wrong package from PyPI. Use `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git...` or `pipx install git+https://github.com/github/spec-kit.git...`.

2. Treating `/speckit.*` as universal Hermes slash commands. They are generated for supported Spec Kit integrations. In Hermes, read the generated command templates or follow the workflow directly.

3. Skipping the constitution. Without governing principles, later planning lacks a stable basis for tradeoffs.

4. Mixing spec and plan. The spec should focus on what and why; technology choices belong in the plan.

5. Implementing before `tasks.md` is checked for coverage. Run an analyze pass before coding.

6. Assuming fixed artifact paths. Spec Kit versions, presets, and extensions can change layout. Discover files in `.specify/` and `specs/`.

7. Running `--force` in a populated directory without checking the diff. Initialize carefully and inspect generated changes.

8. Creating GitHub issues without deduplication. Search existing issues first.

9. Letting implementation drift from spec. If the code must diverge, update the spec or plan with rationale.

## Verification Checklist

- [ ] `specify version` works, or one-time `uvx` command was used intentionally.
- [ ] `specify integration list` was checked when choosing an integration.
- [ ] Project initialization created or updated `.specify/` and relevant agent files.
- [ ] Constitution exists before feature planning.
- [ ] Feature spec states what/why, user stories, requirements, edge cases, assumptions, and success criteria.
- [ ] Technical plan cites constraints, architecture, data model/contracts when relevant, tests, and risks.
- [ ] Tasks are small, ordered, dependency-aware, and map to requirements.
- [ ] Analyze pass found no unresolved blockers before implementation.
- [ ] Tests/linters relevant to changed code were run.
- [ ] Artifact changes and code changes are both included in the final summary.
