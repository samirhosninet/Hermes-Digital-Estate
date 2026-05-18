# Hermes Digital State

Portable governance profile for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

## What is this?

Digital State is a **profile distribution** that installs **on top of** official Hermes Agent — it does not fork or modify the core engine. It adds:

- **Governance documents** — institutional operating model, compliance mapping, risk taxonomy
- **Spec Kit** — three structured specifications (001-003) with model council records
- **Skills** — governance-status monitoring, Spec Kit workflow
- **Runtime governance** — optional guard layer (log-only by default, requires operator approval)
- **Model ministry routing** — fixed provider/model assignments per ministry
- **Scripts** — bootstrap, portability checks, benchmarking

## Windows Stack Installer (Recommended)

**Fresh Windows machine:** open PowerShell and run:

```powershell
irm https://raw.githubusercontent.com/samirhosninet/Hermes-Digital-Estate/main/scripts/bootstrap/install-windows.ps1 | iex
```

This downloads the Digital State bootstrap package, opens the local **Install Digital State Stack** UI, and starts with official Hermes Agent installation. Hermes Agent's Windows installer is responsible for provisioning Python, Node.js 22, and PortableGit.

**Manual fallback:** download the repository ZIP, extract it, then double-click `START.bat`.

The local Web UI checks and installs Hermes Agent, Hermes Workspace, and the Digital State profile in order, with visible logs and manual fallback commands when something fails.

**macOS / Linux:** run the setup wizard directly with `bash START.sh`.

The wizard opens automatically in your browser, starting at `http://127.0.0.1:8484` or the next available local port, with a guided readiness check.

Alternatively, run directly:
```bash
python wizard.py
python wizard.py --no-browser  # diagnostic mode
```

Arabic operator guide: [docs/governance/digital-state-runbook-ar.md](docs/governance/digital-state-runbook-ar.md).

## Quick Install (Advanced)

```bash
# 1. Install official Hermes Agent first, then install this profile distribution
hermes profile install github.com/samirhosninet/Hermes-Digital-Estate --alias

# 2. Verify
hermes profile show digital-state
hermes -p digital-state config check
python3 scripts/governance/bootstrap_digital_state.py --json
python3 scripts/governance/check_portability.py docs/governance skills/devops/governance-status specs/003-portable-digital-state-distribution specs/004-setup-wizard-hardening scripts/bootstrap scripts/governance wizard.py preflight START.bat START.sh
```

## Structure

```
hermes-digital-state/
├── SOUL.md                          # Constitution
├── config.yaml                      # Profile defaults (provider, model routing)
├── distribution.yaml                # Distribution metadata
├── digital-state.manifest.json      # Manifest for portability checks
├── docs/governance/                 # Governance documents and operator runbooks
├── scripts/bootstrap/               # Windows stack installer UI
├── scripts/governance/              # Bootstrap, portability, benchmark scripts
├── skills/devops/governance-status/ # Governance status skill
├── skills/software-development/spec-kit/ # Spec Kit skill
├── specs/                           # 3 specifications with model council records
├── agent/runtime_governance.py      # Runtime governance module
├── preflight/                       # Local setup wizard server and checks
└── tests/                           # Tests for governance components
```

## Compatibility

- **Requires:** Hermes Agent >= 0.12.0
- **Does not:** fork, replace, or break any Hermes core functionality
- **Updates:** Hermes core and Digital State are updated independently

## License

MIT
