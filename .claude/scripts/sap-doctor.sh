#!/usr/bin/env bash
# sap-doctor.sh - one-shot health check of this workspace (skill sap-doctor).
#   bash .claude/scripts/sap-doctor.sh
# Checks: tools on PATH, system-config keys, every SAP MCP server in .mcp.json (cookie file present and
# accepted by ADT discovery, client classified write / read-only), hook syntax, settings.json, the
# integrity check, the .claude/.unlock sentinel and uncommitted changes. Read-only: sends one GET
# /sap/bc/adt/discovery per SAP server, never a query, never a write, never prints a cookie value.
# MCP tool liveness cannot be checked from a shell - the skill does that step with a real SAP search.
# Exit: 0 no FAIL (WARN allowed) · 1 at least one FAIL
set -uo pipefail
ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$ROOT" || exit 1
source .claude/hooks/lib-config.sh

fails=0; warns=0
row() {  # status, check, detail
  printf '%-5s %-34s %s\n' "$1" "$2" "$3"
  [[ "$1" == FAIL ]] && fails=$((fails + 1))
  [[ "$1" == WARN ]] && warns=$((warns + 1))
  return 0
}

echo "sap-doctor $(date '+%Y-%m-%d %H:%M') - $ROOT"
echo "----- ---------------------------------- ----------------------------------------------"

# 1. tools
for t in jq curl git; do
  command -v "$t" >/dev/null 2>&1 && row PASS "tool $t" "$(command -v "$t")" || row FAIL "tool $t" "not on PATH - hooks fail open without jq"
done
py=$(pick_python)
$py -c '' >/dev/null 2>&1 && row PASS "tool python" "$py" || row FAIL "tool python" "no working python/python3"

# 2. system-config
for k in SAP_TIER WRITE_SERVERS READONLY_SERVERS WRITE_CLIENTS SAP_ACTIVE_MODULES BLOCKLIST_PROFILE; do
  v=$(cfg "$k")
  [[ -n "$v" ]] && row PASS "config $k" "$v" || row FAIL "config $k" "missing in .claude/common/system-config.md"
done
[[ "$(cfg SAP_TIER)" == DEV ]] || row FAIL "config SAP_TIER=DEV" "every SAP write is blocked while tier is not DEV"

# 3. SAP MCP servers
if [[ ! -f .mcp.json ]]; then
  row FAIL ".mcp.json" "missing - no MCP server configured"
else
  write_clients=$(cfg WRITE_CLIENTS | tr ',' ' ' | awk '{ for (i = 1; i <= NF; i++) printf "%d ", $i + 0 }')
  while IFS=$'\t' read -r name url client cookie; do
    [[ -z "$url" ]] && continue
    c=$(mcp_client_of "$name")
    if in_list "$name" "$(cfg READONLY_SERVERS)"; then role="read-only"
    elif [[ -n "$c" ]] && in_list "$c" "$write_clients"; then role="write"
    else role="read-only (client not in WRITE_CLIENTS)"; fi
    if [[ -z "$cookie" || ! -f "$cookie" ]]; then
      row FAIL "$name cookie" "cookie file missing ($cookie)"; continue
    fi
    age=$(( ( $(date +%s) - $(date -r "$cookie" +%s) ) / 3600 ))
    res=$(curl -s -o /dev/null -m 20 -w '%{http_code} %{content_type}' -b "$cookie" "$url/sap/bc/adt/discovery?sap-client=$client" || echo "000 none")
    if [[ "$res" == 200\ application/atomsvc+xml* ]]; then
      row PASS "$name ($client, $role)" "ADT discovery OK - cookie ${age}h old"
    else
      row FAIL "$name ($client, $role)" "cookie rejected (got $res, cookie ${age}h old) - refresh: skill sap-doctor step 3"
    fi
  done < <(jq -r '.mcpServers | to_entries[] | select(.value.env.SAP_URL) |
                  [.key, .value.env.SAP_URL, .value.env.SAP_CLIENT, .value.env.SAP_COOKIE_FILE] | @tsv' .mcp.json | tr -d '\r')
  others=$(jq -r '.mcpServers | to_entries[] | select(.value.env.SAP_URL | not) | .key' .mcp.json | tr -d '\r' | tr '\n' ' ')
  [[ -n "$others" ]] && row INFO "other MCP servers" "$others- connection state visible only inside the session"
fi

# 4. hooks and settings
for h in .claude/hooks/*.sh; do
  bash -n "$h" 2>/dev/null && row PASS "hook syntax $(basename "$h")" "" || row FAIL "hook syntax $(basename "$h")" "bash -n fails - every hook sourcing it may break"
done
jq -e . .claude/settings.json >/dev/null 2>&1 && row PASS "settings.json" "valid JSON" || row FAIL "settings.json" "invalid JSON - no hook runs"

# 5. integrity
if out=$(bash .claude/scripts/integrity-check.sh 2>&1); then
  row PASS "integrity-check" "$(echo "$out" | tail -1)"
else
  row FAIL "integrity-check" "$(echo "$out" | grep -E '^FAIL' | head -3 | tr '\n' ' ')"
fi

# 6. lock and git
[[ -f .claude/.unlock ]] && row WARN ".claude/.unlock" "present - .claude/ is writable; delete it when the change is done" \
                         || row PASS ".claude/.unlock" "absent (.claude/ locked)"
dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
[[ "$dirty" == 0 ]] && row PASS "git working tree" "clean" || row WARN "git working tree" "$dirty uncommitted path(s)"

echo "----- ---------------------------------- ----------------------------------------------"
echo "result: $fails FAIL · $warns WARN"
[[ $fails -eq 0 ]]
