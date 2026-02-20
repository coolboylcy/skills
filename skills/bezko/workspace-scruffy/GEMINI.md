# GEMINI.md - KlausNomi Project Context

## Project Overview
**KlausNomi** is a Python-based CLI and client library designed for integrating with the [Nomi AI API](https://api.nomi.ai/docs). It provides full coverage of the Nomi v1 API, including Nomi management, chat interactions, and room (group) operations. The project also features a preliminary **Model Context Protocol (MCP)** server for integration with AI assistants.

### Key Technologies
- **Language:** Python 3.9+
- **HTTP Client:** `httpx` (async)
- **Data Modeling:** Python `dataclasses`
- **CLI Framework:** Custom implementation in `src/klausnomi/cli.py`
- **Testing:** `pytest` with `pytest-asyncio`
- **Linting/Typing:** `ruff`, `mypy`

## Project Structure
- `src/klausnomi/`: Core Python package.
    - `client.py`: `NomiClient` async HTTP client for API interactions.
    - `models.py`: `dataclass` definitions for Nomi, Room, Message, and ChatResponse.
    - `cli.py`: Implementation of the `nomi` and `klausnomi` command-line tools.
    - `mcp.py`: Placeholder TCP-based MCP server implementation.
    - `__main__.py`: Entry point for `python -m klausnomi`.
- `tests/`: Integration and unit tests.
- `scripts/nomi.sh`: A standalone Bash implementation of the Nomi API for lightweight use.
- `AGENTS.md`, `SKILL.md`, `production_plan.md`: Documentation and planning for OpenClaw integration.

## Building and Running

### Development Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Environment Variables
- `NOMI_API_KEY`: Required for all API operations.

### Key Commands
- **Run CLI:** `nomi <command>` or `python -m klausnomi <command>`
- **Run Tests:** `pytest`
- **Linting:** `ruff check src/`
- **Type Checking:** `mypy src/klausnomi`

## Development Conventions

### Code Style & Architecture
- **Asynchronous First:** All network-bound operations in the client and CLI use `asyncio` and `httpx`.
- **Data Models:** Favor `dataclasses` with `from_dict` class methods for deserializing API responses.
- **CLI Output:** Commands support both human-readable text and JSON output (via `--json`).
- **MCP Integration:** The MCP server in `mcp.py` is currently a placeholder TCP server. Future updates should aim for official MCP SDK integration.

### Testing Practices
- Tests use `pytest-asyncio` for handling async client calls.
- New features should include corresponding tests in the `tests/` directory.

### Contribution Guidelines
- Ensure all changes pass `ruff` linting and `mypy` type checks.
- Adhere to the async patterns established in `client.py`.
- Documentation in `README.md` and `SKILL.md` should be updated for any new CLI commands.
