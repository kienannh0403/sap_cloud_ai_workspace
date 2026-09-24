# PS — Projects (Public Cloud: Enterprise Projects, PPM-SCL)

In Public Cloud, classic PS (CJ20N, PROJ/PRPS, BAPI_PROJECT_*) is replaced by **Enterprise Projects** — application
component PPM-SCL (the release repository has **0** objects under `PS`). Customer projects (billing) also live here.

Legend **R / C / f / u**: see `configs/FI/README.md`.

## Traps

- `I_Project`, `I_WBSElement`, `I_WBSElementBasicData` are **not** released (repository: not found). Read projects via
  `I_EnterpriseProject` / `I_EnterpriseProjectElement` (C). For finance reporting by WBS: `I_FinWBSElementHierarchy*`,
  `I_ProfitCenterToWBSElement` (R, FI-GL components).

## Read — CDS views

| Views | Evidence |
|---|---|
| `I_EnterpriseProject`, `I_EnterpriseProjectElement`, `I_ProjectDemand`, `I_ProjectBillingRequest` | C |
| `I_FinWBSElementHierarchy`, `I_FinWBSElementHierarchyNode`, `I_ProfitCenterToWBSElement` | R |

## Write — RAP BOs (EML), all R

`I_EnterpriseProjectTP_3` (+ `D_EntProjCopyToActiveDocumentP`), `I_ProjectDemandTP_2`, `I_ProjectBillingRequestTP_2`
(+ `D_PrjBlgReqCrteBillgDocReqP`). Business events: `D_EnterpriseProjectChanged_2`, `D_EntProjEntProjElmntChgd_2`.

## Extend

Only `ES_PROJECT_BILLINGELEMENT` (R, project billing). Otherwise key-user custom fields / logic.

## Also read

Skills `sap-process-projectsystem-customer-project`, `-internal-project`, `-resource-mgmt`; catalog folder
`PS_Project-System/` (95, PPM-SCL). Key-user config / apps: all **u** (project profiles, "Plan Customer Projects",
"Project Control").
