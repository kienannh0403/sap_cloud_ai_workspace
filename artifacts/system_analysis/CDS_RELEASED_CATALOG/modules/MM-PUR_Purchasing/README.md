# MM-PUR_Purchasing — Purchasing

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `MM-PUR` = **Purchasing**.

**335 view** · data category: (none) 314, Dimension 21 · loại: basic 298, dimension 21, text 13, value_help 3 · 17 view có field DEPRECATED/DECOMMISSIONED · 220 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| MM-PUR-2CL | 2 | component |
| MM-PUR-ANA-2CL | 78 | component |
| MM-PUR-CNF-WFL-2CL | 2 | component |
| MM-PUR-GF-MAS-2CL | 4 | component |
| MM-PUR-GF-MON-2CL | 1 | component |
| MM-PUR-HUB-CSC-2CL | 2 | component |
| MM-PUR-HUB-CTR-2CL | 30 | component |
| MM-PUR-HUB-FND-2CL | 4 | component |
| MM-PUR-HUB-PO-2CL | 8 | component |
| MM-PUR-HUB-PR-2CL | 7 | component |
| MM-PUR-HUB-REQ-2CL | 1 | component |
| MM-PUR-HUB-RFQ-2CL | 18 | component |
| MM-PUR-MPS-2CL | 3 | component |
| MM-PUR-OA | 10 | component |
| MM-PUR-OA-CON | 11 | component |
| MM-PUR-OA-SCH-2CL | 25 | component |
| MM-PUR-PO-2CL | 48 | component |
| MM-PUR-PO-WFL-2CL | 2 | component |
| MM-PUR-REQ-2CL | 18 | component |
| MM-PUR-RFQ-2CL | 26 | component |
| MM-PUR-SQ | 2 | component |
| MM-PUR-SQ-QTA | 2 | component |
| MM-PUR-SQ-QTA-2CL | 2 | component |
| MM-PUR-SQ-SLI | 5 | component |
| MM-PUR-SQ-SLI-2CL | 1 | component |
| MM-PUR-SVC-SES-2CL | 12 | component |
| MM-PUR-VM-REC-2CL | 11 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PURCHASEORDERITEMAPI01 | Purchase Order Item | MM-PUR-PO-2CL |  | 184 |
| I_PROCMTHUBPURORDITMAPI01 | Centrally Managed Purchase Order Item | MM-PUR-HUB-PO-2CL |  | 125 |
| C_PURCHASEREQUISITIONITEMDEX | Data Extraction for Purchase Requisition Item | MM-PUR-ANA-2CL |  | 122 |
| C_PURORDSCHEDLINEENHCDDEX | Data Extraction for Purchase Orders Enhanced | MM-PUR-ANA-2CL |  | 110 |
| I_PURORDSCHEDLINEENHCDAPI01 | Purchase Order Schedule Line Details | MM-PUR-ANA-2CL |  | 110 |
| I_PURCHASEREQUISITIONITEMAPI01 | Purchase Requisition Item | MM-PUR-REQ-2CL |  | 110 |
| C_PURCHASEORDERHISTORYDEX | Data Extraction for Purchase Order History | MM-PUR-ANA-2CL |  | 109 |
| C_PURORDACCOUNTASSIGNMENTDEX | Data Extraction for Purchase Order Account Assignments | MM-PUR-ANA-2CL |  | 106 |
| C_SCHEDULEAGREEMENTITEMDEX | Data Extraction for Purchase Scheduling Agreement Items | MM-PUR-ANA-2CL |  | 102 |
| C_PURCHASEORDERITEMDEX | Data Extraction View for PO Item | MM-PUR-ANA-2CL |  | 101 |
| C_PURORDSCHEDULELINEDEX | Data Extraction for Purchase Order Schedule Lines | MM-PUR-ANA-2CL |  | 99 |
| C_PURCHASECONTRACTITEMDEX | Data Extraction for Purchase Contract Item | MM-PUR-ANA-2CL |  | 98 |
| C_SCHDAGRSCHDLNENHCDDEX | Data Extraction for Scheduling Agreemnet Enhanced | MM-PUR-ANA-2CL |  | 98 |
| I_SCHDAGRSCHDLNENHCDAPI01 | Sched Agreement with Schedule Line Details | MM-PUR-ANA-2CL |  | 98 |
| I_CNTRLSUPPLIERQTANITEMPRICING | Central Supplier Quotation Pricing | MM-PUR-HUB-RFQ-2CL |  | 93 |
| I_PURCHASECONTRACTITEMAPI01 | Purchase Contract Item | MM-PUR-OA-CON |  | 92 |
| I_PURCHASEORDERAPI01 | Purchase Order | MM-PUR-PO-2CL |  | 82 |
| I_PURORDITMPRICINGELEMENTAPI01 | Pricing Element in Purchase Order Item | MM-PUR-PO-2CL |  | 78 |
| I_PRMTHBRPLDPURREQNITEMAPI01 | Replicated Purchase Requisition Item | MM-PUR-HUB-PR-2CL |  | 77 |
| I_SCHEDGAGRMTITMAPI01 | Item of Purchase Scheduling Agreement | MM-PUR-OA-SCH-2CL |  | 74 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| DOC | Purchasing Document | 68 |
| ORG | Purchasing Organization | 65 |
| MASTER | Supplier | 60 |
| ORG | Company Code | 57 |
| MASTER | Material / Product | 44 |
| MASTER | Material Group | 41 |
| CONFIG | Incoterms | 27 |
| CONFIG | Tax Code | 22 |
| ORG | Plant | 18 |
| DOC | Document Condition (pricing) | 13 |
| MASTER | Batch | 11 |
| MASTER | Address | 9 |
| MASTER | G/L Account | 9 |
| ORG | Storage Location | 8 |
| ORG | Profit Center | 8 |
| MASTER | WBS Element | 7 |
| ORG | Business Area | 6 |
| MASTER | Cost Center | 6 |
| MASTER | Fixed Asset | 6 |
| DOC | Order (production / maintenance / internal) | 6 |
| DOC | Delivery | 5 |
| MASTER | Activity Type | 5 |
| ORG | Controlling Area | 5 |
| ORG | Functional Area | 5 |
| MASTER | Grant | 5 |
| MASTER | Personnel | 5 |
| CONFIG | Movement Type | 4 |
| MASTER | Profitability Segment | 4 |
| CONFIG | Fiscal Year | 4 |
| MASTER | Customer | 3 |
| MASTER | Business Partner | 3 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD_other | 3 | 11 | 6 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| LE | 3 | 9 | 6 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Batch, Cost Center, Customer, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| LO_other | 3 | 8 | 5 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |
| MM-IM_Inventory-Management | 3 | 8 | 5 | Delivery, Order (production / maintenance / internal), Purchasing Document, Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| PP_other | 3 | 7 | 8 | Delivery, Order (production / maintenance / internal), Purchasing Document, Address, Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| FI_other | 2 | 15 | 6 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Address, Batch, Business Partner, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| SD-BIL_Billing | 2 | 12 | 6 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, G/L Account, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FIN | 2 | 11 | 6 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Business Partner, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
