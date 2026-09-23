# FI-AR_Accounts-Receivable — Accounts Receivable

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `FI-AR` = **Accounts Receivable**.

**23 view** · data category: Dimension 12, (none) 11 · loại: dimension 12, text 6, basic 4, value_help 1 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-AR-AR-C | 7 | component |
| FI-AR-IS | 16 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_JOURNALENTRYITEMONETIMEDATA | One-Time Data for Journal Entry Item | FI-AR-IS | Dimension | 47 |
| I_ONETIMEACCOUNTCUSTOMER | One-Time Account Data for Customer Items | FI-AR-IS | Dimension | 33 |
| I_ONETIMEACCOUNTSUPPLIER | One-Time Account Data for Supplier Items | FI-AR-IS | Dimension | 33 |
| I_PAYMENTTERMSCONDITIONS | Payment Terms Conditions | FI-AR-IS | Dimension | 29 |
| I_USERTOLERANCEGROUP | Tolerance Group for Group of Users | FI-AR-IS | Dimension | 13 |
| I_TAXBALANCESGRP | Grouping Numbers of Tax Balances | FI-AR-IS |  | 8 |
| I_PAYMENTDIFFERENCEREASONT | Payment Difference Reason - Text | FI-AR-IS |  | 7 |
| I_PAYMENTDIFFERENCEREASON | Payment Difference Reason | FI-AR-IS | Dimension | 6 |
| I_PAYMENTTERMSINSTALLMENTITEM | Installment Items for Terms of Payment | FI-AR-IS |  | 6 |
| I_PAYMENTTERMS | Payment Terms | FI-AR-IS | Dimension | 5 |
| I_DUNNINGAREA | Dunning Area | FI-AR-AR-C | Dimension | 4 |
| I_STATECENTRALBANKPAYTRSN | State Central Bank Payment Reason | FI-AR-IS | Dimension | 4 |
| I_DUNNINGKEY | Dunning Key | FI-AR-AR-C | Dimension | 3 |
| I_USERTOUSERTOLERANCEGROUP | User Assignment to UserTolGroup in Acctg | FI-AR-IS |  | 3 |
| I_DUNNINGBLOCKINGREASONCODE | Dunning Blocking Reason Code | FI-AR-AR-C | Dimension | 2 |
| I_PAYMENTBLOCKINGREASON | Payment Blocking Reason | FI-AR-IS | Dimension | 2 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 9 |
| CONFIG | Fiscal Year | 3 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CA | 0 | 0 | 1 | — |
| CO-OM_Cost-Center-Accounting | 0 | 0 | 1 | — |
| CO_other | 0 | 0 | 1 | — |
| FI-AA_Asset-Accounting | 0 | 0 | 1 | — |
| FI-AP_Accounts-Payable | 0 | 0 | 1 | — |
| FI-GL_General-Ledger | 0 | 0 | 1 | — |
| FIN | 0 | 0 | 1 | — |
| FI_other | 0 | 0 | 1 | — |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
