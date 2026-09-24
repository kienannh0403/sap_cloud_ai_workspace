#!/usr/bin/env bash
# Rule §14 integrity check — run after ANY .claude/ change: bash .claude/scripts/integrity-check.sh
# Exit 0 = all checks PASS. Logic lives in integrity-check.py (next to this file).
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
export CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$here/../.." && pwd)}"
if python3 -c '' >/dev/null 2>&1; then py=python3; else py=python; fi
"$py" -X utf8 "$here/integrity-check.py"
