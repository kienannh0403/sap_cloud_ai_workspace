# PP-MRP_MRP — MRP

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `PP-MRP` = **MRP**.

**93 view** · data category: (none) 51, Dimension 40, Fact 2 · loại: dimension 40, text 27, basic 15, value_help 9, fact 2 · 5 view có field DEPRECATED/DECOMMISSIONED · 22 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PP-FIO-2CL | 6 | keyword |
| PP-MP-DEM-2CL | 6 | keyword |
| PP-MRP-2CL | 3 | component |
| PP-PLO-2CL | 6 | keyword |
| PP-PMR-ENG-2CL | 6 | keyword |
| PP-VDM-2CL | 66 | keyword |

> `alias` = component khác tên trong Sheet1 nhưng cùng nội dung (xem `module_map.md`); `keyword` = **suy luận theo tên view**, độ tin cậy thấp hơn `component`.

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PLANNEDORDERCOMPONENT | Planned Order Component | PP-VDM-2CL | Dimension | 192 |
| I_PLANNEDORDER | Planned Order | PP-VDM-2CL | Dimension | 186 |
| I_PRODUCTMRPAREA | MRP Area Details of a Product | PP-VDM-2CL | Dimension | 62 |
| I_PLANNEDORDERCAPACITY | Planned Order Capacity | PP-VDM-2CL | Dimension | 49 |
| I_PLNDINDEPRQMTBYINTKEY | Planned Independent Requirement by Internal Key | PP-VDM-2CL | Dimension | 40 |
| I_PLNDINDEPRQMTITEMHISTORY | History of Planned Independent Requirement Items | PP-VDM-2CL |  | 39 |
| I_ACTIVEPLNDINDEPRQMT | Active Planned Independent Requirement | PP-VDM-2CL | Dimension | 34 |
| I_MRPMASTERDATAISSUEBASIC | Master Data Related Issues of an MRP Run | PP-MRP-2CL | Fact | 26 |
| I_MRPGROUPCONTROLPARAMETER | MRP Group Control Parameter | PP-VDM-2CL |  | 26 |
| I_MRPPLANTCONTROLPARAMETER | MRP Plant Control Parameters | PP-VDM-2CL | Dimension | 24 |
| I_MRPCONTROLLER | MRP Controller | PP-VDM-2CL | Dimension | 14 |
| I_MRPAREAPLANNINGFILEENTRY | MRP Area Planning File Entry | PP-VDM-2CL | Fact | 13 |
| I_ACTIVEPLNDINDEPRQMTITEM | Active Planned Independent Requirement Item | PP-VDM-2CL | Dimension | 12 |
| I_MRPPLANNINGPERIOD | MRP Planning Period | PP-VDM-2CL | Dimension | 12 |
| I_PLNDINDEPRQMTITEMBYINTKEY | Planned Independent Requirement Item by Internal Key | PP-VDM-2CL | Dimension | 12 |
| I_MRPPLANNINGSCENARIO | MRP Planning Scenario | PP-VDM-2CL | Dimension | 11 |
| I_MRPAREA | MRP Area | PP-VDM-2CL | Dimension | 10 |
| I_MRPLOTSIZINGPROCEDURE | MRP Lot Sizing Procedure | PP-VDM-2CL | Dimension | 8 |
| I_MRPEXCEPTIONMESSAGE | MRP Exception Message | PP-VDM-2CL |  | 7 |
| I_PRODFORECASTREQUIREMENTSSPLT | Product Forecast Requirements Split | PP-VDM-2CL | Dimension | 7 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 19 |
| MASTER | Material / Product | 8 |
| MASTER | WBS Element | 4 |
| ORG | Business Area | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO_other | 0 | 2 | 2 | Material / Product, WBS Element |
| FI-GL_General-Ledger | 0 | 2 | 2 | Material / Product, WBS Element |
| FIN | 0 | 2 | 2 | Material / Product, WBS Element |
| FI_other | 0 | 2 | 2 | Material / Product, WBS Element |
| LE | 0 | 2 | 2 | Material / Product, WBS Element |
| MM-PUR_Purchasing | 0 | 2 | 2 | Material / Product, WBS Element |
| MM_other | 0 | 2 | 2 | Material / Product, WBS Element |
| PM_other | 0 | 2 | 2 | Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
