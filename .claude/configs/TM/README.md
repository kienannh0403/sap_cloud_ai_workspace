# TM — Transportation Management (Public Cloud, embedded TM)

Sub-areas: freight orders / bookings (TM-FRM), freight units (TM-PLN), freight agreements and rate tables (TM-FRA,
TM-MD-CM). Replaces sc4sap `configs/TM/` (on-prem /SCMTMS/ BOPF, tables `/SCMTMS/D_*`).

Legend **R / C / f / u**: see `configs/FI/README.md`.

## Traps (from `verified_external/LE-TM.md`, verified on a real tenant)

- Plain `I_FreightOrder*` views do not exist — read through the TP family (`I_FreightOrderTP`, `I_FreightOrderItemTP`,
  `I_FreightOrderStopTP`, `I_FreightOrderStageTP` — verified in `verified_external/LE-TM.md`; `I_FreightOrderBPTP`,
  `I_FreightOrderChargeTP` R) or the generic transportation-order views `I_TransportationOrder_2` (R),
  `I_TransportationOrderItem_2`, `I_TransportationOrderStop_2` (verified_external).
- The local catalog has **no** TP views at all (see its INDEX "Giới hạn phạm vi") — do not conclude "missing" from it.

## Write — RAP BOs (EML), all R

`I_FreightOrderTP` (+ `D_FreightOrderCreateP`, `D_FreightOrderCreateForDelivP`, `D_FreightOrderCreateForPickupP`),
`I_FreightBookingTP` (+ `D_FreightBookingCreateP`), `I_FreightUnitTP`, `I_FreightAgreementTP`,
`I_TransportationRateTableTP`; transportation-order actions `D_TranspOrdAssignFrtUnitP`, `D_TranspOrdReportEventP`,
`D_TranspOrdChgLocSequenceP` … Business events: `D_TranspOrd*StsChgd`.

## Extend

`/SCMTMS/ES_TRANSP_ORDER_EXTEND` (R) — the only TM spot.

## Also read

`verified_external/LE-TM.md`; catalog folder `TM/` (79) — master data / codes only. Key-user config: all **u**.
