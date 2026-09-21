---
name: handoff
description: Summarizes current progress, outstanding tasks, and crucial context into a structured handoff note; use before context runs out or compaction occurs, or whenever work needs to transition seamlessly to another agent or a new session.
---

# Handoff

Preserve working state across a compaction or session boundary so the next agent/session can resume without re-deriving anything.

## Instructions

1. Review the current state of the task, including completed steps and remaining open items.
2. **Check whether a handoff file already exists** at the target path below. If it does, Read it first and **append** the new progress + rewrite only the "Next Steps" section. Never overwrite — that destroys the "Tried & Failed" history, which is the part with the longest shelf life.
3. Generate a concise but comprehensive markdown summary containing:
   - **Current Status**: What has been achieved. State verified facts only — "activated, Gate 1-3 passed" or "created, not yet activated", never "should be done" (rule §8).
   - **WIP**: What is currently being worked on.
   - **Next Steps**: Explicit instructions for the next agent or session.
   - **Tried & Failed**: Approaches already attempted that did NOT work, each with the reason. This is what stops the next session walking back into the same dead end, and it is the state rule §7 depends on ("one more fix" after ≥3 attempts means it is an architecture/TS problem — the next session can only know the count if it is written down). Carry this section forward on every update.
   - **Critical Context**: Important constraints, bugs encountered, or decisions made — including TR number, package, and system/connection in SAP workflows.
   - **Ledger Pointer**: If a [Skill: scratchpad] ledger exists for this work, give its exact path and state which rows are DONE / IN PROGRESS / REGRESSED. The ledger is the single source of truth — a handoff without it loses the most critical state.
4. **Redact before writing.** Scan the content you are about to save and strip any `client_secret`, token, password, cookie, API key, or customer personal data — replace with `<redacted>`. If you are unsure whether a string is a secret, redact it; do not reason your way to "probably safe". Reference artifacts **by path**, never by pasting their contents — a handoff is an index, not a store.
5. Save the summary to `artifacts/scratchpads/<TARGET>/handoff_<yyyymmdd>.md` (rule §4: all outputs under `artifacts/`, one sub-folder per target; use `artifacts/scratchpads/handoff_<topic>_<yyyymmdd>.md` only when the work has no single target), then tell the user the path. Present inline instead only if the filesystem is unavailable.
