---
name: openclaw-optimizer
description: Master optimization system - APPLIES TO EVERY RESPONSE. Before responding, classify task complexity (simple question vs analysis vs coding). Use Haiku for simple/navigation/extraction/status. Use Sonnet ONLY for writing/analysis/planning/debugging. Monitor context size - if >50k tokens, recommend /compact. For automations, use scheduler wrapper. Never load full conversation history for simple tasks. Heartbeats always Haiku, single-line only. Never use Opus. This skill MUST run before every response to prevent 100k+ token bloat.
---

# OpenClaw Optimizer

**MANDATORY: Run before EVERY response, including normal conversation.**

## ⚠️ CRITICAL - Apply to ALL Sessions

**Before responding to ANY message:**
1. Check context size via session_status - if >50k tokens, STOP and say ONLY: "⚠️ Context bloat detected: {X}k tokens. Compacting now for 90% cost savings..." then immediately use gateway.restart with reason="Auto-compact: context exceeded 50k tokens"
2. Classify task complexity (scripts/router.py logic)
3. Use Haiku for: simple questions, navigation, status checks, extraction, casual chat
4. Use Sonnet ONLY for: writing content, analysis, planning, debugging, code >10 lines
5. If heartbeat: ALWAYS Haiku, single-line response only
6. After compaction completes, resume the original task

## 🎯 What This Does

OpenClaw Optimizer is your **always-on cost + performance orchestrator**. It applies to every task:

1. **Router** - Classifies complexity, picks models, decides strategy
2. **Scheduler** - Wraps automations with preflight/execute/postflight
3. **Browser Governor** - Prevents collisions, stops loops, enforces patterns
4. **Cost Guard** - Predicts cost, enforces budgets, gracefully degrades
5. **Telemetry** - Logs everything, learns from history, recommends budgets

## 🚀 Quick Start

### For Normal Tasks (Manual Override)

Check what the router recommends:

```bash
scripts/router.py "Find openclaw tweets and write replies"
```

Output:
```
Complexity: medium
Strategy: gather_write
Phase 1 (gather): anthropic/claude-3-5-haiku-latest
Phase 2 (write): anthropic/claude-sonnet-4-5
```

### For Automations (Required)

Wrap your cron jobs:

```bash
scripts/scheduler.py twitter_reply "Navigate twitter, find openclaw posts, reply"
```

This automatically does:
- ✅ Classify task → decide models
- ✅ Predict cost → check budget
- ✅ Acquire browser lock (if needed)
- ✅ Execute with cost tracking
- ✅ Release lock + log telemetry

## 📋 Component 1: Router

**Classifies every task as LOW/MED/HIGH and picks the right strategy.**

### Complexity Levels

| Level | Model | Strategy | Use Case |
|-------|-------|----------|----------|
| **LOW** | Haiku | Direct | Browser nav, extraction, lookups, heartbeat |
| **MED** | Haiku→Sonnet | Gather-write | Navigate + reply, search + post |
| **HIGH** | Sonnet | Direct/Spawn | Analysis, planning, complex reasoning |

### Usage

```bash
scripts/router.py "<task description>"
```

**Examples:**

```bash
# LOW complexity (Haiku direct)
scripts/router.py "Click the login button"
scripts/router.py "Extract text from this page"
scripts/router.py "What's the weather?"

# MED complexity (Haiku gather → Sonnet write)
scripts/router.py "Find HN threads and write technical comments"
scripts/router.py "Search twitter for openclaw posts and reply"

# HIGH complexity (Sonnet)
scripts/router.py "Analyze this codebase and write a detailed report"
scripts/router.py "Debug this failing test and propose a fix"
```

### Router Patterns

**Haiku-only triggers:**
- Questions: what, where, when, who
- Commands: list, show, get, find, click, navigate
- Extraction: extract, scrape, parse, format
- Status: heartbeat, status, check

**Sonnet-required triggers:**
- Analysis: analyze, compare, evaluate
- Writing: write tweet/post/comment/article  
- Planning: plan, strategy, design
- Problem-solving: debug, fix, solve
- Coding: code function/class/script

**Gather-write triggers:**
- `find.*write` - Find then write
- `search.*post` - Search then post
- `navigate.*comment` - Navigate then comment

## 🗓️ Component 2: Scheduler

**Wraps automations with smart preflight/execute/postflight.**

### The Three Phases

#### Preflight
1. Classify task (router)
2. Recommend budget (telemetry)
3. Acquire browser lock (if needed)
4. Start cost tracking

#### Execute
- Run the actual task
- Track spending in real-time
- Apply degradation if soft limit hit

#### Postflight
1. Release browser lock
2. Finish cost tracking
3. Log telemetry for learning

### Usage

```bash
scripts/scheduler.py <task_type> "<task_description>"
```

**Examples:**

```bash
scripts/scheduler.py twitter_reply "Find openclaw posts, write natural replies"
scripts/scheduler.py hn_comment "Search HN for agent discussions, add value"
scripts/scheduler.py ih_engage "Find indie makers struggling with AI, help genuinely"
```

### Integration with Cron

Update your cron jobs to use the scheduler:

**Old:**
```yaml
message: "Navigate twitter, find posts, reply"
```

**New:**
```yaml
message: "Run: scripts/scheduler.py twitter_reply 'Navigate twitter, find posts, reply'"
```

The scheduler handles all the orchestration automatically.

## 🌐 Component 3: Browser Governor

**Prevents browser collisions and runaway loops.**

### Rules

1. **One browser session at a time** - Enforced via lock file
2. **Max 20 steps per session** - Hard cap prevents loops
3. **Snapshot → Act pattern** - Enforced for safety
4. **Stale lock detection** - Breaks locks older than 5 minutes

### Usage

```bash
# Check browser availability
scripts/browser_governor.py status

# Acquire lock (automation uses this)
scripts/browser_governor.py acquire <agent_id> "<task>"

# Release lock
scripts/browser_governor.py release

# Increment step counter
scripts/browser_governor.py step
```

### What Happens When Browser Locked?

If browser is locked when you need it:

```
❌ Browser locked by twitter_automation
Task: Replying to openclaw posts
Age: 47s

Options:
1. Wait for lock (timeout: 60s)
2. Skip browser work (use cached data)
3. Return BLOCKED report
```

**The skill chooses automatically:**
- If task can use cache → skip browsing
- If task is urgent → wait (max 60s)
- Otherwise → return BLOCKED report

## 💰 Component 4: Cost Guard

**Predicts cost, enforces budgets, degrades gracefully.**

### Budget Levels

Each task has two budgets:

- **budget_soft** - Warning threshold → degrade
- **budget_max** - Hard stop → abort with partial result

### Degradation Strategy

When soft limit crossed:

1. **Switch to Haiku** (if on Sonnet)
2. **Reduce browser steps** (20 → 5)
3. **Use cached data** (skip fresh scraping)
4. **Skip browsing entirely** (if > 20% over soft limit)

### Usage

```bash
# Predict cost before running
scripts/cost_guard.py predict anthropic/claude-sonnet-4-5 50000 5000

# Start tracking a task
scripts/cost_guard.py start task_123 0.10 0.20 anthropic/claude-3-5-haiku-latest 5000 1000

# Log spending during execution
scripts/cost_guard.py log task_123 5000 1000 anthropic/claude-3-5-haiku-latest

# Get degradation recommendations
scripts/cost_guard.py degrade task_123

# Finish task and get summary
scripts/cost_guard.py finish task_123

# Check daily total
scripts/cost_guard.py daily
```

### Example: Task with Degradation

```
Task: twitter_reply_001
Budget soft: $0.10
Budget max: $0.20

Phase 1 (gather): $0.02 ✅
Phase 2 (write): $0.09 ⚠️  SOFT LIMIT ($0.11 total)

→ Degrading:
  - Switched to Haiku for writing
  - Reduced max steps: 20 → 5
  - Using cached twitter data

Phase 2 (retry with Haiku): $0.02 ✅
Total: $0.13 (within budget_max)
```

## 📊 Component 5: Telemetry

**Logs everything, learns from history, recommends safe budgets.**

### What Gets Logged

Every completed task logs:
- `task_type` - Category (twitter_reply, hn_comment, etc.)
- `model` - Which model was used
- `browser_steps` - How many browser actions
- `input_tokens` - Tokens sent to API
- `output_tokens` - Tokens received
- `cost` - Actual dollars spent
- `duration` - Time taken (seconds)
- `success` - Did it complete?

### Usage

```bash
# Log a completed run
scripts/telemetry.py log twitter_reply anthropic/claude-3-5-haiku-latest 5 5000 1000 0.02 12.5 true

# Get stats for a task type
scripts/telemetry.py stats twitter_reply

# Get budget recommendation (learns from history)
scripts/telemetry.py recommend twitter_reply

# View recent history
scripts/telemetry.py history twitter_reply 20
```

### Self-Tuning Budgets

After 10+ runs, telemetry recommends budgets automatically:

```bash
$ scripts/telemetry.py recommend twitter_reply

💡 Budget recommendation for 'twitter_reply'

Budget soft: $0.08  (p50 + 20% buffer)
Budget max: $0.15   (p90 + 50% buffer)

Confidence: high (based on 23 runs)
Success rate: 95%
```

**How it learns:**
- `budget_soft` = median cost + 20% buffer
- `budget_max` = p90 cost + 50% buffer
- Confidence: low < 5 runs, medium < 10 runs, high ≥ 10 runs

## 🔄 Full Integration Example

Here's how everything works together for a Twitter automation:

### Step 1: Router Classifies

```
Task: "Find openclaw tweets, write witty replies"
→ Complexity: MEDIUM
→ Strategy: GATHER_WRITE
→ Models: Haiku (gather) → Sonnet (write)
```

### Step 2: Telemetry Recommends Budget

```
Based on 15 previous twitter_reply runs:
→ budget_soft: $0.08
→ budget_max: $0.15
```

### Step 3: Browser Governor Acquires Lock

```
→ Lock acquired by automation_twitter_001
→ Max steps: 20
```

### Step 4: Cost Guard Starts Tracking

```
→ Predicted cost: $0.12
→ Within budgets ✅
```

### Step 5: Execute (Two Phases)

**Phase 1 - Gather (Haiku):**
```
→ Navigate twitter.com/search?q=openclaw
→ Snapshot page
→ Extract 3 recent posts
→ Cost: $0.01 (5k input, 500 output)
→ Steps: 3/20
```

**Phase 2 - Write (Sonnet):**
```
→ Spawn Sonnet sub-agent
→ Write 3 witty replies
→ Cost: $0.09 (3k input, 2k output)
→ Total so far: $0.10 ✅ (within budget_soft)
```

**Phase 3 - Post (Haiku):**
```
→ Post replies with browser.act
→ Cost: $0.02 (3k input, 200 output)
→ Steps: 6/20
→ Total: $0.12 ✅ (within budget_max)
```

### Step 6: Postflight

```
→ Browser lock released
→ Cost tracking finished: $0.12
→ Telemetry logged:
  - task_type: twitter_reply
  - models: haiku (gather+post), sonnet (write)
  - browser_steps: 6
  - tokens: 11k input, 2.7k output
  - cost: $0.12
  - duration: 18.3s
  - success: true
```

### Step 7: Learning

Next time twitter_reply runs:
```
→ Updated stats (now 16 runs):
  - p50 cost: $0.10 → budget_soft stays $0.08
  - p90 cost: $0.14 → budget_max adjusted to $0.16
```

## 🎯 Default Routing Rules

These are automatically applied:

### Always Haiku
- Browser navigation (click, scroll, snapshot)
- Data extraction (scrape, parse, format)
- Heartbeats (always single-line response)
- Simple lookups (weather, status, definitions)
- "What do I click next?" decisions

### Always Sonnet
- Writing quality content (tweets, posts, articles)
- Hard reasoning (analysis, comparisons, debugging)
- Planning & strategy
- Code generation (> 10 lines)

### Gather-Write Pattern (Haiku → Sonnet)
- "Find X and write about it"
- "Search Y and post Z"
- "Navigate A and comment B"
- Any automation combining navigation + writing

### Never Use
- **Opus** - Too expensive, Sonnet is sufficient

## 🤖 Heartbeat Optimization

**Special rules for heartbeat checks:**

```yaml
Model: anthropic/claude-3-5-haiku-latest (always)
Response format: Single line only
  - HEARTBEAT_OK
  - HEARTBEAT_ALERT: <one sentence> | NEXT: <one action>

Heartbeat NEVER does:
  - Deep work
  - Browser navigation
  - Multiple tool calls
  - Long responses
```

**Why:** Heartbeats run every 30min. At scale, heartbeat costs dominate. Keep them minimal.

## 📈 Expected Savings

### Before Optimization

```
Automation: 24 runs/day × $0.30 = $7.20/day
Heartbeats: 48 checks/day × $0.15 = $7.20/day
Conversation: $5/day
Total: ~$20/day (without runaway loops)
With loops: $90/day (actual)
```

### After Optimization

```
Automation: 10 runs/day × $0.08 = $0.80/day
  (Haiku gather $0.01 + Sonnet write $0.06 + Haiku post $0.01)
Heartbeats: 48 checks/day × $0.01 = $0.48/day
  (Haiku, single-line, no browsing)
Conversation: $2-3/day
  (Smart routing, degradation)
Total: $3-5/day ✅

Savings: 75-85%
Protection: Circuit breaker stops loops at 3 requests
```

## 🛠️ Troubleshooting

### Browser Lock Won't Release

```bash
# Check status
scripts/browser_governor.py status

# Force release (if stale)
scripts/browser_governor.py release
```

### Task Hitting Budget Limits

```bash
# Check what's expensive
scripts/telemetry.py stats <task_type>

# See if budget is too low
scripts/telemetry.py recommend <task_type>

# Check daily total
scripts/cost_guard.py daily
```

### Router Picking Wrong Model

Task phrasing matters:

❌ Bad: "Do the twitter thing"
✅ Good: "Find openclaw tweets and write replies"

The router uses regex patterns - be explicit.

### Telemetry Not Learning

```bash
# Check if history exists
scripts/telemetry.py history <task_type>

# Need 5+ runs for medium confidence, 10+ for high
```

## 🔧 Configuration

### Adjust Browser Step Limit

Edit `scripts/browser_governor.py`:

```python
self.max_steps = 20  # Change this
```

### Adjust Budget Buffers

Edit `scripts/telemetry.py`:

```python
budget_soft = stats["cost"]["p50"] * 1.2  # 20% buffer
budget_max = stats["cost"]["p90"] * 1.5   # 50% buffer
```

### Add Custom Task Patterns

Edit `scripts/router.py`:

```python
GATHER_WRITE_PATTERNS = [
    r'find.*write',
    r'your.*pattern',  # Add here
]
```

## 📦 Files Structure

```
openclaw-optimizer/
├── SKILL.md (this file)
├── scripts/
│   ├── router.py           - Task classification
│   ├── scheduler.py        - Automation wrapper
│   ├── browser_governor.py - Browser lock + patterns
│   ├── cost_guard.py       - Budget enforcement
│   └── telemetry.py        - Learning from history
└── state/
    ├── browser-lock.json      - Current browser lock
    ├── cost-state.json        - Active task budgets
    └── task-history.jsonl     - All completed runs
```

## 🚀 Next Steps

1. **Update cron jobs** - Wrap with scheduler
2. **Monitor for 24-48h** - Watch telemetry build history
3. **Review stats weekly** - Adjust budgets if needed
4. **Add custom patterns** - For your specific workflows

---

**This is the skill that makes OpenClaw production-ready.**  
Smart routing + cost control + self-learning = sustainable scale.
