# SD_other

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `SD` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**199 view** · data category: (none) 147, Dimension 38, Cube 14 · loại: basic 80, text 67, dimension 38, cube 14 · 9 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SD-ANA | 17 | top-level |
| SD-ANA-SP | 5 | top-level |
| SD-BF | 2 | top-level |
| SD-BF-CM | 24 | top-level |
| SD-BF-MD | 16 | top-level |
| SD-BF-PD | 4 | top-level |
| SD-BF-PR | 35 | top-level |
| SD-BF-TX | 2 | top-level |
| SD-CRF | 2 | top-level |
| SD-CRF-ORG | 16 | top-level |
| SD-MD-CM | 57 | top-level |
| SD-MD-MM | 19 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SLSORDCONFANALYTICSCUBE | Confirmation of Sales Orders - Cube | SD-ANA | Cube | 383 |
| I_SALESORDERITEMCUBE | Sales Order Item - Cube | SD-ANA | Cube | 378 |
| I_SALESQUOTATIONITEMCUBE_2 | Sales Quotation Item - Cube | SD-ANA | Cube | 237 |
| I_SALESCONTRACTITEMCUBE | Sales Contract Item - Cube | SD-ANA | Cube | 213 |
| I_SALESORDERCUBE | Sales Order - Cube | SD-ANA | Cube | 177 |
| I_SALESANALYTICSCUBE_1 | Sales Volume and Open Sales - Cube | SD-ANA | Cube | 150 |
| I_CUSTOMERRETURNITEMCUBE_2 | Customer Return Item - Cube | SD-ANA | Cube | 125 |
| I_SLSPERFORMANCEPLANACTUALCUBE | Planned and Actual Sales Perf – Cube | SD-ANA-SP | Cube | 116 |
| I_CUSTOMERRETURNRATECUBE | Customer Return Rate - Cube | SD-ANA | Cube | 111 |
| I_CREDITMEMOREQUESTITEMCUBE | Credit Memo Request Item - Cube | SD-ANA | Cube | 103 |
| I_DEBITMEMOREQUESTITEMCUBE | Debit Memo Request Item - Cube | SD-ANA | Cube | 103 |
| I_SALESSCHEDGAGRMTITEMCUBE | Sales Scheduling Agreement Item - Cube | SD-ANA | Cube | 76 |
| I_SLSPRCGCONDITIONRECORD | Condition Record for Pricing in Sales | SD-MD-CM |  | 66 |
| I_SLSPRCGCNDNRECDSUPLMNT | Condition Supplement for Pricing in Sales | SD-MD-CM |  | 58 |
| I_PURGPRCGCONDITIONRECORD | Condition Record for Pricing in Purchasing | SD-MD-CM |  | 55 |
| I_PURGPRCGCNDNRECDSUPLMNT | Condition Supplement for Pricing in Purchasing | SD-MD-CM |  | 50 |
| I_SALESCONTRACTITEMFLFMTCUBE | Sales Contract Fulfillment Rate - Cube | SD-ANA | Cube | 48 |
| I_SLSQTANCONVERSIONRATECUBE | Sales Quotation Conversion Rate - Cube | SD-ANA | Cube | 47 |
| I_PRICINGCONDITIONTYPE | Pricing Condition Type | SD-MD-CM |  | 45 |
| I_CREDITBLOCKEDSALESDOCUMENT | Credit Blocked Sales Document | SD-BF-CM |  | 44 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Sales Organization | 22 |
| ORG | Distribution Channel | 21 |
| ORG | Sales Office | 20 |
| MASTER | Customer | 18 |
| ORG | Sales Group | 18 |
| ORG | Division | 17 |
| MASTER | Material / Product | 14 |
| CONFIG | Payment Terms | 14 |
| CONFIG | Sales Document Type | 13 |
| ORG | Business Area | 10 |
| ORG | Shipping Point | 7 |
| ORG | Profit Center | 7 |
| MASTER | Material Group | 6 |
| DOC | Sales Document | 6 |
| ORG | Controlling Area | 5 |
| MASTER | Cost Center | 5 |
| CONFIG | Fiscal Year | 5 |
| ORG | Storage Location | 4 |
| CONFIG | Incoterms | 4 |
| DOC | SD/LE Document (generic VBELN) | 4 |
| DOC | Order (production / maintenance / internal) | 3 |
| DOC | Delivery | 2 |
| MASTER | Batch | 2 |
| MASTER | Profitability Segment | 2 |
| MASTER | WBS Element | 2 |
| MASTER | Address | 2 |
| MASTER | Business Partner | 2 |
| MASTER | Personnel | 2 |
| MASTER | Supplier | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LE | 3 | 8 | 10 | Delivery, Order (production / maintenance / internal), SD/LE Document (generic VBELN), Batch, Cost Center, Customer, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| SD-SLS_Sales | 2 | 11 | 10 | Order (production / maintenance / internal), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 11 | 4 | Delivery, Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FI_other | 2 | 9 | 6 | Order (production / maintenance / internal), Sales Document, Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| LO_other | 2 | 7 | 7 | Delivery, Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, Material / Product, Personnel, Supplier |
| FI-GL_General-Ledger | 2 | 7 | 6 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| MM-IM_Inventory-Management | 2 | 7 | 3 | Delivery, Order (production / maintenance / internal), Batch, Cost Center, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| PP_other | 2 | 6 | 4 | Delivery, Order (production / maintenance / internal), Address, Batch, Material / Product, Material Group, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
