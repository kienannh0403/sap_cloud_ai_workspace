# SD-BIL_Billing — Billing

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `SD-BIL` = **Billing**.

**34 view** · data category: (none) 20, Dimension 14 · loại: dimension 14, basic 10, text 7, value_help 3 · 4 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SD-BIL-GF | 16 | component |
| SD-BIL-IL | 3 | component |
| SD-BIL-IV-BP | 4 | component |
| SD-BIL-IV-PC | 3 | component |
| SD-BIL-PBD | 8 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PRELIMBILLINGDOCUMENTITEM | Preliminary Billing Document Item | SD-BIL-PBD | Dimension | 291 |
| I_PRELIMBILLINGDOCUMENT | Preliminary Billing Document | SD-BIL-PBD | Dimension | 135 |
| I_PRELIMBILLGDOCITEMPRCGELMNT | Prelim Billg Doc Item Pricing Element | SD-BIL-PBD |  | 75 |
| I_PRELIMBILLINGDOCPRCGELMNT | Prelim Billing Document Pricing Element | SD-BIL-PBD |  | 69 |
| I_SLSDOCPAYMENTPLANITEMDETAILS | Sales Document Payment Plan Item Details | SD-BIL-IV-PC |  | 55 |
| I_SDBILLINGPLANITEM | Billing Plan Item for SD Documents | SD-BIL-IV-BP | Dimension | 43 |
| I_CUSTPROJSLSORDITMBILLGPLNITM | Billing Plan Item of Sales Order Item for Customer Project | SD-BIL-IV-BP |  | 32 |
| I_PRELIMBILLINGDOCPARTNER | Preliminary Billing Document Partner | SD-BIL-PBD |  | 18 |
| I_SDBILLINGPLAN | Billing Plan for SD Documents | SD-BIL-IV-BP | Dimension | 17 |
| I_CUSTPROJSLSORDITMBILLGPLN | Billing Plan of Sales Order Item for Customer Project | SD-BIL-IV-BP |  | 14 |
| I_PRELIMBILLINGDOCITEMPARTNER | Preliminary Billing Document Item Partner | SD-BIL-PBD |  | 14 |
| I_INVOICELISTTYPE | Invoice List Type | SD-BIL-IL | Dimension | 7 |
| I_CUSTOMERACCOUNTASSGMTGROUPT | Account Assignment Group of Customer - Text | SD-BIL-GF |  | 5 |
| I_OVERALLBILLINGBLOCKSTATUST | Overall Billing Block Status - Text | SD-BIL-GF |  | 5 |
| I_SDDOCUMENTPAYMENTCARDTYPET | SD Document Payment Card Type - Text | SD-BIL-IV-PC |  | 5 |
| I_INCOTERMSCLASSIFICATION | Incoterms Classification | SD-BIL-GF | Dimension | 3 |
| I_OVERALLBILLINGBLOCKSTATUS | Overall Billing Block Status | SD-BIL-GF | Dimension | 3 |
| I_OVERALLBILLINGSTATUS | Overall Billing Status | SD-BIL-GF | Dimension | 3 |
| I_OVRLBILLINGDOCREQSTATUS | Overall Billing Document Request Status | SD-BIL-GF | Dimension | 3 |
| I_PRELIMBILLGDOCSTATUS | Preliminary Billing Document Status | SD-BIL-GF | Dimension | 3 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Sales Organization | 7 |
| ORG | Distribution Channel | 5 |
| ORG | Division | 5 |
| DOC | Sales Document | 4 |
| MASTER | Customer | 4 |
| CONFIG | Incoterms | 3 |
| CONFIG | Tax Code | 3 |
| CONFIG | Payment Terms | 2 |
| MASTER | G/L Account | 2 |
| MASTER | Address | 2 |
| MASTER | Personnel | 2 |
| MASTER | Supplier | 2 |
| ORG | Company Code | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI_other | 1 | 5 | 4 | Sales Document, Address, Customer, G/L Account, Personnel, Supplier |
| FI-GL_General-Ledger | 1 | 4 | 4 | Sales Document, Customer, G/L Account, Personnel, Supplier |
| SD-SLS_Sales | 1 | 4 | 3 | Sales Document, Address, Customer, Personnel, Supplier |
| SD_other | 1 | 4 | 3 | Sales Document, Address, Customer, Personnel, Supplier |
| PSM | 1 | 3 | 3 | Sales Document, Customer, G/L Account, Personnel |
| PS_Project-System | 1 | 0 | 1 | Sales Document |
| PM_other | 1 | 0 | 0 | Sales Document |
| LO_other | 0 | 5 | 4 | Address, Customer, G/L Account, Personnel, Supplier |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
