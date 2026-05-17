#!/usr/bin/env python3
"""Local HTTP server for the Hermes Digital State Setup Wizard.

Serves static UI and JSON API endpoints.
Binds to 127.0.0.1 ONLY — no external access.
Includes CSRF token protection on mutating endpoints.
"""
from __future__ import annotations

import json
import os
import platform
import secrets
import sys
import tempfile
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

STATIC_DIR = Path(__file__).resolve().parent / "static"
REPO_ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT_SEARCH_LIMIT = 50
ALLOWED_HOSTS = {"127.0.0.1", "localhost"}

# CSRF token — generated per server session
CSRF_TOKEN = secrets.token_hex(32)

# Idle auto-shutdown timer (30 min)
IDLE_TIMEOUT = 1800
_last_activity = time.monotonic()
_lock = threading.Lock()
_env_lock = threading.Lock()


def _touch_activity():
    global _last_activity
    with _lock:
        _last_activity = time.monotonic()


def _idle_watchdog(server: HTTPServer):
    while True:
        time.sleep(60)
        with _lock:
            elapsed = time.monotonic() - _last_activity
        if elapsed >= IDLE_TIMEOUT:
            print("\n[wizard] Idle timeout — shutting down.")
            server.shutdown()
            break


class LocalThreadingHTTPServer(ThreadingHTTPServer):
    """Threaded localhost server with daemon request workers."""

    daemon_threads = True
    allow_reuse_address = True


class WizardHandler(SimpleHTTPRequestHandler):
    """Routes /api/* to check logic, everything else to static files."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    # ---------- suppress default logging clutter ----------
    def log_message(self, format, *args):
        first = str(args[0]) if args else ""
        if "/api/" in first:
            super().log_message(format, *args)

    # ---------- CORS (only 127.0.0.1) ----------
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    # ---------- Routes ----------
    def do_GET(self):
        if not self._host_allowed():
            return self._json({"error": "forbidden host"}, 403)
        _touch_activity()
        path = self.path.split("?")[0]

        if path == "/api/csrf":
            return self._json({"token": CSRF_TOKEN})
        if path == "/api/check/system":
            return self._run_check("check_system")
        if path == "/api/check/hermes":
            return self._run_check("check_hermes")
        if path == "/api/check/governance":
            return self._run_check("check_governance")
        if path == "/api/check/credentials":
            return self._run_check("check_credentials")
        if path == "/api/check/network":
            offline = "offline=true" in self.path
            return self._run_check("check_network", offline=offline)
        if path == "/api/check/audit":
            return self._run_check("check_audit")
        if path == "/api/check/consistency":
            return self._run_check("check_consistency")
        if path == "/api/check/all":
            return self._run_all()
        if path == "/api/info":
            return self._json(self._info())

        # Static file serving
        if path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        if not self._host_allowed():
            return self._json({"error": "forbidden host"}, 403)
        _touch_activity()
        path = self.path.split("?")[0]

        if path == "/api/save/credentials":
            return self._save_credentials()
        self.send_error(404)

    def _host_allowed(self) -> bool:
        host = self.headers.get("Host", "")
        if not host:
            return True
        host = host.strip().lower()
        if host.startswith("["):
            return False
        host_name = host.rsplit(":", 1)[0] if ":" in host else host
        return host_name in ALLOWED_HOSTS

    # ---------- Check runner ----------
    def _run_check(self, func_name: str, **kwargs):
        from preflight import checks
        fn = getattr(checks, func_name, None)
        if not fn:
            return self._json({"error": f"unknown check: {func_name}"}, 404)
        try:
            items = fn(**kwargs)
            return self._json({"checks": items})
        except Exception as e:
            return self._json({"error": str(e)}, 500)

    def _run_all(self):
        from preflight import checks
        offline = "offline=true" in self.path
        try:
            report = checks.run_all(offline=offline)
            return self._json(report)
        except Exception as e:
            return self._json({"error": str(e)}, 500)

    # ---------- Info ----------
    def _info(self) -> dict:
        manifest_path = REPO_ROOT / "digital-state.manifest.json"
        manifest: dict[str, Any] = {}
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text("utf-8"))
            except Exception:
                pass
        return {
            "version": manifest.get("version", "unknown"),
            "name": manifest.get("name", "digital-state"),
            "modes": manifest.get("supported_modes", []),
            "credentials": manifest.get("local_credentials", []),
            "os": platform.system(),
            "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        }

    # ---------- Save credentials ----------
    def _save_credentials(self):
        # CSRF check
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len > 4096:
            self.rfile.read(min(content_len, 8192))
            return self._json({"error": "payload too large"}, 413)
        body = self.rfile.read(content_len)
        try:
            data = json.loads(body)
        except Exception:
            return self._json({"error": "invalid JSON"}, 400)

        token = data.get("csrf", "")
        if not secrets.compare_digest(token, CSRF_TOKEN):
            return self._json({"error": "invalid CSRF token"}, 403)

        credentials = data.get("credentials", {})
        if not isinstance(credentials, dict):
            return self._json({"error": "credentials must be a dict"}, 400)

        # Determine save path
        env_path = REPO_ROOT / ".env"

        with _env_lock:
            # Read existing
            existing: dict[str, str] = {}
            if env_path.exists():
                for line in env_path.read_text("utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        existing[k.strip()] = v.strip()

            # Merge new values (don't overwrite with empty)
            for k, v in credentials.items():
                v = str(v).strip()
                if v:
                    existing[str(k).strip()] = v

            lines = [
                "# Hermes Digital State - Local Credentials",
                "# Generated by Setup Wizard. NEVER commit this file.",
                "",
            ]
            for k, v in existing.items():
                lines.append(f"{k}={v}")

            tmp_name = ""
            try:
                with tempfile.NamedTemporaryFile(
                    "w",
                    encoding="utf-8",
                    dir=env_path.parent,
                    prefix=".env.",
                    suffix=".tmp",
                    delete=False,
                ) as tmp:
                    tmp_name = tmp.name
                    tmp.write("\n".join(lines) + "\n")
                os.replace(tmp_name, env_path)
            finally:
                if tmp_name and os.path.exists(tmp_name):
                    try:
                        os.unlink(tmp_name)
                    except OSError:
                        pass

        return self._json({"ok": True})

    # ---------- JSON response helper ----------
    def _json(self, data: Any, status: int = 200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _bind_server(preferred_port: int, attempts: int = PORT_SEARCH_LIMIT) -> tuple[HTTPServer, int]:
    if preferred_port < 1 or preferred_port > 65535:
        raise ValueError("port must be between 1 and 65535")
    last_error = None
    for candidate in range(preferred_port, min(65535, preferred_port + attempts - 1) + 1):
        try:
            return LocalThreadingHTTPServer((HOST, candidate), WizardHandler), candidate
        except OSError as e:
            last_error = e
    detail = f": {last_error}" if last_error else ""
    raise RuntimeError(
        f"no available localhost port in range {preferred_port}-{min(65535, preferred_port + attempts - 1)}{detail}"
    )


def start(port: int = 8484, open_browser: bool = True):
    """Start the wizard server."""
    server, actual_port = _bind_server(port)
    url = f"http://{HOST}:{actual_port}"

    banner = f"""
+==================================================+
|       Hermes Digital State - Setup Wizard         |
+==================================================+
|  URL:   {url:<40} |
|  Bind:  Local only ({HOST})                   |
|  Idle:  Auto-shutdown after 30 min                |
|  Stop:  Press Ctrl+C                              |
+==================================================+
"""
    try:
        print(banner, flush=True)
    except UnicodeEncodeError:
        print(banner.encode("ascii", "replace").decode("ascii"), flush=True)

    if open_browser:
        import webbrowser
        webbrowser.open(url)

    # Start idle watchdog
    watchdog = threading.Thread(target=_idle_watchdog, args=(server,), daemon=True)
    watchdog.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[wizard] Stopped.")
    finally:
        server.server_close()
