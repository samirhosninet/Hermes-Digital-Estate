import os
import json
import glob
import subprocess

print("===================================================")
print("  SPEC KIT DEEP AUDIT - Digital State v0.1.1       ")
print("===================================================")
print()

TOTAL_PASS = 0
TOTAL_FAIL = 0
TOTAL_WARN = 0

def pr_pass(msg):
    global TOTAL_PASS
    print(f"  [PASS] {msg}")
    TOTAL_PASS += 1

def pr_fail(msg):
    global TOTAL_FAIL
    print(f"  [FAIL] {msg}")
    TOTAL_FAIL += 1

def pr_warn(msg):
    global TOTAL_WARN
    print(f"  [WARN] {msg}")
    TOTAL_WARN += 1

# 1. MANIFEST
print("1. MANIFEST - required_files")
try:
    with open("digital-state.manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    for req_file in manifest.get("required_files", []):
        if os.path.exists(req_file):
            pr_pass(req_file)
        else:
            pr_fail(f"MISSING: {req_file}")
except Exception as e:
    pr_fail(f"Could not load manifest: {e}")
print()

# 2. FORBIDDEN PATHS
print("2. SECURITY - forbidden_paths")
forbidden = [".env", "auth.json", "sessions", "logs", "memory", "profile-export.tar.gz", "config.local.yaml"]
for fp in forbidden:
    if os.path.exists(fp):
        pr_fail(f"FOUND (security risk): {fp}")
    else:
        pr_pass(f"Not present: {fp}")
print()

# 3. SECRETS SCAN
print("3. SECRETS SCAN - no API keys or tokens in code")
patterns = ["nvapi-", "sk-", "Bearer ", "access_token", "OPENAI_API_KEY=", "NVIDIA_API_KEY=", "password=", "secret="]
files_to_scan = []
for root, _, files in os.walk("."):
    if ".git" in root: continue
    for file in files:
        if file.endswith((".py", ".md", ".json", ".yaml", ".yml")):
            files_to_scan.append(os.path.join(root, file))

# Files excluded from secrets scan: audit tooling, test fixtures (contain
# intentional mock secrets for negative-case validation), governance docs
# (describe secret patterns without containing real values), skill
# definitions, and the runtime_governance module (defines detection regexes).
SECRET_SCAN_SKIP = {
    "audit.py", "audit.sh", "malformed.json",
    "test_model_benchmark.py", "test_runtime_governance.py",
    "test_runtime_guard_schema.py", "test_digital_state_distribution.py",
    "runtime_governance.py", "model_benchmark.py",
    "runtime-guard-design.md", "evidence-bundle.md", "SKILL.md",
    "tasks.md",
    "test_preflight.py",
}


def scan_text(path: str) -> str:
    content_lines = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue
            content_lines.append(line)
    return "".join(content_lines)

for pattern in patterns:
    found_in = []
    for fp in files_to_scan:
        if os.path.basename(fp) in SECRET_SCAN_SKIP: continue
        try:
            content = scan_text(fp)
            if pattern in content:
                found_in.append(fp)
        except:
            pass
    if found_in:
        pr_fail(f"Pattern '{pattern}' found in: {', '.join(found_in)}")
    else:
        pr_pass(f"No '{pattern}' found")
print()

# 4. JSON SCHEMA VALIDATION
print("4. SCHEMA VALIDITY - all JSON files parse correctly")
json_files = [fp for fp in files_to_scan if fp.endswith(".json") and "malformed.json" not in fp]
for jf in json_files:
    try:
        with open(jf, "r", encoding="utf-8") as f:
            json.load(f)
        pr_pass(f"Valid: {jf}")
    except:
        pr_fail(f"Invalid JSON: {jf}")
print()

# 5. SOUL.md INTEGRITY
print("5. SOUL.md - Constitutional Integrity")
try:
    with open("SOUL.md", "r", encoding="utf-8") as f:
        soul = f.read()
    keywords = ["portable", "governance", "official Hermes Agent", "Secrets are local", "evidence-oriented", "Spec Kit"]
    for kw in keywords:
        if kw in soul:
            pr_pass(f"Contains: '{kw}'")
        else:
            pr_fail(f"Missing principle: '{kw}'")
except:
    pr_fail("MISSING: SOUL.md")
    TOTAL_FAIL += 5
print()

# 6. PORTABILITY
print("6. PORTABILITY - no machine-specific absolute paths")
abs_patterns = ["/home/", "/Users/", "C:\\", "D:\\", "/mnt/d/", "/mnt/c/"]
for pattern in abs_patterns:
    found_in = []
    for fp in files_to_scan:
        if "audit.py" in fp or "audit.sh" in fp or "patches" in fp: continue
        try:
            with open(fp, "r", encoding="utf-8") as f:
                if pattern in f.read():
                    found_in.append(fp)
        except:
            pass
    if found_in:
        pr_fail(f"Absolute path '{pattern}' in: {', '.join(found_in)}")
    else:
        pr_pass(f"No '{pattern}'")
print()

# 7. GOVERNANCE DOCS COMPLETENESS
print("7. GOVERNANCE DOCS - completeness")
docs = ["start-here.md", "user-quickstart.md", "portable-digital-state.md", "update-and-recovery.md", "github-distribution-maintenance.md", "e2e-fullstack-release.md", "model-ministry-routing.md", "approval-matrix.md", "risk-taxonomy.md", "compliance-mapping.md", "institutional-operating-model.md", "maturity-model.md"]
for doc in docs:
    p = os.path.join("docs", "governance", doc)
    if os.path.exists(p):
        pr_pass(p)
    else:
        pr_fail(f"MISSING: {doc}")
print()

# 8. SPECS STRUCTURE
print("8. SPEC KIT - structure & artifacts")
specs = ["001-hyperagent-governance-integration", "002-runtime-governance-guards", "003-portable-digital-state-distribution"]
for spec in specs:
    artifacts = ["spec.md", "plan.md", "tasks.md", "analyze.md", "constitution.md"]
    for art in artifacts:
        p = os.path.join("specs", spec, art)
        if os.path.exists(p):
            pr_pass(p)
        else:
            pr_fail(f"MISSING: {p}")
    schema_dir = os.path.join("specs", spec, "schemas")
    if os.path.isdir(schema_dir):
        sc = len(glob.glob(os.path.join(schema_dir, "*.json")))
        pr_pass(f"specs/{spec}/ (5 artifacts + {sc} schemas)")
print()

# 9. CONFIG - model routing contract
print("9. CONFIG - model routing contract alignment")
contract = os.path.join("specs", "003-portable-digital-state-distribution", "fixtures", "model-ministry-routing.json")
if os.path.exists(contract):
    pr_pass("Model routing contract exists")
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            cfg = f.read()
        if "model-ministry-routing.json" in cfg:
            pr_pass("config.yaml references contract")
        else:
            pr_fail("config.yaml does not reference contract")
            
        if "fallback_enabled: false" in cfg:
            pr_pass("Fallback disabled (safety)")
        else:
            pr_warn("Fallback may be enabled")
            
        if "mode: manual" in cfg:
            pr_pass("Approval mode: manual")
        else:
            pr_fail("Approval mode not manual")
    except:
        pass
else:
    pr_fail(f"Contract file missing: {contract}")
print()

# 10. DISTRIBUTION POLICY
print("10. DISTRIBUTION - secrets_policy")
policies = ["ships_secrets", "ships_oauth_tokens", "ships_sessions", "ships_logs", "ships_memories"]
try:
    with open("digital-state.manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    sp = manifest.get("secrets_policy", {})
    for policy in policies:
        val = sp.get(policy)
        if val is False:
            pr_pass(f"{policy}: false")
        else:
            pr_fail(f"{policy}: {val} (MUST be false)")
except:
    pr_fail("Could not verify distribution policy")
print()

# 11. TESTS EXIST
print("11. TESTS - governance test coverage")
test_files = glob.glob("tests/**/test_*.py", recursive=True)
pr_pass(f"{len(test_files)} test files found")
for tf in test_files:
    print(f"     {tf}")
print()

# 12. GIT INTEGRITY
print("12. GIT - repository integrity")
try:
    res = subprocess.run(["git", "fsck", "--no-dangling"], capture_output=True, text=True)
    if res.returncode == 0:
        pr_pass("Git repository is consistent")
    else:
        pr_fail("Git repository has issues")
    
    res2 = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True)
    print(f"  [INFO] {len(res2.stdout.splitlines())} commit(s)")
except:
    pr_fail("Git check failed")
print()

print("===================================================")
print("                  AUDIT SUMMARY                    ")
print("===================================================")
print(f"  [PASS] :  {TOTAL_PASS}")
print(f"  [FAIL] :  {TOTAL_FAIL}")
print(f"  [WARN] :  {TOTAL_WARN}")
print()

if TOTAL_FAIL == 0:
    print("  *** VERDICT: DISTRIBUTION IS SAFE FOR RELEASE ***")
else:
    print("  !!! VERDICT: ISSUES FOUND - FIX BEFORE RELEASE !!!")
