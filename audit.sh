#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo '╔═══════════════════════════════════════════════════╗'
echo '║  SPEC KIT DEEP AUDIT — Digital State v0.1.0       ║'
echo '╚═══════════════════════════════════════════════════╝'
echo ''

TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_WARN=0

# ─── 1. MANIFEST required_files ───
echo '══════════════════════════════════════'
echo '1. MANIFEST — required_files'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
while IFS= read -r f; do
    f=$(echo "$f" | tr -d '",' | xargs)
    [ -z "$f" ] && continue
    if [ -f "$f" ]; then
        echo "  ✅ $f"
        PASS=$((PASS+1))
    else
        echo "  ❌ MISSING: $f"
        FAIL=$((FAIL+1))
    fi
done < <(python3 -c "
import json
d=json.load(open('digital-state.manifest.json'))
for f in d['required_files']:
    print(f)
")
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 2. FORBIDDEN PATHS ───
echo '══════════════════════════════════════'
echo '2. SECURITY — forbidden_paths (must NOT exist)'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
for fp in .env auth.json sessions logs memory .git/config profile-export.tar.gz config.local.yaml; do
    if [ -e "$fp" ]; then
        echo "  ❌ FOUND (security risk): $fp"
        FAIL=$((FAIL+1))
    else
        echo "  ✅ Not present: $fp"
        PASS=$((PASS+1))
    fi
done
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 3. SECRETS SCAN ───
echo '══════════════════════════════════════'
echo '3. SECRETS SCAN — no API keys or tokens in code'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
for pattern in 'nvapi-' 'sk-' 'Bearer ' 'access_token' 'OPENAI_API_KEY=' 'NVIDIA_API_KEY=' 'password=' 'secret='; do
    hits=$(grep -rl "$pattern" --include='*.py' --include='*.md' --include='*.json' --include='*.yaml' --include='*.yml' . 2>/dev/null | grep -v '.git/' | grep -v 'audit.sh' || true)
    if [ -n "$hits" ]; then
        echo "  ❌ Pattern '$pattern' found in:"
        echo "$hits" | sed 's/^/     /'
        FAIL=$((FAIL+1))
    else
        echo "  ✅ No '$pattern' found"
        PASS=$((PASS+1))
    fi
done
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 4. JSON SCHEMA VALIDATION ───
echo '══════════════════════════════════════'
echo '4. SCHEMA VALIDITY — all JSON files parse correctly'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
while IFS= read -r jf; do
    if python3 -c "import json; json.load(open('$jf'))" 2>/dev/null; then
        PASS=$((PASS+1))
    else
        echo "  ❌ Invalid JSON: $jf"
        FAIL=$((FAIL+1))
    fi
done < <(find . -name '*.json' -not -path './.git/*')
echo "  ✅ $PASS JSON files valid, $FAIL invalid"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 5. SOUL.md INTEGRITY ───
echo '══════════════════════════════════════'
echo '5. SOUL.md — Constitutional Integrity'
echo '══════════════════════════════════════'
PASS=0; FAIL=0; WARN=0
for keyword in "portable" "governance" "official Hermes Agent" "Secrets are local" "evidence-oriented" "Spec Kit"; do
    if grep -q "$keyword" SOUL.md; then
        echo "  ✅ Contains: '$keyword'"
        PASS=$((PASS+1))
    else
        echo "  ❌ Missing principle: '$keyword'"
        FAIL=$((FAIL+1))
    fi
done
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 6. PORTABILITY — no absolute paths ───
echo '══════════════════════════════════════'
echo '6. PORTABILITY — no machine-specific absolute paths'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
for pattern in '/home/' '/Users/' 'C:\\' 'D:\\' '/mnt/d/' '/mnt/c/'; do
    hits=$(grep -rl "$pattern" --include='*.py' --include='*.md' --include='*.json' --include='*.yaml' . 2>/dev/null | grep -v '.git/' | grep -v 'audit.sh' | grep -v 'patches/' || true)
    if [ -n "$hits" ]; then
        echo "  ❌ Absolute path '$pattern' in:"
        echo "$hits" | sed 's/^/     /'
        FAIL=$((FAIL+1))
    else
        echo "  ✅ No '$pattern'"
        PASS=$((PASS+1))
    fi
done
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 7. GOVERNANCE DOCS COMPLETENESS ───
echo '══════════════════════════════════════'
echo '7. GOVERNANCE DOCS — completeness'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
for doc in start-here.md user-quickstart.md portable-digital-state.md update-and-recovery.md github-distribution-maintenance.md e2e-fullstack-release.md model-ministry-routing.md approval-matrix.md risk-taxonomy.md compliance-mapping.md institutional-operating-model.md maturity-model.md; do
    if [ -f "docs/governance/$doc" ]; then
        echo "  ✅ $doc"
        PASS=$((PASS+1))
    else
        echo "  ❌ MISSING: $doc"
        FAIL=$((FAIL+1))
    fi
done
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 8. SPECS STRUCTURE ───
echo '══════════════════════════════════════'
echo '8. SPEC KIT — structure & artifacts'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
for spec in 001-hyperagent-governance-integration 002-runtime-governance-guards 003-portable-digital-state-distribution; do
    for artifact in spec.md plan.md tasks.md analyze.md constitution.md; do
        if [ -f "specs/$spec/$artifact" ]; then
            PASS=$((PASS+1))
        else
            echo "  ❌ MISSING: specs/$spec/$artifact"
            FAIL=$((FAIL+1))
        fi
    done
    if [ -d "specs/$spec/schemas" ]; then
        sc=$(find "specs/$spec/schemas" -name '*.json' | wc -l)
        echo "  ✅ specs/$spec/ (5 artifacts + $sc schemas)"
    fi
done
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 9. CONFIG — model routing contract ───
echo '══════════════════════════════════════'
echo '9. CONFIG — model routing contract alignment'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
CONTRACT="specs/003-portable-digital-state-distribution/fixtures/model-ministry-routing.json"
if [ -f "$CONTRACT" ]; then
    echo "  ✅ Model routing contract exists"
    PASS=$((PASS+1))
    # Check config references it
    if grep -q "model-ministry-routing.json" config.yaml; then
        echo "  ✅ config.yaml references contract"
        PASS=$((PASS+1))
    else
        echo "  ❌ config.yaml does not reference contract"
        FAIL=$((FAIL+1))
    fi
else
    echo "  ❌ Contract file missing: $CONTRACT"
    FAIL=$((FAIL+1))
fi
if grep -q "fallback_enabled: false" config.yaml; then
    echo "  ✅ Fallback disabled (safety)"
    PASS=$((PASS+1))
else
    echo "  ⚠️  Fallback may be enabled"
    WARN=$((TOTAL_WARN+1))
fi
if grep -q "mode: manual" config.yaml; then
    echo "  ✅ Approval mode: manual"
    PASS=$((PASS+1))
else
    echo "  ❌ Approval mode not manual"
    FAIL=$((FAIL+1))
fi
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 10. DISTRIBUTION POLICY ───
echo '══════════════════════════════════════'
echo '10. DISTRIBUTION — secrets_policy'
echo '══════════════════════════════════════'
PASS=0; FAIL=0
for policy in ships_secrets ships_oauth_tokens ships_sessions ships_logs ships_memories; do
    val=$(python3 -c "import json; d=json.load(open('digital-state.manifest.json')); print(d['secrets_policy']['$policy'])")
    if [ "$val" = "False" ]; then
        echo "  ✅ $policy: false"
        PASS=$((PASS+1))
    else
        echo "  ❌ $policy: $val (MUST be false)"
        FAIL=$((FAIL+1))
    fi
done
echo "  Result: $PASS passed, $FAIL failed"
TOTAL_PASS=$((TOTAL_PASS+PASS)); TOTAL_FAIL=$((TOTAL_FAIL+FAIL))
echo ''

# ─── 11. TESTS EXIST ───
echo '══════════════════════════════════════'
echo '11. TESTS — governance test coverage'
echo '══════════════════════════════════════'
TC=$(find tests/ -name 'test_*.py' | wc -l)
echo "  ✅ $TC test files found"
find tests/ -name 'test_*.py' | sort | sed 's/^/     /'
TOTAL_PASS=$((TOTAL_PASS+1))
echo ''

# ─── 12. GIT INTEGRITY ───
echo '══════════════════════════════════════'
echo '12. GIT — repository integrity'
echo '══════════════════════════════════════'
if git fsck --no-dangling 2>/dev/null; then
    echo "  ✅ Git repository is consistent"
    TOTAL_PASS=$((TOTAL_PASS+1))
else
    echo "  ❌ Git repository has issues"
    TOTAL_FAIL=$((TOTAL_FAIL+1))
fi
COMMITS=$(git log --oneline | wc -l)
echo "  ℹ️  $COMMITS commit(s)"
echo ''

# ─── FINAL SUMMARY ───
echo '╔═══════════════════════════════════════════════════╗'
echo '║                  AUDIT SUMMARY                    ║'
echo '╚═══════════════════════════════════════════════════╝'
echo "  ✅ PASSED:  $TOTAL_PASS"
echo "  ❌ FAILED:  $TOTAL_FAIL"
echo "  ⚠️  WARNINGS: $TOTAL_WARN"
echo ''
if [ "$TOTAL_FAIL" -eq 0 ]; then
    echo '  🏛️ VERDICT: DISTRIBUTION IS SAFE FOR RELEASE'
else
    echo '  🚨 VERDICT: ISSUES FOUND — FIX BEFORE RELEASE'
fi
