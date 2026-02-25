# Slack

## Base URL
```
https://slack.com/api
```

## Authentication
```bash
curl https://slack.com/api/auth.test \
  -H "Authorization: Bearer $SLACK_TOKEN"
```

## Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /chat.postMessage | POST | Send message |
| /conversations.list | GET | List channels |
| /conversations.history | GET | Get messages |
| /users.list | GET | List users |
| /users.info | GET | Get user |
| /files.upload | POST | Upload file |
| /reactions.add | POST | Add reaction |

## Quick Examples

### Send Message
```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0123456",
    "text": "Hello, world!"
  }'
```

### Send Message with Blocks
```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0123456",
    "blocks": [
      {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "*Bold* and _italic_"}
      }
    ]
  }'
```

### List Channels
```bash
curl "https://slack.com/api/conversations.list?types=public_channel,private_channel" \
  -H "Authorization: Bearer $SLACK_TOKEN"
```

### Get Channel History
```bash
curl "https://slack.com/api/conversations.history?channel=C0123456&limit=100" \
  -H "Authorization: Bearer $SLACK_TOKEN"
```

### Upload File
```bash
curl -X POST https://slack.com/api/files.upload \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -F file=@document.pdf \
  -F channels=C0123456 \
  -F title="My Document"
```

## Message Formatting

| Format | Syntax |
|--------|--------|
| Bold | `*text*` |
| Italic | `_text_` |
| Strike | `~text~` |
| Code | `` `code` `` |
| Link | `<https://url|text>` |
| User | `<@U0123456>` |
| Channel | `<#C0123456>` |

## Common Traps

- Always returns 200, check `ok` field in response
- Channel IDs start with C, user IDs with U
- Rate limit varies by method (Tier 1-4)
- files.upload v1 deprecated, use v2 for new code
- Private channels need bot to be invited

## Rate Limits

| Tier | Limit |
|------|-------|
| Tier 1 | 1/min |
| Tier 2 | 20/min |
| Tier 3 | 50/min |
| Tier 4 | 100/min |

## Official Docs
https://api.slack.com/methods
