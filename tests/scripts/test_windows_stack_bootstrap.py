import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP = ROOT / "scripts/bootstrap/windows_bootstrap.ps1"
BOOTSTRAP_UI = ROOT / "scripts/bootstrap/bootstrap-ui.html"
REMOTE_INSTALLER = ROOT / "scripts/bootstrap/install-windows.ps1"


class WindowsStackBootstrapTests(unittest.TestCase):
    def test_bootstrap_files_are_distribution_artifacts(self):
        manifest = json.loads((ROOT / "digital-state.manifest.json").read_text(encoding="utf-8"))
        required = set(manifest["required_files"])
        allowed = set(manifest["allowed_roots"])

        self.assertIn("scripts/bootstrap/", allowed)
        self.assertIn("scripts/bootstrap/install-windows.ps1", required)
        self.assertIn("scripts/bootstrap/windows_bootstrap.ps1", required)
        self.assertIn("scripts/bootstrap/bootstrap-ui.html", required)

    def test_start_bat_delegates_to_powershell_bootstrap(self):
        text = (ROOT / "START.bat").read_text(encoding="utf-8")
        self.assertIn("scripts\\bootstrap\\windows_bootstrap.ps1", text)
        self.assertIn("powershell -NoProfile -ExecutionPolicy Bypass -File", text)
        self.assertIn("Keep this window open", text)

    def test_bootstrap_uses_fixed_install_commands(self):
        text = BOOTSTRAP.read_text(encoding="utf-8")
        self.assertIn("https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1", text)
        self.assertIn("https://github.com/outsourc-e/hermes-workspace.git", text)
        self.assertIn("github.com/samirhosninet/Hermes-Digital-Estate", text)
        self.assertIn('"profile", "install", $DigitalStateSource, "--alias", "-y"', text)
        self.assertIn("$HermesCmdPath", text)
        self.assertIn("Get-HermesCommand", text)

    def test_bootstrap_api_does_not_accept_client_commands(self):
        text = BOOTSTRAP.read_text(encoding="utf-8")
        self.assertNotIn("Request.InputStream", text)
        self.assertNotIn("Invoke-Expression $", text)
        self.assertIn("X-Bootstrap-Token", text)
        self.assertIn("invalid bootstrap nonce", text)
        self.assertIn('"/api/install/hermes"', text)
        self.assertIn('"/api/install/workspace"', text)
        self.assertIn('"/api/install/digital-state"', text)

    def test_bootstrap_ui_explains_stack_and_fallbacks(self):
        html = BOOTSTRAP_UI.read_text(encoding="utf-8")
        self.assertIn("Install Digital State Stack", html)
        self.assertIn("__BOOTSTRAP_NONCE__", html)
        self.assertIn("X-Bootstrap-Token", html)
        self.assertIn("Hermes Agent", html)
        self.assertIn("Hermes Workspace", html)
        self.assertIn("Digital State Profile", html)
        self.assertIn("Full log:", html)
        self.assertIn("Manual command", html)

    def test_remote_installer_downloads_zip_and_launches_start_bat(self):
        text = REMOTE_INSTALLER.read_text(encoding="utf-8")
        self.assertIn("Hermes-Digital-Estate/archive/refs/heads/$Ref.zip", text)
        self.assertIn("$env:LOCALAPPDATA", text)
        self.assertIn("HermesDigitalState\\bootstrap", text)
        self.assertIn("Invoke-WebRequest", text)
        self.assertIn("Expand-Archive", text)
        self.assertIn('Filter "START.bat"', text)
        self.assertIn("Start-Process", text)
        self.assertNotIn("git clone", text)

    def test_bootstrap_treats_hermes_as_source_of_windows_tools(self):
        text = BOOTSTRAP.read_text(encoding="utf-8")
        self.assertIn("Hermes Agent is the first required component", text)
        self.assertIn("official Hermes installer normally provisions PortableGit", text)
        self.assertIn("official Hermes installer normally provisions it", text)
        self.assertIn("Install Hermes Agent first", text)


if __name__ == "__main__":
    unittest.main()
