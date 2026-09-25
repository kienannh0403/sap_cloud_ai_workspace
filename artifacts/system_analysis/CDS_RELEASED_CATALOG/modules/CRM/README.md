# CRM

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `CRM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**315 view** · data category: (none) 263, Dimension 37, Fact 9, Cube 6 · loại: basic 219, text 39, dimension 37, fact 9, cube 6, value_help 5 · 18 view có field DEPRECATED/DECOMMISSIONED · 208 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CRM-S4-ANA-BI-2CL | 6 | top-level |
| CRM-S4-ANA-CDS-2CL | 10 | top-level |
| CRM-S4-BF-CM-2CL | 4 | top-level |
| CRM-S4-BTX-2CL | 18 | top-level |
| CRM-S4-REP-RFW | 103 | top-level |
| CRM-S4-SOL-SLO | 46 | top-level |
| CRM-S4-SRV-CTR-2CL | 32 | top-level |
| CRM-S4-SRV-MC-2CL | 2 | top-level |
| CRM-S4-SRV-SCO-2CL | 22 | top-level |
| CRM-S4-SRV-SVO-2CL | 34 | top-level |
| CRM-S4-SRV-SVQ-2CL | 24 | top-level |
| CRM-S4-SRV-SVT-2CL | 14 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SERVICEDOCUMENTITEMENHCD | Service Transaction Item Enhanced | CRM-S4-REP-RFW | Dimension | 409 |
| I_SERVICEDOCUMENTITEM | Service Transaction Item | CRM-S4-REP-RFW | Dimension | 386 |
| I_SERVICEDOCUMENTITEM_2 | Service Transaction Item v2 | CRM-S4-REP-RFW |  | 263 |
| I_SERVICEDOCUMENTENHCD | Service Transaction Enhanced | CRM-S4-REP-RFW | Dimension | 197 |
| I_SERVICEDOCUMENT | Service Transaction | CRM-S4-REP-RFW | Dimension | 183 |
| I_BUSSOLUTIONORDERITEMENHCD | Solution Order Item Enhanced | CRM-S4-REP-RFW |  | 171 |
| I_BUSINESSSOLUTIONORDERITEM | Solution Order Item | CRM-S4-REP-RFW |  | 160 |
| C_SERVICEORDERITEMDEX | Data Extraction for Service Order | CRM-S4-ANA-BI-2CL |  | 147 |
| C_SERVICECONTRACTITEMDEX | Data Extraction for Service Contract | CRM-S4-ANA-BI-2CL |  | 142 |
| I_SERVICECONTRACTITEMENHCD | Service Contract Item Enhanced | CRM-S4-REP-RFW |  | 137 |
| I_SERVICEDOCUMENT_2 | Service Transaction v2 | CRM-S4-REP-RFW |  | 134 |
| I_SRVCDOCITEMBYDOCUMENTTYPE | Srvc Transaction Item by Transac Type | CRM-S4-REP-RFW | Dimension | 127 |
| C_BUSINESSSOLUTIONORDERITEMDEX | Data Extraction for Bussiness Solution Order | CRM-S4-ANA-BI-2CL |  | 125 |
| I_SERVICECONTRACTITEM | Service Contract Item | CRM-S4-REP-RFW |  | 123 |
| C_SERVICECONFIRMATIONITEMDEX | Data Extraction for Service Confirmation | CRM-S4-ANA-BI-2CL |  | 118 |
| I_SRVCDOCBYDOCUMENTTYPE | Service Transaction by Transaction Type | CRM-S4-REP-RFW | Dimension | 109 |
| I_SERVICECONTRACTENHCD | Service Contract Enhanced | CRM-S4-REP-RFW |  | 93 |
| I_SERVICECONTRACT | Service Contract | CRM-S4-REP-RFW |  | 84 |
| I_SERVICEORDERCUBE_2 | Service Order - Cube | CRM-S4-ANA-CDS-2CL | Cube | 70 |
| I_UPCGSRVCCONTRITEMCUBE | Upcoming Service Contract Item - Cube | CRM-S4-ANA-CDS-2CL | Cube | 70 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Sales Organization | 32 |
| ORG | Sales Group | 31 |
| ORG | Sales Office | 31 |
| MASTER | Material / Product | 17 |
| ORG | Controlling Area | 13 |
| ORG | Profit Center | 13 |
| MASTER | WBS Element | 12 |
| MASTER | Equipment | 8 |
| MASTER | Cost Center | 6 |
| ORG | Plant | 6 |
| DOC | Document Condition (pricing) | 6 |
| CONFIG | Tax Code | 3 |
| MASTER | Business Partner | 2 |
| ORG | Company Code | 2 |
| MASTER | Batch | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD-BIL_Billing | 1 | 5 | 7 | Document Condition (pricing), Batch, Business Partner, Cost Center, Material / Product, WBS Element |
| SD_other | 1 | 5 | 7 | Document Condition (pricing), Batch, Business Partner, Cost Center, Material / Product, WBS Element |
| SD-SLS_Sales | 1 | 5 | 6 | Document Condition (pricing), Batch, Business Partner, Cost Center, Material / Product, WBS Element |
| MM-PUR_Purchasing | 1 | 5 | 4 | Document Condition (pricing), Batch, Business Partner, Cost Center, Material / Product, WBS Element |
| LE | 1 | 4 | 6 | Document Condition (pricing), Batch, Cost Center, Material / Product, WBS Element |
| LO_other | 1 | 4 | 6 | Document Condition (pricing), Batch, Business Partner, Equipment, Material / Product |
| FI_other | 0 | 5 | 5 | Batch, Business Partner, Cost Center, Material / Product, WBS Element |
| QM | 0 | 5 | 5 | Batch, Cost Center, Equipment, Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
