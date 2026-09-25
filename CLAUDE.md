# ABAP Cloud AI — Claude Code Workspace

Pair-programming workspace for **SAP S/4HANA Cloud Public Edition** (ABAP Cloud, Clean Core) with Claude Code. Two DEV tenants: client 080 (write) and client 100 (read / test / debug only) — see `.claude/common/system-config.md`.

@.claude/rules/sap-dev-rule.md
@.claude/common/system-config.md

## How this workspace works

- **Skills** (`.claude/skills/<name>/SKILL.md`, 56 of them) auto-activate when their description matches the request — no manual routing. Grouped catalog in `README.md`; heavy templates live in each skill's `references/`, loaded only when writing that object. 18 of them are `sap-process-*` — SAP Public Cloud business-process/functional-consulting knowledge (O2C, Supply Chain, Manufacturing, Production, Finance, Project System) for `consultant-lead` to draw on during FS analysis; each has a lean always-loaded `SKILL.md` + an on-demand `references/deep-dive.md` for deeper business-logic depth (partner determination, pricing, planning strategy, etc.), read only when the FS genuinely needs it.
- **Subagents** (`.claude/agents/<team>-<layer>.md`, 7 of them) — Team Consultant/Dev/Tester × Lead (opus, judgment-heavy)/Executor (sonnet, template-driven), plus `reviewer-lead` (opus, read-only final verdict in Phase 2.5 of the create-* workflows) — dispatched by workflows via `[Agent: y]` for isolated analysis/drafting. The Manager (this session) alone holds SAP CUD authority; subagents only draft to `artifacts/targets/<TARGET>/build/` and never mark a ledger row DONE.
- **Workflows** are slash commands in `.claude/commands/`. Pick by scenario:

| Scenario | Analyze (FS → TS) | Build (TS → system) |
|---|---|---|
| Report/screen over EXISTING released CDS data | `/sap-dev-fs-analytic` | `/sap-dev-create-report` |
| Brand-new transactional app (no Z-table/CDS yet) | `/sap-dev-fs-analytic-transactional-app` | `/sap-dev-create-transactional-app` |
| Bug on an existing object (mock-data based) | — | `/sap-dev-bug-fix` |
| Inbound / outbound API on Z_API_FWK | — | `/sap-dev-api-inbound` · `/sap-dev-api-outbound` |
| Document / review existing code (read-only) | `/sap-dev-code-analysis` · `/sap-dev-code-review` | — |

- **Reference layer** (sc4sap-style, rule §15): `.claude/common/` (system config, context-loading protocol, cloud ABAP constraints), `.claude/configs/<MODULE>/` (Public Cloud module knowledge — 11 modules: SD, FI, CO, MM, PP, QM, PM, PS, TM, EWM, TR), `.claude/exceptions/` (data-extraction blocklist, profile `standard`). Loaded by tier, never all at once. `bash .claude/scripts/integrity-check.sh` after any `.claude/` change.
- **Outputs** always go under `artifacts/` (rule §4, hook-enforced) — never `.claude/` or the workspace root. Each report/function has ONE folder `artifacts/targets/<TARGET>/` (fs, ts, build, forms, ddlx, test, notes, walkthrough) plus `handbook.json`, rendered to its handbook page by `.claude/scripts/handbook/render_target.py` (`.claude/common/handbook-target.md`).
- **`.claude/` is locked** (rule §14, hook-enforced): to modify rules/skills/hooks on the user's request, the USER must first create `.claude/.unlock` (the agent must never create that file) — remind them, and remind them to delete it afterwards.
- **Naming defaults** follow [Skill: naming-convention], sourced from the project sheet `artifacts/documents/naming_convention/` (CDS/RAP as `Z<prefix>_<module>_<tcode>`, e.g. `ZR_SD_ZSD01` / `ZBP_R_SD_ZSD01`; service `ZUI_`/`ZAPI_` + `_O2`/`_O4`; communication, IAM, application job, launchpad `_UI5R`, form; tables `ZA_`/`ZD_`; packages `ZFPT_*`). Explicit TS/user names always win.

## MCP servers in use

- `sap_cloud_dev` — `tools/vsp/vsp.exe`, client 080 (write), cookie `tools/vsp/cookies_dev.txt`. Matches the PreToolUse matcher `mcp__sap_[a-z0-9]+_dev__.*` (pre-cud-guard).
- `sap_gm2_cus_ro` — `tools/vsp/vsp.exe`, client 100 (read / test / debug only — `tier-readonly-guard.sh` denies create/edit/delete).
- `sap-docs-upstream` — SAP documentation search + API release state (`sap_search_objects`, `sap_get_object_details`) — the lookup for released CDS / classes / BDEFs.
- Released CDS views by module: the local catalog `artifacts/system_analysis/CDS_RELEASED_CATALOG/` (the old `cds-kb` MCP endpoint is dead).

`.mcp.json`, `vsp.exe` and cookie files are local only (not committed). Cookie refresh and setup: `README.md` → "Bắt đầu".
