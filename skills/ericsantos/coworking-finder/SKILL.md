---
name: coworking-finder
description: Find coworking spaces and office spaces in Brazilian cities. Use when the user asks to search for coworkings, shared offices, or workspaces in a specific city/state in Brazil, optionally filtered by neighborhood or region.
---

# Coworking Finder

Search for coworking spaces in Brazilian cities using SerpAPI (Google Search + Google Local) with Perplexity as fallback.

## Input

The user provides a natural language request like:
- "Busca coworkings em Belo Horizonte, MG"
- "Encontre espaços de coworking em São Paulo, SP, região da Vila Madalena"
- "Coworkings em Florianópolis, SC, bairro Centro"

Extract from the request:
- **city** (required): City name
- **state** (required): Brazilian state abbreviation (UF)
- **neighborhood** (optional): Preferred neighborhood or region

## Workflow

### Phase 1: Google Search Discovery

Run multiple SerpAPI Google searches to discover coworking names and leads:

```bash
# Primary searches (run all)
{serpapi}/scripts/search.sh "coworking {city} {state}" --country br --lang pt --num 10
{serpapi}/scripts/search.sh "espaço coworking {city}" --country br --lang pt --num 10
{serpapi}/scripts/search.sh "coworking space {city} Brazil" --country br --lang en --num 10
```

If **neighborhood** was provided, add:
```bash
{serpapi}/scripts/search.sh "coworking {neighborhood} {city}" --country br --lang pt --num 10
```

Where `{serpapi}` = `/root/clawd/skills/serpapi-search`

From the results, extract a list of coworking space names and any URLs found.

### Phase 2: Perplexity Fallback (if needed)

If Phase 1 found fewer than 3 leads (or fewer than 5 when no neighborhood), use Perplexity deep research:

```bash
{perplexity}/scripts/search.sh --mode research --lang pt "lista completa de espaços de coworking em {city} {state} Brasil com endereço, telefone e site{neighborhood_clause}"
```

Where:
- `{perplexity}` = `/root/clawd/skills/perplexity`
- `{neighborhood_clause}` = `, na região de {neighborhood}` if neighborhood was provided, empty otherwise

Extract coworking names from the Perplexity response to enrich the leads list.

### Phase 3: Google Local Details

For each discovered coworking name, fetch detailed info via Google Local:

```bash
{serpapi}/scripts/search.sh "{coworking_name}" --engine google_local --country br --location "{city}, {state}, Brazil" --num 3
```

From Google Local results, extract:
- **Name** (title)
- **Google Maps link** (from `link` or construct from place_id)
- **Website** (from `website` or `links.website`)
- **Address** (from `address`)
- **Phone** (from `phone`)
- **Rating** (from `rating` if available)

### Phase 4: Web Scraping Fallback (per lead)

If Google Local returns no result for a specific coworking, search for its details directly:

```bash
{serpapi}/scripts/search.sh "{coworking_name} {city} site telefone endereço" --country br --lang pt --num 5
```

Use Jina Reader (`/root/clawd/skills/jina-reader`) to extract contact info from the coworking's website or Instagram if found:

```bash
{jina}/scripts/read.sh "{website_url}"
```

Where `{jina}` = `/root/clawd/skills/jina-reader`

Extract address, phone, and website from the page content.

### Phase 5: Fallback to Office Spaces

If after all phases fewer than 3 results (with neighborhood) or 5 results (city-only), broaden the search to traditional office spaces:

```bash
{serpapi}/scripts/search.sh "escritório compartilhado {city} {state}" --country br --lang pt --num 10
{serpapi}/scripts/search.sh "sala comercial coworking {city}" --country br --lang pt --num 10
```

Then repeat Phase 3 (Google Local) for any new leads found.

## Output Format

Present results directly in the chat channel:

```
🏢 Coworkings em {city}/{state}{neighborhood_line}:
{N} espaços encontrados

1. **{Name}**
   📍 {Address}
   🌐 {Website}
   📞 {Phone}
   ⭐ {Rating} (Google)
   🔗 {Google Maps/Local link}

2. **{Name}**
   ...

---
📚 Referências:
• {URL 1}
• {URL 2}
• {URL 3}
```

Where `{neighborhood_line}` = ` — região {neighborhood}` if provided, empty otherwise.

### Output rules:
- Omit fields that were not found (don't show "N/A")
- Include ALL reference URLs used during the search (Google results pages, Perplexity sources, websites visited)
- Minimum targets: 3 results with neighborhood filter, 5 results city-only
- If targets not met after all phases, present what was found with a note explaining the search was exhaustive
- Sort by rating (highest first) when available, otherwise alphabetical

## Dependencies

This skill requires:
- **serpapi-search** skill (Google Search + Google Local)
- **perplexity** skill (deep research fallback)
- **jina-reader** skill (web scraping fallback)
