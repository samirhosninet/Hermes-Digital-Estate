# User Quickstart: Portable Digital State

This guide explains the normal user workflow for Digital State.

## One-minute summary

1. Install official Hermes Agent.
2. Install the Digital State profile from GitHub.
3. Add your own local keys.
4. Run a readiness check.
5. Use Digital State through Hermes chat.
6. Update Digital State with `hermes profile update`.

## Why this design is safe for updates

Digital State is installed as a Hermes Profile Distribution. This means:

- Hermes Agent can still receive official upstream updates.
- Digital State can receive its own GitHub updates.
- User secrets stay local.
- The profile can be reinstalled on a new device.
- The project does not require a custom Hermes fork.

## Install flow

### Step 1: Install official Hermes Agent

Follow the official Hermes Agent installation path first.

Common terminal install:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Run the setup wizard:

```bash
hermes setup
```

Check the installation:

```bash
hermes config check
hermes doctor
```

### Step 2: Install Digital State

Install the profile distribution from GitHub:

```bash
hermes profile install github.com/samirhosninet/Hermes-Digital-Estate --alias
```

For local testing before publication, maintainers may use a local path instead:

```bash
hermes profile install ./hermes-digital-state --alias
```

### Step 3: Add local credentials

Copy the example environment file if instructed by Hermes or the distribution docs:

```bash
cp .env.EXAMPLE .env
```

Then add only the keys you actually need.

Do not commit `.env` to GitHub.

### Step 4: Run readiness checks

From the distribution workspace, run:

```bash
python3 scripts/governance/bootstrap_digital_state.py
```

Optional JSON output:

```bash
python3 scripts/governance/bootstrap_digital_state.py --json
```

### Step 5: Start using Digital State

Start chat with the Digital State profile:

```bash
hermes -p digital-state chat
```

Then type:

```text
Start setup
```

or Arabic:

```text
ابدأ الإعداد
```

## Daily use

Use Digital State like a normal Hermes profile:

```bash
hermes -p digital-state chat
```

Useful requests:

```text
افحص حالة الدولة الرقمية
```

```text
افحص الجاهزية بعد التحديث
```

```text
راجع الخطة باستخدام Spec Kit
```

```text
شغّل فحص قابلية النقل
```

## Updating

Update Digital State:

```bash
hermes profile update digital-state
```

Then run:

```bash
python3 scripts/governance/bootstrap_digital_state.py
```

If the update fails, do not edit Hermes core manually. Use the update and recovery guide.

## Moving to another device

On the new device:

1. Install official Hermes Agent.
2. Install Digital State again from GitHub.
3. Add local keys again.
4. Run bootstrap.
5. Start chat.

Do not copy old sessions, logs, OAuth tokens, or `.env` files unless your organization has a secure secret-transfer process.

## For teams and organizations

Teams should define:

- who manages GitHub releases,
- who approves updates,
- where secrets are stored,
- which models are allowed,
- whether Model Council checks are required,
- what evidence must be saved before major changes.

Use the institution installation and governance docs for that workflow.

## Support boundaries

Digital State is a governance and operating profile. It does not claim government certification, space mission approval, or security accreditation by itself. Those require external organizational review and formal approval.
