# LO-MD-MM_Material-Master — Material Master

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `LO-MD-MM` = **Material Master**.

**102 view** · data category: (none) 68, Dimension 34 · loại: basic 34, dimension 33, text 22, value_help 13 · 4 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| LO-MD-MM | 102 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PRODUCT | Product | LO-MD-MM | Dimension | 256 |
| I_PRODUCTSUPPLYPLANNING | Product SupPlanning active core entity | LO-MD-MM |  | 124 |
| I_PRODUCTPLANTBASIC | Product Plant | LO-MD-MM | Dimension | 120 |
| I_PRODUCTSALESDELIVERY | Product Sales Delivery | LO-MD-MM | Dimension | 101 |
| I_PRODUCTPLANTSUPPLYPLANNING | Product Plant Supply Planning | LO-MD-MM |  | 92 |
| I_PRODUCTCONSUMPTION | Product Consumption | LO-MD-MM |  | 60 |
| I_PRODUCTRETAIL | Product Retail Basic Data | LO-MD-MM | Dimension | 53 |
| I_PRODUCTSALES | Product Sales | LO-MD-MM | Dimension | 53 |
| I_PRODUCTVALUATIONBASIC | Product Valuation | LO-MD-MM |  | 47 |
| I_PRODUCTVALUATIONACCT | Product Valuation Account | LO-MD-MM |  | 38 |
| I_PRODUCTUNITSOFMEASURE | Units of Measure of Product | LO-MD-MM | Dimension | 36 |
| I_PRODUCTSTORAGE_2 | Product Storage | LO-MD-MM | Dimension | 33 |
| I_PRODUCTWORKSCHEDULING | Product WorkScheduling core entity | LO-MD-MM |  | 33 |
| I_PRODUCTSTORAGELOCATIONBASIC | Product Storage Location | LO-MD-MM | Dimension | 27 |
| I_PRODUCTPROCUREMENT | Product Procurement | LO-MD-MM | Dimension | 21 |
| I_PRODUCTVALUATIONACCOUNTING_2 | Product Valuation Account | LO-MD-MM |  | 21 |
| I_PRODUCTVALUATIONCOSTING | Product Valuation Costing Core Entity | LO-MD-MM |  | 21 |
| I_PRODPLNTINPTASSISTANT | Input Assistance for Product Plant | LO-MD-MM |  | 20 |
| I_PRODUCTPLANTCOSTING | Product Plant Costing | LO-MD-MM |  | 20 |
| I_PRODUCTPLANTSALES | Product plant sales | LO-MD-MM |  | 18 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Material / Product | 37 |
| ORG | Plant | 20 |
| ORG | Company Code | 9 |
| ORG | Valuation Area | 9 |
| ORG | Storage Location | 4 |
| ORG | Distribution Channel | 3 |
| ORG | Sales Organization | 3 |
| ORG | Division | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LO_other | 0 | 1 | 7 | Material / Product |
| FI-GL_General-Ledger | 0 | 1 | 6 | Material / Product |
| FI_other | 0 | 1 | 5 | Material / Product |
| LE | 0 | 1 | 5 | Material / Product |
| SD-SLS_Sales | 0 | 1 | 5 | Material / Product |
| MM-IM_Inventory-Management | 0 | 1 | 4 | Material / Product |
| PSM | 0 | 1 | 4 | Material / Product |
| QM | 0 | 1 | 4 | Material / Product |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
