# Protected Business Data (transactional)
<!-- tier: standard -->
<!-- action: warn -->

Transactional documents that combine partner PII with commercial values. At `standard` the hook does not
refuse — it asks the user to confirm each query (`permissionDecision: ask`). Keep such queries scoped
(one document / small key range) and select only the columns the question needs.

| Name | Description | Source |
|---|---|---|
| VBAK / VBAP / VBEP / VBPA | Sales document header / item / schedule / partner | sc4sap |
| VBRK / VBRP | Billing document | sc4sap |
| LIKP / LIPS | Delivery | added (SD scope) |
| EKKO / EKPO | Purchase order | sc4sap |
| BKPF / BSEG / ACDOCA | Accounting document / universal journal | sc4sap |
| CDHDR / CDPOS | Change documents | sc4sap |
| STXH / STXL | Long texts (free-text PII possible) | sc4sap |

## Released CDS views

| Name | Wraps | Source |
|---|---|---|
| I_SALESORDER / I_SALESORDERITEM / I_SALESORDERSCHEDULELINE | VBAK / VBAP / VBEP | local catalog |
| I_SALESCONTRACT | VBAK | local catalog |
| I_DELIVERYDOCUMENT | LIKP | local catalog |
| I_BILLINGDOCUMENT / I_BILLINGDOCUMENTITEM | VBRK / VBRP | Released (A), sap-docs 2026-09-23 |
| I_JOURNALENTRY / I_JOURNALENTRYITEM | BKPF / ACDOCA | local catalog |
| I_GLACCOUNTLINEITEM | ACDOCA | local catalog |
| I_OPERATIONALACCTGDOCITEM | BSEG | local catalog |
| I_PURCHASEORDERAPI01 / I_PURCHASEORDERITEMAPI01 | EKKO / EKPO | local catalog (added 2026-09-23 with MM; `I_PurchaseOrder` itself is not released) |
| I_SUPPLIERINVOICEAPI01 | RBKP | local catalog (added 2026-09-23 with MM) |
