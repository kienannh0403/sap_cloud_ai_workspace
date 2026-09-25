# LO_other

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `LO` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**330 view** · data category: (none) 263, Dimension 66, Fact 1 · loại: basic 184, dimension 64, text 55, value_help 26, fact 1 · 15 view có field DEPRECATED/DECOMMISSIONED · 170 view mới so với file xlsx của user · 1 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| LO-AB | 68 | top-level |
| LO-ARM-2CL | 17 | top-level |
| LO-ARM-INS-2CL | 2 | top-level |
| LO-BM-MD-2CL | 12 | top-level |
| LO-GT-CHB | 22 | top-level |
| LO-HU-2CL | 25 | top-level |
| LO-HU-API-2CL | 6 | top-level |
| LO-MD-BP-2CL | 61 | top-level |
| LO-MD-BP-CM-2CL | 3 | top-level |
| LO-MD-PL-2CL | 4 | top-level |
| LO-MD-SN-2CL | 16 | top-level |
| LO-RFM-CA-SE-2CL | 7 | top-level |
| LO-RFM-MD-ART-2CL | 5 | top-level |
| LO-RFM-MD-MC-2CL | 11 | top-level |
| LO-RFM-STO-FIO-2CL | 2 | top-level |
| LO-VCH-API-2CL | 37 | top-level |
| LO-WTY | 2 | top-level |
| LO-WTY-FIO-2CL | 30 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SETTLMTDOC | Settlement Document | LO-AB | Dimension | 240 |
| I_SETTLMTDOCITEM | Settlement Document Item | LO-AB | Dimension | 238 |
| I_SUPPLIER | Supplier | LO-MD-BP-2CL | Dimension | 157 |
| C_SETTLMTDOCEDP | Settlement Document Email Data Provider | LO-AB |  | 141 |
| I_CUSTOMER | Customer | LO-MD-BP-2CL | Dimension | 131 |
| I_CONDITIONCONTRACT | Condition Contract | LO-GT-CHB | Dimension | 121 |
| I_CNDNCONTRBUSVOLSELCRITERIA | Condition Contract Bus Vol Sel Critra | LO-GT-CHB | Dimension | 120 |
| I_FRTCOSTALLOCITM | Freight Cost Allocation Document Item | LO-AB |  | 113 |
| I_PERSSETTLMTDOC | Personnel Settlement Document | LO-AB |  | 101 |
| I_BUSINESSPARTNERCUSTOMER | Business Partner Customer | LO-MD-BP-2CL | Dimension | 97 |
| I_CUSTOMERSALESAREA | Customer Sales Area | LO-MD-BP-2CL | Dimension | 92 |
| I_PERSSETTLMTDOCITEM | Personnel Settlement Document Item | LO-AB |  | 89 |
| I_HANDLINGUNITHEADER | Handling Unit Header | LO-HU-2CL |  | 83 |
| I_SUPPLIERCOMPANY | Supplier Company | LO-MD-BP-2CL | Fact | 78 |
| I_CUSTOMERCOMPANY | Customer Company | LO-MD-BP-2CL | Dimension | 76 |
| I_SETTLMTDOCITMCUSTPRCGELMNT | Settlmt Doc Item Cust Pricing Element | LO-AB |  | 70 |
| I_SETTLMTDOCITMSUPLRPRCGELMNT | Settlmt Doc Item Suplr Pricing Element | LO-AB |  | 70 |
| I_FRTCOSTALLOCDOC | Freight Cost Allocation Document | LO-AB |  | 68 |
| I_FRTCOSTALLOCITMPRCGELMNT | Frt Cost Allocation Item Pricing Element | LO-AB |  | 67 |
| I_BUSINESSPARTNERSUPPLIER | Business Partner Supplier | LO-MD-BP-2CL | Dimension | 67 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Material / Product | 38 |
| MASTER | Customer | 29 |
| MASTER | Supplier | 27 |
| ORG | Plant | 24 |
| ORG | Sales Organization | 18 |
| ORG | Company Code | 18 |
| ORG | Division | 16 |
| ORG | Distribution Channel | 15 |
| ORG | Purchasing Organization | 12 |
| MASTER | Equipment | 11 |
| ORG | Sales Group | 8 |
| ORG | Sales Office | 8 |
| MASTER | Batch | 8 |
| MASTER | Personnel | 7 |
| MASTER | Business Partner | 7 |
| CONFIG | Incoterms | 5 |
| ORG | Storage Location | 5 |
| CONFIG | Payment Terms | 5 |
| MASTER | G/L Account | 4 |
| CONFIG | Tax Code | 4 |
| ORG | Controlling Area | 3 |
| DOC | Delivery | 3 |
| DOC | Document Condition (pricing) | 3 |
| MASTER | Address | 2 |
| DOC | Inspection Lot | 2 |
| ORG | Valuation Area | 2 |
| DOC | Order (production / maintenance / internal) | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LE | 4 | 5 | 8 | Delivery, Document Condition (pricing), Inspection Lot, Order (production / maintenance / internal), Batch, Customer, G/L Account, Material / Product, Supplier |
| MM-PUR_Purchasing | 3 | 8 | 5 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |
| SD_other | 3 | 7 | 9 | Delivery, Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, Material / Product, Personnel, Supplier |
| PP_other | 3 | 6 | 5 | Delivery, Inspection Lot, Order (production / maintenance / internal), Address, Batch, Equipment, G/L Account, Material / Product, Supplier |
| SD-BIL_Billing | 2 | 8 | 9 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |
| SD-SLS_Sales | 2 | 7 | 8 | Document Condition (pricing), Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, Material / Product, Personnel, Supplier |
| MM-IM_Inventory-Management | 2 | 4 | 5 | Delivery, Order (production / maintenance / internal), Batch, G/L Account, Material / Product, Supplier |
| FI_other | 1 | 8 | 7 | Order (production / maintenance / internal), Address, Batch, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
