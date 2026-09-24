#!/usr/bin/env bash
# PreCompact: write a small snapshot of where the work stands (git status + recently changed
# ledgers/handoffs) to artifacts/scratchpads/_session/precompact_<ts>.md, keep the newest 10,
# and remind the model to run [Skill: handoff] if a workflow is mid-way (rule §10).
# It does not replace the handoff — it only guarantees a trace exists if the handoff was skipped.
# Adapted from sc4sap pre-compact.mjs. Never blocks compaction.
set -uo pipefail
source "$(dirname "$0")/lib-config.sh" 2>/dev/null || exit 0

input=$(cat)
trigger=$(echo "$input" | jq -r '.trigger // "auto"' 2>/dev/null || echo auto)
root="$HOOK_ROOT"
dir="$root/artifacts/scratchpads/_session"
mkdir -p "$dir" 2>/dev/null || exit 0
ts=$(date +%Y%m%d_%H%M%S)
out="$dir/precompact_$ts.md"

{
  echo "# Pre-compact snapshot ($ts, trigger=$trigger)"
  echo
  echo "Auto-written by .claude/hooks/pre-compact.sh. Not a handoff — see the ledger/handoff files below."
  echo
  echo "## git status --short"
  echo '```'
  git -C "$root" status --short 2>/dev/null | head -40
  echo '```'
  echo
  echo "## Ledgers / handoffs changed in the last 24 h"
  find "$root/artifacts/scratchpads" -maxdepth 2 -type f \( -name 'ledger*.md' -o -name 'handoff_*.md' \) \
    -mmin -1440 -printf '- artifacts/scratchpads/%P\n' 2>/dev/null
} > "$out"

# Keep only the newest 10 snapshots.
ls -1t "$dir"/precompact_*.md 2>/dev/null | tail -n +11 | xargs -r rm -f

msg="Compaction starting. Snapshot: artifacts/scratchpads/_session/precompact_$ts.md. If a workflow is mid-way and no fresh handoff exists, the next turn must run [Skill: handoff] first."
jq -n --arg m "$msg" '{"systemMessage":$m}'
