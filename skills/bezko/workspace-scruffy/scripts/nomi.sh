#!/bin/bash

# OpenClaw Nomi Plugin
# Full Nomi AI API implementation
# API Docs: https://api.nomi.ai/docs

set -euo pipefail

BASE_URL="https://api.nomi.ai/v1"
API_KEY="${NOMI_API_KEY:-}"

# Check required tools
check_deps() {
  if ! command -v curl &> /dev/null; then
    echo "❌ Required tool missing: curl"
    exit 1
  fi
  if ! command -v jq &> /dev/null; then
    echo "❌ Required tool missing: jq"
    exit 1
  fi
}

# Verify API key
require_auth() {
  if [ -z "$API_KEY" ]; then
    echo "❌ ERROR: NOMI_API_KEY environment variable is not set"
    echo "Fix: export NOMI_API_KEY=your_api_key"
    exit 1
  fi
}

# Generate Authorization header
auth_header() {
  echo "Authorization: $API_KEY"
}

# ============================
# NOMI ENDPOINTS
# ============================

# List all Nomis
nomi_list() {
  curl -sS "$BASE_URL/nomis" \
    -H "$(auth_header)" \
    -H "Accept: application/json" | jq .
}

# Get specific Nomi
nomi_get() {
  local uuid="$1"
  curl -sS "$BASE_URL/nomis/$uuid" \
    -H "$(auth_header)" \
    -H "Accept: application/json" | jq .
}

# Get Nomi avatar (saves to file)
nomi_avatar() {
  local uuid="$1"
  local output="${2:-nomi-${uuid}-avatar.webp}"
  curl -sS "$BASE_URL/nomis/$uuid/avatar" \
    -H "$(auth_header)" \
    -o "$output"
  echo "Avatar saved to: $output"
}

# Send message to Nomi
nomi_chat() {
  local uuid="$1"
  local message="$2"
  local payload
  payload=$(jq -n --arg msg "$message" '{messageText: $msg}')
  
  curl -sS "$BASE_URL/nomis/$uuid/chat" \
    -H "$(auth_header)" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "$payload" | jq .
}

# ============================
# ROOM ENDPOINTS
# ============================

# List all rooms
room_list() {
  curl -sS "$BASE_URL/rooms" \
    -H "$(auth_header)" \
    -H "Accept: application/json" | jq .
}

# Get specific room
room_get() {
  local uuid="$1"
  curl -sS "$BASE_URL/rooms/$uuid" \
    -H "$(auth_header)" \
    -H "Accept: application/json" | jq .
}

# Create a room
room_create() {
  local name="$1"
  shift
  local nomi_uuids=()
  
  # Parse remaining args as nomi UUIDs or JSON array
  if [ $# -eq 1 ] && [[ "$1" == '['* ]]; then
    # Passed as JSON array string
    nomi_uuids="$1"
  else
    # Build JSON array from args
    nomi_uuids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
  fi
  
  local payload
  payload=$(jq -n --arg name "$name" --argjson uuids "$nomi_uuids" '{name: $name, nomiUuids: $uuids}')
  
  curl -sS -X POST "$BASE_URL/rooms" \
    -H "$(auth_header)" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "$payload" | jq .
}

# Update a room
room_update() {
  local uuid="$1"
  local name="${2:-}"
  shift 2
  local nomi_uuids=()
  
  # Build payload dynamically
  local payload="{}"
  
  if [ -n "$name" ]; then
    payload=$(echo "$payload" | jq --arg n "$name" '. + {name: $n}')
  fi
  
  if [ $# -gt 0 ]; then
    if [ $# -eq 1 ] && [[ "$1" == '['* ]]; then
      nomi_uuids="$1"
    else
      nomi_uuids=$(printf '%s\n' "$@" | jq -R . | jq -s .)
    fi
    payload=$(echo "$payload" | jq --argjson uuids "$nomi_uuids" '. + {nomiUuids: $uuids}')
  fi
  
  curl -sS -X PUT "$BASE_URL/rooms/$uuid" \
    -H "$(auth_header)" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "$payload" | jq .
}

# Delete a room
room_delete() {
  local uuid="$1"
  curl -sS -X DELETE "$BASE_URL/rooms/$uuid" \
    -H "$(auth_header)" \
    -H "Accept: application/json"
  echo "Room $uuid deleted"
}

# Send message to room
room_chat() {
  local uuid="$1"
  local message="$2"
  local payload
  payload=$(jq -n --arg msg "$message" '{messageText: $msg}')
  
  curl -sS -X POST "$BASE_URL/rooms/$uuid/chat" \
    -H "$(auth_header)" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "$payload" | jq .
}

# Request a chat from a specific Nomi in a room
room_chat_request() {
  local room_uuid="$1"
  local nomi_uuid="$2"
  local payload
  payload=$(jq -n --arg nomiId "$nomi_uuid" '{nomiId: $nomiId}')
  
  curl -sS -X POST "$BASE_URL/rooms/$room_uuid/chat/request" \
    -H "$(auth_header)" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "$payload" | jq .
}

# ============================
# UTILITY
# ============================

# Pretty print a Nomi from list
nomi_show() {
  local uuid="$1"
  nomi_list | jq --arg uuid "$uuid" '.nomis[] | select(.uuid == $uuid)'
}

# Get recent reply from a chat (convenience)
nomi_reply() {
  nomi_chat "$1" "$2" | jq -r '.replyMessage.text'
}

# Show usage
usage() {
  cat << 'EOF'
Usage: nomi <command> [args]

NOMI COMMANDS:
  nomi list                           List all your Nomis
  nomi get <uuid>                     Get details of a specific Nomi
  nomi avatar <uuid> [output]         Download Nomi avatar (default: nomi-{uuid}-avatar.webp)
  nomi chat <uuid> "message"          Send a message to a Nomi (returns full JSON)
  nomi reply <uuid> "message"         Send message and get reply text only

ROOM COMMANDS:
  room list                           List all rooms
  room get <uuid>                     Get room details
  room create "Name" <uuid>...        Create room with name and Nomi UUIDs
  room update <uuid> ["Name"] [uuid...]  Update room (name and/or Nomis)
  room delete <uuid>                  Delete a room
  room chat <uuid> "message"          Send message to room
  room request <room_uuid> <nomi_uuid>  Request a specific Nomi to chat

OTHER:
  help                                Show this help

ENVIRONMENT:
  NOMI_API_KEY    Your Nomi API key (required)

EXAMPLES:
  nomi list
  nomi get d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763
  nomi chat d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763 "Hello!"
  nomi reply d4c41601-6ee9-4b92-8d9a-f3a4ab3c2763 "How are you?"
  room create "My Group" uuid1 uuid2 uuid3
  room chat room-uuid "Hey everyone!"

EOF
}

# ============================
# MAIN DISPATCH
# ============================

main() {
  check_deps
  
  if [ $# -eq 0 ]; then
    usage
    exit 1
  fi

  local cmd="$1"
  shift

  case "$cmd" in
    # Nomi commands
    list)
      require_auth
      nomi_list
      ;;
    get)
      require_auth
      if [ $# -lt 1 ]; then
        echo "❌ ERROR: get requires Nomi UUID"
        exit 1
      fi
      nomi_get "$1"
      ;;
    avatar)
      require_auth
      if [ $# -lt 1 ]; then
        echo "❌ ERROR: avatar requires Nomi UUID"
        exit 1
      fi
      nomi_avatar "$1" "${2:-}"
      ;;
    chat)
      require_auth
      if [ $# -lt 2 ]; then
        echo "❌ ERROR: chat requires Nomi UUID and message"
        exit 1
      fi
      nomi_chat "$1" "$2"
      ;;
    reply)
      require_auth
      if [ $# -lt 2 ]; then
        echo "❌ ERROR: reply requires Nomi UUID and message"
        exit 1
      fi
      nomi_reply "$1" "$2"
      ;;
    show)
      require_auth
      if [ $# -lt 1 ]; then
        echo "❌ ERROR: show requires Nomi UUID"
        exit 1
      fi
      nomi_show "$1"
      ;;
    
    # Room commands
    room)
      require_auth
      if [ $# -eq 0 ]; then
        echo "❌ ERROR: room requires a subcommand (list, get, create, update, delete, chat, request)"
        exit 1
      fi
      local room_cmd="$1"
      shift
      case "$room_cmd" in
        list)
          room_list
          ;;
        get)
          if [ $# -lt 1 ]; then
            echo "❌ ERROR: room get requires room UUID"
            exit 1
          fi
          room_get "$1"
          ;;
        create)
          if [ $# -lt 2 ]; then
            echo "❌ ERROR: room create requires name and at least one Nomi UUID"
            exit 1
          fi
          room_create "$@"
          ;;
        update)
          if [ $# -lt 1 ]; then
            echo "❌ ERROR: room update requires room UUID"
            exit 1
          fi
          room_update "$@"
          ;;
        delete)
          if [ $# -lt 1 ]; then
            echo "❌ ERROR: room delete requires room UUID"
            exit 1
          fi
          room_delete "$1"
          ;;
        chat)
          if [ $# -lt 2 ]; then
            echo "❌ ERROR: room chat requires room UUID and message"
            exit 1
          fi
          room_chat "$1" "$2"
          ;;
        request)
          if [ $# -lt 2 ]; then
            echo "❌ ERROR: room request requires room UUID and Nomi UUID"
            exit 1
          fi
          room_chat_request "$1" "$2"
          ;;
        *)
          echo "❌ Unknown room command: $room_cmd"
          usage
          exit 1
          ;;
      esac
      ;;
    
    # Help
    help|--help|-h)
      usage
      ;;
    *)
      echo "❌ Unknown command: $cmd"
      usage
      exit 1
      ;;
  esac
}

main "$@"
