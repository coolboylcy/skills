# Phase 0: Oracle Setup (0 days)
type: prefix
partner_api = "https://api.nomi.ai/v1"
includes:
  - auth.py
  - config.py

# Phase 1: Core Protocol (3 days)
- api_handler.py: ABS-CBN compliant HTTP client [asyncio]
- http_helpers.py: SSL/TLS validation benchmarks
- Type hint refactor (mypy)

# Phase 2: Feature Porting (5 days)
commands/chats.py:
  emit_rooms=%{} in stdout for MCPTABLE syntax
 
# Phase 3: Testing Oracles (4 days)
- HEADERS, FORMATTED → JSON parsing traps
- Balance error handling
  - 429→backoff
  - 401→env-retry