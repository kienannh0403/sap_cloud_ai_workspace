# FI_other

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `FI` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**827 view** · data category: (none) 745, Dimension 70, Fact 6, Cube 6 · loại: basic 488, text 246, dimension 65, value_help 16, fact 6, cube 6 · 32 view có field DEPRECATED/DECOMMISSIONED · 364 view mới so với file xlsx của user · 2 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-BL-PT | 3 | top-level |
| FI-CA-2CL | 308 | top-level |
| FI-CA-INV-2CL | 162 | top-level |
| FI-FIO-AA-ANA-2CL | 21 | top-level |
| FI-FIO-AP-2CL | 6 | top-level |
| FI-FIO-GL-HIE-2CL | 17 | top-level |
| FI-FM | 12 | top-level |
| FI-LOC-AA | 4 | top-level |
| FI-LOC-AA-RU | 4 | top-level |
| FI-LOC-BOE | 2 | top-level |
| FI-LOC-BUP | 3 | top-level |
| FI-LOC-CIT | 14 | top-level |
| FI-LOC-CM-CN | 12 | top-level |
| FI-LOC-EPI-CN | 8 | top-level |
| FI-LOC-FI | 7 | top-level |
| FI-LOC-FI-AR-WHT | 2 | top-level |
| FI-LOC-FI-CH-QR | 1 | top-level |
| FI-LOC-FI-CL | 2 | top-level |
| FI-LOC-FI-IN | 2 | top-level |
| FI-LOC-FI-JP | 7 | top-level |
| FI-LOC-FI-JP-IVS | 1 | top-level |
| FI-LOC-FI-KR | 7 | top-level |
| FI-LOC-FI-MX | 5 | top-level |
| FI-LOC-FI-PH | 3 | top-level |
| FI-LOC-FI-RO | 1 | top-level |
| FI-LOC-FI-RU | 1 | top-level |
| FI-LOC-GAI-CN | 9 | top-level |
| FI-LOC-GEN | 1 | top-level |
| FI-LOC-LO | 1 | top-level |
| FI-LOC-LO-AE | 2 | top-level |
| FI-LOC-LO-BR | 107 | top-level |
| FI-LOC-LO-HR | 1 | top-level |
| FI-LOC-LO-IN | 7 | top-level |
| FI-LOC-ODN | 2 | top-level |
| FI-LOC-SAF-PL | 1 | top-level |
| FI-LOC-SRF-RUN | 1 | top-level |
| FI-LOC-TIM-CN | 10 | top-level |
| FI-LOC-TXS | 4 | top-level |
| FI-LOC-VAT-GEN | 3 | top-level |
| FI-RA-2CL | 51 | top-level |
| FI-TXL-EXT-2CL | 9 | top-level |
| FI-TXL-TGM | 3 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_GLACCOUNTLINEITEMSEMTAG | G/L Line Item with Semantic Tag Including FA | FI-FIO-GL-HIE-2CL | Cube | 610 |
| I_CADOCUMENTBPITEM | Document Business Partner Item | FI-CA-2CL |  | 224 |
| I_CABLLBLEITMMAINBILLED | Billable Item Main Data Billed | FI-CA-INV-2CL |  | 221 |
| I_CABLLBLEITMMAINRAWEXCPTD | Billable Item Main Data Raw Excepted | FI-CA-INV-2CL |  | 218 |
| I_BR_NFITEM | Brazil Nota Fiscal Item | FI-LOC-LO-BR |  | 218 |
| I_CABLLBLEITMMAINBLLBLEEXCPTD | Bllble Itm Main Data Billable Excepted | FI-CA-INV-2CL |  | 217 |
| I_CABLLBLEITMMAINRAW | Billable Item Main Data Raw | FI-CA-INV-2CL |  | 215 |
| I_CABLLBLEITMMAINBILLABLE | Billable Item Main Data Billable | FI-CA-INV-2CL |  | 212 |
| I_BR_NFDOCUMENT | Brazil Nota Fiscal Document Data | FI-LOC-LO-BR |  | 200 |
| I_CAOPENITEMLISTITEM | Contract Accounting Open Item List Item | FI-CA-2CL |  | 192 |
| I_CONTRACTACCOUNTPARTNER | Contract Account Partner | FI-CA-2CL | Dimension | 160 |
| I_FIXEDASSET | Fixed Asset | FI-FIO-AA-ANA-2CL | Dimension | 142 |
| I_PROVIDERCONTRACTITEM | Provider Contract Item | FI-CA-2CL |  | 141 |
| I_CAPROVIDERCONTRACTITEM | Provider Contract Item | FI-CA-2CL | Dimension | 138 |
| I_CABILLGDOCITEM | Billing Document Item | FI-CA-INV-2CL |  | 134 |
| I_CAINVCGDOCITEM | Invoicing Document Item | FI-CA-INV-2CL |  | 131 |
| I_PAYMENTRELEASELISTITEMBASIC | CN Payment Release List Item | FI-LOC-EPI-CN |  | 131 |
| I_CADOCUMENTGLITEM | Document General Ledger Item | FI-CA-2CL |  | 123 |
| I_RAPERFORMANCEOBLIGATION | RA Performance Obligation | FI-RA-2CL | Dimension | 123 |
| I_CABILLGPLNITEM | Billing Plan Item | FI-CA-INV-2CL |  | 103 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 96 |
| CONFIG | Fiscal Year | 22 |
| CONFIG | Tax Code | 21 |
| ORG | Business Area | 19 |
| ORG | Profit Center | 18 |
| MASTER | Customer | 14 |
| MASTER | Supplier | 12 |
| MASTER | Business Partner | 12 |
| ORG | Controlling Area | 11 |
| ORG | Chart of Accounts | 9 |
| MASTER | G/L Account | 9 |
| ORG | Sales Organization | 8 |
| ORG | Plant | 8 |
| MASTER | Cost Center | 7 |
| ORG | Distribution Channel | 7 |
| MASTER | WBS Element | 6 |
| ORG | Division | 6 |
| MASTER | Fixed Asset | 6 |
| MASTER | Material / Product | 6 |
| MASTER | Personnel | 5 |
| DOC | Order (production / maintenance / internal) | 5 |
| ORG | Functional Area | 5 |
| MASTER | Grant | 5 |
| ORG | Segment | 5 |
| MASTER | Activity Type | 4 |
| MASTER | Address | 3 |
| CONFIG | Payment Terms | 3 |
| DOC | Sales Document | 3 |
| MASTER | Profitability Segment | 2 |
| DOC | SD/LE Document (generic VBELN) | 2 |
| ORG | Valuation Area | 2 |
| MASTER | Material Group | 2 |
| DOC | Purchasing Document | 2 |
| CONFIG | Incoterms | 2 |
| MASTER | Batch | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO_other | 4 | 7 | 12 | Order (production / maintenance / internal), Purchasing Document, SD/LE Document (generic VBELN), Sales Document, Activity Type, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| SD-BIL_Billing | 3 | 12 | 8 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, G/L Account, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FIN | 3 | 11 | 12 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Business Partner, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| SD_other | 3 | 11 | 8 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Sales Document, Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| MM_other | 3 | 9 | 6 | Order (production / maintenance / internal), Purchasing Document, SD/LE Document (generic VBELN), Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| PM_other | 3 | 6 | 6 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 15 | 6 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Address, Batch, Business Partner, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FI-GL_General-Ledger | 2 | 11 | 11 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
