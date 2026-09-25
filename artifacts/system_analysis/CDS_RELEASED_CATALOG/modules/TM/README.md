# TM

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `TM` (không thuộc phân hệ ưu tiên nào trong Sheet1). `TM`: Transportation Management.

**305 view** · data category: (none) 273, Dimension 32 · loại: basic 244, dimension 32, text 27, value_help 2 · 0 view có field DEPRECATED/DECOMMISSIONED · 225 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| TM-2CL | 53 | top-level |
| TM-CF-CC-2CL | 13 | top-level |
| TM-FRA-2CL | 48 | top-level |
| TM-FRM-2CL | 60 | top-level |
| TM-FRM-FRB-2CL | 29 | top-level |
| TM-FRM-FRO-2CL | 29 | top-level |
| TM-FRS-2CL | 1 | top-level |
| TM-MD-CM-2CL | 32 | top-level |
| TM-MD-CM-RA-2CL | 6 | top-level |
| TM-MD-ORG-2CL | 3 | top-level |
| TM-MD-PR-2CL | 6 | top-level |
| TM-MD-TN-2CL | 4 | top-level |
| TM-MD-TN-LOC-2CL | 5 | top-level |
| TM-PLN-FU-2CL | 16 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_TRANSPORTATIONORDERITEM_2 | Transportation Order Item | TM-FRM-2CL |  | 100 |
| I_TRANSPORTATIONORDER_2 | Transportation Order | TM-FRM-2CL |  | 91 |
| I_TRANSPORTATIONCHARGEELEMENT | Transportation Charge Element | TM-CF-CC-2CL |  | 56 |
| I_TRANSPCHARGEITEM | Transportation Charge Item | TM-CF-CC-2CL |  | 42 |
| I_TRANSPORTATIONORDERSTAGE_2 | Transportation Order Stage | TM-FRM-2CL |  | 37 |
| I_TRANSPORTATIONORDERSTOP_2 | Transportation Order Stop | TM-FRM-2CL |  | 36 |
| I_TRANSPCHRGCALCSHEETITEM | Transp Charge Calculation Sheet Item | TM-FRA-2CL |  | 32 |
| I_LOCATIONBASIC_2 | Location | TM-MD-TN-LOC-2CL |  | 30 |
| I_TRANSPORTATIONAGREEMENT | Transportation Agreement | TM-FRA-2CL |  | 28 |
| I_TRANSPCHARGECALCBASE | Transportation Charge Calculation Base | TM-CF-CC-2CL |  | 26 |
| I_TRANSPORTATIONRATEVALIDITY_2 | Transportation Rate Validity | TM-FRA-2CL |  | 26 |
| I_TRANSPORTATIONRATE | Transportation Rate Table | TM-FRA-2CL |  | 23 |
| I_TRANSPORTATIONORDEREVENT | Transportation Order Event | TM-FRM-2CL |  | 23 |
| I_TRANSPRATEDIMENSION14 | Rate Table 14 Dimensional Rates | TM-FRA-2CL |  | 22 |
| I_TRANSPORTATIONSCALE | Transportation Scale | TM-FRA-2CL |  | 21 |
| I_TRANSPRATEDIMENSION13 | Rate Table 13 Dimensional Rates | TM-FRA-2CL |  | 21 |
| I_TRANSPRATESCALEREFERENCE | Transportation Rate Scale Reference | TM-FRA-2CL |  | 21 |
| I_TRANSPRATEDIMENSION12 | Rate Table 12 Dimensional Rates | TM-FRA-2CL |  | 20 |
| I_TRANSPRATEDIMENSION11 | Rate Table 11 Dimensional Rates | TM-FRA-2CL |  | 19 |
| I_TRANSPORTATIONCHARGE | Transportation Charge | TM-CF-CC-2CL |  | 18 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Business Partner | 3 |
| MASTER | Material / Product | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CA | 0 | 2 | 0 | Business Partner, Material / Product |
| CRM | 0 | 2 | 0 | Business Partner, Material / Product |
| FIN | 0 | 2 | 0 | Business Partner, Material / Product |
| FI_other | 0 | 2 | 0 | Business Partner, Material / Product |
| LO_other | 0 | 2 | 0 | Business Partner, Material / Product |
| MM-PUR_Purchasing | 0 | 2 | 0 | Business Partner, Material / Product |
| SCM | 0 | 2 | 0 | Business Partner, Material / Product |
| SD-BIL_Billing | 0 | 2 | 0 | Business Partner, Material / Product |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
