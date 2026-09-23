# FI_other

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `FI` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**458 view** · data category: (none) 380, Dimension 66, Fact 6, Cube 6 · loại: basic 237, text 138, dimension 61, value_help 10, fact 6, cube 6 · 20 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI | 2 | top-level |
| FI-CA | 283 | top-level |
| FI-CA-INV | 23 | top-level |
| FI-FIO-AP | 1 | top-level |
| FI-FIO-GL-HIE | 6 | top-level |
| FI-FM | 12 | top-level |
| FI-LOC-AA | 4 | top-level |
| FI-LOC-AA-RU | 4 | top-level |
| FI-LOC-BUP | 1 | top-level |
| FI-LOC-CIT | 2 | top-level |
| FI-LOC-CM-CN | 8 | top-level |
| FI-LOC-EPI-CN | 6 | top-level |
| FI-LOC-FI-CH-QR | 1 | top-level |
| FI-LOC-FI-CL | 2 | top-level |
| FI-LOC-FI-IN | 2 | top-level |
| FI-LOC-FI-JP | 5 | top-level |
| FI-LOC-FI-KR | 7 | top-level |
| FI-LOC-FI-MX | 4 | top-level |
| FI-LOC-FI-PH | 3 | top-level |
| FI-LOC-GAI-CN | 9 | top-level |
| FI-LOC-LO-BR | 6 | top-level |
| FI-LOC-LO-HR | 1 | top-level |
| FI-LOC-LO-IN | 4 | top-level |
| FI-LOC-SAF-PL | 1 | top-level |
| FI-LOC-TIM-CN | 10 | top-level |
| FI-LOC-TXS | 1 | top-level |
| FI-LOC-VAT-GEN | 2 | top-level |
| FI-RA | 36 | top-level |
| FI-TXL-EXT | 9 | top-level |
| FI-TXL-TGM | 3 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_GLACCOUNTLINEITEMSEMTAG | G/L Line Item with Semantic Tag Including FA | FI-FIO-GL-HIE | Cube | 610 |
| I_CADOCUMENTBPITEM | Document Business Partner Item | FI-CA |  | 224 |
| I_CAOPENITEMLISTITEM | Contract Accounting Open Item List Item | FI-CA |  | 192 |
| I_CONTRACTACCOUNTPARTNER | Contract Account Partner | FI-CA | Dimension | 160 |
| I_PROVIDERCONTRACTITEM | Provider Contract Item | FI-CA |  | 141 |
| I_CAPROVIDERCONTRACTITEM | Provider Contract Item | FI-CA | Dimension | 138 |
| I_CABILLGDOCITEM | Billing Document Item | FI-CA-INV |  | 134 |
| I_CAINVCGDOCITEM | Invoicing Document Item | FI-CA-INV |  | 131 |
| I_CADOCUMENTGLITEM | Document General Ledger Item | FI-CA |  | 123 |
| I_RAPERFORMANCEOBLIGATION | RA Performance Obligation | FI-RA | Dimension | 123 |
| I_CABILLGPLNITEM | Billing Plan Item | FI-CA-INV |  | 103 |
| I_US_TAXPARTNERTAXDOCUMENTITEM | US TaxPartnerTaxDocumentItem | FI-TXL-EXT | Dimension | 101 |
| I_CAINVCGDOCHEADER | Invoicing Document Header | FI-CA-INV |  | 98 |
| I_CABILLGDOCHEADER | Billing Document Header | FI-CA-INV |  | 84 |
| I_RAPERFOBLGNWITHOUTACCTASSGMT | RA Perf Oblgn Without Acct Assgmt | FI-RA |  | 78 |
| I_CADOCUMENT | Contract Accounting Document | FI-CA |  | 65 |
| I_REVENUEACCOUNTINGCONTRACT | Revenue Accounting Contract | FI-RA | Dimension | 54 |
| I_CAWRITEOFFDOCUMENT | Contract Accounting Write Off Document | FI-CA | Dimension | 53 |
| I_JP_ANNEX205APBOOKCUBE | Japan Annex215 AP Book - Cube | FI-LOC-FI-JP | Cube | 51 |
| I_CN_TAXINVOICEHEADER | China Tax Invoice Header | FI-LOC-TIM-CN |  | 50 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 57 |
| CONFIG | Tax Code | 11 |
| ORG | Business Area | 10 |
| MASTER | Business Partner | 10 |
| MASTER | Customer | 10 |
| CONFIG | Fiscal Year | 10 |
| ORG | Profit Center | 9 |
| MASTER | G/L Account | 7 |
| ORG | Sales Organization | 6 |
| ORG | Chart of Accounts | 5 |
| ORG | Distribution Channel | 5 |
| ORG | Controlling Area | 4 |
| MASTER | WBS Element | 4 |
| ORG | Division | 4 |
| DOC | Order (production / maintenance / internal) | 4 |
| MASTER | Material / Product | 4 |
| MASTER | Supplier | 4 |
| MASTER | Address | 3 |
| MASTER | Personnel | 3 |
| ORG | Plant | 3 |
| MASTER | Cost Center | 2 |
| MASTER | Profitability Segment | 2 |
| CONFIG | Payment Terms | 2 |
| DOC | Sales Document | 2 |
| ORG | Segment | 2 |
| ORG | Functional Area | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD-SLS_Sales | 2 | 9 | 7 | Order (production / maintenance / internal), Sales Document, Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| SD_other | 2 | 9 | 6 | Order (production / maintenance / internal), Sales Document, Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| FI-GL_General-Ledger | 2 | 8 | 11 | Order (production / maintenance / internal), Sales Document, Cost Center, Customer, G/L Account, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| PM_other | 2 | 2 | 3 | Order (production / maintenance / internal), Sales Document, Material / Product, WBS Element |
| MM-PUR_Purchasing | 1 | 10 | 6 | Order (production / maintenance / internal), Address, Business Partner, Cost Center, Customer, G/L Account, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| LE | 1 | 7 | 8 | Order (production / maintenance / internal), Cost Center, Customer, G/L Account, Material / Product, Profitability Segment, Supplier, WBS Element |
| LO_other | 1 | 7 | 6 | Order (production / maintenance / internal), Address, Business Partner, Customer, G/L Account, Material / Product, Personnel, Supplier |
| MM_other | 1 | 6 | 6 | Order (production / maintenance / internal), Cost Center, G/L Account, Material / Product, Personnel, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
