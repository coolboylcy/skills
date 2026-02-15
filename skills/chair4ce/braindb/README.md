# BrainDB

**Persistent, semantic memory for AI agents.**

BrainDB gives your AI assistant a real memory system — one that survives session resets, context compaction, and restarts. It automatically captures what matters from conversations and recalls it when relevant. Your AI remembers who you are, what you're working on, and what you've told it.

## Features

- **Semantic search** — 768-dimensional embeddings via all-mpnet-base-v2. Finds conceptually related memories, not just keyword matches.
- **Four memory types** — Episodic (events), semantic (facts), procedural (skills), and association (links between memories).
- **Tiered ranking** — Semantic similarity always outranks keyword matches. No more irrelevant results beating relevant ones.
- **Auto-deduplication** — Won't store near-duplicate memories (configurable threshold, default 0.90).
- **Hebbian reinforcement** — Memories strengthen with use, decay without it. Important memories persist; noise fades.
- **Motivation-weighted encoding** — Encoding strength varies by emotional/motivational context.
- **Query expansion** — Understands colloquial phrases ("how do we make money" → revenue, profit, pricing).
- **43ms average recall** at 1,000 memories. Scales to 10K+.

## Requirements

- Docker and Docker Compose
- 4 GB RAM (2 GB for embedding model, 512 MB for Neo4j, rest for gateway)
- 3 GB disk (embedding model download + database)

## Quick Start

```bash
git clone https://github.com/Chair4ce/braindb.git
cd braindb
./setup.sh
```

First run takes 3–5 minutes to download the embedding model. Subsequent starts take ~10 seconds.

The setup script generates a secure random Neo4j password and stores it in `.env`. The gateway binds to `127.0.0.1` only — it is not accessible from other machines on your network.

## Configuration

### Environment Variables (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `NEO4J_USER` | `neo4j` | Neo4j username |
| `NEO4J_PASSWORD` | Auto-generated | Neo4j password |
| `NEO4J_HEAP` | `256m` | Neo4j heap size |
| `NEO4J_PAGECACHE` | `128m` | Neo4j page cache |
| `GATEWAY_PORT` | `3333` | Gateway port (localhost only) |
| `BRAINDB_API_KEY` | Empty | Optional API key for gateway authentication |

### Recall Tuning (`config.json`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `semanticThreshold` | `0.4` | Minimum cosine similarity to consider a match |
| `fastPathThreshold` | `0.6` | Skip text search when top semantic result exceeds this |
| `dedupThreshold` | `0.90` | Reject encodes with similarity above this to existing memories |

## API

### Health Check

```bash
curl http://localhost:3333/health
```

### Encode a Memory

```bash
curl -X POST http://localhost:3333/memory/encode \
  -H "Content-Type: application/json" \
  -d '{
    "event": "User prefers dark mode",
    "content": "User explicitly said they prefer dark mode across all applications",
    "shard": "semantic"
  }'
```

### Recall Memories

```bash
curl -X POST http://localhost:3333/memory/recall \
  -H "Content-Type: application/json" \
  -d '{"query": "UI preferences", "limit": 5}'
```

### Run Decay

```bash
curl -X POST http://localhost:3333/memory/decay
```

### View Stats

```bash
curl http://localhost:3333/memory/stats
```

## Memory Types

| Shard | Purpose | Example |
|-------|---------|---------|
| `episodic` | Events, conversations, decisions | "Deployed v2.0 on Tuesday" |
| `semantic` | Facts, preferences, identity | "User's timezone is EST" |
| `procedural` | Skills, workflows, lessons | "Always run tests before deploy" |
| `association` | Cross-memory links (auto-managed) | Links between related memories |

## Security

BrainDB is designed for local, single-user operation:

- **Gateway binds to `127.0.0.1` only** — not accessible from your network.
- **Neo4j and embedder are not exposed** to the host — they communicate via an isolated Docker network.
- **Neo4j password is auto-generated** during setup (24-character random string).
- **Optional API key** — set `BRAINDB_API_KEY` in `.env` to require `Authorization: Bearer <key>` on all requests (except `/health`).
- **No external API calls during normal operation** — all embedding, search, and storage runs locally. Nothing leaves your machine. (Migration with swarm optionally sends file contents to Google's Gemini API — use `--no-swarm` for fully local migration.)
- **Non-root containers** — gateway and embedder run as unprivileged users inside their containers.

## Migrating Existing Memories

If you have an OpenClaw workspace with `MEMORY.md`, daily notes, or other files:

```bash
# Preview what would be migrated
node migrate.cjs --scan /path/to/workspace

# Migrate everything
node migrate.cjs /path/to/workspace

# Migrate a single file
node migrate.cjs --file /path/to/MEMORY.md
```

The migration tool auto-discovers workspace files, extracts facts, assigns shard types, and deduplicates. Your original files are never modified.

**Migration is fully local by default.** File contents never leave your machine. If you pass `--swarm`, the tool uses Gemini Flash for smarter fact extraction — but this sends file contents to Google's Gemini API. Only use `--swarm` if you're comfortable with that.

Options: `--dry-run`, `--scan`, `--swarm` (opt-in external API), `--braindb URL`, `--batch N`

## OpenClaw Integration

Add to your OpenClaw config:

```json
{
  "plugins": {
    "slots": { "memory": "braindb" },
    "entries": {
      "braindb": {
        "enabled": true,
        "config": {
          "gatewayUrl": "http://localhost:3333",
          "autoCapture": true,
          "autoRecall": true,
          "maxRecallResults": 7
        }
      }
    }
  }
}
```

## Architecture

```
┌─────────────────────────────────────┐
│         Gateway (localhost:3333)     │
│  ┌────────────┐  ┌──────────────┐   │
│  │  Embedding  │  │   Tiered     │   │
│  │   Cache     │  │   Ranking    │   │
│  └────────────┘  └──────────────┘   │
└──────┬──────────────────┬───────────┘
       │    Docker network (internal)
┌──────▼──────┐     ┌──────▼──────┐
│  Embedder   │     │    Neo4j    │
│  (768-dim)  │     │  (graph DB) │
│  mpnet-v2   │     │ All shards  │
└─────────────┘     └─────────────┘
```

All three services run in Docker containers on an isolated network. Only the gateway is accessible from the host, and only on `localhost`.

## Management

```bash
docker compose up -d        # Start
docker compose down         # Stop
docker compose logs -f      # Tail logs
docker compose down -v      # Reset (deletes all data)
```

## Uninstalling

```bash
bash uninstall.sh
```

The uninstaller exports all memories to `~/.openclaw/braindb-export/` (both JSON and readable markdown), stops containers, and removes the OpenClaw plugin config. Your workspace files are never modified. Docker volumes are preserved until you explicitly delete them.

## Performance

| Metric | Value |
|--------|-------|
| Recall accuracy | 98% (50-test benchmark suite) |
| Average latency | 12–20 ms per query |
| Cold query | ~60 ms |
| Memory capacity | Tested to 2,000; projected to 10K+ |
| Storage | ~3 GB (model + database) |
| RAM | ~2.5 GB (model + Neo4j + gateway) |

## License

MIT — Oaiken LLC
