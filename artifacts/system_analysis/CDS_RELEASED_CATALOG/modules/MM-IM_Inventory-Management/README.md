# MM-IM_Inventory-Management — Inventory Management

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `MM-IM` = **Inventory Management**.

**73 view** · data category: Dimension 34, (none) 32, Cube 7 · loại: dimension 34, basic 16, text 16, cube 7 · 4 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| MM-IM-GF | 13 | component |
| MM-IM-RS | 4 | component |
| MM-IM-VDM-PI | 24 | component |
| MM-IM-VDM-RSV | 3 | component |
| MM-IM-VDM-SGM | 29 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_GOODSMOVEMENTCUBE | Analytics of Goods Movements - Cube | MM-IM-VDM-SGM | Cube | 156 |
| I_MATERIALDOCUMENTITEM_2 | Material Document Item | MM-IM-VDM-SGM | Dimension | 152 |
| I_PHYSINVTRYCUBE | Physical Inventory - Cube | MM-IM-VDM-PI | Cube | 90 |
| I_PHYSINVTRYDOCITEM | Physical Inventory Document Item | MM-IM-VDM-PI | Dimension | 87 |
| I_RESERVATIONDOCUMENTITEM | Reservation Document Item | MM-IM-VDM-RSV | Dimension | 75 |
| I_RESERVATIONDOCUMENTHEADER | Reservation Document Header | MM-IM-VDM-RSV | Dimension | 39 |
| I_PHYSINVTRYDOCHEADER | Physical Inventory Document Header | MM-IM-VDM-PI | Dimension | 38 |
| I_MATERIALSTOCK_2 | Material Stock Calculation | MM-IM-VDM-SGM | Cube | 37 |
| V_MMIM_DDL_OM_PARAM | Good Movement Parameter | MM-IM-GF |  | 35 |
| I_MATLSTKATKEYDATEINALTUOM | Stock At Key Date In Alternative UoM | MM-IM-VDM-SGM | Cube | 34 |
| I_STOCKQUANTITYCURRENTVALUE_2 | Current Stock Quantity and Value | MM-IM-VDM-SGM | Cube | 33 |
| I_MATERIALSTOCKTIMESERIES | Material Stock For Periods | MM-IM-VDM-SGM | Cube | 31 |
| I_MATERIALDOCUMENTHEADER_2 | Material Document Header | MM-IM-VDM-SGM | Dimension | 28 |
| V_MMIM_DDL_OM_OR_EMAIL | Output Management Material Documents E-Mail | MM-IM-GF |  | 18 |
| I_STOCKQUANTITYVALUEBYTYPE | Stock Quantity and Value by Type | MM-IM-VDM-SGM | Cube | 18 |
| V_MMIM_DDL_OM_OR_GR4PO_EMAIL | Output Management Material Documents E-Mail | MM-IM-GF |  | 12 |
| V_MMIM_DDL_OM_PARAM_PI | Good Movement Parameter | MM-IM-GF |  | 10 |
| I_GOODSMOVEMENTTYPE | Goods Movement Type | MM-IM-VDM-SGM | Dimension | 9 |
| I_CONTROLOFQUANTITYVALUEUPDATE | Control of quantity and value update | MM-IM-GF |  | 8 |
| I_CUSTOMERCOMPANYBYPLANT | Customer Company by Plant | MM-IM-GF |  | 7 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Plant | 20 |
| ORG | Storage Location | 14 |
| CONFIG | Movement Type | 14 |
| ORG | Company Code | 9 |
| MASTER | Material / Product | 7 |
| MASTER | Batch | 6 |
| CONFIG | Fiscal Year | 6 |
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
| LE | 2 | 8 | 4 | Delivery, Order (production / maintenance / internal), Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| SD_other | 2 | 7 | 3 | Delivery, Order (production / maintenance / internal), Batch, Cost Center, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| MM_other | 2 | 5 | 4 | Order (production / maintenance / internal), Purchasing Document, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| LO_other | 2 | 4 | 5 | Delivery, Order (production / maintenance / internal), Batch, G/L Account, Material / Product, Supplier |
| SD-SLS_Sales | 1 | 7 | 4 | Order (production / maintenance / internal), Batch, Cost Center, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| FI-GL_General-Ledger | 1 | 6 | 5 | Order (production / maintenance / internal), Cost Center, G/L Account, Material / Product, Profitability Segment, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
