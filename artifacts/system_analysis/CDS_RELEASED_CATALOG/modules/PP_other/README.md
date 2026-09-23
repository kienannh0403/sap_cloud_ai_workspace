# PP_other

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `PP` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**300 view** · data category: (none) 150, Dimension 146, Fact 4 · loại: dimension 144, text 102, basic 27, value_help 23, fact 4 · 21 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PP-BD-WKC | 1 | top-level |
| PP-KAB | 1 | top-level |
| PP-KAB-VDM | 84 | top-level |
| PP-VDM | 93 | top-level |
| PP-VDM-MD | 121 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_MFGORDERWITHSTATUS | Manufacturing Order Header with Status | PP-VDM |  | 312 |
| I_MFGORDERCOMPONENTWITHSTATUS | Manufacturing Order Component with Status | PP-VDM | Fact | 249 |
| I_MFGBOOOPERATIONCHANGESTATE | Manufacturing Bill of Operations Operation Change State | PP-VDM-MD | Dimension | 196 |
| I_MFGORDERFOREXTRACTION | Manufacturing Order | PP-VDM | Dimension | 193 |
| I_MFGBOOSUBOPERATIONCHGST | Manufacturing Bill of Operations Sub Operation Change State | PP-VDM-MD | Dimension | 154 |
| I_FAILEDGOODSMOVEMENTITEM | Failed Goods Movement Item | PP-VDM | Dimension | 141 |
| I_WORKCENTER | Work Center | PP-VDM-MD | Dimension | 134 |
| I_CAPACITYREQUIREMENTITEMCAP | Capacity Requirement Item Capacity | PP-VDM | Dimension | 120 |
| I_KANBANCONTROLCYCLE | Kanban Control Cycle | PP-KAB-VDM |  | 98 |
| I_RPTVMFGCONFMATLDOCITEM | Material Document Item of Confirmation in Repetitive Mfg | PP-VDM |  | 87 |
| I_WORKCENTERBYSEMANTICKEY | Work Center By Semantic Key | PP-VDM-MD | Dimension | 87 |
| I_MFGORDERDOCDGOODSMOVEMENT | Documented Goods Movement of a Manufacturing Order | PP-VDM |  | 82 |
| I_PRODUCTIONVERSION | Production Version | PP-VDM-MD | Dimension | 72 |
| I_CAPACITY | Capacity Header | PP-VDM-MD | Dimension | 67 |
| I_MFGBILLOFOPERATIONSCHGST | Manufacturing Bill of Operations Change State | PP-VDM-MD | Dimension | 66 |
| I_WORKCENTERPOOLEDCAPACITY | Work Center Pooled Capacity | PP-BD-WKC | Dimension | 65 |
| I_KANBANCONTAINER | Kanban Container | PP-KAB-VDM |  | 63 |
| I_MFGBOOOPPRODNRSCETOOLCHGST | Mfg BOO Op Prodn Rsce Tool Change State | PP-VDM-MD | Dimension | 57 |
| I_PRODNRSCETOOLMASTERDATA | Production Resource Tool Master Data | PP-VDM-MD | Dimension | 57 |
| I_MATERIALPRODNRSCETOOL | Material Production Resource Tool | PP-VDM-MD | Dimension | 51 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 89 |
| MASTER | Material / Product | 22 |
| MASTER | Task List (routing) group | 15 |
| DOC | Order (production / maintenance / internal) | 8 |
| MASTER | Batch | 8 |
| MASTER | WBS Element | 8 |
| ORG | Controlling Area | 7 |
| MASTER | Supplier | 6 |
| ORG | Company Code | 6 |
| ORG | Business Area | 5 |
| ORG | Functional Area | 5 |
| ORG | Profit Center | 4 |
| ORG | Storage Location | 3 |
| CONFIG | Movement Type | 3 |
| ORG | Purchasing Organization | 3 |
| MASTER | Material Group | 3 |
| MASTER | Equipment | 3 |
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
| SD_other | 2 | 6 | 4 | Delivery, Order (production / maintenance / internal), Address, Batch, Material / Product, Material Group, Supplier, WBS Element |
| MM_other | 2 | 4 | 7 | Order (production / maintenance / internal), Purchasing Document, G/L Account, Material / Product, Supplier, WBS Element |
| PP-SFC_Shop-Floor-Control | 1 | 6 | 6 | Inspection Lot, Batch, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| QM | 1 | 6 | 6 | Inspection Lot, Batch, Equipment, G/L Account, Material / Product, Task List (routing) group, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
