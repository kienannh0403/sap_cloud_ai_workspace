# FI-AA_Asset-Accounting — Asset Accounting

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `FI-AA` = **Asset Accounting**.

**9 view** · data category: (none) 5, Dimension 4 · loại: basic 4, dimension 4, text 1 · 2 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-AA | 3 | component |
| FI-AA-IS | 6 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_FIXEDASSET | Fixed Asset | FI-AA-IS | Dimension | 142 |
| I_FIXEDASSETASSGMT | Fixed Asset Time Dependent Data | FI-AA-IS | Dimension | 57 |
| I_FIXEDASSETUSAGEOBJECT | Fixed Asset Usage Object | FI-AA |  | 16 |
| I_FIXEDASSETFORLEDGER | Fixed Asset for Ledger | FI-AA-IS |  | 15 |
| I_FIXEDASSETUSAGEOBJECTTOTAL | Total Units of Fixed Asset Usage Object | FI-AA |  | 10 |
| I_FIXEDASSETUSAGEOBJECTPERIOD | Period Units of Fixed Asset Usage Object | FI-AA |  | 9 |
| I_MASTERFIXEDASSET | Master Fixed Asset | FI-AA-IS | Dimension | 6 |
| I_CHARTOFDEPRECIATION | Chart of Depreciation | FI-AA-IS | Dimension | 3 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 7 |
| MASTER | Fixed Asset | 4 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI-GL_General-Ledger | 0 | 1 | 1 | Fixed Asset |
| MM-PUR_Purchasing | 0 | 1 | 1 | Fixed Asset |
| MM_other | 0 | 1 | 1 | Fixed Asset |
| CA | 0 | 0 | 1 | — |
| CO-OM_Cost-Center-Accounting | 0 | 0 | 1 | — |
| CO_other | 0 | 0 | 1 | — |
| FI-AP_Accounts-Payable | 0 | 0 | 1 | — |
| FI-AR_Accounts-Receivable | 0 | 0 | 1 | — |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
