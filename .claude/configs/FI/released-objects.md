# FI — released objects

Legend: see [README.md](README.md).

## 1. Read — CDS views

| Area | Views | Evidence |
|---|---|---|
| Journal entry (BKPF) | `I_JournalEntry` | C |
| Line items (ACDOCA / BSEG) | `I_JournalEntryItem`, `I_GLAccountLineItem`, `I_OperationalAcctgDocItem` | C |
| Actual + plan items | `I_ActualPlanJournalEntryItem` | R (catalog: f only) |
| G/L accounts | `I_GLAccount`, `I_GLAccountInChartOfAccounts`, `I_ChartOfAccounts` | C |
| Org / dimensions | `I_CompanyCode`, `I_Ledger`, `I_ProfitCenter`, `I_Segment`, `I_BusinessArea`, `I_FiscalYearPeriod`, `I_FiscalCalendarDate` | C |
| Document type | `I_AccountingDocumentType` | f |
| Customers / suppliers | `I_Customer`, `I_Supplier` (+ company views) | C — **row reads denied** (PII) |
| Tax | `I_TaxCode` (C), `I_TaxCodeRate` (f) | |
| Currency | `I_Currency`, `I_ExchangeRateRawData` | C — conversion in code: `CL_EXCHANGE_RATES` (R) |
| Fixed assets | `I_FixedAsset`, `I_FixedAssetAssgmt` (C), `I_AssetClass` (f) | |
| Banking | `I_HouseBank`, `I_PaymentTerms` | C — bank detail views denied |

Not found anywhere, do not use without checking: `I_GLAcctBalanceCube`, `I_OperationalAcctgDocCube`, `I_DunningLevel`.

## 2. Write — RAP BOs (EML)

| BO | Purpose | Evidence |
|---|---|---|
| `I_JournalEntryTP` | Post / change / reverse journal entries (component AC-INT, not FI) | R |
| `D_JournalEntryPostParameter`, `D_JournalEntryChangeParameter`, `D_JournalEntryPostCurrencyAmtP` | Action parameters | R |
| `I_GLAdjmtAcctgNotifTP` | G/L adjustment accounting notification | R |
| `I_OrganizationalChangeTP` | Organizational change (profit center reassignment) | R |
| `I_RACONTRMNGREVNCONTRTP` | Revenue accounting contracts | R |
| `I_CADocumentTP`, `I_ContractAccountTP`, `I_CABillgDocumentTP`, `I_CAInvcgDocumentTP` | Contract accounting (FI-CA) — only if FI-CA is in scope | R |

No released BDEF for fixed assets or G/L account master found (`query=FIXEDASSET` → 0; `GLACCOUNT` → only consolidation).

## 3. Extend — enhancement spots (core only; the repository lists 195 FI spots, most are country-specific)

| Spot | Area | Evidence |
|---|---|---|
| `ES_FIN_WF_AGENT` | Workflow agent determination (G/L) | R |
| `ES_FINS_LZBKZ_LANDL_DERIVE` | Derivation in G/L posting | R |
| `ES_ACE_DOCUMENT_CLD`, `ES_ACE_DOCUMENT_CUST`, `FACRA_ACCR_REVIEW_APPROVE`, `POAC_ACCR_OBJECT` | Accrual engine | R |
| `FOT_VATDATE_RULES`, `FOT_VAT_DECLARATION`, `FOT_EXT_TAX_CALC_FIELDS_CHANGE` | Tax | R |
| `FBL_BADI_PAYMENT_MEDIUM`, `FBL_BADI_PAYMENT_ADVICE` | Payment medium / advice (AP) | R |
| `FI_INT_NON_LINEAR_INT_FORMULA` | Interest calculation (AR) | R |
| `FAA_DC_UPA_CUSTOMER` | Asset accounting — depreciation | R |
| `ES_EDOCUMENT_EXT` | eDocument (incl. VN eInvoice) | R |

Full list: `sap_search_objects(object_type="ENHS", app_component="FI-GL" | "FI-AR" | "FI-AP" | "FI-AA")`.
