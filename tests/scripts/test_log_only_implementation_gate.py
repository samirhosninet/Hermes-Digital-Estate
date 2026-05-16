import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
FEATURE = ROOT / "specs" / "002-runtime-governance-guards"
SCHEMA = FEATURE / "schemas" / "log-only-implementation-gate-v1.json"
FIXTURE = FEATURE / "fixtures" / "log-only-implementation-gate.json"
DOC = ROOT / "docs" / "governance" / "log-only-implementation-gate.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class LogOnlyImplementationGateTests(unittest.TestCase):
    def test_gate_contract_exists_and_blocks_enforcement_by_default(self):
        schema = load_json(SCHEMA)
        contract = load_json(FIXTURE)

        self.assertEqual(schema["title"], "Log-Only Implementation Gate v1")
        self.assertEqual(contract["schema_version"], "log-only-implementation-gate-v1")
        self.assertEqual(contract["mode"], "log_only")
        self.assertIs(contract["runtime_enforcement_enabled"], False)
        self.assertIs(contract["may_block_commands"], False)
        self.assertIs(contract["changes_terminal_execution_flow"], False)
        self.assertEqual(contract["default_failure_behavior"], "continue_without_governance_block")

    def test_gate_requires_explicit_evidence_before_runtime_touchpoint(self):
        contract = load_json(FIXTURE)
        required = set(contract["required_evidence_before_runtime_touchpoint"])

        self.assertIn("explicit_operator_approval", required)
        self.assertIn("terminal_hook_contract_passed", required)
        self.assertIn("approval_flow_contract_passed", required)
        self.assertIn("unit_tests_passed", required)
        self.assertIn("portability_check_passed", required)
        self.assertIn("rollback_plan_documented", required)

    def test_gate_defines_safe_runtime_touchpoint_constraints(self):
        contract = load_json(FIXTURE)
        constraints = contract["runtime_touchpoint_constraints"]

        self.assertIn("one_small_hook_only", constraints)
        self.assertIn("no_command_mutation", constraints)
        self.assertIn("no_additional_approval_prompt", constraints)
        self.assertIn("audit_write_failure_non_blocking", constraints)
        self.assertIn("feature_flag_disable_path", constraints)

    def test_doc_states_gate_is_not_runtime_enforcement(self):
        text = DOC.read_text(encoding="utf-8")

        self.assertIn("This is not runtime enforcement", text)
        self.assertIn("log-only", text)
        self.assertIn("must not block terminal execution", text)
        self.assertIn("explicit operator approval", text)


if __name__ == "__main__":
    unittest.main()
