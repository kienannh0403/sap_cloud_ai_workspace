---
description: Sử dụng workflow này khi người dùng yêu cầu tạo mới report dựa trên ABAP RAP Model, đọc Technical Specification (TS) do `/sap-dev-fs-analytic` sinh ra và triển khai đúng theo Coding Implementation Plan trong TS — không tự thiết kế hay tự tìm kiếm thêm thông tin ngoài TS.
argument-hint: <package> <transport-request> <ts-file-path>
---

> **Claude Code note:** `[Skill: X]` below means invoke the `x` skill via the Skill tool (auto-discovered from `.claude/skills/x/`). Where a step needs an MCP tool not yet loaded (e.g. an ADT/system-connection tool), use `ToolSearch` first (see `sap-dev-rule.md` §9).

[ROLE & OBJECTIVE]
Act as an Expert SAP ABAP Cloud Developer with SYSTEM EXECUTION PRIVILEGES. CREATE, VALIDATE, and ACTIVATE the complete ABAP RAP Model artifacts described in the TS's Coding Implementation Plan (§9). Use your equipped skills (rap, cds-view-entities, cds-analytical-views, cds-virtual-element, abap, abap-cloud, naming-convention, abap-unit-testing) to guarantee ABAP Cloud syntax, Clean Core, and strict(2) compliance.

[INPUT DATA]
Package Name: [Điền tên Package]
Transport Request: [Điền TR, hoặc "Local Object"]
Technical Specification: [Đường dẫn tới TS_[ReportName].md sinh ra bởi /sap-dev-fs-analytic]
Additional Requirements: [Các yêu cầu thêm]
Arguments: $ARGUMENTS

[GOVERNING RULES]
This workflow operates under the Iron Laws, Red Flags, and Token Efficiency rules in `sap-dev-rule.md` (§6-10). In particular: NO OBJECT CREATION WITHOUT TS COVERAGE — if the TS's Coding Implementation Plan doesn't cover something you need, STOP, do not invent it; "Activated" ≠ "correct" — Phase 2 verifies correctness separately, and [Skill: activation-guard] verifies *activation itself* is genuinely clean and non-cascading before that; Validation Log / Activation Status updates use [Skill: caveman]; never re-print the full TS, quote only the row/section needed for the current step.

[EXECUTION PROTOCOL — 4 PHASES]

**Target refresh (mandatory when `artifacts/targets/<TARGET>/` already exists):** [Skill: target-refresh] Part A before Phase 0 — a change made outside this workspace since the last recorded version becomes its own version, with its real content, before this run opens a new one; Part B (full preview with evidence per item) after the last phase.

## Phase 0 — Input Validation Gate

0.0 VALIDATE INPUT, in order:
- The TS file exists and contains all 11 sections of the template, especially §9 Coding Implementation Plan with at least one row.
- Transport Request is a valid TR number or explicitly "Local Object".
- Package exists / is a valid target.
- Every source view listed in TS §9 is marked released/verified per TS §3.

If ANY check fails → 0.1. If all pass → 0.2.

0.1 GRILL-ME ON GAPS: Use [Skill: grill-me] (max 1-3 targeted questions) to collect exactly the missing information from 0.0. Do not proceed until 0.0 fully passes. If the gap is in the TS content itself (not just Package/TR), tell the user to re-run/patch `/sap-dev-fs-analytic` instead of improvising here.

0.2 TASK LEDGER: Use [Skill: scratchpad] (Ledger Format) to create `artifacts/targets/[ReportName]/build/scratchpad.md`, one row per object from TS §9 in the TS's specified order, status TODO/DOING/DONE/FAILED/REGRESSED. This ledger is the single source of truth for build progress — if the session is interrupted or context is compacted, re-read the ledger instead of re-deriving progress from memory.

0.3 TR BINDING: Extract the TR from [INPUT DATA]. Every tool call that creates or edits an SAP object must explicitly pass the transport/correction-number parameter matching this TR, to prevent an unwanted auto-generated TR. Verify the exact parameter name/tool signature available in your environment before first use (`sap-dev-rule.md` §9) — if the tool isn't loaded yet, use `ToolSearch` to find it; do not assume a hardcoded tool name.

## Phase 1 — Sequential RAP Build (per TS §9, in the TS's specified order)

For each row in TS §9, execute the matching step below in order. **Never build an object or logic absent from TS §9** — if something is missing, STOP and escalate via 0.1.

Per step: GENERATE (draft per the row's spec) → check the name against [Skill: naming-convention] → VALIDATE (Lint via [Skill: abap], fix Critical/Major) → DEPLOY & ACTIVATE → [Skill: activation-guard] (all 4 gates must pass) → update the ledger row. When a row goes DONE, append the object to `objects` in `handbook.json` (`name`, `type`, one-line `role`, `uses` = the objects/released views it reads or builds on) — this drives the handbook object diagram. On activation ERROR: read the exact system error (never guess), consult [Skill: abap-cloud], auto-correct and retry; on a chain of errors use [Skill: handoff] to pause and ask the user. On WARNING: resolve if it violates strict(2), otherwise report as unavoidable — never accept it just because activation returned "success". If Activation Guard's Gate 3 finds a previously-DONE row broke as a side effect of this step, mark that row `REGRESSED` (not a fresh `FAILED`), fix it before continuing forward, then re-run all 4 gates on it.

**Step 1 — Query Data (CDS Data Models):** [Skill: cds-view-entities] + [Skill: find-released-cds-view]. Re-verify sources are released (should already hold per TS §3/§9). Create the Interface View (`DEFINE ROOT VIEW ENTITY`), associations, `@AccessControl.authorizationCheck: #CHECK`, auxiliary views if needed. If TS §9 calls for aggregation, a join, or an input parameter in this view's query logic, also use [Skill: cds-analytical-views] for that part of the syntax. Execute: Lint → Push → Activate → [Skill: activation-guard]. If TS §9 specifies a Custom Entity (`CE_` prefix) instead of a standard CDS Interface View, use [Skill: rap-query-provider] to implement `IF_RAP_QUERY_PROVIDER` (paging/sorting/filtering) in place of the standard BDEF-driven read in this step and Step 3.

**Step 2 — Access Control (DCL):** [Skill: authorization-iam]. Create `DEFINE ROLE` with `pfcg_auth` per TS §10. Execute: Lint → Push → Activate → [Skill: activation-guard].

**Step 3 — Behavior Definition (Base):** [Skill: rap]. Managed/unmanaged per TS, draft handling if applicable, actions/determinations per TS §5/§7. Execute: Lint → Push → Activate → [Skill: activation-guard] (Gate 3 here specifically re-checks Step 1's Interface View is still clean under the new behavior).

**Step 4 — Class Implementation (Behavior Pool):** [Skill: rap] + [Skill: abap-sql-amdp] + [Skill: modern-abap-syntax]. Skip if Read-only. Implement exactly the logic documented in TS §5 — no additional logic beyond it. If TS §7 specifies a business event to raise on an action/determination, use [Skill: rap-business-events] to define and raise it here. Execute: Lint → Push → Activate → [Skill: activation-guard].

**Step 4.5 — Side-task (optional, non-blocking):** [Skill: abap-unit-testing] — generate a test class skeleton for the Step 4 class. In Claude Code, dispatch this via the Agent tool as a background/parallel task if the codebase warrants it; otherwise run inline right after Step 4 without blocking Step 5.

**Step 5 — Projection View & Metadata Extension:** [Skill: cds-view-entities] for the projection view itself; [Skill: cds-analytical-views] owns the `@UI`/value-help annotation syntax for the Metadata Extension. Create the projection (`AS PROJECTION ON`) with `@Search`, `@EndUserText`, `@Metadata.allowExtensions: true`. Do NOT put `@UI` annotations in the projection — generate the full Metadata Extension source and save it to `artifacts/targets/[ReportName]/ddlx/ZMD_[ReportName].md`; tell the user to create the DDLX object manually in Eclipse ADT (the automated tool cannot create DDLX objects directly). Execute: Lint → Push → Activate → [Skill: activation-guard] (Projection View only).

**Step 6 — Projection Behavior:** [Skill: rap]. Skip if no Base BDEF. Execute: Lint → Push → Activate → [Skill: activation-guard].

**Step 7 — Service Definition & Binding:** [Skill: odata]. Create Service Definition, then Service Binding (OData V4 UI, per TS unless stated otherwise). Execute: Lint → Push → Activate → [Skill: activation-guard].

**Step 8 — Form templates (files, not SAP objects; only if TS §8 lists forms):** per §8 row — Excel → [Skill: excel-form-template], PDF → [Skill: pdf-form-template]; outputs in `artifacts/targets/[ReportName]/forms/` (spec + template + sample data). The skill's own gate still applies (no FS form sample → stop, the TS is wrong). Ledger row DONE only when the skill's build/check exits 0 (lint 0 errors / every binding resolves) — [Skill: activation-guard] does not apply to files. Uploading the template (Excel: app "Upload Template file excel"; PDF: Adobe form template store) is a user step → carried to 2.M together with a render check.

## Phase 2 — Runtime Verify Loop: self-verify data + UI, then manual remainder (max 3 iterations)

Start only once all Phase-1 objects are activated and have passed [Skill: activation-guard] (no open Gate-3 ripple issues, no `REGRESSED` rows). The expected side of every check is the **spec** — TS + `artifacts/targets/[ReportName]/fs/fs_markdown.md` (FS incl. transcribed mockups) — never a fixed checklist and never "what the build happens to contain". Helper scripts (read-only, HTTP GET only; host/cookie come from `.mcp.json`): `.claude/scripts/odata-verify/fetch.sh` and `ui-check.js` — run either without arguments for usage. Save every raw output under `artifacts/targets/[ReportName]/build/odata_verify/`.

2.0a PRECONDITION — can the read-only client see this build? Business data is readable only on the read-only server (client 100; the write client 080 returns 0 rows — no data-read authorization). Run `bash .claude/scripts/odata-verify/fetch.sh samecode <TYPE> <NAME>` for the Projection View, its Metadata Extension (once the user has created it), and the Behavior Pool if any. All `SAME` → 2.0b. Any `DIFFERENT`/`http…` → the build is not visible there yet: skip 2.0b/2.U, fall back to the manual route (ask the user to run the service and paste results, 2.1 evidence floor applies) and record why in the ledger.

2.0b DATA VERIFY (self-run). Service URL: `fetch.sh srvurl <read-only server> <SRVB>`. Cover **the whole spec**, not a sample:
- every output field of TS §3 / the Verified Data Model: `fetch.sh sample … '$top=20&$select=<all fields>'` → a field `EMPTY in every row` is a FAIL unless the spec says it may be empty;
- every rule of TS §5 (derived fields, complex logic, hardcoded filters) and every parameter/filter of TS §2, cases per the matrix below, derived from TS §3-§5. Express the expectation as an OData `$filter` whose count is predictable (e.g. rows violating the rule → `total=0`; rows of a known key/period → `total=N`), so the script's count output is the evidence. The script never prints field values — keep business data out of chat (`.claude/exceptions/`).
  **Case matrix (minimum per spec item; each case = one `TC-nn` row in the 2.3 log, its Case column naming the kind: dương / âm / biên / filter):**
  - **Every rule of TS §5** (derived field, complex logic, hardcoded filter, status that must/must not appear) → **2 cases**: *dương* — rows that satisfy the rule, expected `total=N` (exact N when the spec/test data fixes it, otherwise `total>0` for a value known to exist); *âm* — rows that violate the rule, expected `total=0` (e.g. rule "only released PRs" → `$filter=<status> ne '<released>'` → `total=0`).
  - **Rule with a threshold or range** (date/period, quantity, amount, "from–to", "≥ / <") → **+ biên cases**: one at exactly the boundary value and one just outside it, expected result per the spec's inclusive/exclusive wording (if the spec does not say which, that is a TS gap → ask the user, do not guess).
  - **Every parameter/filter of TS §2** → **2 cases**: a value known to exist → `0 < total ≤` unfiltered total; a value known not to exist → `total=0`. CDS input parameters: also one call without the parameter → expected error. Mandatory-filter enforcement and default values are UI behaviour (annotations) — they are checked in 2.U, not here.
  - Write every expected outcome in the checklist BEFORE running any query. A case that cannot be expressed as a count assertion, or for which the tenant has no suitable data, keeps the same dương/âm/biên design but moves to 2.M for the user — never marked PASS here.
- A rule that cannot be expressed as a count assertion, or needs data the tenant does not have → move it to 2.M, never mark it PASS.

2.U UI VERIFY (self-run, spec-driven):
1. Build `artifacts/targets/[ReportName]/build/ui_checklist.md`: one row per UI requirement found in TS §2/§4/§7 AND in `fs_markdown.md` — `| ID (UI-nn from TS, or new) | Requirement | Source (TS §x / FS section) | Proof: metadata / manual | Result | Evidence |`. Take every requirement the spec states (columns and their order, labels' exact wording, selection fields, mandatory filters, value help, default values, sort/group, text-for-code display, toolbar actions, facets/object page, hidden fields, currency/unit formatting, anything else the FS says). Examples in this step are not a scope limit.
2. FS ↔ TS disagreement (a column/filter/label/action in the FS that the TS lacks or states differently) is a TS defect: STOP and ask the user — never pick a side (`sap-dev-rule.md` §6).
3. `fetch.sh metadata <read-only server> <SRVB> <dir>` then `node .claude/scripts/odata-verify/ui-check.js <dir>/metadata_<server>.xml --ddlx <DDLX source file>` (read the DDLX source via ADT into that dir first — positions are not in `$metadata`, duplicates are only visible in source).
4. Judge each checklist row against that output → PASS/FAIL with the quoted line as evidence. Rows metadata cannot prove (actual rendering, F4 returning rows, column width/freeze, number/date display format, anything visual) → `Proof: manual`, carried to 2.M, never PASS here.
5. Reverse check: anything on screen in the metadata (column, selection field, action, facet) with no checklist row is **extra vs spec** → FAIL.
6. `ui-check.js` WARNINGS are hints to look at, not verdicts — each must map to a checklist row or be explained.

2.M MANUAL REMAINDER (user). Send the user one short checklist of exactly the `Proof: manual` rows from 2.0b/2.U (typically: open each value help and confirm it lists rows, visual/layout errors, formatting) and ask for screenshots or pasted values; read screenshots with the Read tool and judge each row against the spec. If TS §8 lists forms: the user previews/uploads each template and renders it once with real data (PDF: Adobe Designer preview with the `_data.xml`, then the system print action; Excel: upload + export) — ask for the rendered file or a screenshot and judge it against the FS form sample.

2.1 Evidence floor (`sap-dev-rule.md` §11): a bare "looks fine" is not a PASS. If the user's reply has no concrete data, ask again for the actual field values/payload/screenshot before recording a result. Log each attempt (2.0b, 2.U, 2.M together = one attempt) in the Scratchpad ledger's Verify Attempts table, citing the saved output file.

2.2 Compare actual against the spec row by row — data (2.0b), UI checklist (2.U), manual rows (2.M), especially the "Complex Logic" entries from TS §5. Every attempt, whatever its outcome, is recorded per 2.3 before anything else. All PASS → Phase 2.5. MISMATCH → root-cause it (trace the actual-vs-expected diff to the specific object/field responsible — do not guess), fix, redeploy the affected object(s), then re-run the affected 2.0b/2.U checks yourself (and the affected 2.M rows with the user). After 3 mismatch iterations, STOP — write up the concrete unresolved discrepancy and ask the user rather than attempting a 4th blind fix (`sap-dev-rule.md` §7). If the user insists on accepting an unverified result, record it as "PASS — unverified, user-accepted", never as a plain PASS.

2.3 TEST LOG IN THE HANDBOOK RECORD (mandatory, every attempt). Record **every** test case of this attempt — each data case (2.0b), each UI checklist row (2.U), each manual row/scenario (2.M) — as one `tests` block of the current version in `artifacts/targets/[ReportName]/handbook.json` (schema `.claude/common/handbook-target.md`), then run `python .claude/scripts/handbook/render_target.py [ReportName]`. Newest block first; never delete or rewrite an older block — the history of FAIL → fix → PASS is the point.
- Block: `title` = `Lần <Attempt #> — <YYYY-MM-DD>`, `summary` = what changed since the previous attempt (the fix, or "lần đầu").
- One case per row, none omitted and none summarised as "các case còn lại OK": `id` = `TC-nn` (data), the checklist's `UI-nn` (UI), `M-nn` (manual); `group` = Data / UI / Manual; `input` = the exact OData query options or the user action; `expected` = the count/outcome written before running; `actual` = the observed count/outcome; `result` = PASS / FAIL / WAIT (chờ user) / ACCEPTED ("PASS — unverified, user-accepted"); `evidence` = the saved file under `build/odata_verify/` or the screenshot under `test/`.
- **No business data values** — counts, field names and yes/no outcomes only; for a manual case summarise what the user showed (e.g. "F4 liệt kê 12 dòng") (`.claude/exceptions/`).
- Set `status` (e.g. "đang test lần 2", "test PASS"). The ledger's Verify Attempts row cites the handbook page instead of repeating the cases.

## Phase 2.5 — Independent Final Review (max 3 rounds)

2.5.0 Save `artifacts/targets/[ReportName]/build/final_source.md`: the current active source of every object in the ledger, read back from the system (not from chat memory), one section per object.

2.5.1 Dispatch [Agent: reviewer-lead] with inputs = the TS path, the ledger path, and `final_source.md`; output = `artifacts/targets/[ReportName]/build/review_verdict.md`. Read the verdict file from disk before acting on it (`sap-dev-rule.md` §12).

2.5.2 Act on the verdict:
- **APPROVE** → Phase 3.
- **CHANGES_REQUIRED** → fix each finding within TS scope (every change goes through Push → Activate → [Skill: activation-guard]; if a fix changes runtime behavior, re-run the affected Phase 2 check), refresh `final_source.md`, re-dispatch. After 3 rounds still not APPROVE, STOP and ask the user (`sap-dev-rule.md` §7).
- **BLOCK** → STOP. Show the user the blocking findings and ask how to proceed; never override a BLOCK yourself.

A finding the user explicitly accepts in writing is recorded in the ledger as "accepted by user" and listed in the walkthrough.

## Phase 3 — Walkthrough & Risk Report

3.0 Save `artifacts/targets/[ReportName]/walkthrough.md`: what was built (object list from the ledger, all DONE), what was verified and how — split into self-verified (2.0b data assertions and 2.U checklist rows, citing the saved `odata_verify/` output files) and user-verified (2.M rows, citing screenshots/pasted values), never "should work" — and link the `#kiem-thu` section of the handbook page (2.3, rendered from `handbook.json`) as the full case-by-case record, the Phase 2.5 review verdict with any user-accepted findings, and any known risks/manual steps outstanding (e.g. "Metadata Extension pending manual creation in ADT"). If a UI Service Binding (Step 7) was created, optionally use [Skill: sap-fiori-apps-reference] to generate the Fiori Launchpad URL from its Semantic Object/Action and include it in the walkthrough. List every form from TS §8 with its files, build/check result and upload/render status.

3.1 VERSION RECORD (mandatory): in `artifacts/targets/[ReportName]/handbook.json` open version `1.0` (a rebuild of an existing target: next minor version) with today's `date`, `source` = "create-report" and `changes` = what was built/changed; run ATC on **every object of the target** (not only the diff — `SAP(action="test", params={"type":"atc","object_url":…})` per object, as in [Skill: activation-guard] Gate 4) and record `atc` = date, variant, scope, result and every finding with its handling (fixed / accepted by user / open); make sure `objects` lists every ledger object with its `uses`, `forms` lists every TS §8 form with its files and render status, and `purpose` comes from TS §1. Then run `python .claude/scripts/handbook/render_target.py [ReportName]` and link the page from the walkthrough.

[OUTPUT FORMAT]
For each Phase-1 step, report in the chat using [Skill: caveman] style for the narration only (short, evidence-based, no filler) — the source code and log content below stay verbatim, never compressed (`sap-dev-rule.md` §10):
- The Object Name & Applied Skill (e.g., `ZC_MY_REPORT` — [Skill: cds-view-entities]).
- The exact validated ABAP/CDS source code (markdown, verbatim).
- SYSTEM EXECUTION RESULT: Validation Log (abaplint/Clean ABAP), Activation Status (Activated/Failed/Activated with Warnings), Auto-Correction Log if any, [Skill: activation-guard] gate results (Gate 1/2/3 pass, or the exact ripple/regression found) — verbatim.
