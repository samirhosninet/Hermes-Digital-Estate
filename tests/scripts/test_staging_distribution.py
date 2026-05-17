import json
import tempfile
import unittest
from pathlib import Path

from scripts.governance import build_staging_distribution as staging


class TestStagingDistribution(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]

    def test_build_staging_copies_manifest_allowed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "digital-state-staging"
            result = staging.build_staging(self.root, output)

            self.assertTrue(result["ok"], result["findings"])
            self.assertGreater(result["copied_count"], 0)
            for rel_path in (
                "distribution.yaml",
                "digital-state.manifest.json",
                "wizard.py",
                "preflight/server.py",
                "docs/governance/start-here.md",
                "docs/governance/digital-state-runbook-ar.md",
                "specs/003-portable-digital-state-distribution/spec.md",
                "specs/004-setup-wizard-hardening/spec.md",
                "scripts/governance/bootstrap_digital_state.py",
                "scripts/governance/build_staging_distribution.py",
            ):
                self.assertTrue((output / rel_path).exists(), rel_path)

    def test_build_staging_rejects_output_inside_source_repo(self):
        result = staging.build_staging(self.root, self.root / "tmp-staging-output")
        codes = {item["code"] for item in result["findings"]}
        self.assertFalse(result["ok"])
        self.assertIn("output_inside_source", codes)

    def test_build_staging_rejects_forbidden_output_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = staging.build_staging(self.root, Path(tmp) / "logs" / "staging")
        codes = {item["code"] for item in result["findings"]}
        self.assertFalse(result["ok"])
        self.assertIn("output_forbidden_path", codes)

    def test_build_staging_does_not_copy_local_env_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            output = Path(tmp) / "digital-state-staging"
            source.mkdir()
            manifest = {
                "allowed_roots": ["distribution.yaml"],
                "forbidden_paths": [".env", ".git/", "logs/", "sessions/", "memory/"],
            }
            (source / "digital-state.manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (source / "distribution.yaml").write_text("name: digital-state\n", encoding="utf-8")
            env_line = "NVIDIA_API_KEY" + "=local-test-value\n"
            (source / ".env").write_text(env_line, encoding="utf-8")

            result = staging.build_staging(source, output)
            self.assertTrue(result["ok"], result["findings"])
            self.assertFalse((output / ".env").exists())
            report_text = json.dumps(result)
            self.assertNotIn("local-test-value", report_text)


if __name__ == "__main__":
    unittest.main()
