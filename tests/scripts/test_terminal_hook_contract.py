import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
FEATURE = ROOT / "specs" / "002-runtime-governance-guards"
SCHEMA = FEATURE / "schemas" / "terminal-hook-dry-run-contract-v1.json"
FIXTURE = FEATURE / "fixtures" / "terminal-hook-dry-run-contract.json"
DOC = ROOT / "docs" / "governance" / "terminal-hook-dry-run-design.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TerminalHookContractTests(unittest.TestCase):
    def test_terminal_hook_contract_exists_and_is_dry_run_only(self):
        schema = load_json(SCHEMA)
        contract = load_json(FIXTURE)

        self.assertEqual(schema["title"], "Terminal Hook Dry-Run Contract v1")
        self.assertEqual(contract["schema_version"], "terminal-hook-dry-run-contract-v1")
        self.assertEqual(contract["mode"], "dry_run_log_only")
        self.assertIs(contract["runtime_enforcement_enabled"], False)
        self.assertIs(contract["changes_terminal_execution_flow"], False)
        self.assertIs(contract["may_block_commands"], False)
        self.assertIs(contract["requires_existing_approval_flow"], True)
        self.assertEqual(contract["rollback"], "remove_hook_call_or_disable_config_flag")

    def test_terminal_hook_contract_lists_required_evidence_before_integration(self):
        contract = load_json(FIXTURE)
        required = set(contract["required_evidence_before_integration"])

        self.assertIn("unit_tests", required)
        self.assertIn("dry_run_audit_sample", required)
        self.assertIn("operator_approval_matrix", required)
        self.assertIn("portability_check", required)
        self.assertIn("secret_redaction_test", required)

    def test_terminal_hook_design_doc_states_no_current_runtime_hook(self):
        text = DOC.read_text(encoding="utf-8")

        self.assertIn("No current terminal runtime hook is active", text)
        self.assertIn("dry-run/log-only", text)
        self.assertIn("must not block, mutate, or reorder terminal execution", text)


if __name__ == "__main__":
    unittest.main()
