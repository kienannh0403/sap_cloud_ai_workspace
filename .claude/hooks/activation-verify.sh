#!/usr/bin/env bash
# PostToolUse (matcher mcp__sap_.*): after a create/edit/delete on a write server, remind the
# model that the step is NOT done until activation-guard's 4 gates pass (rule §5/§6).
# Advisory only — never blocks. Adapted from sc4sap activation-trigger.mjs.
# vsp returns success:true even on failed activations (memory activate-success-is-not-active).
set -euo pipefail
source "$(dirname "$0")/lib-config.sh"

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // ""')
action=$(echo "$input" | jq -r '.tool_input.action // ""' | tr '[:upper:]' '[:lower:]')
target=$(echo "$input" | jq -r '.tool_input.target // ""')

case "$action" in
  create*|edit*|delete*) ;;
  *) exit 0 ;;
esac
in_list "$(mcp_server_of "$tool_name")" "$(cfg WRITE_SERVERS)" || exit 0

msg="SAP '$action' on '${target:-?}' returned. Not DONE yet: run [Skill: activation-guard] 4 gates now — (1) full activation log, every warning assessed; (2) active state proven via analyze inactive_objects, not the ACTIVATE response; (3) ripple check on dependents; (4) zero NEW ATC findings on changed lines. Then update the ledger row with the evidence."
jq -n --arg m "$msg" '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":$m}}'
