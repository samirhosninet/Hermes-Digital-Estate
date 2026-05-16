import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "governance" / "check_runtime_guard_schema.py"
FIXTURES = ROOT / "specs" / "002-runtime-governance-guards" / "fixtures"


def run_check(path):
    return subprocess.run([sys.executable, str(SCRIPT), str(path)], cwd=ROOT, text=True, capture_output=True)


class RuntimeGuardSchemaTests(unittest.TestCase):
    def test_valid_policy_fixture(self):
        result = run_check(FIXTURES / "valid-policy.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["kind"], "policy")

    def test_valid_decision_fixture(self):
        result = run_check(FIXTURES / "valid-decision.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["kind"], "decision")

    def test_valid_audit_fixture(self):
        result = run_check(FIXTURES / "valid-audit-record.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["kind"], "audit")

    def test_policy_missing_rules_fails_closed(self):
        result = run_check(FIXTURES / "invalid-policy-missing-rules.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required fields", result.stdout)

    def test_audit_summary_rejects_secret_like_material(self):
        with tempfile.TemporaryDirectory() as tmp:
            sample = Path(tmp) / "bad-audit.json"
            sample.write_text(json.dumps({
                "schema_version": "runtime-guard-audit-record-v1",
                "timestamp_utc": "2026-05-15T10:00:00Z",
                "boundary": "credentials",
                "risk_class": "R4",
                "decision": "deny",
                "actor": "assistant",
                "policy_version": "runtime-guard-policy-v1",
                "action_hash": "0123456789abcdef",
                "redacted_action_summary": "Bearer secret-token was used"
            }), encoding="utf-8")
            result = run_check(sample)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("secret material", result.stdout)
    def test_valid_dry_run_action_fixture(self):
        result = run_check(FIXTURES / "dry-run-terminal-read-only-action.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["kind"], "action")

    def test_valid_terminal_hook_contract_fixture(self):
        result = run_check(FIXTURES / "terminal-hook-dry-run-contract.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["kind"], "terminal_hook_contract")

    def test_valid_approval_flow_contract_fixture(self):
        result = run_check(FIXTURES / "approval-flow-interaction-contract.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["kind"], "approval_flow_contract")

    def test_valid_log_only_implementation_gate_fixture(self):
        result = run_check(FIXTURES / "log-only-implementation-gate.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["kind"], "log_only_implementation_gate")

    def test_valid_operator_approval_record_fixture(self):
        result = run_check(FIXTURES / "operator-approval-record.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["kind"], "operator_approval_record")


if __name__ == "__main__":
    unittest.main()
