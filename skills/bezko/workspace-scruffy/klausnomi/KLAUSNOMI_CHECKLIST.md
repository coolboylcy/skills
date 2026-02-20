# KlausNomi Technical Debt Checklist

## Critical Vulnerabilities Fixed

### 1. Authentication Risk - ✅ FIXED
- **Issue**: `_auth_header()` returned raw API key without Bearer prefix
- **Fix**: Updated to return `{"Authorization": f"Bearer {self.api_key}"}`
- **File**: `src/klausnomi/client.py` - `_auth_header()` method
- **Test Added**: `test_auth_header_returns_bearer_format()`

### 2. Error Handling Gap - ✅ FIXED
- **Issue**: `_request()` didn't catch `httpx.RequestError` (network-level failures)
- **Fix**: Added try/except block to catch `httpx.RequestError` and convert to `NomiAPIError`
- **File**: `src/klausnomi/client.py` - `_request()` method
- **Test Added**: `test_request_error_raises_nomi_api_error()`

### 3. HTTP Header Redundancy - ✅ FIXED
- **Issue**: `get_avatar()` added duplicate Authorization header (client already has it)
- **Fix**: Removed manual header addition; client default headers now handle auth
- **File**: `src/klausnomi/client.py` - `get_avatar()` method
- **Impact**: Eliminates duplicate header warning from some HTTP servers

### 4. CLI Performance Issue - ✅ FIXED
- **Issue**: `handle_nomi_show()` used O(n) list iteration instead of O(1) direct lookup
- **Fix**: Changed to use `client.get_nomi()` for direct UUID lookup
- **File**: `src/klausnomi/cli.py` - `handle_nomi_show()` function
- **Tests Added**: `test_handle_nomi_show_uses_get_nomi()`, `test_handle_nomi_show_not_found()`

### 5. Documentation Debt - ✅ FIXED (8 Issues)

| # | File | Function | Issue | Fix |
|---|------|----------|-------|-----|
| 1 | `client.py` | `_auth_header()` | Missing Returns section | Added complete docstring with Returns, Raises |
| 2 | `client.py` | `_request()` | Missing Args/Returns/Raises | Added complete docstring |
| 3 | `client.py` | `get_avatar()` | Missing Raises section | Added Raises documentation |
| 4 | `client.py` | `delete_room()` | Missing Returns section | Added Returns documentation |
| 5 | `client.py` | `request_nomi_chat()` | Vague Returns description | Clarified return value description |
| 6 | `client.py` | `close()` | Missing Returns section | Added Returns documentation |
| 7 | `client.py` | `__aenter__`/`__aexit__` | Missing complete docstrings | Added Args/Returns documentation |
| 8 | `cli.py` | `format_nomi()` | Missing Args/Returns | Added complete docstring |
| 9 | `cli.py` | `async_main()` | Missing Args/Returns | Added complete docstring |
| 10 | `cli.py` | `main()` | Missing docstring | Added complete docstring |
| 11 | `cli.py` | `handle_nomi_show()` | Missing Args/Returns | Added complete docstring |
| 12 | `cli.py` | `handle_room_delete()` | Missing Args/Returns | Added complete docstring |

## Test Coverage

- All new functionality has corresponding tests
- Existing tests continue to pass
- New tests added:
  - `test_auth_header_returns_bearer_format()`
  - `test_request_error_raises_nomi_api_error()`
  - `test_handle_nomi_show_uses_get_nomi()`
  - `test_handle_nomi_show_not_found()`

## Cross-File Synchronization

- ✅ `src/klausnomi/client.py` - Updated
- ✅ `src/klausnomi/cli.py` - Updated
- ✅ `tests/test_klausnomi.py` - Updated with new tests
- ✅ `skills/klausnomi/scripts/nomi.py` - Portable CLI (separate concern, uses urllib not httpx)

## Verification

Run tests to verify all fixes:
```bash
cd /home/openclaw/.openclaw/workspace-scruffy/klausnomi
python -m pytest tests/ -v
```
