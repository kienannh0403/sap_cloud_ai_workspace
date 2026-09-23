# PM_other

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `PM` (không thuộc phân hệ ưu tiên nào trong Sheet1). `PM`: Plant Maintenance.

**69 view** · data category: (none) 52, Dimension 13, Fact 3, Cube 1 · loại: basic 33, text 18, dimension 13, fact 3, value_help 1, cube 1 · 3 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PM | 7 | top-level |
| PM-EQM-SF-MPC | 5 | top-level |
| PM-EQM-SF-WA | 3 | top-level |
| PM-PRM-MP | 12 | top-level |
| PM-WOC-MN | 22 | top-level |
| PM-WOC-MO | 20 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_MAINTORDERCOMPONENTDEX | Maintenance Order Component Data | PM-WOC-MO | Fact | 109 |
| I_MAINTENANCEITEM | Maintenance Item | PM-PRM-MP |  | 102 |
| I_MAINTENANCEORDERDEX | Maintenance Order Data | PM-WOC-MO | Fact | 92 |
| I_MAINTENANCENOTIFICATION | Maintenance Notification | PM-WOC-MN |  | 72 |
| I_MAINTORDCONFIRMATIONCUBE | Maintenance Order Confirmation - Cube | PM-WOC-MO | Cube | 71 |
| I_MAINTENANCEPLANBASIC | Maintenance Plan | PM-PRM-MP |  | 64 |
| I_PMNOTIFMAINTENANCEDATA | Notification Maintenance Data | PM-WOC-MN |  | 64 |
| I_MAINTENANCETASKLIST | Maintenance Task List | PM |  | 63 |
| I_MEASURINGPOINT | Measuring Point | PM-EQM-SF-MPC |  | 61 |
| I_MEASUREMENTDOCUMENT | Measurement Document | PM-EQM-SF-MPC |  | 60 |
| I_MAINTTASKLISTOPMATERIAL | Maintenance Task List Operation Material | PM |  | 38 |
| I_MAINTENANCEPLANSCHEDULE | Scheduled calls for Maintenance Plan | PM-PRM-MP |  | 31 |
| I_MAINTITEMOBJLISTTECHOBJ | Maintenance Item Object List with Technical Object | PM-PRM-MP |  | 24 |
| I_PMNOTIFICATIONTYPE | Maintenance Notification Types | PM-WOC-MN |  | 22 |
| I_MAINTTASKLISTGROUPCOUNTER | Maintenance Task List Group Counter | PM |  | 21 |
| I_MAINTENANCESTRATEGY | Maintenance Strategy | PM-PRM-MP |  | 21 |
| I_MAINTORDCHANGEDOCUMENTDEX | Maintenance Order Change Document | PM-WOC-MO | Fact | 20 |
| I_GENERICPRIORITY | Generic Priority | PM-WOC-MN |  | 14 |
| I_MSRGPTLASTMSMTDOCUMENT | Latest Measurement Document | PM-EQM-SF-MPC |  | 13 |
| I_MAINTENANCEPACKAGE | Maintenance Package | PM-PRM-MP |  | 13 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Equipment | 7 |
| MASTER | Task List (routing) group | 5 |
| MASTER | Material / Product | 5 |
| DOC | Order (production / maintenance / internal) | 5 |
| ORG | Plant | 4 |
| ORG | Controlling Area | 3 |
| ORG | Business Area | 2 |
| DOC | Sales Document | 2 |
| MASTER | WBS Element | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI-GL_General-Ledger | 2 | 3 | 3 | Order (production / maintenance / internal), Sales Document, Equipment, Material / Product, WBS Element |
| FI_other | 2 | 2 | 3 | Order (production / maintenance / internal), Sales Document, Material / Product, WBS Element |
| SD-SLS_Sales | 2 | 2 | 3 | Order (production / maintenance / internal), Sales Document, Material / Product, WBS Element |
| SD_other | 2 | 2 | 2 | Order (production / maintenance / internal), Sales Document, Material / Product, WBS Element |
| PP_other | 1 | 4 | 3 | Order (production / maintenance / internal), Equipment, Material / Product, Task List (routing) group, WBS Element |
| LE | 1 | 2 | 3 | Order (production / maintenance / internal), Material / Product, WBS Element |
| MM-PUR_Purchasing | 1 | 2 | 3 | Order (production / maintenance / internal), Material / Product, WBS Element |
| MM_other | 1 | 2 | 3 | Order (production / maintenance / internal), Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
