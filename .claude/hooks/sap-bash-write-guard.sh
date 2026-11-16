#!/usr/bin/env bash
# PreToolUse (Bash|PowerShell): close the side door around the SAP MCP guards (user 2026-11-16).
# pre-cud-guard / tier-readonly-guard / sap-edit-fact-gate only see MCP SAP calls. The cookie files make it
# possible to write to SAP from a shell too (curl PUT to /sap/bc/adt, a Python requests.post, the vsp CLI) and
# none of those guards would run. Every SAP write therefore goes through the MCP SAP tool; this hook denies:
#   A. an HTTP client (curl, wget, Invoke-WebRequest/RestMethod) sending a write method or a body to a SAP path
#   B. inline code (python/node heredoc, -c) issuing POST/PUT/PATCH/DELETE when the command names a SAP path
#   C. vsp CLI subcommands that write or run code: deploy, copy, install, execute, transport, lua, workflow, debug
# Reads stay allowed: curl GET of /sap/bc/adt sources (lean-sap-io.md §2), the workspace scripts (atc_check.py,
# odata-verify fetch.sh) whose POSTs are not in the command text and only read/check.
# Fails CLOSED without jq for a command that matches (exit 2), passes every other command.
set -uo pipefail

input=$(cat)
if command -v jq >/dev/null 2>&1; then
  cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
else
  cmd=$input
fi
lc=$(printf '%s' "$cmd" | tr '[:upper:]' '[:lower:]')

sap_path='/sap/(bc/adt|opu/|bc/http|bc/rest)'
reason=""

if printf '%s' "$lc" | grep -qE "$sap_path"; then
  # A. HTTP client with a write method or a request body
  if printf '%s' "$lc" | grep -qE '(^|[^a-z])(curl|wget|invoke-webrequest|invoke-restmethod|iwr|irm)([^a-z]|$)' \
     && printf '%s' "$lc" | grep -qE '(-x|--request|-method)[[:space:]=]*"?(post|put|patch|delete)|(^|[[:space:]])(-d|--data[a-z-]*|-t|--upload-file|--form|-body|--post-data|--post-file|--method=(post|put|patch|delete))([[:space:]=]|$)'; then
    reason="HTTP client sending a write request to a SAP path"
  fi
  # B. inline code issuing a write method
  if [[ -z "$reason" ]] && printf '%s' "$lc" | grep -qE '(requests|session|s|httpx|axios)\.(post|put|patch|delete)\(|method[[:space:]]*[=:][[:space:]]*["'"'"'](post|put|patch|delete)["'"'"']|urllib\.request\.urlopen\([^)]*data='; then
    reason="inline code issuing POST/PUT/PATCH/DELETE in a command that names a SAP path"
  fi
fi

# C. vsp CLI subcommands that write to SAP or run code there
if [[ -z "$reason" ]] && printf '%s' "$lc" | grep -qE '(^|[/\\[:space:]"'"'"'])vsp(\.exe)?["'"'"']?[[:space:]]+([^|;&]*[[:space:]])?(deploy|copy|install|execute|transport|lua|workflow|debug)([[:space:]]|$)'; then
  reason="vsp CLI subcommand that writes to SAP or runs code there"
fi

[[ -z "$reason" ]] && exit 0

msg="sap-bash-write-guard: $reason - refused. Every SAP write goes through the MCP SAP tool so pre-cud-guard, tier-readonly-guard and sap-edit-fact-gate run on it (rule §2). Reads: curl GET (lean-sap-io.md §2), atc_check.py for ATC / inactive objects, MCP SAP for syntax checks. If this command really only reads, rewrite it without the write method / body, or ask the user."
if command -v jq >/dev/null 2>&1; then
  jq -n --arg reason "$msg" \
    '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":$reason}}'
  exit 0
fi
echo "$msg" >&2
exit 2
