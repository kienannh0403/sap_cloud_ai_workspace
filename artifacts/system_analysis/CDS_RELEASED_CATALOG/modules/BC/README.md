# BC

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `BC` (không thuộc phân hệ ưu tiên nào trong Sheet1). `BC`: Basis / cross-application services.

**90 view** · data category: (none) 68, Dimension 21, Fact 1 · loại: basic 32, text 27, dimension 20, value_help 10, fact 1 · 1 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| BC-DOC-TTL | 2 | top-level |
| BC-DWB-DIC | 2 | top-level |
| BC-SEC-USR-ADM | 2 | top-level |
| BC-SRV-ADR | 36 | top-level |
| BC-SRV-APS-EXT-FLD | 3 | top-level |
| BC-SRV-APS-IAM | 9 | top-level |
| BC-SRV-ASF-FYV | 5 | top-level |
| BC-SRV-ASF-UOM | 9 | top-level |
| BC-SRV-BP | 2 | top-level |
| BC-SRV-BSF-CUR | 10 | top-level |
| BC-SRV-BUM | 2 | top-level |
| BC-SRV-TIM-TZ | 8 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PERSONADDRESS | Address of a Person | BC-SRV-ADR | Dimension | 110 |
| I_PERSONADDRESSDEFAULTRPRSTN | Deafult Represention for Address of a Person | BC-SRV-ADR | Dimension | 100 |
| I_ORGANIZATIONADDRESS | Address of an Organization | BC-SRV-ADR | Dimension | 94 |
| I_ORGADDRESSDEFAULTRPRSTN | Default Representation of an Org Address | BC-SRV-ADR | Dimension | 87 |
| I_ORGNAMEPOSTLADDRDFLTRPRSTN | Dflt Addr Rprstn for Postal and Org | BC-SRV-ADR | Dimension | 58 |
| I_BUSINESSUSERBASIC | Business User Basic View | BC-SRV-BUM |  | 43 |
| I_PERSONWORKPLACEADDRESS | Corporate Workplace Address of a Person | BC-SRV-ADR | Fact | 41 |
| I_WORKPLACEADDRESS | Employee Workplace Address | BC-SRV-BP | Dimension | 30 |
| I_UNITOFMEASURE | Unit of Measure | BC-SRV-ASF-UOM | Dimension | 23 |
| I_IAMBUSINESSUSERLOGONDETAILS | Business User Logon Details | BC-SRV-APS-IAM |  | 22 |
| I_COUNTRY | Country/Region | BC-SRV-ADR | Dimension | 20 |
| I_IAMSUPPORTUSERREQUESTLOG | Support User Request Log | BC-SRV-APS-IAM |  | 17 |
| I_UNITOFMEASUREDIMENSION | Unit of Measure Dimension | BC-SRV-ASF-UOM | Dimension | 12 |
| I_EXCHANGERATEFACTORSRAWDATA | Exchange Rate Factors Raw Data | BC-SRV-BSF-CUR |  | 11 |
| I_IAMBUSINESSROLE | Business Role | BC-SRV-APS-IAM |  | 10 |
| I_EXCHANGERATERAWDATA | Exchange Rate Raw Data | BC-SRV-BSF-CUR |  | 10 |
| I_USER | User | BC-SEC-USR-ADM |  | 9 |
| I_EXCHANGERATETYPE | Exchange Rate Type | BC-SRV-BSF-CUR | Dimension | 9 |
| I_TERTIARYREGION | Tertiary Region | BC-SRV-ADR |  | 8 |
| I_FISCALPERIODTEXTRAWDATA | Fiscal Period Texts Raw Data | BC-SRV-ASF-FYV |  | 8 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Address | 8 |
| MASTER | Business Partner | 3 |
| CONFIG | Fiscal Year | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CA | 0 | 2 | 0 | Address, Business Partner |
| FI_other | 0 | 2 | 0 | Address, Business Partner |
| LO_other | 0 | 2 | 0 | Address, Business Partner |
| MM-PUR_Purchasing | 0 | 2 | 0 | Address, Business Partner |
| SD-SLS_Sales | 0 | 2 | 0 | Address, Business Partner |
| SD_other | 0 | 2 | 0 | Address, Business Partner |
| AP | 0 | 1 | 0 | Business Partner |
| FIN | 0 | 1 | 0 | Business Partner |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
