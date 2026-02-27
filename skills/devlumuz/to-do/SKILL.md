---
name: to-do
description: Give your AI the power to act in the future. Schedule delayed prompts and one-off reminders that automatically wake the agent up at an exact moment to execute workflows, check systems, or send notifications.
metadata: {"clawdbot":{"emoji":"⏰","requires":{"bins":["node"],"env":["OPENCLAW_BIN","OPENCLAW_TZ"]}}}
---

# SKILL: To-Do (Ephemeral Tasks)

<identity>
Cross-platform task scheduler that programs one-off delayed actions using the OS native scheduler (`at` on Linux/macOS · `schtasks` on Windows). It wakes the agent at an exact future moment with full context injection.
</identity>

<goal>
Schedule, list, and manage ephemeral tasks that fire at a precise time in the user's timezone — ensuring the future agent wakes up with a fully self-contained instruction, correct routing, and zero ambiguity.
</goal>

---

## Required Environment Variables

| Variable | Description | Example |
|---|---|---|
| `OPENCLAW_BIN` | Absolute path to the `openclaw` binary | `/usr/bin/openclaw`, `C:\Program Files\OpenClaw\openclaw.exe` |
| `OPENCLAW_TZ` | User's IANA timezone | `America/Mexico_City`, `Europe/Madrid`, `Asia/Tokyo` |

The skill **will not start** if either variable is missing.

> **Why `OPENCLAW_TZ`?** The server may run in UTC while the user lives in a different timezone. This variable ensures "schedule at 15:00" means 15:00 *user time*, not server time.

---

## Commands

```bash
# Schedule a task (timezone is optional — defaults to OPENCLAW_TZ)
node skills/to-do/to-do.js schedule "<YYYY-MM-DD HH:mm>" "<instruction>" "<user_id>" "<channel>" ["<timezone>"]

# Get current time in user's timezone
node skills/to-do/to-do.js now ["<timezone>"]

# List pending tasks
node skills/to-do/to-do.js list

# Delete a task by ID
node skills/to-do/to-do.js delete <ID>
```

---

## Instructions

<instructions>

<always>
- Run `now` BEFORE resolving any relative time ("tomorrow", "in 2 hours", "tonight"). The server clock is NOT the user's clock. Use the `now` output as your reference for "today", "tomorrow", and "right now".
- Convert natural language into an absolute `YYYY-MM-DD HH:mm` timestamp before calling `schedule`.
- Write the `<instruction>` as if explaining to a stranger with ZERO context. Your future self wakes up in a completely isolated session with no memory of this conversation.
- Include in every instruction: exact file paths or URLs, full names (no pronouns), the specific action to take, and which skills or tools are needed.
- Always inject the current session's `user_id` and `channel` so the future payload routes back correctly.
- Run `list` before `delete` to confirm the correct ID.
</always>

<never>
- Never schedule without running `now` first. → Instead, always run `now`, confirm the date/time, then schedule.
- Never schedule a vague or ambiguous instruction. → Instead, ask the user to clarify before creating the task (see triggers below).
- Never use pronouns ("him", "her", "they") in scheduled instructions. → Instead, use full names and explicit references.
- Never guess a task ID when deleting. → Instead, run `list` first, confirm the ID, then delete.
- Never use the server's system clock to interpret relative times. → Instead, use the `now` command output as your time reference.
</never>

</instructions>

---

## Vague Request Triggers — Ask Before Scheduling

<vague_triggers>

If the user's request matches any of these patterns, **stop and ask** before scheduling:

| User says | What's missing |
|---|---|
| "Remind me to send the email" | Which email? To whom? What content? |
| "Check the server later" | Which server? What IP? What to verify? |
| "Follow up with him" | Who? About what? Via which channel? |
| "Do that thing tomorrow" | What thing? What's the expected outcome? |

**Rule:** If you can't write a fully self-contained instruction from what the user said, you don't have enough information to schedule.

</vague_triggers>

---

## Examples

<examples>

<example id="good_instruction">
  <input>User: "Remind me tomorrow at 5pm to check PRs on the backend repo"</input>
  <output>
    1. Run `now` → "🕒 Current Time (America/Mexico_City): 2/26/2026, 2:45 PM" → tomorrow = 2026-02-27
    2. Ask: "Which backend repo? What should I check specifically?"
    3. User clarifies: "backend-api on GitHub, check if there are pending PRs for the auth module"
    4. Schedule:
    ```bash
    node skills/to-do/to-do.js schedule "2026-02-27 17:00" \
      "Check the 'backend-api' repo on GitHub. If there are pending PRs for the authentication module, send Alice (alice@company.com) a Slack reminder to review them before the 5 PM deployment freeze. Reference deployment logs at /var/log/deploy.log." \
      "7684875449" "telegram"
    ```
    5. Confirm with the output format below.
  </output>
</example>

<example id="bad_instruction">
  <input>"Remind him to push the code later."</input>
  <output>
    ❌ DO NOT schedule this. Missing: who is "him"? Which repo? Which branch? What time is "later"?
    → Ask the user to clarify all missing details first.
  </output>
</example>

<example id="time_resolution">
  <input>User: "Set a reminder for in 2 hours"</input>
  <output>
    1. Run `now` → "🕒 Current Time (America/Mexico_City): 2/26/2026, 2:45 PM"
    2. Calculate: 2:45 PM + 2h = 4:45 PM → "2026-02-26 16:45"
    3. Ask what the reminder should say (if not specified)
    4. Schedule with the absolute timestamp
  </output>
</example>

</examples>

---

## Output Format

After scheduling, respond naturally but **always include this confirmation block**:

```
> `[Day, Month DD · HH:MM TZ]`
> *[Exact instruction left for the future agent]*
```

<example id="output">
Done! Here's the exact instruction I left for my future self:

> `Thursday, February 27 · 5:00 PM CST`
> *Check the 'backend-api' repository on GitHub. If there are pending PRs for the authentication module, send Alice a Slack reminder to review them before the 5 PM deployment freeze.*
</example>

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `Missing required environment variable(s)` | `OPENCLAW_BIN` or `OPENCLAW_TZ` not set | Add them to `.env` or shell profile |
| `at` not found | Linux/macOS `atd` daemon not running | `sudo systemctl enable atd && sudo systemctl start atd` |
| Task fires but agent has no context | Vague instruction was scheduled | Re-schedule with a fully self-contained instruction |
| Wrong time — task fired early/late | Used server clock instead of `now` | Always run `now` first; never trust the server clock |
| Deleting wrong task | Guessed the ID | Run `list` first, confirm ID, then `delete` |