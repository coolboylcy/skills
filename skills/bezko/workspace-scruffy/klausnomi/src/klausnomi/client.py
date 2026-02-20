"""HTTP Client for Nomi AI API."""

from __future__ import annotations

import os
from typing import Any

import httpx

from klausnomi.models import Nomi, Room, ChatResponse


class NomiAPIError(Exception):
    """Exception raised for Nomi API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class NomiClient:
    """Client for interacting with the Nomi AI API."""

    BASE_URL = "https://api.nomi.ai/v1"

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize client with API key.

        Args:
            api_key: Nomi API key. If not provided, reads from NOMI_API_KEY env var.

        Raises:
            NomiAPIError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.environ.get("NOMI_API_KEY")
        if not self.api_key:
            raise NomiAPIError(
                "NOMI_API_KEY environment variable is not set. "
                "Fix: export NOMI_API_KEY=your_api_key"
            )

        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": self.api_key,
                "Accept": "application/json",
            },
            timeout=120.0,
        )

    def _auth_header(self) -> dict[str, str]:
        """Get authorization header with Bearer token format.

        Returns:
            Dictionary containing the Authorization header with Bearer token.

        Raises:
            NomiAPIError: If the API key is not set.
        """
        if self.api_key is None:
            raise NomiAPIError("API key is not set")
        return {"Authorization": f"Bearer {self.api_key}"}

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: API endpoint path.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            JSON response as a dictionary.

        Raises:
            NomiAPIError: If the request fails or returns an error status.
        """
        try:
            response = await self._client.request(method, path, **kwargs)
        except httpx.RequestError as e:
            raise NomiAPIError(
                f"Network request failed: {type(e).__name__}: {e}"
            ) from e

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise NomiAPIError(
                f"API request failed: {e.response.text}",
                status_code=e.response.status_code,
            ) from e

        # Handle empty responses (e.g., DELETE requests)
        if not response.content:
            return {}

        result: dict[str, Any] = response.json()
        return result

    # ============================
    # NOMI ENDPOINTS
    # ============================

    async def list_nomis(self) -> list[Nomi]:
        """List all Nomis.

        Returns:
            List of Nomi objects.
        """
        data = await self._request("GET", "/nomis")
        nomis_data = data.get("nomis", [])
        return [Nomi.from_dict(n) for n in nomis_data]

    async def get_nomi(self, uuid: str) -> Nomi:
        """Get a specific Nomi by UUID.

        Args:
            uuid: The Nomi's UUID.

        Returns:
            Nomi object.
        """
        data = await self._request("GET", f"/nomis/{uuid}")
        return Nomi.from_dict(data)

    async def get_avatar(self, uuid: str) -> bytes:
        """Get a Nomi's avatar image.

        Args:
            uuid: The Nomi's UUID.

        Returns:
            Avatar image bytes (WebP format).

        Raises:
            NomiAPIError: If the request fails.
        """
        try:
            response = await self._client.get(f"/nomis/{uuid}/avatar")
            response.raise_for_status()
        except httpx.RequestError as e:
            raise NomiAPIError(f"Network request failed: {e}") from e
        except httpx.HTTPStatusError as e:
            raise NomiAPIError(
                f"API request failed: {e.response.text}",
                status_code=e.response.status_code,
            ) from e
        return response.content

    async def chat_with_nomi(self, uuid: str, message: str) -> ChatResponse:
        """Send a message to a Nomi.

        Args:
            uuid: The Nomi's UUID.
            message: Message text to send.

        Returns:
            ChatResponse containing the reply.
        """
        payload = {"messageText": message}
        data = await self._request(
            "POST",
            f"/nomis/{uuid}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        return ChatResponse.from_dict(data)

    async def get_reply(self, uuid: str, message: str) -> str:
        """Send a message and return just the reply text.

        Args:
            uuid: The Nomi's UUID.
            message: Message text to send.

        Returns:
            Reply text string.
        """
        response = await self.chat_with_nomi(uuid, message)
        return response.reply_message.text

    # ============================
    # ROOM ENDPOINTS
    # ============================

    async def list_rooms(self) -> list[Room]:
        """List all rooms.

        Returns:
            List of Room objects.
        """
        data = await self._request("GET", "/rooms")
        rooms_data = data.get("rooms", [])
        return [Room.from_dict(r) for r in rooms_data]

    async def get_room(self, uuid: str) -> Room:
        """Get a specific room by UUID.

        Args:
            uuid: The room's UUID.

        Returns:
            Room object.
        """
        data = await self._request("GET", f"/rooms/{uuid}")
        return Room.from_dict(data)

    async def create_room(self, name: str, nomi_uuids: list[str]) -> Room:
        """Create a new room.

        Args:
            name: Room name.
            nomi_uuids: List of Nomi UUIDs to add to the room.

        Returns:
            Created Room object.
        """
        payload = {
            "name": name,
            "nomiUuids": nomi_uuids,
            "backchannelingEnabled": False,
            "note": "Created via KlausNomi CLI",
        }
        data = await self._request(
            "POST",
            "/rooms",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        return Room.from_dict(data)

    async def update_room(
        self,
        uuid: str,
        name: str | None = None,
        nomi_uuids: list[str] | None = None,
    ) -> Room:
        """Update a room.

        Args:
            uuid: The room's UUID.
            name: New room name (optional).
            nomi_uuids: New list of Nomi UUIDs (optional).

        Returns:
            Updated Room object.
        """
        payload: dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if nomi_uuids is not None:
            payload["nomiUuids"] = nomi_uuids

        data = await self._request(
            "PUT",
            f"/rooms/{uuid}",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        return Room.from_dict(data)

    async def delete_room(self, uuid: str) -> None:
        """Delete a room.

        Args:
            uuid: The room's UUID.

        Returns:
            None

        Raises:
            NomiAPIError: If the request fails.
        """
        await self._request("DELETE", f"/rooms/{uuid}")

    async def chat_in_room(self, uuid: str, message: str) -> ChatResponse:
        """Send a message to a room.

        Args:
            uuid: The room's UUID.
            message: Message text to send.

        Returns:
            ChatResponse containing the reply.
        """
        payload = {"messageText": message}
        data = await self._request(
            "POST",
            f"/rooms/{uuid}/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        return ChatResponse.from_dict(data)

    async def request_nomi_chat(self, room_uuid: str, nomi_uuid: str) -> dict[str, Any]:
        """Request a specific Nomi to chat in a room.

        Args:
            room_uuid: The room's UUID.
            nomi_uuid: The Nomi's UUID.

        Returns:
            Dictionary containing the API response with the Nomi's reply.

        Raises:
            NomiAPIError: If the request fails.
        """
        payload = {"nomiUuid": nomi_uuid}
        return await self._request(
            "POST",
            f"/rooms/{room_uuid}/chat/request",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

    async def close(self) -> None:
        """Close the HTTP client and release resources.

        Returns:
            None
        """
        await self._client.aclose()

    async def __aenter__(self) -> NomiClient:
        """Async context manager entry.

        Returns:
            The NomiClient instance.
        """
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit.

        Args:
            *args: Exception information (exc_type, exc_val, exc_tb).

        Returns:
            None
        """
        await self.close()
