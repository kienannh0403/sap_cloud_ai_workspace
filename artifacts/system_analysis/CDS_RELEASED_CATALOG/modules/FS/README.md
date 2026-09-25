# FS

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `FS` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**78 view** · data category: (none) 76, Dimension 2 · loại: basic 41, text 31, value_help 4, dimension 2 · 1 view có field DEPRECATED/DECOMMISSIONED · 75 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FS-BP | 75 | top-level |
| FS-CM | 3 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_BPFINANCIALSERVICESREPORTING | Business Partner Reporting Data | FS-BP |  | 54 |
| I_BPFINANCIALSERVICESEXTN | Financial Services Attributes for BP | FS-BP |  | 35 |
| I_BPFISCALYEARINFORMATION | Fiscal year information of BP | FS-BP |  | 35 |
| I_BPCREDITWORTHINESS | Credit Worthiness of Business Partner | FS-BP |  | 23 |
| I_BUSINESSPARTNERRATING | Rating of Business Partner | FS-BP |  | 18 |
| I_BPEMPLOYMENT | Employment of Business Partner | FS-BP |  | 12 |
| I_BUSINESSPARTNERISBANK | Business Partner Identification as bank | FS-BP |  | 8 |
| I_BPRATINGPROCEDURE | Rating Procedure of Business Partner | FS-BP |  | 7 |
| I_BPRATINGPROCEDUREGRADE | Rating Procedure Grade of BP | FS-BP |  | 6 |
| I_BUSINESSPARTNERALIAS | Business Partner Alias | FS-BP |  | 5 |
| I_BPLETTERSALUTATION | Letter Salutation of Business Partner | FS-BP |  | 4 |
| I_INSURANCECLAIMSCOPEOFLOSS | Insurance Claim Scope Of Loss | FS-CM | Dimension | 4 |
| I_BPCNTRLBANKCOUNTRYREGION | Central Bank Country Region | FS-BP |  | 3 |
| I_BPCREDITRATINGAGENCY | Rating Agency of Business Partner | FS-BP |  | 3 |
| I_BPCREDITSTANDINGREVIEW | Credit Standing Review | FS-BP |  | 3 |
| I_BPCREDITWORTHINESSRATING | Credit Worthiness Rating of BP | FS-BP |  | 3 |
| I_BPEMPLOYMENTINDUSTRY | Employment Industry of Business Partner | FS-BP |  | 3 |
| I_BPEMPLOYMENTSTATUS | Employment Status of Business Partner | FS-BP |  | 3 |
| I_BPLEGALPROCEEDINGSTATUS | Legal Proceedings Status of BP | FS-BP |  | 3 |
| I_BPLOANTOMANAGER | Loan to Manager | FS-BP |  | 3 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Business Partner | 4 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| AP | 0 | 1 | 0 | Business Partner |
| BC | 0 | 1 | 0 | Business Partner |
| CA | 0 | 1 | 0 | Business Partner |
| CRM | 0 | 1 | 0 | Business Partner |
| FIN | 0 | 1 | 0 | Business Partner |
| FI_other | 0 | 1 | 0 | Business Partner |
| LO_other | 0 | 1 | 0 | Business Partner |
| MM-PUR_Purchasing | 0 | 1 | 0 | Business Partner |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
