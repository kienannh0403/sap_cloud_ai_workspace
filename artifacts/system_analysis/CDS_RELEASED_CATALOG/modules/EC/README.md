# EC

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `EC` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**13 view** · data category: (none) 10, Dimension 2, Fact 1 · loại: basic 6, dimension 2, text 2, value_help 2, fact 1 · 1 view có field DEPRECATED/DECOMMISSIONED · 4 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| EC-PCA-MD-2CL | 13 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PROFITCENTER | Profit Center | EC-PCA-MD-2CL | Dimension | 49 |
| I_PROFITCENTERHIERARCHYNODE | Profit Center Hierarchy Node | EC-PCA-MD-2CL |  | 18 |
| I_PROFITCENTERHIERARCHYNODET | Profit Center Hierarchy Node - Text | EC-PCA-MD-2CL |  | 12 |
| I_PRFTCTRCOMPANYCODEASSIGNMENT | Company code assignment to profit center | EC-PCA-MD-2CL | Fact | 11 |
| I_PROFITCENTERHIERARCHY | Profit Center Hierarchy | EC-PCA-MD-2CL | Dimension | 11 |
| D_PRFTCTRCHANGEVALIDITYPERIODP | Change Validity Period Parameter | EC-PCA-MD-2CL |  | 0 |
| I_PRFTCTRCOMPCODEASSGMTTP_2 | Prft Center Company Code Assignment - TP | EC-PCA-MD-2CL |  | 0 |
| I_PROFITCENTERTEXTTP_2 | Profit Center - Text TP | EC-PCA-MD-2CL |  | 0 |
| I_PROFITCENTERTP_2 | Profit Center - TP | EC-PCA-MD-2CL |  | 0 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Controlling Area | 8 |
| ORG | Profit Center | 5 |
| ORG | Segment | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO-OM_Cost-Center-Accounting | 0 | 0 | 3 | — |
| CO_other | 0 | 0 | 3 | — |
| FIN | 0 | 0 | 3 | — |
| FI_other | 0 | 0 | 3 | — |
| CRM | 0 | 0 | 2 | — |
| FI-GL_General-Ledger | 0 | 0 | 2 | — |
| LE | 0 | 0 | 2 | — |
| MM-IM_Inventory-Management | 0 | 0 | 2 | — |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
