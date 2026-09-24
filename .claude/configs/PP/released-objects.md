# PP — released objects

Legend: see `configs/FI/README.md`.

## 1. Read — CDS views

| Area | Views | Evidence |
|---|---|---|
| Manufacturing orders | `I_ManufacturingOrder`, `I_ManufacturingOrderItem`, `I_ManufacturingOrderOperation` | C |
| Production order | `I_ProductionOrder` | R (catalog: f) |
| Confirmations | `I_MfgOrderConfirmation` | C |
| Planned orders | `I_PlannedOrder` | C |
| Master data | `I_ProductionVersion`, `I_WorkCenter`, `I_MRPController`, `I_MaterialBOMLink` | C |
| BOM | `I_BillOfMaterialHeaderDEX_2`, `I_BillOfMaterialItemBasic`, `I_BillOfMaterialItemDEX_3` | R |

Not found: `I_ProcessOrder`, `I_ProductionRouting`, `I_PlndIndepRqmt`, `I_SupplyDemandItem` (read via their TP views
or check the repository).

## 2. Write — RAP BOs (EML), all R

| BO | Purpose |
|---|---|
| `I_ProductionOrderTP` (+ `D_ProductionOrderReleaseP_2`, `D_ProdnOrdReexplodeMasterDataP`, `D_ProdnOrdOperationSetDatesP_2`) | Production order |
| `I_ProductionOrdConfirmationTP` | Production order confirmation |
| `I_ProcessOrderTP`, `I_ProcessOrderConfirmationTP` | Process order + confirmation |
| `I_PlannedOrderTP` (+ `D_PlndOrdCnvrtToProdnOrderP`, `D_PlndOrdCnvrtToProcessOrderP`) | Planned order, conversion |
| `I_PlndIndepRqmtTP` | Planned independent requirements |
| `I_RepetitiveMfgConfirmationTP` | Repetitive manufacturing confirmation |
| `I_KanbanControlCycleTP`, `I_ProductionSupplyAreaTP_2` | Kanban |
| `I_WorkCenterTP`, `I_WorkCenterPooledCapacityTP`, `I_ProductionRoutingTP_2`, `I_ProductionVersionTP` | Master data |
| `I_SupplyDemandItemTP` | Supply / demand items |

## 3. Extend — enhancement spots (all R)

| Spot | Area |
|---|---|
| `ES_COBADICFL_MFGORDER`, `ES_COBADICFL_ORDER` | Manufacturing order checks / changes (successor of `WORKORDER_UPDATE`) |
| `ES_COBADI_WORKORDER_GOODSMOVT`, `ES_CONF_BATCH_DETERMINATION` | Goods movements, batch determination at confirmation |
| `ES_COBADI_API_SETTINGS`, `ES_COBADI_MES_REDISTRIBUTION` | API / MES integration |
| `ES_PPH_MRP_BADI_CFL`, `ES_PPH_SUPPLY_DEMAND_LIST`, `ES_PPH_NFP_CALCULATION` | MRP |
| `PP_MRP_CR_RESCHEDULE_CHECKS`, `PP_MRP_CR_GET_CONTROL_PARAM`, `PP_MRP_SUPPLY_AND_DEMAND_ITEM` | MRP apps |
| `ES_KANBAN_CONTROLCYCLE` | Kanban |
| `ES_MAN_OM_MOR_CFLBADI` | Order print / output |
| `PPH_MD_PRODN_VERS_PROPOSAL` | Production version proposal |
