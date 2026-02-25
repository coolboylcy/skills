---
name: API (Stripe, OpenAI, Notion & 100+ more)
slug: api
version: 1.2.1
homepage: https://clawic.com/skills/api
description: Integrate 100+ REST APIs with secure multi-account credential management. GitHub, Twilio, Slack, HubSpot, Shopify, and more.
changelog: Multi-account credential system, dynamic API discovery, 100+ documented APIs.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"anyBins":["curl","jq"]},"os":["linux","darwin","win32"]}}
---

# API

Integrate any API fast. 100+ services documented with authentication, endpoints, and gotchas.

## Setup

On first use, read `setup.md` for integration guidelines and credential setup.

## When to Use

User needs to integrate a third-party API. Agent provides:
- Authentication setup with multi-account support
- Endpoint documentation with curl examples
- Rate limits, pagination patterns, and gotchas
- Credential naming conventions for multiple accounts

## Architecture

```
apis/                    # 100+ API reference files
  ├── stripe.md
  ├── openai.md
  ├── notion.md
  └── ...

~/api/                   # User preferences (created on first use)
  ├── preferences.md     # Default account selection, language
  └── accounts.md        # Registry of configured accounts
```

## Quick Reference

| File | Purpose |
|------|---------|
| `setup.md` | First-time setup and guidelines |
| `credentials.md` | Multi-account credential system |
| `memory-template.md` | Memory template for preferences |
| `auth.md` | Authentication pattern traps |
| `pagination.md` | Pagination pattern traps |
| `resilience.md` | Retry and error handling |
| `webhooks.md` | Webhook security patterns |
| `apis/{service}.md` | API-specific documentation |

## Core Rules

1. **Check API docs first** — Read `apis/{service}.md` before making any call. Each file has auth, endpoints, rate limits, and gotchas specific to that service.

2. **Use multi-account credentials** — Store credentials with naming format `{SERVICE}_{ACCOUNT}_{TYPE}`. Example: `STRIPE_PROD_API_KEY`, `STRIPE_TEST_API_KEY`, `STRIPE_CLIENT_ACME_API_KEY`.

3. **Always include Content-Type** — POST/PUT/PATCH requests need `Content-Type: application/json`. Omitting causes silent 415 errors on many APIs.

4. **Handle rate limits proactively** — Track `X-RateLimit-Remaining` header. Throttle before hitting 0, don't wait for 429. Respect `Retry-After` header.

5. **Validate response schema** — Some APIs return 200 with error in body. Always check response structure, not just status code.

6. **Use idempotency keys** — For payments and critical operations, include idempotency key to prevent duplicates on retry.

7. **Never log credentials** — Use environment variables directly. Never echo, print, or commit credentials to files.

## Credential Management

Use environment variables with multi-account naming convention:

```bash
# Set for current session
export STRIPE_PROD_API_KEY="sk_live_xxx"

# Use in API call
curl https://api.stripe.com/v1/charges -H "Authorization: Bearer $STRIPE_PROD_API_KEY"
```

**Naming format:** `{SERVICE}_{ACCOUNT}_{TYPE}`
- `STRIPE_PROD_API_KEY` — Production
- `STRIPE_TEST_API_KEY` — Development  
- `STRIPE_CLIENT_ACME_API_KEY` — Client project

See `credentials.md` for persistent storage options and multi-account workflows.

## Available APIs (147)

All API documentation is in `apis/`. Categories include:

**AI/ML:** anthropic, openai, cohere, groq, mistral, perplexity, huggingface, replicate, stability, elevenlabs, deepgram, assemblyai, together, anyscale

**Payments:** stripe, paypal, square, plaid, chargebee, paddle, lemonsqueezy, recurly, wise, coinbase, binance, alpaca, polygon

**Communication:** twilio, sendgrid, mailgun, postmark, resend, mailchimp, slack, discord, telegram, zoom, sendbird, stream-chat, pusher, ably, onesignal, courier, knock, novu

**CRM/Sales:** salesforce, hubspot, pipedrive, attio, close, apollo, outreach, gong, drift, crisp, front, customer-io, braze, iterable, klaviyo

**Developer:** github, gitlab, bitbucket, vercel, netlify, railway, render, fly, digitalocean, heroku, cloudflare, circleci, pagerduty, launchdarkly, split, statsig

**Database/Auth:** supabase, firebase, planetscale, neon, upstash, mongodb, fauna, xata, convex, appwrite, clerk, auth0, workos, stytch

**Media:** cloudinary, mux, bunny, imgix, uploadthing, uploadcare, transloadit, vimeo, youtube, spotify, unsplash, pexels, giphy, tenor

**Social:** twitter, linkedin, instagram, tiktok, pinterest, reddit, twitch

**Productivity:** notion, airtable, google-sheets, google-drive, google-calendar, dropbox, linear, jira, asana, trello, monday, clickup, figma, calendly, cal, loom, typeform

**Other:** shopify, docusign, hellosign, bitly, dub, openweather, mapbox, google-maps, intercom, zendesk, freshdesk, helpscout, mixpanel, amplitude, posthog, segment, sentry, datadog, algolia

```bash
# List all APIs
ls apis/

# Search by name
ls apis/ | grep -i payment

# Read specific API
cat apis/stripe.md
```

## Common Traps

- **Missing Content-Type** — POST without `Content-Type: application/json` causes silent 415 errors
- **API keys in URLs** — Query params get logged in access logs, always use headers
- **Ignoring pagination** — Most APIs default to 10-25 items, always paginate
- **Not handling 429** — Implement exponential backoff with jitter
- **Assuming 200 = success** — Check response body for error objects
- **No idempotency keys** — Retries cause duplicate charges/actions
- **Hardcoding credentials** — Use environment variables, never hardcode in source code

## External Endpoints

This skill documents how to call external APIs. Calls go directly from your machine to the API provider. No data is proxied or stored.

| Provider | Base URL | Auth |
|----------|----------|------|
| Various | See `apis/{service}.md` | API Key / OAuth |

## Security & Privacy

**Credentials:** Stored in environment variables with naming convention `{SERVICE}_{ACCOUNT}_{TYPE}`.

**Multi-account:** Each account isolated with unique environment variable names. Naming convention prevents conflicts.

**This skill does NOT:**
- Store credentials in files
- Make requests on your behalf
- Send data to any third party
- Proxy API calls

You control all API calls directly.

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `http` — HTTP request patterns and debugging
- `webhook` — Webhook handling and security
- `json` — JSON processing and jq patterns

## Feedback

- If useful: `clawhub star api`
- Stay updated: `clawhub sync`
