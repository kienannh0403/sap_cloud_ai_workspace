# System Config — Public Cloud workspace (Tier 1)

Single source for "what system is this workspace talking to". Loaded every session (Tier 1, see
`context-loading-protocol.md`). Hooks parse ONLY the `KEY=value` lines inside the fenced `env` block below
(`.claude/hooks/lib-config.sh`) — keep one key per line, no spaces around `=`, no quotes.

```env
SAP_VERSION=S4_CLOUD_PUBLIC
SAP_PRODUCT=SAP S/4HANA Cloud Public Edition
ABAP_LANGUAGE_VERSION=ABAP_FOR_CLOUD_DEVELOPMENT
SAP_ACTIVE_MODULES=SD,FI,CO,MM,PP,QM,PM,PS,TM,EWM,TR
SAP_INDUSTRY=
SAP_COUNTRY=vn
SAP_TIER=DEV
BLOCKLIST_PROFILE=standard
WRITE_SERVERS=sap_cloud_dev
READONLY_SERVERS=sap_gm2_cus_ro
```

## Meaning

| Key | Value | Source / decision |
|---|---|---|
| `SAP_VERSION` | `S4_CLOUD_PUBLIC` | Tier 3 trigger for `cloud-abap-constraints.md` |
| `ABAP_LANGUAGE_VERSION` | ABAP for Cloud Development | Public Cloud developer extensibility — classic ABAP is not available |
| `SAP_ACTIVE_MODULES` | 11 modules | Ledger A1 (2026-09-21): SD only; extended 2026-09-23 (user: "toàn bộ module", 10 Public Cloud modules). WM → `EWM`, PS = Enterprise Projects (PPM-SCL), TR = Treasury. sc4sap's Ariba, BW, HCM left out: no ABAP module in Public Cloud. Adding a module = create `configs/<MODULE>/README.md` first |
| `SAP_INDUSTRY` | *(empty)* | Ledger A2: none chosen |
| `SAP_COUNTRY` | `vn` | Ledger A2 |
| `SAP_TIER` | `DEV` | Rule §2: every connection is DEV. Any other value makes `tier-readonly-guard.sh` block ALL SAP mutations |
| `BLOCKLIST_PROFILE` | `standard` | Ledger A3: `minimal` files (deny) + protected business data (warn); strict-only files excluded |
| `WRITE_SERVERS` | `sap_cloud_dev` | MCP server name. Host my437569, client 080, SID GM2 — the only place objects are written |
| `READONLY_SERVERS` | `sap_gm2_cus_ro` | Host my437557, client 100 — read / test / debug only. `tier-readonly-guard.sh` denies create/edit/delete on it |

## Not recorded here (on purpose)

- **Release / FPS number** — *unverified*: `SAP(action="system", target="INFO")` fails on 080 (no data-read
  authorization, see memory `sap-dev-no-data-read-authorization`), so no release string has been read from the
  tenant. Fill it in from the tenant's "About" dialog when needed; never guess it.
- **URLs, users, cookies** — live connection data lives in `.mcp.json` (git-ignored) and `tools/vsp/cookies_*.txt`.
  Never copy them here.
