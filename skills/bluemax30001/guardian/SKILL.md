---
name: guardian
description: Security scanner for OpenClaw agents. Detects prompt injection, credential exfiltration, and social engineering attacks in real time.
version: 2.0.14
metadata:
  openclaw:
    requires:
      bins:
        - python3
    permissions:
      - read_workspace
      - write_workspace
      - shell_optional
      - network_optional
---

# Guardian

Security scanner for OpenClaw agents. Detects prompt injection, credential
exfiltration attempts, tool abuse patterns, and social engineering attacks using
regex-based signature matching.

Guardian provides two scanning modes:

- **Real-time pre-scan** — checks each incoming message before it reaches the model
- **Batch scan** — periodic sweep of workspace files and conversation logs

All data stays local by default. Optional components:
- **Webhook notifications**: `integrations/webhook.py` (sends JSON payloads to a configured URL)
- **HTTP API server**: `scripts/serve.py` (exposes scan/report endpoints)
- **Cron setup**: `scripts/onboard.py --setup-crons` (configures scanner/report/digest crons)

Scan results are stored in a SQLite database (`guardian.db`).

## Installation

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

## Install mechanism and review
This package includes executable scripts (including `install.sh`) and Python modules.
Review `install.sh` before running in production.
`install.sh` performs local setup/validation; optional helpers (`onboard.py`, `serve.py`, `integrations/webhook.py`) are opt-in and require explicit operator action.

## Onboarding checklist
1) Optional: `python3 scripts/onboard.py --setup-crons` (scanner/report/digest crons)
2) `python3 scripts/admin.py status` (confirm running)
3) `python3 scripts/admin.py threats` (confirm signatures loaded; should show 0/blocked)
4) Optional: `python3 scripts/serve.py --port 8090` (start HTTP API)
5) Optional: set `webhook_url` in `config.json` (enable outbound alerts)

## Scan scope and privacy
Guardian scans configured workspace paths to detect threats. Depending on `scan_paths`, this can include other skill/config files in your OpenClaw workspace.
If you handle sensitive files, set narrow `scan_paths` in `config.json`.

## Quick Start

```bash
# Check status
python3 scripts/admin.py status

# Scan recent threats
python3 scripts/guardian.py --report --hours 24

# Full report
python3 scripts/admin.py report
```

## Admin Commands

```bash
python3 scripts/admin.py status          # Current status
python3 scripts/admin.py enable          # Enable scanning
python3 scripts/admin.py disable         # Disable scanning
python3 scripts/admin.py threats         # List detected threats
python3 scripts/admin.py threats --clear # Clear threat log
python3 scripts/admin.py dismiss INJ-004 # Dismiss a signature
python3 scripts/admin.py allowlist add "safe phrase"
python3 scripts/admin.py allowlist remove "safe phrase"
python3 scripts/admin.py update-defs     # Update threat definitions
```

Add `--json` to any command for machine-readable output.

## Python API

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="telegram")
if guard.should_block(result):
    return guard.format_block_response(result)
```

## Environment variables read
- `GUARDIAN_WORKSPACE` (optional workspace override)
- `OPENCLAW_WORKSPACE` (optional fallback workspace override)
- `GUARDIAN_CONFIG` (optional guardian config path)
- `OPENCLAW_CONFIG_PATH` (optional OpenClaw config path)

## Configuration

Edit `config.json`:

| Setting | Description |
|---|---|
| `enabled` | Master on/off switch |
| `severity_threshold` | Blocking threshold: `low` / `medium` / `high` / `critical` |
| `scan_paths` | Paths to scan (`["auto"]` for common folders) |
| `db_path` | SQLite location (`"auto"` = `<workspace>/guardian.db`) |
| `webhook_url` | Optional: POST scan results here |
| `http_server.port` | Optional: port for scripts/serve.py |

## How It Works

Guardian loads threat signatures from `definitions/*.json` files. Each signature has
an ID, regex pattern, severity level, and category. Incoming text is matched against
all active signatures. Matches above the configured severity threshold are blocked
and logged to the database.

Signatures cover: prompt injection, credential patterns (API keys, tokens),
data exfiltration attempts, tool abuse patterns, and social engineering tactics.
