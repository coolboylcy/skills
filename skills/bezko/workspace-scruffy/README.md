# KlausNomi

Python CLI for Nomi AI API integration with MCP (Model Context Protocol) support.

## Installation

### From PyPI (when published)

```bash
pip install klausnomi
```

### From source (using uv)

```bash
git clone https://github.com/openclaw/klausnomi.git
cd klausnomi
uv venv venv   # create a virtual environment with uv
source venv/bin/activate
uv pip install -e .   # install the package and its dependencies using uv
```

# Optional: If you have a uv lock file, you can sync directly:
# uv sync

## Configuration

Set your Nomi API key as an environment variable:

```bash
export NOMI_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface

The `nomi` command provides full access to the Nomi AI API:

#### Nomi Commands

```bash
# List all your Nomis
nomi list

# Get details of a specific Nomi
nomi get d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763

# Send a message to a Nomi
nomi chat d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763 "Hello there!"

# Send message and get just the reply text
nomi reply d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763 "How are you today?"

# Download a Nomi's avatar (checks that the response is an image)
nomi avatar d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763
nomi avatar d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763 custom-name.webp
```

#### Room Commands

```bash
# List all rooms
nomi room list

# Get room details
nomi room get room-uuid-here

# Create a new room
nomi room create "My Group Chat" nomi-uuid-1 nomi-uuid-2 nomi-uuid-3

# Update a room
nomi room update room-uuid --name "New Name" --nomi-uuids uuid1 uuid2

# Delete a room
nomi room delete room-uuid

# Send a message to a room
nomi room chat room-uuid "Hey everyone!"

# Request a specific Nomi to chat in a room
nomi room request room-uuid nomi-uuid
```

#### JSON Output

All commands support JSON output with the `--json` flag:

```bash
nomi --json list
nomi --json get d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763
nomi room --json list
```

### Python API

Use the async client directly in your Python code:

```python
import asyncio
from klausnomi import NomiClient

async def main():
    async with NomiClient() as client:
        # List all Nomis
        nomis = await client.list_nomis()
        for nomi in nomis:
            print(f"{nomi.name}: {nomi.uuid}")
        
        # Chat with a Nomi
        response = await client.chat_with_nomi(
            "d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763",
            "Hello! How are you?"
        )
        print(response.reply_message.text)
        
        # Create a room (now allows optional backchanneling and note)
        room = await client.create_room(
            "My Group",
            ["nomi-uuid-1", "nomi-uuid-2"],
            backchanneling_enabled=False,
            note="Created via KlausNomi CLI",
        )
        print(f"Created room: {room.uuid}")
        
        # Chat in a room
        await client.chat_in_room(room.uuid, "Hello everyone!")

asyncio.run(main())
```

### MCP Server Integration

KlausNomi includes MCP (Model Context Protocol) integration for use with AI assistants. **Note:** the MCP server implementation is still a TODO placeholder – see `src/klausnomi/mcp.py` for details.

```python
from klausnomi import NomiClient
from klausnomi.mcp import NomiMCPServer

# Start the MCP server (currently a stub)
server = NomiMCPServer()
server.run()
```

## Development

```bash
# Clone the repository
git clone https://github.com/openclaw/klausnomi.git
cd klausnomi

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check src/

# Run type checker
mypy src/klausnomi
```

## Project Structure

```
klausnomi/
├── src/
│   └── klausnomi/
│       ├── __init__.py       # Package initialization
│       ├── __main__.py       # Entry point for python -m klausnomi
│       ├── client.py         # HTTP client for Nomi API
│       ├── models.py         # Data models
│       ├── cli.py            # Command-line interface
│       └── mcp.py            # MCP server integration (TODO)
├── tests/
│   └── test_klausnomi.py     # Test suite
├── pyproject.toml            # Project configuration
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Contributing

We welcome contributions! Please see the `CONTRIBUTING.md` file for guidelines on setting up a development environment, running tests, and submitting pull requests.

## License

MIT License - See LICENSE file for details.

## API Documentation

For full Nomi AI API documentation, visit: https://api.nomi.ai/docs
