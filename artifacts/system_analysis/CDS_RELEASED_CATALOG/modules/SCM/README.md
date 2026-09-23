# SCM

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `SCM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**41 view** · data category: (none) 36, Dimension 5 · loại: basic 24, text 12, dimension 5 · 4 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SCM-EWM-DLP | 11 | top-level |
| SCM-EWM-WOP | 30 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_EWM_WAREHOUSETASK_2 | Open and Confirmed Warehouse Tasks | SCM-EWM-WOP |  | 142 |
| I_EWM_PHYSSTOCKPROD | Physical Stock for Products | SCM-EWM-WOP |  | 91 |
| I_EWM_INBDELIVERYITEM | Warehouse Inbound Delivery Item | SCM-EWM-DLP |  | 86 |
| I_EWM_PRODUCTWAREHOUSE | Product Warehouse Data | SCM-EWM-WOP |  | 83 |
| I_EWM_OUTBDELIVORDITEM | Warehouse Outbound Delivery Order Item | SCM-EWM-DLP |  | 78 |
| I_EWM_PHYSINVTRYITEMROW | Row of PInv Item with Quantity in Whse | SCM-EWM-WOP |  | 65 |
| I_EWM_PHYSICALINVENTORYITEM | Warehouse Physical Inventory Item | SCM-EWM-WOP |  | 60 |
| I_EWM_PINVITEMFLATTENEDROW | Flattened Row of PInv Item in Warehouse | SCM-EWM-WOP |  | 59 |
| I_EWM_PRODUCTSTORAGETYPE | Product Storage Type | SCM-EWM-WOP |  | 57 |
| I_EWM_WAREHOUSEORDER_2 | Warehouse Order | SCM-EWM-WOP |  | 42 |
| I_EWM_AVAILABLESTOCK | Available Stock | SCM-EWM-WOP |  | 37 |
| I_EWM_OUTBDELIVORDHDR | Warehouse Outbound Delivery Order Header | SCM-EWM-DLP |  | 33 |
| I_EWM_INBDELIVERYHEADER | Warehouse Inbound Delivery Header | SCM-EWM-DLP |  | 21 |
| I_EWM_WHSEORDERHNDLGUNIT_2 | Handling Unit for Warehouse Order | SCM-EWM-WOP |  | 17 |
| I_EWM_FIXEDBINASSIGNMENT | Warehouse Fixed Bin Assignment | SCM-EWM-WOP |  | 12 |
| I_EWM_PINVITEMROWSRLNMBR | Serial Number of Whse PInv Item Row | SCM-EWM-WOP |  | 11 |
| I_EWM_PLANTSTORLOCMAPTOWHSE | Mapping plant and stor loc to warehouse | SCM-EWM-WOP |  | 6 |
| I_EWM_WHSETASKEXCEPTIONCODE_2 | Exception Code for Warehouse Task | SCM-EWM-WOP |  | 6 |
| I_EWM_DELIVERYTYPETEXT_2 | Warehouse Delivery Type - Text | SCM-EWM-DLP |  | 5 |
| I_EWM_INBDELIVERYITEMSRLNMBR | Warehouse Inb Deliv Item Serial Number | SCM-EWM-DLP |  | 5 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Material / Product | 8 |
| MASTER | Batch | 6 |
| MASTER | WBS Element | 5 |
| MASTER | Business Partner | 4 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| MM-PUR_Purchasing | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| SD-SLS_Sales | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| SD_other | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| CRM | 0 | 3 | 0 | Batch, Material / Product, WBS Element |
| FI_other | 0 | 3 | 0 | Business Partner, Material / Product, WBS Element |
| LE | 0 | 3 | 0 | Batch, Material / Product, WBS Element |
| LO_other | 0 | 3 | 0 | Batch, Business Partner, Material / Product |
| MM-IM_Inventory-Management | 0 | 3 | 0 | Batch, Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
