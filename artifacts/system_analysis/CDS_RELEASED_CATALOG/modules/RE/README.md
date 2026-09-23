# RE

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `RE` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**51 view** · data category: (none) 32, Dimension 19 · loại: text 23, dimension 19, basic 9 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| RE-FX | 20 | top-level |
| RE-FX-BD | 12 | top-level |
| RE-FX-CN | 16 | top-level |
| RE-FX-IP | 1 | top-level |
| RE-FX-RA | 2 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_RECONTRACTDATA | Real Estate Contract | RE-FX-CN |  | 82 |
| I_REINVOICEDATA | Real Estate Invoice Header | RE-FX-RA |  | 26 |
| I_RECONDITIONTYPE | Condition Type | RE-FX-CN | Dimension | 16 |
| I_REINVOICEITEMDATA | Real Estate Invoice Item | RE-FX-RA |  | 14 |
| I_RECONDITIONTYPEBYCNDNGROUP | Condition Type per Condition Group | RE-FX-CN | Dimension | 12 |
| I_REFLOWTYPE | Flow Type | RE-FX-CN | Dimension | 9 |
| I_RECONTRACTNOTICEREASON | Contract Notice Reason | RE-FX-CN | Dimension | 8 |
| I_RENOTICERULE | Notice Rules | RE-FX | Dimension | 5 |
| I_RERENEWALRULE | Renewal Rules | RE-FX | Dimension | 5 |
| I_REARCHITECTUREOBJECTTYPE | Real Estate Architecture Object Type | RE-FX-BD |  | 4 |
| I_REGNRCRENTALOBJUSAGECATEGORY | RE Generic Rental Object Usage Category | RE-FX-BD |  | 4 |
| I_REAUTOMATICRENEWALTYPE | Automatic Renewal Type | RE-FX | Dimension | 3 |
| I_RENOTICEGIVINGPARTY | Notice Giving Party | RE-FX | Dimension | 3 |
| I_RENOTICEPROCEDURE | Contract Notice Procedure | RE-FX | Dimension | 3 |
| I_RENOTICERULETYPE | Notice Rule Types | RE-FX | Dimension | 3 |
| I_RENOTICETYPE | Notice Types | RE-FX | Dimension | 3 |
| I_REOBJECTTYPE | Real Estate Object Type | RE-FX |  | 3 |
| I_RERENEWALRULETYPE | Renewal Rule Type | RE-FX | Dimension | 3 |
| I_RERENEWALTYPE | Renewal Types | RE-FX | Dimension | 3 |
| I_REGNRCRENTALOBJUSAGETYPE | Real Estate Rental Object Usage Type | RE-FX-BD |  | 3 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CA | 0 | 0 | 1 | — |
| CO-OM_Cost-Center-Accounting | 0 | 0 | 1 | — |
| CO_other | 0 | 0 | 1 | — |
| FI-AA_Asset-Accounting | 0 | 0 | 1 | — |
| FI-AP_Accounts-Payable | 0 | 0 | 1 | — |
| FI-AR_Accounts-Receivable | 0 | 0 | 1 | — |
| FI-GL_General-Ledger | 0 | 0 | 1 | — |
| FIN | 0 | 0 | 1 | — |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
