# MM_other

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `MM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**117 view** · data category: (none) 90, Dimension 26, Fact 1 · loại: basic 72, dimension 26, text 18, fact 1 · 5 view có field DEPRECATED/DECOMMISSIONED · 32 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| MM | 69 | top-level |
| MM-IV-HUB-CIM-2CL | 2 | top-level |
| MM-IV-INT-WF-2CL | 4 | top-level |
| MM-IV-LIV-2CL | 42 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_SUPPLIERINVOICEAPI01 | Supplier Invoice | MM-IV-LIV-2CL |  | 91 |
| I_SUPLRINVCITMACCTASSGMTAPI01 | Account Assignment for Supplier Invoice | MM-IV-LIV-2CL |  | 49 |
| I_SUPLRINVOICEITEMGLACCTAPI01 | G/L Account Item of Supplier Invoice | MM-IV-LIV-2CL |  | 49 |
| I_SUPLRINVCITEMPURORDREFAPI01 | Purchase Order Ref of Supplier Invoice | MM-IV-LIV-2CL |  | 42 |
| C_SUPLRINVCBLKDWRKFLWEMLDCSN | Approve or Reject Email for Blocked Invoice | MM-IV-INT-WF-2CL |  | 25 |
| C_SUPLRINVCWRKFLWEMLDCSNRSN | Approve or Reject Email for Invoice | MM-IV-INT-WF-2CL |  | 25 |
| I_SUPCSGNMTPPLINEWTHDRWLAPI01 | Consignment and Pipeline Withdrawal of Supplier | MM-IV-LIV-2CL |  | 25 |
| I_SUPLRINVCITEMASSETAPI01 | Asset Item of Supplier Invoice | MM-IV-LIV-2CL |  | 24 |
| C_SUPLRINVCWRKFLWEMLDEADLINE | Supplier Invoice Details for WF Deadline Email | MM-IV-INT-WF-2CL |  | 23 |
| I_SUPLRINVCITEMCSGNMTAPI01 | Consignment Settlement Item | MM-IV-LIV-2CL |  | 23 |
| I_SUPLRINVCWRKFLWEMLDEADLINE | Supplier Invoice Details for Workflow Deadline Email | MM-IV-INT-WF-2CL |  | 22 |
| I_SUPLRINVCITEMMATERIALAPI01 | Material Item of Supplier Invoice | MM-IV-LIV-2CL |  | 21 |
| I_PURGOBJITEMTXTOBJOUTPRLVNCE | Output Relevance of Purchasing Itm Notes | MM |  | 16 |
| I_PURORDCHANGEDOCUMENTITEM | Purchase Order Change Document Items | MM |  | 16 |
| I_SUPPLIERINVOICETAXAPI01 | Tax for Supplier Invoice | MM-IV-LIV-2CL |  | 14 |
| I_PURGOBJTEXTOBJECTOUTPRLVNCE | Output Relevance of Purchasing Notes | MM |  | 13 |
| I_SUPLRINVCCHGDOCITMAPI01 | Change Document Items for Supplier Invoices | MM-IV-LIV-2CL |  | 13 |
| I_PURCHASEORDERCHANGEDOCUMENT | Purchase Order Change Document | MM |  | 10 |
| I_SUPLRINVCCHGDOCAPI01 | Change Documents for Supplier Invoices | MM-IV-LIV-2CL |  | 10 |
| I_SUPPLIERINVOICEBLOCKAPI01 | Supplier Invoice Block Logistics | MM-IV-LIV-2CL |  | 10 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| CONFIG | Fiscal Year | 21 |
| ORG | Company Code | 16 |
| CONFIG | Tax Code | 7 |
| ORG | Plant | 6 |
| ORG | Profit Center | 5 |
| ORG | Business Area | 4 |
| MASTER | Material / Product | 4 |
| MASTER | G/L Account | 4 |
| ORG | Purchasing Organization | 3 |
| MASTER | Fixed Asset | 2 |
| DOC | Purchasing Document | 2 |
| MASTER | Supplier | 2 |
| MASTER | Activity Type | 2 |
| ORG | Controlling Area | 2 |
| MASTER | Cost Center | 2 |
| ORG | Functional Area | 2 |
| MASTER | Grant | 2 |
| DOC | Order (production / maintenance / internal) | 2 |
| MASTER | Personnel | 2 |
| DOC | SD/LE Document (generic VBELN) | 2 |
| MASTER | WBS Element | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI_other | 3 | 9 | 6 | Order (production / maintenance / internal), Purchasing Document, SD/LE Document (generic VBELN), Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| CO_other | 3 | 6 | 7 | Order (production / maintenance / internal), Purchasing Document, SD/LE Document (generic VBELN), Activity Type, Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| MM-PUR_Purchasing | 2 | 9 | 7 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| FIN | 2 | 9 | 6 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Supplier, WBS Element |
| SD-BIL_Billing | 2 | 6 | 5 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Cost Center, G/L Account, Material / Product, Personnel, Supplier, WBS Element |
| PM_other | 2 | 5 | 7 | Order (production / maintenance / internal), Purchasing Document, Activity Type, Cost Center, Material / Product, Supplier, WBS Element |
| LE | 2 | 5 | 5 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| SD_other | 2 | 5 | 5 | Order (production / maintenance / internal), SD/LE Document (generic VBELN), Cost Center, Material / Product, Personnel, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
