---
name: activation-guard
description: After creating, editing, or deleting any SAP object (CDS view, DDIC object, BDEF, class, service definition/binding), verify it is genuinely active with zero unresolved errors/warnings, that no other object depending on it broke as a side effect, AND that the code you just changed introduces zero new ATC findings (any priority). Use immediately after every "Push → Activate" (or delete) step in any workflow that mutates SAP system objects, before marking that step DONE in a build ledger — this is what stops a chain reaction of activation failures propagating through Steps N+1, N+2... and what keeps a TR move from failing a Clean Core check later.
---

# Activation Guard

## Why this exists

"Activated" is not "correct," and "correct in isolation" is not "correct in context." Two failure modes cause cascades across a sequential RAP/API build:

1. An object activates with a **warning that actually matters** (silently treated as "unavoidable" without real assessment), or the tool reports success while the object is still inconsistent server-side.
2. An object built **earlier** in the same ledger gets modified later (e.g. going back to fix Step 1's Interface View after Step 3's Behavior Definition already built on top of it) — and nobody re-checks whether that earlier, already-DONE object is still valid.

Either one produces exactly the symptom this skill exists to catch: object N looks fine, but N+1 or N-1 quietly breaks.

## When to run

Immediately after every DEPLOY & ACTIVATE (or DELETE) of any SAP object, in any workflow — `/sap-dev-create-report`, `/sap-dev-create-transactional-app`, `/sap-dev-api-inbound`, `/sap-dev-api-outbound`, `/sap-dev-bug-fix`, or any ad-hoc object change — before that workflow marks the corresponding ledger row DONE and moves on.

> Tool note: examples below use `mcp__sap_cloud_dev__SAP` (the write server, `WRITE_SERVERS` in `.claude/common/system-config.md`) as the connected ADT/system-execution tool. If a different MCP server is connected, use `ToolSearch` to find its equivalent action (`sap-dev-rule.md` §9) — the 4 gates below are the requirement, not the specific tool call syntax.

## Protocol — 4 gates, all must pass before DONE

Token-lean I/O for the edit and the gates (short unique `EDITSOURCE` anchors + whole-source diff afterwards,
reading by method/grep, condensed check output): `.claude/common/lean-sap-io.md`.

### Gate 1 — Full Activation Log Capture (never trust a boolean)

- Capture the COMPLETE activation result — every message, not just top-line pass/fail.
  `SAP(action="edit", target="ACTIVATE", params={"object_url": "...", "object_name": "..."})`
- Classify every message:
  - **Error** → hard stop. Fix and retry Gate 1 before moving to Gate 2.
  - **Warning** → do NOT default to "unavoidable." Assess it against strict(2)/Clean Core (`sap-dev-rule.md`). Only accept it as unavoidable if fixing it is genuinely impossible or out of the TS/FS's scope — and say so explicitly, quoting the exact warning text. A warning dismissed without that assessment is an unverified claim per `sap-dev-rule.md` §8/§11.
- If any doubt remains about whether an error was fully cleared, re-run an explicit syntax check rather than re-trusting the activate response:
  `SAP(action="analyze", params={"type": "syntax_check", "object_url": "...", "content": "..."})`

### Gate 2 — Confirmed Active State (don't trust the tool's return message alone)

- A tool can report "success" while the object is still flagged inactive/revised server-side (e.g. a downstream inconsistency). Independently confirm — token-lean, prints only the watched names:
  `python .claude/scripts/atc/atc_check.py inactive --names <OBJ1>,<OBJ2>,<PREFIX>*`
  (exit 0 none inactive · 1 a watched object is inactive · 2 session/SAP error → refresh the cookie, or fall back to
  `SAP(action="analyze", params={"type": "inactive_objects"})`, which lists every inactive object of every user).
- The object you just touched must NOT appear in that list. If it does, treat it exactly like a Gate 1 error — diagnose the real message behind it, fix, re-activate, re-run both gates.

### Gate 3 — Ripple / Cross-Impact Check (the gate most builds skip entirely)

This is what actually prevents "N+1 breaks because N changed."

- Get the list of objects that DEPEND ON (are downstream of / reference) the object you just touched — not what it depends on:
  - CDS view: `SAP(action="analyze", params={"type": "cds_impact", "cds_view": "<name>"})` or `SAP(action="read", target="CDS_DEPS <name>")`
  - Class/program: `SAP(action="analyze", params={"type": "callers", "object_uri": "..."})`
  - Broader multi-hop impact: `SAP(action="analyze", params={"type": "impact", "object_type": "...", "object_name": "...", "max_depth": 3})`
- **This matters most when the object you just touched is a fix/edit to something already built EARLIER in this same ledger.** Cross-check every dependent that is ALSO already in this ledger's scope: is it still active with no new error? Re-run Gate 1 + Gate 2 on each one that's downstream and already marked DONE.
- If a previously-DONE ledger row now fails because of this change, do not silently re-fix it and move on — mark it `REGRESSED` in the ledger first (see [Skill: scratchpad] Ledger Format), noting which step caused it, THEN fix it in dependency order, then flip it back to `DONE` only once it re-passes all 4 gates.
- If the connected tool has no impact/where-used capability for this object type, do not silently skip this gate — record in the ledger: "Ripple check unavailable for this object type via the connected tool; dependents not automatically re-verified" so the gap is visible, not hidden.

### Gate 4 — ATC Check, zero NEW findings (added 2026-09-23, user standing rule)

**Why:** ATC (ABAP Test Cockpit) is a different check from Gate 1's syntax/activation messages — it covers Clean
Core / cloud-readiness / code-quality rules that don't block activation but DO block a TR release later. Running
it now, object by object, means a TR move never has to stop and re-check — that's the whole point (user,
2026-09-23): *"bắt buộc phải ATC check, sửa tất cả các lỗi ATC... để khi move TR không cần phải check lại."*
Applies to **every package**, local or transportable — not just objects headed for a TR.

- **Run with the script (default, user 2026-10-06 — same ATC run on SAP, condensed output):**
  1. BEFORE the edit (existing object): `python .claude/scripts/atc/atc_check.py baseline --target <T> --label <l> --uri <adt uri>`
  2. AFTER the edit: `python .claude/scripts/atc/atc_check.py run --target <T> --label <l> --uri <adt uri>`
     (new object: `run … --new`, baseline = empty → every finding is new). `--uri` may repeat; a package uri checks
     the whole package tree.
  It runs the system check variant (`ABAP_CLOUD_DEVELOPMENT_DEFAULT` on this tenant) through the ADT API with the
  `.mcp.json` cookie, saves every finding to `artifacts/targets/<T>/build/atc/<stamp>_<label>_<baseline|run>.json`
  (the evidence — cite that path in the ledger), and prints one line per object plus full details of NEW findings
  only. Exit 0 = no new finding · 1 = NEW findings (gate fails) · 2 = SAP/session error (never a pass: refresh the
  cookie or fall back) · 3 = usage (e.g. no baseline). Validated 2026-10-06 against the MCP ATC of package ZMA01:
  67 findings, identical per object.
- Fallback when the script exits 2: `SAP(action="test", params={"type": "atc", "object_url": "<uri>"})` (full JSON
  into the conversation — expensive), then compare by hand the same way.
- **Scope = what this step introduced, not the whole object** (user-approved 2026-09-23): pre-existing findings do
  not block — the object may carry legacy findings, and this gate is not a mandate to clean unrelated old code.
  - "New" is decided by signature, not by line number: object + check + message id + message text, counted as a
    multiset. A legacy finding that only moved because lines were inserted stays "kept" (comparing raw line numbers
    would call every shifted finding new); one more occurrence of an existing signature IS new. A message whose
    text embeds a line/variable name may look new after an edit — the script then prints it in full, check it.
  - Kept findings: note the count in the ledger evidence (e.g. "21 = baseline, NEW 0"), do not fix them as part of
    this step, do not let them block DONE.
  - NEW findings: **all three priorities (1 error / 2 warning / 3 info) must be fixed to 0** before this gate
    passes — same standard as Gate 1's "no unassessed warning," now applied to ATC.
- If a genuinely new finding cannot be fixed (architectural constraint, ATC rule doesn't apply to this pattern,
  etc.), do not silently accept it: stop and ask the user, and only record `PASS — unverified, user-accepted`
  (rule §11) with the user's explicit written acceptance — never a plain PASS with an unresolved new finding.
- New object (nothing pre-existing) → `run … --new`: the baseline is empty, so Gate 4 IS "zero findings, whole
  object" for that object, which is the correct outcome for brand-new code.

## Ledger integration

Only mark a ledger row `DONE` after all 4 gates pass. A regression found by Gate 3 goes to `REGRESSED`, not a fresh generic `FAILED` — the distinct status is what makes the cascade visible to a human skimming the ledger later, instead of looking like an unrelated new failure. A Gate 4 finding that can't be fixed follows rule §11 (`PASS — unverified, user-accepted`), never a silent pass.

## What this replaces

Any workflow step that previously said just "Execute: Lint → Push → Activate" now reads "Execute: Lint → Push → Activate → [Skill: activation-guard]." A bare "Activated" claim without having run all 4 gates is not sufficient completion evidence.
