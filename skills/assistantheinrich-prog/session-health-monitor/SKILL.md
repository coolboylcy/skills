---
name: session-health-monitor
description: Context window health monitoring with compaction detection, pre-compaction snapshots, and memory rotation for Claude Code sessions.
allowed-tools:
  - Bash
  - Read
  - Write
version: 1.0.0
author: heinrichclawdster
---

# Session Health Monitor

Monitor your Claude Code context window health, detect compactions, save critical facts before they're lost, and keep your memory directory clean.

## Overview

Four capabilities, fully standalone (no OpenClaw required):

1. **StatusLine Display** — Color-coded context window usage in your Claude Code status bar
2. **Compaction Detection** — Infers when context was compacted by tracking usage drops
3. **Pre-Compaction Snapshots** — Save key facts and decisions to daily memory files
4. **Memory Rotation** — Archive old daily memory files to prevent clutter

## Quick Setup

```bash
bash scripts/setup-statusline.sh
```

That's it. Restart Claude Code and the statusline appears.

For snapshot and rotation, the scripts work standalone — call them from your agent loops or manually.

## Context Health Thresholds

| Level  | Condition                              | Action                        |
|--------|----------------------------------------|-------------------------------|
| GREEN  | <50% used AND 0 compactions            | Normal operation              |
| YELLOW | >=50% used OR >=1 compaction           | Consider saving key facts     |
| RED    | >=75% used OR >=2 compactions          | Save facts NOW, session ending|

## StatusLine Display

The statusline shows a color-coded indicator:

```
42% Context | 0x compact     # GREEN — all good
63% Context | 1x compact     # YELLOW — getting warm
81% Context | 2x compact     # RED — save facts immediately
```

Colors use ANSI codes compatible with Claude Code's terminal rendering.

## Pre-Compaction Snapshot Protocol

**When context reaches YELLOW or above, the agent SHOULD:**

1. Extract 3-5 key facts from the current session (decisions made, files changed, blockers found)
2. Write them to `memory/YYYY-MM-DD.md` using `scripts/snapshot.sh`
3. Include any unfinished work or next steps
4. Do this BEFORE the session ends or context is compacted

**Example snapshot content:**
```markdown
## Pre-Compaction Snapshot (14:32)
- Refactored auth module to use JWT instead of sessions (files: src/auth.ts, src/middleware.ts)
- Bug found in rate limiter: counter resets on deploy, not on TTL expiry
- Next: write tests for new auth flow, fix rate limiter reset logic
- Decision: using RS256 for JWT signing (user preference)
```

**When to trigger:**
- Context hits 50%+ for the first time in a session
- After any detected compaction
- Before ending a long session
- When the agent detects it has accumulated significant context

## Scripts Reference

### statusline.sh
Reads Claude Code statusline JSON from stdin and outputs formatted context info.

```bash
# Called automatically by Claude Code via settings.local.json
# Manual test:
echo '{"context_window":{"used_percentage":42},"session_id":"test-123"}' | bash scripts/statusline.sh
```

### setup-statusline.sh
One-command installer. Copies the statusline script and patches Claude Code settings.

```bash
bash scripts/setup-statusline.sh
# Backs up settings.local.json before patching
# Requires: jq
```

### context-check.sh
Standalone health check, useful in heartbeat loops or CI.

```bash
bash scripts/context-check.sh                    # Human-readable output
bash scripts/context-check.sh --json              # Machine-readable JSON
echo '{"context_window":{"used_percentage":72}}' | bash scripts/context-check.sh
# Exit codes: 0=GREEN, 1=YELLOW, 2=RED
```

### snapshot.sh
Save facts to daily memory file.

```bash
bash scripts/snapshot.sh "Fact one" "Fact two" "Fact three"
echo -e "Fact one\nFact two" | bash scripts/snapshot.sh -
```

### rotate.sh
Archive old daily memory files.

```bash
bash scripts/rotate.sh           # Archives files older than 3 days (default)
KEEP_DAYS=7 bash scripts/rotate.sh  # Keep 7 days instead
```

## Messaging Footer

When context is at YELLOW or above, agents should append a footer to outgoing messages:

```
---
63% Context Window | 1x compacted
```

This helps the user understand when a session is running long and may need a fresh start.

## Configuration

All configuration is via environment variables with sensible defaults:

| Variable             | Default                                          | Description                            |
|----------------------|--------------------------------------------------|----------------------------------------|
| `MEMORY_DIR`         | Auto-detect (see below)                          | Where to write daily memory files      |
| `KEEP_DAYS`          | `3`                                              | Days to keep before archiving          |
| `HEALTH_GREEN_MAX`   | `50`                                             | Max % for GREEN status                 |
| `HEALTH_RED_MIN`     | `75`                                             | Min % for RED status                   |
| `COMPACTION_DROP`    | `30`                                             | % drop that indicates compaction       |

**Memory directory auto-detection order:**
1. `$MEMORY_DIR` environment variable
2. `~/.openclaw/workspace/memory` (if exists)
3. `~/.claude/memory` (fallback)

## Troubleshooting

### jq not installed
```bash
# macOS
brew install jq
# Linux
sudo apt-get install jq
```

### Statusline not updating
1. Check the script is at `~/.claude/session-health-statusline.sh`
2. Check `settings.local.json` has the `statusLine` key
3. Restart Claude Code
4. Test manually: `echo '{}' | bash ~/.claude/session-health-statusline.sh`

### Reset compaction state
```bash
rm /tmp/session-health-*.json
```

### Statusline shows "Context Window" with no percentage
Normal on first run — the statusline needs one data point from Claude Code before it can display usage. It will update on the next tick.
