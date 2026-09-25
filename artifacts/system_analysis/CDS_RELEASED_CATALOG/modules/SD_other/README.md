# SD_other

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `SD` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**267 view** · data category: (none) 215, Dimension 38, Cube 14 · loại: basic 132, text 81, dimension 38, cube 14, value_help 2 · 11 view có field DEPRECATED/DECOMMISSIONED · 68 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SD-ANA-2CL | 27 | top-level |
| SD-ANA-SP-2CL | 8 | top-level |
| SD-BF | 2 | top-level |
| SD-BF-ACT-2CL | 2 | top-level |
| SD-BF-CM-2CL | 24 | top-level |
| SD-BF-MD-2CL | 18 | top-level |
| SD-BF-PD-2CL | 4 | top-level |
| SD-BF-PR-2CL | 39 | top-level |
| SD-BF-TX-2CL | 2 | top-level |
| SD-CRF-2CL | 2 | top-level |
| SD-CRF-ORG-2CL | 16 | top-level |
| SD-MD-AM-CMI-2CL | 2 | top-level |
| SD-MD-CM-2CL | 74 | top-level |
| SD-MD-MM-2CL | 44 | top-level |
| SD-MD-MM-DET-2CL | 2 | top-level |
| SD-MD-MM-LIS-2CL | 1 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SLSORDCONFANALYTICSCUBE | Confirmation of Sales Orders - Cube | SD-ANA-2CL | Cube | 383 |
| I_SALESORDERITEMCUBE | Sales Order Item - Cube | SD-ANA-2CL | Cube | 378 |
| I_BILLINGDOCUMENTITEMCUBE | Sales Volume - Cube | SD-ANA-2CL |  | 338 |
| I_SALESQUOTATIONITEMCUBE_2 | Sales Quotation Item - Cube | SD-ANA-2CL | Cube | 237 |
| I_SALESCONTRACTITEMCUBE | Sales Contract Item - Cube | SD-ANA-2CL | Cube | 213 |
| C_SALESDOCUMENTITEMDEX_1 | Data Extraction for Sales Document Item | SD-ANA-2CL |  | 191 |
| I_SALESORDERCUBE | Sales Order - Cube | SD-ANA-2CL | Cube | 177 |
| I_SALESANALYTICSCUBE_1 | Sales Volume and Open Sales - Cube | SD-ANA-2CL | Cube | 150 |
| I_CUSTOMERRETURNITEMCUBE_2 | Customer Return Item - Cube | SD-ANA-2CL | Cube | 125 |
| I_SLSPERFORMANCEPLANACTUALCUBE | Planned and Actual Sales Perf – Cube | SD-ANA-SP-2CL | Cube | 116 |
| I_CUSTOMERRETURNRATECUBE | Customer Return Rate - Cube | SD-ANA-2CL | Cube | 111 |
| C_SALESDOCUMENTSCHEDLINEDEX_1 | Data Extraction for Sales Document Schedule Lines | SD-ANA-2CL |  | 107 |
| I_CREDITMEMOREQUESTITEMCUBE | Credit Memo Request Item - Cube | SD-ANA-2CL | Cube | 103 |
| I_DEBITMEMOREQUESTITEMCUBE | Debit Memo Request Item - Cube | SD-ANA-2CL | Cube | 103 |
| C_SALESDOCITMPRCGELMNTDEX_1 | Data Extraction for Sales Doc Item Pricing Elements | SD-ANA-2CL |  | 91 |
| I_SALESSCHEDGAGRMTITEMCUBE | Sales Scheduling Agreement Item - Cube | SD-ANA-2CL | Cube | 76 |
| I_BILLGITMPRCGELFORCOTYPC | Billing Document Item Pricing Element - Cube | SD-ANA-2CL |  | 67 |
| I_SLSPRCGCONDITIONRECORD | Condition Record for Pricing in Sales | SD-MD-CM-2CL |  | 66 |
| I_SLSMATLLSTGOREXCLSNRECORD | Sales Material Listing Exclusion Record | SD-MD-MM-LIS-2CL |  | 63 |
| I_BILLGITMPRCGELFORCOTYPAN | Billing Document Item Pricing Element Analytics | SD-ANA-2CL |  | 60 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Sales Organization | 33 |
| ORG | Distribution Channel | 30 |
| ORG | Division | 27 |
| ORG | Sales Office | 27 |
| MASTER | Customer | 25 |
| MASTER | Material / Product | 23 |
| ORG | Sales Group | 22 |
| CONFIG | Sales Document Type | 19 |
| CONFIG | Payment Terms | 16 |
| ORG | Business Area | 12 |
| DOC | Sales Document | 11 |
| CONFIG | Incoterms | 10 |
| MASTER | Material Group | 10 |
| ORG | Shipping Point | 10 |
| ORG | Profit Center | 9 |
| ORG | Controlling Area | 8 |
| CONFIG | Fiscal Year | 8 |
| MASTER | Cost Center | 7 |
| MASTER | Batch | 7 |
| ORG | Storage Location | 7 |
| DOC | Order (production / maintenance / internal) | 5 |
| MASTER | Profitability Segment | 4 |
| MASTER | WBS Element | 4 |
| DOC | Billing Document | 4 |
| ORG | Company Code | 4 |
| ORG | Plant | 4 |
| DOC | SD/LE Document (generic VBELN) | 4 |
| DOC | Document Condition (pricing) | 3 |
| DOC | Delivery | 2 |
| MASTER | Address | 2 |
| MASTER | Business Partner | 2 |
| MASTER | Personnel | 2 |
| MASTER | Supplier | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD-BIL_Billing | 5 | 11 | 12 | Billing Document, Document Condition (pricing), Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| LE | 4 | 8 | 11 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), SD/LE Document (generic VBELN), Batch, Cost Center, Customer, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| SD-SLS_Sales | 3 | 11 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FI_other | 3 | 11 | 8 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| MM-PUR_Purchasing | 3 | 11 | 6 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| LO_other | 3 | 7 | 9 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, Material / Product, Personnel, Supplier |
| CO_other | 3 | 5 | 10 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| CA | 2 | 8 | 5 | Billing Document, Order (production / maintenance / internal), Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
