# FI-AR_Accounts-Receivable — Accounts Receivable

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `FI-AR` = **Accounts Receivable**.

**28 view** · data category: (none) 15, Dimension 13 · loại: dimension 13, text 8, basic 5, value_help 2 · 0 view có field DEPRECATED/DECOMMISSIONED · 5 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-AR-AR-C-2CL | 7 | component |
| FI-AR-AR-RF-2CL | 3 | component |
| FI-AR-IS-2CL | 18 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PARKEDOPLACCTGDOCRBLSITEM | Parked Accounts Receivable Item | FI-AR-IS-2CL | Dimension | 129 |
| I_JOURNALENTRYITEMONETIMEDATA | One-Time Data for Journal Entry Item | FI-AR-IS-2CL | Dimension | 47 |
| I_ONETIMEACCOUNTCUSTOMER | One-Time Account Data for Customer Items | FI-AR-IS-2CL | Dimension | 33 |
| I_ONETIMEACCOUNTSUPPLIER | One-Time Account Data for Supplier Items | FI-AR-IS-2CL | Dimension | 33 |
| I_PAYMENTTERMSCONDITIONS | Payment Terms Conditions | FI-AR-IS-2CL | Dimension | 29 |
| I_APARTOLERANCEGROUP | Tolerance Group for Cust and Suppl | FI-AR-IS-2CL |  | 13 |
| I_USERTOLERANCEGROUP | Tolerance Group for Group of Users | FI-AR-IS-2CL | Dimension | 13 |
| I_PAYMENTDIFFERENCEREASONT | Payment Difference Reason - Text | FI-AR-IS-2CL |  | 7 |
| I_PAYMENTDIFFERENCEREASON | Payment Difference Reason | FI-AR-IS-2CL | Dimension | 6 |
| I_PAYMENTTERMSINSTALLMENTITEM | Installment Items for Terms of Payment | FI-AR-IS-2CL |  | 6 |
| I_PAYMENTTERMS | Payment Terms | FI-AR-IS-2CL | Dimension | 5 |
| I_DUNNINGAREA | Dunning Area | FI-AR-AR-C-2CL | Dimension | 4 |
| I_STATECENTRALBANKPAYTRSN | State Central Bank Payment Reason | FI-AR-IS-2CL | Dimension | 4 |
| I_DUNNINGKEY | Dunning Key | FI-AR-AR-C-2CL | Dimension | 3 |
| I_USERTOUSERTOLERANCEGROUP | User Assignment to UserTolGroup in Acctg | FI-AR-IS-2CL |  | 3 |
| I_DUNNINGBLOCKINGREASONCODE | Dunning Blocking Reason Code | FI-AR-AR-C-2CL | Dimension | 2 |
| I_RECEIVABLEFINANCINGSTATUS | Receivable Financing Status | FI-AR-AR-RF-2CL |  | 2 |
| I_PAYMENTBLOCKINGREASON | Payment Blocking Reason | FI-AR-IS-2CL | Dimension | 2 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 12 |
| CONFIG | Fiscal Year | 4 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| AC | 0 | 0 | 1 | — |
| CA | 0 | 0 | 1 | — |
| CO-OM_Cost-Center-Accounting | 0 | 0 | 1 | — |
| CO_other | 0 | 0 | 1 | — |
| CRM | 0 | 0 | 1 | — |
| EAM-OBJ_Technical-Objects | 0 | 0 | 1 | — |
| FI-AA_Asset-Accounting | 0 | 0 | 1 | — |
| FI-AP_Accounts-Payable | 0 | 0 | 1 | — |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
