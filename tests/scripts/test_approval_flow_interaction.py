import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
FEATURE = ROOT / "specs" / "002-runtime-governance-guards"
SCHEMA = FEATURE / "schemas" / "approval-flow-interaction-contract-v1.json"
FIXTURE = FEATURE / "fixtures" / "approval-flow-interaction-contract.json"
DOC = ROOT / "docs" / "governance" / "approval-flow-interaction.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class ApprovalFlowInteractionTests(unittest.TestCase):
    def test_approval_flow_contract_exists_and_preserves_existing_flow(self):
        schema = load_json(SCHEMA)
        contract = load_json(FIXTURE)

        self.assertEqual(schema["title"], "Approval Flow Interaction Contract v1")
        self.assertEqual(contract["schema_version"], "approval-flow-interaction-contract-v1")
        self.assertEqual(contract["mode"], "dry_run_log_only")
        self.assertIs(contract["runtime_enforcement_enabled"], False)
        self.assertIs(contract["duplicates_approval_prompt"], False)
        self.assertIs(contract["bypasses_existing_approval"], False)
        self.assertIs(contract["changes_terminal_execution_flow"], False)
        self.assertIs(contract["may_block_commands"], False)

    def test_contract_defines_required_interaction_events(self):
        contract = load_json(FIXTURE)
        events = contract["required_interaction_events"]

        self.assertEqual(events[0], "proposed_terminal_action")
        self.assertIn("governance_dry_run_decision", events)
        self.assertIn("existing_approval_flow_observed", events)
        self.assertIn("terminal_execution_continues_unchanged", events)
        self.assertIn("redacted_audit_record_written_or_buffered", events)

    def test_contract_requires_disable_and_failure_behavior(self):
        contract = load_json(FIXTURE)

        self.assertEqual(contract["disable_flag"], "governance.terminal_dry_run_enabled=false")
        self.assertEqual(contract["audit_failure_behavior"], "continue_terminal_flow_and_record_local_error")
        self.assertEqual(contract["approval_failure_behavior"], "defer_to_existing_approval_flow")

    def test_design_doc_states_no_duplicate_or_bypass(self):
        text = DOC.read_text(encoding="utf-8")

        self.assertIn("must not create a second approval prompt", text)
        self.assertIn("must not bypass the existing approval flow", text)
        self.assertIn("dry-run/log-only", text)
        self.assertIn("No runtime integration is active", text)


if __name__ == "__main__":
    unittest.main()
