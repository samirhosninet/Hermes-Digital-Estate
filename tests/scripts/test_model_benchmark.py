import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "governance" / "model_benchmark.py"


def load_module():
    spec = importlib.util.spec_from_file_location("model_benchmark", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["model_benchmark"] = module
    spec.loader.exec_module(module)
    return module


class ModelBenchmarkTests(unittest.TestCase):
    def test_recommended_timeout_uses_successful_p95_with_safety_margin(self):
        bench = load_module()
        records = [
            {"status": "returned", "total_seconds": 10.0},
            {"status": "returned", "total_seconds": 20.0},
            {"status": "returned", "total_seconds": 30.0},
        ]
        self.assertEqual(bench.recommend_timeout_seconds(records, minimum=30, maximum=600, margin=2.0), 58)

    def test_recommended_timeout_for_all_failures_uses_existing_timeout(self):
        bench = load_module()
        records = [
            {"status": "timeout_or_error", "timeout_seconds": 120},
            {"status": "timeout_or_error", "timeout_seconds": 180},
        ]
        self.assertEqual(bench.recommend_timeout_seconds(records, minimum=30, maximum=600), 180)

    def test_summarize_model_marks_chat_ready_only_when_success_rate_high(self):
        bench = load_module()
        records = [
            {"model": "m", "status": "returned", "total_seconds": 12.0, "timeout_seconds": 60},
            {"model": "m", "status": "returned", "total_seconds": 18.0, "timeout_seconds": 60},
            {"model": "m", "status": "timeout_or_error", "timeout_seconds": 60, "error": "timeout"},
        ]
        summary = bench.summarize_model("m", records)
        self.assertEqual(summary["success_count"], 2)
        self.assertEqual(summary["attempt_count"], 3)
        self.assertFalse(summary["chat_ready"])
        self.assertGreaterEqual(summary["recommended_timeout_seconds"], 36)

    def test_write_report_outputs_json_without_secret_value(self):
        bench = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            bench.write_report(
                path,
                {
                    "provider": "nvidia",
                    "api_key": "nvapi-secret-should-not-appear",
                    "results": [],
                    "summaries": [],
                },
            )
            text = path.read_text(encoding="utf-8")
        self.assertNotIn("nvapi-secret-should-not-appear", text)
        payload = json.loads(text)
        self.assertEqual(payload["provider"], "nvidia")
        self.assertNotIn("api_key", payload)


if __name__ == "__main__":
    unittest.main()
