---
name: proactive-claw
version: 1.2.0
description: >
  Transform AI agents into governed execution partners that understand your work, monitor your
  context, and act ahead of you — predictively and under your control. 🧠⚙️🦞

  **LOCAL-FIRST AUTOMATION**: Reads your calendars (read-only) and writes only to its own
  "Proactive Claw — Actions" calendar. Runs a user-level background daemon (15-min cycles).
  All decisions logged locally. **Safe defaults: most features OFF by default.**

  **Two modes of action:**
  1. **Daemon mode** (background, PLAN→EXECUTE every 15 min): ingests user events, detects
     deletions, auto-relinks moved events, plans reminders and prep blocks, fires due actions
     idempotently. Reads all user calendars (read-only). Writes action calendar + SQLite DB only.
  2. **Conversation mode** (optional, requires separate enabled LLM): when chatting with you,
     Claude Code can optionally call proactive-claw scripts to read your calendar context,
     propose schedule changes, or log outcomes — **only if you enable this per conversation.**
     This is NOT automatic and requires explicit user opt-in each time.

  **Governance layer**: Unified proactivity engine merges energy, notification, policy, and
  relationship signals. Priority tiers P0–P5, quiet hours, cooldowns, max nudges/day. Global
  intensity dial (low/balanced/executive) and max autonomy cap (advisory/confirm/autonomous).
  Explainability mode traces every decision.

  **Memory & Learning**: Decay-weighted scoring (recent data counts more). SQLite link graph
  connects user events to planned actions. Policy conflict detection. System health audit.

  **Productization**: Config wizard, data export/backup, monthly drift monitoring, simulation
  mode, soft-cancel policy.

  **Requires**: python3, Google OAuth credentials (or Nextcloud app password).

  **Optional (all OFF by default)**: gh CLI (feature_cross_skill), NOTION_API_KEY, Telegram
  bot token (feature_telegram), LLM_RATER_API_KEY (feature_llm_rater), Apple Notes osascript
  (macOS only, notes_destination=apple-notes), Notion outcome DB (notes_destination=notion).

  **SAFE DEFAULTS**: feature_cross_skill=false, feature_voice=false, feature_team_awareness=false,
  feature_llm_rater=false, max_autonomy_level=confirm (not autonomous).

requires:
  bins:
    - python3
  env_vars: []
  credentials:
    - Google OAuth credentials (via setup.sh) OR Nextcloud app password (via setup.sh)

install:
  - kind: script
    label: "One-time setup — creates calendar, installs dependencies, configures daemon"
    command: "bash scripts/setup.sh"

side_effects:
  - Installs a user-level background daemon (launchd on macOS, systemd user timer on Linux) via install_daemon.sh. Runs every 15 min. Does NOT run as root. Uninstall instructions in SKILL.md.
  - Writes local files under ~/.openclaw/workspace/skills/proactive-agent/ only. No files written outside this directory.
  - Creates a "Proactive Claw — Actions" calendar in Google/Nextcloud. Never modifies your existing calendars — reads them only.
  - Maintains a SQLite link graph (proactive_links.db) tracking connections between your events and planned actions.
  - Outbound HTTPS to Google Calendar API only by default. Notion, Telegram, GitHub, clawhub.ai, LLM rating API are all opt-in via feature_* flags in config.json.
  - pip installs google-api-python-client, google-auth-oauthlib, google-auth-httplib2 (Google backend) or caldav, icalendar (Nextcloud backend) during setup.sh.
---

# 🦞 Proactive Claw v1.2.0

> Transform AI agents into governed execution partners that understand your work, monitor your context, and act ahead of you — predictively and under your control.

---

## 🏗️ Architecture — 2-Calendar + Link Graph

```
┌──────────────────────┐     ┌───────────────────────────┐
│   YOUR CALENDARS     │     │  Proactive Claw — Actions  │
│   (read-only)        │────▶│  (skill-owned, visible)    │
│   N calendars        │     │  Reminders, prep, buffers  │
└──────────────────────┘     └───────────────────────────┘
         │                              │
         └──────────┬───────────────────┘
                    ▼
          ┌──────────────────┐
          │   Link Graph DB   │
          │  (SQLite)         │
          │  user_events      │
          │  action_events    │
          │  links            │
          │  suppression      │
          │  sent_actions     │
          └──────────────────┘
```

**Your calendars** are read-only — never modified. All actions are written to a single **"Proactive Claw — Actions"** calendar that you can see in your calendar app. Events are linked via a SQLite graph so actions stay in sync when source events move or are deleted.

### Daemon Cycle: PLAN → EXECUTE

Every 15 minutes:

1. **PLAN** — Ingest user events, detect deletions, auto-relink moved events, plan reminder/prep/buffer/debrief actions
2. **EXECUTE** — Fire due actions idempotently (check `sent_actions` table before sending)
3. **CLEANUP** — Once daily: rename paused/canceled events, delete old canceled entries

---

## 🔒 Security & Privacy

### ⚠️ CRITICAL: Before Installing

1. **Review setup scripts first:**
   ```bash
   cat ~/.openclaw/workspace/skills/proactive-agent/scripts/setup.sh
   cat ~/.openclaw/workspace/skills/proactive-agent/scripts/install_daemon.sh
   ```
   Both are plain shell scripts. Confirm they only write to `~/.openclaw/` and create user-level timers (not root services).

2. **Start with safe defaults:**
   - Do NOT copy `config.example.json` directly to `config.json`
   - Run `python3 config_wizard.py` for guided setup
   - OR manually create `config.json` with `max_autonomy_level: "confirm"` (not `autonomous`)
   - Ensure all `feature_*` are `false` unless you explicitly need them

3. **For credentials:**
   - Google: use standard OAuth desktop flow (setup.sh handles this)
   - Do NOT use `clawhub_token` unless you trust clawhub.ai
   - Nextcloud: generate app-specific password (never your account password)
   - All external APIs (Telegram, Notion, GitHub, LLM): only provide tokens when you enable the feature

4. **Test in dry-run mode:**
   ```bash
   python3 daemon.py --simulate --days 3  # safe preview
   python3 action_planner.py --dry-run    # see what would be planned
   python3 action_executor.py --dry-run   # see what would be executed
   ```

### Security Guarantees

| What | Detail |
|------|--------|
| **Credentials stay local** | `credentials.json`, `token.json`, `config.json` stored only in `~/.openclaw/workspace/skills/proactive-agent/`. Never uploaded anywhere. |
| **User-level daemon only** | `install_daemon.sh` creates user-level timers (launchd on macOS, systemd user service on Linux). Runs as your user only — never root. Uninstall: `launchctl unload ~/Library/LaunchAgents/ai.openclaw.proactive-agent.plist && rm ~/Library/LaunchAgents/ai.openclaw.proactive-agent.plist` (macOS) or `systemctl --user disable --now openclaw-proactive-agent.timer && rm ~/.config/systemd/user/openclaw-proactive-agent.*` (Linux) |
| **Calendar writes isolated** | Only writes to the `Proactive Claw — Actions` calendar it creates. Reads your other calendars but never modifies them. |
| **Network calls gated** | All external network calls require explicit config or feature flag. Default: Google Calendar API only (core feature). Notion, Telegram, GitHub, clawhub.ai, LLM services are all opt-in. |
| **Nextcloud password** | Use an app-specific password only. Generate at `your-nextcloud.com/settings/personal/security`. Never store your account password. |
| **Safe-by-default config** | `max_autonomy_level` defaults to `confirm` (asks before acting). All external features default to `false`. |
| **Inspect scripts** | `setup.sh` and `install_daemon.sh` are plain shell — no obfuscated downloads, no root commands. Read them before running. |
| **clawhub OAuth scope** | `clawhub_token` (optional) downloads only the OAuth client definition (`credentials.json`). Your personal Google token (`token.json`) is generated locally in your browser and never sent to clawhub.ai. |
| **LLM rater is local-first** | Defaults to Ollama on `localhost` — no API key, no data sent anywhere. Cloud backends require explicit `base_url` + `api_key_env` configuration. |
| **Link graph is local** | `proactive_links.db` stores only event UIDs, fingerprints, and link metadata. All local SQLite. |

### What data leaves your machine

| Service | When | What is sent | Gated by |
|---------|------|-------------|----------|
| Google Calendar API | Always (core feature) | Calendar event read/write requests with your OAuth token | `feature_calendar` |
| clawhub.ai | Setup only, if using clawhub OAuth path | `clawhub_token` to fetch `credentials.json` | `clawhub_token` set in config |
| Notion API (search) | Only if enabled | Event title (first 50 chars) — read only | `feature_cross_skill: true` + `NOTION_API_KEY` set |
| Notion API (write) | Only if enabled | Event title, date, sentiment, notes text | `notes_destination: notion` + `NOTION_API_KEY` + `NOTION_OUTCOMES_DB_ID` set |
| GitHub API | Only if enabled | Read-only: open PRs and issues via `gh` CLI | `feature_cross_skill: true` + `gh` CLI authenticated |
| Telegram API | Only if enabled | Notification message text | `notification_channels` includes `telegram` |
| Nextcloud CalDAV | Only if using Nextcloud backend | Calendar read/write via CalDAV | `calendar_backend: nextcloud` |
| LLM rating API | Only if enabled AND using cloud backend | Outcome notes + event title + sentiment for rating | `llm_rater.enabled: true` + non-localhost `base_url` + `LLM_RATER_API_KEY` set |

> **Local LLM = zero external calls.** With `base_url: http://localhost:11434/v1` (Ollama) or `http://localhost:1234/v1` (LM Studio), nothing leaves your machine.

**Nothing else.** No analytics, no telemetry, no data sent to the skill author.

---

## ✨ Features at a glance

| # | Feature | Description |
|---|---------|-------------|
| 1 | Conversation Radar | Score 0–10 silently after every exchange |
| 2 | Calendar Monitoring | Scan + conflict detection + actionable events |
| 3 | Background Daemon | PLAN→EXECUTE→CLEANUP cycles every 15 min |
| 4 | SQLite Memory | Outcome history with TF-IDF semantic search |
| 5 | Cross-Skill Intelligence | GitHub + Notion context (opt-in) |
| 6 | Natural Language Rules | User-defined rules engine |
| 7 | Post-Event Intelligence | Follow-ups, weekly digest, quarterly insights |
| 8 | Calendar Policy Engine | Autonomous prep/focus/buffer/debrief blocking |
| 9 | Multi-Agent Orchestration | Full pre-event preparation pipeline |
| 10 | Energy Prediction | Predictive energy scheduling with decay weighting |
| 11 | Calendar Editing | Move, find free time, clear, read in plain English |
| 12 | Relationship Memory | Lightweight CRM from attendees + outcomes |
| 13 | Voice-First | Whisper integration + intent routing |
| 14 | Adaptive Notifications | Self-tuning channel + time learning with decay |
| 15 | Team Awareness | Opt-in cross-calendar coordination |
| 16 | LLM Interaction Rater | Local model rates check-in quality |
| 17 | **Proactivity Engine** | Unified scoring: energy + notification + policy + relationship signals |
| 18 | **Interruption Governance** | Priority tiers P0–P5, max nudges/day, cooldowns |
| 19 | **Explainability Mode** | Trace every nudge/policy/energy decision |
| 20 | **Proactivity Intensity Dial** | low / balanced / executive mode |
| 21 | **Max Autonomy Cap** | advisory / confirm / autonomous global override |
| 22 | **Memory Decay** | Exponential recency weighting across all modules |
| 23 | **System Health Audit** | 7 diagnostic checks: DB, daemon, config, calendar, flags, stale, disk |
| 24 | **Policy Conflict Detection** | Pairwise detection of contradictory policies |
| 25 | **Config Wizard** | Interactive CLI setup with validation |
| 26 | **Simulation Mode** | Dry-run daemon over N future days |
| 27 | **Quiet Hours** | Suppress non-safety nudges during quiet windows |
| 28 | **Data Export/Import** | JSON/CSV backup + restore |
| 29 | **Drift Monitoring** | Monthly behaviour reports with delta alerts |
| 30 | **2-Calendar Architecture** | Read user calendars, write to Action Calendar only |
| 31 | **Link Graph** | SQLite graph connecting user events ↔ planned actions |
| 32 | **Action Planner** | PLAN phase: ingest, detect missing, auto-relink, create actions |
| 33 | **Action Executor** | EXECUTE phase: fire due actions idempotently |
| 34 | **Deletion Detection** | Fingerprint-based move detection + confirm/suppress workflow |
| 35 | **Soft-Cancel Policy** | Rename canceled events, cleanup after N days |

---

## 🛠️ Setup (run once)

```bash
bash ~/.openclaw/workspace/skills/proactive-agent/scripts/setup.sh
```

### Option A — clawhub OAuth (recommended, mobile-friendly)

1. Go to https://clawhub.ai/settings/integrations → Connect Google Calendar → copy your token
2. In `config.json` set `"clawhub_token": "your-token-here"`
3. Run `setup.sh` — credentials download automatically, no Google Cloud Console needed

### Option B — Manual Google credentials

1. https://console.cloud.google.com → New project → Enable Google Calendar API
2. Create OAuth 2.0 credentials (Desktop app) → download JSON
3. `mv ~/Downloads/credentials.json ~/.openclaw/workspace/skills/proactive-agent/credentials.json`
4. Run `setup.sh`

### Option C — Nextcloud CalDAV

```json
"calendar_backend": "nextcloud",
"nextcloud": { "url": "https://your-nextcloud.com", "username": "...", "password": "app-password" }
```
> ⚠️ Use a Nextcloud **app-specific password**, not your account password. Generate one at `your-nextcloud.com/settings/personal/security`. The password is stored locally in `config.json` on your machine only.

Run `setup.sh` — connects, creates Proactive Claw — Actions calendar, saves URL.

### Install background daemon

```bash
bash ~/.openclaw/workspace/skills/proactive-agent/scripts/install_daemon.sh
```

- **macOS**: installs launchd plist, runs every 15 min automatically
- **Linux**: installs systemd user timer
- Logs: `~/.openclaw/workspace/skills/proactive-agent/daemon.log`

### Migrate existing outcomes to SQLite

```bash
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/memory.py --import-outcomes
```

### Interactive config wizard (optional)

```bash
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/config_wizard.py
```

---

## ⚙️ Configuration

`~/.openclaw/workspace/skills/proactive-agent/config.json`

Edit this file directly to change settings. Only modify values in the right-hand column — do not change keys or structure.

| Key | Default | Description |
|-----|---------|-------------|
| `calendar_backend` | `google` | `google`, `nextcloud` |
| `timezone` | `UTC` | IANA tz e.g. `Europe/Berlin` |
| `daemon_interval_minutes` | `15` | How often daemon scans |
| `proactivity_mode` | `balanced` | `low`, `balanced`, `executive` — controls scoring multiplier + max nudges |
| `max_autonomy_level` | `autonomous` | `advisory` (suggest only), `confirm` (ask first), `autonomous` (act) |
| `quiet_hours` | `{"weekdays":"22:00-07:00","weekends":"21:00-09:00"}` | Suppress non-safety nudges during these windows |
| `memory_decay_half_life_days` | `90` | Half-life for exponential decay weighting |
| `max_nudges_per_day` | `12` | Hard cap on daily nudges |
| `nudge_cooldown_minutes` | `30` | Minimum gap after a dismissed nudge |
| `watched_calendars` | `[]` | Calendar IDs to watch (empty = all except action calendar) |
| `ignored_calendars` | `[]` | Calendar IDs to ignore |
| `action_cleanup_days` | `30` | Days before canceled action events are deleted |
| `notification_channels` | `["openclaw","system"]` | `openclaw`, `system`, `telegram` |
| `telegram.bot_token` | `""` | Telegram bot token |
| `telegram.chat_id` | `""` | Your Telegram chat ID |
| `clawhub_token` | `""` | Token from clawhub.ai/settings/integrations |
| `notes_destination` | `local` | `local`, `apple-notes` (macOS osascript), `notion` |

### Feature Flags

All local features default ON. External-facing features default OFF.

| Flag | Default | Description |
|------|---------|-------------|
| `feature_conversation` | `true` | Conversation radar scoring |
| `feature_calendar` | `true` | Calendar scanning |
| `feature_daemon` | `true` | Background daemon |
| `feature_memory` | `true` | SQLite memory |
| `feature_conflicts` | `true` | Conflict detection |
| `feature_rules` | `true` | Rules engine |
| `feature_intelligence_loop` | `true` | Follow-ups + digest |
| `feature_policy_engine` | `true` | Calendar policies |
| `feature_orchestrator` | `true` | Multi-agent orchestration |
| `feature_energy` | `true` | Energy prediction |
| `feature_cal_editor` | `true` | Calendar editing |
| `feature_relationship` | `true` | Relationship CRM |
| `feature_adaptive_notifications` | `true` | Self-tuning notifications |
| `feature_proactivity_engine` | `true` | Unified proactivity scoring |
| `feature_interrupt_controller` | `true` | Interruption governance |
| `feature_explainability` | `true` | Decision trace |
| `feature_health_check` | `true` | System diagnostics |
| `feature_simulation` | `true` | Simulation mode |
| `feature_export` | `true` | Data export/import |
| `feature_behaviour_report` | `true` | Drift monitoring |
| `feature_config_wizard` | `true` | Config wizard |
| `feature_policy_conflict_detection` | `true` | Policy conflict alerts |
| `feature_cross_skill` | **`false`** | GitHub/Notion context (external) |
| `feature_voice` | **`false`** | Voice (requires whisper skill) |
| `feature_team_awareness` | **`false`** | Team cross-calendar (external) |
| `feature_llm_rater` | **`false`** | LLM rater (external if cloud) |

### LLM Rater Config

| Key | Default | Description |
|-----|---------|-------------|
| `llm_rater.enabled` | `false` | Enable the rater |
| `llm_rater.base_url` | `http://localhost:11434/v1` | LLM endpoint (Ollama default — local, no key needed) |
| `llm_rater.model` | `qwen2.5:3b` | Model name |
| `llm_rater.api_key_env` | `""` | Env var name holding API key (empty = no key, for local) |
| `llm_rater.timeout` | `30` | Request timeout in seconds |

---

## Feature 1 — Conversation Radar

Score 0–10 silently after every exchange. Ask once, briefly, at threshold.

| +Points | Signal |
|---------|--------|
| +3 | Explicit future event |
| +3 | Active preparation language |
| +2 | Importance / stress markers |
| +2 | Hard deadline |
| +1 | Recurring obligation |
| +1 | Post-event reflection |
| −2 | Hypothetical or historical |

**Before asking**, check pending nudges from daemon:
```bash
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/cross_skill.py --pending-nudges
```
If nudges exist, surface the most urgent one first instead of a new ask.

---

## Feature 2 — Calendar Monitoring + Conflict Detection

### Scan
```bash
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/scan_calendar.py
```
Cache-aware (TTL from config). Returns `actionable` list pre-filtered to threshold + not snoozed.

### Library function (used by action_planner)
```python
from scan_calendar import scan_user_events
events = scan_user_events(config, backend, now, time_max)
```
Scans only user calendars (excludes action calendar). Respects `watched_calendars` and `ignored_calendars`.

### Conflict detection
```bash
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/scan_calendar.py | \
  python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/conflict_detector.py
```

Detects: **Overlaps**, **Overloaded days** (4+ events), **Back-to-back runs** (3+ with <10 min gaps).

---

## Feature 3 — Background Daemon + Conversation Mode

### Background Daemon (PLAN → EXECUTE) — Automatic

Runs every 15 minutes (after `install_daemon.sh`):

**Phase 1 — PLAN** (`action_planner.py`):
- Ingest user events into link graph
- Detect missing events (deletion/move detection)
- Auto-relink moved events via fingerprint matching
- Create confirm_delete actions after 2 consecutive misses
- Plan reminder, prep, buffer, and debrief actions

**Phase 2 — EXECUTE** (`action_executor.py`):
- Fire only due actions from the action calendar
- Idempotency: check `sent_actions` table before sending
- Skip paused/canceled/suppressed actions

**Phase 3 — Legacy** (backward compatible):
- Conflict detection + notifications
- Follow-up nudges
- Policy evaluation

**Phase 4 — CLEANUP** (once daily via `action_cleanup.py`):
- Rename paused events to `🦞 [Paused] ...`
- Rename canceled events to `🦞 [Canceled] ...`
- Delete canceled entries older than `action_cleanup_days`

**Legacy fallback**: If `action_planner` fails, falls back to the v1.1.x scan→notify flow automatically.

```bash
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/daemon.py --status
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/daemon.py --simulate --days 7
```

**Notification channels**: `openclaw` (pending_nudges.json), `system` (desktop via osascript on macOS / notify-send on Linux), `telegram` (optional)

### Conversation Mode (Optional) — Manual, Per-Request

Claude Code can optionally call proactive-claw scripts during conversations to:
- **Read context**: `scan_calendar.py --read` to check your schedule
- **Propose changes**: `cal_editor.py --move` or `--find-free` with your approval
- **Log outcomes**: `capture_outcome.py` after events
- **Check policies**: `policy_engine.py --evaluate` to show what automation would trigger

**This is NOT automatic.** Each call requires:
1. You enable it in conversation (e.g., "Check my calendar")
2. Claude Code shows you the proposed action
3. You approve before it executes
4. `max_autonomy_level: confirm` enforces this (default in safe config)

If you set `max_autonomy_level: advisory`, Claude Code can only suggest actions, never execute them.
If you set `max_autonomy_level: autonomous`, Claude Code can act without asking (NOT recommended).

---

## Feature 4 — SQLite Memory + Semantic Search

```bash
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/memory.py \
  --save '{"event_title":"Demo","sentiment":"positive","follow_up_needed":true}'

python3 memory.py --search "times I felt underprepared"
python3 memory.py --open-actions
python3 memory.py --summary --days 90
```

Memory now uses **decay-weighted averages** — recent outcomes count more than old ones. Configurable via `memory_decay_half_life_days`.

---

## Feature 5 — Cross-Skill Intelligence

**Scope clarification:** `cross_skill.py` does NOT read other skills' tokens, config files, or stored data. It only:
1. Checks whether specific skills are installed by testing if their `SKILL.md` file exists on disk
2. If the `github` skill is present AND `gh` CLI is authenticated: runs `gh pr list` and `gh issue list` (read-only, using your existing gh CLI auth)
3. If the `notion` skill is present AND `NOTION_API_KEY` env var is set: searches Notion for pages matching the event title

No other skills' data, secrets, or context is accessed. `feature_cross_skill` defaults to `false`.

```bash
python3 ~/.openclaw/workspace/skills/proactive-agent/scripts/cross_skill.py \
  --event-title "Sprint Review" --event-type "one_off_high_stakes"
python3 cross_skill.py --list-available
```

---

## Feature 6 — Natural Language Rules

```bash
python3 rules_engine.py --parse "Never bother me about standups unless I haven't spoken in 2 weeks"
python3 rules_engine.py --parse "Always prep me 2 days before anything with the word board"
python3 rules_engine.py --list
```

---

## Feature 7 — Post-Event Intelligence Loop

```bash
python3 intelligence_loop.py --weekly-digest
python3 intelligence_loop.py --check-followups
python3 intelligence_loop.py --create-followups
python3 intelligence_loop.py --summary --days 90
```

---

## Feature 8 — Autonomous Calendar Policy Engine

Parse and execute natural language calendar policies autonomously:

```bash
python3 policy_engine.py --parse "Always block 1 hour of prep time before board meetings"
python3 policy_engine.py --parse "Add 15 min buffer after back-to-back meetings"
python3 policy_engine.py --parse "Block focus time every Tuesday morning"
python3 policy_engine.py --parse "Always schedule a debrief 30 min after investor calls"
python3 policy_engine.py --evaluate   # run all policies against current calendar
python3 policy_engine.py --list
python3 policy_engine.py --delete <id>
```

Now respects `max_autonomy_level`:
- `advisory` → suggests actions but never executes
- `confirm` → presents action for user approval
- `autonomous` → executes immediately (original behavior)

---

## Feature 9 — Multi-Agent Orchestration

```bash
python3 orchestrator.py --event-id <id> --event-title "Sprint Review" \
  --event-type one_off_high_stakes --event-datetime 2025-03-15T10:00:00
python3 orchestrator.py --dry-run ...
```

Pipeline: open action items → cross-skill context → outcome patterns → prep block → draft email → Notion notes → enriched nudge.

---

## Feature 10 — Predictive Energy Scheduling

Now uses **decay-weighted scoring** — recent energy data counts more than old data.

```bash
python3 energy_predictor.py --analyse
python3 energy_predictor.py --suggest-focus-time
python3 energy_predictor.py --check "2025-03-15T09:00:00" one_off_high_stakes
python3 energy_predictor.py --block-focus-week
```

---

## Feature 11 — Natural Language Calendar Editing

```bash
python3 cal_editor.py --move "Sprint Review" "next Monday 2pm"
python3 cal_editor.py --find-free "tomorrow" --duration 60
python3 cal_editor.py --clear "this Friday afternoon"   # OpenClaw events only (safe)
python3 cal_editor.py --read "this week"
python3 cal_editor.py --reschedule-conflict
```

---

## Feature 12 — Relationship Memory

```bash
python3 relationship_memory.py --ingest
python3 relationship_memory.py --lookup "Alice"
python3 relationship_memory.py --brief "Sprint Review"
python3 relationship_memory.py --stale --days 30
python3 relationship_memory.py --top
python3 relationship_memory.py --add-note alice@example.com "Prefers async updates"
```

---

## Feature 13 — Voice-First Interaction

```bash
python3 voice_bridge.py --check-whisper
python3 voice_bridge.py --record --seconds 10
python3 voice_bridge.py --transcribe /path/audio.wav
python3 voice_bridge.py --route "move sprint review to next Monday"
```

Backends: OpenClaw `whisper` skill → `openai-whisper` package → `whisper` CLI.

---

## Feature 14 — Adaptive Notification Intelligence

Now uses **decay-weighted response scoring** — recent response patterns count more.

```bash
python3 adaptive_notifications.py --record-response <nudge_id> opened \
  --event-type one_off_high_stakes --channel system --sent-at 2025-03-15T09:00:00
python3 adaptive_notifications.py --get-channel "one_off_high_stakes"
python3 adaptive_notifications.py --get-timing "Monday"
python3 adaptive_notifications.py --analyse
```

---

## Feature 15 — Team Awareness

Opt-in cross-calendar coordination. All sharing is explicit — nothing automatic:

```bash
python3 team_awareness.py --add-member alice@example.com "Alice"
python3 team_awareness.py --availability "this week"
python3 team_awareness.py --meeting-time "Sprint Review" --attendees "alice@example.com,bob@example.com"
```

---

## Feature 16 — LLM Interaction Rater

Local-first quality rating. Defaults to Ollama — no cloud account needed.

```bash
python3 llm_rater.py --outcome-file <path>
python3 llm_rater.py --check-backend
python3 llm_rater.py --list-backends
```

---

## Feature 17 — Proactivity Engine 🆕

Unified scoring core that merges 5 signal sources into a single proactivity score per event:

```bash
python3 proactivity_engine.py --score <scan_json>
python3 proactivity_engine.py --score-event <event_json>
python3 proactivity_engine.py --history <event_id>
```

**Signals merged**: energy_delta, notification_delta, policy_delta, relationship_delta + base score. Applies `proactivity_mode` multiplier (low=0.5, balanced=1.0, executive=1.3). Stores in `proactivity_scores` SQLite table.

**Local only** — no network calls, no subprocess spawning. Reads from local SQLite databases only.

---

## Feature 18 — Interruption Governance 🆕

Priority-based nudge filtering with enforcement of daily limits, cooldowns, and quiet hours:

```bash
python3 interrupt_controller.py --filter <scan_json>
python3 interrupt_controller.py --status
python3 interrupt_controller.py --record-dismissal <event_id>
python3 interrupt_controller.py --quiet-hours-check
```

**Priority tiers**:
| Tier | Category | Example |
|------|----------|---------|
| P0 | Safety | Conflicts, double-books |
| P1 | High-stakes prep | < 24h to important event |
| P2 | Policy-triggered | Auto-blocked prep/focus time |
| P3 | Follow-up | Stale action items |
| P4 | Routine | Periodic check-ins |
| P5 | Informational | Digests, stats |

**Mode limits**: low=3, balanced=6, executive=12 top-N nudges per session.

**Local only** — no network calls, no subprocess spawning.

---

## Feature 19 — Explainability Mode 🆕

Trace every decision the system makes:

```bash
python3 explain.py --explain-nudge <event_id>
python3 explain.py --explain-policy <policy_id>
python3 explain.py --explain-energy-decision <event_id>
python3 explain.py --trace <event_id>   # full decision trace
```

Shows all signal contributions, priority classification, suppression reasons, and scoring breakdowns.

**Local only** — reads from local SQLite databases only.

---

## Feature 20 — Proactivity Intensity Dial 🆕

Global mode that controls scoring multiplier and nudge limits:

| Mode | Score Multiplier | Max Nudges/Session |
|------|-----------------|-------------------|
| `low` | 0.5 (non-high-stakes) | 3 |
| `balanced` | 1.0 | 6 |
| `executive` | 1.3 | 12 |

Set in config: `"proactivity_mode": "balanced"`

---

## Feature 21 — Max Autonomy Cap 🆕

Global override that limits what the system can do without asking:

| Level | Behavior |
|-------|----------|
| `advisory` | Suggest only — never create/modify events |
| `confirm` | Present action for approval before executing |
| `autonomous` | Act immediately (default) |

Set in config: `"max_autonomy_level": "autonomous"`

---

## Feature 22 — Memory Decay 🆕

Exponential recency weighting across all modules. Recent data gets higher weight, old data fades.

Used by: `energy_predictor.py`, `adaptive_notifications.py`, `memory.py`, `proactivity_engine.py`

Config: `"memory_decay_half_life_days": 90`

Shared library: `scripts/decay.py` — pure math, no I/O, no network, no subprocess.

---

## Feature 23 — System Health Audit 🆕

7 diagnostic checks in one command:

```bash
python3 health_check.py                    # full report
python3 health_check.py --check db         # database integrity
python3 health_check.py --check daemon     # is daemon running?
python3 health_check.py --check config     # config validity
python3 health_check.py --check calendar   # calendar connectivity
python3 health_check.py --check flags      # feature flag consistency
python3 health_check.py --check stale      # stale data detection
python3 health_check.py --check disk       # disk usage
```

**Note**: The `daemon` check uses `subprocess` to run `launchctl list` (macOS) or `systemctl --user status` (Linux) — local process inspection only, no network calls. The `calendar` check uses the calendar backend to verify connectivity (same network scope as core calendar features).

---

## Feature 24 — Policy Conflict Detection 🆕

Detects contradictory policies before they cause issues:

```bash
python3 policy_conflict_detector.py --check-all
python3 policy_conflict_detector.py --check-new '<policy_json>'
```

Detects: overlapping conditions with conflicting actions, autonomy mismatches, duplicate policies.

**Local only** — reads from local SQLite only.

---

## Feature 25 — Config Wizard 🆕

Interactive CLI setup:

```bash
python3 config_wizard.py                   # interactive mode
python3 config_wizard.py --defaults        # non-interactive, safe defaults
python3 config_wizard.py --validate        # check existing config
```

Detects system timezone, walks through backend/mode/autonomy/channels/quiet-hours. Writes `config.json` only.

---

## Feature 26 — Simulation Mode 🆕

Dry-run the daemon over N future days to see what would fire:

```bash
python3 daemon.py --simulate --days 7
```

All state in-memory only — no writes to DB, calendar, or files.

---

## Feature 27 — Quiet Hours 🆕

Suppress non-P0 (non-safety) nudges during configured quiet windows:

```json
"quiet_hours": { "weekdays": "22:00-07:00", "weekends": "21:00-09:00" }
```

P0 (safety) nudges like double-bookings still come through. Implemented in `interrupt_controller.py`.

---

## Feature 28 — Data Export/Import 🆕

Backup and restore all data:

```bash
python3 export_data.py --export --output ~/backup --format json
python3 export_data.py --export --output ~/backup --format csv
python3 export_data.py --import ~/backup
python3 export_data.py --list-tables
```

Exports all SQLite tables + redacted config (secrets stripped). Import uses `INSERT OR REPLACE`.

**Local only** — reads/writes local files only.

---

## Feature 29 — Drift Monitoring 🆕

Monthly behaviour reports that detect concerning trends:

```bash
python3 behaviour_report.py --monthly
python3 behaviour_report.py --snapshot
python3 behaviour_report.py --compare "2025-01" "2025-02"
python3 behaviour_report.py --drift-alert
```

Alerts when: dismiss rate increases >20%, prep rate drops >15%, negative sentiment rises >15%.

**Local only** — reads from local SQLite only.

---

## Feature 30 — 2-Calendar Architecture 🆕

Your calendars are **read-only**. All actions are written to the **"Proactive Claw — Actions"** calendar.

- `watched_calendars: []` — which calendars to monitor (empty = all except action calendar)
- `ignored_calendars: []` — calendars to skip entirely
- Action calendar is identified by `openclaw_cal_id` in config (created by `setup.sh`)

**Migration**: `setup.sh` checks for both old name ("OpenClaw") and new name ("Proactive Claw — Actions") — existing setups migrate automatically.

---

## Feature 31 — Link Graph 🆕

SQLite database (`proactive_links.db`) with 5 tables:

| Table | Purpose |
|-------|---------|
| `user_events` | Tracked user events with fingerprint + missing_count |
| `action_events` | Planned actions (reminder, prep, buffer, debrief, confirm_delete) |
| `links` | Connects user_events ↔ action_events with relationship type |
| `suppression` | Events the user said "don't ask me about this" |
| `sent_actions` | Idempotency log: action_uid + due_ts = unique key |

```bash
python3 link_store.py --status      # graph stats
python3 link_store.py --missing     # events with missing_count > 0
python3 link_store.py --links <uid> # show all linked actions for a user event
```

**Fingerprint**: SHA256 of normalized `title|start|end|attendees|location` — detects moved/recreated events.

**Local only** — SQLite only, no network calls.

---

## Feature 32 — Action Planner (PLAN Phase) 🆕

The PLAN phase of the daemon cycle:

```bash
python3 action_planner.py --plan        # full plan cycle
python3 action_planner.py --dry-run     # show what would be planned
python3 action_planner.py --status      # show plan stats
```

Steps:
1. **Ingest**: Upsert all seen user events, reset missing_count
2. **Detect missing**: Mark unseen events, increment missing_count, pause linked actions
3. **Auto-relink**: Check fingerprint/title match for moved events
4. **Confirm delete**: After ≥2 consecutive misses, create confirm_delete action
5. **Plan actions**: Create reminder, prep, buffer, debrief actions based on policies

**Local only** — reads calendar via scan_calendar library function (same network scope as core), writes to local SQLite only.

---

## Feature 33 — Action Executor (EXECUTE Phase) 🆕

The EXECUTE phase of the daemon cycle:

```bash
python3 action_executor.py --execute    # fire due actions
python3 action_executor.py --dry-run    # show what would fire
python3 action_executor.py --due        # list due actions
```

- Idempotent: checks `sent_actions` table before sending
- Skips paused/canceled/suppressed actions
- Default lookahead: 20 minutes (> daemon interval of 15 min)
- Sends notifications via daemon's `send_notification()` function

**Note**: Notification delivery uses the same channels as the daemon (system/osascript, Telegram, pending_nudges.json).

---

## Feature 34 — Deletion Detection 🆕

When a user event disappears from the calendar:

1. **First miss**: `missing_count` incremented, linked actions paused
2. **Auto-relink attempt**: Checks fingerprint match (moved event) or title+near-time match
3. **Second miss**: Creates `confirm_delete` action with 3 options:
   - **Yes** → mark deleted, cancel all linked actions
   - **No** → 24h cooldown, expanded recovery scan (180 days)
   - **Don't ask** → suppress event permanently

```bash
python3 confirm_delete.py --yes <user_event_uid>
python3 confirm_delete.py --no <user_event_uid>
python3 confirm_delete.py --dont-ask <user_event_uid>
```

**Local only** — reads/writes local SQLite only.

---

## Feature 35 — Soft-Cancel Policy 🆕

Canceled action events aren't deleted immediately — they're renamed so users can see what happened:

- Paused → `🦞 [Paused] Original Title`
- Canceled → `🦞 [Canceled] Original Title`
- Cleanup: entries older than `action_cleanup_days` (default 30) are permanently deleted

```bash
python3 action_cleanup.py --cleanup             # run cleanup cycle
python3 action_cleanup.py --cleanup --dry-run   # show what would be cleaned
python3 action_cleanup.py --status              # show cleanup stats
```

**Note**: Cleanup writes to the action calendar only (rename/delete action events). Uses the same calendar backend as core features.

---

## PC_ACTION Metadata Encoding

Action calendar events include a machine-readable marker in the description for cross-backend compatibility:

```
PC_ACTION: {"action_event_uid":"abc123","action_type":"reminder","source_event_uid":"def456","status":"active"}
```

This allows the system to track which action events belong to which user events, even when using CalDAV backends that don't support custom properties.

```bash
# Codec utility (library only, used by action_planner and action_executor)
python3 -c "from action_codec import decode_action_description; print(decode_action_description('...'))"
```

**Local only** — pure string encoding/decoding, no I/O.

---

## Recurring Event Intelligence

| Type | Detection | Behaviour |
|------|-----------|-----------|
| `routine_low_stakes` | Recurring + internal + avg 0 action items | Suppress. Every 4th occurrence only. |
| `routine_high_stakes` | Recurring + external OR avg ≥ 2 action items | Always check in, personalise with history. |
| `one_off_standard` | Not recurring, < 60 min, internal | Standard scoring. |
| `one_off_high_stakes` | Not recurring + external OR importance signals | Max prep. Full orchestration pipeline. |

---

## Auto Agenda & Talking Points

| Event type | Auto-generated content |
|-----------|----------------------|
| Presentation / Demo | Hook → Problem → Solution → Demo → CTA |
| Interview | STAR prompts for role/company if mentioned |
| 1:1 | Open action items + relationship brief |
| Standup | GitHub activity from cross_skill.py |
| Board / Investor | Metrics, narrative arc, likely hard questions |
| Workshop | Desired outcomes, pre-reads |
| External (no history) | Company/attendee context + relationship brief |

---

## Error Handling

| Error | User message |
|-------|-------------|
| `calendar_backend_unavailable` | "Can't reach your calendar. Try again, or continue without calendar features?" |
| `failed_to_list_calendars` | "Trouble reading calendars. Check connection and that setup.sh ran." |
| `failed_to_create_events` | "Couldn't create check-in events — [detail]. Try again?" |
| Setup not run | "Calendar not set up yet. Run: `bash ~/.openclaw/workspace/skills/proactive-agent/scripts/setup.sh`" |
| `python_version_too_old` | "Python 3.8+ required. Install at https://www.python.org/downloads/" |
| Daemon not installed | "Background notifications are off. Run install_daemon.sh to enable." |
| Voice backend missing | "No transcription backend found. Run: `pip install openai-whisper`" |
| Team calendar not accessible | "Alice's calendar isn't accessible. Ask her to share it with your Google account." |
| `action_planner_failed` | Falls back to v1.1.x scan→notify flow automatically. |
| `link_graph_unavailable` | "Link graph database unavailable. Actions may not be tracked." |

---

## 📋 Script Audit — Full Inventory

### Network and subprocess behavior per script

All new v1.2.0 scripts are **local-only** unless noted otherwise.

| Script | Network | Subprocess | Notes |
|--------|---------|------------|-------|
| `scan_calendar.py` | Google/Nextcloud API | None | Core calendar read |
| `conflict_detector.py` | None | None | Local analysis |
| `daemon.py` | Google/Nextcloud API, Telegram (opt-in) | `osascript` (macOS notifications), `notify-send` (Linux) | Core daemon loop |
| `memory.py` | None | None | Local SQLite |
| `capture_outcome.py` | Notion API (opt-in) | `osascript` (Apple Notes, opt-in) | Outcome storage |
| `cross_skill.py` | Notion API (opt-in), GitHub via `gh` CLI (opt-in) | `gh pr list`, `gh issue list` (opt-in) | External context |
| `rules_engine.py` | None | None | Local SQLite |
| `intelligence_loop.py` | None | `python3` (calls scan/conflict scripts) | Local orchestration |
| `policy_engine.py` | Google/Nextcloud API (creates events) | None | Calendar writes to action calendar only |
| `orchestrator.py` | None | `python3` (calls sub-scripts) | Local orchestration |
| `energy_predictor.py` | Google/Nextcloud API (creates focus blocks) | None | Calendar writes to action calendar only |
| `cal_editor.py` | Google/Nextcloud API | `python3` (calls scan/conflict) | Calendar read/write |
| `relationship_memory.py` | None | None | Local SQLite |
| `voice_bridge.py` | None | `whisper`, `sox`, `arecord`/`afrecord` | Local audio processing |
| `adaptive_notifications.py` | None | None | Local SQLite |
| `team_awareness.py` | Google/Nextcloud API (reads shared calendars) | None | Opt-in team features |
| `llm_rater.py` | LLM API (local Ollama default, cloud opt-in) | None | Rating endpoint |
| `cal_backend.py` | Google/Nextcloud API | None | Calendar abstraction layer |
| `setup.sh` | clawhub.ai (opt-in), Google OAuth, Nextcloud | `pip3 install` | One-time setup |
| `install_daemon.sh` | None | `launchctl`/`systemctl` | One-time daemon install |
| **`decay.py`** 🆕 | None | None | Pure math library |
| **`proactivity_engine.py`** 🆕 | None | None | Local SQLite scoring |
| **`interrupt_controller.py`** 🆕 | None | None | Local SQLite nudge filter |
| **`explain.py`** 🆕 | None | None | Local SQLite trace |
| **`health_check.py`** 🆕 | Calendar API (connectivity check) | `launchctl`/`systemctl` (daemon check) | Diagnostic tool |
| **`policy_conflict_detector.py`** 🆕 | None | None | Local SQLite |
| **`config_wizard.py`** 🆕 | None | None | Interactive CLI, writes config.json |
| **`export_data.py`** 🆕 | None | None | Local file I/O |
| **`behaviour_report.py`** 🆕 | None | None | Local SQLite |
| **`link_store.py`** 🆕 | None | None | Local SQLite (proactive_links.db) |
| **`action_codec.py`** 🆕 | None | None | Pure string encoding |
| **`action_planner.py`** 🆕 | Via scan_calendar (Google/Nextcloud API) | None | PLAN phase |
| **`action_executor.py`** 🆕 | Via daemon send_notification (system/Telegram) | None | EXECUTE phase |
| **`confirm_delete.py`** 🆕 | None | None | Local SQLite |
| **`action_cleanup.py`** 🆕 | Via cal_backend (Google/Nextcloud API) | None | Calendar event rename/delete |

### scripts/install_daemon.sh — complete source

This script does exactly four things:
1. Detects macOS or Linux
2. Writes a plist file to `~/Library/LaunchAgents/` (macOS) or a `.service` + `.timer` file to `~/.config/systemd/user/` (Linux) — **user directory, not system**
3. Registers the timer with `launchctl load` (macOS) or `systemctl --user enable` (Linux)
4. Prints status and uninstall instructions

No `sudo`. No root. No downloads. No curl/wget. No network calls. Writes only to your home directory.

```bash
#!/bin/bash
# install_daemon.sh — Install proactive-agent as a background daemon
# Supports: macOS (launchd) | Linux (systemd user service)
# Run once after setup.sh

set -e

SKILL_DIR="$HOME/.openclaw/workspace/skills/proactive-agent"
PYTHON=$(command -v python3)
PLATFORM=$(uname -s)

if [ "$PLATFORM" = "Darwin" ]; then
  PLIST_DIR="$HOME/Library/LaunchAgents"
  PLIST="$PLIST_DIR/ai.openclaw.proactive-agent.plist"
  mkdir -p "$PLIST_DIR"
  cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>         <string>ai.openclaw.proactive-agent</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$SKILL_DIR/scripts/daemon.py</string>
  </array>
  <key>StartInterval</key> <integer>900</integer>
  <key>RunAtLoad</key>     <true/>
  <key>StandardOutPath</key>  <string>$SKILL_DIR/daemon.log</string>
  <key>StandardErrorPath</key><string>$SKILL_DIR/daemon.log</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>HOME</key> <string>$HOME</string>
    <key>PATH</key> <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
  </dict>
  <key>WorkingDirectory</key> <string>$SKILL_DIR</string>
</dict>
</plist>
EOF
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST"

elif [ "$PLATFORM" = "Linux" ]; then
  SERVICE_DIR="$HOME/.config/systemd/user"
  mkdir -p "$SERVICE_DIR"
  cat > "$SERVICE_DIR/openclaw-proactive-agent.service" << EOF
[Unit]
Description=OpenClaw Proactive Agent
After=network.target
[Service]
Type=oneshot
ExecStart=$PYTHON $SKILL_DIR/scripts/daemon.py
StandardOutput=append:$SKILL_DIR/daemon.log
StandardError=append:$SKILL_DIR/daemon.log
Environment=HOME=$HOME
EOF
  cat > "$SERVICE_DIR/openclaw-proactive-agent.timer" << EOF
[Unit]
Description=Run OpenClaw Proactive Agent every 15 minutes
[Timer]
OnBootSec=2min
OnUnitActiveSec=15min
Unit=openclaw-proactive-agent.service
[Install]
WantedBy=timers.target
EOF
  systemctl --user daemon-reload
  systemctl --user enable --now openclaw-proactive-agent.timer
else
  echo "Platform not supported. Run manually: python3 $SKILL_DIR/scripts/daemon.py --loop"
fi
```

**Uninstall:**
- macOS: `launchctl unload ~/Library/LaunchAgents/ai.openclaw.proactive-agent.plist && rm ~/Library/LaunchAgents/ai.openclaw.proactive-agent.plist`
- Linux: `systemctl --user disable --now openclaw-proactive-agent.timer && rm ~/.config/systemd/user/openclaw-proactive-agent.*`

---

### scripts/setup.sh — what each block does

| Step | What it does | Network? |
|------|-------------|----------|
| 1 | Checks Python 3.8+ is installed | No |
| 2 | Reads `calendar_backend` from config.json (defaults to `google`) | No |
| 3 | **If** `clawhub_token` is set AND `credentials.json` doesn't exist: fetches OAuth config from `clawhub.ai/api/oauth/google-calendar-credentials` | One HTTPS GET to clawhub.ai, optional |
| 4 | Creates default `config.json` if it doesn't exist | No |
| 5 | Creates `outcomes/` directory | No |
| **Nextcloud path** | `pip3 install caldav icalendar`; connects to Nextcloud; creates "Proactive Claw — Actions" calendar if missing | HTTPS to your own Nextcloud only |
| **Google path** | `pip3 install google-api-python-client google-auth-oauthlib google-auth-httplib2`; OAuth flow; creates "Proactive Claw — Actions" calendar | HTTPS to Google OAuth + Calendar API only |

No curl/wget. No arbitrary downloads. No root. No system file modifications. No data sent to skill author.

---

## 🗃️ SQLite Tables

### memory.db (existing)

| Table | Purpose |
|-------|---------|
| `outcomes` | Event outcomes with sentiment, action items, notes |
| `rules` | User-defined natural language rules |
| `policies` | Calendar automation policies |
| `contacts` | Relationship memory CRM |
| `notification_log` | Adaptive notification tracking |
| `energy_scores` | Energy prediction data |
| `proactivity_scores` | Unified proactivity scoring |
| `nudge_log` | Interruption governance tracking |
| `policy_conflicts` | Detected policy contradictions |
| `behaviour_snapshots` | Monthly drift monitoring data |

### proactive_links.db (new in v1.2.0)

| Table | Purpose |
|-------|---------|
| `user_events` | Tracked user events with fingerprint + missing_count |
| `action_events` | Planned actions with type, status, due_ts |
| `links` | User event ↔ action event connections |
| `suppression` | Events user said "don't ask about" |
| `sent_actions` | Idempotency log for action execution |

---

## Tone & Rules

- **One question at a time.** Never stack asks.
- **Daemon nudges first** — check pending_nudges before starting new asks at conversation open.
- **Never repeat** the same event ask twice in one conversation.
- **Always confirm** before writing calendar events (title, date, friendly time + tz).
- **Always confirm** before clearing or moving events — show what will change first.
- **Always confirm** before writing outcome notes (bullet summary).
- **Respect "no"** — dismissed forever; "not now" snoozed.
- **Be brief** — check-in prompts ≤ 2 sentences. Agenda = starting point.
- **Surface, don't overwhelm** — multiple actionable items → highest-scored first.
- **Timezone-aware** — always display in user's `timezone` config, never UTC.
- **Privacy first** — team calendar features are opt-in, never auto-enroll anyone.
- The Action calendar is internal — never tell users to look at it directly.
- **Respect autonomy cap** — if `max_autonomy_level` is `advisory`, never create events.
- **Respect quiet hours** — no non-safety nudges during configured quiet windows.
