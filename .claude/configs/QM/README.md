# QM — Quality Management (Public Cloud)

Sub-areas: inspection lots and results (QM-IM), inspection planning (QM-PT), quality notifications, defects and tasks
(QM-QN), certificates (QM-CA), quality levels (QM-QC).
Replaces sc4sap `configs/QM/` (QA01/QA32/QM01, QALS/QAVE/QMEL, BAPI_INSPLOT_*, `NOTIF_EVENT_POST`).

Legend **R / C / f / u**: see `configs/FI/README.md`.

## Traps

- The notification view is **`I_QltyNotification`** (C), not `I_QualityNotification` (not found) — see
  `verified_external/QM.md`.
- `NOTIF_EVENT_POST` (classic) is *notToBeReleased* → `QQM_NOTIF_EVENT_POST_CLD` (R).

## Read — CDS views

| Views | Evidence |
|---|---|
| `I_InspectionLot`, `I_InspectionCharacteristic`, `I_InspectionResult`, `I_InspLotUsageDecision` | C |
| `I_QltyNotification`, `I_Defect`, `I_InspectionPlan` | C |

## Write — RAP BOs (EML), all R

`I_InspectionLotTP_2` (+ `D_InspLotRecordUsageDecisionP`), `I_InspectionPlanTP_2`, `I_QltyNotificationTP`,
`I_DefectTP_2`, `I_QualityTaskTP_2`, `I_QltyProcmtCertTP_2`, `I_QualityInProcurementTP_2`, `I_QualityLevelTP_2`.

## Extend — enhancement spots, all R

`QAAT_INSPLOT_CRT_CHECK`, `QPL1_INSPLOT_CHANGE` (inspection lot) · `QASDR_PLAN_TO_INSPECTION_CLD` (sampling) ·
`QQM_NOTIF_DEFAULT_VAL_CLD`, `QQM_NOTIF_EVENT_SAVE_CLD`, `QQM_NOTIF_EVENT_POST_CLD`, `QQM_NOTIF_ACTIONBOX_FOA_CLD`
(notification) · `QM_FOLLOW_UP` (tasks) · `QM_QUALITY_CERTIFICATE_OUT`, `QC_CERT_FUNC_MODULE` (certificates) ·
`ARC_QM_DEFECT` (archiving).

## Also read

`verified_external/QM.md`; catalog folder `QM/` (173). Key-user config / apps: all **u** (SSCUIs, "Manage Inspection
Lots", "Record Inspection Results", …).
