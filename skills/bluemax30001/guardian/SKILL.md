---
name: guardian
description: OpenClaw security shield for prompt-injection, exfiltration, tool-abuse, and social-engineering defense.
version: 1.0.0
---

# Guardian

Guardian adds policy enforcement, scanning, and reporting for OpenClaw deployments.

## Installation

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

Optional explicit Python executable:

```bash
VENV_PYTHON=/path/to/python3 ./install.sh
```

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

## Troubleshooting

- `scripts/admin.py status` fails: ensure `config.json` is valid JSON and DB path is writable.
- No threats appear: confirm definitions exist in `definitions/*.json` and `enabled` is true.
- Update checks fail: validate network access to `definitions.update_url` and run `python3 definitions/update.py --version`.
- Dashboard export empty: check the DB path used by `scripts/dashboard_export.py --db /path/to/guardian.db`.
- Unexpected blocking: inspect recent events with `python3 scripts/admin.py threats --json` and tune `severity_threshold` or allowlist patterns.
