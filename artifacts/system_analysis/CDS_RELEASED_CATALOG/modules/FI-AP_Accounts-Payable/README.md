# FI-AP_Accounts-Payable — Accounts Payable

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `FI-AP` = **Accounts Payable**.

**20 view** · data category: (none) 14, Dimension 3, Fact 3 · loại: basic 8, text 5, dimension 3, fact 3, value_help 1 · 0 view có field DEPRECATED/DECOMMISSIONED · 6 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-AP-AP-2CL | 2 | component |
| FI-AP-AP-B-2CL | 8 | component |
| FI-AP-AP-Q-2CL | 4 | component |
| FI-AP-IS-2CL | 6 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PARKEDOPLACCTGDOCPYBLSITEM | Parked Accounts Payable Item | FI-AP-IS-2CL | Dimension | 160 |
| I_PAYMENTPROPOSALPAYMENT | Payment Proposal Payment | FI-AP-AP-B-2CL | Fact | 153 |
| I_PAYMENTPROPOSALITEM | Payment Proposal Item | FI-AP-AP-B-2CL | Fact | 93 |
| I_WITHHOLDINGTAXITEM | Withholding Tax Item | FI-AP-AP-Q-2CL | Fact | 55 |
| I_PAYMENTPROGRAMCONTROL | Payment Program Control | FI-AP-AP-B-2CL |  | 18 |
| I_PAYMENTMETHOD | Payment Method for Country/Region | FI-AP-IS-2CL | Dimension | 12 |
| I_PAYTPRPSLBLKDFINACCOUNT | Payment Proposal Blocked Fin Account | FI-AP-AP-B-2CL |  | 11 |
| I_CORRESPONDENCETYPE | Correspondence Type | FI-AP-AP-2CL |  | 7 |
| I_WITHHOLDINGTAXINCOMETYPE | Withholding Tax Income Type | FI-AP-AP-Q-2CL |  | 4 |
| I_PAYMENTBLOCKLEVEL | Payment Block Level | FI-AP-AP-B-2CL | Dimension | 3 |
| I_PAYMENTREASON | Payment Reason for Purpose Codes | FI-AP-AP-B-2CL |  | 2 |
| I_APFLEXIBLEAGING | Aging Analysis Smart Business App | FI-AP-IS-2CL |  | 0 |
| I_APJRNLENTRITMAGINGGRID | Aging Grid of Accounts Payables | FI-AP-IS-2CL |  | 0 |
| I_PAYMENTMETHODINCOMPANYCODE | Payment Method for Company Code | FI-AP-IS-2CL |  | 0 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 4 |
| MASTER | Customer | 2 |
| MASTER | G/L Account | 2 |
| MASTER | Supplier | 2 |
| CONFIG | Fiscal Year | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| CO-OM_Cost-Center-Accounting | 0 | 3 | 1 | Customer, G/L Account, Supplier |
| FI-GL_General-Ledger | 0 | 3 | 1 | Customer, G/L Account, Supplier |
| FIN | 0 | 3 | 1 | Customer, G/L Account, Supplier |
| FI_other | 0 | 3 | 1 | Customer, G/L Account, Supplier |
| LO_other | 0 | 3 | 1 | Customer, G/L Account, Supplier |
| MM-PUR_Purchasing | 0 | 3 | 1 | Customer, G/L Account, Supplier |
| SD-BIL_Billing | 0 | 3 | 1 | Customer, G/L Account, Supplier |
| LE | 0 | 3 | 0 | Customer, G/L Account, Supplier |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
