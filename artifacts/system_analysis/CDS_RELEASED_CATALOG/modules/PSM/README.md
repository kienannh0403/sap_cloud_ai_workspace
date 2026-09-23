# PSM

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `PSM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**35 view** · data category: (none) 20, Dimension 13, Cube 2 · loại: dimension 13, text 11, basic 5, value_help 4, cube 2 · 2 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PSM | 13 | top-level |
| PSM-FM-BU | 2 | top-level |
| PSM-FM-IS | 2 | top-level |
| PSM-FM-MD | 4 | top-level |
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
| I_FUNDTYPE | Fund Type | PSM | Dimension | 6 |
| I_PUBSECBUDGETCNSMPNTYPEGROUPT | Budget Consumption Type Group - Text | PSM-FM-UP |  | 6 |
| I_SPONSOREDPROGRAMTEXTCORE | Sponsored Program - Text | PSM-GM-GTE-MD |  | 6 |
| I_PUBSECBDGTCNSMPNTYPE | Budget Consumption Type | PSM-FM-UP |  | 5 |
| I_BUDGETDOCWORKFLOWSTATUS | Budget Document Work Flow Status | PSM | Dimension | 3 |
| I_COMMITMENTITEMSHORTID | Commitment Item Short ID | PSM |  | 3 |
| I_PUBSECBUDGETSCENARIO | Budget Scenario for Public Sector | PSM-FM-BU | Dimension | 3 |
| I_PUBSECBDGTACCTREVNEXPNCODE | Revenue and Expense Code for Bdgt Accts | PSM-FM-UP | Dimension | 3 |
| I_PUBSECBDGTCNSMPNAMTTYPE | Budget Consumption Amount Type | PSM-FM-UP | Dimension | 3 |
| I_PUBSECBUDGETCNSMPNTYPEGROUP | Budget Consumption Type Group | PSM-FM-UP | Dimension | 3 |
| I_GRANTEEMGMTFUNDTYPE | Grantee Management Fund Type | PSM-GM-GTE | Dimension | 3 |
| I_FUNDPERIODICITY | Fund Frequency | PSM-FM-MD |  | 2 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Grant | 3 |
| MASTER | Activity Type | 2 |
| ORG | Company Code | 2 |
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
| FI_other | 1 | 4 | 6 | Sales Document, Customer, G/L Account, Material / Product, Personnel |
| SD-SLS_Sales | 1 | 3 | 4 | Sales Document, Customer, Material / Product, Personnel |
| SD-BIL_Billing | 1 | 3 | 3 | Sales Document, Customer, G/L Account, Personnel |
| SD_other | 1 | 3 | 3 | Sales Document, Customer, Material / Product, Personnel |
| PM_other | 1 | 1 | 2 | Sales Document, Material / Product |
| PS_Project-System | 1 | 1 | 2 | Sales Document, Material / Product |
| MM-PUR_Purchasing | 0 | 6 | 3 | Activity Type, Customer, G/L Account, Grant, Material / Product, Personnel |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
