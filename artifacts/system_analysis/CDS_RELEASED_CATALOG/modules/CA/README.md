# CA

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `CA` (không thuộc phân hệ ưu tiên nào trong Sheet1). `CA`: Cross-Application.

**249 view** · data category: (none) 134, Dimension 105, Fact 7, Cube 3 · loại: dimension 103, basic 89, text 34, value_help 13, fact 7, cube 3 · 3 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CA-ATP | 1 | top-level |
| CA-ATP-OVD | 2 | top-level |
| CA-ATP-PAL | 26 | top-level |
| CA-CL | 55 | top-level |
| CA-CPD-SS | 1 | top-level |
| CA-DMS | 33 | top-level |
| CA-EPT-SUB | 2 | top-level |
| CA-FL-SRV | 1 | top-level |
| CA-GTF-CSC | 2 | top-level |
| CA-GTF-CSC-EDO-CH | 2 | top-level |
| CA-GTF-CSC-EDO-CO | 3 | top-level |
| CA-GTF-CSC-EDO-GR | 1 | top-level |
| CA-GTF-CSC-EDO-HU | 1 | top-level |
| CA-GTF-CSC-EDO-IN-EW | 1 | top-level |
| CA-GTF-CSC-EDO-IN-IV | 1 | top-level |
| CA-GTF-CSC-EDO-IT | 2 | top-level |
| CA-GTF-DF | 13 | top-level |
| CA-GTF-FXU-FI-AR | 2 | top-level |
| CA-GTF-FXU-FI-CO | 1 | top-level |
| CA-GTF-GL-CAL | 20 | top-level |
| CA-GTF-TRB | 1 | top-level |
| CA-GTF-VDM | 11 | top-level |
| CA-JVA | 38 | top-level |
| CA-JVA-JVA | 1 | top-level |
| CA-TS-S4 | 14 | top-level |
| CA-WFD | 5 | top-level |
| CA-WFD-BL | 9 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_JVAJNTINTERESTBILLINGDATA | JVA Joint Interest Billing Report | CA-JVA |  | 102 |
| I_JVAGLOBALCOMPANYPARAMETER | JV Global Company Parameter C1 | CA-JVA |  | 86 |
| I_JVAJOINTOPERATINGAGRMTDET_2 | JVA and cost object MD information | CA-JVA | Cube | 86 |
| I_PAYMENTADVICEITEM | Payment Advice Item | CA-GTF-FXU-FI-AR |  | 71 |
| I_PAYMENTADVICE | Payment Advice Header | CA-GTF-FXU-FI-AR |  | 57 |
| I_TIMESHEETRECORD | Time Recording Data | CA-TS-S4 | Fact | 57 |
| I_GR_ELECTRONICDOCINVOICE | eDocument Greece Country/Region Specific Data | CA-GTF-CSC-EDO-GR |  | 55 |
| I_CLFNCHARACTERISTIC | Classification Characteristic | CA-CL |  | 52 |
| I_CLFNCHARACTERISTICFORKEYDATE | Clfn Characteristic for Key Date | CA-CL |  | 52 |
| I_JVAVENTURECOSTOBJECTDETS_2 | Joint Venture Cost Object Details | CA-JVA | Cube | 52 |
| I_IN_ELECTRONICDOCTRANSPTREGN | India eWay Bill details | CA-GTF-CSC-EDO-IN-EW |  | 50 |
| I_JOINTVENTUREDETAILS | Master Data for Joint Venture | CA-JVA |  | 49 |
| I_CLFNCHARACTERISTICDEX | Classification Characteristic DEX | CA-CL | Dimension | 48 |
| I_FLDLOGSSUPPLIERITEM | Field Logistics Supplier Items | CA-FL-SRV |  | 44 |
| I_WORKASSIGNMENTADDRESS | Work Assignment Address Details | CA-WFD-BL |  | 44 |
| I_JOINTVENTUREMASTERFLD | Joint Venture Master Data Fields | CA-JVA | Dimension | 43 |
| I_DOCUMENTINFORECORD | Document Info Record Details | CA-DMS | Dimension | 41 |
| I_WORKFORCEPERSONADDRESS | Workforce Person Address Details | CA-WFD-BL |  | 40 |
| I_CLFNCLASSFORKEYDATE | Classification Class for Key Date | CA-CL |  | 38 |
| I_CLFNCLASS | Classification Class | CA-CL |  | 37 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 47 |
| CONFIG | Fiscal Year | 18 |
| MASTER | WBS Element | 13 |
| ORG | Controlling Area | 10 |
| MASTER | Business Partner | 8 |
| ORG | Plant | 5 |
| CONFIG | Tax Code | 5 |
| MASTER | Cost Center | 5 |
| MASTER | Address | 3 |
| CONFIG | Payment Terms | 3 |
| ORG | Business Area | 2 |
| ORG | Chart of Accounts | 2 |
| ORG | Valuation Area | 2 |
| DOC | Order (production / maintenance / internal) | 2 |
| MASTER | Activity Type | 2 |
| MASTER | Personnel | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| MM-PUR_Purchasing | 1 | 6 | 4 | Order (production / maintenance / internal), Activity Type, Address, Business Partner, Cost Center, Personnel, WBS Element |
| FI_other | 1 | 5 | 5 | Order (production / maintenance / internal), Address, Business Partner, Cost Center, Personnel, WBS Element |
| SD-SLS_Sales | 1 | 5 | 3 | Order (production / maintenance / internal), Address, Business Partner, Cost Center, Personnel, WBS Element |
| SD_other | 1 | 5 | 2 | Order (production / maintenance / internal), Address, Business Partner, Cost Center, Personnel, WBS Element |
| FI-GL_General-Ledger | 1 | 4 | 6 | Order (production / maintenance / internal), Activity Type, Cost Center, Personnel, WBS Element |
| MM_other | 1 | 4 | 4 | Order (production / maintenance / internal), Activity Type, Cost Center, Personnel, WBS Element |
| LO_other | 1 | 3 | 4 | Order (production / maintenance / internal), Address, Business Partner, Personnel |
| MM-IM_Inventory-Management | 1 | 2 | 4 | Order (production / maintenance / internal), Cost Center, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
