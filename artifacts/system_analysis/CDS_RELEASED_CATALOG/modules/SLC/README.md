# SLC

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `SLC` (không thuộc phân hệ ưu tiên nào trong Sheet1). `SLC`: Supplier Lifecycle Management.

**102 view** · data category: (none) 101, Dimension 1 · loại: basic 82, text 19, dimension 1 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| SLC-ACT | 22 | top-level |
| SLC-CAT | 10 | top-level |
| SLC-EVL | 47 | top-level |
| SLC-SUP | 23 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SUPLREVALRSPQUESTIONAPI01 | Question for Supplier Eval Response | SLC-EVL |  | 22 |
| I_PURGCATPARTYAPI01 | Party Referenced by Purchasing Category | SLC-CAT |  | 21 |
| I_PURGCATPURCHASERRESPAPI01 | Purchaser Resp Referenced by Purg Cat | SLC-CAT |  | 18 |
| I_PURGCATSUPPLIERAPI01 | Supplier Referenced by Purg Category | SLC-CAT |  | 18 |
| I_SUPLREVALSCCRDSUPPLIERAPI01 | Supplier for Supplier Eval Scorecard | SLC-EVL |  | 18 |
| I_PURGCATMEMBERAPI01 | Team Member for Purchasing Category | SLC-CAT |  | 17 |
| I_SUPLREVALRSPSUPPLIERAPI01 | Supplier Party for Suplr Eval Response | SLC-EVL |  | 17 |
| I_SUPLREVALTMPLPURRRESPAPI01 | Purchaser Resp for Eval Template | SLC-EVL |  | 17 |
| I_SUPLRACTIVITYSUPPLIERAPI01 | Supplier for Supplier Activity | SLC-ACT |  | 16 |
| I_SUPLRACTYPARTICIPANTAPI01 | Participant in Supplier Activity | SLC-ACT |  | 16 |
| I_SUPLRACTYPURCHASERRESPAPI01 | Purchaser Resp for Supplier Activity | SLC-ACT |  | 16 |
| I_SUPLRACTYTASKEMAILTMPLAPI01 | Email Template for Task Notification | SLC-ACT |  | 16 |
| I_SUPLRACTYTASKPROCESSORAPI01 | Processor of Supplier Activity Task | SLC-ACT |  | 16 |
| I_SUPLRACTYTASKPURRRESPAPI01 | Purchaser Resp for Supplier Acty Task | SLC-ACT |  | 16 |
| I_SUPLRACTYTASKSUPPLIERAPI01 | Supplier for Supplier Activity Task | SLC-ACT |  | 16 |
| I_SLCMGMTQNAIREPURRRESPAPI01 | Purchaser Responsible for Questionnaire | SLC-EVL |  | 16 |
| I_SUPLREVALRSPAPPRAISERAPI01 | Appraiser of Supplier Eval Response | SLC-EVL |  | 16 |
| I_SUPLREVALRSPPURRRESPAPI01 | Purchaser Resp for Suplr Eval Response | SLC-EVL |  | 16 |
| I_SUPLREVALSCCRDPURRRESPAPI01 | Purchaser Resp for Suplr Eval Scorecard | SLC-EVL |  | 16 |
| I_SUPLRGEVALEMAILTMPLAPI02 | Email Template for Eval Notification | SLC-EVL |  | 16 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Business Partner | 8 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| AP | 0 | 1 | 0 | Business Partner |
| BC | 0 | 1 | 0 | Business Partner |
| CA | 0 | 1 | 0 | Business Partner |
| FIN | 0 | 1 | 0 | Business Partner |
| FI_other | 0 | 1 | 0 | Business Partner |
| LO_other | 0 | 1 | 0 | Business Partner |
| MM-PUR_Purchasing | 0 | 1 | 0 | Business Partner |
| SCM | 0 | 1 | 0 | Business Partner |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
