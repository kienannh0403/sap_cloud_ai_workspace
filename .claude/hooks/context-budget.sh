#!/usr/bin/env bash
# UserPromptSubmit + Stop: watch the live context size of this session (token budget, user 2026-11-16).
# Logic and thresholds: context_budget.py. Advisory, never blocks; fail open without Python.
source "$(dirname "$0")/lib-config.sh"
py=$(pick_python)
command -v "$py" >/dev/null 2>&1 || exit 0
exec "$py" -X utf8 "$(dirname "$0")/context_budget.py"
