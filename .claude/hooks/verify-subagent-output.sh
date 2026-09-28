#!/usr/bin/env bash
# SubagentStop guard for the team agents (.claude/agents/*.md) - rule §12: "an agent's completion claim is
# unverified until you read its output on disk". Every team agent must end by naming the file(s) it wrote
# under artifacts/. This hook reads the agent's final message and:
#   - names no artifacts/ path at all            -> blocks once: "state the exact output path(s)"
#   - names a path that is missing or empty      -> blocks once: "the file is not on disk"
#   - a line starting "OUTPUT: none"             -> passes (read-only answer, e.g. skill ask-consultant)
# "Blocks once" = exit 2 the first time per agent_id (the agent continues and can fix it); the second stop is
# let through so a stuck agent cannot loop - the Manager still reads the files itself (rule §12).
# Other agent types (Explore, Plan, general-purpose...) are not checked.
set -uo pipefail
source "$(dirname "$0")/lib-config.sh"

input=$(cat)
agent_type=$(echo "$input" | jq -r '.agent_type // ""' | tr -d '\r')
agent_id=$(echo "$input" | jq -r '.agent_id // "unknown"' | tr -d '\r')
msg=$(echo "$input" | jq -r '.last_assistant_message // ""')

team=""
for f in "$HOOK_ROOT"/.claude/agents/*.md; do team+="$(basename "$f" .md) "; done
in_list "$agent_type" "$team" || exit 0

state_dir="$HOOK_ROOT/artifacts/scratchpads/_session/subagent-verify"
mkdir -p "$state_dir" 2>/dev/null
marker="$state_dir/$(echo "$agent_id" | tr -c 'A-Za-z0-9_-' '_')"
[[ -f "$marker" ]] && exit 0        # already blocked once for this agent - let it stop

block() {
  : > "$marker"
  echo "verify-subagent-output (rule §12): $1" >&2
  exit 2
}

# A read-only answer (e.g. skill ask-consultant) writes no file and says so explicitly.
echo "$msg" | grep -qE '^OUTPUT: none' && exit 0

paths=$(echo "$msg" | grep -oE 'artifacts/[A-Za-z0-9_./<>-]*[A-Za-z0-9_]\.[A-Za-z0-9]+' | grep -v '[<>]' | sort -u)
if [[ -z "$paths" ]]; then
  block "your final message names no output file. End with the exact path(s) under artifacts/ that you wrote (e.g. artifacts/targets/<TARGET>/build/<file>.md), or say BLOCKED and why; a read-only answer ends with a line 'OUTPUT: none'."
fi

bad=()
while IFS= read -r p; do
  f="$HOOK_ROOT/$p"
  if [[ ! -f "$f" ]]; then bad+=("$p (missing)")
  elif [[ ! -s "$f" ]]; then bad+=("$p (empty)"); fi
done <<< "$paths"
if [[ ${#bad[@]} -gt 0 ]]; then
  block "these files named in your final message are not on disk: ${bad[*]}. Write them, or correct the paths in your final message."
fi
exit 0
