#!/bin/bash
# SecureVibes Scanner — wrapper script with input validation
# Usage: scan.sh <project-path> [extra args...]
set -euo pipefail

PROJECT_PATH="${1:?Usage: scan.sh <project-path> [--severity high] [--format json] [--subagent threat-modeling] ...}"
shift

# Input validation: reject paths with shell metacharacters
if [[ "$PROJECT_PATH" =~ [\;\|\&\$\`\(\)\{\}\<\>\!\#] ]]; then
    echo "❌ Invalid path: contains shell metacharacters"
    exit 1
fi

# Resolve to absolute path and verify it exists
PROJECT_PATH="$(realpath -- "$PROJECT_PATH" 2>/dev/null)" || {
    echo "❌ Path does not exist: $1"
    exit 1
}

if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ Not a directory: $PROJECT_PATH"
    exit 1
fi

# Check securevibes is installed
if ! command -v securevibes &>/dev/null; then
    echo "❌ securevibes not found. Install with: pip install securevibes"
    echo "  https://pypi.org/project/securevibes/"
    exit 1
fi

# Check API key (optional if authenticated via Anthropic Max/Pro OAuth)
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo "ℹ️  ANTHROPIC_API_KEY not set — using Anthropic OAuth (Max/Pro subscription)."
    echo "   If auth fails, set ANTHROPIC_API_KEY or run: claude login"
fi

echo "🛡️  SecureVibes Scanner"
echo "📂 Target: ${PROJECT_PATH}"
echo "⏳ Starting scan..."
echo ""

securevibes scan "$PROJECT_PATH" "$@"
