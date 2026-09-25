# FT

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `FT` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**12 view** · data category: (none) 12 · loại: basic 9, text 3 · 0 view có field DEPRECATED/DECOMMISSIONED · 11 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FT-ITR-CLS | 7 | top-level |
| FT-ITR-TRC | 5 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| C_COMMODITYCODEFORKEYDATE | Commodity Code for Key Date | FT-ITR-CLS |  | 21 |
| C_CSTMSTRIFNMBRFORKEYDATE | Customs Tariff Number for Key Date | FT-ITR-CLS |  | 21 |
| C_PRODCOMMODITYCODEFORKEYDATE | Product Commodity Code Classification for Key Date | FT-ITR-CLS |  | 20 |
| C_TRDCMPLNCDOCITMLICASSGMT | Trade Compliance Document Item License Assignment | FT-ITR-TRC |  | 18 |
| C_PRODCSTMSTRIFNMBRFORKEYDATE | Product Tariff Number Classification for Key Date | FT-ITR-CLS |  | 17 |
| C_CONTROLCLASSFORKEYDATE | Control Class for Key Date | FT-ITR-CLS |  | 13 |
| C_PRODLGLCTRLCLFNFORKEYDATE | Product Legal Control Classification for Key Date | FT-ITR-CLS |  | 10 |
| I_CUSTOMSPREFERENCE | Trade Preference Indicator | FT-ITR-TRC |  | 2 |
| I_TRDPREFSTMNTINTORIGINCODE | Preference Internal Origin Code | FT-ITR-TRC |  | 2 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Material / Product | 3 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CA | 0 | 1 | 0 | Material / Product |
| CO_other | 0 | 1 | 0 | Material / Product |
| CRM | 0 | 1 | 0 | Material / Product |
| EAM-OBJ_Technical-Objects | 0 | 1 | 0 | Material / Product |
| FI-GL_General-Ledger | 0 | 1 | 0 | Material / Product |
| FIN | 0 | 1 | 0 | Material / Product |
| FI_other | 0 | 1 | 0 | Material / Product |
| LE | 0 | 1 | 0 | Material / Product |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
