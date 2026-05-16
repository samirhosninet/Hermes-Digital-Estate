import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "governance" / "read_governance_status.py"
FIXTURES = ROOT / "tests" / "fixtures" / "governance"


def run_status(path):
    return subprocess.run([sys.executable, str(SCRIPT), str(path)], cwd=ROOT, text=True, capture_output=True)


class GovernanceStatusTests(unittest.TestCase):
    def test_valid_status_outputs_stable_summary(self):
        result = run_status(FIXTURES / "valid-status.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIs(payload["ok"], True)
        self.assertEqual(payload["schema_version"], "governance-status-v1")
        self.assertIs(payload["portable"], True)
        self.assertGreaterEqual(payload["model_council"]["returned_count"], 3)
        self.assertIs(payload["model_council"]["quorum_met"], True)

    def test_missing_required_field_fails_closed(self):
        result = run_status(FIXTURES / "invalid-status-missing-field.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required fields", result.stderr)

    def test_malformed_json_fails_closed(self):
        result = run_status(FIXTURES / "malformed.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("malformed JSON", result.stderr)

    def test_missing_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_status(Path(tmp) / "missing.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("file not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
