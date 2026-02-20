"""Tests for klausnomi."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json

from klausnomi.client import NomiClient, NomiAPIError
from klausnomi.models import Nomi, Room, ChatResponse, Message
from klausnomi import cli


class TestModels:
    """Test data models."""
    
    def test_nomi_from_dict(self) -> None:
        """Test Nomi model creation from dict."""
        data = {
            "uuid": "test-uuid-123",
            "name": "Test Nomi",
            "gender": "female",
            "profile": "A test profile",
            "created": "2024-01-01",
            "updated": "2024-01-02",
        }
        nomi = Nomi.from_dict(data)
        assert nomi.uuid == "test-uuid-123"
        assert nomi.name == "Test Nomi"
        assert nomi.gender == "female"
    
    def test_room_from_dict(self) -> None:
        """Test Room model creation from dict."""
        data = {
            "uuid": "room-uuid-123",
            "name": "Test Room",
            "nomiUuids": ["nomi-1", "nomi-2"],
            "created": "2024-01-01",
            "updated": "2024-01-02",
        }
        room = Room.from_dict(data)
        assert room.uuid == "room-uuid-123"
        assert room.name == "Test Room"
        assert room.nomi_uuids == ["nomi-1", "nomi-2"]
    
    def test_chat_response_from_dict(self) -> None:
        """Test ChatResponse model creation from dict."""
        data = {
            "replyMessage": {
                "text": "Hello there!",
                "sender": "nomi-1",
                "timestamp": "2024-01-01T00:00:00",
            },
            "conversationId": "conv-123",
        }
        response = ChatResponse.from_dict(data)
        assert response.reply_message.text == "Hello there!"
        assert response.conversation_id == "conv-123"


class TestClientAuth:
    """Test client authentication."""
    
    def test_client_requires_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that client requires API key."""
        monkeypatch.delenv("NOMI_API_KEY", raising=False)
        with pytest.raises(NomiAPIError, match="NOMI_API_KEY"):
            NomiClient()
    
    def test_client_accepts_api_key_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that client reads API key from environment."""
        monkeypatch.setenv("NOMI_API_KEY", "test-api-key")
        client = NomiClient()
        assert client.api_key == "test-api-key"
    
    def test_client_accepts_api_key_from_arg(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that client accepts API key as argument."""
        monkeypatch.delenv("NOMI_API_KEY", raising=False)
        client = NomiClient(api_key="test-api-key")
        assert client.api_key == "test-api-key"


@pytest.mark.asyncio
class TestClientMethods:
    """Test client API methods."""
    
    @pytest.fixture
    def mock_client(self, monkeypatch: pytest.MonkeyPatch) -> NomiClient:
        """Create a mocked client."""
        monkeypatch.setenv("NOMI_API_KEY", "test-key")
        client = NomiClient()
        client._client = AsyncMock()
        return client
    
    async def test_list_nomis(self, mock_client: NomiClient) -> None:
        """Test listing Nomis."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "nomis": [
                {"uuid": "1", "name": "Nomi 1", "gender": "female", "profile": "", "created": "", "updated": ""},
                {"uuid": "2", "name": "Nomi 2", "gender": "male", "profile": "", "created": "", "updated": ""},
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_client._client.request.return_value = mock_response
        
        nomis = await mock_client.list_nomis()
        assert len(nomis) == 2
        assert nomis[0].name == "Nomi 1"
    
    async def test_get_nomi(self, mock_client: NomiClient) -> None:
        """Test getting a specific Nomi."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "uuid": "test-uuid",
            "name": "Test Nomi",
            "gender": "female",
            "profile": "Test profile",
            "created": "2024-01-01",
            "updated": "2024-01-02",
        }
        mock_response.raise_for_status = MagicMock()
        mock_client._client.request.return_value = mock_response
        
        nomi = await mock_client.get_nomi("test-uuid")
        assert nomi.name == "Test Nomi"
    
    async def test_chat_with_nomi(self, mock_client: NomiClient) -> None:
        """Test chatting with a Nomi."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "replyMessage": {
                "text": "Hello!",
                "sender": "nomi-uuid",
                "timestamp": "2024-01-01",
            },
            "conversationId": "conv-123",
        }
        mock_response.raise_for_status = MagicMock()
        mock_client._client.request.return_value = mock_response
        
        response = await mock_client.chat_with_nomi("nomi-uuid", "Hi!")
        assert response.reply_message.text == "Hello!"
    
    async def test_create_room(self, mock_client: NomiClient) -> None:
        """Test creating a room."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "uuid": "room-uuid",
            "name": "Test Room",
            "nomiUuids": ["nomi-1", "nomi-2"],
            "created": "2024-01-01",
            "updated": "2024-01-01",
        }
        mock_response.raise_for_status = MagicMock()
        mock_client._client.request.return_value = mock_response
        
        room = await mock_client.create_room("Test Room", ["nomi-1", "nomi-2"])
        assert room.name == "Test Room"
        assert room.nomi_uuids == ["nomi-1", "nomi-2"]


class TestCLI:
    """Test CLI functionality."""
    
    def test_parser_creates_subcommands(self) -> None:
        """Test that parser creates all subcommands."""
        parser = cli.create_parser()
        
        # Test nomi commands
        args = parser.parse_args(["list"])
        assert args.command == "list"
        
        args = parser.parse_args(["get", "uuid-123"])
        assert args.command == "get"
        assert args.uuid == "uuid-123"
        
        args = parser.parse_args(["chat", "uuid-123", "Hello!"])
        assert args.command == "chat"
        assert args.message == "Hello!"
        
        # Test room commands
        args = parser.parse_args(["room", "list"])
        assert args.command == "room"
        assert args.room_command == "list"
        
        args = parser.parse_args(["room", "create", "My Room", "n1", "n2"])
        assert args.room_command == "create"
        assert args.name == "My Room"
        assert args.nomi_uuids == ["n1", "n2"]
    
    @pytest.mark.asyncio
    async def test_handle_nomi_list(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        """Test handling nomi list command."""
        monkeypatch.setenv("NOMI_API_KEY", "test-key")
        
        mock_client = AsyncMock()
        mock_client.list_nomis.return_value = [
            Nomi(uuid="1", name="Nomi 1", gender="female", profile="", created="", updated=""),
            Nomi(uuid="2", name="Nomi 2", gender="male", profile="", created="", updated=""),
        ]
        
        args = cli.create_parser().parse_args(["list"])
        await cli.handle_nomi_list(mock_client, args)
        
        captured = capsys.readouterr()
        assert "Nomi 1" in captured.out
        assert "Nomi 2" in captured.out
    
    @pytest.mark.asyncio
    async def test_handle_nomi_list_json(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        """Test handling nomi list command with JSON output."""
        monkeypatch.setenv("NOMI_API_KEY", "test-key")
        
        mock_client = AsyncMock()
        mock_client.list_nomis.return_value = [
            Nomi(uuid="1", name="Nomi 1", gender="female", profile="", created="", updated=""),
        ]
        
        args = cli.create_parser().parse_args(["--json", "list"])
        await cli.handle_nomi_list(mock_client, args)
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data) == 1
        assert data[0]["name"] == "Nomi 1"


class TestIntegration:
    """Integration tests."""
    
    @pytest.mark.asyncio
    async def test_main_no_command(self, capsys: pytest.CaptureFixture) -> None:
        """Test main with no command shows help."""
        result = await cli.async_main([])
        assert result == 1
        captured = capsys.readouterr()
        assert "usage:" in captured.out
    
    @pytest.mark.asyncio
    async def test_main_no_api_key(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        """Test main without API key shows error."""
        monkeypatch.delenv("NOMI_API_KEY", raising=False)
        result = await cli.async_main(["list"])
        assert result == 1
        captured = capsys.readouterr()
        assert "NOMI_API_KEY" in captured.err
