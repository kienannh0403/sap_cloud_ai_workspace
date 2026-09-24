# PM — Plant / Asset Maintenance, EAM (Public Cloud)

Sub-areas: technical objects (equipment, functional location, measuring points — PM-EQM), notifications and orders
(PM-WOC), preventive maintenance (maintenance plans / items / task lists — PM-PRM).
Replaces sc4sap `configs/PM/` (IW31/IW21/IE01, AUFK/AFIH/QMEL/EQUI, BAPI_ALM_ORDER_MAINTAIN, IWO10018 exits).

Legend **R / C / f / u**: see `configs/FI/README.md`.

## Traps

- **`I_MaintenanceOrder` is NOT released** (repository: not found). Use `I_MaintenanceOrderBasic` (R) or read through
  the TP views (`I_MaintenanceOrderTP`, `I_MaintenanceOrderOperationTP` — R). Status: `I_MaintenanceOrderStatus` (R).
- `I_MaintenancePlan` / `I_MaintenancePlant` not in catalog or repository search — use `I_MaintenancePlanTP_2` read.

## Read — CDS views

| Views | Evidence |
|---|---|
| `I_MaintenanceNotification`, `I_Equipment`, `I_FunctionalLocation`, `I_TechnicalObject`, `I_MeasuringPoint`, `I_MaintenanceItem` | C |
| `I_MaintenanceOrderBasic`, `I_MaintenanceOrderStatus`, `I_MaintenanceOrderPhase`, `I_MaintenanceOrderDEX` | R |

## Write — RAP BOs (EML), all R

`I_MaintenanceOrderTP` (+ `D_MaintOrdTechnicalCompleteP`), `I_MaintOrderConfirmationTP` (+ `D_MaintOrdConfirmationCancelP`),
`I_MaintenanceNotificationTP_2`, `I_EquipmentTP`, `I_FunctionalLocationTP`, `I_EquipMatlSerialNumberTP`,
`I_MaintenancePlanTP_2`, `I_MaintenanceItemTP_2`, `I_MaintenanceTaskListTP_2`, `I_MeasuringPointTP_2`,
`I_MeasurementDocumentTP_2`.

## Extend — enhancement spots, all R

`EAMS_ORDER_EXT` (maintenance order), `EAMS_TO_EXT` (technical objects), `EAM_ORDER_PROCMT_INTEG` (order procurement).
Only 3 spots in PM — most PM logic changes go through the BDEF-based BOs or key-user custom logic.

## Also read

Catalog folders `PM_other/` (69), `EAM-OBJ_Technical-Objects/` (28). Key-user config / apps: all **u**.
