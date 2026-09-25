# AC

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `AC` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**27 view** · data category: (none) 27 · loại: basic 24, value_help 3 · 0 view có field DEPRECATED/DECOMMISSIONED · 27 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| AC-INT-2CL | 19 | top-level |
| AC-INT-ECS-2CL | 8 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_FINSGLERRORITEMDETAIL | Financial Services GL Error Item Detail | AC-INT-ECS-2CL |  | 45 |
| I_FINSGLPOSTEDITEM | Financial Services GL Posted Item | AC-INT-ECS-2CL |  | 29 |
| I_FINSGLMODIFIEDITEM | Financial Services GL Modified Item | AC-INT-ECS-2CL |  | 19 |
| I_FINSGLORIGINALITEM | Financial Services GL Original Item | AC-INT-ECS-2CL |  | 19 |
| I_FINSGLERRORMESSAGE | Financial Services GL Error Message | AC-INT-ECS-2CL |  | 9 |
| D_GLADJMTITEMPOSTJOURNALENTRYP | G/L Adjustment Item Post Parameter | AC-INT-2CL |  | 0 |
| D_GLADJMTPOSTJOURNALENTRYP | G/L Adjustment Post Parameter | AC-INT-2CL |  | 0 |
| D_GLADJMTREVERSEJOURNALENTRYP | G/L Adjustment Reverse Parameter | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYCHANGEAPARITEMP | Journal Entry APAR Item | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYCHANGEGLITEMP | Journal Entry GL Item | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYCHANGEPARAMETER | Journal Entry Change | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYCREATED | Journal Entry Created | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYPOSTAPITEMP | Journal Entry AP Item | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYPOSTARITEMP | Journal Entry AR Item | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYPOSTCOPAP | Journal Entry Profitability Supplement | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYPOSTCPDP | Journal Entry One Time Customer/Supplier | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYPOSTCURRENCYAMTP | Journal Entry Currency Amount | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYPOSTGLITEMP | Journal Entry GL Item | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYPOSTPARAMETER | Journal Entry Abstract View Parameter | AC-INT-2CL |  | 0 |
| D_JOURNALENTRYPOSTTAXITEMP | Journal Entry Tax Item | AC-INT-2CL |  | 0 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 3 |
| CONFIG | Fiscal Year | 3 |
| MASTER | Cost Center | 2 |
| ORG | Profit Center | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO-OM_Cost-Center-Accounting | 0 | 1 | 2 | Cost Center |
| CO_other | 0 | 1 | 2 | Cost Center |
| CRM | 0 | 1 | 2 | Cost Center |
| FIN | 0 | 1 | 2 | Cost Center |
| FI_other | 0 | 1 | 2 | Cost Center |
| MM-IM_Inventory-Management | 0 | 1 | 2 | Cost Center |
| MM-PUR_Purchasing | 0 | 1 | 2 | Cost Center |
| MM_other | 0 | 1 | 2 | Cost Center |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
