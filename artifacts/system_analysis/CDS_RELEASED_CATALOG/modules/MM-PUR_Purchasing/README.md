# MM-PUR_Purchasing — Purchasing

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `MM-PUR` = **Purchasing**.

**115 view** · data category: (none) 94, Dimension 21 · loại: basic 80, dimension 21, text 12, value_help 2 · 15 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| MM-PUR | 2 | component |
| MM-PUR-ANA | 24 | component |
| MM-PUR-GF-MAS | 2 | component |
| MM-PUR-HUB-CTR | 5 | component |
| MM-PUR-HUB-FND | 4 | component |
| MM-PUR-HUB-PO | 6 | component |
| MM-PUR-HUB-PR | 3 | component |
| MM-PUR-HUB-RFQ | 10 | component |
| MM-PUR-OA-CON | 5 | component |
| MM-PUR-OA-SCH | 5 | component |
| MM-PUR-PO | 14 | component |
| MM-PUR-REQ | 12 | component |
| MM-PUR-RFQ | 14 | component |
| MM-PUR-SQ-QTA | 5 | component |
| MM-PUR-SVC-SES | 4 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PURCHASEORDERITEMAPI01 | Purchase Order Item | MM-PUR-PO |  | 184 |
| I_PROCMTHUBPURORDITMAPI01 | Centrally Managed Purchase Order Item | MM-PUR-HUB-PO |  | 125 |
| I_PURORDSCHEDLINEENHCDAPI01 | Purchase Order Schedule Line Details | MM-PUR-ANA |  | 110 |
| I_PURCHASEREQUISITIONITEMAPI01 | Purchase Requisition Item | MM-PUR-REQ |  | 110 |
| I_SCHDAGRSCHDLNENHCDAPI01 | Sched Agreement with Schedule Line Details | MM-PUR-ANA |  | 98 |
| I_CNTRLSUPPLIERQTANITEMPRICING | Central Supplier Quotation Pricing | MM-PUR-HUB-RFQ |  | 93 |
| I_PURCHASECONTRACTITEMAPI01 | Purchase Contract Item | MM-PUR-OA-CON |  | 92 |
| I_PURCHASEORDERAPI01 | Purchase Order | MM-PUR-PO |  | 82 |
| I_PURORDITMPRICINGELEMENTAPI01 | Pricing Element in Purchase Order Item | MM-PUR-PO |  | 78 |
| I_PRMTHBRPLDPURREQNITEMAPI01 | Replicated Purchase Requisition Item | MM-PUR-HUB-PR |  | 77 |
| I_SCHEDGAGRMTITMAPI01 | Item of Purchase Scheduling Agreement | MM-PUR-OA-SCH |  | 74 |
| I_PROCMTHUBRPLDPURCHASEORDER | Extensibility of Purchase Order in Procurement Hub | MM-PUR-HUB-PO |  | 72 |
| I_PURORDPRICINGELEMENTAPI01 | Pricing Element in Purchase Order | MM-PUR-PO |  | 70 |
| I_POSUBCONTRACTINGCOMPAPI01 | Subcontracting Component in PurOrd | MM-PUR-PO |  | 69 |
| I_PURORDACCOUNTASSIGNMENTAPI01 | Account Assignment in Purchase Order | MM-PUR-PO |  | 68 |
| I_PURREQNACCTASSGMTAPI01 | Account Assgmt in Purchase Requisition | MM-PUR-REQ |  | 68 |
| I_PURCHASEORDERHISTORYAPI01 | Purchase Order History | MM-PUR-PO |  | 67 |
| I_PROCMTHUBPURORDHDRAPI01 | Centrally Managed Purchase Order Header | MM-PUR-HUB-PO |  | 63 |
| I_CENTRALSUPPLIERQUOTATION | Central Supplier Quotation Header | MM-PUR-HUB-RFQ |  | 59 |
| I_CNTRLSUPPLIERQUOTATIONITEM | Central Supplier Quotation Item | MM-PUR-HUB-RFQ |  | 58 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| DOC | Purchasing Document | 36 |
| ORG | Purchasing Organization | 26 |
| ORG | Company Code | 24 |
| MASTER | Supplier | 22 |
| CONFIG | Incoterms | 20 |
| MASTER | Material Group | 18 |
| MASTER | Material / Product | 17 |
| CONFIG | Tax Code | 14 |
| DOC | Document Condition (pricing) | 9 |
| MASTER | G/L Account | 8 |
| MASTER | Batch | 7 |
| ORG | Storage Location | 6 |
| MASTER | Address | 6 |
| ORG | Profit Center | 6 |
| MASTER | WBS Element | 6 |
| ORG | Plant | 6 |
| MASTER | Cost Center | 5 |
| MASTER | Fixed Asset | 5 |
| DOC | Order (production / maintenance / internal) | 5 |
| MASTER | Activity Type | 4 |
| ORG | Business Area | 4 |
| ORG | Controlling Area | 4 |
| ORG | Functional Area | 4 |
| MASTER | Grant | 4 |
| MASTER | Profitability Segment | 3 |
| MASTER | Business Partner | 3 |
| MASTER | Customer | 2 |
| DOC | Delivery | 2 |
| MASTER | Personnel | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LE | 3 | 9 | 6 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Batch, Cost Center, Customer, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| LO_other | 3 | 8 | 5 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |
| MM-IM_Inventory-Management | 3 | 8 | 5 | Delivery, Order (production / maintenance / internal), Purchasing Document, Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| PP_other | 3 | 7 | 8 | Delivery, Order (production / maintenance / internal), Purchasing Document, Address, Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| SD-SLS_Sales | 2 | 11 | 5 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| SD_other | 2 | 11 | 4 | Delivery, Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| MM_other | 2 | 9 | 7 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| FI-GL_General-Ledger | 1 | 11 | 6 | Order (production / maintenance / internal), Activity Type, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
