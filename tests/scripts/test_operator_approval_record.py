import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FEATURE = ROOT / "specs" / "002-runtime-governance-guards"
FIXTURES = FEATURE / "fixtures"
SCHEMAS = FEATURE / "schemas"
DOC = ROOT / "docs" / "governance" / "operator-approval-record.md"


class OperatorApprovalRecordContractTests(unittest.TestCase):
    def test_operator_approval_record_contract_exists_and_blocks_runtime_without_scope(self):
        schema = SCHEMAS / "operator-approval-record-v1.json"
        fixture = FIXTURES / "operator-approval-record.json"

        self.assertTrue(schema.exists(), "operator approval schema is required before runtime touchpoints")
        self.assertTrue(fixture.exists(), "operator approval fixture is required before runtime touchpoints")
        self.assertTrue(DOC.exists(), "operator approval runbook is required before runtime touchpoints")

        data = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "operator-approval-record-v1")
        self.assertEqual(data["approval_status"], "not_granted")
        self.assertEqual(data["runtime_scope"], "none")
        self.assertFalse(data["runtime_touchpoint_allowed"])
        self.assertFalse(data["enforcement_allowed"])
        self.assertEqual(data["maximum_mode"], "log_only")
        self.assertIn("tools/terminal", data["explicitly_out_of_scope"])
        self.assertIn("tools/file", data["explicitly_out_of_scope"])
        self.assertIn("gateway", data["explicitly_out_of_scope"])
        self.assertIn("model_routing", data["explicitly_out_of_scope"])
        self.assertIn("rollback_plan", data)
        self.assertIn("required_validation", data)
        self.assertIn("operator_reapproval_required_for", data)

    def test_operator_approval_record_doc_states_no_current_runtime_approval(self):
        self.assertTrue(DOC.exists())
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("No runtime touchpoint is approved by this record", text)
        self.assertIn("explicit operator approval", text.lower())
        self.assertIn("log-only", text.lower())
        self.assertIn("rollback", text.lower())


if __name__ == "__main__":
    unittest.main()
