# Data-Extraction Blocklist (index)

Tables and released CDS views whose **rows** the agent must not pull (`SAP(action="query")`, ADT data preview,
curl `datapreview/freestyle`). Reading metadata (DDLS source, field list, `sap_get_object_details`) is always
allowed. This index is not parsed; the hook `.claude/hooks/block-forbidden-tables.sh` reads every other `*.md` here.

Active profile: `BLOCKLIST_PROFILE` in `.claude/common/system-config.md` — **`standard`** (ledger A3, 2026-09-21).

| Profile | Includes | Action |
|---|---|---|
| `minimal` | files tagged `tier: minimal` | per file (`deny`; `custom-patterns.md` = `warn`) |
| `standard` | minimal + `tier: standard` | protected business data = `warn` (user confirms each query) |
| `strict` | not built — sc4sap's audit-log and communication-workflow files were excluded by the A3 decision | — |

| File | Tier | Action | Category |
|---|---|---|---|
| [banking-payment.md](banking-payment.md) | minimal | deny | Bank accounts, payment runs, cards |
| [master-data-pii.md](master-data-pii.md) | minimal | deny | Customer / supplier / BP master PII |
| [addresses-communication.md](addresses-communication.md) | minimal | deny | Addresses, phone, e-mail |
| [auth-security.md](auth-security.md) | minimal | deny | Users, roles, credentials |
| [hr-payroll.md](hr-payroll.md) | minimal | deny | HR / payroll |
| [tax-government-ids.md](tax-government-ids.md) | minimal | deny | Tax / VAT IDs |
| [pricing-conditions.md](pricing-conditions.md) | minimal | deny | Prices, conditions, rebates |
| [custom-patterns.md](custom-patterns.md) | minimal | warn | Sensitive Z/Y objects |
| [protected-business-data.md](protected-business-data.md) | standard | warn | Sales / billing / delivery / accounting documents |

## File format (what the hook parses)

- `<!-- tier: minimal|standard|strict -->` and `<!-- action: deny|warn -->` near the top of the file.
- Every markdown table row: the **first cell** holds one or more names separated by `/` or `,`.
- `NAME*` = prefix wildcard, `A###` = one digit per `#`. Header / separator rows are ignored.
- Names are matched case-insensitively against every identifier after `FROM` / `JOIN` in the SQL.

## When a request needs blocked data

Refuse the extraction, name the category ("pricing — condition records"), and offer: aggregates without the
sensitive columns, a screenshot from the Fiori app, or the functional owner. Never silently bypass the hook.

## Source note

Table names come from sc4sap `exceptions/` (MIT, v0.6.18). CDS view names marked "local catalog" exist in
`artifacts/system_analysis/CDS_RELEASED_CATALOG/catalog_all.csv`; that catalog covers 4,025 views, not all of
them, so "unverified (not in local catalog)" means only that — not that the view does not exist. sc4sap view names
absent from the catalog (e.g. `I_BankAccount`, `I_PriceCondition`) were dropped rather than guessed.
