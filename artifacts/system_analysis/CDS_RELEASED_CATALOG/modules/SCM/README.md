# SCM

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `SCM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**130 view** · data category: (none) 125, Dimension 5 · loại: basic 102, text 23, dimension 5 · 10 view có field DEPRECATED/DECOMMISSIONED · 89 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SCM-EWM-DLP-2CL | 29 | top-level |
| SCM-EWM-PRN-2CL | 1 | top-level |
| SCM-EWM-WOP-2CL | 100 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_EWM_WHSETASKITEMCUBE_2 | Warehouse Task Item - Cube | SCM-EWM-WOP-2CL |  | 231 |
| I_EWM_INBDELIVERYITEMC_2 | Inbound Delivery Item - Cube | SCM-EWM-DLP-2CL |  | 222 |
| I_EWM_ODONOPARAMC_2 | ODO Without Mandatory Parameters - Cube | SCM-EWM-DLP-2CL |  | 166 |
| I_EWM_WAREHOUSETASK_2 | Open and Confirmed Warehouse Tasks | SCM-EWM-WOP-2CL |  | 142 |
| I_EWM_OUTBDELIVORDC_2 | Warehouse Outbound Delivery Order - Cube | SCM-EWM-DLP-2CL |  | 141 |
| I_EWM_WAREHOUSEWAVEC_2 | Warehouse Wave - Cube | SCM-EWM-WOP-2CL |  | 132 |
| I_EWM_WHSEDOCUMENTITEM | Warehouse Document Item | SCM-EWM-WOP-2CL |  | 104 |
| I_EWM_PHYSSTOCKPROD | Physical Stock for Products | SCM-EWM-WOP-2CL |  | 91 |
| I_EWM_INBDELIVERYITEM | Warehouse Inbound Delivery Item | SCM-EWM-DLP-2CL |  | 86 |
| I_EWM_WHSEORDERCUBE_2 | Warehouse Order - Cube | SCM-EWM-WOP-2CL |  | 86 |
| I_EWM_PRODUCTWAREHOUSE | Product Warehouse Data | SCM-EWM-WOP-2CL |  | 83 |
| I_EWM_STORAGEBINACTYAREACUBE | Storage Bin Activity Area - Cube | SCM-EWM-WOP-2CL |  | 81 |
| I_EWM_STORAGEBINCUBE | Storage Bin - Cube | SCM-EWM-WOP-2CL |  | 79 |
| I_EWM_OUTBDELIVORDITEM | Warehouse Outbound Delivery Order Item | SCM-EWM-DLP-2CL |  | 78 |
| I_EWM_PRODNMATLREQITEM | Production Material Request Item | SCM-EWM-DLP-2CL |  | 76 |
| I_EWM_PHYSINVTRYITEMC | Warehouse Physical Inventory Item - Cube | SCM-EWM-WOP-2CL |  | 76 |
| I_EWM_HANDLINGUNITHDR_2 | Warehouse Handling Unit Header | SCM-EWM-WOP-2CL |  | 72 |
| I_EWM_PHYSINVTRYITEMROW | Row of PInv Item with Quantity in Whse | SCM-EWM-WOP-2CL |  | 65 |
| I_EWM_PHYSICALINVENTORYITEM | Warehouse Physical Inventory Item | SCM-EWM-WOP-2CL |  | 60 |
| I_EWM_PINVITEMFLATTENEDROW | Flattened Row of PInv Item in Warehouse | SCM-EWM-WOP-2CL |  | 59 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Material / Product | 12 |
| MASTER | Batch | 11 |
| MASTER | Business Partner | 8 |
| MASTER | WBS Element | 7 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CRM | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| FI_other | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| MM-PUR_Purchasing | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| SD-BIL_Billing | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| SD-SLS_Sales | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| SD_other | 0 | 4 | 0 | Batch, Business Partner, Material / Product, WBS Element |
| CA | 0 | 3 | 0 | Business Partner, Material / Product, WBS Element |
| FIN | 0 | 3 | 0 | Business Partner, Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
