# MM — Materials Management (Public Cloud)

Sub-areas: MM-PUR (purchasing: requisition, PO, contract, RFQ, info record, source list), MM-IM (inventory:
material documents, stock, physical inventory, reservations), MM-IV (supplier invoice), product master (LO-MD-MM).
Replaces sc4sap `configs/MM/` (ME21N, MIGO, MIRO, EKKO/EKPO/MSEG, BAPI_PO_CREATE1, ME_PROCESS_PO_CUST).

Legend **R / C / f / u**: see `configs/FI/README.md`. Files: [released-objects.md](released-objects.md).

## Key traps

- **`I_PurchaseOrder` / `I_PurchaseOrderItem` are NOT released** (repository: not found). Use
  `I_PurchaseOrderAPI01` / `I_PurchaseOrderItemAPI01` (C). Same pattern for requisition and info record (`…API01`).
- The classic PO BAdI `ME_PROCESS_PO_CUST` is *notToBeReleased*; its successor is `ES_MMPUR_PROCESS_PO_CLOUD` (R).
  Likewise `ME_PROCESS_OUT` → `MM_PUR_S4_CTR`, `ES_MMPUR_REQ_FIELDCONTROLS` → `MM_PUR_S4_PR_FLDCNTRL_SIMPLE`.
- Sourcing-project BDEFs (`I_SourcingProjectTP` …) are **deprecated** — do not build on them.
- Material = "Product" in S/4 Cloud: `I_Product`, `I_ProductPlantBasic`, `I_ProductText`.

## Key-user side (all **u**)

- Configuration via SSCUIs (document types, release strategy replaced by flexible workflow, movement types).
- Apps replace ME21N / MIGO / MIRO (Manage Purchase Orders, Post Goods Movement, Create Supplier Invoice …).
- PO / PR approval = flexible workflow; agents via `MMPUR_WORKFLOW_AGENTS_V2`, `MM_PUR_S4_PR_WFL_RESTART` (R).

## Also read

- Skill `sap-process-supplychain-inventory-mgmt`.
- Catalog folders `MM-PUR_Purchasing/` (115), `MM-IM_Inventory-Management/` (73), `MM_other/` (85),
  `LO-MD-MM_Material-Master/` (102).
- Blocklist: purchase orders / supplier invoices = ask; supplier master, bank, purchasing conditions = deny.
