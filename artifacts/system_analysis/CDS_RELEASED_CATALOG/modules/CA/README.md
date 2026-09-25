# CA

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `CA` (không thuộc phân hệ ưu tiên nào trong Sheet1). `CA`: Cross-Application.

**453 view** · data category: (none) 338, Dimension 105, Fact 7, Cube 3 · loại: basic 270, dimension 103, text 41, value_help 29, fact 7, cube 3 · 4 view có field DEPRECATED/DECOMMISSIONED · 205 view mới so với file xlsx của user · 32 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CA-ATP-2CL | 3 | top-level |
| CA-ATP-ACL-2CL | 4 | top-level |
| CA-ATP-OVD-2CL | 2 | top-level |
| CA-ATP-PAL-2CL | 40 | top-level |
| CA-BK-BNK | 7 | top-level |
| CA-CL-2CL | 55 | top-level |
| CA-CPD-SS | 1 | top-level |
| CA-DMS | 33 | top-level |
| CA-DT | 2 | top-level |
| CA-EPT-SUB-2CL | 2 | top-level |
| CA-EPT-TAS | 15 | top-level |
| CA-FIM-FMA | 2 | top-level |
| CA-FL-RET | 8 | top-level |
| CA-FL-SG | 21 | top-level |
| CA-FL-SRV | 3 | top-level |
| CA-GTF-ANL | 8 | top-level |
| CA-GTF-BEL | 4 | top-level |
| CA-GTF-CSC | 2 | top-level |
| CA-GTF-CSC-CH | 1 | top-level |
| CA-GTF-CSC-EDC | 4 | top-level |
| CA-GTF-CSC-EDO | 2 | top-level |
| CA-GTF-CSC-EDO-CH | 5 | top-level |
| CA-GTF-CSC-EDO-CO | 3 | top-level |
| CA-GTF-CSC-EDO-EG | 13 | top-level |
| CA-GTF-CSC-EDO-ES | 1 | top-level |
| CA-GTF-CSC-EDO-GR | 1 | top-level |
| CA-GTF-CSC-EDO-HU | 1 | top-level |
| CA-GTF-CSC-EDO-IN-EW | 1 | top-level |
| CA-GTF-CSC-EDO-IN-IV | 1 | top-level |
| CA-GTF-CSC-EDO-IT | 7 | top-level |
| CA-GTF-CSC-EDO-KR | 6 | top-level |
| CA-GTF-CSC-EDO-KZ | 1 | top-level |
| CA-GTF-CSC-EDO-MY | 1 | top-level |
| CA-GTF-CSC-EDO-PAP | 11 | top-level |
| CA-GTF-CSC-EDO-PT | 2 | top-level |
| CA-GTF-CSC-EDO-SA | 3 | top-level |
| CA-GTF-CSC-EDO-TR | 12 | top-level |
| CA-GTF-CSC-EDO-VN | 1 | top-level |
| CA-GTF-DF | 15 | top-level |
| CA-GTF-FXU-FI-AR | 2 | top-level |
| CA-GTF-FXU-FI-GL | 1 | top-level |
| CA-GTF-GEM | 7 | top-level |
| CA-GTF-GL-CAL | 20 | top-level |
| CA-GTF-OC | 1 | top-level |
| CA-GTF-TRB | 1 | top-level |
| CA-GTF-VDM | 11 | top-level |
| CA-JVA | 44 | top-level |
| CA-JVA-JVA | 24 | top-level |
| CA-TS-S4 | 15 | top-level |
| CA-WFD | 6 | top-level |
| CA-WFD-BL | 9 | top-level |
| CA-WFD-INT | 8 | top-level |

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
| I_CLFNCHARACTERISTIC | Classification Characteristic | CA-CL-2CL |  | 52 |
| I_CLFNCHARACTERISTICFORKEYDATE | Clfn Characteristic for Key Date | CA-CL-2CL |  | 52 |
| I_JVAVENTURECOSTOBJECTDETS_2 | Joint Venture Cost Object Details | CA-JVA | Cube | 52 |
| I_IN_ELECTRONICDOCTRANSPTREGN | India eWay Bill details | CA-GTF-CSC-EDO-IN-EW |  | 50 |
| I_JOINTVENTUREDETAILS | Master Data for Joint Venture | CA-JVA |  | 49 |
| I_CLFNCHARACTERISTICDEX | Classification Characteristic DEX | CA-CL-2CL | Dimension | 48 |
| I_FLDLOGSSUPPLIERITEM | Field Logistics Supplier Items | CA-FL-SRV |  | 44 |
| I_WORKASSIGNMENTADDRESS | Work Assignment Address Details | CA-WFD-BL |  | 44 |
| I_JOINTVENTUREMASTERFLD | Joint Venture Master Data Fields | CA-JVA | Dimension | 43 |
| I_DOCUMENTINFORECORD | Document Info Record Details | CA-DMS | Dimension | 41 |
| I_WORKFORCEPERSONADDRESS | Workforce Person Address Details | CA-WFD-BL |  | 40 |
| I_CLFNCLASSFORKEYDATE | Classification Class for Key Date | CA-CL-2CL |  | 38 |
| I_BUSEVTLOGBUSINESSEVENT | Business Event Header Data | CA-GTF-BEL |  | 38 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 77 |
| CONFIG | Fiscal Year | 20 |
| MASTER | WBS Element | 13 |
| CONFIG | Tax Code | 10 |
| ORG | Controlling Area | 9 |
| MASTER | Business Partner | 8 |
| MASTER | Customer | 7 |
| ORG | Plant | 7 |
| MASTER | Address | 6 |
| MASTER | Supplier | 5 |
| ORG | Sales Organization | 4 |
| MASTER | Cost Center | 4 |
| MASTER | Material / Product | 3 |
| CONFIG | Payment Terms | 3 |
| DOC | Billing Document | 2 |
| ORG | Distribution Channel | 2 |
| ORG | Chart of Accounts | 2 |
| ORG | Valuation Area | 2 |
| DOC | Order (production / maintenance / internal) | 2 |
| MASTER | Activity Type | 2 |
| MASTER | Personnel | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD-BIL_Billing | 2 | 8 | 5 | Billing Document, Order (production / maintenance / internal), Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |
| SD_other | 2 | 8 | 5 | Billing Document, Order (production / maintenance / internal), Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |
| FI_other | 1 | 9 | 7 | Order (production / maintenance / internal), Activity Type, Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |
| MM-PUR_Purchasing | 1 | 9 | 3 | Order (production / maintenance / internal), Activity Type, Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |
| FIN | 1 | 8 | 7 | Order (production / maintenance / internal), Activity Type, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |
| SD-SLS_Sales | 1 | 8 | 4 | Order (production / maintenance / internal), Address, Business Partner, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |
| FI-GL_General-Ledger | 1 | 7 | 7 | Order (production / maintenance / internal), Activity Type, Cost Center, Customer, Material / Product, Personnel, Supplier, WBS Element |
| LO_other | 1 | 6 | 6 | Order (production / maintenance / internal), Address, Business Partner, Customer, Material / Product, Personnel, Supplier |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
