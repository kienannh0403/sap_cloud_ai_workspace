# SD-SLS_Sales — Sales

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `SD-SLS` = **Sales**.

**191 view** · data category: (none) 100, Dimension 91 · loại: dimension 91, basic 75, text 19, value_help 6 · 16 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SD-SLS | 16 | component |
| SD-SLS-CMR | 16 | component |
| SD-SLS-GF | 86 | component |
| SD-SLS-OA-CCO | 17 | component |
| SD-SLS-OA-SCH | 9 | component |
| SD-SLS-PBS | 5 | component |
| SD-SLS-QUT | 11 | component |
| SD-SLS-RE | 6 | component |
| SD-SLS-SO | 25 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SALESDOCUMENTITEM | Sales Document Item | SD-SLS | Dimension | 442 |
| I_SALESORDERITEM | Sales Order Item | SD-SLS-SO | Dimension | 353 |
| I_SALESDOCUMENT | Sales Document | SD-SLS | Dimension | 297 |
| I_SALESORDERWITHOUTCHARGEITEM | Item for Sales Order Without Charge | SD-SLS-SO | Dimension | 297 |
| I_CUSTOMERRETURNITEMENHANCED | Returns Order Item Enhanced | SD-SLS-RE | Dimension | 292 |
| I_SALESCONTRACTITEM | Sales Contract Item | SD-SLS-OA-CCO | Dimension | 291 |
| I_CUSTOMERRETURNITEM | Returns Order Item | SD-SLS-RE | Dimension | 275 |
| I_SALESQUOTATIONITEM | Sales Quotation Item | SD-SLS-QUT | Dimension | 259 |
| I_SALESORDER | Sales Order | SD-SLS-SO | Dimension | 247 |
| I_CREDITMEMOREQUESTITEM | Credit Memo Request Item | SD-SLS-CMR | Dimension | 236 |
| I_DEBITMEMOREQUESTITEM | Debit Memo Request Item | SD-SLS-CMR | Dimension | 234 |
| I_SALESSCHEDGAGRMTITEM | Sales Scheduling Agreement Item | SD-SLS-OA-SCH | Dimension | 228 |
| I_SALESCONTRACT | Sales Contract | SD-SLS-OA-CCO | Dimension | 208 |
| I_SALESINQUIRYITEM | Sales Inquiry Item | SD-SLS-QUT | Dimension | 207 |
| I_SALESORDERWITHOUTCHARGE | Sales Order Without Charge | SD-SLS-SO | Dimension | 200 |
| I_CUSTOMERRETURNENHANCED | Returns Order Enhanced | SD-SLS-RE | Dimension | 195 |
| I_CUSTOMERRETURN | Returns Order | SD-SLS-RE | Dimension | 187 |
| I_SALESQUOTATION | Sales Quotation | SD-SLS-QUT | Dimension | 183 |
| I_CREDITMEMOREQUEST | Credit Memo Request | SD-SLS-CMR | Dimension | 171 |
| I_DEBITMEMOREQUEST | Debit Memo Request | SD-SLS-CMR | Dimension | 170 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Distribution Channel | 45 |
| ORG | Division | 45 |
| ORG | Sales Organization | 45 |
| MASTER | Customer | 37 |
| DOC | Sales Document | 30 |
| CONFIG | Payment Terms | 26 |
| DOC | Order (production / maintenance / internal) | 25 |
| CONFIG | Fiscal Year | 22 |
| CONFIG | Incoterms | 22 |
| ORG | Sales Group | 22 |
| ORG | Sales Office | 22 |
| ORG | Business Area | 21 |
| DOC | Document Condition (pricing) | 21 |
| ORG | Controlling Area | 20 |
| CONFIG | Sales Document Type | 19 |
| MASTER | Address | 16 |
| MASTER | Business Partner | 15 |
| MASTER | Supplier | 14 |
| MASTER | Personnel | 13 |
| MASTER | Material / Product | 12 |
| ORG | Profit Center | 12 |
| MASTER | WBS Element | 12 |
| CONFIG | Tax Code | 11 |
| MASTER | Batch | 11 |
| MASTER | Material Group | 11 |
| MASTER | Profitability Segment | 11 |
| MASTER | Cost Center | 10 |
| ORG | Shipping Point | 8 |
| ORG | Storage Location | 8 |
| CONFIG | Movement Type | 5 |
| ORG | Plant | 3 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD_other | 2 | 11 | 10 | Order (production / maintenance / internal), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 11 | 5 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FI_other | 2 | 9 | 7 | Order (production / maintenance / internal), Sales Document, Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| LE | 2 | 8 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Batch, Cost Center, Customer, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| LO_other | 2 | 7 | 8 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, Material / Product, Personnel, Supplier |
| FI-GL_General-Ledger | 2 | 7 | 7 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| PM_other | 2 | 2 | 3 | Order (production / maintenance / internal), Sales Document, Material / Product, WBS Element |
| MM-IM_Inventory-Management | 1 | 7 | 4 | Order (production / maintenance / internal), Batch, Cost Center, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
