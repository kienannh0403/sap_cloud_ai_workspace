# Lean SAP I/O — keep checks complete, keep the conversation small (user 2026-10-06)

The user asked to cut token use without dropping any check. Every rule below keeps the full evidence — it moves
bulk output into files and reads only what the step needs. Rule §8/§11 (evidence) is unchanged.

## 0. Session length is the biggest cost (user 2026-11-16)
Every turn re-reads the whole conversation. Measured on ZGL02 session 624dbb89: 1,563 turns at ~250k context each
= 395M cache-read tokens, ~70% of the session cost; all tool output together was a fraction of that. So:
- **One report per session, compacted between fixes** (user 2026-11-16: "mỗi session anh làm một báo cáo"). The
  session keeps the report's continuity; the context must not keep every old excerpt. At each boundary — a
  fix/update through its 4 gates, a TS handed off, a target-refresh / preview done — record the outcome in
  `artifacts/targets/<T>/notes/` + `INDEX.md` (what changed, where, why, test result), then tell the user to run
  `/compact giữ: trạng thái <T>, quyết định đã chốt, lỗi đã gặp, việc đang dở; bỏ: đoạn source và output tool cũ`.
  ~150k → ~20–30k, same session. Estimate for 10 fixes × ~100 steps: ~135M tokens uncompacted vs ~35M compacted.
- After a compact, re-read only the source region the next request needs from a fresh pull — a source excerpt
  from before the compact may be stale (the class was edited since), never use it as an anchor or evidence.
- `context-budget.sh` (UserPromptSubmit + Stop) warns at `CONTEXT_BUDGET_TOKENS` (120k) and every
  `CONTEXT_BUDGET_STEP` (40k) above it, naming the active target: finish the current fix, record, propose the compact
  — do not start the next fix first. A new session (`/clear`) is for another report, with [Skill: handoff] only if
  work on this one is left unfinished.

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

## 3a. The edit result is compacted for you (`tool-output-shrink.sh`, user 2026-11-16)
vsp's `edit` result echoed `oldString` + `newString` and the syntax warnings of the WHOLE object on every call
(~8k chars per edit on a 6,000-line class, 34% of all tool output in the ZGL02 session). The PostToolUse hook now
rewrites it before it reaches the conversation — measured on 125 real ZGL02 edits: −77…89%:
- `oldString` / `newString` dropped; every other key (success, activation messages, errors, matchCount) kept verbatim.
- First edit of an object in the session: `syntaxWarnings_grouped` — each distinct text once, with all its lines.
  Later edits: `syntaxWarnings_new` (only warnings not in the previous edit of that object) + counts.
- `syntaxErrors` identical to `syntaxWarnings` (vsp refuses an edit over warnings: "Use ignore_warnings=true")
  → one note instead of the repeat; otherwise `syntaxErrors_grouped`, texts never seen as a warning first.
- `full_output` = file with the verbatim response — the Gate 1 evidence to cite.
- A SAML login page (expired cookie) becomes one line naming the server and [Skill: sap-doctor].
- On an object that carries pre-existing warnings, the first edit is refused with that message: assess the
  grouped warnings (Gate 1), then retry with `ignore_warnings: true` — never pass it before that assessment.

## 4. Screenshots: taken and kept, not opened by default (user 2026-11-16)
- Take as many screenshots as you like (they cost nothing until read) and keep them as the user's evidence; judge
  from the step log (rows, columns, labels, messages, console/HTTP errors) — [Skill: fiori-ui-check] Step 4.
- Open one only for a row that is visual by nature (overlap, cut-off, layout) or an anomaly the log text cannot
  explain; crop to the region first (`python .claude/skills/fiori-ui-check/scripts/crop.py <png> <x0> <y0> <x1> <y1>`
  or `--rows y0 y1`), at most ~3 per run. A visual-only row not opened stays `Proof: manual` with the file path.

## 4a. Shell and SQL output: ask for little, the hook cuts the rest (user 2026-11-16)
`tool-output-shrink.sh` cuts Bash/PowerShell stdout over `TOOL_OUTPUT_CAP_BASH` (6000 chars), SAP `query` output
over `TOOL_OUTPUT_CAP_SQL` (4000) and any other SAP output over `TOOL_OUTPUT_CAP_SAP` (15000) to head + tail; the
full text is saved under `artifacts/scratchpads/_session/tool-output/` (git-ignored, pruned after 7 days) and the
cut names that file. The cap is a safety net — a cut output was still paid for in part, so ask small first:
- `grep -c` (how many) before `grep -n`; then `grep -n -m 20` or `| head -40`. Never `grep -r` the whole workspace
  without `--include` and a limit.
- `sed -n 'a,bp'` at most ~80 lines per call; find `a,b` with `grep -n` first.
- Scripts you write print counts and the deciding lines; bulk results go to a file you then grep.
- SQL: name the columns you need (never `SELECT *`), `UP TO 50 ROWS`, `COUNT(*)` first when the size is unknown;
  a full extract goes to a file, not into the chat.
- When the whole output is really needed (a diff you must review line by line), put `#full-output` in the command
  — once, deliberately.

## 5. Chat
The user reads the reports in full (2026-10-06: "anh cần đọc kĩ những gì em làm để nắm tình hình") — keep the
explanations; the savings come from 1–4, not from shorter answers.
