import json
import tempfile
import unittest
from pathlib import Path

from scripts.governance import bootstrap_digital_state as bootstrap


class TestDigitalStateDistribution(unittest.TestCase):
    def test_current_workspace_distribution_is_valid(self):
        result = bootstrap.run(Path(__file__).resolve().parents[2])
        self.assertTrue(result["ok"], result["findings"])

    def test_manifest_rejects_missing_required_field(self):
        manifest = {
            "schema_version": "digital-state-manifest-v1",
            "name": "digital-state",
        }
        findings = bootstrap.validate_manifest(manifest, root=Path.cwd())
        codes = {item["code"] for item in findings}
        self.assertIn("manifest_missing_key", codes)

    def test_manifest_rejects_absolute_and_windows_paths(self):
        manifest = self._valid_manifest()
        manifest["allowed_roots"] = ["docs/governance/", "/mock/user/example", "X:/secret"]
        findings = bootstrap.validate_manifest(manifest, root=Path.cwd())
        details = [item["detail"] for item in findings]
        self.assertTrue(any("/mock/user/example" in detail for detail in details))
        self.assertTrue(any("X:/secret" in detail for detail in details))

    def test_distribution_rejects_real_env_file_as_owned_path(self):
        manifest = self._valid_manifest()
        distribution = self._valid_distribution()
        distribution["distribution_owned"].append(".env")
        findings = bootstrap.validate_distribution(distribution, manifest)
        codes = {item["code"] for item in findings}
        self.assertIn("distribution_forbidden_owned_path", codes)

    def test_secret_like_content_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/governance").mkdir(parents=True)
            (root / "docs/governance/bad.md").write_text("api_key = 'sk-1234567890abcdef'", encoding="utf-8")
            manifest = self._valid_manifest()
            manifest["allowed_roots"] = ["docs/governance/"]
            findings = bootstrap.scan_portable_files(root, manifest)
            codes = {item["code"] for item in findings}
            self.assertIn("secret_like_content", codes)

    def test_distribution_yaml_parser_handles_env_requires(self):
        distribution = bootstrap._simple_yaml_load(Path(__file__).resolve().parents[2] / "distribution.yaml")
        self.assertEqual(distribution["name"], "digital-state")
        self.assertIsInstance(distribution["env_requires"], list)
        self.assertEqual(distribution["env_requires"][0]["name"], "NVIDIA_API_KEY")
        self.assertFalse(distribution["env_requires"][0]["required"])

    def test_non_technical_user_docs_are_required_distribution_files(self):
        manifest = json.loads((Path(__file__).resolve().parents[2] / "digital-state.manifest.json").read_text(encoding="utf-8"))
        required = set(manifest["required_files"])
        self.assertIn("config.yaml", required)
        self.assertIn("scripts/governance/bootstrap_digital_state.py", required)
        self.assertIn("docs/governance/start-here.md", required)
        self.assertIn("docs/governance/user-quickstart.md", required)
        for rel_path in ("docs/governance/start-here.md", "docs/governance/user-quickstart.md"):
            text = (Path(__file__).resolve().parents[2] / rel_path).read_text(encoding="utf-8")
            self.assertIn("hermes profile install", text)
            self.assertIn("hermes -p digital-state chat", text)

    def test_update_safety_docs_are_required_distribution_files(self):
        root = Path(__file__).resolve().parents[2]
        manifest = json.loads((root / "digital-state.manifest.json").read_text(encoding="utf-8"))
        required = set(manifest["required_files"])
        self.assertIn("docs/governance/update-and-recovery.md", required)
        self.assertIn("docs/governance/github-distribution-maintenance.md", required)
        self.assertIn("docs/governance/e2e-fullstack-release.md", required)
        update_text = (root / "docs/governance/update-and-recovery.md").read_text(encoding="utf-8")
        maintenance_text = (root / "docs/governance/github-distribution-maintenance.md").read_text(encoding="utf-8")
        e2e_text = (root / "docs/governance/e2e-fullstack-release.md").read_text(encoding="utf-8")
        self.assertIn("hermes profile update digital-state", update_text)
        self.assertIn("not a fork", update_text)
        self.assertIn("Hermes core", maintenance_text)
        self.assertIn("CI", maintenance_text)
        self.assertIn("hermes profile install", e2e_text)
        self.assertIn("digital-state-test", e2e_text)
        self.assertIn("GitHub", e2e_text)

    def test_update_safety_contract_keeps_digital_state_out_of_hermes_core(self):
        root = Path(__file__).resolve().parents[2]
        contract = json.loads((root / "specs/003-portable-digital-state-distribution/fixtures/update-safety-contract.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["schema_version"], "update-safety-contract-v1")
        self.assertEqual(contract["architecture"], "profile_distribution_not_core_fork")
        self.assertFalse(contract["hermes_core_policy"]["digital_state_may_modify_core"])
        self.assertFalse(contract["hermes_core_policy"]["runtime_changes_allowed_in_feature_003"])
        self.assertEqual(contract["digital_state_update_policy"]["primary_update_command"], "hermes profile update digital-state")
        self.assertIn("Hermes core runtime modifications", contract["forbidden_update_contents"])

    def test_setup_wizard_files_are_declared_distribution_artifacts(self):
        root = Path(__file__).resolve().parents[2]
        manifest = json.loads((root / "digital-state.manifest.json").read_text(encoding="utf-8"))
        distribution = bootstrap._simple_yaml_load(root / "distribution.yaml")
        required = set(manifest["required_files"])
        allowed = set(manifest["allowed_roots"])
        owned = set(distribution["distribution_owned"])

        for path in ("START.bat", "START.sh", "wizard.py", "preflight/"):
            self.assertIn(path, allowed)
            self.assertIn(path, owned)
        self.assertIn("preflight/server.py", required)
        self.assertIn("preflight/checks.py", required)
        self.assertIn("preflight/static/index.html", required)
        self.assertIn("specs/004-setup-wizard-hardening/spec.md", required)

    def _valid_manifest(self):
        return {
            "schema_version": "digital-state-manifest-v1",
            "name": "digital-state",
            "version": "0.1.0",
            "distribution": {
                "type": "hermes_profile_distribution",
                "install_command": "hermes profile install github.com/YOUR-ORG/hermes-digital-state --alias digital-state",
                "update_command": "hermes profile update digital-state",
                "run_command": "hermes -p digital-state chat",
            },
            "compatible_hermes": ">=0.12.0",
            "allowed_roots": ["docs/governance/"],
            "forbidden_paths": [".env"],
            "required_files": [],
            "required_checks": [],
            "supported_modes": ["personal"],
            "local_credentials": ["NVIDIA_API_KEY"],
            "secrets_policy": {
                "ships_secrets": False,
                "ships_oauth_tokens": False,
                "ships_sessions": False,
                "ships_logs": False,
                "ships_memories": False,
            },
            "update_policy": {},
        }

    def _valid_distribution(self):
        return {
            "name": "digital-state",
            "version": "0.1.0",
            "description": "Portable Digital State",
            "hermes_requires": ">=0.12.0",
            "env_requires": [
                {"name": "NVIDIA_API_KEY", "description": "optional", "required": False}
            ],
            "distribution_owned": ["SOUL.md", "docs/governance/"],
        }


if __name__ == "__main__":
    unittest.main()
