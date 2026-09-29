#!/usr/bin/env bash
# PreToolUse fact-forcing gate for SAP edit/delete on EXISTING objects (idea adapted from ECC gateguard, MIT,
# github.com/affaan-m/ecc). activation-guard Gate 3 checks the ripple AFTER a change; this gate makes the agent
# gather the facts BEFORE it: asking "is this safe?" gets "yes", asking "list the dependents" forces a real lookup.
#   1st edit/delete of an object in a session -> deny, naming the facts to gather (dependents, authority)
#   the retry (same session, same object)     -> allow; later edits of that object in the session pass too
# Scope: action edit* / delete on any SAP server (create is not gated: a new object has no dependents yet).
# Advisory in nature: no jq / no object name -> pass (pre-cud-guard + tier-readonly-guard are the hard gates).
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0
source "$(dirname "$0")/lib-config.sh"

input=$(cat)
action=$(echo "$input" | jq -r '.tool_input.action // ""' | tr '[:upper:]' '[:lower:]' | tr -d '\r')
case "$action" in
  edit*|delete) ;;
  *) exit 0 ;;
esac

# Object: "TYPE NAME" in target (edit puts the name only there), else a params name key.
target=$(echo "$input" | jq -r '.tool_input.target // ""' | tr -d '\r')
if [[ -z "$target" ]]; then
  target=$(echo "$input" | jq -r '.tool_input.params | objects | (.name // .object_name // .class_name // "")' | tr -d '\r')
fi
[[ -z "$target" ]] && exit 0
obj_type=$(echo "$target" | awk '{print toupper($1)}')
obj_name=$(echo "$target" | awk '{print toupper($NF)}')

session=$(echo "$input" | jq -r '.session_id // "nosession"' | tr -d '\r')
# Server is part of the key: a call denied on the read-only server must not unlock the same object on 080.
server=$(mcp_server_of "$(echo "$input" | jq -r '.tool_name // ""' | tr -d '\r')")
state_dir="$HOOK_ROOT/artifacts/scratchpads/_session/sap-fact-gate"
mkdir -p "$state_dir" 2>/dev/null
marker="$state_dir/$(echo "${session}_${server}_${obj_type}_${obj_name}" | tr -c 'A-Za-z0-9_-' '_')"
[[ -f "$marker" ]] && exit 0
: > "$marker" 2>/dev/null || exit 0

case "$obj_type" in
  DDLS) deps_cmd="SAP(action=\"analyze\", params={\"type\": \"cds_impact\", \"cds_view\": \"$obj_name\"})" ;;
  CLAS|PROG|INTF|FUNC|FUGR) deps_cmd="SAP(action=\"analyze\", params={\"type\": \"callers\", \"object_uri\": \"<uri of $obj_name>\"})" ;;
  *) deps_cmd="SAP(action=\"analyze\", params={\"type\": \"impact\", \"object_type\": \"$obj_type\", \"object_name\": \"$obj_name\", \"max_depth\": 3})" ;;
esac

extra=""
[[ "$action" == "delete" ]] && extra=" (3) DELETE: if any dependent exists, the delete breaks it - stop and ask the user instead of retrying."

reason="sap-edit-fact-gate: before you ${action} ${obj_type} ${obj_name}, state these facts in chat, then retry the same call: (1) DEPENDENTS - run ${deps_cmd} and list every object that depends on it (or 'none', citing the command); these are what activation-guard Gate 3 must re-check afterwards. (2) AUTHORITY - the TS Coding Implementation Plan row, bug-fix step or explicit user request this change implements (rule §6: no change absent from the plan).${extra} If the tool has no where-used for this type, say so explicitly (activation-guard Gate 3 wording). This gate fires once per object per session."

jq -n --arg reason "$reason" \
  '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":$reason}}'
exit 0
