---
name: sap-analyze-symptom
description: Read-only root-cause triage of a runtime symptom on SAP Public Cloud — a short dump / runtime error, an app or OData call that fails, a RAP save that pops up an error, wrong numbers with no mock data yet — by reading dumps, traces, inactive objects, where-used / impact and the object sources through the SAP MCP server, narrowing hypotheses with as few user questions as possible, then handing a confirmed root cause to /sap-dev-bug-fix. Use when the user reports "bị dump", "lỗi runtime", "app báo lỗi", "short dump", "ABAP runtime error", "OData lỗi 500", "không lưu được", or pastes an error message and does not yet know which object is wrong.
---

# Analyze Symptom — find the cause before anyone fixes anything

Read-only. This skill never edits, activates, deletes, runs ABAP (`analyze type=execute_abap`) or sets breakpoints
(`action=debug`) — the fix belongs to `/sap-dev-bug-fix` after the user approves it.

## Step 1 — capture the symptom (one round of questions, max 3)
What the user did (app / service / report + action), when (date, time, roughly), which system/client (080 dev test or
100 test — both readable), the exact message text or a screenshot. Everything else comes from the system.

**Then look the error up in the codex before collecting anything:** `python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py find "<message ID / HTTP status /
exception / log text>"` (try 2-3 keys from the message). A hit gives known root causes with their proof
(`verified`, `evidence`) — Step 2 then checks whether THIS case matches one of them instead of starting blind;
an entry with `verified: false` is a hypothesis, not a finding. Several hits on one key = several known causes:
the evidence decides which. Format and rules: `artifacts/system_analysis/ERROR_CODEX/README.md`.

## Step 2 — collect evidence from SAP (`mcp__<server>__SAP`, load with ToolSearch first — rule §9)
Run on the client where the symptom happened; cookie dead → [Skill: sap-doctor].

| Evidence | Call | Look for |
|---|---|---|
| Runtime errors | `SAP(action="analyze", params={"type": "list_dumps"})`, then `get_dump` with the matching `dump_id` | error class, program/include/line, the Z object on the call stack closest to the error |
| Inactive or broken objects | `analyze type=inactive_objects`; `analyze type=syntax_check` on the suspect | a half-activated chain (memory `activate-success-is-not-active`) |
| Who calls what | `analyze type=callers` / `callees` / `impact` / `references` on the suspect | whether a recent change in a dependency is the real cause |
| Performance / SQL | `analyze type=list_traces`, `get_trace`; `list_sql_traces` (only if a trace was recorded) | long-running statements, SELECT in loop |
| Source | `SAP(action="read", target="<TYPE> <NAME>")` — the line the dump points to, plus its method | the actual statement, not a guess |
| Recent change | the target's handbook / `build/snapshot/` (skill target-refresh), `git log` of the target folder | a change the handbook does not know about |

`list_dumps` verified on client 100 (2026-09-28): it returns every user's dumps of the system, newest first, with
`title` (error text), `category` (the program/class, e.g. `ZCL_…========CP`), `timestamp` and the `id` to pass to
`get_dump` — filter by the time and the object the user named; `user`/`client` come back empty. `get_dump` verified the
same day: it returns the dump as HTML (`rawHtml`) holding runtime error name, short text, user, client, the
include + line where it terminated, a source extract and the call stack. Check the package of the failing object
first — a dump in someone's personal/local package (`LOCAL_NO_TR_PACKAGES`) run from the ADT console is usually their
experiment, not a project defect: report it and ask before analysing further. Traces not yet exercised. A dump shows variable values: treat any business data in it like a
data read (`.claude/exceptions/`) — quote field names and error text, never customer/pricing/personal values.

## Step 3 — hypotheses
List 1–3 hypotheses, each with the evidence for and against it and the one check that would decide it. Run that check
(read-only) before asking the user anything. Known traps to test first on RAP apps: message without `failed` → HTTP 412
"Proceed anyway?" (memory `rap-failed-vs-reported-412-popup`); text cut at 50 characters (memory
`rap-message-text-50-char-limit`); `%control` overwriting fields (memory `rap-modify-control-vs-update-fields`).
Three rounds without a confirmed cause → stop and say so (rule §7 "one more fix" applies to diagnosis too).

## Step 4 — report and hand-off
Write `artifacts/targets/<TARGET>/analysis/symptom_<yyyymmdd>.md` (the target the failing object belongs to — its
INDEX.md; no folder yet → create folder + INDEX.md per rule §4):
- symptom as reported · evidence collected (call + what it returned) · root cause **confirmed / probable** with the
  proof · affected objects · suggested fix direction (no code) · regression risk.
- One line in the target's INDEX.md; a trap worth remembering → `notes/<topic>.md`.
- Root cause **confirmed** → update the codex (README "Khi nào ghi"): same cause as an entry → add an
  `occurrences` row; new cause → new entry with `evidence` pointing at this report. Then `codex.py check` exit 0.
  A probable (unproven) cause is not written to the codex.
Then offer `/sap-dev-bug-fix` with this report as its input — the report replaces its "mock data" interview only for
the facts it proved.
