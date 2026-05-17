#!/usr/bin/env bash
# Hermes Digital State - One-Click Setup Wizard
# Usage: double-click or run: bash START.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "  ==================================================="
echo "   Hermes Digital State - Setup Wizard"
echo "  ==================================================="
echo ""

PY=""
for cmd in python3 python; do
    if command -v "$cmd" >/dev/null 2>&1; then
        ver="$("$cmd" --version 2>&1 | awk '{print $2}')"
        major="$(printf '%s' "$ver" | cut -d. -f1)"
        minor="$(printf '%s' "$ver" | cut -d. -f2)"
        if [ "${major:-0}" -ge 3 ] && [ "${minor:-0}" -ge 10 ]; then
            PY="$cmd"
            break
        fi
    fi
done

if [ -z "$PY" ]; then
    echo "  [ERROR] Python 3.10+ not found!"
    echo ""
    echo "  Install Python:"
    echo "    macOS:  brew install python3"
    echo "    Ubuntu: sudo apt install python3"
    echo "    Fedora: sudo dnf install python3"
    echo ""
    exit 1
fi

LOG="${TMPDIR:-/tmp}/hermes-digital-state-wizard.log"
rm -f "$LOG"

echo "  Python found: $($PY --version 2>&1)"
echo "  Starting wizard in the background..."
echo "  Log: $LOG"

"$PY" "$SCRIPT_DIR/wizard.py" --no-browser >"$LOG" 2>&1 &
WIZARD_PID=$!

cleanup_failed() {
    if kill -0 "$WIZARD_PID" >/dev/null 2>&1; then
        kill "$WIZARD_PID" >/dev/null 2>&1 || true
    fi
}

URL=""
deadline=$((SECONDS + 20))
while [ "$SECONDS" -lt "$deadline" ]; do
    if [ -s "$LOG" ]; then
        URL="$(grep -Eo 'http://127\.0\.0\.1:[0-9]+' "$LOG" | head -n 1 || true)"
        if [ -n "$URL" ]; then
            if "$PY" - "$URL" <<'PY' >/dev/null 2>&1
import sys
from urllib.request import urlopen

with urlopen(sys.argv[1] + "/api/info", timeout=2) as response:
    raise SystemExit(0 if response.status == 200 else 1)
PY
            then
                break
            fi
        fi
        if grep -Eq 'Traceback|RuntimeError|ValueError|Error:' "$LOG"; then
            break
        fi
    fi
    sleep 0.5
done

if [ -z "$URL" ]; then
    cleanup_failed
    echo ""
    echo "  [ERROR] Wizard did not become ready."
    echo "  Review the log:"
    echo "  $LOG"
    echo ""
    [ -f "$LOG" ] && cat "$LOG"
    echo ""
    exit 1
fi

echo "  Wizard ready: $URL"
"$PY" - "$URL" <<'PY' >/dev/null 2>&1 || true
import sys
import webbrowser

webbrowser.open(sys.argv[1])
PY
