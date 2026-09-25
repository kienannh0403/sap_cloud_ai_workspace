# FI-GL_General-Ledger — General Ledger

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `FI-GL` = **General Ledger**.

**286 view** · data category: (none) 185, Dimension 91, Cube 10 · loại: basic 99, dimension 91, text 62, value_help 25, cube 9 · 24 view có field DEPRECATED/DECOMMISSIONED · 85 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-GL-GL-2CL | 13 | component |
| FI-GL-GL-A-2CL | 49 | component |
| FI-GL-GL-AAC | 1 | component |
| FI-GL-GL-ACE-2CL | 1 | component |
| FI-GL-GL-ADB-2CL | 2 | component |
| FI-GL-GL-F-2CL | 11 | component |
| FI-GL-GL-N-2CL | 39 | component |
| FI-GL-IS-2CL | 145 | component |
| FI-GL-OC-2CL | 25 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_JOURNALENTRYITEM | Journal Entry Item | FI-GL-IS-2CL | Cube | 739 |
| I_GLACCOUNTLINEITEM | General Ledger Account Line Item | FI-GL-IS-2CL | Cube | 734 |
| I_GLACCOUNTLINEITEMRAWDATA | Raw Data of G/L Account Line Item | FI-GL-IS-2CL | Cube | 603 |
| I_OPERATIONALACCTGDOCITEM | Operational Accounting Document Item | FI-GL-IS-2CL | Dimension | 474 |
| I_ACTUALPLANJOURNALENTRYITEM | Actual Plan for Journal Entry Item | FI-GL-IS-2CL |  | 465 |
| I_FINANCIALPLANNINGENTRYITEM | Financial Planning Entry Item | FI-GL-IS-2CL | Cube | 333 |
| I_FINPLANNINGENTRYITEMCUBE | Financial Planning Entry Item - Cube | FI-GL-IS-2CL | Cube | 323 |
| I_PARKEDOPLACCTGDOCITEM | Parked Operational Acctg Document Item | FI-GL-IS-2CL | Cube | 219 |
| I_ACCOUNTINGDOCUMENTJOURNAL | Journal | FI-GL-IS-2CL |  | 215 |
| I_ADDLLEDGEROPLACCTGDOCITEM | Additional Ledger Journal Entry Item | FI-GL-IS-2CL |  | 186 |
| I_FINSGLAVGDAILYBALKEYFIGC | ADB Key Figures - Cube | FI-GL-GL-ADB-2CL |  | 182 |
| I_PARKEDOPLACCTGDOCGLITEM | Parked General Ledger Item | FI-GL-IS-2CL | Dimension | 150 |
| I_JOURNALENTRY | Journal Entry | FI-GL-IS-2CL | Dimension | 131 |
| I_PARKEDOPLACCTGDOCASSETITEM | Parked Asset Item | FI-GL-IS-2CL | Dimension | 107 |
| C_FINSGLAVGDAILYBALTRLBALQRY | ADB Key Figures - Query | FI-GL-GL-ADB-2CL |  | 102 |
| I_FINSTATISTICALKEYFIGUREITEM | Statistical Keyfigures per period | FI-GL-IS-2CL | Cube | 73 |
| I_OPLACCTGDOCITEMFREEDFNDCRCY | Amount in Freely Defined Currency | FI-GL-IS-2CL |  | 68 |
| I_FINSTATISTICALKEYFIGITEMBSC | Statistical Keyfigure Items | FI-GL-IS-2CL | Cube | 60 |
| I_PARKEDOPLACCTGDOCUMENT | Parked Accounting Document | FI-GL-IS-2CL | Dimension | 51 |
| I_GLACCOUNTINCOMPANYCODE | General Ledger Account in Company Code | FI-GL-GL-N-2CL | Dimension | 50 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 59 |
| ORG | Controlling Area | 33 |
| CONFIG | Fiscal Year | 30 |
| MASTER | G/L Account | 25 |
| ORG | Segment | 20 |
| ORG | Chart of Accounts | 17 |
| MASTER | Activity Type | 14 |
| MASTER | Grant | 14 |
| ORG | Plant | 14 |
| MASTER | Material / Product | 13 |
| MASTER | Personnel | 11 |
| DOC | Sales Document | 11 |
| ORG | Valuation Area | 10 |
| MASTER | Customer | 9 |
| ORG | Distribution Channel | 8 |
| ORG | Division | 8 |
| ORG | Sales Organization | 8 |
| ORG | Functional Area | 7 |
| MASTER | Supplier | 7 |
| DOC | Order (production / maintenance / internal) | 7 |
| CONFIG | Sales Document Type | 6 |
| MASTER | Profitability Segment | 6 |
| MASTER | Equipment | 5 |
| MASTER | WBS Element | 5 |
| ORG | Business Area | 4 |
| MASTER | Fixed Asset | 4 |
| MASTER | Cost Center | 3 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI_other | 2 | 11 | 11 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| FIN | 2 | 10 | 11 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| SD-BIL_Billing | 2 | 8 | 7 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, G/L Account, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| SD_other | 2 | 7 | 7 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| CO-OM_Cost-Center-Accounting | 2 | 7 | 6 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Customer, G/L Account, Personnel, Supplier, WBS Element |
| SD-SLS_Sales | 2 | 7 | 6 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| CO_other | 2 | 6 | 11 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| PM_other | 2 | 6 | 5 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Equipment, Material / Product, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
