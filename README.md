# Hermes Digital State 🏛️

Portable governance profile for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

## What is this?

Digital State is a **profile distribution** that installs **on top of** official Hermes Agent — it does not fork or modify the core engine. It adds:

- **Governance documents** — institutional operating model, compliance mapping, risk taxonomy
- **Spec Kit** — three structured specifications (001-003) with model council records
- **Skills** — governance-status monitoring, Spec Kit workflow
- **Runtime governance** — optional guard layer (log-only by default, requires operator approval)
- **Model ministry routing** — fixed provider/model assignments per ministry
- **Scripts** — bootstrap, portability checks, benchmarking

## Quick Install

```bash
# 1. Clone official Hermes Agent
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 2. Clone Digital State overlay
git clone https://github.com/YOUR-ORG/hermes-digital-state.git /tmp/ds-overlay

# 3. Install overlay (non-destructive copy)
bash /tmp/ds-overlay/install.sh

# 4. Apply hermes core patches (optional, for NVIDIA provider fixes)
cd /path/to/hermes-agent
for p in patches/*.patch; do git apply "$p" 2>/dev/null; done

# 5. Verify
python3 scripts/governance/bootstrap_digital_state.py --json
python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution scripts/governance
```

## Structure

```
hermes-digital-state/
├── SOUL.md                          # Constitution
├── config.yaml                      # Profile defaults (provider, model routing)
├── distribution.yaml                # Distribution metadata
├── digital-state.manifest.json      # Manifest for portability checks
├── docs/governance/                 # 24 governance documents
├── scripts/governance/              # Bootstrap, portability, benchmark scripts
├── skills/devops/governance-status/ # Governance status skill
├── skills/software-development/spec-kit/ # Spec Kit skill
├── specs/                           # 3 specifications with model council records
├── agent/runtime_governance.py      # Runtime governance module
├── tests/                           # Tests for governance components
├── patches/                         # Patches for hermes core modifications
└── install.sh                       # Non-destructive installer
```

## Compatibility

- **Requires:** Hermes Agent >= 0.12.0
- **Does not:** fork, replace, or break any Hermes core functionality
- **Updates:** Hermes core and Digital State are updated independently

## License

MIT
