# PP-SFC_Shop-Floor-Control — Shop Floor Control

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `PP-SFC` = **Shop Floor Control**.

**23 view** · data category: Dimension 15, (none) 8 · loại: dimension 15, text 6, value_help 1, basic 1 · 9 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PP-VDM | 23 | keyword |

> `alias` = component khác tên trong Sheet1 nhưng cùng nội dung (xem `module_map.md`); `keyword` = **suy luận theo tên view**, độ tin cậy thấp hơn `component`.

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_MANUFACTURINGORDEROPERATION | Manufacturing Order Operation | PP-VDM | Dimension | 408 |
| I_MFGORDEROPERATIONWITHSTATUS | Manufacturing Order Operation with Status | PP-VDM |  | 402 |
| I_MANUFACTURINGORDER | Manufacturing Order | PP-VDM | Dimension | 267 |
| I_MFGORDEROPERATIONCOMPONENT | Manufacturing Order Operation Component | PP-VDM | Dimension | 258 |
| I_MFGORDERCONFIRMATION | Manufacturing Order Confirmation | PP-VDM | Dimension | 184 |
| I_MANUFACTURINGORDERITEM | Manufacturing Order Item | PP-VDM | Dimension | 174 |
| I_MFGORDERFAILEDCONFIRMATION | Manufacturing Order Failed Confirmation | PP-VDM | Dimension | 126 |
| I_MFGORDEROPERATIONPRT | Mfg Order Operation Production Resource Tool | PP-VDM | Dimension | 100 |
| I_REPETITIVEMFGCONFIRMATION | Repetitive Manufacturing Confirmation | PP-VDM | Dimension | 79 |
| I_MFGORDEROPERATIONTRGGRPOINT | Manufacturing Order Operation Trigger Point | PP-VDM | Dimension | 49 |
| I_CONFIRMATIONAPPLORIGIN | Confirmation Application Origin | PP-VDM | Dimension | 3 |
| I_CONFIRMATIONRECORDTYPE | Confirmation Record Type | PP-VDM | Dimension | 3 |
| I_FINALCONFIRMATIONTYPE | Final Confirmation Type | PP-VDM | Dimension | 3 |
| I_MANUFACTURINGORDERIMPORTANCE | Manufacturing Order Importance Code | PP-VDM | Dimension | 3 |
| I_ORDERCONFIRMATIONTYPE | Order Confirmation Type | PP-VDM | Dimension | 3 |
| I_CONFIRMATIONGROUP | Confirmation Group | PP-VDM | Dimension | 1 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 8 |
| ORG | Business Area | 7 |
| ORG | Company Code | 7 |
| ORG | Controlling Area | 6 |
| ORG | Functional Area | 4 |
| MASTER | Material / Product | 4 |
| ORG | Profit Center | 4 |
| MASTER | Batch | 3 |
| DOC | Inspection Lot | 3 |
| MASTER | WBS Element | 3 |
| MASTER | Supplier | 3 |
| MASTER | Task List (routing) group | 3 |
| MASTER | Material Group | 2 |
| MASTER | Cost Center | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| PP_other | 1 | 6 | 6 | Inspection Lot, Batch, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| LE | 1 | 6 | 5 | Inspection Lot, Batch, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| QM | 1 | 5 | 5 | Inspection Lot, Batch, Cost Center, Material / Product, Task List (routing) group, WBS Element |
| LO_other | 1 | 3 | 3 | Inspection Lot, Batch, Material / Product, Supplier |
| MM-PUR_Purchasing | 0 | 6 | 6 | Batch, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| MM-IM_Inventory-Management | 0 | 6 | 4 | Batch, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| SD-SLS_Sales | 0 | 6 | 4 | Batch, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| SD_other | 0 | 6 | 3 | Batch, Cost Center, Material / Product, Material Group, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
