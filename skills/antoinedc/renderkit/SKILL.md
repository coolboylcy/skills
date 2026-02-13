---
name: renderkit
version: "1.3.2"
description: Render structured data as beautiful hosted web pages, and create hosted forms for data collection, using the RenderKit API. Use this for visual pages, surveys, RSVPs, feedback forms, or any structured data.
metadata:
  openclaw:
    requires:
      env:
        - RENDERKIT_API_KEY
      bins:
        - curl
    primaryEnv: RENDERKIT_API_KEY
    homepage: https://renderkit.live
---

# RenderKit

RenderKit has two endpoints. **Pick the right one before making any API call:**

| User intent | Endpoint | Result |
|---|---|---|
| Present results, summaries, research, comparisons, itineraries | `POST /v1/render` | Read-only visual page at `/p/{slug}` |
| Collect input — forms, surveys, RSVPs, signups, feedback, questionnaires, configuration | `POST /v1/forms` | Interactive form at `/f/{slug}` that collects and stores submissions |

**Rule:** If the output needs input fields that people fill out and submit → `/v1/forms`. If it's content for people to read → `/v1/render`. Never use `/v1/render` with template `freeform` to fake a form — it produces a static page that cannot collect responses.

## Authentication

All API calls require a Bearer token in the `Authorization` header:

```
Authorization: Bearer $RENDERKIT_API_KEY
```

Get your API key by signing up at https://renderkit.live or via the API (`POST /v1/auth/signup`).

## Visual Rendering (`/v1/render`)

When you have substantial results to present to the user, use this endpoint to create a beautiful hosted web page instead of dumping raw text.

### When to Use

- Presenting research results or summaries
- Sharing travel plans or itineraries
- Comparing products, services, or options
- User asks to "show", "display", "visualize", or "make a page"
- Any time a visual page would be more useful than plain text
- **NOT** for collecting user input — use `/v1/forms` for that

### How to Use

1. Gather all relevant data from the current conversation
2. Pick the best template:
   - `travel_itinerary` — trip plans, day-by-day itineraries
   - `freeform` — anything else (AI picks the best layout)
3. POST to `https://renderkit.live/v1/render`:

```bash
curl -X POST https://renderkit.live/v1/render \
  -H "Authorization: Bearer $RENDERKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": "freeform",
    "context": "brief description of what this content is",
    "data": {
      "title": "Page Title",
      "content": "your data here — markdown, structured objects, anything"
    }
  }'
```

4. The API returns a `url` (human-readable slug), a `slug`, and a `render_id`. Share the URL with the user. Use the `render_id` or `slug` for PATCH/status calls.
5. If the user asks to expand, refine, or continue content you already rendered in this conversation, **update the existing page** instead of creating a new one:

```bash
curl -X PATCH https://renderkit.live/v1/render/$RENDER_ID \
  -H "Authorization: Bearer $RENDERKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "merge",
    "context": "updated description of the content",
    "data": {
      "content": "new or additional data to merge in"
    }
  }'
```

   - `strategy: "merge"` — deep-merges new data into existing data (best for adding sections)
   - `strategy: "replace"` — swaps all data with the new payload (best for rewrites)
   - The page URL stays the same, so any links the user already has still work

**Rule of thumb:** if you rendered a page in this conversation, prefer PATCH over POST for follow-up changes.

### Key Details

- **Include URLs inline** in your data — they are automatically enriched with images, ratings, and metadata
- **Format options**: `url` (default, hosted page) or `html` (raw HTML string)
- **Templates**: `travel_itinerary`, `freeform` (more coming)
- **Theme**: optionally pass `"theme": { "mode": "dark", "palette": ["#color1", "#color2"] }`
- **Full API docs**: https://renderkit.live/docs.md

## Forms — Data Collection (`/v1/forms`)

**Use this whenever the goal is to collect input from people.** This includes surveys, RSVPs, feedback, signups, configuration forms, questionnaires, order forms, polls, registrations — anything where someone fills in fields and submits. Do NOT use `/v1/render` for this.

Create a hosted form:

```bash
curl -X POST https://renderkit.live/v1/forms \
  -H "Authorization: Bearer $RENDERKIT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Event RSVP",
    "prompt": "Create an RSVP form for a dinner party. Ask for name, email, dietary restrictions, and plus-one.",
    "multi_response": true,
    "expires_in": 604800
  }'
```

The API returns a `url` to share with respondents. You can also provide explicit `fields` instead of a `prompt`.

- **Poll for responses:** `GET /v1/forms/{form_id}/status`
- **Retrieve responses:** `GET /v1/forms/{form_id}/responses`
- **Close form:** `DELETE /v1/forms/{form_id}`

The form URL (`/f/{slug}`) hosts a fully interactive form with validation and response storage.

Forms share the same API key and quota as renders. Full docs: https://renderkit.live/docs.md
