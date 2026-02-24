---
name: deep-research
description: "Autonomous multi-step deep research that produces comprehensive cited reports. Use when: (1) user asks for in-depth research on any topic, (2) user says 'research X' or 'deep dive on X', (3) complex questions requiring multiple sources and cross-validation, (4) market/competitor/stock/industry analysis. NOT for: simple factual lookups (just web_search), or questions answerable in one search."
---

# Deep Research

Autonomous research agent that iteratively searches, reads, discovers, and synthesizes — producing a structured, cited report.

## Workflow

### Phase 1: Decompose (30s)

Break the topic into 5-8 research sub-questions. Think like an investigative journalist:
- What are the key facts?
- What are different perspectives/sources?
- What's the timeline/history?
- What data/evidence exists?
- What are the unknowns or controversies?

### Phase 2: Iterative Search (3-8 min)

For each sub-question, run **multiple search rounds**:

```
Round 1: Broad search → read top 3-5 results via web_fetch
Round 2: Follow leads discovered in Round 1 → targeted searches
Round 3: Fill gaps, verify claims, find contradicting sources
```

**Key behaviors:**
- After each fetch, extract NEW leads (names, companies, dates, claims) and search for those
- Cross-reference claims across 2+ independent sources
- When you find a primary source (official report, SEC filing, press release), always prefer it over secondary coverage
- Track source quality: official > reputable media > blog > forum
- Use `web_fetch` to read full articles, not just search snippets
- Try different search queries for the same sub-question (rephrase, use quotes, add site: filters)
- Minimum 15 unique sources for a standard research task, 25+ for complex ones

### Phase 3: Synthesize

Produce a structured report:

```markdown
# [Topic] — Deep Research Report

## Executive Summary
3-5 sentence overview of key findings.

## Key Findings

### [Finding 1 Title]
Analysis with inline citations [1][2].

### [Finding 2 Title]
...

## Data & Evidence
Tables, numbers, comparisons where applicable.

## Risks / Unknowns / Controversies
What we couldn't confirm, conflicting information, gaps.

## Conclusion & Recommendations
Actionable takeaways.

## Sources
[1] Title — URL (date accessed)
[2] ...
```

### Phase 4: Store

- Save report to `memory/research/[topic-slug]-[date].md`
- If the research is related to an active project or investment, cross-reference in relevant memory files

## Quality Standards

- **Minimum sources**: 15 unique URLs for standard topics, 25+ for complex
- **Source diversity**: No more than 3 citations from same domain
- **Freshness**: Prefer sources < 6 months old; flag older data
- **Cross-validation**: Key claims must appear in 2+ independent sources
- **Bias check**: Include opposing viewpoints when they exist
- **No hallucination**: Every factual claim must have a source. If unsure, say "unverified" or "could not confirm"

## Adaptation by Topic Type

### Financial / Stock Research
- Check SEC/regulatory filings, earnings transcripts, analyst reports
- Include key financial metrics (revenue, margins, P/E, debt)
- Note insider transactions, institutional holdings
- See `references/financial-research.md`

### Market / Industry Research
- TAM/SAM/SOM when available
- Competitive landscape, key players, market share
- Trends, growth rates, inflection points

### Technical / Product Research
- Architecture, tech stack, benchmarks
- Alternatives comparison matrix
- Community sentiment (GitHub stars, HN/Reddit discussions)

### Person / Company Research
- Background, track record, key decisions
- Public statements, interviews
- Red flags, controversies
