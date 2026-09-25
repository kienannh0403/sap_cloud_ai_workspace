# LO-MD-BOM_Bill-of-Material — Bill of Material

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `LO-MD-BOM` = **Bill of Material**.

**63 view** · data category: (none) 62, Fact 1 · loại: basic 57, text 3, value_help 2, fact 1 · 0 view có field DEPRECATED/DECOMMISSIONED · 56 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| LO-MD-BOM-2CL | 63 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_BOMCOMPONENTWITHKEYDATE | Bill of Material Component Details | LO-MD-BOM-2CL |  | 107 |
| I_BILLOFMATERIALITEMDEX_3 | Data Extraction for BOM Item | LO-MD-BOM-2CL |  | 98 |
| I_MATLBILLOFMATERIALITEMDEX | Bill of Material Item Extraction | LO-MD-BOM-2CL |  | 98 |
| I_SALESORDERBOMITEMDEX | Sales Order BOM Item Extraction | LO-MD-BOM-2CL |  | 98 |
| I_WBSBILLOFMATERIALITEMDEX | WBS BOM Item Extraction | LO-MD-BOM-2CL |  | 98 |
| I_BILLOFMATERIALITEMBASIC | Bill of Material Item Details | LO-MD-BOM-2CL |  | 97 |
| I_BILLOFMATERIALWITHKEYDATE | Bill of Material Header Details | LO-MD-BOM-2CL |  | 49 |
| I_BILLOFMATERIALHEADERDEX_2 | Data Extraction for BOM Header | LO-MD-BOM-2CL |  | 40 |
| I_MATBILLOFMATERIALHEADERDEX | Data Extraction for BOM Header | LO-MD-BOM-2CL |  | 40 |
| I_SALESORDERBOMHEADERDEX | Sales Order BOM Header Extraction | LO-MD-BOM-2CL |  | 40 |
| I_WBSBILLOFMATERIALHEADERDEX | WBS BOM Header Extraction | LO-MD-BOM-2CL |  | 40 |
| I_MATLBILLOFMATERIALCHANGEHIST | BOM Change document retrieval | LO-MD-BOM-2CL |  | 28 |
| I_MATERIALBOMLINK | Material Link for Bill of Material | LO-MD-BOM-2CL | Fact | 13 |
| I_MATERIALBOMLINKDEX_2 | Bill of Material Link Data Extraction | LO-MD-BOM-2CL |  | 13 |
| I_SALESORDERBOMLINKDEX_2 | Sales Order BOM Link extraction | LO-MD-BOM-2CL |  | 12 |
| I_WBSBILLOFMATERIALLINKDEX | WBS BOM Link Data Extraction | LO-MD-BOM-2CL |  | 11 |
| I_BILLOFMATERIALSUBITEMSBASIC | Bill of Material Sub items Details | LO-MD-BOM-2CL |  | 9 |
| I_BOMVARIANTUSAGE | Bill Of Material Usage | LO-MD-BOM-2CL |  | 9 |
| I_MATERIALBOMSUBITEMDEX | Data Extraction For BOM Subitem | LO-MD-BOM-2CL |  | 9 |
| I_PROJECTBOMSUBITEMDEX | WBS BOM Subitem Extraction | LO-MD-BOM-2CL |  | 9 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Material / Product | 11 |
| ORG | Plant | 10 |
| MASTER | Material Group | 6 |
| ORG | Purchasing Organization | 6 |
| MASTER | Supplier | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO_other | 0 | 3 | 2 | Material / Product, Material Group, Supplier |
| MM-PUR_Purchasing | 0 | 3 | 2 | Material / Product, Material Group, Supplier |
| PM_other | 0 | 3 | 2 | Material / Product, Material Group, Supplier |
| PP_other | 0 | 3 | 2 | Material / Product, Material Group, Supplier |
| FI_other | 0 | 3 | 1 | Material / Product, Material Group, Supplier |
| LE | 0 | 3 | 1 | Material / Product, Material Group, Supplier |
| MM-IM_Inventory-Management | 0 | 3 | 1 | Material / Product, Material Group, Supplier |
| PP-SFC_Shop-Floor-Control | 0 | 3 | 1 | Material / Product, Material Group, Supplier |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
