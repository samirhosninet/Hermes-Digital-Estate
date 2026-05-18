# Start Here: Digital State for Hermes Agent

This page is for non-technical users. You do not need to understand Git, Python, workspaces, or profiles to start.

Arabic operator guide: [دليل تشغيل الدولة الرقمية](digital-state-runbook-ar.md).

## What this is

Digital State is an add-on profile for official Hermes Agent.

- Hermes Agent is the engine.
- Digital State is the governance and operating layer installed on top of Hermes.
- Your keys, accounts, memory, sessions, and logs stay on your own device.

Digital State is not a fork of Hermes Agent and does not replace the official Hermes installation.

## The simple path

### Windows: use the stack installer

On a fresh Windows machine, open PowerShell and run:

```powershell
irm https://raw.githubusercontent.com/samirhosninet/Hermes-Digital-Estate/refs/heads/main/scripts/bootstrap/install-windows.ps1 | iex
```

This downloads the Digital State bootstrap package and opens a local Web UI. The UI installs official Hermes Agent first; Hermes Agent's Windows installer provisions Python, Node.js 22, and PortableGit.

Manual fallback: download the repository ZIP, extract it, then double-click:

```bat
START.bat
```

The local UI checks and installs Hermes Agent, Hermes Workspace, and the Digital State profile in order. If something is missing, the UI explains what failed, why it matters, and the command or link to fix it.

### Terminal path: install official Hermes Agent

Use the official Hermes installation instructions from NousResearch.

If you are using a terminal, the common install command is:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Then run:

```bash
hermes setup
hermes config check
```

### Install Digital State

Install the Digital State profile distribution:

```bash
hermes profile install github.com/samirhosninet/Hermes-Digital-Estate --alias
```

This is the canonical GitHub source for the Digital State profile distribution.

### Start Digital State

Run:

```bash
hermes -p digital-state chat
```

If an alias wrapper is created by Hermes, you may also be able to run:

```bash
digital-state chat
```

### Say this

Inside the chat, type:

```text
ابدأ الإعداد
```

or:

```text
Start setup
```

Digital State should guide you through the next steps.

## What you may need to add

You may need one or more model/API keys depending on the features you want:

- NVIDIA_API_KEY for NVIDIA NIM models and Model Council checks.
- OPENROUTER_API_KEY for optional OpenRouter models.
- ANTHROPIC_API_KEY for optional Anthropic models.
- VOICE_TOOLS_OPENAI_KEY only if voice features are enabled.

Never paste keys into public GitHub files, docs, screenshots, or chat logs that may be shared.

## Check if everything is ready

From the Digital State project folder, run:

```bash
python3 scripts/governance/bootstrap_digital_state.py
```

A healthy result says:

```text
Digital State bootstrap: OK
```

If it says FAILED, read the lines below it. They should explain what is missing.

## How to update

Update official Hermes Agent separately using the official Hermes update flow.

Update Digital State with:

```bash
hermes profile update digital-state
```

Then run the bootstrap check again.

## If you move to another device

On the new device:

1. Install official Hermes Agent.
2. Install Digital State again with `hermes profile install ...`.
3. Add your own local API keys again.
4. Run the bootstrap check.
5. Start `hermes -p digital-state chat`.

Digital State should not depend on a Windows drive, a personal home folder, or another project folder.

## What Digital State does not do yet

Digital State currently provides governance, docs, skills, checks, and planning.

It does not currently enforce runtime blocking on terminal/file/gateway commands. Runtime guard work is tracked separately and must be approved explicitly before any live hook is enabled.
