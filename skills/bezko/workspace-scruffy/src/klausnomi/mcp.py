"""MCP (Model Context Protocol) server integration for KlausNomi.

This module provides MCP server capabilities for integrating Nomi AI
with AI assistants that support the Model Context Protocol.

TODO: Integrate with mcporter when available on PyPI.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from klausnomi.client import NomiClient


class NomiMCPServer:
    """MCP server for Nomi AI integration.
    
    This is a placeholder implementation. When mcporter is available,
    this will be updated to use the official MCP SDK.
    
    Example:
        server = NomiMCPServer()
        server.run()
    """
    
    def __init__(self, api_key: str | None = None) -> None:
        """Initialize the MCP server.
        
        Args:
            api_key: Nomi API key. If not provided, reads from NOMI_API_KEY env var.
        """
        self.client = NomiClient(api_key=api_key)
    
    async def handle_list_tools(self) -> list[dict[str, Any]]:
        """List available tools.
        
        Returns:
            List of tool definitions.
        """
        return [
            {
                "name": "nomi_list",
                "description": "List all your Nomis",
                "parameters": {},
            },
            {
                "name": "nomi_chat",
                "description": "Send a message to a Nomi",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uuid": {"type": "string", "description": "Nomi UUID"},
                        "message": {"type": "string", "description": "Message to send"},
                    },
                    "required": ["uuid", "message"],
                },
            },
            {
                "name": "room_list",
                "description": "List all rooms",
                "parameters": {},
            },
            {
                "name": "room_chat",
                "description": "Send a message to a room",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uuid": {"type": "string", "description": "Room UUID"},
                        "message": {"type": "string", "description": "Message to send"},
                    },
                    "required": ["uuid", "message"],
                },
            },
        ]
    
    async def handle_call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        """Call a tool.
        
        Args:
            name: Tool name.
            arguments: Tool arguments.
            
        Returns:
            Tool result.
        """
        async with self.client:
            if name == "nomi_list":
                nomis = await self.client.list_nomis()
                return {
                    "content": [
                        {"type": "text", "text": json.dumps([n.__dict__ for n in nomis])}
                    ]
                }
            
            elif name == "nomi_chat":
                response = await self.client.chat_with_nomi(
                    arguments["uuid"],
                    arguments["message"],
                )
                return {
                    "content": [
                        {"type": "text", "text": response.reply_message.text}
                    ]
                }
            
            elif name == "room_list":
                rooms = await self.client.list_rooms()
                return {
                    "content": [
                        {"type": "text", "text": json.dumps([r.__dict__ for r in rooms])}
                    ]
                }
            
            elif name == "room_chat":
                response = await self.client.chat_in_room(
                    arguments["uuid"],
                    arguments["message"],
                )
                return {
                    "content": [
                        {"type": "text", "text": response.reply_message.text}
                    ]
                }
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle an incoming MCP request.
        
        Expected request format (JSON):
        {
            "method": "list_tools" | "call_tool",
            "params": {
                "name": "tool_name",               # for call_tool
                "arguments": { ... }               # for call_tool
            }
        }
        """
        data = await reader.read(8192)
        if not data:
            writer.close()
            await writer.wait_closed()
            return
        try:
            request = json.loads(data.decode())
            method = request.get("method")
            if method == "list_tools":
                result = await self.handle_list_tools()
                response = {"result": result}
            elif method == "call_tool":
                params = request.get("params", {})
                name = params.get("name")
                arguments = params.get("arguments", {})
                result = await self.handle_call_tool(name, arguments)
                response = {"result": result}
            else:
                response = {"error": f"Unknown method: {method}"}
        except Exception as e:
            response = {"error": str(e)}
        writer.write(json.dumps(response).encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    def run(self) -> None:
        """Run a minimal TCP MCP server.
        
        The server listens on localhost:8000 and accepts JSON-encoded requests.
        Supported methods:
        - "list_tools" → returns the list of tool definitions.
        - "call_tool" with params {"name": "tool_name", "arguments": {...}} → invokes the tool.
        """
        async def _serve():
            server = await asyncio.start_server(
                self._handle_client,
                host="127.0.0.1",
                port=8000,
            )
            addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
            print(f"MCP server listening on {addrs}")
            async with server:
                await server.serve_forever()
        try:
            asyncio.run(_serve())
        except KeyboardInterrupt:
            print("\nMCP server stopped by user")


if __name__ == "__main__":
    server = NomiMCPServer()
    server.run()
