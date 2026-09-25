# PSM

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `PSM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**44 view** · data category: (none) 29, Dimension 13, Cube 2 · loại: basic 14, dimension 13, text 11, value_help 4, cube 2 · 2 view có field DEPRECATED/DECOMMISSIONED · 9 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PSM | 19 | top-level |
| PSM-FM-BU | 2 | top-level |
| PSM-FM-IS | 3 | top-level |
| PSM-FM-MD | 5 | top-level |
| PSM-FM-PO-EF | 1 | top-level |
| PSM-FM-UP | 8 | top-level |
| PSM-GM-GTE | 1 | top-level |
| PSM-GM-GTE-MD | 5 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PUBSECCMTMTACTLITEMCUBE | Commitment and Actual Items - Cube | PSM-FM-IS | Cube | 476 |
| I_PUBSECBDGTLINEITEMCUBE | Budget Line Items - Cube | PSM-FM-IS | Cube | 227 |
| I_FUNDSMGMTFUNCTIONALAREA | Funds Management Functional Area | PSM | Dimension | 25 |
| I_PUBSECBUDGETACCOUNT | Budget Account | PSM-FM-MD | Dimension | 23 |
| I_SPONSOREDCLASSCORE | Sponsored Class | PSM-GM-GTE-MD | Dimension | 14 |
| I_SPONSOREDPROGRAMCORE | Sponsored Program | PSM-GM-GTE-MD | Dimension | 10 |
| I_FINANCIALMANAGEMENTAREA | Financial Management Area | PSM | Dimension | 8 |
| I_FISCALYEARFORFINMGMTAREA | Fiscal Year for Fin Management Area | PSM | Dimension | 7 |
| I_EMRKDFUNDDOCMAILPARAM | Earmarked Funds Document Email Parameter | PSM-FM-PO-EF |  | 7 |
| I_FUNDTYPE | Fund Type | PSM | Dimension | 6 |
| I_PUBSECBUDGETCNSMPNTYPEGROUPT | Budget Consumption Type Group - Text | PSM-FM-UP |  | 6 |
| I_SPONSOREDPROGRAMTEXTCORE | Sponsored Program - Text | PSM-GM-GTE-MD |  | 6 |
| I_PUBSECBDGTCNSMPNTYPE | Budget Consumption Type | PSM-FM-UP |  | 5 |
| I_PUBSECPLANNINGCATEGORY | Planning Category for PSM | PSM-FM-IS |  | 4 |
| I_BUDGETDOCWORKFLOWSTATUS | Budget Document Work Flow Status | PSM | Dimension | 3 |
| I_COMMITMENTITEMSHORTID | Commitment Item Short ID | PSM |  | 3 |
| I_PUBSECBUDGETSCENARIO | Budget Scenario for Public Sector | PSM-FM-BU | Dimension | 3 |
| I_FISCALYEARFORCOMMITMENTITEM | Fiscal years of Commitment Item | PSM-FM-MD |  | 3 |
| I_PUBSECBDGTACCTREVNEXPNCODE | Revenue and Expense Code for Bdgt Accts | PSM-FM-UP | Dimension | 3 |
| I_PUBSECBDGTCNSMPNAMTTYPE | Budget Consumption Amount Type | PSM-FM-UP | Dimension | 3 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 3 |
| MASTER | Grant | 3 |
| MASTER | Activity Type | 2 |
| ORG | Controlling Area | 2 |
| MASTER | Customer | 2 |
| ORG | Distribution Channel | 2 |
| CONFIG | Fiscal Year | 2 |
| MASTER | G/L Account | 2 |
| MASTER | Material / Product | 2 |
| MASTER | Personnel | 2 |
| ORG | Plant | 2 |
| DOC | Sales Document | 2 |
| CONFIG | Sales Document Type | 2 |
| ORG | Sales Organization | 2 |
| ORG | Segment | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI-GL_General-Ledger | 1 | 6 | 6 | Sales Document, Activity Type, Customer, G/L Account, Grant, Material / Product, Personnel |
| FIN | 1 | 6 | 6 | Sales Document, Activity Type, Customer, G/L Account, Grant, Material / Product, Personnel |
| FI_other | 1 | 6 | 6 | Sales Document, Activity Type, Customer, G/L Account, Grant, Material / Product, Personnel |
| SD-BIL_Billing | 1 | 4 | 5 | Sales Document, Customer, G/L Account, Material / Product, Personnel |
| CO-OM_Cost-Center-Accounting | 1 | 4 | 4 | Sales Document, Activity Type, Customer, G/L Account, Personnel |
| CO_other | 1 | 3 | 6 | Sales Document, Activity Type, G/L Account, Material / Product |
| SD_other | 1 | 3 | 5 | Sales Document, Customer, Material / Product, Personnel |
| SD-SLS_Sales | 1 | 3 | 4 | Sales Document, Customer, Material / Product, Personnel |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
