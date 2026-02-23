#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
TARGET_SCRIPT="scripts/feed_to_md.py"

pass_count=0
fail_count=0

run_expect_fail() {
  local name="$1"
  local expected="$2"
  shift 2

  local output=""
  local status=0
  if output="$("$@" 2>&1)"; then
    status=0
  else
    status=$?
  fi

  if [[ $status -eq 0 ]]; then
    echo "FAIL: $name (expected failure, got success)"
    ((fail_count += 1))
    return
  fi

  if [[ "$output" == *"$expected"* ]]; then
    echo "PASS: $name"
    ((pass_count += 1))
  else
    echo "FAIL: $name"
    echo "  expected to contain: $expected"
    echo "  got: $output"
    ((fail_count += 1))
  fi
}

run_expect_fail \
  "reject non-http(s) URL" \
  "URL must use http or https" \
  "$PYTHON_BIN" "$TARGET_SCRIPT" "file:///tmp/feed.xml"

run_expect_fail \
  "reject localhost URL" \
  "localhost feeds are not allowed" \
  "$PYTHON_BIN" "$TARGET_SCRIPT" "http://localhost/feed.xml"

run_expect_fail \
  "reject private/loopback IP URL" \
  "non-public IP address" \
  "$PYTHON_BIN" "$TARGET_SCRIPT" "http://127.0.0.1/feed.xml"

# Use a public IP literal to pass URL validation without depending on DNS.
run_expect_fail \
  "reject absolute output path" \
  "Output path must be relative to the current workspace" \
  "$PYTHON_BIN" "$TARGET_SCRIPT" "https://1.1.1.1/feed.xml" --output "/tmp/feed.md"

run_expect_fail \
  "reject path traversal output path" \
  "Output path must not contain '..'" \
  "$PYTHON_BIN" "$TARGET_SCRIPT" "https://1.1.1.1/feed.xml" --output "../feed.md"

run_expect_fail \
  "reject non-markdown output extension" \
  "Output path must end with .md" \
  "$PYTHON_BIN" "$TARGET_SCRIPT" "https://1.1.1.1/feed.xml" --output "feed.txt"

echo
echo "Regression tests complete: pass=$pass_count fail=$fail_count"

if [[ $fail_count -ne 0 ]]; then
  exit 1
fi
