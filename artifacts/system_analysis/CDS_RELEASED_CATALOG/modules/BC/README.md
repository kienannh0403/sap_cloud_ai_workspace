# BC

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `BC` (không thuộc phân hệ ưu tiên nào trong Sheet1). `BC`: Basis / cross-application services.

**230 view** · data category: (none) 208, Dimension 21, Fact 1 · loại: basic 143, text 47, dimension 20, value_help 19, fact 1 · 3 view có field DEPRECATED/DECOMMISSIONED · 142 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| BC-ABA-LA | 2 | top-level |
| BC-ABA-SC | 2 | top-level |
| BC-BMT-OM | 1 | top-level |
| BC-BMT-WFM | 17 | top-level |
| BC-BMT-WFP | 3 | top-level |
| BC-CTS-ORG | 3 | top-level |
| BC-CUS-TOL-MBC | 2 | top-level |
| BC-DOC-TTL | 3 | top-level |
| BC-DWB-CEX-CCM | 3 | top-level |
| BC-DWB-DIC | 42 | top-level |
| BC-DWB-TOO-ATF | 4 | top-level |
| BC-SEC-USR-ADM | 2 | top-level |
| BC-SRV-ADR | 78 | top-level |
| BC-SRV-APS-EXT-FLD | 7 | top-level |
| BC-SRV-APS-EXT-REL | 5 | top-level |
| BC-SRV-APS-IAM | 9 | top-level |
| BC-SRV-ASF-CAL | 6 | top-level |
| BC-SRV-ASF-CHD | 1 | top-level |
| BC-SRV-ASF-FYV | 5 | top-level |
| BC-SRV-ASF-UOM | 7 | top-level |
| BC-SRV-BP | 3 | top-level |
| BC-SRV-BSF-CUR-2CL | 10 | top-level |
| BC-SRV-BUM | 7 | top-level |
| BC-SRV-TIM-TZ | 8 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PERSONADDRESS | Address of a Person | BC-SRV-ADR | Dimension | 110 |
| I_PERSONADDRESSDEFAULTRPRSTN | Deafult Represention for Address of a Person | BC-SRV-ADR | Dimension | 100 |
| I_ADDRESS_2 | Address of an Organization or a Person | BC-SRV-ADR |  | 98 |
| I_ORGANIZATIONADDRESS | Address of an Organization | BC-SRV-ADR | Dimension | 94 |
| I_ADDRESSDEFAULTREPRESENTATION | Dflt Addr Rprstn of an Org or a Person | BC-SRV-ADR |  | 91 |
| I_ORGADDRESSDEFAULTRPRSTN | Default Representation of an Org Address | BC-SRV-ADR | Dimension | 87 |
| I_ADDRORGNAMEPOSTALADDRESS | Postal Address and Organization Name | BC-SRV-ADR |  | 65 |
| I_ORGNAMEPOSTLADDRDFLTRPRSTN | Dflt Addr Rprstn for Postal and Org | BC-SRV-ADR | Dimension | 58 |
| I_BUSINESSUSERBASIC | Business User Basic View | BC-SRV-BUM |  | 43 |
| SATC_API_FINDINGS | ATC: Findings | BC-DWB-TOO-ATF |  | 41 |
| I_PERSONWORKPLACEADDRESS | Corporate Workplace Address of a Person | BC-SRV-ADR | Fact | 41 |
| I_ADDRESSPERSONNAME | Person Name | BC-SRV-ADR |  | 33 |
| SATC_API_RESULT_HEADERS | ATC: Result Headers | BC-DWB-TOO-ATF |  | 32 |
| I_WORKPLACEADDRESS | Employee Workplace Address | BC-SRV-BP | Dimension | 30 |
| SATC_EXEMPTIONS_DDLV_EC2 | View for ATC Exemptions (Cat.  2 - transportable Exemptions) | BC-DWB-TOO-ATF |  | 29 |
| SATC_EXEMPTIONS_DDLV_EC1 | View for ATC Exemptions (Cat. 1 - CI Exemptions) | BC-DWB-TOO-ATF |  | 28 |
| I_ADDRPERSNNAMEDFLTRPRSTN | Default Representation for Person Name | BC-SRV-ADR |  | 27 |
| I_UNITOFMEASURE | Unit of Measure | BC-SRV-ASF-UOM | Dimension | 23 |
| I_IAMBUSINESSUSERLOGONDETAILS | Business User Logon Details | BC-SRV-APS-IAM |  | 22 |
| I_WORKFLOWSTATUSDETAILS | Workflow Task | BC-BMT-WFM |  | 20 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Address | 24 |
| MASTER | Business Partner | 6 |
| CONFIG | Fiscal Year | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| AP | 0 | 2 | 0 | Address, Business Partner |
| CA | 0 | 2 | 0 | Address, Business Partner |
| FI_other | 0 | 2 | 0 | Address, Business Partner |
| LO_other | 0 | 2 | 0 | Address, Business Partner |
| MM-PUR_Purchasing | 0 | 2 | 0 | Address, Business Partner |
| RE | 0 | 2 | 0 | Address, Business Partner |
| SD-BIL_Billing | 0 | 2 | 0 | Address, Business Partner |
| SD-SLS_Sales | 0 | 2 | 0 | Address, Business Partner |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
