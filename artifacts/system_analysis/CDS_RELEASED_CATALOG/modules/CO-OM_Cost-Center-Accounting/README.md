# CO-OM_Cost-Center-Accounting — Cost Center Accounting

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `CO-OM` = **Cost Center Accounting**.

**63 view** · data category: (none) 51, Dimension 11, Fact 1 · loại: basic 37, dimension 10, text 9, value_help 6, fact 1 · 4 view có field DEPRECATED/DECOMMISSIONED · 28 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CO-OM-2CL | 44 | component |
| CO-OM-CCA-2CL | 10 | component |
| CO-OM-CCA-A-2CL | 8 | component |
| CO-OM-CCA-AVC-2CL | 1 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_ACTPLNCOSTCENTERRPTGCUBE | Cost Center Review Booklet - Cube | CO-OM-CCA-2CL |  | 155 |
| I_INTERNALORDER | Internal Order | CO-OM-2CL | Dimension | 128 |
| I_COSTCENTER | Cost Center | CO-OM-2CL | Dimension | 118 |
| I_COSTCENTERBUDGET | Cost Center Budget Report | CO-OM-CCA-AVC-2CL |  | 80 |
| C_COSTCENTERACTUALQUERY | Cost Center Actuals - Query | CO-OM-CCA-2CL |  | 58 |
| I_ENTPROJSETTLMTDISTRRULE | Ent Project Settlement Distribution Rule | CO-OM-2CL |  | 56 |
| C_COSTCENTERPLANACTUALQUERY | Cost Center Plan and Actual Values - Query | CO-OM-CCA-2CL |  | 46 |
| I_SERVICECOSTRATE_2 | Service Cost Rate | CO-OM-2CL | Fact | 43 |
| I_COSTCENTERCHANGELOG | Cost Center Change Log | CO-OM-2CL |  | 33 |
| I_COSTCENTERACTIVITYTYPE | Cost Center Activity Type | CO-OM-2CL | Dimension | 30 |
| I_SERVICECOSTRATEDEX | Data Extraction for Service Cost Rate | CO-OM-2CL |  | 29 |
| I_ENTPROJSETTLMTRULE | Enterprise Project Settlement Rule | CO-OM-2CL |  | 28 |
| I_ACTUALCOSTRATEDEX | Data Extraction for Actual Cost Rate | CO-OM-2CL |  | 22 |
| I_COSTCENTERINCOMPANYCODE | Cost Center In Company Code | CO-OM-2CL | Dimension | 22 |
| I_PLANCOSTRATEDEX | Data Extraction for Plan Cost Rate | CO-OM-2CL |  | 22 |
| I_STATISTICALKEYFIGURE | Statistical Key Figure | CO-OM-2CL |  | 21 |
| I_COSTCENTERHIERARCHYNODE | Cost Center Hierarchy Node | CO-OM-2CL |  | 18 |
| I_COSTCTRACTIVITYTYPEHIERNODE | Cost Center Activity Type Hierarchy Node | CO-OM-2CL |  | 18 |
| I_STSTCLKEYFIGUREHIERNODE | Statistical Key Figure Hierarchy Node | CO-OM-2CL |  | 18 |
| I_CONTROLLINGOBJECT | Controlling Object | CO-OM-2CL | Dimension | 14 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Controlling Area | 33 |
| ORG | Company Code | 14 |
| MASTER | Activity Type | 12 |
| MASTER | Cost Center | 9 |
| ORG | Plant | 5 |
| MASTER | G/L Account | 5 |
| MASTER | WBS Element | 5 |
| ORG | Functional Area | 4 |
| CONFIG | Fiscal Year | 4 |
| ORG | Profit Center | 3 |
| DOC | Order (production / maintenance / internal) | 2 |
| DOC | Sales Document | 2 |
| ORG | Business Area | 2 |
| MASTER | Personnel | 2 |
| MASTER | Customer | 2 |
| ORG | Segment | 2 |
| MASTER | Supplier | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FIN | 2 | 7 | 7 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Customer, G/L Account, Personnel, Supplier, WBS Element |
| FI_other | 2 | 7 | 7 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Customer, G/L Account, Personnel, Supplier, WBS Element |
| FI-GL_General-Ledger | 2 | 7 | 6 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Customer, G/L Account, Personnel, Supplier, WBS Element |
| SD-BIL_Billing | 2 | 6 | 5 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, G/L Account, Personnel, Supplier, WBS Element |
| CO_other | 2 | 5 | 7 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, G/L Account, Supplier, WBS Element |
| SD_other | 2 | 5 | 5 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Personnel, Supplier, WBS Element |
| SD-SLS_Sales | 2 | 5 | 4 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Personnel, Supplier, WBS Element |
| PM_other | 2 | 4 | 6 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
