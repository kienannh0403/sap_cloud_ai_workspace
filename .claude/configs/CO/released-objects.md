# CO — released objects

Legend: see `configs/FI/README.md`.

## 1. Read — CDS views

| Area | Views | Evidence |
|---|---|---|
| Cost centers | `I_CostCenter`, `I_CostCenterText`, `I_CostCenterActivityType` | C |
| Controlling area / objects | `I_ControllingArea`, `I_ControllingObject` | C |
| Internal orders | `I_InternalOrder` | C |
| Profit center | `I_ProfitCenter` | C |
| Actual / plan line items | `I_ActualPlanJournalEntryItem` | R |
| Product cost estimate | `I_ProductCostEstimate` | C |
| Statistical key figures | `I_StatisticalKeyFigure` | f |
| Profitability segment | `I_ProfitabilitySegment` | f |

Not usable despite annotations: `I_ActualCostRate`, `I_PlanCostRate` (not in catalog; see README trap).
`I_CostElement` / `I_ActivityType` not found in the catalog — check the repository before using.

## 2. Write — RAP BOs (EML)

| BO | Purpose | Evidence |
|---|---|---|
| `I_CostCenterTP_2` | Cost center master (+ `D_CostCtrCreateValidityPeriodP`, `D_CostCtrUpdateValidityPeriodP`) | R |
| `I_ActualCostRateTP`, `I_PlanCostRateTP`, `I_ServiceCostRateTP` | Cost rates | R |
| `I_DirectActivityAllocationTP_2` | Direct activity allocation | R |
| `I_CostAndRevenueReassignmentTP` | Reposting of costs / revenues | R |
| `I_StatisticalKeyFigureTP_2` | Statistical key figures | R |
| `I_ProductCostEstimateTP` | Product cost estimate (+ `D_CostEstGetBrkdwnByCompViewP/R`, `D_CostEstCostComponentR`) | R |
| `I_EventBasedOrderPostingRuleTP` | Event-based posting rules | R |

## 3. Extend — enhancement spots (all R)

| Spot | Area |
|---|---|
| `FIN_COST_CENTER` | Cost center master checks / derivation |
| `MDI_COSTCENTER_MAP` | Cost center replication mapping |
| `FCO_COST_RATE` | Cost rates |
| `FCO_EB_PSTRL_GNRT_DFLT_RULE` | Event-based posting rule defaults |
| `FIN_ACT_COST_SPLIT`, `FIN_ACT_CROSS_COMPANY` | Actual costing |
