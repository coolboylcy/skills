#!/usr/bin/env bash
# pl.sh — PromptLayer REST API CLI wrapper
# Usage: pl.sh <command> [subcommand] [args...]
set -euo pipefail

BASE_URL="${PROMPTLAYER_BASE_URL:-https://api.promptlayer.com}"
API_KEY="${PROMPTLAYER_API_KEY:?Set PROMPTLAYER_API_KEY env var}"

auth_header="Authorization: Bearer $API_KEY"
json_header="Content-Type: application/json"

api() {
  local method="$1" path="$2"; shift 2
  curl -sS -X "$method" "${BASE_URL}${path}" \
    -H "$auth_header" -H "$json_header" "$@"
}

usage() {
  cat <<'EOF'
Usage: pl.sh <command> [subcommand] [args...]

Commands:
  templates list                          List prompt templates
  templates get <name> [--label <label>]  Get a prompt template
  templates publish <name> --commit "msg" Publish a prompt template
  log                                     Log a request (JSON on stdin)
  track-score <req_id> <name> <value>     Track a score
  track-metadata <req_id> --json '{}'     Track metadata
  track-group <req_id> <group_id>         Track group
  datasets list                           List datasets
  evals list                              List evaluation pipelines
  evals run <pipeline_id>                 Run an evaluation pipeline
  evals get <pipeline_id>                 Get evaluation results
  agents list                             List agents
  agents run <id> --input '{}'            Run an agent
  help                                    Show this help
EOF
}

# --- Templates ---
cmd_templates() {
  local sub="${1:-}"; shift || true
  case "$sub" in
    list)
      api GET "/prompt-templates"
      ;;
    get)
      local name="${1:?Usage: pl.sh templates get <name> [--label <label>]}"
      shift
      local label=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --label) label="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      local body="{\"prompt_name\": \"$name\""
      [[ -n "$label" ]] && body+=", \"label\": \"$label\""
      body+="}"
      api POST "/prompt-templates" -d "$body"
      ;;
    publish)
      local name="${1:?Usage: pl.sh templates publish <name> --commit \"msg\"}"
      shift
      local commit=""
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --commit) commit="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      api POST "/prompt-templates/publish" \
        -d "{\"prompt_name\": \"$name\", \"commit_message\": \"$commit\"}"
      ;;
    *)
      echo "Usage: pl.sh templates [list|get|publish]" >&2; exit 1
      ;;
  esac
}

# --- Logging ---
cmd_log() {
  local body
  body="$(cat)"
  api POST "/log-request" -d "$body"
}

# --- Tracking ---
cmd_track_score() {
  local req_id="${1:?}" score_name="${2:?}" value="${3:?}"
  api POST "/track-score" \
    -d "{\"request_id\": $req_id, \"score_name\": \"$score_name\", \"value\": $value}"
}

cmd_track_metadata() {
  local req_id="${1:?}"; shift
  local json=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --json) json="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  api POST "/track-metadata" \
    -d "{\"request_id\": $req_id, \"metadata\": $json}"
}

cmd_track_group() {
  local req_id="${1:?}" group_id="${2:?}"
  api POST "/track-group" \
    -d "{\"request_id\": $req_id, \"group_id\": $group_id}"
}

# --- Datasets ---
cmd_datasets() {
  local sub="${1:-list}"
  case "$sub" in
    list) api GET "/datasets" ;;
    *) echo "Usage: pl.sh datasets list" >&2; exit 1 ;;
  esac
}

# --- Evaluations ---
cmd_evals() {
  local sub="${1:-}"; shift || true
  case "$sub" in
    list)
      api GET "/report"
      ;;
    run)
      local pipeline_id="${1:?Usage: pl.sh evals run <pipeline_id>}"
      api POST "/report/${pipeline_id}/run"
      ;;
    get)
      local pipeline_id="${1:?Usage: pl.sh evals get <pipeline_id>}"
      api GET "/report/${pipeline_id}"
      ;;
    *)
      echo "Usage: pl.sh evals [list|run|get]" >&2; exit 1
      ;;
  esac
}

# --- Agents ---
cmd_agents() {
  local sub="${1:-}"; shift || true
  case "$sub" in
    list)
      api GET "/workflows"
      ;;
    run)
      local agent_id="${1:?Usage: pl.sh agents run <id> --input '{}'}"
      shift
      local input="{}"
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --input) input="$2"; shift 2 ;;
          *) shift ;;
        esac
      done
      api POST "/workflows/${agent_id}/run" -d "$input"
      ;;
    *)
      echo "Usage: pl.sh agents [list|run]" >&2; exit 1
      ;;
  esac
}

# --- Main ---
cmd="${1:-help}"; shift || true
case "$cmd" in
  templates)      cmd_templates "$@" ;;
  log)            cmd_log "$@" ;;
  track-score)    cmd_track_score "$@" ;;
  track-metadata) cmd_track_metadata "$@" ;;
  track-group)    cmd_track_group "$@" ;;
  datasets)       cmd_datasets "$@" ;;
  evals)          cmd_evals "$@" ;;
  agents)         cmd_agents "$@" ;;
  help|--help|-h) usage ;;
  *)              echo "Unknown command: $cmd" >&2; usage; exit 1 ;;
esac
