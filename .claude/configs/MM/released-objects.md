# MM — released objects

Legend: see `configs/FI/README.md`.

## 1. Read — CDS views

| Area | Views | Evidence |
|---|---|---|
| Purchase order | `I_PurchaseOrderAPI01`, `I_PurchaseOrderItemAPI01` | C |
| Purchase requisition | `I_PurchaseRequisitionAPI01`, `I_PurchaseRequisitionItemAPI01` | C |
| Info record | `I_PurchasingInfoRecordApi01` | C |
| Org | `I_PurchasingOrganization`, `I_PurchasingGroup`, `I_Plant`, `I_StorageLocation` | C |
| Material documents | `I_MaterialDocumentHeader_2`, `I_MaterialDocumentItem_2` | C |
| Stock | `I_MaterialStock_2`, `I_StockQuantityCurrentValue_2` | C |
| Physical inventory / reservation | `I_PhysInvtryDocItem`, `I_ReservationDocumentItem` | C |
| Supplier invoice | `I_SupplierInvoiceAPI01` | C |
| Product master | `I_Product`, `I_ProductPlantBasic`, `I_ProductText` | C |

**Not released:** `I_PurchaseOrder`, `I_PurchaseOrderItem` (repository: not found). `I_PurchaseContract` not in
catalog — use `I_PurchaseContractTP` read access or check the repository.

## 2. Write — RAP BOs (EML), all R

| BO | Purpose |
|---|---|
| `I_PurchaseOrderTP_2` | Purchase order |
| `I_PurchaseRequisitionTP` | Purchase requisition |
| `I_PurchaseContractTP` | Purchase contract |
| `I_SchedgAgrmtHdrTP_2` | Scheduling agreement |
| `I_RequestForQuotationTP`, `I_SupplierQuotationTP` (+ `D_RFQCreateFromPurReqnP`, `D_SuplrQtanCrteFrmRFQP`) | RFQ / quotation |
| `I_PurchasingInfoRecordTP`, `I_PurchasingSourceListTP`, `I_PurgQuotaArrgmtTP_2` | Sources of supply |
| `I_ServiceEntrySheetTP_2` | Service entry sheet |
| `I_StockTransportOrderTP` | Stock transport order |
| `I_MaterialDocumentTP` (+ `D_MaterialDocumentCancelP`) | Goods movements |
| `I_PhysicalInventoryDocumentTP`, `I_ReservationDocumentTP` | Physical inventory, reservations |
| `I_SupplierInvoiceTP` (+ `D_SuplrInvcCreateP`, `D_SuplrInvcChangeP`) | Supplier invoice |
| Central procurement: `I_CntrlPurchaseContractTP_2`, `I_CntrlRequestForQuotationTP_2`, `I_CentralSupplierQuotationTP_2` | Only if central procurement is in scope |

Deprecated (do not use): `I_SourcingProjectTP`, `I_ProcurementProjectTP`, `I_SupplierListTP_2` and related.

## 3. Extend — enhancement spots (all R unless noted; 79 in total, main ones below)

| Spot | Area |
|---|---|
| `ES_MMPUR_PROCESS_PO_CLOUD` | Purchase order checks / changes (successor of `ME_PROCESS_PO_CUST`) |
| `MM_PUR_S4_PR`, `MM_PUR_S4_PR_FLDCNTRL_SIMPLE` | Purchase requisition, field control |
| `MM_PUR_S4_CTR`, `MM_PUR_S4_SA`, `MM_PUR_S4_RFQ`, `MM_PUR_S4_QTN`, `MM_PUR_S4_SES`, `MM_PUR_S4_SL` | Contract, scheduling agreement, RFQ, quotation, service entry sheet, source list |
| `MMPUR_WORKFLOW_AGENTS_V2`, `MMPUR_WFL_CONTEXT_ENHANCE`, `MMPUR_PO_WORKFLOW_RESTART` | Flexible workflow |
| `MMPUR_PURCHASE_ORDER_OUTPUT`, `MMPUR_PO_OUTPUT_TEXT` | PO output |
| `MMIM_CLOUD_BADI`, `MMIM_CREATE_GOODS_MOVEMENT`, `MMIM_PI_MANAGE_COUNT` | Inventory |
| `MRM_CHECK_INVOICE_CLOUD`, `MRM_HEADER_DATA_DEFAULT`, `MRM_ERS_CLOUD`, `MRM_WORKFLOW_AGENTS` | Supplier invoice |
