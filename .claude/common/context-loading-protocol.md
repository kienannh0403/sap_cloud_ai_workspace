# Context Loading Protocol — 4 tiers, on demand

How the Manager and subagents decide which rule/reference files to read. Adapted from sc4sap
`common/context-loading-protocol.md` (MIT, v0.6.18) to this workspace's layout. Goal: the safety rails are
always in context, everything else is read only when the task needs it.

## Tier 1 — always loaded (every session, every agent)

| File | How it gets loaded | Why |
|---|---|---|
| `.claude/rules/sap-dev-rule.md` | `@`-import in `CLAUDE.md` | §1–§15: scope, safety, iron laws. Section numbers are stable — 60 files cite them |
| `.claude/common/system-config.md` | `@`-import in `CLAUDE.md` | Version, module, country, tier, blocklist profile, write vs read-only server |

Subagents do not see `CLAUDE.md` imports automatically: their agent file tells them to read both files first
(see Tier 2).

## Tier 2 — per agent role (read at dispatch, before any work)

| Role | Agents | Extra files |
|---|---|---|
| Consultant | `consultant-lead`, `consultant-executor` | `configs/<MODULE>/README.md` for each module **the FS touches** (must be in `SAP_ACTIVE_MODULES`); then only the `configs/<MODULE>/*.md` file(s) the FS topic needs |
| Dev | `dev-lead`, `dev-executor` | `common/cloud-abap-constraints.md` |
| Tester | `tester-lead`, `tester-executor` | `common/cloud-abap-constraints.md` |
| Manager (main session) | — | Tier 1 only; Tier 3 by trigger |

## Tier 3 — triggered reads

| Trigger | Read |
|---|---|
| Writing, reviewing or designing ABAP / CDS / BDEF | `common/cloud-abap-constraints.md` |
| Any business-data read (`SAP(action="query")`, data preview, curl `datapreview/freestyle`) | `exceptions/README.md` (hook `block-forbidden-tables.sh` enforces it anyway) |
| FS / TS / functional question in an active module | `configs/<MODULE>/README.md`, then the one topic file needed |
| Picking a released CDS view | `artifacts/system_analysis/CDS_RELEASED_CATALOG/INDEX.md` (memory `cds-released-catalog`) |
| Resuming work on a target | `artifacts/targets/<TARGET>/INDEX.md`, then only the `notes/*.md` it links that the task needs (rule §4) |
| Country-specific requirement: tax, invoice, statutory accounting, fixed assets, amount/currency or date format (`SAP_COUNTRY=vn`) | `country/vn.md` — its `to verify` regulation rows are questions for the customer, not facts |

## Tier 4 — per-task kit

Declared by the workflow or skill at the step that needs it: a skill's `references/*.md`, the TS section named
in an `[Agent: y]` dispatch, the ledger row being worked. Never preloaded.

## Discipline

1. Do not preload `configs/`, `exceptions/` or skill `references/` "just in case" — that defeats the tiers.
2. A subagent that needs a file outside Tier 1–4 may read ONE more and must say so in its return message; needing
   more than that means the dispatch was under-specified → return `BLOCKED — context kit insufficient: <files>`.
3. Workflows declare Tier 4 only; they do not restate Tier 1/2.
4. Adding a module: create `configs/<MODULE>/README.md` (plus `released-objects.md` when the module has enough
   released objects to need one), then add it to `SAP_ACTIVE_MODULES`. Never the other way round — the integrity
   check fails on an active module without a README.
5. A consultant reads only the README of the module(s) the FS touches, not all 11.
