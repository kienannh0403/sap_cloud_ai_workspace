# Pricing / Conditions / Rebates
<!-- tier: minimal -->
<!-- action: deny -->

Negotiated prices, discounts, rebates — top commercial risk. **SD impact:** the agent may not pull raw
pricing-element rows. Allowed instead: DDLS/metadata reads, `COUNT(*)` or aggregates without rate/amount columns,
or a screenshot from the Fiori app supplied by the user.

| Name | Description | Source |
|---|---|---|
| KONH / KONP / KONM / KONW | Condition records / scales | sc4sap |
| KONA | Rebate agreements | sc4sap |
| KONV | Document conditions (ECC) | sc4sap |
| PRCD_ELEMENTS / PRCD_ELEMENT | Document conditions (S/4) | sc4sap |
| PRCD_COND_HEAD / PRCD_COND | Condition records (S/4) | sc4sap |
| A### | Condition tables A001–A999 | sc4sap |

## Released CDS views

| Name | Wraps | Source |
|---|---|---|
| I_SLSPRCGCONDITIONRECORD | sales condition records | local catalog |
| I_PURGPRCGCONDITIONRECORD | purchasing condition records | local catalog |
| I_SALESDOCUMENTPRICINGELEMENT / I_SALESDOCITEMPRICINGELEMENT | sales document pricing | local catalog |
| I_SALESORDERPRICINGELEMENT / I_SALESORDERITEMPRICINGELEMENT | sales order pricing | local catalog |
| I_SALESQUOTATIONPRCGELMNT / I_SALESQUOTATIONITEMPRCGELMNT | quotation pricing | local catalog |
| I_SLSCONTRITEMPRICINGELEMENT | sales contract pricing | local catalog |
| I_CREDITMEMOREQPRCGELMNT / I_CREDITMEMOREQITEMPRCGELMNT | credit memo request pricing | local catalog |
| I_DEBITMEMOREQPRCGELMNT / I_DEBITMEMOREQITEMPRCGELMNT | debit memo request pricing | local catalog |
| I_PRELIMBILLINGDOCPRCGELMNT / I_PRELIMBILLGDOCITEMPRCGELMNT | preliminary billing pricing | local catalog |
| I_BILLINGDOCUMENTPRCGELMNT / I_BILLINGDOCUMENTITEMPRCGELMNT | billing pricing | Released (A), sap-docs 2026-09-23 |
| I_PURORDPRICINGELEMENTAPI01 / I_PURORDITMPRICINGELEMENTAPI01 | PO pricing | local catalog |
