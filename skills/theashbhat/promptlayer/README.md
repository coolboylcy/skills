# openclaw-skill-promptlayer

An [OpenClaw](https://openclaw.ai) skill for [PromptLayer](https://promptlayer.com) — prompt management, versioning, evaluations, and LLM observability.

## What it does

Gives your OpenClaw agent the ability to:

- **Manage prompts** — list, get, version, and publish prompt templates
- **Log LLM requests** — track every request with metadata, scores, and tags
- **Run evaluations** — execute eval pipelines against datasets
- **Manage agents** — list and run PromptLayer agent workflows
- **Work with datasets** — list and create test datasets

## Installation

Copy the skill to your OpenClaw workspace:

```bash
cp -r promptlayer/ ~/your-workspace/skills/promptlayer/
```

Or clone directly:

```bash
cd ~/your-workspace/skills
git clone https://github.com/theashbhat/openclaw-skill-promptlayer.git promptlayer
```

## Configuration

1. Get your API key from [PromptLayer Dashboard → Settings](https://dashboard.promptlayer.com/settings)

2. Run the setup script:
   ```bash
   bash skills/promptlayer/scripts/setup.sh
   ```

   Or manually add to `~/.openclaw/.env`:
   ```
   PROMPTLAYER_API_KEY=pl_xxxxxxxxxxxxx
   ```

## Usage

Once installed, your OpenClaw agent can use PromptLayer naturally:

> "List my prompt templates"
> "Get the production version of my welcome-email prompt"
> "Run the accuracy eval pipeline"
> "Show me my PromptLayer agents"

### CLI

The skill includes `pl.sh` for direct API access:

```bash
# List templates
./scripts/pl.sh templates list

# Get a specific template
./scripts/pl.sh templates get welcome-email --label prod

# Log a request
echo '{"function_name": "openai.chat.completions.create", ...}' | ./scripts/pl.sh log

# Track a score
./scripts/pl.sh track-score 12345 accuracy 0.95

# Run an eval
./scripts/pl.sh evals run pipeline_abc123
```

## Links

- [PromptLayer Docs](https://docs.promptlayer.com)
- [PromptLayer REST API](https://docs.promptlayer.com/reference/rest-api-reference)
- [OpenClaw Docs](https://docs.openclaw.ai)

## License

MIT
