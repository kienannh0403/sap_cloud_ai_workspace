# PP — Production Planning & Execution (Public Cloud)

Sub-areas: MRP / planned orders / PIR (PP-MRP, PP-PLO, PP-MP), discrete production orders (PP-SFC), process orders
(PP-PI), repetitive (PP-REM), kanban (PP-KAB), master data (work center, routing, production version, BOM in LO-MD-BOM).
Replaces sc4sap `configs/PP/` (CO01, MD04, AFKO/AFPO/RESB, BAPI_PRODORD_*, WORKORDER_UPDATE).

Legend **R / C / f / u**: see `configs/FI/README.md`. Files: [released-objects.md](released-objects.md).

## Key traps

- Order header views: `I_ManufacturingOrder` (C) covers production *and* process orders; `I_ProductionOrder` is
  released (R) but only in the catalog's `_fields_only/`. `I_ProcessOrder` not found.
- BOM: `I_BillOfMaterial` / `I_BillOfMaterialItem` not found; released are `I_BillOfMaterialHeaderDEX_2`,
  `I_BillOfMaterialItemBasic`, `I_BillOfMaterialItemDEX_3` (R), `I_MaterialBOMLink` (C). `…DEX` / `…DEX_2` older
  versions are deprecated.
- `WORKORDER_UPDATE` (classic) is *notToBeReleased* → `ES_COBADICFL_MFGORDER` (R). `MD_ADD_ELEMENTS` →
  `ES_PPH_SUPPLY_DEMAND_LIST` (R).
- `verified_external/PP.md` lists fields verified on a real tenant (e.g. `I_PlndIndepRqmtTp` for PIR writes).

## Key-user side (all **u**)

- Configuration via SSCUIs (order types, scheduling, MRP groups). Apps replace CO01/CO11N/MD04 (Manage Production
  Orders, Confirm Production Operation, Monitor Material Coverage …).

## Also read

- Skills `sap-process-production-discrete-planning`, `-process-planning`, `-repetitive-planning`,
  `sap-process-manufacturing-discrete-execution`, `-process-execution`, `-repetitive-execution`.
- Catalog folders `PP_other/` (300), `PP-MRP_MRP/` (71), `PP-SFC_Shop-Floor-Control/` (23),
  `LO-MD-BOM_Bill-of-Material/` (9); `verified_external/PP.md`.
