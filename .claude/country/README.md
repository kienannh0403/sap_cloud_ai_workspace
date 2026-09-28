# Country / localization references

One file per country code in `SAP_COUNTRY` (`.claude/common/system-config.md`), lowercase ISO alpha-2. Read on demand
(Tier 3, `.claude/common/context-loading-protocol.md`) when work touches tax, invoices, statutory accounting, fixed
assets, currency/amount display or date formats — never preloaded.

| File | Country | Content |
|---|---|---|
| `vn.md` | Vietnam | SAP objects released for VN (eDocument only), VND/amount/date traps, regulations cited in FS (marked `to verify` until checked) |

Adding a country: create `<iso>.md` with the same split — SAP facts with their source, regulation with a status — then
add the code to `SAP_COUNTRY`.
