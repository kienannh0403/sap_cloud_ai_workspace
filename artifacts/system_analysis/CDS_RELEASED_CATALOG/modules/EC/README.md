# EC

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `EC` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**8 view** · data category: (none) 6, Dimension 2 · loại: dimension 2, basic 2, text 2, value_help 2 · 1 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| EC-PCA-MD | 8 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PROFITCENTER | Profit Center | EC-PCA-MD | Dimension | 49 |
| I_PROFITCENTERHIERARCHYNODE | Profit Center Hierarchy Node | EC-PCA-MD |  | 18 |
| I_PROFITCENTERHIERARCHYNODET | Profit Center Hierarchy Node - Text | EC-PCA-MD |  | 12 |
| I_PROFITCENTERHIERARCHY | Profit Center Hierarchy | EC-PCA-MD | Dimension | 11 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Controlling Area | 7 |
| ORG | Profit Center | 4 |
| ORG | Segment | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI-GL_General-Ledger | 0 | 0 | 3 | — |
| FIN | 0 | 0 | 3 | — |
| FI_other | 0 | 0 | 3 | — |
| CRM | 0 | 0 | 2 | — |
| LE | 0 | 0 | 2 | — |
| MM-IM_Inventory-Management | 0 | 0 | 2 | — |
| MM-PUR_Purchasing | 0 | 0 | 2 | — |
| MM_other | 0 | 0 | 2 | — |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
