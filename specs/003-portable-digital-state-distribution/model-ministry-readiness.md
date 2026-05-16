# Model Ministry Readiness: Pre-GitHub Check

This check tests the Digital State model-ministry architecture without fallback substitution.

## Policy

Fallback is disabled for the Digital State ministry model test. Each ministry is tested only with its assigned model. If a model fails, the assigned ministry is marked failed/slow/experimental; another model is not substituted.

## Results

| Ministry | Model | Status | Observed time | Launch critical | Notes |
|---|---|---:|---:|---:|---|
| Strategy Ministry | openai-codex:gpt-5.5 | returned | CLI returned `STRATEGY_OK` | yes | Primary strategy/synthesis model. |
| Operations Ministry | nvidia:meta/llama-4-maverick-17b-128e-instruct | returned | 0.767s | yes | Healthy and fast. |
| Signals Ministry | nvidia:mistralai/mistral-large-3-675b-instruct-2512 | returned | 21.996s | yes | Healthy; slower than Llama but acceptable. |
| Audit Office | nvidia:z-ai/glm-5.1 | returned after retry | 172.297s retry | no | First 240s attempt failed; retry with 420s returned. Slow healthy only. |
| Governance Office | nvidia:deepseek-ai/deepseek-v4-flash | returned | 213.927s | no | Very slow; ministry-specific reasoning only. |
| Citizen Services | nvidia:minimaxai/minimax-m2.7 | returned | 50.850s | no | Works in this smoke test; keep experimental due prior response-shape variability. |
| Research and Space Planning | nvidia:moonshotai/kimi-k2.6 | returned | 19.457s | no | Worked in this run; keep ministry-specific only. |
| Reserve / Not assigned | nvidia:deepseek-ai/deepseek-v4-pro | not launch-ready | previous 300s timeout | no | Not assigned to any ministry until it passes readiness. |

## Launch interpretation

The system is not using fallback for ministries.

The launch-critical ministries passed:

- Strategy Ministry
- Operations Ministry
- Signals Ministry

Non-critical ministries are usable but some are slow or experimental. The GitHub release can document these as ministry-specific/experimental, not as guaranteed fast chat paths.

## Evidence files

- `specs/003-portable-digital-state-distribution/model-ministry-readiness-results.json`
- `specs/003-portable-digital-state-distribution/model-ministry-readiness-glm-retry.json`
- `specs/003-portable-digital-state-distribution/fixtures/model-ministry-routing.json`
