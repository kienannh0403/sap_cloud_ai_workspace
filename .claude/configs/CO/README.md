# CO — Controlling (Public Cloud)

Sub-areas: CO-OM (cost centers, internal orders, activity types, cost rates), CO-PC (product costing, actual costing),
margin analysis (on-prem CO-PA; in Public Cloud it lives in the universal journal).
Replaces sc4sap `configs/CO/` (KS01, KP06, CK11N, COEP/COSP tables, BAPI_COSTCENTER_*).

Legend **R / C / f / u**: see `configs/FI/README.md`. Files: [released-objects.md](released-objects.md).

## Key-user side (all **u**)

- Cost element = G/L account of type "secondary/primary cost" (no separate KA01 master in S/4) — read via G/L views.
- Planning is done in SAP Analytics Cloud or plan-data apps; do not assume on-prem KP06 tables.
- Configuration via SSCUIs (controlling area is predefined in Public Cloud).

## Traps (from `verified_external/CO.md`, verified on a real tenant)

- `I_ActualCostRate` and `I_AccountingCostRate_2` carry `#PUBLIC_LOCAL_API` but are **not** usable in ABAP Cloud
  ("use not permitted"). Only the release repository / ADT view browser proves release. Write via `I_ActualCostRateTP` (R).

## Also read

- `artifacts/system_analysis/CDS_RELEASED_CATALOG/verified_external/CO.md`.
- Catalog folders `CO-OM_Cost-Center-Accounting/` (5), `CO_other/` (34); much of CO reads through FI views (`FIN/`).
- Skill `sap-process-finance-financial-close`.
