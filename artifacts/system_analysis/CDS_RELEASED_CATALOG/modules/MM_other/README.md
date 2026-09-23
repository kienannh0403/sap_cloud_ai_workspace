# MM_other

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `MM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**85 view** · data category: (none) 58, Dimension 26, Fact 1 · loại: basic 45, dimension 26, text 13, fact 1 · 2 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| MM | 60 | top-level |
| MM-IV-INT-WF | 1 | top-level |
| MM-IV-LIV | 24 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SUPPLIERINVOICEAPI01 | Supplier Invoice | MM-IV-LIV |  | 91 |
| I_SUPLRINVCITMACCTASSGMTAPI01 | Account Assignment for Supplier Invoice | MM-IV-LIV |  | 49 |
| I_SUPLRINVOICEITEMGLACCTAPI01 | G/L Account Item of Supplier Invoice | MM-IV-LIV |  | 49 |
| I_SUPLRINVCITEMPURORDREFAPI01 | Purchase Order Ref of Supplier Invoice | MM-IV-LIV |  | 42 |
| I_SUPCSGNMTPPLINEWTHDRWLAPI01 | Consignment and Pipeline Withdrawal of Supplier | MM-IV-LIV |  | 25 |
| I_SUPLRINVCITEMASSETAPI01 | Asset Item of Supplier Invoice | MM-IV-LIV |  | 24 |
| I_SUPLRINVCITEMCSGNMTAPI01 | Consignment Settlement Item | MM-IV-LIV |  | 23 |
| I_SUPLRINVCWRKFLWEMLDEADLINE | Supplier Invoice Details for Workflow Deadline Email | MM-IV-INT-WF |  | 22 |
| I_SUPLRINVCITEMMATERIALAPI01 | Material Item of Supplier Invoice | MM-IV-LIV |  | 21 |
| I_PURGOBJITEMTXTOBJOUTPRLVNCE | Output Relevance of Purchasing Itm Notes | MM |  | 16 |
| I_PURORDCHANGEDOCUMENTITEM | Purchase Order Change Document Items | MM |  | 16 |
| I_SUPPLIERINVOICETAXAPI01 | Tax for Supplier Invoice | MM-IV-LIV |  | 14 |
| I_PURGOBJTEXTOBJECTOUTPRLVNCE | Output Relevance of Purchasing Notes | MM |  | 13 |
| I_SUPLRINVCCHGDOCITMAPI01 | Change Document Items for Supplier Invoices | MM-IV-LIV |  | 13 |
| I_PURCHASEORDERCHANGEDOCUMENT | Purchase Order Change Document | MM |  | 10 |
| I_SUPLRINVCCHGDOCAPI01 | Change Documents for Supplier Invoices | MM-IV-LIV |  | 10 |
| I_SUPPLIERINVOICEBLOCKAPI01 | Supplier Invoice Block Logistics | MM-IV-LIV |  | 10 |
| I_PURCHASINGDOCUMENTTYPE | Purchasing Document Type | MM | Dimension | 9 |
| I_SUPLRINVCHEADERWHLDGTAXAPI01 | Withholding Tax for Supplier Invoice | MM-IV-LIV |  | 9 |
| I_SUPPLIERINVOICEUPLOADAPI01 | Supplier Invoice Upload | MM-IV-LIV |  | 9 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| CONFIG | Fiscal Year | 17 |
| ORG | Company Code | 11 |
| CONFIG | Tax Code | 7 |
| ORG | Plant | 6 |
| ORG | Profit Center | 5 |
| ORG | Business Area | 4 |
| MASTER | Material / Product | 4 |
| MASTER | G/L Account | 4 |
| ORG | Purchasing Organization | 3 |
| MASTER | Fixed Asset | 2 |
| DOC | Purchasing Document | 2 |
| MASTER | Supplier | 2 |
| MASTER | Activity Type | 2 |
| ORG | Controlling Area | 2 |
| MASTER | Cost Center | 2 |
| ORG | Functional Area | 2 |
| MASTER | Grant | 2 |
| DOC | Order (production / maintenance / internal) | 2 |
| MASTER | Personnel | 2 |
| DOC | SD/LE Document (generic VBELN) | 2 |
| MASTER | WBS Element | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| MM-PUR_Purchasing | 2 | 9 | 7 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| LE | 2 | 5 | 5 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| MM-IM_Inventory-Management | 2 | 5 | 4 | Order (production / maintenance / internal), Purchasing Document, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| SD_other | 2 | 5 | 3 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Cost Center, Material / Product, Personnel, Supplier, WBS Element |
| PP_other | 2 | 4 | 7 | Order (production / maintenance / internal), Purchasing Document, G/L Account, Material / Product, Supplier, WBS Element |
| FI-GL_General-Ledger | 1 | 9 | 6 | Order (production / maintenance / internal), Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| FI_other | 1 | 6 | 6 | Order (production / maintenance / internal), Cost Center, G/L Account, Material / Product, Personnel, Supplier, WBS Element |
| SD-SLS_Sales | 1 | 5 | 4 | Order (production / maintenance / internal), Cost Center, Material / Product, Personnel, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
