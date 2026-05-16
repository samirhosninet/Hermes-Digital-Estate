import json
import tempfile
import unittest
from pathlib import Path

from agent.runtime_governance import RuntimeGovernanceGuard, build_terminal_dry_run_action


VALID_POLICY = {
    "schema_version": "runtime-guard-policy-v1",
    "policy_id": "test-policy-1",
    "mode": "dry_run",
    "portable": True,
    "default_decision": "escalate",
    "rules": [
        {
            "id": "allow-read-only-terminal",
            "boundary": "terminal",
            "risk_class": "R1",
            "decision": "allow",
            "match": {"command_class": "read_only"},
            "reason": "Read-only terminal inspection is allowed.",
        },
        {
            "id": "escalate-package-mutation",
            "boundary": "package",
            "risk_class": "R3",
            "decision": "escalate",
            "match": {"changes_lockfile": True},
            "reason": "Dependency or lockfile changes require approval.",
        },
        {
            "id": "deny-credential-exfiltration",
            "boundary": "credentials",
            "risk_class": "R4",
            "decision": "deny",
            "match": {"secret_path": True},
            "reason": "Credential paths are forbidden.",
        },
    ],
}


class RuntimeGovernanceGuardTests(unittest.TestCase):
    def write_policy(self, directory: Path, content=VALID_POLICY) -> Path:
        path = directory / "policy.json"
        path.write_text(json.dumps(content), encoding="utf-8")
        return path

    def test_missing_policy_in_strict_mode_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing-policy.json"

            guard = RuntimeGovernanceGuard.from_policy_file(missing, strict=True)
            decision = guard.evaluate({"boundary": "terminal", "command": "pwd", "read_only": True})

            self.assertEqual(decision.decision, "fail_closed")
            self.assertEqual(decision.reason, "policy_missing")
            self.assertFalse(decision.policy_loaded)

    def test_malformed_policy_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.json"
            path.write_text("{not json", encoding="utf-8")

            guard = RuntimeGovernanceGuard.from_policy_file(path, strict=True)
            decision = guard.evaluate({"boundary": "terminal", "command": "pwd", "read_only": True})

            self.assertEqual(decision.decision, "fail_closed")
            self.assertEqual(decision.reason, "policy_malformed")
            self.assertFalse(decision.policy_loaded)

    def test_safe_read_only_terminal_action_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = self.write_policy(Path(tmp))

            guard = RuntimeGovernanceGuard.from_policy_file(policy, strict=True)
            decision = guard.evaluate({"boundary": "terminal", "command": "pwd", "read_only": True})

            self.assertEqual(decision.decision, "allow")
            self.assertEqual(decision.reason, "read_only_allowed")
            self.assertEqual(decision.risk_class, "R1")

    def test_package_mutation_escalates(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = self.write_policy(Path(tmp))

            guard = RuntimeGovernanceGuard.from_policy_file(policy, strict=True)
            decision = guard.evaluate({"boundary": "package", "command": "pip install requests"})

            self.assertEqual(decision.decision, "escalate")
            self.assertEqual(decision.reason, "boundary_requires_approval")
            self.assertEqual(decision.risk_class, "R3")

    def test_credential_path_access_is_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = self.write_policy(Path(tmp))

            guard = RuntimeGovernanceGuard.from_policy_file(policy, strict=True)
            decision = guard.evaluate({"boundary": "file", "path": "~/.hermes/.env", "operation": "read"})

            self.assertEqual(decision.decision, "deny")
            self.assertEqual(decision.reason, "secret_path")
            self.assertEqual(decision.risk_class, "R4")

    def test_audit_record_redacts_secret_bearing_action_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            policy = self.write_policy(Path(tmp))

            guard = RuntimeGovernanceGuard.from_policy_file(policy, strict=True)
            decision = guard.evaluate(
                {
                    "boundary": "terminal",
                    "command": "curl -H 'Authorization: Bearer sk-secret-token' https://example.com",
                }
            )
            audit = guard.build_audit_record(decision)

            encoded = json.dumps(audit, sort_keys=True)
            self.assertNotIn("sk-secret-token", encoded)
            self.assertIn("action_hash", audit)
            self.assertEqual(audit["decision"], decision.decision)
            self.assertEqual(audit["schema_version"], "runtime-guard-audit-record-v1")
            self.assertIn("redacted_action_summary", audit)
    def test_terminal_dry_run_action_classifies_without_execution(self):
        safe = build_terminal_dry_run_action("pwd")
        self.assertEqual(safe["boundary"], "terminal")
        self.assertEqual(safe["command"], "pwd")
        self.assertTrue(safe["read_only"])
        self.assertEqual(safe["command_class"], "read_only")

        package = build_terminal_dry_run_action("pip install requests")
        self.assertEqual(package["boundary"], "package")
        self.assertFalse(package["read_only"])
        self.assertEqual(package["command_class"], "package_mutation")

        destructive_git = build_terminal_dry_run_action("git reset --hard HEAD~1")
        self.assertEqual(destructive_git["boundary"], "git_destructive")
        self.assertFalse(destructive_git["read_only"])
        self.assertEqual(destructive_git["command_class"], "git_destructive")


if __name__ == "__main__":
    unittest.main()
