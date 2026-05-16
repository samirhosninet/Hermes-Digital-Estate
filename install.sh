#!/usr/bin/env bash
# install.sh — Non-destructive Digital State installer for Hermes Agent
# Usage: bash install.sh [hermes-agent-dir]
#
# This script copies Digital State files INTO an existing Hermes Agent
# installation WITHOUT overwriting any Hermes core files.
# If a target file already exists and belongs to Hermes core, it is SKIPPED.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HERMES_DIR="${1:-$(pwd)}"

# --- Validation ---
if [[ ! -f "$HERMES_DIR/pyproject.toml" ]] || ! grep -q "hermes" "$HERMES_DIR/pyproject.toml" 2>/dev/null; then
    echo "❌ Error: '$HERMES_DIR' does not look like a Hermes Agent directory."
    echo "   Usage: bash install.sh /path/to/hermes-agent"
    exit 1
fi

echo "🏛️  Digital State Installer"
echo "   Source:  $SCRIPT_DIR"
echo "   Target:  $HERMES_DIR"
echo ""

# --- Helper: safe copy (skip if target exists in git history) ---
safe_copy() {
    local src="$1"
    local dst="$2"
    local rel_dst="${dst#$HERMES_DIR/}"

    # Create parent directory
    mkdir -p "$(dirname "$dst")"

    # Check if this file is tracked by hermes git (= core file)
    if cd "$HERMES_DIR" && git ls-files --error-unmatch "$rel_dst" &>/dev/null 2>&1; then
        echo "   ⏭️  SKIP (hermes core): $rel_dst"
        return 0
    fi

    cp "$src" "$dst"
    echo "   ✅ COPY: $rel_dst"
}

# --- Helper: safe copy directory ---
safe_copy_dir() {
    local src_dir="$1"
    local dst_dir="$2"

    find "$src_dir" -type f | while read -r src_file; do
        local rel="${src_file#$src_dir/}"
        safe_copy "$src_file" "$dst_dir/$rel"
    done
}

# --- Root files ---
echo "📄 Root files:"
for f in SOUL.md config.yaml distribution.yaml digital-state.manifest.json inspect_codex_auth.py; do
    if [[ -f "$SCRIPT_DIR/$f" ]]; then
        safe_copy "$SCRIPT_DIR/$f" "$HERMES_DIR/$f"
    fi
done
echo ""

# --- Directories ---
echo "📁 Governance docs:"
safe_copy_dir "$SCRIPT_DIR/docs/governance" "$HERMES_DIR/docs/governance"
echo ""

echo "📁 Governance scripts:"
safe_copy_dir "$SCRIPT_DIR/scripts/governance" "$HERMES_DIR/scripts/governance"
echo ""

echo "📁 Skills:"
safe_copy_dir "$SCRIPT_DIR/skills" "$HERMES_DIR/skills"
echo ""

echo "📁 Specs:"
safe_copy_dir "$SCRIPT_DIR/specs" "$HERMES_DIR/specs"
echo ""

echo "📁 Agent modules:"
safe_copy "$SCRIPT_DIR/agent/runtime_governance.py" "$HERMES_DIR/agent/runtime_governance.py"
echo ""

echo "📁 Tests:"
safe_copy_dir "$SCRIPT_DIR/tests" "$HERMES_DIR/tests"
echo ""

# --- Apply patches (optional) ---
if [[ -d "$SCRIPT_DIR/patches" ]]; then
    echo "🩹 Applying patches to hermes core:"
    cd "$HERMES_DIR"
    for patch_file in "$SCRIPT_DIR/patches/"*.patch; do
        patch_name="$(basename "$patch_file")"
        if git apply --check "$patch_file" 2>/dev/null; then
            git apply "$patch_file"
            echo "   ✅ APPLIED: $patch_name"
        else
            echo "   ⚠️  SKIP (conflict or already applied): $patch_name"
        fi
    done
    echo ""
fi

# --- Verification ---
echo "🔍 Running verification..."
cd "$HERMES_DIR"

if [[ -f "scripts/governance/bootstrap_digital_state.py" ]]; then
    python3 scripts/governance/bootstrap_digital_state.py --json 2>/dev/null && echo "   ✅ Bootstrap check passed" || echo "   ⚠️  Bootstrap check had warnings"
fi

if [[ -f "scripts/governance/check_portability.py" ]]; then
    python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution scripts/governance 2>/dev/null && echo "   ✅ Portability check passed" || echo "   ⚠️  Portability check had warnings"
fi

echo ""
echo "✅ Digital State installation complete!"
echo "   Next: hermes -p digital-state chat"
