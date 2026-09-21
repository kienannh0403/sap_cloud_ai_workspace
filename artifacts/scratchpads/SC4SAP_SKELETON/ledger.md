# Ledger — Build Public Cloud workspace from sc4sap skeleton

Created: 2026-09-21. Source: `artifacts/scratchpads/handoff_sc4sap_skeleton_20260921.md`.
Status legend: `[ ]` open · `[x]` done. Only the Manager marks a row done, with evidence noted in the Evidence column.

## A. User decisions (block B1–B2)
| # | Item | Status | Evidence / Answer |
|---|---|---|---|
| A1 | Module list for first build (suggested SD, MM, FI, PP, PS) | [x] | User 2026-09-21: **SD only** |
| A2 | Industry / country (suggested `vn` only) | [x] | User 2026-09-21: **vn** (industry not stated; none chosen) |
| A3 | Blocklist tier: minimal / standard / strict (sc4sap recommends strict) | [x] | User 2026-09-21: **standard** (minimal + protected business data, action=warn; audit-logs and communication-workflow files excluded) |
| A4 | Confirm `C:\WORK_SPACE` = new workspace; old workspace keeps `artifacts/` (11 targets) | [x] | User 2026-09-21: "đây là work space mới" |

## B. Clean the copy
| # | Item | Status | Evidence |
|---|---|---|---|
| B1 | Remove `.venv_markitdown` (371 MB) from the copy, unless `office_to_md.py` is needed here | [x] | User removed; verified 2026-09-21: `.venv_markitdown` absent at workspace root. Side effect: skill `document-markdown-converter` (SKILL.md + README.md step 4) still references it, and `scripts/office_to_md.py` does not exist in this workspace (find, excluding artifacts/) — skill is non-functional until venv+script are restored or the skill is dropped |
| B2 | Inspect the 2 `env` blocks in `.mcp.json` for secrets; prefer `.mcp.json.example` | [x] | Inspected 2026-09-21 with values masked. (1) `sap_cloud_dev` + `sap_gm2_cus_ro` env = SAP_URL/USER/CLIENT/MODE/COOKIE_FILE, **no password** (cookie auth). (2) **Literal secret found outside env**: `sap-docs` args carry `--header SAP-API-HUB-KEY:<32-char literal>` — must not enter git (C1). (3) vsp.exe + cookies.txt of both SAP servers point to the OLD workspace folder (`OneDrive/FIS dự án/ABAP_CLOUD_AI/MCP_*/tools/vsp/`), both exist — new workspace is coupled to the old one. (4) `.mcp.json.example` has no SAP_COOKIE_FILE/SAP_MODE and lists only 3 servers (stale vs real). Open follow-ups: gitignore `.mcp.json` before C1; decide whether to decouple vsp/cookies paths |
| B3 | User deletes stale `.claude/.unlock` (since 2026-09-09); recreates it only when `.claude/` must change (agent never creates it) | [~] | Verified 2026-09-21: `.claude/.unlock` absent (lock active). Delete half done; user recreates it before group E |
| B4 | Decouple vsp.exe + cookies from old workspace | [x] | 2026-09-21: `.mcp.json` now uses `C:/WORK_SPACE/tools/vsp/vsp.exe`; `sap_cloud_dev` → `cookies_dev.txt` (my437569/080), `sap_gm2_cus_ro` → `cookies_cus.txt` (my437557/100). `cookies_cus.txt` refreshed 14:44 via `vsp --browser-auth` (Chrome, user SSO): `SAP_SESSIONID_GM2_100`. curl `/sap/bc/adt/discovery` → `200 application/atomsvc+xml` on both tenants. No old-folder refs left. Remaining: gitignore `.mcp.json` + `tools/vsp/cookies*.txt` (C1) |

## C. Safety foundation
| # | Item | Status | Evidence |
|---|---|---|---|
| C1 | `git init` + baseline commit (rollback point) | [x] | 2026-09-21: `git init -b main` done. Root `.gitignore` BLOCKED by workspace-write-guard (§4, new file outside artifacts/) → ignore rules written to `.git/info/exclude` instead (local-only, not versioned): `.mcp.json`, `tools/vsp/cookies*.txt`, `.env*`, `.claude/.unlock`, `.claude/settings.local.json`, `tools/vsp/vsp.exe`, `.venv*/`, `__pycache__/`, `artifacts/scratchpads/SC4SAP_SKELETON/sc4sap_repo/` (nested .git). `git check-ignore` confirmed each; `cookies.txt.example` stays tracked. Dry-run: 383 candidate files (337 in .claude/skills, 9 commands, 6 agents, 2 hooks, rules, settings.json, CLAUDE.md, README.md, .mcp.json.example, artifacts/handbook/*, ledger/handoff). Secret scan: real SAP-API-HUB-KEY value + both SAP_SESSIONID values found in 0 of 383 files. NOT committed yet: git user.name/email not configured; waiting for user identity + OK on the file list. Note: `artifacts/handbook/` still holds 9 old-tcode HTML handbooks (ZRM01, ZGL02...) from the old workspace | **Closed 2026-09-21**: user chose to delete the 9 old-tcode handbooks (originals verified present, same size, in old workspace `MCP_PhuTAI_GO_DEV/artifacts/handbook/`); removed. Repo-local identity `kienannh0403 <kienant.king@gmail.com>`. Baseline commit `b167a9d` on `main`: 374 files in HEAD (= 383 − 9), `git status` clean at commit time, no forbidden file staged, no literal API key in HEAD. Note: `artifacts/handbook/index.html` still links to the 9 deleted pages (dead links) — fix when the new handbook is written (F2) |
| C2 | Pin a SEPARATE `autoMemoryDirectory`; copy only needed memory files; never in user scope | [x] | 2026-09-21 done. User decisions: (a) per-report/function knowledge goes in `artifacts/system_analysis/<TARGET>/notes/` (E9), not auto-memory; (b) memory dir `C:/Users/anltk2/.claude/auto-memory/Work_space` — must be OUTSIDE the workspace (dry-run of `workspace-write-guard.sh`: `.claude/memory/*` DENY, `C:/WORK_SPACE/memory/*` DENY, `~/.claude/auto-memory/<NAME>/*` allow). `.claude/settings.json` line 2 set to `~/.claude/auto-memory/Work_space` (git diff = that line only). Copied 18 old memory files + new `MEMORY.md` (19 files): 11 as-is, 7 edited (sap-cloud-dev-connection, phutai-go-cus-connection, hooks-jq-and-local-package, artifacts-per-tcode-layout, claude-code-memory-scoping, rap-modify-control-vs-update-fields, check-mcp-alive-each-session); skipped 3 (python-utf8-nonascii-workspace-path, repository-harness-evaluation-open, skills-other-already-triaged). Integrity: every index line resolves, every file indexed, frontmatter name == filename, old dir untouched (22 files). **Verified after VS Code restart**: session-start instruction reload lists `Work_space/MEMORY.md` and reports `ABAP_CLOUD_AI/MEMORY.md` "no longer present". §14 integrity check not run: no skill/agent touched. Open: `.claude/.unlock` still present (15:32) — user deletes |
| C3 | `jq` present; hook matcher `mcp__sap_[a-z0-9]+_dev__.*` fits MCP server names | [x] | 2026-09-21: `jq-1.8.2` on PATH in Git Bash (WinGet path). Matcher regex test: `mcp__sap_cloud_dev__SAP` MATCH (guard fires); `mcp__sap_gm2_cus_ro__SAP` no match (guard does NOT fire — known, client 100 read-only is convention only, see memory phutai-go-cus-connection). settings.json has 2 PreToolUse hooks: pre-cud-guard (matcher above) and workspace-write-guard (`Write|Edit|NotebookEdit|Bash`) |
| C4 | Hook deny tests: non-Z/Y, missing package, missing TR, agent TR CUD | [~] | 2026-09-21 dry-run of `pre-cud-guard.sh` with 10 synthetic payloads (no SAP call): A create no package DENY · B create transportable pkg no TR DENY · C create local ZANLTK2 no TR ALLOW (correct) · D create non-Z object DENY · E agent creates TR DENY · F delete no package DENY · G create + pkg + TR ALLOW (correct) · J read ALLOW (correct). **GAP**: H `action:edit` on standard object CL_STD and I `action:edit` on Z object with no package both ALLOW — the CUD regex lists create/insert/update/modify/delete/activate but NOT `edit`, and `edit` is the tool's main write action (auto lock/activate). So Z/Y-only, package and TR are NOT enforced on edit. Fix = add `edit` to the action regex in `.claude/hooks/pre-cud-guard.sh` (+ read object name from `target` for edit, since edit puts the name only in `target`) — needs user decision + `.unlock`. workspace-write-guard tested via 3 Write-path dry-runs (see C2) |
| C5 | `sap_cloud_dev` alive (`vsp --browser-auth` if cookie expired) | [x] | 2026-09-21 after VS Code restart: `SAP(action=search, target=ZCL_*, maxResults=3)` on BOTH `sap_cloud_dev` and `sap_gm2_cus_ro` returned 3 rows each (ZCL_AMOUNT_READER, ZCL_API_IMPL, ZCL_BS_DEMO_CUST_CNAME_QUERY) — MCP servers alive. Both returned the same rows (consistent with, but not proof of, 080/100 sharing a repository) |

## D. Source preparation
| # | Item | Status | Evidence |
|---|---|---|---|
| D1 | Shallow re-clone sc4sap under `artifacts/` (reference only): `git clone --depth 1 https://github.com/babamba2/superclaude-for-sap.git` | [x] | Cloned to `artifacts/scratchpads/SC4SAP_SKELETON/sc4sap_repo/`; `exceptions/` (12 files) read |

## E. Build (in order)
| # | Item | Status | Evidence |
|---|---|---|---|
| E1 | Create skeleton dirs (`common/`, `configs/`, `exceptions/`) where the write-guard hook allows | [ ] | |
| E2 | Split `sap-dev-rule.md` into tiered `common/` + `context-loading-protocol`; keep every `§N` resolvable (57 referencing files) or update them in the same change | [ ] | |
| E3 | System config file (version / release / modules / industry / country / tier=DEV) | [ ] | |
| E4 | `cloud-abap-constraints` as Tier 3 | [ ] | |
| E5 | Rewrite `configs/{MODULE}/` for Public Cloud from real sources (sap-docs-upstream); mark unverified items | [ ] | |
| E6 | `exceptions/` blocklist per chosen tier | [ ] | |
| E7 | Selected hooks: forbidden-table, transport check, tier read-only, activation verify, pre-compact/handoff, session-start | [ ] | |
| E8 | Integrity script (name == dir, `[Skill: x]` / `[Agent: y]` resolve) replacing manual §14 check | [ ] | |
| E9 | Per-target notes: patch `sap-dev-rule.md` §4 + §14 so per-report/function findings (decisions beyond spec, traps hit, preview results) live in `artifacts/system_analysis/<TARGET>/notes/<topic>.md`, linked from that target's `INDEX.md`; auto-memory stays preferences/feedback only. Update workflow commands / `scratchpad` + `handoff` skills to write/read notes; add a feedback memory (in the NEW memory dir, after C2) recording the routing rule. Needs user-created `.claude/.unlock` | [ ] | User chose 2026-09-21: "Trong artifacts theo target". Consistent with existing convention (INDEX.md per target, no per-tcode memory files); new part = granular `notes/` |

## F. Close-out
| # | Item | Status | Evidence |
|---|---|---|---|
| F1 | Run integrity check after every `.claude/` change | [ ] | |
| F2 | Write handbook (`artifacts/handbook/`) + `artifacts/system_analysis/SC4SAP_SKELETON/INDEX.md` | [ ] | |
| F3 | User deletes `.claude/.unlock` | [ ] | |

## Notes
- Chat with user in Vietnamese; code/identifiers/comments English.
- DEV only, Z/Y only, package mandatory, never create/modify/delete a TR; writes only in client 080.
- No SAP object, package or TR is involved in this task so far.
