---
name: ryot
description: Track and manage media consumption (TV shows, movies, books, anime, games) via Ryot API. Use when the user wants to mark content as watched/read/completed, search for media, check viewing progress, or log media activities. Triggers include requests like "mark X as completed", "did I watch Y?", "add Z to my list", "search for movie/show/book", or any media tracking tasks.
metadata:
  credentials:
    required:
      - name: RYOT_CONFIG
        description: Config file at /home/node/clawd/config/ryot.json with "url" (Ryot instance URL) and "api_token" (API authentication token)
        path: /home/node/clawd/config/ryot.json
        format: |
          {
            "url": "https://your-ryot-instance.com",
            "api_token": "your_api_token_here"
          }
---

# Ryot Media Tracker

Track TV shows, movies, books, anime, and games via the Ryot GraphQL API.

## Setup (Required)

Before using this skill, you must configure your Ryot instance:

1. **Create config file** at `/home/node/clawd/config/ryot.json`:

```json
{
  "url": "https://your-ryot-instance.com",
  "api_token": "your_api_token_here"
}
```

2. **Set your Ryot instance URL** - Replace `https://your-ryot-instance.com` with your actual Ryot server address
3. **Get your API token** from your Ryot instance settings
4. **Save the config** - The skill will read this file automatically

## Usage

Use `scripts/ryot_api.py` for all Ryot operations.

## Common Tasks

### 1. Mark Media as Completed

```bash
# Search for the item first
python3 scripts/ryot_api.py search "Breaking Bad" --type SHOW

# Mark as completed (uses metadata ID from search)
python3 scripts/ryot_api.py complete met_XXXXX
```

### 2. Search for Media

```bash
# Search for TV shows
python3 scripts/ryot_api.py search "The Wire" --type SHOW

# Search for movies
python3 scripts/ryot_api.py search "Inception" --type MOVIE

# Search for books
python3 scripts/ryot_api.py search "1984" --type BOOK

# Search for anime
python3 scripts/ryot_api.py search "Death Note" --type ANIME
```

### 3. Get Media Details

Verify metadata (title, year, etc.) before marking as completed:

```bash
python3 scripts/ryot_api.py details met_XXXXX
```

## Workflow

1. **User request** → "I finished watching Breaking Bad"
2. **Search** → Find the correct metadata ID
3. **Verify** → Check year/details if ambiguous
4. **Mark complete** → Deploy bulk progress update

## Media Types

Supported `lot` values:
- `SHOW` - TV series
- `MOVIE` - Films
- `BOOK` - Books
- `ANIME` - Anime series
- `GAME` - Video games

## Important Notes

- **Before first use:** Check if `/home/node/clawd/config/ryot.json` exists. If not, ask the user for their Ryot instance URL and API token, then create the config file.
- Always search first to get the correct metadata ID
- Verify the year if multiple results match the title
- The API uses GraphQL at `/backend/graphql`
- Metadata IDs start with `met_`

## Resources

### scripts/ryot_api.py

Python script for Ryot GraphQL operations. Supports:
- `search` - Find media by title
- `details` - Get metadata details
- `complete` - Mark as completed
