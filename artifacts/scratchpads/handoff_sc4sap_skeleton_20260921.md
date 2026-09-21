# Handoff — Build Public Cloud workspace from sc4sap skeleton (2026-09-21)

## Current Status (verified facts only)
- Task: build a new SAP Public Cloud workspace **modelled on the skeleton** of https://github.com/babamba2/superclaude-for-sap (sc4sap). NOT installing the plugin, NOT connecting to it — skeleton is a template only (user clarified).
- Repo shallow-cloned and read in the previous session (plugin.json version 0.6.18, MIT). Clone lived in that session's temp scratchpad — **it is gone for the new session; re-clone if needed** (`git clone --depth 1 https://github.com/babamba2/superclaude-for-sap.git`), preferably under `artifacts/` of the new workspace (hook blocks new files elsewhere).
- Nothing was installed, nothing in this workspace was modified except this handoff file.
- User decision (2026-09-21): **copy the current workspace out to a new folder and continue there.** Copy is done by the user.

## Skeleton findings (read from the repo, not inferred)
| sc4sap layer | Verdict for Public Cloud |
|---|---|
| `CLAUDE.md` = index only (rules.md is empty) | take the idea |
| `common/*.md` + `context-loading-protocol.md` = 4-tier on-demand loading (T1 global always, T2 per agent role, T3 triggered, T4 per-task kit) | **take** |
| `common/cloud-abap-constraints.md` (prohibited statements + API replacements when `SAP_VERSION=S4_CLOUD_PUBLIC`) | **take nearly verbatim** as a Tier-3 file |
| `agents/` (25) — Mandatory_Baseline + Role + read-only tool list + disallowedTools | take the template |
| `skills/` (14) — SKILL.md + per-phase files (e.g. create-program/phase4-parallel.md, spec-approval-gate.md) | take the template |
| `configs/{MODULE}/` = spro, tcodes, bapi, tables, enhancements, workflows (+ configs/common) | **rewrite** for Public Cloud: SSCUI / Fiori app ID / released API / released CDS `I_*` / key-user+developer extensibility+released BAdI / flexible workflow |
| `exceptions/` blocklist by category with tier tag minimal/standard/strict | take the template |
| `hooks/hooks.json` + `scripts/` (~15 hooks) | pick: forbidden-table block, transport check, tier read-only guard, activation verify, pre-compact/handoff, session-start |
| `industry/`, `country/` | only `country/vn.md` (+ chosen industry) |
| `tests/validation/` (name==dir, version match) | take the idea → script replacing manual §14 check |
| `abap/`, `bridge/`, `src/`, `runtime-deps/` (ZMCP_ADT_* objects, MCP server code) | **skip** — on-prem; Public Cloud cannot create free ICF/SICF nodes |
- Config really lives in `sap.env` (SAP_URL, SAP_CLIENT, SAP_AUTH_TYPE, SAP_TIER, SAP_VERSION, ABAP_RELEASE, SAP_ACTIVE_MODULES, SAP_INDUSTRY ...) + `config.json`. There are **no** `SC4SAP_*` env vars.
- Public Cloud connection auth values (`SAP_AUTH_TYPE`, `SAP_SYSTEM_TYPE`) are NOT documented in INSTALLATION.md — irrelevant now since we are not using their MCP.

## Risk assessment result (in-place vs separate)
Measured on the current workspace:
- No git repository → in-place edits have no rollback.
- 57 files under `.claude/skills|commands|agents` reference `§N` / `sap-dev-rule` → splitting `sap-dev-rule.md` in place breaks many references.
- `workspace-write-guard.sh` blocks new files outside `artifacts/` → the skeleton's root `common/`, `configs/`, `exceptions/` cannot be created in this workspace without fighting the hook.
- `settings.json` pins `autoMemoryDirectory` = `~/.claude/auto-memory/ABAP_CLOUD_AI` → a new folder shares OR loses memory depending on that key.
- Hooks need `jq` and relative paths (`./.claude/hooks/*.sh`); PreToolUse matcher `mcp__sap_[a-z0-9]+_dev__.*`.
- `.mcp.json` has 6 servers (cds-kb, sap-docs, sap-docs-upstream, sap_cloud_dev, sap_gm2_cus_ro); 2 have an `env` block — **contents NOT inspected for secrets**.
- Sizes: `artifacts/` 291 MB (11 targets: ZFPT_EINVOICE, ZGL02, ZGL04, ZMA01E, ZMA02, ZMFGKH01, ZMFGKH01_N, ZMFGLSX, ZPM01_EX, ZRM01, ZRM01_EX), `.venv_markitdown` 371 MB, `docs` 23 MB, `tools` 16 MB, `.claude` 12 MB.
- `.claude/.unlock` exists since 2026-09-09 16:47 (user-created) → the `.claude/` lock has been inactive for 10+ days.

## WIP
- Nothing in progress. Waiting for the user to copy the workspace and open a new Claude Code session in it.

## Next Steps (for the session in the NEW workspace)
1. Confirm the working directory is the new copy (not the old one) and that ASCII path is used.
2. **Copy only what is needed**: `.claude/`, `CLAUDE.md`, `README.md`, `.mcp.json.example`, empty `artifacts/` skeleton. Leave `artifacts/` (291 MB) and `.venv_markitdown` (371 MB) in the old workspace; reference old targets through their `artifacts/system_analysis/<TCODE>/INDEX.md`.
3. `git init` and commit immediately (baseline = rollback point).
4. Memory: pin a **separate** `autoMemoryDirectory` for the new workspace and copy over only the memory files still needed. Never put that key in user scope.
5. `.mcp.json`: inspect the 2 `env` blocks for secrets **before** copying; prefer `.mcp.json.example`. Re-test `sap_cloud_dev` (session-start standing check).
6. Re-verify hooks: `jq` present; matcher still fits the MCP server names; test that Z/Y-only, package, TR guards still deny.
7. Re-clone sc4sap into the new workspace under `artifacts/` (reference only) if the skeleton needs to be re-read.
8. Ask the user the 3 open questions (below) if not answered, then start build steps B1–B2: create skeleton dirs; split `sap-dev-rule.md` into tiered `common/` + `context-loading-protocol`, keeping every `§N` reference resolvable (or update the 57 referencing files in the same change).
9. Then: system config file (version/release/modules/industry/country/tier=DEV) → `cloud-abap-constraints` as Tier 3 → rewrite `configs/{MODULE}/` for Public Cloud from real sources (sap-docs-upstream; mark unverified items as such) → `exceptions/` blocklist → selected hooks → integrity script replacing manual §14 check → handbook + INDEX.md.
10. After any `.claude/` change: run the §14 integrity check. When finished, tell the user to delete `.claude/.unlock`.

## Tried & Failed
- WebFetch summaries of the repo were unreliable (skills 14 vs 19, agents 24 vs 25; invented `SC4SAP_*` env vars). Fixed by a real shallow clone — read the source, do not rely on summaries.
- `gh` CLI is not installed on this machine; use `git clone`.
- `du` on the whole workspace hung (OneDrive) in the foreground; run size checks per folder or in the background.
- MCP servers `cds-kb` and `sap-docs` returned 404 this session; `sap-docs-upstream` tools are available (deferred, load via ToolSearch).

## Critical Context
- Rules: chat in Vietnamese; code/identifiers/comments English; DEV only; Z/Y only; package mandatory; **never create/modify/delete a TR**; local packages `ZANLTK2`/`$TMP` need no TR; writes only in client 080 (client 100 = read/test/debug only, not hook-enforced).
- Agent must never create `.claude/.unlock`.
- Connection: `sap_cloud_dev` MCP (vsp, cookie SSO) — refresh via `vsp --browser-auth`; ACTIVATE `success:true` does not mean active → verify with `analyze inactive_objects` / `syntax_check`.
- No TR, package or SAP object is involved in this task so far.

## Open questions (asked, unanswered)
1. Module list for the first build (suggested: SD, MM, FI, PP, PS).
2. Industry / country (suggested: `vn` only).
3. Blocklist tier: minimal / standard / strict (sc4sap default recommendation: strict).
4. Location and name of the new workspace (user said they will copy it themselves).

## Ledger Pointer
No scratchpad ledger exists for this work yet. Create one when build steps start (`artifacts/scratchpads/<TARGET>/`).
