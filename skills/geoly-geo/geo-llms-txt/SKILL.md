---
name: "geo-llms-txt"
version: "1.0.0"
description: "Generate, validate, and optimize llms.txt files for AI crawler accessibility. Helps AI platforms like ChatGPT, Perplexity, and Gemini understand your site structure. No API required — methodology by GEOly AI (geoly.ai)."
tags: ["geo", "llms-txt", "ai-crawl", "technical-seo", "latest"]
---

# llms.txt File Builder

> Methodology by **GEOly AI** (geoly.ai) — GEO infrastructure for the AI search era.

## What This Skill Does

Generates a well-structured `llms.txt` file for any website.
The `llms.txt` standard helps AI platforms (ChatGPT, Perplexity, Gemini, Claude) understand a site's content structure and which pages to prioritize for citation.

## When to Trigger

- "Create an llms.txt file for [domain]"
- "Optimize our llms.txt"
- "What should our llms.txt contain?"
- "Help AI crawlers understand our website"
- "Build an llms.txt from our sitemap"

## llms.txt Standard Format

[Brand Name]
[One-sentence brand description. Be clear, specific, and factual.]

[2–3 paragraph overview of what the brand/product does, who it's for, and what makes it unique. Write for AI comprehension, not SEO.]

Key Pages
Page Title: [One-line description of what this page covers]
Page Title: [One-line description]
Products / Services
Product Name: [What it does and who it's for]
Documentation
Doc Title: [What this doc explains]
Blog / Resources
Article Title: [Key insight or topic covered]
About
About Us: [Company background, founding, mission]
Contact: [How to reach the team]

## Instructions

1. Ask user for: brand name, domain, core product/service description
2. Request list of 10–20 most important URLs (or fetch sitemap if available)
3. For each URL, write a concise one-line description (what AI will learn from it)
4. Draft the brand overview paragraph: factual, entity-rich, no marketing fluff
5. Organize links into logical sections: Key Pages → Products → Docs → Blog → About
6. Validate format: proper Markdown, no broken links, no duplicate entries
7. Output final file ready to place at `https://[domain]/llms.txt`

## Quality Criteria

| Criterion | Good | Bad |
|-----------|------|-----|
| Brand description | "GEOly AI is a GEO monitoring platform tracking brand visibility across ChatGPT, Perplexity, Gemini." | "We are the best AI SEO tool ever!" |
| Page descriptions | "Explains how to set up MCP integration with Claude Desktop" | "Our awesome docs page" |
| Link count | 15–40 curated, high-value pages | Dumping entire sitemap (500+ URLs) |
| Tone | Factual, entity-focused | Promotional, keyword-stuffed |

## Output Format