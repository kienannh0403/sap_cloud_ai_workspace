# PP-SFC_Shop-Floor-Control — Shop Floor Control

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `PP-SFC` = **Shop Floor Control**.

**72 view** · data category: (none) 57, Dimension 15 · loại: basic 44, dimension 15, text 8, value_help 5 · 9 view có field DEPRECATED/DECOMMISSIONED · 49 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PP-PI-POR-2CL | 1 | keyword |
| PP-REM-ADE-2CL | 2 | keyword |
| PP-SFC-2CL | 18 | component |
| PP-SFC-EXE-CON-2CL | 8 | component |
| PP-VDM-2CL | 43 | keyword |

> `alias` = component khác tên trong Sheet1 nhưng cùng nội dung (xem `module_map.md`); `keyword` = **suy luận theo tên view**, độ tin cậy thấp hơn `component`.

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_MANUFACTURINGORDEROPERATION | Manufacturing Order Operation | PP-VDM-2CL | Dimension | 408 |
| I_MFGORDEROPERATIONWITHSTATUS | Manufacturing Order Operation with Status | PP-VDM-2CL |  | 402 |
| I_PRODUCTIONORDEROPERATION_2 | Production Order Operation | PP-VDM-2CL |  | 325 |
| I_MANUFACTURINGORDER | Manufacturing Order | PP-VDM-2CL | Dimension | 267 |
| I_MFGORDEROPERATIONCOMPONENT | Manufacturing Order Operation Component | PP-VDM-2CL | Dimension | 258 |
| I_PRODUCTIONORDERCOMPONENT | Production Order Component | PP-VDM-2CL |  | 205 |
| I_MFGORDERCONFIRMATION | Manufacturing Order Confirmation | PP-VDM-2CL | Dimension | 184 |
| I_PRODUCTIONORDER | Production Order Header | PP-VDM-2CL |  | 178 |
| I_MANUFACTURINGORDERITEM | Manufacturing Order Item | PP-VDM-2CL | Dimension | 174 |
| I_PRODUCTIONORDERCONFIRMATION | Production Order Confirmation | PP-VDM-2CL |  | 152 |
| I_MFGORDERFAILEDCONFIRMATION | Manufacturing Order Failed Confirmation | PP-VDM-2CL | Dimension | 126 |
| I_PRODUCTIONORDERITEM | Production Order Item | PP-VDM-2CL |  | 121 |
| I_MFGORDEROPERATIONPRT | Mfg Order Operation Production Resource Tool | PP-VDM-2CL | Dimension | 100 |
| I_PRODUCTIONORDERPRT | PRT of a Production Order | PP-VDM-2CL |  | 88 |
| I_REPETITIVEMFGCONFIRMATION | Repetitive Manufacturing Confirmation | PP-VDM-2CL | Dimension | 79 |
| I_PRODNORDEROPERATIONCAPACITY | Individual Capacity of Production Order Operation | PP-VDM-2CL |  | 60 |
| I_PROCORDEROPERATIONCAPACITY | Individual Capacity of Process Order Operation | PP-VDM-2CL |  | 52 |
| I_MFGORDEROPERATIONTRGGRPOINT | Manufacturing Order Operation Trigger Point | PP-VDM-2CL | Dimension | 49 |
| I_PRODUCTIONORDERTRIGGERPOINT | Production Order Trigger Point | PP-VDM-2CL |  | 45 |
| I_PRODUCTIONORDERSEQUENCE | Production Order Sequence | PP-VDM-2CL |  | 40 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 15 |
| ORG | Business Area | 12 |
| ORG | Company Code | 12 |
| ORG | Controlling Area | 10 |
| ORG | Functional Area | 7 |
| ORG | Profit Center | 7 |
| MASTER | Material / Product | 6 |
| MASTER | Batch | 5 |
| MASTER | WBS Element | 5 |
| MASTER | Supplier | 5 |
| MASTER | Task List (routing) group | 5 |
| DOC | Inspection Lot | 4 |
| MASTER | Material Group | 4 |
| MASTER | Cost Center | 2 |
| MASTER | G/L Account | 2 |
| CONFIG | Movement Type | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| PP_other | 1 | 7 | 6 | Inspection Lot, Batch, G/L Account, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| LE | 1 | 7 | 5 | Inspection Lot, Batch, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| QM | 1 | 6 | 5 | Inspection Lot, Batch, Cost Center, G/L Account, Material / Product, Task List (routing) group, WBS Element |
| LO_other | 1 | 4 | 3 | Inspection Lot, Batch, G/L Account, Material / Product, Supplier |
| CO_other | 0 | 7 | 6 | Cost Center, G/L Account, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| FI_other | 0 | 7 | 6 | Batch, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| MM-PUR_Purchasing | 0 | 7 | 6 | Batch, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| SD-BIL_Billing | 0 | 7 | 5 | Batch, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
