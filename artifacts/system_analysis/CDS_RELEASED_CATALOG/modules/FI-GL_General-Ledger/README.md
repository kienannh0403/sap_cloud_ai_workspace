# FI-GL_General-Ledger — General Ledger

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `FI-GL` = **General Ledger**.

**233 view** · data category: (none) 118, Dimension 104, Cube 10, Fact 1 · loại: dimension 103, basic 48, text 47, value_help 25, cube 9, fact 1 · 22 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-GL-GL | 12 | component |
| FI-GL-GL-A | 26 | component |
| FI-GL-GL-AAC | 1 | component |
| FI-GL-GL-F | 1 | component |
| FI-GL-GL-N | 19 | component |
| FI-GL-IS | 162 | component |
| FI-GL-OC | 12 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_JOURNALENTRYITEM | Journal Entry Item | FI-GL-IS | Cube | 739 |
| I_GLACCOUNTLINEITEM | General Ledger Account Line Item | FI-GL-IS | Cube | 734 |
| I_GLACCOUNTLINEITEMRAWDATA | Raw Data of G/L Account Line Item | FI-GL-IS | Cube | 603 |
| I_OPERATIONALACCTGDOCITEM | Operational Accounting Document Item | FI-GL-IS | Dimension | 474 |
| I_FINANCIALPLANNINGENTRYITEM | Financial Planning Entry Item | FI-GL-IS | Cube | 333 |
| I_FINPLANNINGENTRYITEMCUBE | Financial Planning Entry Item - Cube | FI-GL-IS | Cube | 323 |
| I_PARKEDOPLACCTGDOCITEM | Parked Operational Acctg Document Item | FI-GL-IS | Cube | 219 |
| I_PARKEDOPLACCTGDOCPYBLSITEM | Parked Accounts Payable Item | FI-GL-IS | Dimension | 160 |
| I_PARKEDOPLACCTGDOCGLITEM | Parked General Ledger Item | FI-GL-IS | Dimension | 150 |
| I_JOURNALENTRY | Journal Entry | FI-GL-IS | Dimension | 131 |
| I_PARKEDOPLACCTGDOCRBLSITEM | Parked Accounts Receivable Item | FI-GL-IS | Dimension | 129 |
| I_INTERNALORDER | Internal Order | FI-GL-IS | Dimension | 128 |
| I_COSTCENTER | Cost Center | FI-GL-IS | Dimension | 118 |
| I_PARKEDOPLACCTGDOCASSETITEM | Parked Asset Item | FI-GL-IS | Dimension | 107 |
| I_FINSTATISTICALKEYFIGUREITEM | Statistical Keyfigures per period | FI-GL-IS | Cube | 73 |
| I_OPLACCTGDOCITEMFREEDFNDCRCY | Amount in Freely Defined Currency | FI-GL-IS |  | 68 |
| I_FINSTATISTICALKEYFIGITEMBSC | Statistical Keyfigure Items | FI-GL-IS | Cube | 60 |
| I_PARKEDOPLACCTGDOCUMENT | Parked Accounting Document | FI-GL-IS | Dimension | 51 |
| I_GLACCOUNTINCOMPANYCODE | General Ledger Account in Company Code | FI-GL-GL-N | Dimension | 50 |
| I_LEDGERCOMPANYCODECRCYROLES | Currency Roles for Ledger | FI-GL-IS | Dimension | 43 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 55 |
| ORG | Controlling Area | 52 |
| CONFIG | Fiscal Year | 27 |
| MASTER | G/L Account | 22 |
| ORG | Chart of Accounts | 18 |
| ORG | Segment | 16 |
| MASTER | Activity Type | 16 |
| MASTER | Grant | 14 |
| ORG | Plant | 12 |
| MASTER | Material / Product | 10 |
| ORG | Functional Area | 9 |
| DOC | Order (production / maintenance / internal) | 9 |
| DOC | Sales Document | 9 |
| MASTER | Personnel | 9 |
| MASTER | Cost Center | 7 |
| ORG | Valuation Area | 7 |
| MASTER | Customer | 7 |
| MASTER | WBS Element | 6 |
| ORG | Distribution Channel | 5 |
| ORG | Division | 5 |
| CONFIG | Sales Document Type | 5 |
| ORG | Sales Organization | 5 |
| MASTER | Supplier | 5 |
| MASTER | Profitability Segment | 5 |
| ORG | Business Area | 4 |
| MASTER | Equipment | 4 |
| MASTER | Fixed Asset | 4 |
| ORG | Profit Center | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI_other | 2 | 8 | 11 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, G/L Account, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| SD-SLS_Sales | 2 | 7 | 7 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| SD_other | 2 | 7 | 6 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| PM_other | 2 | 3 | 3 | Order (production / maintenance / internal), Sales Document, Equipment, Material / Product, WBS Element |
| MM-PUR_Purchasing | 1 | 11 | 6 | Order (production / maintenance / internal), Activity Type, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| MM_other | 1 | 9 | 6 | Order (production / maintenance / internal), Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| LE | 1 | 7 | 8 | Order (production / maintenance / internal), Cost Center, Customer, G/L Account, Material / Product, Profitability Segment, Supplier, WBS Element |
| LO_other | 1 | 6 | 7 | Order (production / maintenance / internal), Customer, Equipment, G/L Account, Material / Product, Personnel, Supplier |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
