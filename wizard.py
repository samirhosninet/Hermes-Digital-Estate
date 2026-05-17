#!/usr/bin/env python3
"""Hermes Digital State — Setup Wizard.

Usage:
    python wizard.py              # Start on first available port from 8484
    python wizard.py --port 9090  # Prefer 9090, then try later ports
    python wizard.py --no-browser # Don't auto-open browser
"""
from __future__ import annotations

import argparse
import sys

MIN_PYTHON = (3, 10)

def main():
    if sys.version_info < MIN_PYTHON:
        print(f"Error: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required, found {sys.version}")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Hermes Digital State Setup Wizard",
        epilog="Opens a guided web interface at http://127.0.0.1:PORT",
    )
    parser.add_argument("--port", type=int, default=8484, help="Preferred port to bind (default: 8484)")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open browser")
    args = parser.parse_args()

    from preflight.server import start
    start(port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
