# LO_other

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `LO` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**158 view** · data category: (none) 92, Dimension 65, Fact 1 · loại: dimension 63, basic 52, text 30, value_help 12, fact 1 · 14 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| LO-AB | 33 | top-level |
| LO-ARM | 11 | top-level |
| LO-ARM-INS | 2 | top-level |
| LO-GT-CHB | 9 | top-level |
| LO-HU | 4 | top-level |
| LO-MD-BP | 48 | top-level |
| LO-MD-PL | 4 | top-level |
| LO-MD-SN | 14 | top-level |
| LO-RFM-MD-ART | 1 | top-level |
| LO-WTY-FIO | 32 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SETTLMTDOC | Settlement Document | LO-AB | Dimension | 240 |
| I_SETTLMTDOCITEM | Settlement Document Item | LO-AB | Dimension | 238 |
| I_SUPPLIER | Supplier | LO-MD-BP | Dimension | 157 |
| I_CUSTOMER | Customer | LO-MD-BP | Dimension | 131 |
| I_CONDITIONCONTRACT | Condition Contract | LO-GT-CHB | Dimension | 121 |
| I_CNDNCONTRBUSVOLSELCRITERIA | Condition Contract Bus Vol Sel Critra | LO-GT-CHB | Dimension | 120 |
| I_FRTCOSTALLOCITM | Freight Cost Allocation Document Item | LO-AB |  | 113 |
| I_PERSSETTLMTDOC | Personnel Settlement Document | LO-AB |  | 101 |
| I_BUSINESSPARTNERCUSTOMER | Business Partner Customer | LO-MD-BP | Dimension | 97 |
| I_CUSTOMERSALESAREA | Customer Sales Area | LO-MD-BP | Dimension | 92 |
| I_PERSSETTLMTDOCITEM | Personnel Settlement Document Item | LO-AB |  | 89 |
| I_HANDLINGUNITHEADER | Handling Unit Header | LO-HU |  | 83 |
| I_SUPPLIERCOMPANY | Supplier Company | LO-MD-BP | Fact | 78 |
| I_CUSTOMERCOMPANY | Customer Company | LO-MD-BP | Dimension | 76 |
| I_SETTLMTDOCITMCUSTPRCGELMNT | Settlmt Doc Item Cust Pricing Element | LO-AB |  | 70 |
| I_SETTLMTDOCITMSUPLRPRCGELMNT | Settlmt Doc Item Suplr Pricing Element | LO-AB |  | 70 |
| I_FRTCOSTALLOCDOC | Freight Cost Allocation Document | LO-AB |  | 68 |
| I_FRTCOSTALLOCITMPRCGELMNT | Frt Cost Allocation Item Pricing Element | LO-AB |  | 67 |
| I_BUSINESSPARTNERSUPPLIER | Business Partner Supplier | LO-MD-BP | Dimension | 67 |
| I_SETTLMTDOCCUSTPRCGELMNT | Settlmt Doc Customer Pricing Element | LO-AB |  | 66 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Customer | 26 |
| MASTER | Supplier | 21 |
| MASTER | Material / Product | 17 |
| ORG | Company Code | 15 |
| ORG | Sales Organization | 13 |
| ORG | Division | 12 |
| MASTER | Equipment | 11 |
| ORG | Distribution Channel | 10 |
| ORG | Plant | 10 |
| ORG | Purchasing Organization | 9 |
| ORG | Sales Group | 7 |
| ORG | Sales Office | 7 |
| MASTER | Personnel | 7 |
| MASTER | Business Partner | 7 |
| CONFIG | Incoterms | 5 |
| CONFIG | Payment Terms | 5 |
| MASTER | G/L Account | 4 |
| CONFIG | Tax Code | 4 |
| ORG | Controlling Area | 3 |
| ORG | Storage Location | 3 |
| DOC | Delivery | 3 |
| MASTER | Batch | 2 |
| MASTER | Address | 2 |
| DOC | Inspection Lot | 2 |
| ORG | Valuation Area | 2 |
| DOC | Order (production / maintenance / internal) | 2 |
| DOC | Document Condition (pricing) | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LE | 4 | 5 | 8 | Delivery, Document Condition (pricing), Inspection Lot, Order (production / maintenance / internal), Batch, Customer, G/L Account, Material / Product, Supplier |
| MM-PUR_Purchasing | 3 | 8 | 5 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |
| PP_other | 3 | 6 | 5 | Delivery, Inspection Lot, Order (production / maintenance / internal), Address, Batch, Equipment, G/L Account, Material / Product, Supplier |
| SD-SLS_Sales | 2 | 7 | 8 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, Material / Product, Personnel, Supplier |
| SD_other | 2 | 7 | 7 | Delivery, Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, Material / Product, Personnel, Supplier |
| MM-IM_Inventory-Management | 2 | 4 | 5 | Delivery, Order (production / maintenance / internal), Batch, G/L Account, Material / Product, Supplier |
| FI_other | 1 | 7 | 6 | Order (production / maintenance / internal), Address, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |
| FI-GL_General-Ledger | 1 | 6 | 7 | Order (production / maintenance / internal), Customer, Equipment, G/L Account, Material / Product, Personnel, Supplier |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
