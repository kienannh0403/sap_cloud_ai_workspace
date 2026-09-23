# CRM

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `CRM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**107 view** · data category: (none) 55, Dimension 37, Fact 9, Cube 6 · loại: dimension 37, text 37, basic 17, fact 9, cube 6, value_help 1 · 14 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CRM-S4-ANA-CDS | 10 | top-level |
| CRM-S4-BF-CM | 4 | top-level |
| CRM-S4-REP-RFW | 90 | top-level |
| CRM-S4-SRV-SVO-FIO | 3 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SERVICEDOCUMENTITEMENHCD | Service Transaction Item Enhanced | CRM-S4-REP-RFW | Dimension | 409 |
| I_SERVICEDOCUMENTITEM | Service Transaction Item | CRM-S4-REP-RFW | Dimension | 386 |
| I_SERVICEDOCUMENTENHCD | Service Transaction Enhanced | CRM-S4-REP-RFW | Dimension | 197 |
| I_SERVICEDOCUMENT | Service Transaction | CRM-S4-REP-RFW | Dimension | 183 |
| I_SERVICECONTRACTITEMENHCD | Service Contract Item Enhanced | CRM-S4-REP-RFW |  | 137 |
| I_SRVCDOCITEMBYDOCUMENTTYPE | Srvc Transaction Item by Transac Type | CRM-S4-REP-RFW | Dimension | 127 |
| I_SERVICECONTRACTITEM | Service Contract Item | CRM-S4-REP-RFW |  | 123 |
| I_SRVCDOCBYDOCUMENTTYPE | Service Transaction by Transaction Type | CRM-S4-REP-RFW | Dimension | 109 |
| I_SERVICECONTRACTENHCD | Service Contract Enhanced | CRM-S4-REP-RFW |  | 93 |
| I_SERVICECONTRACT | Service Contract | CRM-S4-REP-RFW |  | 84 |
| I_SERVICEORDERCUBE_2 | Service Order - Cube | CRM-S4-ANA-CDS | Cube | 70 |
| I_UPCGSRVCCONTRITEMCUBE | Upcoming Service Contract Item - Cube | CRM-S4-ANA-CDS | Cube | 70 |
| I_BUSSOLNORDITMBASICFINANCIAL | Solution Order Item for Fin Reporting | CRM-S4-ANA-CDS | Dimension | 69 |
| I_SERVICECONTRACTCUBE_2 | Service Contract - Cube | CRM-S4-ANA-CDS | Cube | 68 |
| I_SRVCDOCITEMPRICEELEMENT | Service Transaction Item Pricing Element | CRM-S4-REP-RFW |  | 68 |
| I_SRVCCONTRITEMPRICEELEMENT | Service Contract Item Pricing Element | CRM-S4-REP-RFW |  | 66 |
| I_BSORDGLACCTLINEITEMCUBE | GL Account Item for Soln Order - Cube | CRM-S4-ANA-CDS | Cube | 61 |
| I_BUSSOLNORDITMFINANCIALCUBE | Solution Order Item Financials - Cube | CRM-S4-ANA-CDS | Cube | 61 |
| I_BUSSOLNORDBASICFINANCIAL | Solution Order for Financial Reporting | CRM-S4-ANA-CDS | Dimension | 49 |
| I_BUSINESSSOLUTIONORDERCUBE | Solution Order - Cube | CRM-S4-ANA-CDS | Cube | 39 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Sales Organization | 20 |
| ORG | Sales Group | 19 |
| ORG | Sales Office | 19 |
| MASTER | Material / Product | 8 |
| MASTER | WBS Element | 8 |
| ORG | Controlling Area | 6 |
| ORG | Profit Center | 6 |
| DOC | Document Condition (pricing) | 5 |
| MASTER | Equipment | 2 |
| MASTER | Batch | 2 |
| MASTER | Cost Center | 2 |
| ORG | Plant | 2 |
| CONFIG | Tax Code | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| LE | 1 | 4 | 6 | Document Condition (pricing), Batch, Cost Center, Material / Product, WBS Element |
| SD-SLS_Sales | 1 | 4 | 6 | Document Condition (pricing), Batch, Cost Center, Material / Product, WBS Element |
| MM-PUR_Purchasing | 1 | 4 | 3 | Document Condition (pricing), Batch, Cost Center, Material / Product, WBS Element |
| LO_other | 1 | 3 | 5 | Document Condition (pricing), Batch, Equipment, Material / Product |
| QM | 0 | 5 | 4 | Batch, Cost Center, Equipment, Material / Product, WBS Element |
| SD_other | 0 | 4 | 5 | Batch, Cost Center, Material / Product, WBS Element |
| FI-GL_General-Ledger | 0 | 4 | 4 | Cost Center, Equipment, Material / Product, WBS Element |
| MM-IM_Inventory-Management | 0 | 4 | 3 | Batch, Cost Center, Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
