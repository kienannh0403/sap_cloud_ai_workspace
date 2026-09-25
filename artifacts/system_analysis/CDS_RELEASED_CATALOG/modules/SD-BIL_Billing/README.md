# SD-BIL_Billing — Billing

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `SD-BIL` = **Billing**.

**134 view** · data category: (none) 121, Dimension 13 · loại: basic 87, text 21, value_help 13, dimension 13 · 15 view có field DEPRECATED/DECOMMISSIONED · 102 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SD-BIL-2CL | 11 | component |
| SD-BIL-BD-2CL | 30 | component |
| SD-BIL-BDR-2CL | 29 | component |
| SD-BIL-GF-2CL | 25 | component |
| SD-BIL-IL-2CL | 12 | component |
| SD-BIL-IV-BP-2CL | 14 | component |
| SD-BIL-IV-PC-2CL | 3 | component |
| SD-BIL-PBD-2CL | 10 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_BILLINGDOCUMENTITEMBASIC | Item in Billing Process Document | SD-BIL-2CL |  | 333 |
| I_BILLINGDOCUMENTITEM | Billing Document Item | SD-BIL-BD-2CL |  | 321 |
| I_PRELIMBILLINGDOCUMENTITEM | Preliminary Billing Document Item | SD-BIL-PBD-2CL | Dimension | 291 |
| I_BILLINGDOCUMENTREQUESTITEM | Billing Document Request Item | SD-BIL-BDR-2CL |  | 201 |
| I_BILLINGDOCUMENTBASIC | Billing Process Document | SD-BIL-2CL |  | 179 |
| C_BILLINGDOCITEMBASICDEX_1 | Data Extraction for Billing Doc Item Basic | SD-BIL-2CL |  | 162 |
| I_BILLINGDOCUMENT | Billing Document | SD-BIL-BD-2CL |  | 162 |
| I_PRELIMBILLINGDOCUMENT | Preliminary Billing Document | SD-BIL-PBD-2CL | Dimension | 135 |
| I_INVOICELIST | Invoice List | SD-BIL-IL-2CL |  | 131 |
| I_BILLINGDOCUMENTREQUEST | Billing Document Request | SD-BIL-BDR-2CL |  | 114 |
| C_BILLGDOCITMPRCGELMNTBSCDEX_1 | Data Extraction for Billing Doc Item Pricing Element Basic | SD-BIL-2CL |  | 86 |
| I_BILLINGDOCITEMPRCGELMNTBASIC | Item Pricing Element in Billing Process Document | SD-BIL-2CL |  | 77 |
| I_BILLINGDOCUMENTITEMPRCGELMNT | Billing Document Item Pricing Element | SD-BIL-BD-2CL |  | 77 |
| I_BILLINGDOCREQITEMPRCGELMNT | Billing Doc Req Item Pricing Element | SD-BIL-BDR-2CL |  | 76 |
| I_PRELIMBILLGDOCITEMPRCGELMNT | Prelim Billg Doc Item Pricing Element | SD-BIL-PBD-2CL |  | 75 |
| I_BILLINGDOCPRCGELMNTBASIC | Pricing Element in Billing Process Document | SD-BIL-2CL |  | 71 |
| I_BILLINGDOCUMENTPRCGELMNT | Billing Document Pricing Element | SD-BIL-BD-2CL |  | 71 |
| I_BILLINGDOCREQPRCGELMNT | Billing Document Request Pricing Element | SD-BIL-BDR-2CL |  | 70 |
| I_PRELIMBILLINGDOCPRCGELMNT | Prelim Billing Document Pricing Element | SD-BIL-PBD-2CL |  | 69 |
| I_INVOICELISTPRCGELMNT | Invoice List Pricing Element | SD-BIL-IL-2CL |  | 62 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Sales Organization | 24 |
| MASTER | Customer | 22 |
| DOC | Billing Document | 19 |
| ORG | Distribution Channel | 15 |
| ORG | Division | 15 |
| CONFIG | Tax Code | 12 |
| ORG | Company Code | 11 |
| DOC | Sales Document | 9 |
| MASTER | Address | 9 |
| MASTER | Personnel | 9 |
| MASTER | Supplier | 9 |
| DOC | Document Condition (pricing) | 8 |
| CONFIG | Incoterms | 8 |
| MASTER | Business Partner | 8 |
| MASTER | G/L Account | 8 |
| CONFIG | Payment Terms | 7 |
| ORG | Controlling Area | 6 |
| MASTER | Cost Center | 6 |
| MASTER | Material / Product | 6 |
| MASTER | Material Group | 6 |
| ORG | Sales Group | 6 |
| ORG | Sales Office | 6 |
| CONFIG | Fiscal Year | 5 |
| MASTER | Batch | 5 |
| ORG | Business Area | 5 |
| DOC | Order (production / maintenance / internal) | 5 |
| ORG | Plant | 5 |
| ORG | Profit Center | 5 |
| MASTER | Profitability Segment | 5 |
| ORG | Shipping Point | 5 |
| ORG | Storage Location | 5 |
| MASTER | WBS Element | 5 |
| DOC | SD/LE Document (generic VBELN) | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD_other | 5 | 11 | 12 | Billing Document, Document Condition (pricing), Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FI_other | 3 | 12 | 8 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, G/L Account, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| SD-SLS_Sales | 3 | 11 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| LE | 3 | 9 | 11 | Document Condition (pricing), Order (production / maintenance / internal), SD/LE Document (generic VBELN), Batch, Cost Center, Customer, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| CO_other | 3 | 6 | 10 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 12 | 6 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Cost Center, Customer, G/L Account, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| LO_other | 2 | 8 | 9 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |
| FIN | 2 | 8 | 8 | Order (production / maintenance / internal), Sales Document, Business Partner, Cost Center, Customer, G/L Account, Material / Product, Personnel, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
