# SUS

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `SUS` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**32 view** · data category: (none) 23, Dimension 9 · loại: dimension 9, text 9, value_help 9, basic 5 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SUS-INT | 27 | top-level |
| SUS-PFM-INT | 5 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_CO2EQSUPLRFPRNTAVGBASEUOM_2 | Avg Suplr Related CO2eq Footprint | SUS-PFM-INT |  | 19 |
| I_CO2EQFPRNTAVGRLTVBASEUOM_2 | Avg Rltv CO2eq Footprint of Prod at Plnt | SUS-PFM-INT |  | 16 |
| I_PFMTRANSDATACO2EQFPRNTGHGCAT | Trans data footprint GHG Category | SUS-PFM-INT |  | 10 |
| I_CO2EQFPRNTAVGGHGCAT | Avg Rltv CO2eq Footprint GHG Category | SUS-PFM-INT |  | 8 |
| I_PFMTRANSDATACO2EQFPRNT | Carbon Footprint of Transaction Data | SUS-PFM-INT |  | 8 |
| I_GHGCATEGORY | GHG Category Codelist | SUS-INT | Dimension | 4 |
| I_GHGSCP2CALCMETHOD | GHG Scope 2 Calculation Method Codelist | SUS-INT | Dimension | 4 |
| I_GHGSCP2CNTRCTLINSTRUMENT | GHG Scope 2 Contractual Instrument Codelist | SUS-INT | Dimension | 4 |
| I_GHGDTAQLTYCHARACTERISTIC | GHG Data Quality Characteristic Codelist | SUS-INT | Dimension | 3 |
| I_GHGENERGYCLASSIFICATION | GHG Energy Classification Codelist | SUS-INT | Dimension | 3 |
| I_GHGENERGYMIX | GHG Energy Mix Codelist | SUS-INT | Dimension | 3 |
| I_GHGENERGYSOURCINGTYPE | GHG Energy Sourcing Type Codelist | SUS-INT | Dimension | 3 |
| I_GHGSCOPE | GHG Scope Codelist | SUS-INT | Dimension | 3 |
| I_SUSTMODEOFTRANSPORT | Sustainability Mode of Transport Codelist | SUS-INT | Dimension | 3 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Material / Product | 2 |
| ORG | Plant | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO_other | 0 | 1 | 1 | Material / Product |
| CRM | 0 | 1 | 1 | Material / Product |
| FI-GL_General-Ledger | 0 | 1 | 1 | Material / Product |
| FI_other | 0 | 1 | 1 | Material / Product |
| LE | 0 | 1 | 1 | Material / Product |
| LO-MD-BOM_Bill-of-Material | 0 | 1 | 1 | Material / Product |
| LO-MD-MM_Material-Master | 0 | 1 | 1 | Material / Product |
| LO_other | 0 | 1 | 1 | Material / Product |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
