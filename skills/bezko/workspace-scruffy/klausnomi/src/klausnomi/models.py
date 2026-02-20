"""Data models for Nomi API responses."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Nomi:
    """Represents a Nomi AI companion."""
    uuid: str
    name: str
    gender: str
    profile: str
    created: str
    updated: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Nomi:
        """Create Nomi from API response dict."""
        return cls(
            uuid=data.get("uuid", ""),
            name=data.get("name", ""),
            gender=data.get("gender", ""),
            profile=data.get("profile", ""),
            created=data.get("created", ""),
            updated=data.get("updated", ""),
        )


@dataclass
class Room:
    """Represents a Nomi room/conversation group."""
    uuid: str
    name: str
    nomi_uuids: list[str] = field(default_factory=list)
    created: str = ""
    updated: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Room:
        """Create Room from API response dict."""
        return cls(
            uuid=data.get("uuid", ""),
            name=data.get("name", ""),
            nomi_uuids=data.get("nomiUuids", []),
            created=data.get("created", ""),
            updated=data.get("updated", ""),
        )


@dataclass
class Message:
    """Represents a message in a conversation."""
    text: str
    sender: str
    timestamp: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Message:
        """Create Message from API response dict."""
        return cls(
            text=data.get("text", ""),
            sender=data.get("sender", ""),
            timestamp=data.get("timestamp", ""),
        )


@dataclass
class ChatResponse:
    """Response from sending a chat message."""
    reply_message: Message
    conversation_id: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ChatResponse:
        """Create ChatResponse from API response dict."""
        reply_data = data.get("replyMessage", {})
        return cls(
            reply_message=Message.from_dict(reply_data),
            conversation_id=data.get("conversationId", ""),
        )
