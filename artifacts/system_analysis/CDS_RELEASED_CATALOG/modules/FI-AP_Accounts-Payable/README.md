# FI-AP_Accounts-Payable — Accounts Payable

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `FI-AP` = **Accounts Payable**.

**11 view** · data category: (none) 6, Fact 3, Dimension 2 · loại: text 3, basic 3, fact 3, dimension 2 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| FI-AP-AP-B | 8 | component |
| FI-AP-AP-Q | 1 | component |
| FI-AP-IS | 2 | component |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PAYMENTPROPOSALPAYMENT | Payment Proposal Payment | FI-AP-AP-B | Fact | 153 |
| I_PAYMENTPROPOSALITEM | Payment Proposal Item | FI-AP-AP-B | Fact | 93 |
| I_WITHHOLDINGTAXITEM | Withholding Tax Item | FI-AP-AP-Q | Fact | 55 |
| I_PAYMENTPROGRAMCONTROL | Payment Program Control | FI-AP-AP-B |  | 18 |
| I_PAYMENTMETHOD | Payment Method for Country/Region | FI-AP-IS | Dimension | 12 |
| I_PAYTPRPSLBLKDFINACCOUNT | Payment Proposal Blocked Fin Account | FI-AP-AP-B |  | 11 |
| I_PAYMENTBLOCKLEVEL | Payment Block Level | FI-AP-AP-B | Dimension | 3 |
| I_PAYMENTREASON | Payment Reason for Purpose Codes | FI-AP-AP-B |  | 2 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 3 |
| MASTER | Customer | 2 |
| MASTER | Supplier | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI-GL_General-Ledger | 0 | 2 | 1 | Customer, Supplier |
| FI_other | 0 | 2 | 1 | Customer, Supplier |
| LO_other | 0 | 2 | 1 | Customer, Supplier |
| MM-PUR_Purchasing | 0 | 2 | 1 | Customer, Supplier |
| SD-BIL_Billing | 0 | 2 | 1 | Customer, Supplier |
| LE | 0 | 2 | 0 | Customer, Supplier |
| SD-SLS_Sales | 0 | 2 | 0 | Customer, Supplier |
| SD_other | 0 | 2 | 0 | Customer, Supplier |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
