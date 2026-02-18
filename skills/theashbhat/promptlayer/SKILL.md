---
name: promptlayer
description: Manage prompts, log LLM requests, run evaluations, and track scores via the PromptLayer API. Use when working with prompt versioning, A/B testing prompts, LLM observability/logging, prompt evaluation pipelines, datasets, or PromptLayer agents.
---

# PromptLayer

Interact with PromptLayer's REST API for prompt management, logging, evals, and observability.

## Setup

Requires `PROMPTLAYER_API_KEY` env var. Run `scripts/setup.sh` to configure.

## CLI Usage

All commands via `scripts/pl.sh`:

```bash
# Prompt Templates
pl.sh templates list
pl.sh templates get <name> [--label <release-label>]
pl.sh templates publish <name> --commit "message"

# Logging & Tracking
echo '<json>' | pl.sh log
pl.sh track-score <request_id> <score_name> <value>
pl.sh track-metadata <request_id> --json '{"key": "value"}'
pl.sh track-group <request_id> <group_id>

# Datasets
pl.sh datasets list

# Evaluations
pl.sh evals list
pl.sh evals run <pipeline_id>
pl.sh evals get <pipeline_id>

# Agents
pl.sh agents list
pl.sh agents run <agent_id> --input '{"var": "value"}'
```

## Direct API

Base URL: `https://api.promptlayer.com`
Auth header: `Authorization: Bearer $PROMPTLAYER_API_KEY`

For full endpoint reference, see `references/api.md`.
