# SD — Public Cloud module config (Tier 2 for consultants, Tier 3 for module work)

Replaces sc4sap `configs/SD/` (spro / tcodes / bapi / tables / enhancements / workflows), which is on-premise:
SPRO, SE38 tcodes, BAPIs, direct table reads and user exits do not exist for ABAP Cloud developer
extensibility on S/4HANA Cloud Public Edition.

| sc4sap file (on-prem) | Public Cloud equivalent | Here |
|---|---|---|
| `tables.md` (VBAK, VBAP, LIKP…) | Released CDS views (`I_*`) | [released-objects.md](released-objects.md) §1 |
| `bapi.md` (BAPI_SALESORDER_*) | Released RAP BOs (`I_*TP`) via EML; OData/SOAP APIs for external callers | [released-objects.md](released-objects.md) §2 |
| `enhancements.md` (user exits, MV45AFZZ) | Released enhancement spots + BAdIs (developer extensibility); custom fields/logic (key-user) | [released-objects.md](released-objects.md) §3 |
| `spro.md` | SSCUI / "Manage Your Solution" configuration (key-user, not code) | [functional.md](functional.md) |
| `tcodes.md` | Fiori apps | [functional.md](functional.md) |
| `workflows.md` | Flexible workflow | [functional.md](functional.md) |

## Evidence levels used in these files

- **Released (A)** — found on 2026-09-23 in SAP's API release-state repository (SAP/abap-atc-cr-cv-s4hc) via
  `sap-docs-upstream` `sap_search_objects` / `sap_get_object_details` with `system_type=public_cloud`.
- **Local catalog** — present in `artifacts/system_analysis/CDS_RELEASED_CATALOG/catalog_all.csv` (user-supplied
  list, 4,025 views). Not yet read on the tenant.
- **Unverified** — general SAP knowledge, not checked against either source. Verify before putting it in a TS.

Nothing in this folder has been verified on the tenant itself (my437569/080). Before first use of any object,
read it there: `SAP(action="read", target="DDLS <name>")` / `BDEF <name>`.

## Also read (do not duplicate)

- Business process knowledge: skills `sap-process-o2c-sell-from-stock`, `sap-process-o2c-customer-returns`,
  `sap-process-o2c-down-payment-billing` (+ their `references/deep-dive.md` only when the FS needs it).
- Full view lists per sub-module: `artifacts/system_analysis/CDS_RELEASED_CATALOG/modules/SD-SLS_Sales/`
  (191 views), `SD-BIL_Billing/` (34), `SD_other/` (199), `LE/` (116, deliveries).
- Data-read limits for SD documents and pricing: `.claude/exceptions/README.md` (sales/billing docs = ask,
  pricing elements = deny).
