---
name: fact-checker
version: 1.0.1
description: |
  Verify claims, numbers, and facts in markdown drafts against source data.
metadata:
  {
    "openclaw": {
      "emoji": "🔍",
      "requires": { "bins": ["python3"] },
      "network": { "outbound": false, "reason": "All verification is done against local files and APIs. No external network calls." }
    }
  }
  Use when: reviewing blog posts, reports, or documentation for accuracy
  before publication. Cross-references against FINDINGS.md, live APIs,
  scored run files, memory logs, and git history.
allowed-tools:
  - Read
  - exec
---

# Fact-Checker: Verify Markdown Claims Against Source Data

Given a markdown draft file, this skill extracts every verifiable claim
(numbers, dates, model names, scores, causal statements) and cross-references
them against available source data to produce a verification report.

## Usage

```bash
python3 skills/fact-checker/scripts/fact_check.py <draft.md>
python3 skills/fact-checker/scripts/fact_check.py <draft.md> --output report.md
```

## What It Checks

### Claim types extracted
- **Numeric claims** — integers and floats with surrounding context
- **Model references** — `model/task` (phi4/classify) and `model:tag` (phi4:latest)
- **Dates** — `YYYY-MM-DD` format
- **Score values** — decimal scores like `0.923`, `1.000`
- **Percentages** — `42%`, `95.3%`

### Source data consulted (in priority order)
1. `projects/hybrid-control-plane/FINDINGS.md` — primary source of truth
2. Control Plane `/status` API at `http://localhost:8765/status` — live scored run data
3. `projects/hybrid-control-plane/data/scores/*.json` — raw scored run files on disk
4. `memory/*.md` — daily logs with timestamps and decisions
5. `git log` in `projects/hybrid-control-plane/` — commit hashes, dates, authorship
6. `projects/hybrid-control-plane/CHANGELOG.md` — sprint history

## Output Format

Each claim produces one line:

```
✅ CONFIRMED:    "phi4/classify scored 1.000" → /status API: phi4_latest_classify mean=1.000 n=23
⚠️ UNVERIFIABLE: "this took about a day" → no timestamp correlation found in logs
❌ CONTRADICTED: "909 runs" → /status API shows 958 total runs (stale number?)
```

Followed by a summary count of confirmed / unverifiable / contradicted claims.

## When To Use This Skill

When asked to "fact-check" or "verify" a draft blog post, report, or
documentation file — run this skill and present the report to the user.
If any claims are ❌ CONTRADICTED, flag them prominently and suggest corrections.

## Instructions for Agent

1. Run the script with the path to the draft file.
2. Parse the output report.
3. Summarise key findings — especially any ❌ CONTRADICTED claims.
4. Suggest specific corrections with the correct values from the evidence.
5. If the `/status` API is unavailable, note it and rely on FINDINGS.md + score files.
