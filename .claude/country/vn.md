# Vietnam (`SAP_COUNTRY=vn`) — localization reference

Tier 3 (`.claude/common/context-loading-protocol.md`): read when an FS/TS, report, form or code touches tax, invoices,
statutory accounting, fixed assets, amounts/currency display or date formats for a Vietnamese company code.

Two kinds of content, kept apart on purpose:
- **SAP facts** — checked against SAP's own release data in this workspace (source column). Reliable.
- **Regulation** — Vietnamese law/circulars from general knowledge, **not** read from an official gazette in this
  workspace. Status `to verify` means: confirm the number, date and scope with the customer's chief accountant or the
  official text before it drives a design decision. Never quote a `to verify` item to the customer as fact.

## 1. SAP objects released for Vietnam (Public Cloud)

| Object | Kind | What it is | Source |
|---|---|---|---|
| `I_VN_EDocInvoice` | CDS view (basic), package `GLO-EDO-VN`, component `CA-GTF-CSC-EDO-VN` | eDocument Vietnam Invoice — the read entry point for VN e-invoice status/data, key entity company code, 13 fields | CDS catalog (`in_080=yes`) + API Hub 2026-09-10 |
| `VNINV_01*` | 77 structures + 16 table types + 10 data elements in total with `VNDELN_01*` (same component) | Message types of the VN **e-invoice** (header `HDON`, seller `NBAN`, buyer `NMUA`, lines `HHDVU`, tax rate `TSUAT`, fees `LPHI`, discount rate `TLCKHAU`…) — names follow the Vietnamese XML tags of the tax authority schema | `SAP_RELEASE_WATCH/released_objects/objects.csv` |
| `VNDELN_01*` | same family | Messages of the VN **delivery note** e-document (phiếu xuất kho kiêm vận chuyển nội bộ: transport means `PTVCHUYEN`, from/to warehouse `HVTNXHANG`/`HVTNNHANG`, internal dispatch order `LDDNBO`, economic contract no./date `HDKTSO`/`HDKTNGAY`) | same |
| `EDOC_ADAPTOR_CLOUD`, `EDOC_ADAPTOR_CLOUD_VAR_KEY`, `EDOCUMENT_BASE_EXT`, `EDOCUMENT_INT_CONN_EXT` | BAdI (generic eDocument, all countries) | The only extension points for eDocument on Public Cloud — **there is no Vietnam-specific eDocument BAdI** (India, Mexico, Spain, Turkey, Thailand have their own; VN does not) | API Hub `artifacts.csv` |
| `FAA_DC_UPA_CUSTOMER`, `FAA_DC_MEMO_VALUE` | BAdI (asset accounting) | Customer depreciation calculation / country-specific memo value — the hooks if a VN depreciation rule is not covered by standard depreciation keys | API Hub `artifacts.csv` |

Not found in SAP's release data (so: not available as released objects, design around it): a VN VAT return / tax
declaration view, a VN statutory financial-statement (B01/B02/B03/B09) view, a VN asset-register view. Such reports are
built on the generic released views (`I_JournalEntryItem`, `I_GLAccountLineItem`, `I_FixedAsset…`, tax views of the FI
catalog) — look them up in `artifacts/system_analysis/CDS_RELEASED_CATALOG/` per module, never assume a VN view exists.

## 2. Amounts, currency, dates (SAP behaviour — verified traps)

| Rule | Why |
|---|---|
| VND has **0 decimals** (ISO 4217). SAP stores CURR amounts with 2 decimal places and shifts currencies with 0 decimals by factor 100 internally | ADT data preview shows `240717268` VND as `2407172.68` (memory `sap-cloud-dev-connection`, ZGL02 2026-09-10). Never read decimals from a data preview; compare with the app output or an export |
| Every amount field keeps its currency reference (`@Semantics.amount.currencyCode` in CDS, currency-aware output in ABAP/forms) — never divide/multiply by 100 by hand | The shift is currency-dependent; a hard-coded factor breaks USD/EUR lines in the same report |
| Display: thousands separator `.` and decimal separator `,` is the Vietnamese convention; the user's SAP profile decides what Fiori shows — a form/Excel output must state the format it uses | FS mock-ups usually show `1.234.567` — confirm per report, do not assume |
| Dates: `dd/mm/yyyy` on printed documents | Statutory forms and e-invoices use day-first |
| Amount in words (số tiền bằng chữ) on invoices/vouchers: Vietnamese wording, no released SAP function for it on Public Cloud — a Z helper is needed | Candidate already on the system: `ZCL_AMOUNT_READER` / `ZIF_AMOUNT_READER` in package `ZUTIL` ("convert amount to words", Z catalog 2026-09-28) — read its source before reusing; amount formatting: `ZCL_FORMAT_AMOUNT` and `ZCL_FORMAT_AMOUNT_V2` (same package, check which one is current) |

## 3. Regulation that FS documents cite (to verify before relying on it)

| Topic | Commonly cited basis | What it means for SAP work | Status |
|---|---|---|---|
| Accounting regime (chế độ kế toán doanh nghiệp) | Circular 200/2014/TT-BTC (large enterprises), 133/2016/TT-BTC (SMEs); **200 reported replaced by Circular 99/2025/TT-BTC from 2026-01-01** | Chart of accounts, statutory statement layouts (B01-DN balance sheet, B02-DN P&L, B03-DN cash flow, B09-DN notes). An FS that still says "theo TT200" for FY2026+ → ask which regime the customer applies | to verify |
| Fixed assets — recognition and depreciation | Circular 45/2013/TT-BTC (+ amendments 147/2016, 28/2017): asset threshold ≥ 30 million VND and useful life > 1 year; straight-line default; useful-life frames per asset group | ZAA01-type reports: columns for opening/increase/decrease/closing of original cost (nguyên giá), accumulated depreciation and net book value per asset class; assets below threshold are tools & supplies (CCDC), not FA | to verify |
| E-invoice | Decree 123/2020/ND-CP and Circular 78/2021/TT-BTC; Decree 70/2025/ND-CP amends 123 (from 2025-06-01) | Invoice data flows through eDocument (§1); a report of issued invoices reads `I_VN_EDocInvoice` + billing documents, not a Z table | to verify |
| VAT | Law on VAT 48/2024/QH15 (from 2025-07-01); rates 0 % / 5 % / 10 %, plus temporary reductions to 8 % decided by National Assembly resolutions for limited periods | Tax codes in the company code carry the rate; a VAT report groups by tax code — never hard-code rates, the 8 % reduction changes with each resolution | to verify |
| Accounting documents & books | Law on Accounting 88/2015/QH13; voucher and book forms in the accounting-regime circular | Printed vouchers (phiếu thu/chi, phiếu nhập/xuất kho) follow the regime's form numbers → PDF/Excel form skills | to verify |

## 4. How to use it
- FS analysis: when the FS cites a circular, check it against §3 and raise a question if the status is `to verify`
  or the FS's regime differs from the fiscal year's.
- Designing a source: §1 first — a VN-specific released object exists only for eDocument.
- Output (report, form, Excel): §2 rules apply to every amount and date column.
- New fact learned (verified with the customer or an official text) → propose an update to this file (rule §14),
  with the source and date; move the row from `to verify` to `verified <date>, <source>`.
