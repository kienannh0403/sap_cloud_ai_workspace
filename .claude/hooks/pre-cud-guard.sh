#!/usr/bin/env bash
# PreToolUse guard for SAP CUD calls (matcher mcp__sap_[a-z0-9_]+__.*|mcp__.+__SAP$ in settings.json —
# every SAP server, whatever its name; which client may be written is tier-readonly-guard.sh's job).
# Hard-enforces rules from .claude/rules/sap-dev-rule.md §2 that were previously prompt-only:
#   - Z/Y-only object naming
#   - Package mandatory for object CUD
#   - TR mandatory for object CUD in a TRANSPORTABLE package, EXCEPT objects in a
#     LOCAL (non-transportable) package listed in LOCAL_NO_TR_PACKAGES (rule §2 local exception)
#   - the agent must never create/delete/modify a Transport Request itself
#
# Field lookups are tuned to the sap_cloud_dev "SAP" tool create/edit payload
# (verified 2026-07-27 via SAP(action="help", target="create")):
#   - object name lives in params keys: name / class_name / program_name /
#     target_name / interface_name / function_name  (NOT in `target`, which is a TYPE keyword)
#   - package lives in "package" OR "package_name"
set -euo pipefail

# Fail CLOSED without jq: deny() needs jq to emit a decision, and a hook that errors with an exit code
# other than 2 is non-blocking — the SAP call would pass unchecked. exit 2 blocks without needing jq.
command -v jq >/dev/null 2>&1 || { echo "pre-cud-guard: jq not found on PATH - blocking SAP call (fail closed). Install jq and restart VS Code." >&2; exit 2; }

# --- Local (non-transportable) packages exempt from the TR requirement (rule §2). ---
# Single source: LOCAL_NO_TR_PACKAGES in .claude/common/system-config.md = $TMP + package ZLOCAL
# + every package below ZLOCAL (the hook only sees the package NAME, not the SAP hierarchy, so
# each sub-package is listed by name — add a new one there when it is created under ZLOCAL).
# Comma/space separated; entries may use shell globs; matched case-insensitively.
# Missing/unreadable config -> empty list -> TR required everywhere (fail closed).
source "$(dirname "$0")/lib-config.sh"
LOCAL_NO_TR_PACKAGES=$(cfg LOCAL_NO_TR_PACKAGES | tr ',' ' ')

input=$(cat)
tool_input=$(echo "$input" | jq -c '.tool_input // {}' 2>/dev/null || echo '{}')
payload=$(echo "$tool_input" | tr '[:upper:]' '[:lower:]')

deny() {
  jq -n --arg reason "$1" \
    '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":$reason}}'
  exit 0
}

# Rule: the agent must never create/delete/modify a Transport Request itself.
# Only explicit, SAP-specific TR tokens count — a bare "tr" is likely a *reference* to an
# existing TR on an object-CUD call and must pass through to the checks below.
tr_token='(transport[_ ]?request|trkorr)'
verb='(create|delete|remove|release|change|modify)'
if echo "$payload" | grep -qE "${tr_token}.{0,60}${verb}" \
   || echo "$payload" | grep -qE "${verb}.{0,60}${tr_token}"; then
  deny "sap-dev-rule.md: agent must never create/delete/modify a Transport Request. Stop and ask the user to supply/manage the TR."
fi

# Object names: (1) params keys used by create/edit payloads, (2) the "TYPE NAME" in `target`
# (for action=edit the name lives ONLY in `target`, e.g. "CLAS ZCL_X").
obj_name=$(echo "$tool_input" | grep -oE '"(object_name|objectname|obj_name|name|class_name|program_name|interface_name|function_name|target_name)"[[:space:]]*:[[:space:]]*"[^"]+"' \
  | head -1 | sed -E 's/.*:[[:space:]]*"([^"]+)"/\1/' || true)
target_name=$(echo "$tool_input" | jq -r '(.target // "") | tostring | split(" ")[1] // ""' 2>/dev/null || true)

# Rule: Custom Z/Y objects only — never touch Standard objects (rule §2). Used by CUD and edit calls.
check_zy() {
  local n first
  for n in "$obj_name" "$target_name"; do
    [[ -z "$n" ]] && continue
    first=$(echo "${n:0:1}" | tr '[:upper:]' '[:lower:]')
    if [[ "$first" != "z" && "$first" != "y" ]]; then
      deny "sap-dev-rule.md: Custom Z/Y objects only. Target object '$n' does not match Z*/Y* naming — never touch Standard objects."
    fi
  done
}

# Below only applies to calls that look like an object CUD action.
if echo "$payload" | grep -qE '"(action|operation|method)"[[:space:]]*:[[:space:]]*"(create|insert|update|modify|delete|activate)"' \
   || echo "$payload" | grep -qE '\b(create|insert|update|modify|delete|activate)_object\b'; then

  # --- Package: mandatory for every object CUD (rule §2). Read value from "package"/"package_name". ---
  pkg=$(echo "$tool_input" | grep -oE '"(package|package_name)"[[:space:]]*:[[:space:]]*"[^"]+"' \
    | head -1 | sed -E 's/.*:[[:space:]]*"([^"]+)"/\1/' || true)
  if [[ -z "$pkg" ]]; then
    deny "sap-dev-rule.md: Package mandatory for object CUD — no \"package\"/\"package_name\" in payload. Stop and ask the user."
  fi

  # --- Is the package a LOCAL (non-transportable) package exempt from the TR requirement? ---
  pkg_lc=$(echo "$pkg" | tr '[:upper:]' '[:lower:]')
  is_local="no"
  for entry in $LOCAL_NO_TR_PACKAGES; do
    entry_lc=$(echo "$entry" | tr '[:upper:]' '[:lower:]')
    # shellcheck disable=SC2254
    case "$pkg_lc" in
      $entry_lc) is_local="yes"; break ;;
    esac
  done

  # --- TR: mandatory for transportable packages (SID + K/T + 6 digits, e.g. GM2K900123). ---
  # Skipped for local packages in LOCAL_NO_TR_PACKAGES (rule §2 local exception).
  if [[ "$is_local" == "no" ]]; then
    if ! echo "$payload" | grep -qE '[a-z0-9]{3}[a-z][0-9]{6}'; then
      deny "sap-dev-rule.md: TR mandatory for object CUD in transportable package '$pkg' — none found. Ask the user to supply a TR (never auto-generate). If '$pkg' is a package below ZLOCAL, the user adds it to LOCAL_NO_TR_PACKAGES in .claude/common/system-config.md."
    fi
  fi

  # --- Rule: Custom Z/Y objects only — never touch Standard objects. ---
  check_zy
fi

# Edit of an EXISTING object (action=edit*): the payload carries no package/TR (the object already
# has both) so only Z/Y-only can be enforced here; package/TR discipline for edits stays with the
# agent (rule §2). Before 2026-09-21 this hook ignored action=edit entirely.
if echo "$payload" | grep -qE '"(action|operation|method)"[[:space:]]*:[[:space:]]*"edit[a-z_]*"'; then
  check_zy
fi

exit 0
