# QM

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `QM` (không thuộc phân hệ ưu tiên nào trong Sheet1). `QM`: Quality Management.

**173 view** · data category: (none) 143, Dimension 30 · loại: basic 69, text 59, dimension 27, value_help 18 · 4 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| QM | 3 | top-level |
| QM-CA | 2 | top-level |
| QM-IM | 73 | top-level |
| QM-PT | 77 | top-level |
| QM-QN | 18 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_INSPECTIONLOT | Inspection Lot | QM-IM |  | 239 |
| I_INSPECTIONLOTVALUEHELP | Inspection Lot | QM-IM |  | 139 |
| I_INSPSPECIFICATIONVERSION | Version of Master Insp Characteristic | QM-PT |  | 129 |
| I_INSPECTIONCHARACTERISTIC | Characteristic in Inspection Lot | QM-IM |  | 128 |
| I_INSPPLANOPCHARCVERSION_2 | Version of Insp Plan Characteristic | QM-PT |  | 118 |
| I_DEFECT | Defect | QM-QN | Dimension | 103 |
| I_QLTYNOTIFICATION | Quality Notification | QM-QN |  | 100 |
| I_INSPECTIONRESULT | Summarized Insp Result for an Insp Charc | QM-IM |  | 77 |
| I_INSPSUBSETRESULT | Insp Result for an Inspection Point | QM-IM |  | 77 |
| I_INSPECTIONRESULTVALUE | Single Value of an Inspection Charc Rslt | QM-IM |  | 60 |
| I_QUALITYNOTIFICATIONITEM | Quality Notification Item | QM-QN | Dimension | 60 |
| I_INSPECTIONSUBSET | Inspection Point of Inspection Operation | QM-IM |  | 59 |
| I_QUALITYTASK | Quality Task | QM-QN | Dimension | 58 |
| I_INSPECTIONPLANVERSION | Version of Inspection Plan | QM-PT |  | 53 |
| I_QLTYNOTIFICATIONTASK | Quality Notification Task | QM-QN |  | 53 |
| I_SAMPLINGPROCEDURE | Sampling Procedure | QM-PT | Dimension | 43 |
| I_INSPPLANOPERATIONVERSION_2 | Version of Inspection Plan Operation | QM-PT |  | 34 |
| I_INSPLOTUSAGEDECISION | Usage Decision for Inspection Lot | QM-IM |  | 33 |
| I_PRODUCTINSPTYPESETTING | Settings for Inspection Type in Product | QM-PT |  | 33 |
| I_INSPSUBSETCHARACTERISTIC | Inspection Charc for an Inspection Point | QM-IM |  | 31 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 22 |
| DOC | Inspection Lot | 19 |
| MASTER | Material / Product | 6 |
| MASTER | Task List (routing) group | 6 |
| MASTER | Batch | 4 |
| MASTER | Equipment | 4 |
| MASTER | Cost Center | 3 |
| ORG | Sales Organization | 3 |
| ORG | Business Area | 2 |
| ORG | Company Code | 2 |
| ORG | Controlling Area | 2 |
| MASTER | G/L Account | 2 |
| CONFIG | Movement Type | 2 |
| ORG | Profit Center | 2 |
| MASTER | WBS Element | 2 |
| ORG | Storage Location | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| PP_other | 1 | 6 | 6 | Inspection Lot, Batch, Equipment, G/L Account, Material / Product, Task List (routing) group, WBS Element |
| LE | 1 | 5 | 6 | Inspection Lot, Batch, Cost Center, G/L Account, Material / Product, WBS Element |
| PP-SFC_Shop-Floor-Control | 1 | 5 | 5 | Inspection Lot, Batch, Cost Center, Material / Product, Task List (routing) group, WBS Element |
| LO_other | 1 | 4 | 5 | Inspection Lot, Batch, Equipment, G/L Account, Material / Product |
| FI-GL_General-Ledger | 0 | 5 | 6 | Cost Center, Equipment, G/L Account, Material / Product, WBS Element |
| MM-PUR_Purchasing | 0 | 5 | 6 | Batch, Cost Center, G/L Account, Material / Product, WBS Element |
| MM-IM_Inventory-Management | 0 | 5 | 5 | Batch, Cost Center, G/L Account, Material / Product, WBS Element |
| CRM | 0 | 5 | 4 | Batch, Cost Center, Equipment, Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
