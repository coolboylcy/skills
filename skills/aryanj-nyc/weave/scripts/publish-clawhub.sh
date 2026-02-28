#!/usr/bin/env bash
set -euo pipefail

print_usage() {
  cat <<'EOF'
Usage:
  bash skills/weave/scripts/publish-clawhub.sh <version> [changelog]

Examples:
  bash skills/weave/scripts/publish-clawhub.sh 0.1.0
  bash skills/weave/scripts/publish-clawhub.sh 0.1.1 "Docs-only update for skills.sh listing notes"

Environment variables:
  SKILL_PATH_REL   Repo-relative skill path (default: skills/weave)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  print_usage
  exit 0
fi

if [[ $# -lt 1 ]]; then
  print_usage
  exit 1
fi

if ! command -v clawhub >/dev/null 2>&1; then
  echo "Error: 'clawhub' CLI is not installed or not on PATH." >&2
  exit 1
fi

version="$1"
default_changelog="Publish weave skill ${version}: full lifecycle flow docs and runtime-safe token guidance."
changelog="${2:-$default_changelog}"

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd -- "${script_dir}/../../.." && pwd)"
skill_path_rel="${SKILL_PATH_REL:-skills/weave}"

(
  cd "${repo_root}"
  echo "Publishing '${skill_path_rel}' with version '${version}'..."
  clawhub publish "${skill_path_rel}" --version "${version}" --changelog "${changelog}"
)

