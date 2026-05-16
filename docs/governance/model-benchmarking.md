# Model Benchmarking for the Portable Digital State

This document defines how Hermes Agent measures Model Council readiness without guessing and without changing runtime routing.

## Purpose

Model benchmark records are evidence artifacts. They answer:

- which configured models currently respond
- which models time out or return unusable output
- which models are reasonable for chat, planning, or heavy analysis
- what timeout value should be tested next

A model listed in a provider catalog is not considered healthy until it returns a usable completion in a benchmark or Model Council run.

## Tool

Use the stdlib-only script:

```bash
python3 scripts/governance/model_benchmark.py --suite smoke --repeat 1 --timeout 60 --max-tokens 32 --output specs/001-hyperagent-governance-integration/model-benchmark-smoke-results.json
```

If `NVIDIA_API_KEY` is stored in the Hermes env file, load it without printing secrets:

```bash
set -a; [ -f ~/.hermes/.env ] && source ~/.hermes/.env; set +a
python3 scripts/governance/model_benchmark.py --suite smoke --repeat 1 --timeout 60 --max-tokens 32
```

For deeper calibration, run:

```bash
python3 scripts/governance/model_benchmark.py --suite all --repeat 3 --timeout 180 --max-tokens 128
```

## Suites

- `smoke`: minimal OK response. Use to confirm endpoint health.
- `chat`: short ordinary chat task. Use to select chat/fallback models.
- `analysis`: concise governance analysis. Use to evaluate planning/model-council usefulness.
- `all`: runs all three suites.

## Readiness Classes

- `chat_ready: true`: enough successful responses and low latency for everyday chat/fallback use.
- `returned but slow`: usable for analysis or council review, not first fallback.
- `timeout_or_error`: attempted but not counted as a reviewer or healthy model.
- `empty`: endpoint returned but produced no usable content; treat as unhealthy until fixed.
- `skipped`: dry-run or intentionally not called.

## Current Smoke Evidence

The latest smoke run is stored at:

`specs/001-hyperagent-governance-integration/model-benchmark-smoke-results.json`

At 60 seconds per model, the models that returned were:

- `mistralai/mistral-large-3-675b-instruct-2512` in about 1.0s
- `meta/llama-4-maverick-17b-128e-instruct` in about 1.6s

The models that timed out in this run were:

- `z-ai/glm-5.1`
- `deepseek-ai/deepseek-v4-pro`
- `deepseek-ai/deepseek-v4-flash`
- `minimaxai/minimax-m2.7`
- `moonshotai/kimi-k2.6`

This is a point-in-time provider-health record, not a permanent judgment about model quality.

## Timeout Policy

Use evidence, not assumptions:

1. Start with `smoke` at 60 seconds.
2. Promote returned models to `chat` at 120 seconds.
3. Promote stable chat models to `analysis` at 180-300 seconds.
4. For heavy or inconsistent models, test 300-600 seconds only when their output is valuable enough to justify waiting.
5. Do not make a timeout-heavy model the default chat model.

## Safety Rules

- Do not write API keys to reports.
- Do not treat timeouts as reviews.
- Do not change default routing from a single benchmark run.
- Keep benchmark results repo-relative and portable.
- Keep operator-local credentials in `~/.hermes/.env` or profile-local state, not in the repository.

## Deep Benchmark Evidence

The latest deep benchmark is stored at:

`specs/001-hyperagent-governance-integration/model-benchmark-deep-results.json`

Command shape:

```bash
python3 scripts/governance/model_benchmark.py --suite all --repeat 3 --timeout 180 --max-tokens 128 --models 'mistralai/mistral-large-3-675b-instruct-2512,meta/llama-4-maverick-17b-128e-instruct' --output specs/001-hyperagent-governance-integration/model-benchmark-deep-results.json
```

Point-in-time result:

- `meta/llama-4-maverick-17b-128e-instruct`: 9/9 returned, average about 1.754s, max about 3.05s, recommended timeout 60s. Best NVIDIA chat/fallback candidate from this evidence.
- `mistralai/mistral-large-3-675b-instruct-2512`: 8/9 returned, average about 27.949s, max successful about 57.313s, one 180s timeout, recommended timeout 104s by the script. Good analysis/council candidate, but less stable than Llama 4 for first fallback.

Recommended current NVIDIA roles from this evidence:

1. First NVIDIA chat fallback: `meta/llama-4-maverick-17b-128e-instruct`.
2. Analysis / heavier council reviewer: `mistralai/mistral-large-3-675b-instruct-2512`.
3. Timeout-heavy models should stay late in fallback order until they pass a future benchmark.

Do not treat this as permanent provider truth; repeat after provider changes, major config changes, or before high-risk governance phases.
