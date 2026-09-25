# FIN

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `FIN` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**1098 view** · data category: (none) 903, Dimension 191, Cube 3, Fact 1 · loại: basic 646, dimension 191, text 147, value_help 110, cube 3, fact 1 · 62 view có field DEPRECATED/DECOMMISSIONED · 584 view mới so với file xlsx của user · 4 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FIN-CS-2CL | 2 | top-level |
| FIN-CS-COR-IS-2CL | 13 | top-level |
| FIN-CS-COR-MON-2CL | 22 | top-level |
| FIN-CS-EA-2CL | 6 | top-level |
| FIN-CS-ICR-2CL | 5 | top-level |
| FIN-CS-JE-2CL | 3 | top-level |
| FIN-CS-MD-2CL | 493 | top-level |
| FIN-FIO-CCD-COL-2CL | 9 | top-level |
| FIN-FIO-CCD-CR-2CL | 7 | top-level |
| FIN-FSCM-CLM-2CL | 13 | top-level |
| FIN-FSCM-CLM-BAM-2CL | 22 | top-level |
| FIN-FSCM-CLM-FQM-2CL | 5 | top-level |
| FIN-FSCM-COL-2CL | 189 | top-level |
| FIN-FSCM-CR-2CL | 31 | top-level |
| FIN-FSCM-DM-2CL | 64 | top-level |
| FIN-FSCM-DP-DP-2CL | 2 | top-level |
| FIN-FSCM-PF-IHB-2CL | 18 | top-level |
| FIN-FSCM-TRM-2CL | 166 | top-level |
| FIN-FSCM-TRM-AC-2CL | 1 | top-level |
| FIN-FSCM-TRM-CR-2CL | 6 | top-level |
| FIN-FSCM-TRM-MR-2CL | 8 | top-level |
| FIN-FSCM-TRM-TM-2CL | 1 | top-level |
| FIN-IE-FS-2CL | 11 | top-level |
| FIN-UA-2CL | 1 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| ICA_MATCHINGJOURNALENTRYITEM | Matching Journal Entry Item | FIN-CS-ICR-2CL |  | 396 |
| ICA_MATCHINGOPLACCTGDOCITEM | Match Operational Accounting Document Item | FIN-CS-ICR-2CL |  | 331 |
| I_CNSLDTNTASKLOGITEMDATAENTRY | Consolidation Task Log Item Data Entry | FIN-CS-COR-IS-2CL |  | 173 |
| I_CNSLDTNTASKLOGITEMDATAINPUT | Consolidation Task Log Item Data Input | FIN-CS-COR-IS-2CL |  | 173 |
| I_TRSYLDGRPOSITIONWITHVALUES | Treasury Ledger Position with Values | FIN-FSCM-TRM-2CL |  | 153 |
| I_FINANCIALTRANSACTIONDEX | Financial Transaction | FIN-FSCM-TRM-2CL |  | 137 |
| I_FINANCIALTRANSACTION | Financial Transaction | FIN-FSCM-TRM-2CL | Dimension | 125 |
| I_CNSLDTNGROUPJRNLENTRITMDEX | Group Journal Entry Item Extraction | FIN-CS-EA-2CL |  | 124 |
| I_SECURITYCLASSCONDITIONITEM | Security Class Condition Item | FIN-FSCM-TRM-2CL |  | 105 |
| I_CNSLDTNTSKLOGITEMDATAPROCESS | Consolidation Task Log Item Data Process | FIN-CS-COR-IS-2CL |  | 98 |
| I_CNSLDTNTSKLGITMRCLASSFCTN | Cnsldtn Task Log Item Reclassification | FIN-CS-COR-IS-2CL |  | 85 |
| I_CNSLDTNTSKLGITMLINEVALDTN | Cnsldtn Task Log Item Line Validation | FIN-CS-COR-IS-2CL |  | 82 |
| I_FINTRANSUNDERLYINGFLOW | Fin Transaction Underlying Flow | FIN-FSCM-TRM-2CL |  | 72 |
| I_MEMORECORD_2 | Memo Record | FIN-FSCM-CLM-2CL |  | 69 |
| I_SECURITYCLASS | Security Class | FIN-FSCM-TRM-2CL | Dimension | 68 |
| I_FINTRANSACTIVITY | Financial Transaction Activity | FIN-FSCM-TRM-2CL |  | 64 |
| I_CNSLDTNTSKLGITMCRCYTRNSLTN | Cnsldtn Tsk Lg Item Currency Translation | FIN-CS-COR-IS-2CL |  | 53 |
| C_TRSYLDGRTRANSFLOWDEX | Treasury Ledger Transaction Flow DEX | FIN-FSCM-TRM-2CL |  | 44 |
| I_STSTCLKEYFIGUREVALUEITEM | Statistical Key Figure Value Item | FIN-UA-2CL |  | 41 |
| I_CONSOLIDATIONTASKLOG | Consolidation Task Log | FIN-CS-COR-IS-2CL |  | 38 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 32 |
| MASTER | Grant | 15 |
| MASTER | Business Partner | 14 |
| CONFIG | Fiscal Year | 11 |
| ORG | Functional Area | 10 |
| ORG | Profit Center | 10 |
| MASTER | Cost Center | 9 |
| MASTER | WBS Element | 7 |
| ORG | Segment | 7 |
| ORG | Chart of Accounts | 6 |
| ORG | Business Area | 6 |
| ORG | Controlling Area | 6 |
| MASTER | Customer | 5 |
| MASTER | Material / Product | 3 |
| DOC | Order (production / maintenance / internal) | 3 |
| ORG | Plant | 3 |
| MASTER | Supplier | 3 |
| MASTER | G/L Account | 3 |
| MASTER | Personnel | 3 |
| ORG | Distribution Channel | 2 |
| ORG | Division | 2 |
| ORG | Sales Organization | 2 |
| MASTER | Activity Type | 2 |
| MASTER | Fixed Asset | 2 |
| DOC | Purchasing Document | 2 |
| DOC | Sales Document | 2 |
| CONFIG | Tax Code | 2 |
| ORG | Valuation Area | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI_other | 3 | 11 | 12 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Business Partner, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| CO_other | 3 | 6 | 12 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| PM_other | 3 | 5 | 6 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Cost Center, Material / Product, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 11 | 6 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Business Partner, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| FI-GL_General-Ledger | 2 | 10 | 11 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| MM_other | 2 | 9 | 6 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| SD-BIL_Billing | 2 | 8 | 8 | Order (production / maintenance / internal), Sales Document, Business Partner, Cost Center, Customer, G/L Account, Material / Product, Personnel, Supplier, WBS Element |
| SD_other | 2 | 7 | 8 | Order (production / maintenance / internal), Sales Document, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
