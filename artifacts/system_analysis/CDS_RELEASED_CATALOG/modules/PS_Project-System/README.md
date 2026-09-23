# PS_Project-System — Project System

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `PS` = **Project System**.

**95 view** · data category: (none) 70, Dimension 24, Fact 1 · loại: basic 43, text 27, dimension 24, fact 1 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PPM-SCL-BIL | 31 | alias |
| PPM-SCL-DMN | 24 | alias |
| PPM-SCL-STR | 40 | alias |

> `alias` = component khác tên trong Sheet1 nhưng cùng nội dung (xem `module_map.md`); `keyword` = **suy luận theo tên view**, độ tin cậy thấp hơn `component`.

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PROJECTBILLINGELEMENTENTRY | Entries for Project Billing Element | PPM-SCL-BIL |  | 75 |
| I_PROJECTBILLINGREQUESTITEM | Items for Project Billing Request | PPM-SCL-BIL |  | 62 |
| I_ENTERPRISEPROJECT | Enterprise Project | PPM-SCL-STR | Dimension | 58 |
| I_PROJECTBILLINGELEMENTENTRFLW | Entry Flow for Project Billing Element | PPM-SCL-BIL |  | 56 |
| I_ENTERPRISEPROJECTELEMENT | Enterprise Project Element | PPM-SCL-STR | Dimension | 53 |
| I_PROJECTDEMAND | Project Demand | PPM-SCL-DMN |  | 50 |
| I_ENTERPRISEPROJECTELEMENT_2 | Enterprise Project Element | PPM-SCL-STR | Dimension | 49 |
| I_PROJECTBILLINGELEMENT | Project Billing Element | PPM-SCL-BIL |  | 26 |
| I_PROJECTBILLINGREQUEST | Project Billing Request | PPM-SCL-BIL |  | 23 |
| I_PROJDMNDRSCEASSGMTDISTR | Rsce Assgmt Distribution for Rsce Dmnd | PPM-SCL-DMN |  | 23 |
| I_PROJDMNDRSCEREQDISTRIBUTION | Resource Req Distribution for Rsce Dmnd | PPM-SCL-DMN |  | 22 |
| I_PROJDMNDRESOURCEASSIGNMENT | Resource Assignment to Rsce Dmnd | PPM-SCL-DMN |  | 20 |
| I_ENTPRJELMNTPROFNLSRVCPLNDKPI | Work package attributes and planned KPIs | PPM-SCL-STR |  | 20 |
| I_PRJBLGELMENTRJRNLENTRLINK | Journal Entry for Billing Element | PPM-SCL-BIL |  | 19 |
| I_PROJECTDEMANDMATERIAL | Project Demand for Material | PPM-SCL-DMN |  | 19 |
| I_ENTPROJCHGDOCUMENTDEX | Data Extraction for Project Change Document | PPM-SCL-STR | Fact | 19 |
| I_PROJSRVCORG | Service Organization | PPM-SCL-STR |  | 19 |
| I_PROJECTDEMANDSERVICE | Project Demand for Service | PPM-SCL-DMN |  | 18 |
| I_PROJECTDEMANDWORK | Project Demand for Resource | PPM-SCL-DMN |  | 17 |
| I_PROJDMNDEXPENSEDISTRIBUTION | Distribution of Proj Demand for Expense | PPM-SCL-DMN |  | 16 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| DOC | Sales Document | 5 |
| MASTER | WBS Element | 5 |
| ORG | Plant | 4 |
| ORG | Functional Area | 3 |
| ORG | Profit Center | 3 |
| ORG | Company Code | 2 |
| DOC | SD/LE Document (generic VBELN) | 2 |
| MASTER | Material / Product | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| SD_other | 2 | 2 | 1 | SD/LE Document (generic VBELN), Sales Document, Material / Product, WBS Element |
| FI-GL_General-Ledger | 1 | 2 | 4 | Sales Document, Material / Product, WBS Element |
| FI_other | 1 | 2 | 4 | Sales Document, Material / Product, WBS Element |
| MM_other | 1 | 2 | 4 | SD/LE Document (generic VBELN), Material / Product, WBS Element |
| LE | 1 | 2 | 3 | SD/LE Document (generic VBELN), Material / Product, WBS Element |
| CO_other | 1 | 2 | 2 | SD/LE Document (generic VBELN), Material / Product, WBS Element |
| SD-SLS_Sales | 1 | 2 | 2 | Sales Document, Material / Product, WBS Element |
| PM_other | 1 | 2 | 1 | Sales Document, Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
