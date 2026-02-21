---
name: guardian
description: '"I heard OpenClaw has security risks. How do I lock it down?" Install Guardian. That''s it.'
version: 2.0.3
---

# Guardian

## ⚡ AGENT — DO THIS FIRST (every time you read this file)

**Step 1 — Check if Guardian needs activation:**

```bash
# Check for pending activation marker (written by install.sh)
ls .guardian-activate-pending 2>/dev/null && echo "NEEDS_ACTIVATION" || \
python3 skills/guardian/scripts/onboard.py --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','unknown'))"
```

- If output is `NEEDS_ACTIVATION` or `onboarded` is not in output → **run Steps 2–5 now**
- If output is `onboarded` → Guardian is active, skip to normal operation

**Step 2 — Activate and notify:**

```bash
python3 skills/guardian/scripts/onboard.py
```

Capture the full output. It contains three sections:
1. `SECTION 1 — AGENT BRIEFING` — confirms GUARDIAN.md was written to workspace root. Nothing to send.
2. `SECTION 2 — ADMIN NOTIFICATION` — **send this to the user via their primary channel RIGHT NOW** (Telegram/Discord/Signal). Use your messaging tool. Do not just show it in the chat response.
3. `SECTION 3 — SETUP CHECKLIST` — **send this to the user too**. It shows what's running, what's missing, and ready-to-paste cron commands.

**Step 3 — Set up background scanning (critical):**

Check if cron jobs are needed:

```bash
python3 skills/guardian/scripts/onboard.py --status
```

If any ❌ items appear, run:

```bash
python3 skills/guardian/scripts/onboard.py --setup-crons
```

This auto-installs the missing cron jobs. Confirm to the user: "Background scanning is now active."

If `--setup-crons` fails (permission issue), show the user the manual cron lines from `--status` output and tell them to run `crontab -e` and paste them in.

**Step 4 — Config review:**

```bash
python3 skills/guardian/scripts/onboard.py --config-review
```

Send that output to the user. It shows what's set and flags anything worth changing.

**Step 5 — Confirm and clean up:**

Send the user a final confirmation:
> "✅ Guardian is now fully operational. Background scanning is active, your dashboard is live at [URL], and you'll get alerts for any threats. You're protected."

Then delete the pending marker if it exists:
```bash
rm -f .guardian-activate-pending
```

> If onboard.py doesn't exist yet, run `./install.sh` first.

---

## 🎯 AGENT — Skill Invoked With No Specific Request

When the user says "use the guardian skill" or similar without specifying what they want, provide a **concise status card + menu** instead of asking "what do you need?":

**Step 1 — Get current status:**

```bash
python3 skills/guardian/scripts/admin.py status --json 2>/dev/null
```

**Step 2 — Format the response like this:**

```
🛡️ **Guardian Security Status**

**Current State:**
• Status: [enabled/disabled]
• Mode: [realtime/bypass if admin_override is true]
• Severity threshold: [low/medium/high/critical]
• Recent threats: [count from last 24h]
• Background scanning: [active/inactive based on cron status]

**Quick Actions:**
1️⃣ **Scan now** — `python3 skills/guardian/scripts/guardian.py --report --hours 24`
2️⃣ **View dashboard** — [dashboard URL from config]
3️⃣ **Show recent threats** — `python3 skills/guardian/scripts/admin.py threats`
4️⃣ **Update definitions** — `python3 skills/guardian/scripts/admin.py update-defs`
5️⃣ **Full security report** — `python3 skills/guardian/scripts/admin.py report`
6️⃣ **Modify config** — Edit `skills/guardian/config.json`

What would you like to do?
```

**Step 3 — If status command fails:**
Fall back to a simplified response:
```
🛡️ **Guardian Security**

Guardian provides real-time threat detection and workspace scanning.

**Available actions:**
• Run a security scan
• View the dashboard
• Check recent threats
• Update threat definitions
• Review/modify configuration

What would you like me to help with?
```

---

## Installation

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

`install.sh` automatically runs onboarding. But the **agent** (you) must relay the notification output to the user — the script can't send to Telegram/Discord directly.

Optional explicit Python executable:
```bash
VENV_PYTHON=/path/to/python3 ./install.sh
```

---

## Re-running Onboarding

After any config change, re-run:
```bash
python3 skills/guardian/scripts/onboard.py --refresh
```
Then send the updated notification to the user.

Override the dashboard URL:
```bash
python3 skills/guardian/scripts/onboard.py --refresh --dashboard-url http://YOUR-SERVER-IP:PORT/guardian.html
```

---

## Admin Quick Reference

```bash
python3 scripts/admin.py status
python3 scripts/admin.py disable
python3 scripts/admin.py disable --until "2h"
python3 scripts/admin.py enable
python3 scripts/admin.py bypass --on
python3 scripts/admin.py bypass --off
python3 scripts/admin.py dismiss INJ-004
python3 scripts/admin.py allowlist add "safe test phrase"
python3 scripts/admin.py allowlist remove "safe test phrase"
python3 scripts/admin.py threats
python3 scripts/admin.py threats --clear
python3 scripts/admin.py report
python3 scripts/admin.py update-defs
```

Use machine-readable mode with `--json` on any command.

---

## Real-Time Pre-Scan (Layer 1)

Use `RealtimeGuard` before handling user requests:

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="discord")
if guard.should_block(result):
    return guard.format_block_response(result)
```

Behavior:
- Scans only `high` and `critical` signatures for low latency.
- Blocks critical/high-risk payloads before they reach the main model/tool chain.
- Returns `ScanResult(blocked, threats, score, suggested_response)`.

---

## Configuration Reference (`config.json`)

- `enabled`: Master on/off switch for Guardian.
- `admin_override`: Bypass mode (log and report, do not block).
- `scan_paths`: Paths to scan (`["auto"]` discovers common OpenClaw folders).
- `db_path`: SQLite location (`"auto"` resolves to `<workspace>/guardian.db`).
- `scan_interval_minutes`: Batch scan cadence.
- `severity_threshold`: Blocking threshold for scanner (`low|medium|high|critical`).
- `dismissed_signatures`: Signature IDs globally suppressed.
- `custom_definitions_dir`: Custom definition directory override.
- `channels.monitor_all`: Whether all channels are monitored.
- `channels.exclude_channels`: Channels to ignore.
- `alerts.notify_on_critical`: Emit critical alerts.
- `alerts.notify_on_high`: Emit high alerts.
- `alerts.daily_digest`: Send daily digest.
- `alerts.daily_digest_time`: Digest delivery time.
- `admin.bypass_token`: Optional token for admin bypass workflows.
- `admin.disable_until`: Temporary disable-until timestamp.
- `admin.trusted_sources`: Trusted channels/sources for privileged requests.
- `admin.require_confirmation_for_severity`: Severity levels requiring confirmation.
- `false_positive_suppression.min_context_words`: Minimum context size for suppression.
- `false_positive_suppression.suppress_assistant_number_matches`: Avoid noisy number matches.
- `false_positive_suppression.allowlist_patterns`: Pattern list to suppress known false positives.
- `definitions.update_url`: Optional manifest URL for definition updates (default upstream URL used when absent).

### Control UI integration

Guardian config now renders in the OpenClaw Control UI **Config** panel (http://localhost:18789) under `skills.guardian.config`. The UI exposes:
- `enabled`
- `severity_threshold`
- `scan_interval_minutes`
- `trusted_sources`
- `alerts.notify_on_critical`
- `alerts.notify_on_high`
- `alerts.daily_digest`
- `alerts.daily_digest_time`

Guardian reads these values from `openclaw.json` first and falls back to `skills/guardian/config.json` if they are missing.

---

## Allowlist Feature (False Positive Suppression)

The allowlist completely bypasses threat scanning for messages matching specific patterns. This is useful for known-safe system messages that might otherwise trigger false positives.

### Current Allowlist Patterns

The default configuration includes patterns for OpenClaw internal system messages:

```json
"allowlist_patterns": [
  "WORKFLOW_AUTO\\.md",
  "(?i)openclaw\\s+(internal|system|post-compaction|audit)",
  "(?i)post-compaction\\s+(audit|restore|protocol)",
  "(?i)system\\s+(reminder|protocol|message).*(?:read|follow|check).*(?:SOUL\\.md|USER\\.md|MEMORY\\.md|WORKFLOW_AUTO\\.md)"
]
```

These patterns protect:
- **WORKFLOW_AUTO.md references** - System workflow restoration after context compaction
- **OpenClaw internal messages** - System audit and status messages
- **Post-compaction protocols** - Context restore and agent startup procedures
- **System file reminders** - Instructions to read SOUL.md, USER.md, MEMORY.md

### Adding Allowlist Patterns

**Via CLI (recommended):**
```bash
python3 scripts/admin.py allowlist add "PATTERN"
python3 scripts/admin.py allowlist remove "PATTERN"
```

**Manual (edit config.json):**
```json
{
  "false_positive_suppression": {
    "allowlist_patterns": [
      "your-safe-pattern-here"
    ]
  }
}
```

### Security Best Practices

**✅ DO:**
- Use specific patterns that identify internal system processes
- Include unique markers (file names, system identifiers)
- Test patterns thoroughly before deployment
- Document why each pattern is safe

**❌ DON'T:**
- Add broad patterns that could match user input
- Allowlist based solely on message content without context
- Use as a workaround for signature tuning
- Add patterns containing `.*` or other broad wildcards

### Testing Allowlist Patterns

```bash
cd skills/guardian

# Test a specific message
python3 -c "from core.scanner import quick_scan; import json; \
  result = quick_scan('YOUR MESSAGE HERE'); \
  print('Allowlisted:', result.get('allowlisted', False)); \
  print('Clean:', result['clean'])"

# Run allowlist test suite
python3 test_allowlist.py
```

### Examples

**Safe Pattern (✅):**
```json
"WORKFLOW_AUTO\\.md"
```
Matches only messages containing "WORKFLOW_AUTO.md" - a specific system file.

**Unsafe Pattern (❌):**
```json
".*system.*"
```
Too broad - would match any user message containing "system".

**Balanced Pattern (✅):**
```json
"(?i)openclaw\\s+internal:\\s+"
```
Specific enough - requires "OpenClaw internal:" prefix which is only used by system messages.

---

## Standalone Dashboard

Guardian includes a self-contained dashboard (no full NOC stack required):

```bash
cd skills/guardian/dashboard
python3 -m http.server 8091
# Open: http://localhost:8091/guardian.html
```

Or access it via the NOC dashboard Guardian tab if installed.

---

## Troubleshooting

- `scripts/admin.py status` fails: ensure `config.json` is valid JSON and DB path is writable.
- No threats appear: confirm definitions exist in `definitions/*.json` and `enabled` is true.
- Update checks fail: validate network access to `definitions.update_url` and run `python3 definitions/update.py --version`.
- Dashboard export empty: check the DB path used by `scripts/dashboard_export.py --db /path/to/guardian.db`.
- Unexpected blocking: inspect recent events with `python3 scripts/admin.py threats --json` and tune `severity_threshold` or allowlist patterns.
