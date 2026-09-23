# CO-OM_Cost-Center-Accounting — Cost Center Accounting

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `CO-OM` = **Cost Center Accounting**.

**5 view** · data category: (none) 4, Fact 1 · loại: basic 3, text 1, fact 1 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CO-OM | 4 | component |
| CO-OM-CCA-AVC | 1 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_COSTCENTERBUDGET | Cost Center Budget Report | CO-OM-CCA-AVC |  | 80 |
| I_SERVICECOSTRATE_2 | Service Cost Rate | CO-OM | Fact | 43 |
| I_SERVICECOSTLEVELTEXT_2 | Service Cost Level - Text | CO-OM |  | 6 |
| I_SERVICECOSTLEVEL | Service Cost Level | CO-OM |  | 4 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 2 |
| ORG | Controlling Area | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CA | 0 | 0 | 2 | — |
| CO_other | 0 | 0 | 2 | — |
| FI-GL_General-Ledger | 0 | 0 | 2 | — |
| FIN | 0 | 0 | 2 | — |
| FI_other | 0 | 0 | 2 | — |
| LO_other | 0 | 0 | 2 | — |
| MM-IM_Inventory-Management | 0 | 0 | 2 | — |
| MM-PUR_Purchasing | 0 | 0 | 2 | — |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
