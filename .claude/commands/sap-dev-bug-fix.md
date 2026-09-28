---
description: Sử dụng workflow này khi cần chẩn đoán và sửa lỗi (bug) trên object SAP hiện có, dựa trên mock data do user cung cấp, đảm bảo phân tích root cause và đánh giá rủi ro trước khi sửa.
argument-hint: <object-name> <observed-vs-expected-behavior>
---

> **Claude Code note:** `[Skill: X]`/"Load `X`" below means invoke the `x` skill via the Skill tool (auto-discovered from `.claude/skills/x/`).

# Workflow: Bug Fix & Troubleshooting
**Trigger Command:** `/sap-dev-bug-fix`

## Context & Core Constraints
- **Business data — read-only, client 100 only:** the write client (080, `sap_cloud_dev`) has no data-read authorization — SQL returns 0 rows silently, so an empty result there is never evidence. The read-only client (100, `sap_gm2_cus_ro`) CAN read business data: use it to **reproduce the bug on real data** before and after the fix — via the object's OData service with `bash .claude/scripts/odata-verify/fetch.sh sample sap_gm2_cus_ro <SRVB> <EntitySet> '<query>'` (HTTP GET, prints counts and fill ratios only, never values), or a read-only SQL query on the source CDS view through `sap_gm2_cus_ro` (subject to `.claude/exceptions/` and the data blocklist hook). Run `fetch.sh samecode <TYPE> <NAME>` first when the fixed code must be visible on 100 — if it reports DIFFERENT, the post-fix reproduction cannot run there yet; say so. **Mock Data / Sample Data** from the User stays the input for ABAP Unit tests (Phase 4), which remain mandatory: real-data reproduction proves the bug and the fix on today's data, unit tests keep it from regressing.
- **Cross-Impact Analysis (Mandatory):** Any logic/condition change must be evaluated for regression risks affecting other objects or business flows that reuse this component. If a risk is detected, the Agent **MUST report and request User approval** before making any code changes.
- **Governing Rules:** Operates under the Iron Laws, Red Flags, and Token Efficiency rules in `sap-dev-rule.md` (§6-10) — in particular, a root-caused fix is not a verified fix until Phase 4's unit test evidence exists, and it is not a *safe* fix until `[Skill: activation-guard]` confirms the edited object activated clean AND nothing that depends on it broke as a side effect; progress updates use `[Skill: caveman]`.

Arguments: $ARGUMENTS

---

## Skill Execution Sequence (Routing)

**Target refresh (mandatory when `artifacts/targets/<TARGET>/` already exists):** [Skill: target-refresh] Part A before Phase 1 (once the target is known) — a change made outside this workspace since the last recorded version becomes its own version, with its real content, before this run opens a new one; Part B (full preview with evidence per item) after the last phase.

### Phase 1: Context Initialization & Mock Data Gathering
1. **Load `grill-me` & `scratchpad`**:
   - Initialize `scratchpad` to document the entire troubleshooting process.
   - Actively interview the User to gather 2 critical pieces of information:
     - (1) The name of the failing Object (CDS View, RAP BO, Class) or App.
     - (2) **Mock Data**: The incorrect input/output behavior observed by the User (e.g., "When passing SO Type = ZOR2, expected Output = 10 but got 0").

### Phase 2: Root Cause Analysis (RCA) & Impact Analysis
2. **Load `fs-data-model-extractor` (Trace mode) & `fs-logic-behavior-translator`**:
   - Starting from the reported Object, trace down the source code from the UI/Consumption layer to the Base/Database layer.
   - Pinpoint the exact line of code, JOIN condition, or logic block (e.g., CASE/WHEN) causing the issue by running a dry-run analysis with the provided Mock Data.
   - Where the object is readable on client 100, also reproduce the bug on real data (see Context: count assertions via `fetch.sh`, or a read-only SQL query) and save the output under `artifacts/targets/[ObjectName]/build/repro/` — this is the *trước sửa* evidence of the `R-nn` rows in step 7; re-run the same query after the fix for the *sau sửa* row.
3. **Execute Impact Analysis**:
   - Check where else this View/Logic is being used. Evaluate if changing this logic poses a risk to other dependent Apps or reports.

### Phase 3: Solution Proposal & Risk Reporting (Halt for Approval)
- **Action:** The Agent MUST NOT modify the code immediately. It MUST present to the User:
  - (1) The root cause of the bug.
  - (2) A draft of the proposed code fix (snippet).
  - (3) A **Cross-Impact Report** detailing any potential risks.
- **HALT and wait for the User's explicit approval** of the proposed solution.

### Phase 4: Fix Implementation & Quality Assurance
4. **Load `cds-view-entities`, `cds-analytical-views`, `rap`, `modern-abap-syntax`, `oo-design-patterns` & `abap`**:
   - Implement the code changes based on the approved solution. Ensure the code uses modern ABAP syntax and strictly follows Clean ABAP principles (checked via `abap`). Apply an OO design pattern only if refactoring complex logic genuinely warrants one.
   - If the approved fix's root cause requires extending SAP standard behavior rather than editing a Z/Y object directly, also load `[Skill: badi-enhancement]` to find/implement the appropriate released BAdI instead of any other extension mechanism.
5. **Load `abap-unit-testing`**:
   - Create or update the Local Test Class (`cl_abap_unit_assert`) using Test Doubles and the Mock Data provided by the User — one test method per case of the minimum matrix in step 7 (reproduction + dương/âm/biên per rule the fix touches).
   - **Note:** Creating an ABAP Unit Test using Mock Data is mandatory to compensate for the lack of real data in DEV and to prevent future regressions.
6. **Boundary, Activation & Ripple Check — `[Skill: activation-guard]`**:
   - Ensure NO Standard Objects were modified (Z/Y custom only).
   - Deploy and activate the edited object(s) yourself using your system-execution tool — do not just hand the user a to-do list. Run all 4 `[Skill: activation-guard]` gates: full activation log (no unresolved Error, every Warning explicitly assessed against strict(2)/Clean Core, never dismissed just because activation returned "success"), confirmed active state (not sitting inactive server-side), the ripple/cross-impact check against every consumer identified in the Phase 3 Cross-Impact Report — the gate that matters most for a fix touching an object other things already depend on — and zero NEW ATC findings introduced by the fix (diff-scoped, any priority). Re-verify each of those consumers is still active with no new error, not just the object you directly edited.
   - Only after all 4 gates pass on the edited object AND every impacted consumer, report the final object list with confirmed Activation Status per object (never "should be fine, please activate").
7. **Version + test record in the handbook (mandatory, every run)** — `artifacts/targets/<TARGET>/handbook.json` (schema `.claude/common/handbook-target.md`), `<TARGET>` = the report/app the fixed object belongs to (per its `INDEX.md`; the object name itself if it belongs to none — then create the folder, `INDEX.md` and `handbook.json` first):
   - First run of this fix: open a **new version** (next minor, e.g. 1.0 → 1.1) with today's `date`, `source` = "bug-fix", `changes` = the bug in one line + root cause + the fix applied. Later runs of the same fix add test blocks to that version.
   - Per run add one `tests` block on top (never delete or rewrite an older block): `title` = `Bug-fix lần <n> — <YYYY-MM-DD>`, `summary` = root cause + fix, or what changed since the previous run. One case per row, none omitted:
     - `R-nn` **Tái hiện** — the user's reported mock case: one row *trước sửa* (actual = the wrong behaviour observed, result = bug reproduced — by the real-data reproduction on client 100 when available, else by the Phase 2 dry-run) and one row *sau sửa* (the same real-data query re-run after the fix when available, plus the unit test asserting the expected value);
     - `UT-nn` **Unit test** — one per ABAP Unit test method, with the minimum matrix of the build workflows' Phase 2.0b for every rule the fix touches: *dương*, *âm*, *biên*;
     - `REG-nn` **Hồi quy** — one per consumer in the Phase 3 Cross-Impact Report: [Skill: activation-guard] Gate 3 result, plus that consumer's existing unit tests if any.
   - `source` = the user's report / TS section / Cross-Impact line; `input` = synthetic mock values only (field names and codes, never amounts or partner data — `.claude/exceptions/`); `result` = PASS / FAIL / ACCEPTED; `evidence` = the ABAP Unit output under `artifacts/targets/<TARGET>/build/unit_test/` or the activation-guard log.
   - When the fix is done: run ATC on **every object of the target** (not only the edited one) and record `atc` on the version (date, variant, scope, result, each finding + handling); update `objects` if the fix added/removed one; set `status`.
   - Run `python .claude/scripts/handbook/render_target.py <TARGET>`. A FAIL means the fix is not done: fix, re-run, and log a new block.

## Output Format

Report chat progress in `[Skill: caveman]` style (short, evidence-based) — narration only. Save a Fix Report to `artifacts/targets/[ObjectName]/walkthrough_bugfix.md` in full detail, NOT caveman-compressed (`sap-dev-rule.md` §10): the root cause, the approved fix applied, the ABAP Unit Test evidence (not "should work"), the Cross-Impact Report, the `[Skill: activation-guard]` gate results for the edited object and every re-checked consumer, and the exact list of objects with their confirmed Activation Status, and a link to the `#kiem-thu` block of the handbook page (step 7) as the full case-by-case record.
