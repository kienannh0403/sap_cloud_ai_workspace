# EAM-OBJ_Technical-Objects — Technical Objects

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `EAM-OBJ` = **Technical Objects**.

**63 view** · data category: (none) 53, Dimension 10 · loại: basic 36, dimension 10, text 9, value_help 8 · 1 view có field DEPRECATED/DECOMMISSIONED · 35 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PM-EQM-EQ-2CL | 54 | alias |
| PM-EQM-FL-2CL | 9 | alias |

> `alias` = component khác tên trong Sheet1 nhưng cùng nội dung (xem `module_map.md`); `keyword` = **suy luận theo tên view**, độ tin cậy thấp hơn `component`.

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_TECHNICALOBJECT | Technical Object | PM-EQM-EQ-2CL | Dimension | 85 |
| I_EQUIPMENT | Equipment | PM-EQM-EQ-2CL | Dimension | 72 |
| I_FUNCTIONALLOCATION | Functional Location | PM-EQM-FL-2CL | Dimension | 61 |
| I_LOCATIONACCOUNTASSIGNMENT | Location and Account Assignment | PM-EQM-FL-2CL | Dimension | 54 |
| C_FUNCNLLOCCLFNCHARCVALUEDEX | Floc Charc Values Data Extraction | PM-EQM-EQ-2CL |  | 32 |
| C_EQUIPMENTCLFNCHARCVALUEDEX | Equipment Charac Values Data Extraction | PM-EQM-EQ-2CL |  | 31 |
| I_EQUIPMENTCATEGORY | Equipment Category | PM-EQM-EQ-2CL | Dimension | 12 |
| I_EQUIPMENTSTATUS | Equipment Status | PM-EQM-EQ-2CL |  | 10 |
| I_EQUIPMENTTEXTDEX | Data Extraction for Equipment - Text | PM-EQM-EQ-2CL |  | 10 |
| I_FUNCLOCATIONSTRUCTURE | Functional Location Structure | PM-EQM-FL-2CL |  | 7 |
| I_TECHOBJISEQUIPORFUNCNLLOCT | Tech Object is Equi or Func Loc - Text | PM-EQM-EQ-2CL |  | 5 |
| I_FUNCNLLOCATIONHIERARCHYNODE | Functional Location Hiearchy Interface | PM-EQM-FL-2CL |  | 5 |
| I_FUNCTIONALLOCATIONCATEGORY | Functional Location Category | PM-EQM-FL-2CL | Dimension | 5 |
| I_ABCINDICATOR | ABC Indicator | PM-EQM-EQ-2CL |  | 3 |
| I_TECHNICALOBJECTTYPE | Techncial Object Type | PM-EQM-EQ-2CL | Dimension | 3 |
| I_TECHOBJAUTHZNGRP | Technical Object Authorization Group | PM-EQM-EQ-2CL | Dimension | 2 |
| I_TECHOBJINSPECTIONLEVELCODE | Technical Object Inspection Level | PM-EQM-EQ-2CL | Dimension | 2 |
| I_TECHOBJISEQUIPORFUNCNLLOC | Technical Object is Equi or Func Loc | PM-EQM-EQ-2CL | Dimension | 2 |
| D_EQUIPCRTEMASSMATLSRLNMBRP | Abstract Parameter for Mass Create | PM-EQM-EQ-2CL |  | 0 |
| D_EQUIPCRTEMASSMATLSRLNMBRR | Abstract Result for Mass Create | PM-EQM-EQ-2CL |  | 0 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Equipment | 7 |
| ORG | Company Code | 3 |
| MASTER | Material / Product | 3 |
| ORG | Distribution Channel | 2 |
| ORG | Division | 2 |
| ORG | Sales Group | 2 |
| ORG | Sales Office | 2 |
| ORG | Sales Organization | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LO_other | 0 | 2 | 6 | Equipment, Material / Product |
| CRM | 0 | 2 | 4 | Equipment, Material / Product |
| FI-GL_General-Ledger | 0 | 2 | 4 | Equipment, Material / Product |
| QM | 0 | 2 | 2 | Equipment, Material / Product |
| PM_other | 0 | 2 | 1 | Equipment, Material / Product |
| PP_other | 0 | 2 | 1 | Equipment, Material / Product |
| CO_other | 0 | 1 | 6 | Material / Product |
| SD-BIL_Billing | 0 | 1 | 6 | Material / Product |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
