---
name: target-refresh
description: Step 0 of every workflow that touches an existing report/function target (artifacts/targets/<TARGET>/) — pull the current source of every Z object of the target from SAP, detect changes made outside this workspace since the last recorded version (drift_check.py), record such a change as its own intermediate version with its real content BEFORE starting the new work, and at the end run the full preview (test run, ATC over the whole target, INDEX/notes, snapshot, handbook render) with evidence per item. Use whenever the user asks to update, fix, extend, re-test, review or re-document a report/function that already has a folder under artifacts/targets/, even if they do not say "preview" and even if they say nothing changed.
---

# Target Refresh — "preview lại" every time a target is touched

## Why this exists

The user can change a target's objects in ADT without telling the agent. Example: version 2.0 recorded
on 23/09, the user edits on 25/09, then on 26/09 asks for version 4.0 → the 25/09 change has no record,
no ATC, no test. This skill closes that gap: every touch starts by comparing SAP against the last
recorded snapshot, and every touch ends with a full preview whose evidence is written into the handbook.
Schema of `snapshot` / `preview` / `period`: `.claude/common/handbook-target.md`.

## Part A — at the start (before any other step of the workflow)

1. **Read** `artifacts/targets/<TARGET>/INDEX.md` and `handbook.json`. No folder yet → this skill does not
   apply; the calling workflow creates the record (handbook-target.md "First workflow on the target").
2. **Pull sources.** For every Z/Y object in `handbook.json.objects[]` read the active source from the WRITE
   server (`WRITE_SERVERS`, `.claude/common/system-config.md`) with
   `SAP(action="read", target="<TYPE> <NAME>", params={"include_context": false})` and save it unchanged to
   `artifacts/targets/<TARGET>/build/snapshot/<yyyymmdd>/<NAME>.<ext>` (`.abap` classes/programs, `.asddls` CDS,
   `.asbdef` BDEF, `.srvd` service definition, `.ddlx` metadata extension, `.txt` otherwise).
   `objects[]` empty (target never built) → skip to the workflow. A read that fails → STOP and report the
   exact error; a refresh with a missing object is not a refresh.
3. **Compare:** `python .claude/scripts/handbook/drift_check.py <TARGET>`
   - exit 0 → no drift, go on to the workflow.
   - exit 2 → no baseline yet: record it into the newest version
     (`drift_check.py <TARGET> --record <newest version>`) and go on. Say so to the user — changes made
     before this first snapshot cannot be detected.
   - exit 1 → drift, do step 4 before anything else.
   - exit 3 → input problem, fix it (message says what), never skip.
4. **Record the external change as its own version**, completely, before the new work starts:
   - New block at the top of `versions`: next major number, `source: "sửa ngoài workspace"`,
     `date` = today, `period` = "giữa <baseline snapshot date> và <today>" (the exact date/author only if SAP
     actually returned them — never guess).
   - `changes` = **the real content of the change**, read from `build/snapshot/<today>/drift.diff`: per
     object one or more lines saying what changed in business/logic terms ("ZR_FI_ZAA01: công thức (22)
     thêm điều kiện lọc TSCĐ legacy", "ZC_…: thêm cột X"), plus added/removed objects. Never "có thay đổi".
     Show these lines to the user and ask whether the change was intended / anything to add.
   - ATC over every object of the target → `atc`; re-run the previous version's test cases (group
     "Hồi quy") → `tests`, results with evidence as usual (rule §11).
   - Close it: `drift_check.py <TARGET> --record <that version>`, add its `preview` block (Part B list),
     `python .claude/scripts/handbook/render_target.py <TARGET>`, one line in INDEX.md.
   - Only now open the version for the user's request.

Read-only workflows (code-analysis, code-review) run steps 1–3 only; on drift they report it to the user
and ask whether to record the intermediate version — they never open a new version themselves.

## Part B — at the end (always, even when nothing drifted and even for a small change)

Run the full preview and write one `preview` block into the version just closed:

| item | what to do | evidence |
|---|---|---|
| `test` | run the report/app: data preview / OData verify per the workflow's verify phase | `build/odata_verify/…` |
| `atc` | ATC over **every** object of the target (not only the diff) | the version's `atc` block |
| `objects` | `objects[]` matches what exists in SAP (added/removed objects, `uses` edges) | `handbook.json` |
| `snapshot` | pull sources again (Part A step 2) and `drift_check.py <TARGET> --record <version>` | `build/snapshot/<yyyymmdd>/` |
| `index` | INDEX.md status, open questions, file map up to date | `INDEX.md` |
| `notes` | every finding worth keeping as `notes/<topic>.md`, linked from INDEX.md | `notes/…` or "không có finding mới" |
| `handbook` | `python .claude/scripts/handbook/render_target.py <TARGET>` | `artifacts/handbook/<target>.html` |

Each item: `{"item": "...", "status": "done|skipped", "evidence": "<path>", "note": "..."}`. An item that
cannot be done (e.g. 080 has no data-read authorization) is `skipped` **with the reason in `note`** — never
left out, never marked done without its evidence (rule §8, §11). The handbook render comes last so the page
shows the finished preview.
