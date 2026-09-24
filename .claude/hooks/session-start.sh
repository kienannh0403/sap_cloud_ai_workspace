#!/usr/bin/env bash
# SessionStart (startup | resume | compact): inject a short orientation block — system config,
# .claude lock state, standing checks, and where the live task state is. Advisory only.
# Adapted from sc4sap session-start.mjs. Never fails the session: errors -> exit 0 silently.
set -uo pipefail
source "$(dirname "$0")/lib-config.sh" 2>/dev/null || exit 0

input=$(cat)
source_evt=$(echo "$input" | jq -r '.source // "startup"' 2>/dev/null || echo startup)
root="$HOOK_ROOT"

lines=()
lines+=("Workspace system (system-config.md): $(cfg SAP_VERSION) · modules=$(cfg SAP_ACTIVE_MODULES) · country=$(cfg SAP_COUNTRY) · tier=$(cfg SAP_TIER) · blocklist=$(cfg BLOCKLIST_PROFILE) · write=$(cfg WRITE_SERVERS) · read-only=$(cfg READONLY_SERVERS).")

if [[ -f "$root/.claude/.unlock" ]]; then
  lines+=("WARNING: .claude/.unlock is PRESENT — the .claude/ lock is off. Remind the user to delete it when the .claude/ change is finished.")
fi

if [[ "$source_evt" == "startup" ]]; then
  lines+=("Standing check (memory check-mcp-alive-each-session): verify both SAP MCP servers are alive before SAP work.")
fi

# Most recently touched ledgers / handoffs = where work was left.
recent=$(find "$root/artifacts/scratchpads" -maxdepth 2 -type f \( -name 'ledger*.md' -o -name 'handoff_*.md' \) \
  -printf '%T@ %P\n' 2>/dev/null | sort -rn | head -3 | cut -d' ' -f2- | sed 's#^#artifacts/scratchpads/#' | paste -sd ',' -)
if [[ -n "$recent" ]]; then
  lines+=("Most recent ledger/handoff files: ${recent//,/, }.")
fi

if [[ "$source_evt" == "compact" ]]; then
  lines+=("Context was just COMPACTED: re-read the active ledger and the target's artifacts/system_analysis/<TARGET>/INDEX.md before continuing — do not trust recalled progress (rule §10/§12).")
fi

ctx=$(printf '%s\n' "${lines[@]}")
jq -n --arg c "$ctx" '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":$c}}'
