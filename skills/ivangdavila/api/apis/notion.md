# Notion

## Base URL
```
https://api.notion.com/v1
```

## Authentication
```bash
curl https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

Note: `Notion-Version` header is required.

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /pages | POST | Create page |
| /pages/:id | GET | Get page |
| /pages/:id | PATCH | Update page |
| /databases/:id/query | POST | Query database |
| /databases | POST | Create database |
| /blocks/:id/children | GET | Get blocks |
| /blocks/:id/children | PATCH | Append blocks |
| /search | POST | Search pages/databases |

## Quick Examples

### Query Database
```bash
curl -X POST "https://api.notion.com/v1/databases/DB_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "property": "Status",
      "select": {"equals": "Done"}
    }
  }'
```

### Create Page
```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "DB_ID"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Page"}}]},
      "Status": {"select": {"name": "In Progress"}}
    }
  }'
```

### Update Page Properties
```bash
curl -X PATCH "https://api.notion.com/v1/pages/PAGE_ID" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Status": {"select": {"name": "Done"}}
    }
  }'
```

### Append Block Content
```bash
curl -X PATCH "https://api.notion.com/v1/blocks/PAGE_ID/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "paragraph": {
          "rich_text": [{"text": {"content": "Hello World"}}]
        }
      }
    ]
  }'
```

### Search
```bash
curl -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "meeting notes"}'
```

## Property Types

| Type | Example Value |
|------|---------------|
| title | `{"title": [{"text": {"content": "..."}}]}` |
| rich_text | `{"rich_text": [{"text": {"content": "..."}}]}` |
| number | `{"number": 42}` |
| select | `{"select": {"name": "Option"}}` |
| multi_select | `{"multi_select": [{"name": "Tag1"}]}` |
| date | `{"date": {"start": "2024-01-01"}}` |
| checkbox | `{"checkbox": true}` |
| url | `{"url": "https://..."}` |
| email | `{"email": "user@example.com"}` |

## Common Traps

- Always include `Notion-Version` header
- Page IDs can have dashes or not (both work)
- Database queries return max 100 items (paginate with `start_cursor`)
- Integration must be shared with pages/databases to access them
- Rich text is always an array, even for single text

## Rate Limits

- 3 requests/second per integration
- Pagination: 100 items max per request

## Official Docs
https://developers.notion.com/reference
