import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTING_PATH = ROOT / "specs/003-portable-digital-state-distribution/fixtures/model-ministry-routing.json"
DOC_PATH = ROOT / "docs/governance/model-ministry-routing.md"
CONFIG_PATH = ROOT / "config.yaml"


class ModelMinistryRoutingTests(unittest.TestCase):
    def test_model_ministry_routing_contract_exists_and_disables_fallback(self):
        self.assertTrue(ROUTING_PATH.exists(), "model-ministry-routing fixture is required")
        payload = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))

        self.assertEqual(payload["schema_version"], "model-ministry-routing-v1")
        self.assertFalse(payload["fallback_enabled"])
        self.assertIn("ministries", payload)
        self.assertGreaterEqual(len(payload["ministries"]), 6)

        ministry_names = {item["name"] for item in payload["ministries"]}
        for expected in {
            "strategy-ministry",
            "operations-ministry",
            "signals-ministry",
            "audit-office",
            "governance-office",
            "citizen-services",
            "research-and-space-planning",
        }:
            self.assertIn(expected, ministry_names)

        assigned_models = {item["model"] for item in payload["ministries"]}
        for expected_model in {
            "openai-codex:gpt-5.5",
            "nvidia:meta/llama-4-maverick-17b-128e-instruct",
            "nvidia:mistralai/mistral-large-3-675b-instruct-2512",
            "nvidia:z-ai/glm-5.1",
            "nvidia:deepseek-ai/deepseek-v4-flash",
            "nvidia:minimaxai/minimax-m2.7",
            "nvidia:moonshotai/kimi-k2.6",
        }:
            self.assertIn(expected_model, assigned_models)

    def test_deepseek_pro_is_not_launch_critical_until_healthy(self):
        payload = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
        reserve = payload.get("reserve_models", [])
        deepseek_pro = [item for item in reserve if item.get("model") == "nvidia:deepseek-ai/deepseek-v4-pro"]
        self.assertEqual(len(deepseek_pro), 1)
        self.assertEqual(deepseek_pro[0]["status"], "not_launch_ready")
        self.assertFalse(deepseek_pro[0]["assigned_to_ministry"])

    def test_user_facing_doc_explains_no_fallback_ministry_routing(self):
        self.assertTrue(DOC_PATH.exists(), "model ministry routing doc is required")
        text = DOC_PATH.read_text(encoding="utf-8")
        self.assertIn("No fallback-by-default", text)
        self.assertIn("كل وزارة لها موديل محدد", text)
        self.assertIn("deepseek-ai/deepseek-v4-pro", text)
    def test_profile_config_declares_ministry_routing_not_fallback(self):
        text = CONFIG_PATH.read_text(encoding="utf-8")
        self.assertIn("digital_state:", text)
        self.assertIn("model_ministries:", text)
        self.assertIn("fallback_enabled: false", text)
        self.assertIn("strategy-ministry:", text)
        self.assertIn("operations-ministry:", text)
        self.assertNotIn("fallback_providers:", text)


if __name__ == "__main__":
    unittest.main()
