#!/usr/bin/env bash
# UserPromptSubmit reminder (advisory, never blocks): when the prompt names a target that already has
# artifacts/targets/<TARGET>/handbook.json, remind the agent to run skill target-refresh first —
# a change the user made in ADT without telling the agent must become its own version before new work
# (.claude/common/handbook-target.md). Matching is by whole word, case-insensitive.
set -uo pipefail
source "$(dirname "$0")/lib-config.sh"

prompt=$(jq -r '.prompt // ""' 2>/dev/null || true)
[[ -z "$prompt" ]] && exit 0

hits=()
for hb in "$HOOK_ROOT"/artifacts/targets/*/handbook.json; do
  [[ -f "$hb" ]] || continue
  t=$(basename "$(dirname "$hb")")
  if echo "$prompt" | grep -qiE "(^|[^A-Za-z0-9_])${t}([^A-Za-z0-9_]|\$)"; then
    hits+=("$t")
  fi
done
[[ ${#hits[@]} -eq 0 ]] && exit 0

ctx="target-refresh reminder: the prompt names existing target(s) ${hits[*]}. Before any other step on them run [Skill: target-refresh] Part A (pull sources, drift_check.py; a change made outside the workspace becomes its own version with its real content first), and Part B (full preview with evidence) at the end."
jq -n --arg c "$ctx" '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":$c}}'
exit 0
