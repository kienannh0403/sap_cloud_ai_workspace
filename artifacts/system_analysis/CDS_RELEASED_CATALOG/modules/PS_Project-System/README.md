# PS_Project-System — Project System

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Phân hệ ưu tiên (Sheet1): component `PS` = **Project System**.

**171 view** · data category: (none) 146, Dimension 24, Fact 1 · loại: basic 112, text 33, dimension 24, fact 1, value_help 1 · 0 view có field DEPRECATED/DECOMMISSIONED · 76 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| PPM-SCL-BIL | 46 | alias |
| PPM-SCL-DMN | 40 | alias |
| PPM-SCL-PRS | 1 | alias |
| PPM-SCL-STR | 84 | alias |

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
| I_WRITTENOFFPRJBILLGELMENTRY | Written off PBE entries | PPM-SCL-BIL |  | 33 |
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

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | WBS Element | 11 |
| DOC | Sales Document | 5 |
| ORG | Plant | 5 |
| ORG | Functional Area | 4 |
| ORG | Profit Center | 4 |
| ORG | Company Code | 3 |
| MASTER | Material / Product | 3 |
| CONFIG | Fiscal Year | 2 |
| DOC | SD/LE Document (generic VBELN) | 2 |
| MASTER | Grant | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI_other | 2 | 3 | 4 | SD/LE Document (generic VBELN), Sales Document, Grant, Material / Product, WBS Element |
| CO_other | 2 | 2 | 4 | SD/LE Document (generic VBELN), Sales Document, Material / Product, WBS Element |
| SD-BIL_Billing | 2 | 2 | 3 | SD/LE Document (generic VBELN), Sales Document, Material / Product, WBS Element |
| SD_other | 2 | 2 | 3 | SD/LE Document (generic VBELN), Sales Document, Material / Product, WBS Element |
| FIN | 1 | 3 | 4 | Sales Document, Grant, Material / Product, WBS Element |
| MM_other | 1 | 3 | 4 | SD/LE Document (generic VBELN), Grant, Material / Product, WBS Element |
| FI-GL_General-Ledger | 1 | 3 | 3 | Sales Document, Grant, Material / Product, WBS Element |
| PM_other | 1 | 2 | 4 | Sales Document, Material / Product, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
