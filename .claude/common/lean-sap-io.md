# Lean SAP I/O — keep checks complete, keep the conversation small (user 2026-10-06)

The user asked to cut token use without dropping any check. Every rule below keeps the full evidence — it moves
bulk output into files and reads only what the step needs. Rule §8/§11 (evidence) is unchanged.

## 1. Checks → condensed output, full result in a file
- ATC and inactive objects: `.claude/scripts/atc/atc_check.py` ([Skill: activation-guard] Gates 2 and 4) — one line
  per object on the console, every finding saved under `artifacts/targets/<T>/build/atc/`. MCP ATC only as fallback.
- Same idea for any bulk read you write yourself: send the response to a file in the session scratchpad (or the
  target's `build/`), then print counts / the few lines that decide the step.

## 2. Read source by method or by grep, not whole
- One method: `SAP(action="read", target="CLAS <name>", params={"method": "<METHOD>"})`.
- Find the place first: pull the source to a file with curl (`/sap/bc/adt/oo/classes/<name>/source/main`,
  `/includes/implementations`, `/ddic/ddl/sources/<name>/source/main` …, cookie from `.mcp.json`) and `grep -n`
  the identifiers — read only the matching region (`sed -n 'a,bp'`).
- `params={"include_context": false}` on every full read you do need — the dependency context is often larger
  than the object.
- Read a whole object only when the task is to understand all of it (code analysis of that object, a rewrite).
  Then read it once, keep the pulled file, and grep that file afterwards instead of re-reading.

## 3. `EDITSOURCE` with the shortest unique anchor
`old_string` and `new_string` travel to SAP and come back in the result — a 20-line anchor costs ~80 lines for a
4-line change. Instead:
1. Pull the current source to a file; pick ONE line next to the change that occurs exactly once
   (`assert source.count(anchor) == 1`); if it repeats, add the neighbouring line until it is unique.
2. Pure insertion: `old` = anchor line, `new` = anchor line + inserted lines.
3. Dependent changes (a JOIN and the column that uses it, a declaration and its use): one call per change, ordered
   so that every intermediate state compiles (declare / join first, use after) — EDITSOURCE syntax-checks and
   activates each call. Merge into one long anchor only when no compiling order exists.
4. Completeness check, always: build the expected file locally by applying the same patches to the pulled source,
   then after the last patch pull the whole source from SAP and diff it against that expectation — must be
   identical. SAP also refuses a patch whose anchor matches 0 or >1 times (`matchCount`).

## 4. Screenshots: read only what the step needs, cropped
- Take as many screenshots as you like (they cost nothing until read); Read only the ones that prove a checklist
  row, and crop to the region first:
  `python .claude/skills/fiori-ui-check/scripts/crop.py <png> <x0> <y0> <x1> <y1> [out.png]`
  (or `--rows y0 y1` for a full-width band).
- A value in the step log (rows, columns, messages) is cheaper than a picture — use the picture for layout,
  labels, overlap and anything visual only.

## 5. Chat
The user reads the reports in full (2026-10-06: "anh cần đọc kĩ những gì em làm để nắm tình hình") — keep the
explanations; the savings come from 1–4, not from shorter answers.
