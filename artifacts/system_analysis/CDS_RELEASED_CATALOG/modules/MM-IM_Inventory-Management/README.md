# MM-IM_Inventory-Management — Inventory Management

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `MM-IM` = **Inventory Management**.

**101 view** · data category: (none) 60, Dimension 34, Cube 7 · loại: basic 41, dimension 34, text 16, cube 7, value_help 3 · 4 view có field DEPRECATED/DECOMMISSIONED · 28 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| MM-IM-GF-2CL | 22 | component |
| MM-IM-PI-2CL | 12 | component |
| MM-IM-RS-2CL | 9 | component |
| MM-IM-VDM-PI-2CL | 26 | component |
| MM-IM-VDM-RSV-2CL | 3 | component |
| MM-IM-VDM-SGM-2CL | 29 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_GOODSMOVEMENTCUBE | Analytics of Goods Movements - Cube | MM-IM-VDM-SGM-2CL | Cube | 156 |
| I_MATERIALDOCUMENTITEM_2 | Material Document Item | MM-IM-VDM-SGM-2CL | Dimension | 152 |
| I_PHYSINVTRYCUBE | Physical Inventory - Cube | MM-IM-VDM-PI-2CL | Cube | 90 |
| I_PHYSINVTRYDOCITEM | Physical Inventory Document Item | MM-IM-VDM-PI-2CL | Dimension | 87 |
| I_RESERVATIONDOCUMENTITEM | Reservation Document Item | MM-IM-VDM-RSV-2CL | Dimension | 75 |
| I_RESERVATIONDOCUMENTHEADER | Reservation Document Header | MM-IM-VDM-RSV-2CL | Dimension | 39 |
| I_PHYSINVTRYDOCHEADER | Physical Inventory Document Header | MM-IM-VDM-PI-2CL | Dimension | 38 |
| I_MATERIALSTOCK_2 | Material Stock Calculation | MM-IM-VDM-SGM-2CL | Cube | 37 |
| V_MMIM_DDL_OM_PARAM | Good Movement Parameter | MM-IM-GF-2CL |  | 35 |
| I_MATLSTKATKEYDATEINALTUOM | Stock At Key Date In Alternative UoM | MM-IM-VDM-SGM-2CL | Cube | 34 |
| I_STOCKQUANTITYCURRENTVALUE_2 | Current Stock Quantity and Value | MM-IM-VDM-SGM-2CL | Cube | 33 |
| I_MATERIALSTOCKTIMESERIES | Material Stock For Periods | MM-IM-VDM-SGM-2CL | Cube | 31 |
| I_MATERIALDOCUMENTHEADER_2 | Material Document Header | MM-IM-VDM-SGM-2CL | Dimension | 28 |
| V_MMIM_DDL_OM_OR_EMAIL | Output Management Material Documents E-Mail | MM-IM-GF-2CL |  | 18 |
| I_STOCKQUANTITYVALUEBYTYPE | Stock Quantity and Value by Type | MM-IM-VDM-SGM-2CL | Cube | 18 |
| V_MMIM_DDL_OM_OR_GR4PO_EMAIL | Output Management Material Documents E-Mail | MM-IM-GF-2CL |  | 12 |
| V_MMIM_DDL_OM_PARAM_PI | Good Movement Parameter | MM-IM-GF-2CL |  | 10 |
| I_GOODSMOVEMENTTYPE | Goods Movement Type | MM-IM-VDM-SGM-2CL | Dimension | 9 |
| I_CONTROLOFQUANTITYVALUEUPDATE | Control of quantity and value update | MM-IM-GF-2CL |  | 8 |
| I_CUSTOMERCOMPANYBYPLANT | Customer Company by Plant | MM-IM-GF-2CL |  | 7 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 22 |
| ORG | Storage Location | 14 |
| CONFIG | Movement Type | 14 |
| ORG | Company Code | 9 |
| CONFIG | Fiscal Year | 8 |
| MASTER | Material / Product | 7 |
| MASTER | Batch | 6 |
| MASTER | WBS Element | 5 |
| ORG | Valuation Area | 4 |
| DOC | Purchasing Document | 4 |
| ORG | Controlling Area | 3 |
| MASTER | Cost Center | 3 |
| ORG | Profit Center | 3 |
| MASTER | G/L Account | 3 |
| MASTER | Supplier | 2 |
| DOC | Order (production / maintenance / internal) | 2 |
| MASTER | Profitability Segment | 2 |
| MASTER | Material Group | 2 |
| DOC | Delivery | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| MM-PUR_Purchasing | 3 | 8 | 5 | Delivery, Order (production / maintenance / internal), Purchasing Document, Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| PP_other | 3 | 6 | 5 | Delivery, Order (production / maintenance / internal), Purchasing Document, Batch, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| FI_other | 2 | 8 | 5 | Order (production / maintenance / internal), Purchasing Document, Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| LE | 2 | 8 | 4 | Delivery, Order (production / maintenance / internal), Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| SD_other | 2 | 7 | 5 | Delivery, Order (production / maintenance / internal), Batch, Cost Center, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| CO_other | 2 | 6 | 5 | Order (production / maintenance / internal), Purchasing Document, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| FIN | 2 | 5 | 5 | Order (production / maintenance / internal), Purchasing Document, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| MM_other | 2 | 5 | 4 | Order (production / maintenance / internal), Purchasing Document, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
