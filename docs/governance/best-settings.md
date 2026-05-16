# Recommended Hermes Settings for the Digital State

These are recommended operator settings, not hard requirements for the repo.

## Baseline

- Primary chat model: `gpt-5.5` via `openai-codex` when available.
- NVIDIA fallback for chat: `meta/llama-4-maverick-17b-128e-instruct`.
- NVIDIA fallback for deeper analysis: `mistralai/mistral-large-3-675b-instruct-2512`.
- Compression: enabled, with a threshold around 0.5 and a target ratio around 0.2.
- Approvals: `smart` for daily work, `manual` for critical/government/space-grade deployments.
- Secret redaction: enabled for shared/enterprise/government environments.
- Model Council: record every requested model as returned, timeout/error, empty, or skipped.

## Do not store in repo

Do not commit API keys, OAuth stores, gateway tokens, auth JSON, local `.env`, or unsanitized profile exports.

## Critical environments

For institutions, governments, and space agencies, prefer manual approvals, least-privilege toolsets, no YOLO mode, offline-readable docs, and written audit records for irreversible actions.
