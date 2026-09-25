# PM_other

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `PM` (không thuộc phân hệ ưu tiên nào trong Sheet1). `PM`: Plant Maintenance.

**164 view** · data category: (none) 147, Dimension 13, Fact 3, Cube 1 · loại: basic 125, text 21, dimension 13, fact 3, value_help 1, cube 1 · 3 view có field DEPRECATED/DECOMMISSIONED · 95 view mới so với file xlsx của user · 8 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PM-2CL | 15 | top-level |
| PM-EQM-SF-MPC-2CL | 13 | top-level |
| PM-EQM-SF-WA-2CL | 8 | top-level |
| PM-PRM-MP-2CL | 25 | top-level |
| PM-PRM-TL-2CL | 13 | top-level |
| PM-WOC-2CL | 2 | top-level |
| PM-WOC-JC-2CL | 1 | top-level |
| PM-WOC-MN-2CL | 29 | top-level |
| PM-WOC-MO-2CL | 58 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_MAINTORDEROPERANDSUBOPER | Maintenance Order Operation and SubOper | PM-WOC-MO-2CL |  | 144 |
| I_MAINTORDERTECHOBJCUBE | Maintenance Order With Tech Object - Cube | PM-WOC-MO-2CL |  | 127 |
| I_MAINTORDEROPERATION_DEX | Maintenance Order Operation Data | PM-WOC-MO-2CL |  | 125 |
| I_MAINTENANCEORDERBASIC | Maintenance Order | PM-WOC-MO-2CL |  | 123 |
| I_MAINTORDERCOMPONENTDEX | Maintenance Order Component Data | PM-WOC-MO-2CL | Fact | 109 |
| I_MAINTENANCEITEM | Maintenance Item | PM-PRM-MP-2CL |  | 102 |
| I_MAINTENANCEORDERDEX | Maintenance Order Data | PM-WOC-MO-2CL | Fact | 92 |
| I_MAINTENANCENOTIFICATION | Maintenance Notification | PM-WOC-MN-2CL |  | 72 |
| I_MAINTORDCONFIRMATIONCUBE | Maintenance Order Confirmation - Cube | PM-WOC-MO-2CL | Cube | 71 |
| I_MAINTORDEROPERATIONBASIC | Maintenance Order Operation | PM-WOC-MO-2CL |  | 70 |
| C_MAINTTASKLISTOPERATIONDEX | Maintenance Task List Operation | PM-PRM-TL-2CL |  | 66 |
| I_MAINTENANCEPLANBASIC | Maintenance Plan | PM-PRM-MP-2CL |  | 64 |
| I_PMNOTIFMAINTENANCEDATA | Notification Maintenance Data | PM-WOC-MN-2CL |  | 64 |
| I_MAINTENANCETASKLIST | Maintenance Task List | PM-2CL |  | 63 |
| I_MEASURINGPOINT | Measuring Point | PM-EQM-SF-MPC-2CL |  | 61 |
| I_MEASUREMENTDOCUMENT | Measurement Document | PM-EQM-SF-MPC-2CL |  | 60 |
| C_MAINTENANCETASKLISTDEX | Maintenance Task List Data for DEX | PM-PRM-TL-2CL |  | 47 |
| I_MAINTTASKLISTOPMATERIAL | Maintenance Task List Operation Material | PM-2CL |  | 38 |
| I_MAINTORDEROPPHASECONTROL | Maintenance Order Op Phase Controls | PM-WOC-MO-2CL |  | 32 |
| I_MAINTENANCEPLANSCHEDULE | Scheduled calls for Maintenance Plan | PM-PRM-MP-2CL |  | 31 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Equipment | 15 |
| DOC | Order (production / maintenance / internal) | 15 |
| ORG | Plant | 10 |
| ORG | Controlling Area | 9 |
| MASTER | Task List (routing) group | 9 |
| ORG | Business Area | 7 |
| MASTER | Material / Product | 7 |
| MASTER | Material Group | 5 |
| ORG | Purchasing Organization | 5 |
| MASTER | Supplier | 5 |
| ORG | Functional Area | 5 |
| ORG | Profit Center | 5 |
| MASTER | WBS Element | 5 |
| MASTER | Activity Type | 4 |
| ORG | Company Code | 4 |
| DOC | Sales Document | 2 |
| DOC | Purchasing Document | 2 |
| MASTER | Cost Center | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO_other | 3 | 7 | 7 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Cost Center, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| FI_other | 3 | 6 | 6 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| FIN | 3 | 5 | 6 | Order (production / maintenance / internal), Purchasing Document, Sales Document, Activity Type, Cost Center, Material / Product, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 6 | 7 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| PP_other | 2 | 6 | 7 | Order (production / maintenance / internal), Purchasing Document, Equipment, Material / Product, Material Group, Supplier, Task List (routing) group, WBS Element |
| FI-GL_General-Ledger | 2 | 6 | 5 | Order (production / maintenance / internal), Sales Document, Activity Type, Cost Center, Equipment, Material / Product, Supplier, WBS Element |
| MM_other | 2 | 5 | 7 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, Material / Product, Supplier, WBS Element |
| SD-BIL_Billing | 2 | 5 | 5 | Order (production / maintenance / internal), Sales Document, Cost Center, Material / Product, Material Group, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
