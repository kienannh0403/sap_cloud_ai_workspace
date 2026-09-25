# PLM

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `PLM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**33 view** · data category: (none) 33 · loại: basic 30, value_help 2, text 1 · 0 view có field DEPRECATED/DECOMMISSIONED · 30 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PLM-CR-2CL | 17 | top-level |
| PLM-WUI-OBJ-ECN-2CL | 16 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| C_CHANGEMASTERDEX_2 | Engineering Change Master | PLM-WUI-OBJ-ECN-2CL |  | 34 |
| C_CHANGERECDMAILTMPLFORAPPRVL | Email Template for Approval | PLM-CR-2CL |  | 20 |
| C_CHANGERECORDEMAILTEMPLATE | Change record email template helper | PLM-CR-2CL |  | 18 |
| C_CHANGEMSTROBJMGMTRECORDDEX | Object Management Rec of Change Master | PLM-WUI-OBJ-ECN-2CL |  | 16 |
| C_CHGRECHDREXTENSIONDEX | Change Record Header Ext for DEX | PLM-CR-2CL |  | 12 |
| C_CHANGERECORDFLEXIBLEWORKFLOW | Change Record Flexible Workflow | PLM-CR-2CL |  | 10 |
| C_CHANGEMASTERSTATUSDEX | Change Master Status | PLM-WUI-OBJ-ECN-2CL |  | 5 |
| C_CHANGEMASTERSTATUSTEXTDEX | Change Master Status - Text | PLM-WUI-OBJ-ECN-2CL |  | 4 |
| C_CHANGERECORDDESCDEX | Extraction for change record description | PLM-CR-2CL |  | 3 |
| C_CHANGERECORDHIERARCHYDEX | Change Record Hierarchy | PLM-CR-2CL |  | 2 |
| C_CHANGERECORDITEMDEX_2 | Change Record General Item Details | PLM-CR-2CL |  | 2 |
| C_CHANGERECORDBOMITEMDEX | Extraction BOM as Item for Change Record | PLM-CR-2CL |  | 1 |
| C_CHANGERECORDDEX_2 | Change Record Header Extraction | PLM-CR-2CL |  | 1 |
| C_CHANGERECORDDOCITEMDEX | Change Record Document as Item | PLM-CR-2CL |  | 1 |
| C_CHANGERECORDPRODUCTITEMDEX | Change Record Product as Item | PLM-CR-2CL |  | 1 |
| C_CHANGERECORDCHARCDEX | Change Record Characteristics Extraction | PLM-CR-2CL |  | 0 |
| C_CHANGERECORDCLASSDEX | Change Record Class Extraction | PLM-CR-2CL |  | 0 |
| C_CHANGERECORDLONGTEXTDEX_2 | Change Record Long Text | PLM-CR-2CL |  | 0 |
| C_CHANGERECORDORDERBOMDEX | Change Record Sales Order BOM Extraction | PLM-CR-2CL |  | 0 |
| C_CHANGERECORDPARTNERDEX_2 | Change Record Partner or Person Resp | PLM-CR-2CL |  | 0 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
