# SD-SLS_Sales — Sales

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `SD-SLS` = **Sales**.

**363 view** · data category: (none) 272, Dimension 91 · loại: basic 225, dimension 91, text 41, value_help 6 · 16 view có field DEPRECATED/DECOMMISSIONED · 172 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SD-SLS-2CL | 19 | component |
| SD-SLS-API-2CL | 9 | component |
| SD-SLS-CMR-2CL | 61 | component |
| SD-SLS-GF-2CL | 102 | component |
| SD-SLS-GF-BET-2CL | 6 | component |
| SD-SLS-OA-2CL | 8 | component |
| SD-SLS-OA-CCO-2CL | 25 | component |
| SD-SLS-OA-SCH-2CL | 30 | component |
| SD-SLS-PBS | 5 | component |
| SD-SLS-PH-2CL | 3 | component |
| SD-SLS-QUT-2CL | 30 | component |
| SD-SLS-RE-2CL | 24 | component |
| SD-SLS-SO-2CL | 30 | component |
| SD-SLS-SO-RAP-2CL | 11 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SALESDOCUMENTITEM | Sales Document Item | SD-SLS-2CL | Dimension | 442 |
| I_SALESORDERITEM | Sales Order Item | SD-SLS-SO-2CL | Dimension | 353 |
| I_SALESDOCUMENT | Sales Document | SD-SLS-2CL | Dimension | 297 |
| I_SALESORDERWITHOUTCHARGEITEM | Item for Sales Order Without Charge | SD-SLS-SO-2CL | Dimension | 297 |
| I_CUSTOMERRETURNITEMENHANCED | Returns Order Item Enhanced | SD-SLS-RE-2CL | Dimension | 292 |
| I_SALESCONTRACTITEM | Sales Contract Item | SD-SLS-OA-CCO-2CL | Dimension | 291 |
| I_CUSTOMERRETURNITEM | Returns Order Item | SD-SLS-RE-2CL | Dimension | 275 |
| I_SALESQUOTATIONITEM | Sales Quotation Item | SD-SLS-QUT-2CL | Dimension | 259 |
| I_SALESORDER | Sales Order | SD-SLS-SO-2CL | Dimension | 247 |
| I_CREDITMEMOREQUESTITEM | Credit Memo Request Item | SD-SLS-CMR-2CL | Dimension | 236 |
| I_DEBITMEMOREQUESTITEM | Debit Memo Request Item | SD-SLS-CMR-2CL | Dimension | 234 |
| I_SALESSCHEDGAGRMTITEM | Sales Scheduling Agreement Item | SD-SLS-OA-SCH-2CL | Dimension | 228 |
| I_SALESCONTRACT | Sales Contract | SD-SLS-OA-CCO-2CL | Dimension | 208 |
| I_SALESINQUIRYITEM | Sales Inquiry Item | SD-SLS-QUT-2CL | Dimension | 207 |
| I_SALESORDERWITHOUTCHARGE | Sales Order Without Charge | SD-SLS-SO-2CL | Dimension | 200 |
| I_CUSTOMERRETURNENHANCED | Returns Order Enhanced | SD-SLS-RE-2CL | Dimension | 195 |
| I_CUSTOMERRETURN | Returns Order | SD-SLS-RE-2CL | Dimension | 187 |
| I_SALESQUOTATION | Sales Quotation | SD-SLS-QUT-2CL | Dimension | 183 |
| I_CREDITMEMOREQUEST | Credit Memo Request | SD-SLS-CMR-2CL | Dimension | 171 |
| I_DEBITMEMOREQUEST | Debit Memo Request | SD-SLS-CMR-2CL | Dimension | 170 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Distribution Channel | 47 |
| ORG | Sales Organization | 47 |
| ORG | Division | 46 |
| MASTER | Customer | 37 |
| DOC | Sales Document | 30 |
| CONFIG | Payment Terms | 26 |
| DOC | Order (production / maintenance / internal) | 25 |
| CONFIG | Sales Document Type | 24 |
| CONFIG | Fiscal Year | 22 |
| CONFIG | Incoterms | 22 |
| ORG | Sales Group | 22 |
| ORG | Sales Office | 22 |
| ORG | Business Area | 21 |
| DOC | Document Condition (pricing) | 21 |
| ORG | Controlling Area | 20 |
| MASTER | Address | 16 |
| MASTER | Business Partner | 15 |
| MASTER | Supplier | 14 |
| CONFIG | Tax Code | 13 |
| MASTER | Personnel | 13 |
| MASTER | Material / Product | 12 |
| ORG | Profit Center | 12 |
| MASTER | WBS Element | 12 |
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
| SD-BIL_Billing | 3 | 11 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| SD_other | 3 | 11 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FI_other | 2 | 11 | 7 | Order (production / maintenance / internal), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 11 | 5 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| LE | 2 | 8 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Batch, Cost Center, Customer, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| LO_other | 2 | 7 | 8 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, Material / Product, Personnel, Supplier |
| FIN | 2 | 7 | 7 | Order (production / maintenance / internal), Sales Document, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |
| FI-GL_General-Ledger | 2 | 7 | 6 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
