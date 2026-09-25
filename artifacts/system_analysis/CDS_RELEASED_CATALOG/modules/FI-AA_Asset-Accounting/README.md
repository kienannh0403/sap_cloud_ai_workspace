# FI-AA_Asset-Accounting — Asset Accounting

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `FI-AA` = **Asset Accounting**.

**22 view** · data category: (none) 22 · loại: basic 15, text 6, value_help 1 · 0 view có field DEPRECATED/DECOMMISSIONED · 19 view mới so với file xlsx của user · 3 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-AA-2CL | 3 | component |
| FI-AA-AA-2CL | 17 | component |
| FI-AA-AA-H-2CL | 2 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_ASSETREVALUATIONINDEX | Asset Revaluation Index | FI-AA-AA-H-2CL |  | 21 |
| I_FIXEDASSETUSAGEOBJECT | Fixed Asset Usage Object | FI-AA-2CL |  | 16 |
| I_FIXEDASSETUSAGEOBJECTTOTAL | Total Units of Fixed Asset Usage Object | FI-AA-2CL |  | 10 |
| I_FIXEDASSETUSAGEOBJECTPERIOD | Period Units of Fixed Asset Usage Object | FI-AA-2CL |  | 9 |
| I_ASSETREVALUATIONINDEXITEM | Asset Revaluation Index Item | FI-AA-AA-H-2CL |  | 5 |
| I_ASSETCAPITALIZATIONTOYEAR |  | FI-AA-AA-2CL |  | 0 |
| I_ASSETDEPRCALCPHASELEVELVALUE |  | FI-AA-AA-2CL |  | 0 |
| I_ASSETDEPRECIATIONPHASE | Asset Depreciation Phase | FI-AA-AA-2CL |  | 0 |
| I_ASSETDEPRECIATIONTYPE | Asset Depreciation Type | FI-AA-AA-2CL |  | 0 |
| I_ASSETKEYFIGURE | Asset Key Figure | FI-AA-AA-2CL |  | 0 |
| I_ASSETKEYFIGURESET | Asset Key Figure Set | FI-AA-AA-2CL |  | 0 |
| I_ASSETSORTEDKEYFIGURESETSPEC | Sorted Fixed Asset Key Figure Set Specification | FI-AA-AA-2CL |  | 0 |
| I_DEPRECIATIONPROFILE | Depreciation Profile | FI-AA-AA-2CL |  | 0 |
| I_DEPRPROFILEPHASE | Depreciation Profile Phase Settings | FI-AA-AA-2CL |  | 0 |
| I_DEPRPROFILEPHASELEVEL | Depreciation Profile Phase Level | FI-AA-AA-2CL |  | 0 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 3 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| AC | 0 | 0 | 1 | — |
| CA | 0 | 0 | 1 | — |
| CO-OM_Cost-Center-Accounting | 0 | 0 | 1 | — |
| CO_other | 0 | 0 | 1 | — |
| CRM | 0 | 0 | 1 | — |
| EAM-OBJ_Technical-Objects | 0 | 0 | 1 | — |
| FI-AP_Accounts-Payable | 0 | 0 | 1 | — |
| FI-AR_Accounts-Receivable | 0 | 0 | 1 | — |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
