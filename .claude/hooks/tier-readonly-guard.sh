#!/usr/bin/env bash
# PreToolUse guard for every SAP MCP server (matcher mcp__sap_.* in settings.json).
# Hard-enforces rule §2 "DEV only" and the client-100 read-only convention, using
# .claude/common/system-config.md:
#   - SAP_TIER != DEV            -> deny every mutating action on every SAP server
#   - server in READONLY_SERVERS -> deny every mutating action on that server
# Mutating actions of the vsp "SAP" tool: create, edit, delete (read/search/query/grep/
# test/analyze/debug/system/help pass). Adapted from sc4sap tier-readonly-guard.mjs.
# Fails CLOSED for mutations when system-config.md is missing: the tier is then unknown.
set -euo pipefail
source "$(dirname "$0")/lib-config.sh"

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // ""')
action=$(echo "$input" | jq -r '.tool_input.action // ""' | tr '[:upper:]' '[:lower:]')
server=$(mcp_server_of "$tool_name")

deny() {
  jq -n --arg reason "$1" \
    '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":$reason}}'
  exit 0
}

case "$action" in
  create*|edit*|delete*|update*|modify*|activate*) ;;
  *) exit 0 ;;
esac

if [[ ! -f "$SYSTEM_CONFIG" ]]; then
  deny "tier-readonly-guard: .claude/common/system-config.md is missing, so the system tier is unknown — mutating SAP action '$action' refused. Restore the file (git) first."
fi

tier=$(cfg SAP_TIER)
if [[ "$tier" != "DEV" ]]; then
  deny "sap-dev-rule.md §2 (DEV only): system-config.md says SAP_TIER='$tier'. Every mutating SAP action is refused. STOP and ask the user."
fi

if in_list "$server" "$(cfg READONLY_SERVERS)"; then
  deny "tier-readonly-guard: MCP server '$server' is READ-ONLY (READONLY_SERVERS in system-config.md: read/test/debug only). Write on '$(cfg WRITE_SERVERS)' instead."
fi

exit 0
