#!/usr/bin/env bash
# PreToolUse guard for every SAP MCP server (matcher mcp__sap_[a-z0-9_]+__.*|mcp__.+__SAP$ in settings.json).
# Hard-enforces rule §2 "DEV only" and the client-100 read-only convention, using
# .claude/common/system-config.md:
#   - SAP_TIER != DEV            -> deny every mutating action on every SAP server
#   - server in READONLY_SERVERS -> deny every mutating action on that server
#   - server's SAP_CLIENT (.mcp.json) not in WRITE_CLIENTS -> deny every mutating action
#     (write permission follows the client, not the server name; unknown client = deny)
# Mutating actions of the vsp "SAP" tool: create, edit, delete (read/search/query/grep/test/help pass).
# Side doors (2026-09-28): TR create/release/delete via action=system -> deny; analyze execute_abap -> deny on a
# read-only server, ask on a write server; debug -> allowed read-only, ask on a write server.
# Adapted from sc4sap tier-readonly-guard.mjs.
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

ask() {
  jq -n --arg reason "$1" \
    '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":$reason}}'
  exit 0
}

# Is this server read-only? (listed in READONLY_SERVERS, or its client is unknown / not in WRITE_CLIENTS)
server_is_readonly() {
  in_list "$server" "$(cfg READONLY_SERVERS)" && return 0
  local c wc
  c=$(mcp_client_of "$server")
  wc=$(cfg WRITE_CLIENTS | tr ',' ' ' | awk '{ for (i = 1; i <= NF; i++) printf "%d ", $i + 0 }')
  [[ -z "$c" ]] && return 0
  in_list "$c" "$wc" && return 1
  return 0
}

# Side doors that are not create/edit/delete (user decision 2026-09-28):
#   system type=create/release/delete/modify/change_transport -> deny everywhere (rule §2: agent never manages a TR)
#   analyze type=execute_abap -> deny on a read-only server, ask on a write server (arbitrary ABAP can change data)
#   debug                     -> allowed on a read-only server (read / test / debug), ask on a write server
sub_type=$(echo "$input" | jq -r '.tool_input.params.type // .tool_input.type // ""' | tr '[:upper:]' '[:lower:]')
case "$action" in
  system)
    if [[ "$sub_type" =~ ^(create|release|delete|modify|change)_?transport ]]; then
      deny "sap-dev-rule.md §2: the agent never creates, releases, deletes or changes a Transport Request ('$sub_type'). Ask the user to do it; reading TRs (list/get) is allowed."
    fi
    exit 0 ;;
  analyze)
    if [[ "$sub_type" == execute_abap* ]]; then
      server_is_readonly && deny "tier-readonly-guard: running arbitrary ABAP (execute_abap) is refused on read-only server '$server' — it can change data."
      ask "tier-readonly-guard: execute_abap runs arbitrary ABAP on '$server' and can change data. Confirm this exact code is intended."
    fi
    exit 0 ;;
  debug)
    server_is_readonly && exit 0
    ask "tier-readonly-guard: debug on write server '$server' (breakpoints / running reports or RFCs can change data). Confirm." ;;
esac

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

client=$(mcp_client_of "$server")
write_clients=$(cfg WRITE_CLIENTS | tr ',' ' ' | awk '{ for (i = 1; i <= NF; i++) printf "%d ", $i + 0 }')
if [[ -z "$client" ]]; then
  deny "tier-readonly-guard: SAP client of MCP server '$server' is unknown (no env.SAP_CLIENT for it in .mcp.json) — mutating SAP action '$action' refused. Only clients in WRITE_CLIENTS ($(cfg WRITE_CLIENTS)) may be written."
fi
if ! in_list "$client" "$write_clients"; then
  deny "tier-readonly-guard: MCP server '$server' is client $client — only clients in WRITE_CLIENTS ($(cfg WRITE_CLIENTS), system-config.md) may be written. Write on '$(cfg WRITE_SERVERS)' instead."
fi

exit 0
