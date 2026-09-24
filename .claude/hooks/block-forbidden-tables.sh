#!/usr/bin/env bash
# PreToolUse wrapper (matchers: mcp__sap_.* and Bash) for block_forbidden_tables.py.
# Bash calls are pre-filtered here so Python only starts for ADT data-preview curls.
set -euo pipefail
source "$(dirname "$0")/lib-config.sh"

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // ""')
if [[ "$tool_name" == "Bash" ]]; then
  echo "$input" | jq -r '.tool_input.command // ""' | grep -q 'datapreview' || exit 0
else
  action=$(echo "$input" | jq -r '.tool_input.action // ""' | tr '[:upper:]' '[:lower:]')
  [[ "$action" == "query" ]] || exit 0
fi

echo "$input" | "$(pick_python)" -X utf8 "$(dirname "$0")/block_forbidden_tables.py"
