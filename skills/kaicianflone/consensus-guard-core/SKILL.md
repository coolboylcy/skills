---
name: consensus-guard-core
description: Shared deterministic guard primitives for the Consensus.Tools skill family: hard-block taxonomy, weighted vote aggregation, reputation updates, idempotency keys, strict schema enforcement, and indexed board artifact access.
homepage: https://github.com/kaicianflone/consensus-guard-core
source: https://github.com/kaicianflone/consensus-guard-core
metadata:
  {"openclaw": {"requires": {"bins": ["node", "tsx"]}}}
---

# consensus-guard-core

`consensus-guard-core` is the common policy engine behind the Consensus guard ecosystem.

## What this skill/package provides

- unified hard-block taxonomy
- deterministic `aggregateVotes()` policy function
- deterministic reputation update rules with clamping
- idempotency key generation for retry-safe execution
- strict-schema unknown-field rejection helpers
- indexed board read helpers for scalable artifact lookup

## Why this matters

Without a shared core, every guard drifts into incompatible policy logic. This package keeps behavior consistent, replayable, and comparable across domains.

## Ecosystem role

`consensus-guard-core` is consumed by publish/support/merge/action guards and should be treated as policy infrastructure, not an end-user workflow skill.

## Benefits for LLM orchestration

- lower integration drift
- consistent decision semantics across workflows
- easier auditing and cross-skill analytics


## Runtime, credentials, and network behavior

- runtime binaries: `node`, `tsx`
- network calls: none in the guard decision path itself
- conditional network behavior: if a run needs persona generation and your persona-generator backend uses an external LLM, that backend may perform outbound API calls
- credentials: `OPENAI_API_KEY` (or equivalent provider key) may be required **only** for persona generation in LLM-backed setups; if `persona_set_id` is provided, guards can run without LLM credentials
- filesystem writes: board/state artifacts under the configured consensus state path

## Dependency trust model

- `consensus-guard-core` and `consensus-persona-generator` are first-party consensus packages
- versions are semver-pinned in `package.json` for reproducible installs
- this skill does not request host-wide privileges and does not mutate other skills

## Quick start

```bash
npm test
```

## Tool-call integration

This skill is wired to the consensus-interact contract boundary (via shared consensus-guard-core wrappers where applicable):
- readBoardPolicy
- getLatestPersonaSet / getPersonaSet
- writeArtifact / writeDecision
- idempotent decision lookup

This keeps board orchestration standardized across skills.

## Invoke Contract

This skill exposes a canonical entrypoint:

- `invoke(input, opts?) -> Promise<OutputJson | ErrorJson>`

`invoke()` starts the guard flow, which then executes persona evaluation and consensus-interact-contract board operations (via shared guard-core wrappers where applicable).
