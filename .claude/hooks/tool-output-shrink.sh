#!/usr/bin/env bash
# PostToolUse (Bash|PowerShell|SAP MCP): shrink bulky tool output before it enters the conversation.
# Logic and rules: tool_output_shrink.py. Advisory / fail open: no Python -> the original output passes.
source "$(dirname "$0")/lib-config.sh"
py=$(pick_python)
command -v "$py" >/dev/null 2>&1 || exit 0
exec "$py" -X utf8 "$(dirname "$0")/tool_output_shrink.py"
