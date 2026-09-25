# QM

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `QM` (không thuộc phân hệ ưu tiên nào trong Sheet1). `QM`: Quality Management.

**233 view** · data category: (none) 203, Dimension 30 · loại: basic 118, text 64, dimension 27, value_help 24 · 4 view có field DEPRECATED/DECOMMISSIONED · 60 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| QM-2CL | 3 | top-level |
| QM-CA-2CL | 3 | top-level |
| QM-IM-2CL | 101 | top-level |
| QM-PT-2CL | 93 | top-level |
| QM-QC-2CL | 1 | top-level |
| QM-QN-2CL | 32 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_INSPECTIONLOT | Inspection Lot | QM-IM-2CL |  | 239 |
| I_INSPECTIONLOTVALUEHELP | Inspection Lot | QM-IM-2CL |  | 139 |
| I_INSPSPECIFICATIONVERSION | Version of Master Insp Characteristic | QM-PT-2CL |  | 129 |
| I_INSPECTIONCHARACTERISTIC | Characteristic in Inspection Lot | QM-IM-2CL |  | 128 |
| I_INSPPLANOPCHARCVERSION_2 | Version of Insp Plan Characteristic | QM-PT-2CL |  | 118 |
| I_DEFECT | Defect | QM-QN-2CL | Dimension | 103 |
| I_QLTYNOTIFICATION | Quality Notification | QM-QN-2CL |  | 100 |
| I_INSPECTIONRESULT | Summarized Insp Result for an Insp Charc | QM-IM-2CL |  | 77 |
| I_INSPSUBSETRESULT | Insp Result for an Inspection Point | QM-IM-2CL |  | 77 |
| I_QUALITYINPROCUREMENT | Quality Info Record in Procurement | QM-PT-2CL |  | 62 |
| I_INSPECTIONRESULTVALUE | Single Value of an Inspection Charc Rslt | QM-IM-2CL |  | 60 |
| I_QUALITYNOTIFICATIONITEM | Quality Notification Item | QM-QN-2CL | Dimension | 60 |
| I_INSPECTIONSUBSET | Inspection Point of Inspection Operation | QM-IM-2CL |  | 59 |
| I_QUALITYTASK | Quality Task | QM-QN-2CL | Dimension | 58 |
| I_INSPECTIONPLANVERSION | Version of Inspection Plan | QM-PT-2CL |  | 53 |
| I_QLTYNOTIFICATIONTASK | Quality Notification Task | QM-QN-2CL |  | 53 |
| I_QUALITYLEVEL | Quality Level | QM-IM-2CL |  | 52 |
| I_SAMPLINGPROCEDURE | Sampling Procedure | QM-PT-2CL | Dimension | 43 |
| I_INSPPLANOPERATIONVERSION_2 | Version of Inspection Plan Operation | QM-PT-2CL |  | 34 |
| I_INSPLOTUSAGEDECISION | Usage Decision for Inspection Lot | QM-IM-2CL |  | 33 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 24 |
| DOC | Inspection Lot | 22 |
| MASTER | Material / Product | 7 |
| MASTER | Task List (routing) group | 6 |
| MASTER | Equipment | 5 |
| MASTER | Batch | 4 |
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
| PP-SFC_Shop-Floor-Control | 1 | 6 | 5 | Inspection Lot, Batch, Cost Center, G/L Account, Material / Product, Task List (routing) group, WBS Element |
| LE | 1 | 5 | 6 | Inspection Lot, Batch, Cost Center, G/L Account, Material / Product, WBS Element |
| LO_other | 1 | 4 | 5 | Inspection Lot, Batch, Equipment, G/L Account, Material / Product |
| SD-BIL_Billing | 0 | 5 | 7 | Batch, Cost Center, G/L Account, Material / Product, WBS Element |
| CO_other | 0 | 5 | 6 | Cost Center, G/L Account, Material / Product, Task List (routing) group, WBS Element |
| FI_other | 0 | 5 | 6 | Batch, Cost Center, G/L Account, Material / Product, WBS Element |
| MM-PUR_Purchasing | 0 | 5 | 6 | Batch, Cost Center, G/L Account, Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
