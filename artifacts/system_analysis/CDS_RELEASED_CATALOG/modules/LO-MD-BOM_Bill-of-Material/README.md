# LO-MD-BOM_Bill-of-Material — Bill of Material

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `LO-MD-BOM` = **Bill of Material**.

**9 view** · data category: (none) 6, Fact 3 · loại: basic 6, fact 3 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| LO-MD-BOM | 9 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_MATERIALBOMLINK | Material Link for Bill of Material | LO-MD-BOM | Fact | 13 |
| I_SALESORDERBOMLINK | Sales Order Link for BOM | LO-MD-BOM |  | 9 |
| I_PROJECTBOMLINK | Work Breakdown Structure Link for BOM | LO-MD-BOM |  | 8 |
| I_DOCUMENTBOMLINK | Document Link for Bill of Material | LO-MD-BOM |  | 7 |
| I_EQUIPMENTBOMLINK | Equipment to BOM Link | LO-MD-BOM |  | 7 |
| I_FUNCTIONALLOCBOMLINK | Link Between Functional Location and BOM | LO-MD-BOM |  | 7 |
| I_STANDARDBOMLINK | Standard Link for BOM | LO-MD-BOM |  | 7 |
| I_MATERIALBOMLINKDEX | Data Extraction MAST | LO-MD-BOM | Fact | 0 |
| I_SALESORDERBOMLINKDEX | Data extraction for SO bomlink | LO-MD-BOM | Fact | 0 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 6 |
| MASTER | Material / Product | 3 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO_other | 0 | 1 | 1 | Material / Product |
| CRM | 0 | 1 | 1 | Material / Product |
| FI-GL_General-Ledger | 0 | 1 | 1 | Material / Product |
| FI_other | 0 | 1 | 1 | Material / Product |
| LE | 0 | 1 | 1 | Material / Product |
| LO-MD-MM_Material-Master | 0 | 1 | 1 | Material / Product |
| LO_other | 0 | 1 | 1 | Material / Product |
| MM-IM_Inventory-Management | 0 | 1 | 1 | Material / Product |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
