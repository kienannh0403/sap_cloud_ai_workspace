# CO_other

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `CO` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**98 view** · data category: (none) 83, Cube 6, Dimension 6, Fact 3 · loại: basic 54, value_help 16, text 14, cube 6, dimension 5, fact 3 · 3 view có field DEPRECATED/DECOMMISSIONED · 64 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CO-FIO-CCA-TRA-2CL | 8 | top-level |
| CO-FIO-PA-2CL | 4 | top-level |
| CO-PA-2CL | 1 | top-level |
| CO-PC-ACT-2CL | 7 | top-level |
| CO-PC-ML-2CL | 10 | top-level |
| CO-PC-OBJ-ORD-2CL | 9 | top-level |
| CO-PC-OBJ-PER-2CL | 2 | top-level |
| CO-PC-OBJ-SRV-2CL | 7 | top-level |
| CO-PC-PCP-2CL | 50 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_COMPANYMARGINCUBEDST | Company Margin - Cube | CO-FIO-PA-2CL |  | 273 |
| I_PRODCOSTESTCOSTCOMPRAWDEX | Prod Cost Est Cost Comp Raw Data Ext | CO-PC-PCP-2CL | Fact | 135 |
| I_ACCTGSRVCDOCUMENTITEMBASIC | Accounting Service Document Item | CO-PC-OBJ-SRV-2CL |  | 123 |
| I_ACCOUNTINGSERVICEDOCUMENT | Accounting Service Document | CO-PC-OBJ-SRV-2CL |  | 106 |
| I_PRODUCTCOSTESTIMATE | Product Cost Estimate | CO-PC-PCP-2CL | Fact | 104 |
| I_PRODUCTCOSTESTIMATEITEM | Product Cost Estimate Item | CO-PC-PCP-2CL |  | 83 |
| I_MATERIALLEDGERCUBE_LIT | Line Item for Material Ledger - Cube | CO-PC-ML-2CL | Cube | 78 |
| I_MFGORDERACTLPLANTGTLDGRCOST | Manufacturing Order Actual Plan Target Ledger Specific Cost | CO-PC-OBJ-ORD-2CL | Cube | 74 |
| I_PROFITABILITYSEGMENT | Profitability Segment | CO-PA-2CL |  | 67 |
| I_SALESORDERITEMCOSTESTIMATE |  Sales Order Item Cost Estimate | CO-PC-PCP-2CL |  | 65 |
| I_MFGORDEREVTBSDWIPVARIANCE | Event-Based WIP and Variance of Manufacturing Order | CO-PC-OBJ-ORD-2CL | Cube | 62 |
| I_SALESORDERITEMCOSTESTITEM | Sales Order Item Cost Estimate Item | CO-PC-PCP-2CL |  | 58 |
| I_EVENTBASEDORDERPOSTINGRULE | Event-Based Mfg Order Posting Rule | CO-PC-OBJ-ORD-2CL |  | 45 |
| I_ACTLCOSTGMATLVALUECHAINITEM | Actual Costing Material Value Chain Item | CO-PC-ACT-2CL |  | 39 |
| I_TRANSBSDMATLVALUECHAINITEM | Transaction-Based Material Value Chain Item | CO-PC-ACT-2CL | Fact | 39 |
| I_PCCACTLTGTCOSTCUBE | Actual and Target Costs for PCC - Cube | CO-PC-OBJ-PER-2CL | Cube | 38 |
| I_ACTUALCOSTINGACTIVITYRESULT | Actual Costing Run Result Activity Data | CO-PC-ACT-2CL |  | 33 |
| I_WIPQUANTITYDOCUMENT | Work In Process Quantity Document | CO-PC-ACT-2CL |  | 32 |
| I_INVENTORYPRICEBYKEYDATE_2 | Inventory Price By KeyDate | CO-PC-ML-2CL |  | 32 |
| I_MATLINVTRYLDGRQTYSTRUCTURE | Matl Invtry Ledger with Qty Structure | CO-PC-ACT-2CL |  | 31 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 18 |
| ORG | Controlling Area | 17 |
| MASTER | Material / Product | 16 |
| ORG | Valuation Area | 14 |
| ORG | Plant | 11 |
| MASTER | WBS Element | 9 |
| MASTER | G/L Account | 8 |
| MASTER | Supplier | 8 |
| CONFIG | Fiscal Year | 7 |
| DOC | SD/LE Document (generic VBELN) | 7 |
| ORG | Profit Center | 6 |
| MASTER | Activity Type | 4 |
| ORG | Business Area | 3 |
| DOC | Order (production / maintenance / internal) | 3 |
| ORG | Sales Organization | 3 |
| ORG | Distribution Channel | 2 |
| ORG | Division | 2 |
| ORG | Functional Area | 2 |
| MASTER | Material Group | 2 |
| DOC | Sales Document | 2 |
| ORG | Segment | 2 |
| MASTER | Cost Center | 2 |
| ORG | Chart of Accounts | 2 |
| ORG | Sales Group | 2 |
| ORG | Sales Office | 2 |
| MASTER | Task List (routing) group | 2 |
| DOC | Purchasing Document | 2 |
| ORG | Purchasing Organization | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI_other | 4 | 7 | 12 | Order (production / maintenance / internal), Purchasing Document, SD/LE Document (generic VBELN), Sales Document, Activity Type, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| PM_other | 3 | 7 | 7 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Cost Center, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| FIN | 3 | 6 | 12 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| SD-BIL_Billing | 3 | 6 | 10 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| MM_other | 3 | 6 | 7 | Order (production / maintenance / internal), Purchasing Document, SD/LE Document (generic VBELN), Activity Type, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| SD_other | 3 | 5 | 10 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 7 | 7 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| FI-GL_General-Ledger | 2 | 6 | 11 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
