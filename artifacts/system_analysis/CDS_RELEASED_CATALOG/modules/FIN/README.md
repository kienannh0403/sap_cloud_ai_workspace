# FIN

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `FIN` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**514 view** · data category: (none) 319, Dimension 191, Cube 3, Fact 1 · loại: dimension 191, basic 145, text 100, value_help 74, cube 3, fact 1 · 61 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FIN-CS-COR-MON | 12 | top-level |
| FIN-CS-EA | 2 | top-level |
| FIN-CS-MD | 294 | top-level |
| FIN-FSCM-CLM | 3 | top-level |
| FIN-FSCM-CLM-BAM | 6 | top-level |
| FIN-FSCM-COL | 8 | top-level |
| FIN-FSCM-CR | 23 | top-level |
| FIN-FSCM-DM | 15 | top-level |
| FIN-FSCM-FQM | 5 | top-level |
| FIN-FSCM-TRM | 125 | top-level |
| FIN-FSCM-TRM-CR | 6 | top-level |
| FIN-FSCM-TRM-MR | 5 | top-level |
| FIN-IE-FS | 10 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_FINANCIALTRANSACTION | Financial Transaction | FIN-FSCM-TRM | Dimension | 125 |
| I_CNSLDTNGROUPJRNLENTRITMDEX | Group Journal Entry Item Extraction | FIN-CS-EA |  | 124 |
| I_SECURITYCLASSCONDITIONITEM | Security Class Condition Item | FIN-FSCM-TRM |  | 105 |
| I_SECURITYCLASS | Security Class | FIN-FSCM-TRM | Dimension | 68 |
| I_FINTRANSACTIVITY | Financial Transaction Activity | FIN-FSCM-TRM |  | 64 |
| I_HOUSEBANK | Master data for House Bank | FIN-FSCM-CLM-BAM | Dimension | 35 |
| I_TRSYLEDGERTRANSACTIONFLOW | Treasury Ledger Flow | FIN-FSCM-TRM |  | 35 |
| I_TREASURYPOSITIONIDENTIFIER | Treasury Position Identifier | FIN-FSCM-TRM | Fact | 32 |
| I_CNSLDTNFSITEMBYTIMEVERSION | Consolidation FS Item by Time Version | FIN-CS-MD |  | 29 |
| I_SECURITYCLASSBASIC | Security Class Basic | FIN-FSCM-TRM |  | 28 |
| I_CNSLDTNVERSION | Consolidation Version | FIN-CS-MD | Dimension | 27 |
| I_FINTRANSACTIONNPVCUBE | Financial Transaction NPV - Cube | FIN-FSCM-TRM-MR | Cube | 25 |
| I_HOUSEBANKACCOUNTLINKAGE | House Bank Account Linkage | FIN-FSCM-CLM-BAM |  | 24 |
| I_CNSLDTNUNITBYTIMEVERSION_2 | Consolidation Unit by Time and Version | FIN-CS-MD |  | 22 |
| I_CREDITMANAGEMENTACCOUNT | Credit Management Account | FIN-FSCM-CR |  | 21 |
| I_CNSLDTNFSITEM_2 | Consolidation Financial Statement Item | FIN-CS-MD | Dimension | 20 |
| I_HEDGINGRELATIONSHIP | Hedging Relationship | FIN-FSCM-TRM | Dimension | 19 |
| I_CNSLDTNGROUPSTRUCTURE_2 | Consolidation Group Structure | FIN-CS-MD |  | 18 |
| I_CREDITACCOUNTADDITIONALINFO | Credit Account Additional Information | FIN-FSCM-CR |  | 18 |
| I_CREDITEXPOSUREITEM | Credit Exposure Items | FIN-FSCM-CR |  | 18 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 20 |
| MASTER | Business Partner | 8 |
| MASTER | Cost Center | 3 |
| ORG | Functional Area | 3 |
| ORG | Profit Center | 3 |
| ORG | Business Area | 2 |
| ORG | Controlling Area | 2 |
| ORG | Segment | 2 |
| MASTER | Grant | 2 |
| MASTER | WBS Element | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| MM-PUR_Purchasing | 0 | 4 | 5 | Business Partner, Cost Center, Grant, WBS Element |
| FI-GL_General-Ledger | 0 | 3 | 6 | Cost Center, Grant, WBS Element |
| FI_other | 0 | 3 | 6 | Business Partner, Cost Center, WBS Element |
| MM_other | 0 | 3 | 5 | Cost Center, Grant, WBS Element |
| CA | 0 | 3 | 3 | Business Partner, Cost Center, WBS Element |
| SD-SLS_Sales | 0 | 3 | 3 | Business Partner, Cost Center, WBS Element |
| SD_other | 0 | 3 | 3 | Business Partner, Cost Center, WBS Element |
| PP-SFC_Shop-Floor-Control | 0 | 2 | 5 | Cost Center, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
