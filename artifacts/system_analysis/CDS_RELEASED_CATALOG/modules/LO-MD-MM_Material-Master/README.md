# LO-MD-MM_Material-Master — Material Master

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `LO-MD-MM` = **Material Master**.

**179 view** · data category: (none) 145, Dimension 34 · loại: basic 99, dimension 33, text 29, value_help 18 · 4 view có field DEPRECATED/DECOMMISSIONED · 77 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| LO-MD-MM-2CL | 179 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PRODUCT | Product | LO-MD-MM-2CL | Dimension | 256 |
| I_PRODUCTSUPPLYPLANNING | Product SupPlanning active core entity | LO-MD-MM-2CL |  | 124 |
| I_PRODUCTPLANTBASIC | Product Plant | LO-MD-MM-2CL | Dimension | 120 |
| I_PRODUCTPLANTMRP | MRP area data of a Product | LO-MD-MM-2CL |  | 107 |
| I_PRODUCTSALESDELIVERY | Product Sales Delivery | LO-MD-MM-2CL | Dimension | 101 |
| I_PRODUCTPLANTSUPPLYPLANNING | Product Plant Supply Planning | LO-MD-MM-2CL |  | 92 |
| I_PRODUCTCONSUMPTION | Product Consumption | LO-MD-MM-2CL |  | 60 |
| I_PRODUCTRETAIL | Product Retail Basic Data | LO-MD-MM-2CL | Dimension | 53 |
| I_PRODUCTSALES | Product Sales | LO-MD-MM-2CL | Dimension | 53 |
| I_PRODUCTCHANGEDOCUMENT_2 | Product Change Document | LO-MD-MM-2CL |  | 48 |
| I_PRODUCTVALUATIONBASIC | Product Valuation | LO-MD-MM-2CL |  | 47 |
| I_PRODUCTVALUATIONACCT | Product Valuation Account | LO-MD-MM-2CL |  | 38 |
| I_PRODUCTUNITSOFMEASURE | Units of Measure of Product | LO-MD-MM-2CL | Dimension | 36 |
| I_PRODUCTSTORAGE_2 | Product Storage | LO-MD-MM-2CL | Dimension | 33 |
| I_PRODUCTWORKSCHEDULING | Product WorkScheduling core entity | LO-MD-MM-2CL |  | 33 |
| I_PRODUCTSTORAGELOCATIONBASIC | Product Storage Location | LO-MD-MM-2CL | Dimension | 27 |
| I_PRODUCTPROCUREMENT | Product Procurement | LO-MD-MM-2CL | Dimension | 21 |
| I_PRODUCTVALUATIONACCOUNTING_2 | Product Valuation Account | LO-MD-MM-2CL |  | 21 |
| I_PRODUCTVALUATIONCOSTING | Product Valuation Costing Core Entity | LO-MD-MM-2CL |  | 21 |
| I_PRODPLNTINPTASSISTANT | Input Assistance for Product Plant | LO-MD-MM-2CL |  | 20 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Material / Product | 42 |
| ORG | Plant | 21 |
| ORG | Valuation Area | 10 |
| ORG | Company Code | 9 |
| ORG | Distribution Channel | 4 |
| ORG | Sales Organization | 4 |
| ORG | Storage Location | 4 |
| ORG | Division | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LO_other | 0 | 1 | 7 | Material / Product |
| CO_other | 0 | 1 | 6 | Material / Product |
| FI-GL_General-Ledger | 0 | 1 | 6 | Material / Product |
| FIN | 0 | 1 | 6 | Material / Product |
| FI_other | 0 | 1 | 6 | Material / Product |
| SD-BIL_Billing | 0 | 1 | 6 | Material / Product |
| SD_other | 0 | 1 | 6 | Material / Product |
| CA | 0 | 1 | 5 | Material / Product |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
