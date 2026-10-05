---
name: fiori-ui-check
description: Open a SAP Fiori Elements (OData V4) app of a target in headless Chrome — the deployed app, or, when none is deployed yet, a generated preview over its published service binding (like ADT's Preview) — and check its UI the way a user would — in Vietnamese AND English logon — typing filters, running the search, opening value helps, reading columns / toolbar actions / object page, collecting console errors, failed requests and screenshots, read-only (never presses Post, Save, Delete or any action). Also screenshots any local HTML page (handbook) to check layout. Use in the UI-verify step of /sap-dev-create-report and /sap-dev-create-transactional-app, in the `test` item of target-refresh's final preview when the target has a deployed app, and whenever the user asks "kiểm tra UI", "mở app lên xem", "preview app", "check lỗi giao diện", "value help không ra dữ liệu", "app lỗi khi đăng nhập tiếng Việt".
---

# Fiori UI Check (read-only)

Drives the real app in headless Chrome over the DevTools Protocol with `scripts/ui_check.mjs` (Node ≥ 22, no
extra libs; Chrome at `C:/Program Files/Google/Chrome/Application/chrome.exe`, override with `--chrome`).
Login = the read-only client's SAP session cookie (`tools/vsp/cookies_cus.txt`, client 100 — rule §2 / system-config
`READONLY_SERVERS`). Never the write client 080 (no data-read authorization there, and no UI test belongs on it).

## Safety (non-negotiable)
- **Read-only.** The script has no step type that presses a button; `eval` steps containing press/click/execute/
  create/delete are rejected (exit 3). Never work around it. Testing an action (Post, Save, Create, Delete…) needs the
  user's explicit written consent for that action, on that client, and is done by the user or with that consent —
  this skill does not do it.
- Reading the app shows business data. If it falls under `.claude/exceptions/` (accounting, sales, billing… =
  `protected-business-data.md`, action warn) ask the user first, like any data query.
- Output (screenshots, logs) goes to the **session scratchpad** (or another folder outside the workspace). Only
  screenshots **without amounts or personal data** may be copied to `artifacts/targets/<TARGET>/test/ui_<yyyymmdd>/`.
- Never print or copy cookie values.

## Step 1 — find the app
1. The target's Fiori app = its `UIAD` / `WAPA` objects (Z object catalog or `SAP(action="search")`). The BSP name
   (`WAPA`, e.g. `ZZMA01E`) gives `https://<read-only host>/sap/bc/ui5_ui5/sap/<bsp lowercase>/index.html?sap-client=<client>`.
2. `curl -s -o /dev/null -w "%{http_code}" -b <cookie file> "<url>"` must be `200`, and
   `…/manifest.json` gives the entity set (`sap.ui5.routing.targets`) and the main service URI.
   - **No deployed app yet** (only a published OData V4 service binding) → **preview mode**, Step 1b.
   - HTML login page / 401 → cookie dead → [Skill: sap-doctor] cookie refresh, then retry.
   - OData V2 / non-Fiori-Elements app → only `eval` + screenshots work; say so.

## Step 1b — preview mode (no deployed app)
Same idea as the service binding's *Preview* in ADT: `scripts/preview_server.mjs` serves a generated Fiori Elements
List Report + Object Page on `http://127.0.0.1:<port>/index.html` (UI5 from `ui5.sap.com`, needs internet) and proxies
every `/sap/...` request to the read-only host with the cookie — one origin, no CORS. Filters, columns, labels, value
helps, actions, facets all come from the service annotations (CDS + DDLX), so the screen is what the deployed app
will show **except what only the app's `manifest.json` sets** (frozen columns, default variant, custom
extensions, FLP tile/navigation) → those rows stay `Proof: manual`. The proxy is read-only: anything but GET/HEAD
and GET-only `$batch` gets 403. `ui_check.mjs` starts and stops the server itself:
```bash
MSYS_NO_PATHCONV=1 node .claude/skills/fiori-ui-check/scripts/ui_check.mjs \
  --service /sap/opu/odata4/sap/<binding>/srvd/sap/<srvd>/0001/ --host https://<read-only host> --client 100 \
  [--entity <EntitySet>] [--table GridTable|ResponsiveTable] \
  --cookies tools/vsp/cookies_cus.txt --out "<scratchpad>/uic_<target>" --steps steps.json --langs VI,EN --wait 30000
```
- `MSYS_NO_PATHCONV=1`: Git Bash otherwise rewrites `/sap/...` into a Windows path (the server also repairs it).
- Service path: SRVB on the read-only client must be **published**; the path is the binding's service URL.
- `--entity`: the List Report's entity set (default: first non-value-help entity set). `--table`: what the TS / the
  app to be deployed uses (FE default `ResponsiveTable`).
- Validated 2026-10-05 on ZMA01 (`ZUI_PBCP_LSX`, GridTable): every step result equal to the deployed app ZZMA01E —
  VI value help empty / EN 3 entries, 5 rows, dates, columns, actions, object page section + 11 fields, same console
  errors. Preview-only noise (`Component-preload.js` 404, `flp;sap-metrics-only` 403) is filtered.

## Step 2 — write the steps (one file per check run)
`steps.json` = list of `{ "do": … }`, executed in order, one screenshot after each (types in the script header):

| do | fields | proves |
|---|---|---|
| `value_help` | `field` | the F4 list opens and how many entries it has (empty list = "Không có dữ liệu") |
| `fill` / `fill_date` | `field`, `value` / `date` (YYYY-MM-DD) | typed like a user; validation messages are captured |
| `go` | | search runs; messages / dialogs captured |
| `rows` | `props` | row count + distinct values of a few properties (e.g. a date the filter should have set) |
| `columns`, `actions` | | visible column headers in order; toolbar buttons + enabled/disabled (never pressed) |
| `scroll_right`, `open_row` (`index`), `facets`, `back` | | layout to the last column; object page header, sections, field count |
| `eval` | `js`, `name` | anything else, read-only |

Field names = the CDS element names (the filter field id ends with `::FilterField::<element>`). Fill every mandatory
filter from the TS/FS test data; take the values the data-verify step already used, so UI and data checks agree.

## Step 3 — run, both logon languages
```bash
node .claude/skills/fiori-ui-check/scripts/ui_check.mjs --url "<app url>" --cookies tools/vsp/cookies_cus.txt \
     --out "<scratchpad>/uic_<target>_<yyyymmdd>" --steps "<scratchpad>/steps.json" --langs VI,EN
```
Prints a per-language summary; details in `<out>/<LANG>_log.json` (step results, messages, dialogs, console errors,
HTTP ≥ 400 except favicon; framework noise such as `PropertyInfoValidator` / i18n fallback is counted, not listed).
Always run **VI and EN**: Z value helps on `DDCDS_CUSTOMER_DOMAIN_VALUE_T` filtered by `$session.system_language`
come back empty for VI when the domain texts exist only in E — a real defect, found this way on ZMA01 (2026-10-05).

## Step 4 — judge and record
1. **Look at the screenshots** (Read tool) for every step whose result matters — a returned value is not a picture:
   overlapping or cut-off text, wrong/missing labels, untranslated text, empty columns, error dialogs.
2. Judge each UI requirement (the `ui_checklist.md` row, or the FS/TS line) PASS / FAIL with the step result or
   screenshot as evidence. Each finding = one case `UI-nn`, `group: "UI"`, with input (filters, language) and actual.
3. Things this run cannot prove stay `Proof: manual` (actions that change data, printing/forms, exact visual taste,
   FLP tile/navigation, personalization; in preview mode also every `manifest.json`-only setting) — never mark them
   PASS. Say in the evidence which mode ran (`deployed app` / `preview mode`).
4. Write `artifacts/targets/<TARGET>/build/odata_verify/<yyyymmdd>_ui_check.md` (table UI-nn · check · result ·
   evidence, no amounts) and record the cases where the calling workflow says (version `tests` block for a build or
   fix; today's `records` entry for a check without code change — `.claude/common/handbook-target.md`).
5. A test artefact is not an app defect (e.g. a "required fields" dialog because Enter was pressed while other
   mandatory filters were still empty) — name it as such.

## Local HTML pages (handbook) — screenshot only
`"<chrome>" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,<height> --screenshot=<png> file:///<page>`
then Read the PNG. A `#anchor` does not scroll the shot — take a tall window and crop (PIL). Do this after every
change to the handbook renderer before saying it is done.
