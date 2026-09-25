# PP_other

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `PP` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**383 view** · data category: (none) 233, Dimension 146, Fact 4 · loại: dimension 144, text 104, basic 104, value_help 27, fact 4 · 22 view có field DEPRECATED/DECOMMISSIONED · 83 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PP-BD-WKC-2CL | 4 | top-level |
| PP-CFS-CE-2CL | 1 | top-level |
| PP-ES | 5 | top-level |
| PP-FIO-2CL | 6 | top-level |
| PP-FIO-MRP-2CL | 1 | top-level |
| PP-KAB-2CL | 4 | top-level |
| PP-KAB-CC-2CL | 2 | top-level |
| PP-KAB-VDM-2CL | 85 | top-level |
| PP-PI-POR-2CL | 15 | top-level |
| PP-PLO-2CL | 4 | top-level |
| PP-REM-ADE-2CL | 2 | top-level |
| PP-VDM-2CL | 101 | top-level |
| PP-VDM-MD-2CL | 153 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_MFGORDERWITHSTATUS | Manufacturing Order Header with Status | PP-VDM-2CL |  | 312 |
| I_MFGORDERCOMPONENTWITHSTATUS | Manufacturing Order Component with Status | PP-VDM-2CL | Fact | 249 |
| I_MFGBOOOPERATIONCHANGESTATE | Manufacturing Bill of Operations Operation Change State | PP-VDM-MD-2CL | Dimension | 196 |
| I_MFGORDERFOREXTRACTION | Manufacturing Order | PP-VDM-2CL | Dimension | 193 |
| I_MFGBOOSUBOPERATIONCHGST | Manufacturing Bill of Operations Sub Operation Change State | PP-VDM-MD-2CL | Dimension | 154 |
| I_FAILEDGOODSMOVEMENTITEM | Failed Goods Movement Item | PP-VDM-2CL | Dimension | 141 |
| I_WORKCENTER | Work Center | PP-VDM-MD-2CL | Dimension | 134 |
| I_CAPACITYREQUIREMENTITEMCAP | Capacity Requirement Item Capacity | PP-VDM-2CL | Dimension | 120 |
| I_MFGORDERCONFMATLDOCITEM | Material Document Items of Mfg Order Confirmation | PP-VDM-2CL |  | 109 |
| I_KANBANCONTROLCYCLE | Kanban Control Cycle | PP-KAB-VDM-2CL |  | 98 |
| I_RPTVMFGCONFMATLDOCITEM | Material Document Item of Confirmation in Repetitive Mfg | PP-VDM-2CL |  | 87 |
| I_WORKCENTERBYSEMANTICKEY | Work Center By Semantic Key | PP-VDM-MD-2CL | Dimension | 87 |
| I_MFGORDERDOCDGOODSMOVEMENT | Documented Goods Movement of a Manufacturing Order | PP-VDM-2CL |  | 82 |
| I_PRODUCTIONVERSION | Production Version | PP-VDM-MD-2CL | Dimension | 72 |
| I_CAPACITY | Capacity Header | PP-VDM-MD-2CL | Dimension | 67 |
| I_MFGBILLOFOPERATIONSCHGST | Manufacturing Bill of Operations Change State | PP-VDM-MD-2CL | Dimension | 66 |
| I_WORKCENTERPOOLEDCAPACITY | Work Center Pooled Capacity | PP-BD-WKC-2CL | Dimension | 65 |
| I_KANBANCONTAINER | Kanban Container | PP-KAB-VDM-2CL |  | 63 |
| I_MFGBOOOPPRODNRSCETOOLCHGST | Mfg BOO Op Prodn Rsce Tool Change State | PP-VDM-MD-2CL | Dimension | 57 |
| I_PRODNRSCETOOLMASTERDATA | Production Resource Tool Master Data | PP-VDM-MD-2CL | Dimension | 57 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 95 |
| MASTER | Material / Product | 23 |
| MASTER | Task List (routing) group | 15 |
| MASTER | Batch | 9 |
| MASTER | WBS Element | 9 |
| DOC | Order (production / maintenance / internal) | 8 |
| ORG | Controlling Area | 7 |
| MASTER | Supplier | 6 |
| ORG | Company Code | 6 |
| ORG | Business Area | 5 |
| ORG | Functional Area | 5 |
| ORG | Profit Center | 4 |
| MASTER | Equipment | 4 |
| ORG | Storage Location | 3 |
| CONFIG | Movement Type | 3 |
| ORG | Purchasing Organization | 3 |
| MASTER | Material Group | 3 |
| DOC | Delivery | 2 |
| MASTER | G/L Account | 2 |
| DOC | Inspection Lot | 2 |
| MASTER | Address | 2 |
| DOC | Purchasing Document | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| MM-PUR_Purchasing | 3 | 7 | 8 | Delivery, Order (production / maintenance / internal), Purchasing Document, Address, Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| LE | 3 | 6 | 6 | Delivery, Inspection Lot, Order (production / maintenance / internal), Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| LO_other | 3 | 6 | 5 | Delivery, Inspection Lot, Order (production / maintenance / internal), Address, Batch, Equipment, G/L Account, Material / Product, Supplier |
| MM-IM_Inventory-Management | 3 | 6 | 5 | Delivery, Order (production / maintenance / internal), Purchasing Document, Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| FI_other | 2 | 7 | 6 | Order (production / maintenance / internal), Purchasing Document, Address, Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| CO_other | 2 | 6 | 7 | Order (production / maintenance / internal), Purchasing Document, G/L Account, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| PM_other | 2 | 6 | 7 | Order (production / maintenance / internal), Purchasing Document, Equipment, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| SD_other | 2 | 6 | 6 | Delivery, Order (production / maintenance / internal), Address, Batch, Material / Product, Material Group, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
