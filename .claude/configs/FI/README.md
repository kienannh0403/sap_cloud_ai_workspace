# FI — Financial Accounting (Public Cloud)

Sub-areas: FI-GL (general ledger / universal journal), FI-AR, FI-AP, FI-AA (asset accounting), tax.
Replaces sc4sap `configs/FI/` (on-prem SPRO, FB01/FB50, BAPI_ACC_DOCUMENT_POST, BKPF/BSEG, user exits).

**Evidence legend** (same as `configs/SD/README.md`): **R** = Released (A) in SAP's release repository,
checked 2026-09-23 via `sap-docs-upstream` (`system_type=public_cloud`) · **C** = in local catalog
`CDS_RELEASED_CATALOG/catalog_all.csv` · **f** = only in the catalog's `_fields_only/` · **u** = unverified.
Nothing here has been read on the tenant — read a DDLS/BDEF there before first use.

Files: [released-objects.md](released-objects.md).

## Key-user side (all **u**)

- Configuration via "Manage Your Solution" SSCUIs (chart of accounts, document types, posting periods, tax codes,
  payment methods). Never hard-code their values — read them through released CDS (e.g. `I_AccountingDocumentType`).
- Apps replace FB01/FB50/F-02 (Post General Journal Entries, Manage Journal Entries, Manage Fixed Assets …).
- Approvals: flexible workflow (e.g. journal entry verification); agent determination via `ES_FIN_WF_AGENT` (**R**).

## Vietnam (SAP_COUNTRY=vn)

- eInvoice VN: `I_VN_EDocInvoice` (**R**, CA-GTF-CSC-EDO-VN) + released `VNINV_01*` / `VNDELN_01*` structures;
  generic eDocument extension spot `ES_EDOCUMENT_EXT` (**R**). There is no `FI-LOC-FI-VN` component in the release
  repository (0 objects) — VN localization lives under CA-GTF-CSC-EDO-VN.
- Tax codes / tax numbers (MST) are blocklisted for row reads (`exceptions/tax-government-ids.md`).

## Also read

- Skills `sap-process-finance-general-ledger`, `sap-process-finance-asset-accounting`,
  `sap-process-finance-financial-close`.
- `artifacts/system_analysis/CDS_RELEASED_CATALOG/verified_external/FI.md` — fields and traps **verified on a real
  tenant** (other project); more reliable than the catalog.
- Catalog folders `FI-GL_General-Ledger/` (233), `FI-AR_Accounts-Receivable/` (23), `FI-AP_Accounts-Payable/` (11),
  `FI-AA_Asset-Accounting/` (9), `FI_other/` (458), `FIN/` (514).
- Blocklist: journal entries / line items = ask; bank, tax IDs = deny.
