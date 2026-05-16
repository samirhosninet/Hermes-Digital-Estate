# Pre-GitHub Model Readiness Check

Purpose: record live model health before publishing the Digital State Profile Distribution to GitHub.

Scope: no runtime/core changes; smoke checks only; secrets are not stored in these artifacts.

## Result

| Model | Status now | Evidence | Suggested launch role |
|---|---:|---|---|
| gpt-5.5 | PASS | `hermes chat --provider openai-codex -m gpt-5.5` returned `OK` | primary chat/default |
| meta/llama-4-maverick-17b-128e-instruct | PASS | 1/1, avg 17.116s, recommended timeout 60s, `model-benchmark-pre-github-smoke-results.json` | usable; prefer fallback if stable |
| mistralai/mistral-large-3-675b-instruct-2512 | PASS | 1/1, avg 4.094s, recommended timeout 60s, `model-benchmark-retry-mistral.json` | usable; prefer fallback if stable |
| z-ai/glm-5.1 | PASS | 1/1, avg 106.568s, recommended timeout 214s, `model-benchmark-retry-glm.json` | usable; prefer fallback if stable |
| deepseek-ai/deepseek-v4-flash | PASS | 1/1, avg 42.683s, recommended timeout 86s, `model-benchmark-pre-github-smoke-results.json` | usable; prefer fallback if stable |
| minimaxai/minimax-m2.7 | PASS | 1/1, avg 18.962s, recommended timeout 60s, `model-benchmark-pre-github-smoke-results.json` | usable; prefer fallback if stable |
| moonshotai/kimi-k2.6 | PASS | 1/1, avg 97.659s, recommended timeout 196s, `model-benchmark-retry-kimi.json` | usable; prefer fallback if stable |
| deepseek-ai/deepseek-v4-pro | FAIL/TIMEOUT | 0/1, timeout 300s, `model-benchmark-retry-deepseek-pro-300.json` | exclude from launch-critical fallback |

## Launch recommendation

- Use `gpt-5.5` as the primary chat model.
- Use `meta/llama-4-maverick-17b-128e-instruct` as first NVIDIA fallback.
- Use `mistralai/mistral-large-3-675b-instruct-2512` as second fallback / analysis model.
- Treat `z-ai/glm-5.1`, `moonshotai/kimi-k2.6`, `deepseek-ai/deepseek-v4-flash`, and `minimaxai/minimax-m2.7` as available but slow/variable; do not make them launch-critical defaults.
- Do not rely on `deepseek-ai/deepseek-v4-pro` for launch: it timed out even with a 300s smoke test in this run.

## Important interpretation

NVIDIA catalog presence is not enough for launch readiness. A model is launch-ready only if it returns a live chat/completions response during smoke or benchmark checks.
