import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "governance" / "check_runtime_guard_schema.py"
SCENARIOS = ROOT / "specs" / "002-runtime-governance-guards" / "fixtures" / "scenarios"


class RuntimeGuardScenarioFixtureTests(unittest.TestCase):
    def run_checker(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_safe_read_terminal_scenario_is_allow_decision(self):
        path = SCENARIOS / "dry-run-safe-read-allow.json"
        data = json.loads(path.read_text(encoding="utf-8"))

        result = self.run_checker(path)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["schema_version"], "runtime-guard-decision-v1")
        self.assertEqual(data["decision"], "allow")
        self.assertEqual(data["boundary"], "terminal")
        self.assertEqual(data["risk_class"], "R0")

    def test_package_mutation_scenario_escalates(self):
        path = SCENARIOS / "dry-run-package-escalate.json"
        data = json.loads(path.read_text(encoding="utf-8"))

        result = self.run_checker(path)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["schema_version"], "runtime-guard-decision-v1")
        self.assertEqual(data["decision"], "escalate")
        self.assertEqual(data["boundary"], "package")
        self.assertEqual(data["risk_class"], "R3")

    def test_secret_path_scenario_is_deny_decision(self):
        path = SCENARIOS / "dry-run-secret-path-deny.json"
        data = json.loads(path.read_text(encoding="utf-8"))

        result = self.run_checker(path)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["schema_version"], "runtime-guard-decision-v1")
        self.assertEqual(data["decision"], "deny")
        self.assertEqual(data["boundary"], "credentials")
        self.assertEqual(data["risk_class"], "R4")

    def test_missing_policy_scenario_fails_closed(self):
        path = SCENARIOS / "dry-run-policy-missing-fail-closed.json"
        data = json.loads(path.read_text(encoding="utf-8"))

        result = self.run_checker(path)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(data["schema_version"], "runtime-guard-decision-v1")
        self.assertEqual(data["decision"], "fail_closed")
        self.assertEqual(data["risk_class"], "R5")


if __name__ == "__main__":
    unittest.main()
