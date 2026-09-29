#!/usr/bin/env bash
# PreToolUse wrapper (matchers: mcp__sap_.* and Bash) for block_forbidden_tables.py.
# Bash calls are pre-filtered here so Python only starts for ADT data-preview curls.
set -euo pipefail
source "$(dirname "$0")/lib-config.sh"

input=$(cat)

# Fail CLOSED without jq, but only for what this hook polices (crude match on the raw payload): an ADT
# data-preview curl, or an MCP action=query. Other calls pass, so jq can be reinstalled.
if ! command -v jq >/dev/null 2>&1; then
  if echo "$input" | grep -q 'datapreview' \
     || echo "$input" | grep -qiE '"action"[[:space:]]*:[[:space:]]*"query"'; then
    echo "block-forbidden-tables: jq not found on PATH - blocking data reads (fail closed). Install jq (winget install --id jqlang.jq -e) and restart VS Code." >&2
    exit 2
  fi
  exit 0
fi

tool_name=$(echo "$input" | jq -r '.tool_name // ""')
if [[ "$tool_name" == "Bash" ]]; then
  echo "$input" | jq -r '.tool_input.command // ""' | grep -q 'datapreview' || exit 0
else
  action=$(echo "$input" | jq -r '.tool_input.action // ""' | tr '[:upper:]' '[:lower:]')
  [[ "$action" == "query" ]] || exit 0
fi

echo "$input" | "$(pick_python)" -X utf8 "$(dirname "$0")/block_forbidden_tables.py"
