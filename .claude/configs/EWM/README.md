# EWM — Extended Warehouse Management (Public Cloud, replaces WM)

Classic WM (LT01, LTAK/LTAP, lean WM) does not exist in Public Cloud; warehouse processes use **embedded EWM**
(component SCM-EWM, namespace `/SCWM/`). sc4sap `configs/WM/` maps here.

Legend **R / C / f / u**: see `configs/FI/README.md`.

## Read — CDS views

| Views | Evidence |
|---|---|
| `I_EWM_AvailableStock`, `I_EWM_PhysStockProd`, `I_EWM_ProductWarehouse`, `I_EWM_ProductStorageType`, `I_EWM_FixedBinAssignment` | C |
| `I_EWM_InbDeliveryHeader` / `…Item`, `I_EWM_OutbDelivOrdHdr` / `…Item` | C |
| `I_EWM_PhysicalInventoryItem`, `I_EWM_HndlgUnitID`, `I_EWM_PlantStorLocMapToWhse` | C |
| `I_EWM_WarehouseTask_2` | R |

Names are `I_EWM_*` with short forms — `I_EWM_OutbDelivOrderHeader`, `I_EWM_StorageBin`, `I_EWM_WarehouseOrder` were
**not** found; confirm the exact name before use.

## Write — RAP BOs (EML)

Only `I_EWM_OutbDelivOrderHeaderTP` (R). Most EWM writes go through apps / standard APIs, not EML.

## Extend — enhancement spots, all R

`/SCWM/ES4_CORE_CR`, `/SCWM/ES4_CORE_PTS`, `/SCWM/ES4_CORE_RMS` (warehouse operations), `/SCWM/ES4_OM_EXTEND`
(output), `/SCWM/ES_PACK_OUTBDLV` (packing).

## Also read

Skill `sap-process-supplychain-warehouse-mgmt`; catalog folder `SCM/` (41, SCM-EWM). Key-user config: all **u**.
