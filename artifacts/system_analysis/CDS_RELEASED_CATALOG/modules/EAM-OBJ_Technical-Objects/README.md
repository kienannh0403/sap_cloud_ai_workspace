# EAM-OBJ_Technical-Objects — Technical Objects

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `EAM-OBJ` = **Technical Objects**.

**28 view** · data category: (none) 18, Dimension 10 · loại: dimension 10, text 8, value_help 5, basic 5 · 1 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PM-EQM-EQ | 20 | alias |
| PM-EQM-FL | 8 | alias |

> `alias` = component khác tên trong Sheet1 nhưng cùng nội dung (xem `module_map.md`); `keyword` = **suy luận theo tên view**, độ tin cậy thấp hơn `component`.

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_TECHNICALOBJECT | Technical Object | PM-EQM-EQ | Dimension | 85 |
| I_EQUIPMENT | Equipment | PM-EQM-EQ | Dimension | 72 |
| I_FUNCTIONALLOCATION | Functional Location | PM-EQM-FL | Dimension | 61 |
| I_LOCATIONACCOUNTASSIGNMENT | Location and Account Assignment | PM-EQM-FL | Dimension | 54 |
| I_EQUIPMENTCATEGORY | Equipment Category | PM-EQM-EQ | Dimension | 12 |
| I_EQUIPMENTSTATUS | Equipment Status | PM-EQM-EQ |  | 10 |
| I_EQUIPMENTTEXTDEX | Data Extraction for Equipment - Text | PM-EQM-EQ |  | 10 |
| I_FUNCLOCATIONSTRUCTURE | Functional Location Structure | PM-EQM-FL |  | 7 |
| I_TECHOBJISEQUIPORFUNCNLLOCT | Tech Object is Equi or Func Loc - Text | PM-EQM-EQ |  | 5 |
| I_FUNCNLLOCATIONHIERARCHYNODE | Functional Location Hiearchy Interface | PM-EQM-FL |  | 5 |
| I_FUNCTIONALLOCATIONCATEGORY | Functional Location Category | PM-EQM-FL | Dimension | 5 |
| I_TECHNICALOBJECTTYPE | Techncial Object Type | PM-EQM-EQ | Dimension | 3 |
| I_TECHOBJAUTHZNGRP | Technical Object Authorization Group | PM-EQM-EQ | Dimension | 2 |
| I_TECHOBJINSPECTIONLEVELCODE | Technical Object Inspection Level | PM-EQM-EQ | Dimension | 2 |
| I_TECHOBJISEQUIPORFUNCNLLOC | Technical Object is Equi or Func Loc | PM-EQM-EQ | Dimension | 2 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Equipment | 6 |
| MASTER | Material / Product | 2 |
| ORG | Distribution Channel | 2 |
| ORG | Division | 2 |
| ORG | Sales Group | 2 |
| ORG | Sales Office | 2 |
| ORG | Sales Organization | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LO_other | 0 | 2 | 5 | Equipment, Material / Product |
| CRM | 0 | 2 | 3 | Equipment, Material / Product |
| FI-GL_General-Ledger | 0 | 2 | 3 | Equipment, Material / Product |
| QM | 0 | 2 | 1 | Equipment, Material / Product |
| PM_other | 0 | 2 | 0 | Equipment, Material / Product |
| PP_other | 0 | 2 | 0 | Equipment, Material / Product |
| LE | 0 | 1 | 5 | Material / Product |
| SD-SLS_Sales | 0 | 1 | 5 | Material / Product |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
