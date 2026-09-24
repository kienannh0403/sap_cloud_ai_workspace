#!/usr/bin/env bash
# Shared helpers for hooks: read KEY=value pairs from the ```env block of
# .claude/common/system-config.md (the single source for tier / servers / blocklist profile).
# Usage: source "$(dirname "$0")/lib-config.sh"; tier=$(cfg SAP_TIER)

HOOK_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
SYSTEM_CONFIG="$HOOK_ROOT/.claude/common/system-config.md"

# Print the value of KEY (empty if missing). Only lines inside the first ```env fence count.
cfg() {
  [[ -f "$SYSTEM_CONFIG" ]] || return 0
  awk -v key="$1" '
    /^```env[[:space:]]*$/ { inblock = 1; next }
    inblock && /^```/      { exit }
    inblock {
      sub(/\r$/, "")
      if (index($0, key "=") == 1) { print substr($0, length(key) + 2); exit }
    }' "$SYSTEM_CONFIG"
}

# "mcp__sap_gm2_cus_ro__SAP" -> "sap_gm2_cus_ro"
mcp_server_of() {
  local t="${1#mcp__}"
  echo "${t%%__*}"
}

# True if word $1 is in the comma/space separated list $2.
in_list() {
  local item="$1" list="${2//,/ }" w
  for w in $list; do [[ "$w" == "$item" ]] && return 0; done
  return 1
}

# Resolve a Python that actually runs (on Windows "python3" can be a Store alias stub).
pick_python() {
  if python3 -c '' >/dev/null 2>&1; then echo python3; else echo python; fi
}
