# PP-MRP_MRP — MRP

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `PP-MRP` = **MRP**.

**71 view** · data category: Dimension 40, (none) 29, Fact 2 · loại: dimension 40, text 22, value_help 5, fact 2, basic 2 · 5 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PP-FIO | 6 | keyword |
| PP-MRP | 3 | component |
| PP-PMR-ENG | 6 | keyword |
| PP-VDM | 56 | keyword |

> `alias` = component khác tên trong Sheet1 nhưng cùng nội dung (xem `module_map.md`); `keyword` = **suy luận theo tên view**, độ tin cậy thấp hơn `component`.

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PLANNEDORDERCOMPONENT | Planned Order Component | PP-VDM | Dimension | 192 |
| I_PLANNEDORDER | Planned Order | PP-VDM | Dimension | 186 |
| I_PRODUCTMRPAREA | MRP Area Details of a Product | PP-VDM | Dimension | 62 |
| I_PLANNEDORDERCAPACITY | Planned Order Capacity | PP-VDM | Dimension | 49 |
| I_PLNDINDEPRQMTBYINTKEY | Planned Independent Requirement by Internal Key | PP-VDM | Dimension | 40 |
| I_PLNDINDEPRQMTITEMHISTORY | History of Planned Independent Requirement Items | PP-VDM |  | 39 |
| I_ACTIVEPLNDINDEPRQMT | Active Planned Independent Requirement | PP-VDM | Dimension | 34 |
| I_MRPMASTERDATAISSUEBASIC | Master Data Related Issues of an MRP Run | PP-MRP | Fact | 26 |
| I_MRPGROUPCONTROLPARAMETER | MRP Group Control Parameter | PP-VDM |  | 26 |
| I_MRPPLANTCONTROLPARAMETER | MRP Plant Control Parameters | PP-VDM | Dimension | 24 |
| I_MRPCONTROLLER | MRP Controller | PP-VDM | Dimension | 14 |
| I_MRPAREAPLANNINGFILEENTRY | MRP Area Planning File Entry | PP-VDM | Fact | 13 |
| I_ACTIVEPLNDINDEPRQMTITEM | Active Planned Independent Requirement Item | PP-VDM | Dimension | 12 |
| I_MRPPLANNINGPERIOD | MRP Planning Period | PP-VDM | Dimension | 12 |
| I_PLNDINDEPRQMTITEMBYINTKEY | Planned Independent Requirement Item by Internal Key | PP-VDM | Dimension | 12 |
| I_MRPPLANNINGSCENARIO | MRP Planning Scenario | PP-VDM | Dimension | 11 |
| I_MRPAREA | MRP Area | PP-VDM | Dimension | 10 |
| I_MRPLOTSIZINGPROCEDURE | MRP Lot Sizing Procedure | PP-VDM | Dimension | 8 |
| I_PRODFORECASTREQUIREMENTSSPLT | Product Forecast Requirements Split | PP-VDM | Dimension | 7 |
| I_MRPAREASTORAGELOCATION | MRP Area Storage Location | PP-VDM | Dimension | 6 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 17 |
| MASTER | Material / Product | 8 |
| MASTER | WBS Element | 4 |
| ORG | Business Area | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI-GL_General-Ledger | 0 | 2 | 2 | Material / Product, WBS Element |
| FI_other | 0 | 2 | 2 | Material / Product, WBS Element |
| LE | 0 | 2 | 2 | Material / Product, WBS Element |
| MM-PUR_Purchasing | 0 | 2 | 2 | Material / Product, WBS Element |
| MM_other | 0 | 2 | 2 | Material / Product, WBS Element |
| PM_other | 0 | 2 | 2 | Material / Product, WBS Element |
| PP-SFC_Shop-Floor-Control | 0 | 2 | 2 | Material / Product, WBS Element |
| PP_other | 0 | 2 | 2 | Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
