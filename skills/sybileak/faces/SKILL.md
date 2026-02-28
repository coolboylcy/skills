---
name: faces
description: Use this skill whenever the user wants to interact with the Faces AI platform — including logging in or registering, creating or managing face personas, running inference (chat, messages, or responses), training a face by uploading or compiling documents and threads, managing API keys, checking billing, balance, or compile quota, or inspecting account state.
allowed-tools: Bash(faces *)
---

# Faces Skill

You have access to the `faces` CLI. Use it to fulfill any Faces platform request.

## Current config
!`faces config show 2>/dev/null || echo "(no config saved)"`

## Setup check

Before running any command, verify credentials are available:

```bash
faces config show          # see what's saved
faces auth whoami          # confirm login works
```

If no credentials exist and the user hasn't provided a key:
- For interactive sessions: run `faces auth login` and prompt for email + password
- For API-key-only context: tell the user to set `FACES_API_KEY=<key>` or run `faces config set api_key <key>`

Install (if `faces` command not found):
```bash
pip install faces-cli
```

---

## Auth rules

| Command group | Requires |
|---|---|
| `faces auth *`, `faces keys *` | JWT only — run `faces auth login` first |
| Everything else | JWT **or** API key |

---

## Common tasks

### Login
```bash
faces auth login --email user@example.com --password secret
faces auth whoami
```

### Create a face and chat with it
```bash
faces face create --name "Jony Five" --username jony-five
faces chat chat jony-five --message "Hello!"

# With a specific LLM
faces chat chat jony-five --llm claude-sonnet-4-6 --message "Hello!"

# Stream response
faces chat chat jony-five --stream --message "Write a long response"
```

### Compile a document into face memory
```bash
# Step 1 — create the document
DOC_ID=$(faces compile doc create <face_id> --label "Notes" --file notes.txt | jq -r '.id')

# Step 2 — run LLM extraction
faces compile doc prepare "$DOC_ID"

# Step 3 — sync to memory (charges compile quota; --yes skips confirm)
faces compile doc sync "$DOC_ID" --yes
```

### Upload a file (PDF, audio, video, text)
```bash
faces face upload <face_id> --file report.pdf --kind document
faces face upload <face_id> --file interview.mp4 --kind thread
```

### Check billing state
```bash
faces billing balance        # credits + payment method status
faces billing subscription   # plan, face count, renewal date
faces billing quota          # compile token usage per face
```

### Create a scoped API key
```bash
# JWT required — keys cannot manage themselves
faces keys create \
  --name "Partner key" \
  --face jony-five \
  --budget 10.00 \
  --expires-days 30
```

### Anthropic Messages proxy
```bash
faces chat messages jony-five@claude-sonnet-4-6 \
  --message "What do you know about me?" \
  --max-tokens 512
```

### OpenAI Responses proxy
```bash
faces chat responses jony-five@gpt-4o \
  --message "Summarize my recent work"
```

---

## Output format

All commands output JSON by default. Use `jq` to extract fields:

```bash
faces face list | jq '.[].username'
faces billing balance | jq '.balance_usd'
faces compile doc list <face_id> | jq '.[] | {id, label, status}'
```

Pass `--no-json` for human-readable output.

---

## Full command reference

```
faces auth login        --email  --password
faces auth logout
faces auth register     --email  --password  --name  --username  [--invite-key]
faces auth whoami
faces auth refresh

faces face create       --name  --username  [--attr KEY=VALUE]...  [--tool NAME]...
faces face list
faces face get          <face_id>
faces face update       <face_id>  [--name]  [--attr KEY=VALUE]...
faces face delete       <face_id>  [--yes]
faces face stats
faces face upload       <face_id>  --file PATH  --kind document|thread

faces chat chat         <face_username>  -m MSG  [--llm MODEL]  [--system]  [--stream]
                        [--max-tokens N]  [--temperature F]  [--file PATH]
faces chat messages     <face@model>  -m MSG  [--system]  [--stream]  [--max-tokens N]
faces chat responses    <face@model>  -m MSG  [--instructions]  [--stream]

faces compile doc create   <face_id>  [--label]  (--content TEXT | --file PATH)
faces compile doc list     <face_id>
faces compile doc get      <doc_id>
faces compile doc prepare  <doc_id>
faces compile doc sync     <doc_id>  [--yes]
faces compile doc delete   <doc_id>

faces compile thread create   <face_id>  [--label]
faces compile thread list     <face_id>
faces compile thread message  <thread_id>  -m MSG
faces compile thread sync     <thread_id>

faces keys create   --name  [--expires-days N]  [--budget F]  [--face USERNAME]...  [--model NAME]...
faces keys list
faces keys revoke   <key_id>  [--yes]
faces keys update   <key_id>  [--name]  [--budget F]  [--reset-spent]

faces billing balance
faces billing subscription
faces billing quota
faces billing usage     [--group-by api_key|model|llm|date]  [--from DATE]  [--to DATE]
faces billing topup     --amount F  [--payment-ref REF]
faces billing checkout  --plan standard|pro
faces billing card-setup

faces account state

faces config set    <key> <value>
faces config show
faces config clear  [--yes]
```

Global options (before any subcommand):
```
faces [--base-url URL] [--token JWT] [--api-key KEY] [--json/--no-json] COMMAND
```

Env vars: `FACES_BASE_URL`, `FACES_TOKEN`, `FACES_API_KEY`
