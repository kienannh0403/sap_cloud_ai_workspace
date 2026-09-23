# LE

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `LE` (không thuộc phân hệ ưu tiên nào trong Sheet1). `LE`: Logistics Execution.

**116 view** · data category: (none) 63, Dimension 52, Cube 1 · loại: dimension 52, basic 35, text 26, value_help 2, cube 1 · 7 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| LE-DSD | 10 | top-level |
| LE-SHP-FIO-ANA | 1 | top-level |
| LE-SHP-GF | 101 | top-level |
| LE-TRA | 4 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_DELIVERYDOCUMENTITEM | Delivery Document Item | LE-SHP-GF | Dimension | 312 |
| I_OUTBOUNDDELIVERYITEM | Outbound Delivery Document Item | LE-SHP-GF | Dimension | 264 |
| I_DELIVERYDOCUMENT | Delivery Document | LE-SHP-GF | Dimension | 259 |
| I_INBOUNDDELIVERYITEM | Inbound Delivery Item | LE-SHP-GF | Dimension | 237 |
| I_CUSTOMERRETURNDELIVERYITEM | Customer Returns Delivery Document Item | LE-SHP-GF | Dimension | 200 |
| I_OUTBOUNDDELIVERY | Outbound Delivery Document | LE-SHP-GF | Dimension | 199 |
| I_INBOUNDDELIVERY | Inbound Delivery | LE-SHP-GF | Dimension | 179 |
| I_CUSTOMERRETURNDELIVERY | Customer Returns Delivery Document | LE-SHP-GF | Dimension | 165 |
| I_SHPDASPLNDDELIVITEMSCUBE | Delivery Items Shipped as Planned - Cube | LE-SHP-FIO-ANA | Cube | 65 |
| I_DELIVERYPICKVIEWITEM | Delivery Pick List Item | LE-SHP-GF |  | 62 |
| I_DSD_SETTLEMENTDOCUMENTHEADER | Settlement Document Header | LE-DSD |  | 56 |
| I_DSD_SETTLEMENTQUANTITYDIFF | Settlement Quantity Differences | LE-DSD |  | 44 |
| I_DSD_SETTLMTQTYDETERMINATION | Settlement Quantity Determination | LE-DSD |  | 39 |
| I_DELIVERYDUEINDEX | Delivery Due Index | LE-SHP-GF |  | 39 |
| I_DELIVERYPICKVIEWHEADER | Delivery Pick List Header | LE-SHP-GF |  | 31 |
| I_DELIVERYDOCUMENTTYPE | Delivery Document Type | LE-SHP-GF | Dimension | 29 |
| I_DSD_CURRENTTOURSTATUS | Current Tour Status | LE-DSD |  | 26 |
| I_DSD_SETTLEMENTPAYMENTDIFF | Settlement Payment Differences | LE-DSD |  | 18 |
| I_DSD_STKVISIBILITYTRUCKSTOCK | Stock Visibility Truck Stock | LE-DSD |  | 18 |
| I_DSD_SETTLEMENTDOCUMENTFLOW | Settlement Document Flow | LE-DSD |  | 11 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 14 |
| ORG | Shipping Point | 13 |
| MASTER | Material / Product | 9 |
| DOC | Delivery | 9 |
| DOC | Order (production / maintenance / internal) | 9 |
| ORG | Sales Office | 9 |
| MASTER | Batch | 8 |
| MASTER | Customer | 7 |
| MASTER | Supplier | 6 |
| ORG | Sales Organization | 5 |
| ORG | Distribution Channel | 5 |
| ORG | Division | 5 |
| DOC | Inspection Lot | 5 |
| CONFIG | Movement Type | 5 |
| ORG | Sales Group | 5 |
| ORG | Storage Location | 5 |
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
| LO_other | 4 | 5 | 8 | Delivery, Document Condition (pricing), Inspection Lot, Order (production / maintenance / internal), Batch, Customer, G/L Account, Material / Product, Supplier |
| MM-PUR_Purchasing | 3 | 9 | 6 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Batch, Cost Center, Customer, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| SD_other | 3 | 8 | 10 | Delivery, Order (production / maintenance / internal), SD/LE Document (generic VBELN), Batch, Cost Center, Customer, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| PP_other | 3 | 6 | 6 | Delivery, Inspection Lot, Order (production / maintenance / internal), Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| SD-SLS_Sales | 2 | 8 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Batch, Cost Center, Customer, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| MM-IM_Inventory-Management | 2 | 8 | 4 | Delivery, Order (production / maintenance / internal), Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| MM_other | 2 | 5 | 5 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| FI-GL_General-Ledger | 1 | 7 | 8 | Order (production / maintenance / internal), Cost Center, Customer, G/L Account, Material / Product, Profitability Segment, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
