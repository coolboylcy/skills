#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required." >&2
  exit 1
fi

python3 - <<'PY'
import sys
if sys.version_info < (3, 8):
    raise SystemExit("Error: Python 3.8+ is required.")
print(f"Python check OK: {sys.version.split()[0]}")
PY

export PYTHONPATH="$ROOT_DIR/core:${PYTHONPATH:-}"

python3 - <<'PY'
import sys
sys.path.insert(0, 'core')
from guardian_db import GuardianDB

db = GuardianDB()
print(f"Database ready: {db.db_path}")
db.close()
PY

python3 - <<'PY'
import json
import re
from pathlib import Path

defs_dir = Path('definitions')
errors = []
for p in defs_dir.glob('*.json'):
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f"{p.name}: JSON parse failed: {exc}")
        continue
    items = data.get('signatures', data.get('checks', [])) if isinstance(data, dict) else []
    for item in items:
        pat = item.get('pattern')
        if pat:
            try:
                re.compile(pat)
            except re.error as exc:
                errors.append(f"{p.name}:{item.get('id', '?')}: invalid regex: {exc}")

if errors:
    raise SystemExit("Definition validation failed:\n" + "\n".join(errors))

print("Definition validation OK")
PY

cat <<'OUT'

Guardian install complete.
Next steps:
1) Review ./config.json for scan paths, DB path, and severity threshold.
2) Run a quick scan: python3 scripts/guardian.py --scan "ignore previous instructions" --pretty
3) Run a report scan: python3 scripts/guardian.py --report ~/.openclaw/agents --hours 24 --pretty

Optional cron setup (example every 2 minutes):
*/2 * * * * cd <guardian-path> && python3 scripts/guardian.py --report ~/.openclaw/agents --hours 1
OUT
