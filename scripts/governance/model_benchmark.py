#!/usr/bin/env python3
"""Benchmark Hermes Model Council models without changing runtime state.

This script is intentionally standalone/stdlib-only. It can run real NVIDIA
OpenAI-compatible chat probes when NVIDIA_API_KEY is present, but its report
format is useful even in dry-run/test contexts.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODELS = [
    "z-ai/glm-5.1",
    "deepseek-ai/deepseek-v4-pro",
    "deepseek-ai/deepseek-v4-flash",
    "mistralai/mistral-large-3-675b-instruct-2512",
    "minimaxai/minimax-m2.7",
    "moonshotai/kimi-k2.6",
    "meta/llama-4-maverick-17b-128e-instruct",
]
DEFAULT_PROMPTS = {
    "smoke": "Reply with exactly: OK",
    "chat": "In two concise sentences, explain why portable governance matters for an AI agent.",
    "analysis": "List five risks and five mitigations for adding runtime governance guards to an AI agent. Keep it concise.",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * pct
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[int(rank)]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (rank - lower)


def recommend_timeout_seconds(
    records: list[dict[str, Any]],
    *,
    minimum: int = 60,
    maximum: int = 600,
    margin: float = 2.0,
) -> int:
    """Recommend timeout from successful total durations or prior attempts.

    If there are successful attempts, use ceil(P95 * margin), clamped. If all
    attempts failed, keep the largest attempted timeout so repeated failures do
    not accidentally lower the threshold.
    """
    successful = [float(r["total_seconds"]) for r in records if r.get("status") == "returned" and r.get("total_seconds") is not None]
    if successful:
        recommended = int(math.ceil(percentile(successful, 0.95) * margin))
        return max(minimum, min(maximum, recommended))
    attempted = [int(r.get("timeout_seconds", 0)) for r in records if r.get("timeout_seconds")]
    if attempted:
        return max(minimum, min(maximum, max(attempted)))
    return minimum


def summarize_model(model: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    model_records = [r for r in records if r.get("model") == model]
    success = [r for r in model_records if r.get("status") == "returned"]
    total_seconds = [float(r["total_seconds"]) for r in success if r.get("total_seconds") is not None]
    attempt_count = len(model_records)
    success_count = len(success)
    success_rate = (success_count / attempt_count) if attempt_count else 0.0
    return {
        "model": model,
        "attempt_count": attempt_count,
        "success_count": success_count,
        "success_rate": round(success_rate, 3),
        "avg_total_seconds": round(sum(total_seconds) / len(total_seconds), 3) if total_seconds else None,
        "max_total_seconds": round(max(total_seconds), 3) if total_seconds else None,
        "recommended_timeout_seconds": recommend_timeout_seconds(model_records),
        "chat_ready": success_rate >= 0.8 and bool(total_seconds) and percentile(total_seconds, 0.95) <= 120,
    }


def chat_completion_once(
    *,
    model: str,
    prompt_name: str,
    prompt: str,
    api_key: str,
    base_url: str,
    timeout_seconds: int,
    max_tokens: int,
) -> dict[str, Any]:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0,
        "stream": False,
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8", errors="replace")
        elapsed = time.monotonic() - started
        payload = json.loads(raw)
        choice = (payload.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        content = message.get("content") or message.get("reasoning_content") or ""
        return {
            "model": model,
            "prompt": prompt_name,
            "status": "returned" if content else "empty",
            "total_seconds": round(elapsed, 3),
            "timeout_seconds": timeout_seconds,
            "content_preview": str(content)[:500],
            "finish_reason": choice.get("finish_reason"),
        }
    except Exception as exc:  # noqa: BLE001 - CLI report should capture all failures
        elapsed = time.monotonic() - started
        return {
            "model": model,
            "prompt": prompt_name,
            "status": "timeout_or_error",
            "total_seconds": round(elapsed, 3),
            "timeout_seconds": timeout_seconds,
            "error": describe_error(exc),
        }


def describe_error(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        try:
            body = exc.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            body = ""
        return f"HTTP {exc.code}: {body}"
    return f"{exc.__class__.__name__}: {exc}"


def sanitized_report(report: dict[str, Any]) -> dict[str, Any]:
    blocked = {"api_key", "authorization", "token", "secret"}
    return {key: value for key, value in report.items() if key.lower() not in blocked}


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sanitized_report(report), indent=2, sort_keys=True), encoding="utf-8")


def parse_models(value: str | None) -> list[str]:
    if not value:
        return list(DEFAULT_MODELS)
    return [item.strip() for item in value.split(",") if item.strip()]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Benchmark Model Council/NVIDIA chat models.")
    parser.add_argument("--provider", default="nvidia", choices=["nvidia"], help="Provider to benchmark.")
    parser.add_argument("--models", help="Comma-separated model ids. Defaults to Hermes NVIDIA council models.")
    parser.add_argument("--base-url", default=os.getenv("NVIDIA_BASE_URL", DEFAULT_NVIDIA_BASE_URL))
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--max-tokens", type=int, default=96)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--suite", choices=["smoke", "chat", "analysis", "all"], default="smoke")
    parser.add_argument("--output", type=Path, default=Path("specs/001-hyperagent-governance-integration/model-benchmark-results.json"))
    parser.add_argument("--dry-run", action="store_true", help="Write the planned benchmark without network calls.")
    args = parser.parse_args(argv[1:])

    models = parse_models(args.models)
    prompt_items = list(DEFAULT_PROMPTS.items()) if args.suite == "all" else [(args.suite, DEFAULT_PROMPTS[args.suite])]
    api_key = os.getenv("NVIDIA_API_KEY", "")
    if not args.dry_run and not api_key:
        print(json.dumps({"ok": False, "error": "NVIDIA_API_KEY is required unless --dry-run is used"}, indent=2), file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    if args.dry_run:
        for model in models:
            for prompt_name, _prompt in prompt_items:
                for _ in range(args.repeat):
                    results.append({"model": model, "prompt": prompt_name, "status": "skipped", "timeout_seconds": args.timeout, "reason": "dry_run"})
    else:
        for model in models:
            for prompt_name, prompt in prompt_items:
                for _ in range(args.repeat):
                    results.append(
                        chat_completion_once(
                            model=model,
                            prompt_name=prompt_name,
                            prompt=prompt,
                            api_key=api_key,
                            base_url=args.base_url,
                            timeout_seconds=args.timeout,
                            max_tokens=args.max_tokens,
                        )
                    )

    summaries = [summarize_model(model, results) for model in models]
    report = {
        "ok": True,
        "schema_version": "model-benchmark-v1",
        "created_at": now_iso(),
        "provider": args.provider,
        "base_url": args.base_url,
        "suite": args.suite,
        "repeat": args.repeat,
        "results": results,
        "summaries": summaries,
        "api_key": api_key,
    }
    write_report(args.output, report)
    print(json.dumps(sanitized_report({"ok": True, "output": str(args.output), "summaries": summaries}), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
