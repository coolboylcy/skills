# AGENTS.md - OpenClaw Nomi Plugin

## Setup Commands:
- Install deps: `uv venv`
- Activate environment: `source .uv/bin/activate`
- Set API key: `export NOMI_API_KEY=YourAPITokenHere`

## Development Notes:
- Uses `curl` and `jq` for API interactions
- Plaintext-only response workflows
- No authentication handling (requires user-set env var)

## Testing Instructions:
- Verify API key: `curl -H "Authorization: $NOMI_API_KEY" https://api.nomi.ai/v1/nomis`
- Check script execution: `nomi list | jq .`
- Example chat: `nomi chat <uuid> "test"`

## Code Style:
- Follows BankrBot skill patterns (script + SKILL.md)
- **Commands**: `nomi list`, `nomi chat <uuid> <message>`
- Keep scripts lean (curl wrappers with jq)

## TODO:
- [ ] Complete `dchat()` function in scripts/nomi.sh (currently incomplete)
- [ ] Add main dispatch logic (case statement for `list`/`chat` subcommands)
- [ ] Add SKILL.md for proper OpenClaw skill integration

## Security:
- Never commit API keys to repositories
- Regenerate keys if exposed

---
## BankrBot Reference
[https://github.com/BankrBot/openclaw-skills/tree/main/bankr](https://github.com/BankrBot/openclaw-skills/tree/main/bankr)

---
## Nomi API Documentation
**Base URL**: https://api.nomi.ai/v1/

**Endpoints**:
- `GET /nomis` - List agents
- `POST /nomis/{uuid}/chat` - Send messages

**Usage**:
```bash
# List agents
nomi list

# Send message
nomi chat <uuid> "Your message here"
```

**Key**: Required `Authorization: Bearer` header