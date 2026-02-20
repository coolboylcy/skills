"""Command-line interface for KlausNomi."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Sequence

from klausnomi.client import NomiClient, NomiAPIError
from klausnomi.models import Nomi


def format_nomi(nomi: Nomi) -> str:
    """Format Nomi for display."""
    return f"{nomi.name} ({nomi.uuid}) - {nomi.gender}"


async def handle_nomi_list(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'nomi list' command."""
    nomis = await client.list_nomis()
    if args.json:
        print(json.dumps([n.__dict__ for n in nomis], indent=2))
    else:
        for nomi in nomis:
            print(format_nomi(nomi))
    return 0


async def handle_nomi_get(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'nomi get' command."""
    nomi = await client.get_nomi(args.uuid)
    if args.json:
        print(json.dumps(nomi.__dict__, indent=2))
    else:
        print(f"Name: {nomi.name}")
        print(f"UUID: {nomi.uuid}")
        print(f"Gender: {nomi.gender}")
        print(f"Profile: {nomi.profile}")
        print(f"Created: {nomi.created}")
        print(f"Updated: {nomi.updated}")
    return 0


async def handle_nomi_avatar(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'nomi avatar' command."""
    avatar_data = await client.get_avatar(args.uuid)
    output_path = Path(args.output or f"nomi-{args.uuid}-avatar.webp")
    output_path.write_bytes(avatar_data)
    print(f"Avatar saved to: {output_path}")
    return 0


async def handle_nomi_chat(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'nomi chat' command."""
    response = await client.chat_with_nomi(args.uuid, args.message)
    if args.json:
        print(json.dumps({
            "replyMessage": response.reply_message.__dict__,
            "conversationId": response.conversation_id,
        }, indent=2))
    else:
        print(response.reply_message.text)
    return 0


async def handle_nomi_reply(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'nomi reply' command."""
    reply = await client.get_reply(args.uuid, args.message)
    print(reply)
    return 0


async def handle_nomi_show(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'nomi show' command."""
    try:
        nomi = await client.get_nomi(args.uuid)
    except NomiAPIError as e:
        print(f"❌ Nomi with UUID {args.uuid} not found: {e}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(nomi.__dict__, indent=2))
    else:
        print(format_nomi(nomi))
    return 0


async def handle_room_list(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'room list' command."""
    rooms = await client.list_rooms()
    if args.json:
        print(json.dumps([r.__dict__ for r in rooms], indent=2))
    else:
        for room in rooms:
            print(f"{room.name} ({room.uuid})")
            print(f"  Nomis: {', '.join(room.nomi_uuids)}")
    return 0


async def handle_room_get(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'room get' command."""
    room = await client.get_room(args.uuid)
    if args.json:
        print(json.dumps(room.__dict__, indent=2))
    else:
        print(f"Name: {room.name}")
        print(f"UUID: {room.uuid}")
        print(f"Nomis: {', '.join(room.nomi_uuids)}")
        print(f"Created: {room.created}")
        print(f"Updated: {room.updated}")
    return 0


async def handle_room_create(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'room create' command."""
    room = await client.create_room(args.name, args.nomi_uuids)
    if args.json:
        print(json.dumps(room.__dict__, indent=2))
    else:
        print(f"Room created: {room.name} ({room.uuid})")
    return 0


async def handle_room_update(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'room update' command."""
    room = await client.update_room(
        args.uuid,
        name=args.name,
        nomi_uuids=args.nomi_uuids,
    )
    if args.json:
        print(json.dumps(room.__dict__, indent=2))
    else:
        print(f"Room updated: {room.name} ({room.uuid})")
    return 0


async def handle_room_delete(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'room delete' command."""
    await client.delete_room(args.uuid)
    print(f"Room {args.uuid} deleted")
    return 0


async def handle_room_chat(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'room chat' command."""
    response = await client.chat_in_room(args.uuid, args.message)
    if args.json:
        print(json.dumps({
            "replyMessage": response.reply_message.__dict__,
            "conversationId": response.conversation_id,
        }, indent=2))
    else:
        print(response.reply_message.text)
    return 0


async def handle_room_request(client: NomiClient, args: argparse.Namespace) -> int:
    """Handle 'room request' command."""
    result = await client.request_nomi_chat(args.room_uuid, args.nomi_uuid)
    print(json.dumps(result, indent=2))
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="nomi",
        description="KlausNomi - Python CLI for Nomi AI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ENVIRONMENT:
  NOMI_API_KEY    Your Nomi API key (required)

EXAMPLES:
  nomi list
  nomi get d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763
  nomi chat d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763 "Hello!"
  nomi reply d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763 "How are you?"
  room create "My Group" uuid1 uuid2 uuid3
  room chat room-uuid "Hey everyone!"
        """,
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # ============================
    # NOMI COMMANDS
    # ============================
    
    # nomi list
    subparsers.add_parser("list", help="List all your Nomis")
    
    # nomi get
    get_parser = subparsers.add_parser("get", help="Get details of a specific Nomi")
    get_parser.add_argument("uuid", help="Nomi UUID")
    
    # nomi avatar
    avatar_parser = subparsers.add_parser(
        "avatar",
        help="Download Nomi avatar",
    )
    avatar_parser.add_argument("uuid", help="Nomi UUID")
    avatar_parser.add_argument(
        "output",
        nargs="?",
        help="Output file path (default: nomi-{uuid}-avatar.webp)",
    )
    
    # nomi chat
    chat_parser = subparsers.add_parser(
        "chat",
        help="Send a message to a Nomi (returns full JSON)",
    )
    chat_parser.add_argument("uuid", help="Nomi UUID")
    chat_parser.add_argument("message", help="Message text")
    
    # nomi reply
    reply_parser = subparsers.add_parser(
        "reply",
        help="Send message and get reply text only",
    )
    reply_parser.add_argument("uuid", help="Nomi UUID")
    reply_parser.add_argument("message", help="Message text")
    
    # nomi show
    show_parser = subparsers.add_parser(
        "show",
        help="Show a Nomi from the list",
    )
    show_parser.add_argument("uuid", help="Nomi UUID")
    
    # ============================
    # ROOM COMMANDS
    # ============================
    
    room_parser = subparsers.add_parser("room", help="Room management commands")
    room_subparsers = room_parser.add_subparsers(
        dest="room_command",
        help="Room subcommands",
    )
    
    # room list
    room_subparsers.add_parser("list", help="List all rooms")
    
    # room get
    room_get_parser = room_subparsers.add_parser("get", help="Get room details")
    room_get_parser.add_argument("uuid", help="Room UUID")
    
    # room create
    room_create_parser = room_subparsers.add_parser(
        "create",
        help="Create a room with name and Nomi UUIDs",
    )
    room_create_parser.add_argument("name", help="Room name")
    room_create_parser.add_argument(
        "nomi_uuids",
        nargs="+",
        help="Nomi UUIDs to add to the room",
    )
    
    # room update
    room_update_parser = room_subparsers.add_parser(
        "update",
        help="Update room (name and/or Nomis)",
    )
    room_update_parser.add_argument("uuid", help="Room UUID")
    room_update_parser.add_argument(
        "--name",
        help="New room name",
    )
    room_update_parser.add_argument(
        "--nomi-uuids",
        nargs="+",
        help="New Nomi UUIDs",
    )
    
    # room delete
    room_delete_parser = room_subparsers.add_parser("delete", help="Delete a room")
    room_delete_parser.add_argument("uuid", help="Room UUID")
    
    # room chat
    room_chat_parser = room_subparsers.add_parser(
        "chat",
        help="Send message to room",
    )
    room_chat_parser.add_argument("uuid", help="Room UUID")
    room_chat_parser.add_argument("message", help="Message text")
    
    # room request
    room_request_parser = room_subparsers.add_parser(
        "request",
        help="Request a specific Nomi to chat in a room",
    )
    room_request_parser.add_argument("room_uuid", help="Room UUID")
    room_request_parser.add_argument("nomi_uuid", help="Nomi UUID")
    
    return parser


async def async_main(argv: Sequence[str] | None = None) -> int:
    """Main async entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 1
    
    try:
        client = NomiClient()
    except NomiAPIError as e:
        print(f"❌ ERROR: {e}", file=sys.stderr)
        return 1
    
    try:
        async with client:
            if args.command == "list":
                return await handle_nomi_list(client, args)
            elif args.command == "get":
                return await handle_nomi_get(client, args)
            elif args.command == "avatar":
                return await handle_nomi_avatar(client, args)
            elif args.command == "chat":
                return await handle_nomi_chat(client, args)
            elif args.command == "reply":
                return await handle_nomi_reply(client, args)
            elif args.command == "show":
                return await handle_nomi_show(client, args)
            elif args.command == "room":
                if args.room_command is None:
                    parser.print_help()
                    return 1
                elif args.room_command == "list":
                    return await handle_room_list(client, args)
                elif args.room_command == "get":
                    return await handle_room_get(client, args)
                elif args.room_command == "create":
                    return await handle_room_create(client, args)
                elif args.room_command == "update":
                    return await handle_room_update(client, args)
                elif args.room_command == "delete":
                    return await handle_room_delete(client, args)
                elif args.room_command == "chat":
                    return await handle_room_chat(client, args)
                elif args.room_command == "request":
                    return await handle_room_request(client, args)
                else:
                    print(f"❌ Unknown room command: {args.room_command}", file=sys.stderr)
                    return 1
            else:
                print(f"❌ Unknown command: {args.command}", file=sys.stderr)
                return 1
    except NomiAPIError as e:
        print(f"❌ API Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted", file=sys.stderr)
        return 130


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point."""
    return asyncio.run(async_main(argv))


if __name__ == "__main__":
    sys.exit(main())
