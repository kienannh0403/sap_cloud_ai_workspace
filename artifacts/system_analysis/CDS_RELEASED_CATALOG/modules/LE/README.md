# LE

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `LE` (không thuộc phân hệ ưu tiên nào trong Sheet1). `LE`: Logistics Execution.

**199 view** · data category: (none) 146, Dimension 52, Cube 1 · loại: basic 113, dimension 52, text 30, value_help 3, cube 1 · 7 view có field DEPRECATED/DECOMMISSIONED · 84 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| LE-DSD | 10 | top-level |
| LE-JIT-S2C | 43 | top-level |
| LE-SHP-API-2CL | 27 | top-level |
| LE-SHP-FIO-ANA-2CL | 1 | top-level |
| LE-SHP-GF-2CL | 115 | top-level |
| LE-TRA | 3 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_DELIVERYDOCUMENTITEM | Delivery Document Item | LE-SHP-GF-2CL | Dimension | 312 |
| I_OUTBOUNDDELIVERYITEM | Outbound Delivery Document Item | LE-SHP-GF-2CL | Dimension | 264 |
| I_DELIVERYDOCUMENT | Delivery Document | LE-SHP-GF-2CL | Dimension | 259 |
| I_INBOUNDDELIVERYITEM | Inbound Delivery Item | LE-SHP-GF-2CL | Dimension | 237 |
| I_CUSTOMERRETURNDELIVERYITEM | Customer Returns Delivery Document Item | LE-SHP-GF-2CL | Dimension | 200 |
| I_OUTBOUNDDELIVERY | Outbound Delivery Document | LE-SHP-GF-2CL | Dimension | 199 |
| I_INBOUNDDELIVERY | Inbound Delivery | LE-SHP-GF-2CL | Dimension | 179 |
| I_CUSTOMERRETURNDELIVERY | Customer Returns Delivery Document | LE-SHP-GF-2CL | Dimension | 165 |
| I_JITINBCALLCOMPONENTGROUP | JIT Inbound Call Component Group | LE-JIT-S2C |  | 96 |
| I_SHPDASPLNDDELIVITEMSCUBE | Delivery Items Shipped as Planned - Cube | LE-SHP-FIO-ANA-2CL | Cube | 65 |
| I_DELIVERYPICKVIEWITEM | Delivery Pick List Item | LE-SHP-GF-2CL |  | 62 |
| I_DSD_SETTLEMENTDOCUMENTHEADER | Settlement Document Header | LE-DSD |  | 56 |
| I_JITINBOUNDCALL | JIT Inbound Call | LE-JIT-S2C |  | 45 |
| I_DSD_SETTLEMENTQUANTITYDIFF | Settlement Quantity Differences | LE-DSD |  | 44 |
| I_JITINBCALLCOMPONENT | JIT Inbound Call Component | LE-JIT-S2C |  | 41 |
| I_DSD_SETTLMTQTYDETERMINATION | Settlement Quantity Determination | LE-DSD |  | 39 |
| I_DELIVERYDUEINDEX | Delivery Due Index | LE-SHP-GF-2CL |  | 39 |
| I_JITINBCALLACTIONLOG | JIT Inbound Call Action Log | LE-JIT-S2C |  | 32 |
| I_DELIVERYPICKVIEWHEADER | Delivery Pick List Header | LE-SHP-GF-2CL |  | 31 |
| I_DELIVERYDOCUMENTTYPE | Delivery Document Type | LE-SHP-GF-2CL | Dimension | 29 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 18 |
| ORG | Shipping Point | 14 |
| MASTER | Material / Product | 10 |
| DOC | Delivery | 9 |
| DOC | Order (production / maintenance / internal) | 9 |
| ORG | Sales Office | 9 |
| MASTER | Batch | 8 |
| MASTER | Customer | 8 |
| ORG | Division | 7 |
| ORG | Storage Location | 7 |
| ORG | Distribution Channel | 6 |
| ORG | Sales Organization | 6 |
| MASTER | Supplier | 6 |
| DOC | Inspection Lot | 5 |
| CONFIG | Movement Type | 5 |
| ORG | Sales Group | 5 |
| CONFIG | Incoterms | 4 |
| ORG | Business Area | 4 |
| ORG | Controlling Area | 4 |
| MASTER | Cost Center | 4 |
| MASTER | G/L Account | 4 |
| MASTER | Material Group | 4 |
| ORG | Profit Center | 4 |
| MASTER | Profitability Segment | 4 |
| DOC | Document Condition (pricing) | 3 |
| ORG | Functional Area | 3 |
| DOC | SD/LE Document (generic VBELN) | 2 |
| MASTER | WBS Element | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD_other | 4 | 8 | 11 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), SD/LE Document (generic VBELN), Batch, Cost Center, Customer, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| LO_other | 4 | 5 | 8 | Delivery, Document Condition (pricing), Inspection Lot, Order (production / maintenance / internal), Batch, Customer, G/L Account, Material / Product, Supplier |
| SD-BIL_Billing | 3 | 9 | 11 | Document Condition (pricing), Order (production / maintenance / internal), SD/LE Document (generic VBELN), Batch, Cost Center, Customer, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| MM-PUR_Purchasing | 3 | 9 | 6 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Batch, Cost Center, Customer, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| PP_other | 3 | 6 | 6 | Delivery, Inspection Lot, Order (production / maintenance / internal), Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| FI_other | 2 | 9 | 8 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Batch, Cost Center, Customer, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| SD-SLS_Sales | 2 | 8 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Batch, Cost Center, Customer, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| MM-IM_Inventory-Management | 2 | 8 | 4 | Delivery, Order (production / maintenance / internal), Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
