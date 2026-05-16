import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "governance" / "check_portability.py"


def run_portability(*paths):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, paths)], cwd=ROOT, text=True, capture_output=True)


class GovernancePortabilityTests(unittest.TestCase):
    def test_clean_governance_docs_and_skill_are_portable(self):
        result = run_portability(
            ROOT / "docs" / "governance",
            ROOT / "skills" / "devops" / "governance-status",
            ROOT / "specs" / "001-hyperagent-governance-integration" / "schemas",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIs(payload["portable"], True)
        self.assertEqual(payload["findings"], [])

    def test_detects_forbidden_absolute_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            sample = Path(tmp) / "bad.md"
            sample.write_text("required path: D:\\secret\n", encoding="utf-8")
            result = run_portability(sample)
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertIs(payload["portable"], False)
        self.assertEqual(payload["findings"][0]["pattern"], "windows_drive_path")

    def test_detects_external_concept_folder_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            sample = Path(tmp) / "bad.md"
            sample.write_text("runtime requires hermes_hyperagent", encoding="utf-8")
            result = run_portability(sample)
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["findings"][0]["pattern"], "external_concept_folder")

    def test_ignores_portability_scanner_tests_when_scanning_repo_artifacts(self):
        result = run_portability(ROOT / "tests" / "scripts")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIs(payload["portable"], True)
    def test_json_escaped_newline_after_colon_is_not_windows_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            sample = Path(tmp) / "preview.json"
            sample.write_text(json.dumps({"content_preview": "AI agent:\n- safe text"}), encoding="utf-8")
            result = run_portability(sample)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIs(payload["portable"], True)


if __name__ == "__main__":
    unittest.main()
