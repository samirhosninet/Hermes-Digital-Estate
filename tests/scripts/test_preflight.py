#!/usr/bin/env python3
"""Tests for the preflight check engine."""
from __future__ import annotations

import json
import socket
import sys
import tempfile
import threading
import unittest
from http.client import HTTPConnection
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from preflight.checks import (
    check_system,
    check_hermes,
    check_governance,
    check_credentials,
    check_network,
    check_audit,
    check_consistency,
    run_all,
)
from preflight import server as wizard_server


class PreflightCheckShapeTests(unittest.TestCase):
    """Verify every check function returns well-formed dicts."""

    REQUIRED_KEYS = {"status", "label", "detail"}
    VALID_STATUSES = {"pass", "warn", "fail"}

    def _assert_valid(self, results: list[dict]):
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0, "check returned empty list")
        for item in results:
            self.assertIsInstance(item, dict)
            self.assertTrue(
                self.REQUIRED_KEYS.issubset(item.keys()),
                f"Missing keys in {item}",
            )
            self.assertIn(item["status"], self.VALID_STATUSES)

    def test_check_system_returns_valid_shape(self):
        self._assert_valid(check_system())

    def test_check_governance_returns_valid_shape(self):
        self._assert_valid(check_governance())

    def test_check_credentials_returns_valid_shape(self):
        self._assert_valid(check_credentials())

    def test_check_network_offline_returns_valid_shape(self):
        self._assert_valid(check_network(offline=True))

    def test_check_consistency_returns_valid_shape(self):
        self._assert_valid(check_consistency())


class PreflightAggregateTests(unittest.TestCase):
    """Verify the aggregate runner."""

    def test_run_all_offline_returns_summary(self):
        report = run_all(offline=True)
        self.assertIn("layers", report)
        self.assertIn("summary", report)
        summary = report["summary"]
        for key in ("pass", "warn", "fail", "total", "ready"):
            self.assertIn(key, summary)
        self.assertIsInstance(summary["ready"], bool)
        self.assertEqual(
            summary["total"],
            summary["pass"] + summary["warn"] + summary["fail"],
        )

    def test_run_all_layers_have_names(self):
        report = run_all(offline=True)
        for layer in report["layers"]:
            self.assertIn("name", layer)
            self.assertIn("checks", layer)
            self.assertIsInstance(layer["checks"], list)


class PreflightSecurityTests(unittest.TestCase):
    """Verify no secrets leak through check outputs."""

    def test_credential_check_never_reveals_key_values(self):
        results = check_credentials()
        for item in results:
            detail = item.get("detail", "")
            # Should never contain actual key material
            self.assertNotRegex(
                detail,
                r"[A-Za-z0-9_\-]{20,}",
                f"Potential secret leak in: {item['label']}",
            )

    def test_audit_output_never_contains_env_values(self):
        # run_all should not contain raw .env values
        report = run_all(offline=True)
        report_json = json.dumps(report)
        # Ensure no common API key patterns appear
        import re
        self.assertIsNone(
            re.search(r"sk-[A-Za-z0-9]{20,}", report_json),
            "API key pattern found in report",
        )


class WizardServerHardeningTests(unittest.TestCase):
    """Verify setup wizard server hardening behavior."""

    def _free_port(self) -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return int(s.getsockname()[1])

    def _start_server(self):
        httpd = wizard_server.LocalThreadingHTTPServer(
            ("127.0.0.1", 0),
            wizard_server.WizardHandler,
        )
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        return httpd, int(httpd.server_address[1])

    def _request(self, port: int, method: str, path: str, body: bytes | None = None, headers: dict | None = None):
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            response = conn.getresponse()
            data = response.read()
            return response.status, data
        finally:
            conn.close()

    def test_bind_server_uses_requested_port_when_available(self):
        port = self._free_port()
        httpd, actual = wizard_server._bind_server(port, attempts=1)
        try:
            self.assertEqual(actual, port)
        finally:
            httpd.server_close()

    def test_bind_server_moves_to_next_port_when_busy(self):
        first = self._free_port()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as blocker:
            blocker.bind(("127.0.0.1", first))
            blocker.listen(1)
            httpd, actual = wizard_server._bind_server(first, attempts=3)
            try:
                self.assertGreater(actual, first)
            finally:
                httpd.server_close()

    def test_bind_server_fails_when_range_is_exhausted(self):
        first = self._free_port()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as blocker:
            blocker.bind(("127.0.0.1", first))
            blocker.listen(1)
            with self.assertRaises(RuntimeError):
                wizard_server._bind_server(first, attempts=1)

    def test_info_endpoint_accepts_local_host(self):
        httpd, port = self._start_server()
        try:
            status, data = self._request(port, "GET", "/api/info")
            self.assertEqual(status, 200)
            self.assertIn(b"version", data)
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_info_endpoint_rejects_non_local_host(self):
        httpd, port = self._start_server()
        try:
            status, _ = self._request(port, "GET", "/api/info", headers={"Host": "example.com"})
            self.assertEqual(status, 403)
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_concurrent_info_requests_succeed(self):
        httpd, port = self._start_server()
        statuses: list[int] = []

        def call_info():
            status, _ = self._request(port, "GET", "/api/info")
            statuses.append(status)

        threads = [threading.Thread(target=call_info) for _ in range(8)]
        try:
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=5)
            self.assertEqual(statuses, [200] * 8)
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_save_credentials_rejects_bad_csrf_and_large_payload(self):
        httpd, port = self._start_server()
        try:
            bad = json.dumps({"csrf": "bad", "credentials": {}}).encode("utf-8")
            status, _ = self._request(port, "POST", "/api/save/credentials", bad, {"Content-Type": "application/json"})
            self.assertEqual(status, 403)

            large = b"x" * 4097
            status, _ = self._request(port, "POST", "/api/save/credentials", large, {"Content-Type": "application/json"})
            self.assertEqual(status, 413)
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_save_credentials_merges_and_writes_atomically(self):
        old_root = wizard_server.REPO_ROOT
        with tempfile.TemporaryDirectory() as tmp:
            wizard_server.REPO_ROOT = Path(tmp)
            httpd, port = self._start_server()
            try:
                body = json.dumps({
                    "csrf": wizard_server.CSRF_TOKEN,
                    "credentials": {
                        "NVIDIA_API_KEY": "unit-test-provider-key",
                        "OPENROUTER_API_KEY": "",
                    },
                }).encode("utf-8")
                status, data = self._request(port, "POST", "/api/save/credentials", body, {"Content-Type": "application/json"})
                self.assertEqual(status, 200)
                self.assertNotIn(str(tmp).encode("utf-8"), data)

                body = json.dumps({
                    "csrf": wizard_server.CSRF_TOKEN,
                    "credentials": {
                        "NVIDIA_API_KEY": "",
                        "ANTHROPIC_API_KEY": "unit-test-anthropic-key",
                    },
                }).encode("utf-8")
                status, _ = self._request(port, "POST", "/api/save/credentials", body, {"Content-Type": "application/json"})
                self.assertEqual(status, 200)

                env_text = (Path(tmp) / ".env").read_text("utf-8")
                self.assertIn("NVIDIA_API_KEY=unit-test-provider-key", env_text)
                self.assertIn("ANTHROPIC_API_KEY=unit-test-anthropic-key", env_text)
                self.assertFalse(list(Path(tmp).glob(".env.*.tmp")))
            finally:
                httpd.shutdown()
                httpd.server_close()
                wizard_server.REPO_ROOT = old_root

    def test_launch_rejects_bad_csrf(self):
        httpd, port = self._start_server()
        try:
            bad = json.dumps({"csrf": "bad"}).encode("utf-8")
            status, _ = self._request(port, "POST", "/api/launch", bad, {"Content-Type": "application/json"})
            self.assertEqual(status, 403)
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_launch_rejects_non_local_host(self):
        httpd, port = self._start_server()
        try:
            body = json.dumps({"csrf": wizard_server.CSRF_TOKEN}).encode("utf-8")
            status, _ = self._request(
                port,
                "POST",
                "/api/launch",
                body,
                {"Content-Type": "application/json", "Host": "example.com"},
            )
            self.assertEqual(status, 403)
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_launch_endpoint_ignores_client_command(self):
        httpd, port = self._start_server()
        try:
            with mock.patch.object(wizard_server, "_launch_terminal", return_value={"ok": True, "command": "hermes -p digital-state chat"}) as launch:
                body = json.dumps({
                    "csrf": wizard_server.CSRF_TOKEN,
                    "command": "calc.exe",
                }).encode("utf-8")
                status, data = self._request(port, "POST", "/api/launch", body, {"Content-Type": "application/json"})
            self.assertEqual(status, 200)
            launch.assert_called_once_with()
            response = json.loads(data)
            self.assertEqual(response["command"], "hermes -p digital-state chat")
            self.assertNotIn("calc", data.decode("utf-8"))
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_launch_terminal_uses_fixed_windows_command_without_shell(self):
        with mock.patch.object(wizard_server.platform, "system", return_value="Windows"), \
             mock.patch.object(wizard_server.subprocess, "Popen") as popen:
            result = wizard_server._launch_terminal()
        self.assertTrue(result["ok"])
        args, kwargs = popen.call_args
        self.assertEqual(args[0], ["cmd.exe", "/k", "hermes", "-p", "digital-state", "chat"])
        self.assertNotIn("shell", kwargs)

    def test_launch_terminal_reports_clear_fallback_when_no_terminal(self):
        with mock.patch.object(wizard_server.platform, "system", return_value="Linux"), \
             mock.patch.object(wizard_server.shutil, "which", return_value=None), \
             mock.patch.object(wizard_server.subprocess, "Popen") as popen:
            result = wizard_server._launch_terminal()
        self.assertFalse(result["ok"])
        self.assertEqual(result["command"], "hermes -p digital-state chat")
        self.assertIn("message", result)
        popen.assert_not_called()

    def test_wizard_ui_contains_launch_button_and_fallback_command(self):
        html = (REPO_ROOT / "preflight/static/index.html").read_text("utf-8")
        self.assertIn("/api/launch", html)
        self.assertIn("Launch Digital State", html)
        self.assertIn("hermes -p digital-state chat", html)
        self.assertIn("launchFailed", html)


if __name__ == "__main__":
    unittest.main()
