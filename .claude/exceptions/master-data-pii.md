# Customer / Supplier / Business Partner master PII
<!-- tier: minimal -->
<!-- action: deny -->

Names, addresses, tax IDs, national IDs, relationships of business partners.

| Name | Description | Source |
|---|---|---|
| KNA1 / KNB1 / KNVV / KNVK | Customer master | sc4sap |
| LFA1 / LFB1 / LFM1 / LFM2 | Supplier master | sc4sap |
| BUT000 | Business partner — general | sc4sap |
| BUT020 / BUT021 | BP addresses / usages | sc4sap |
| BUT050 / BUT051 | BP relationships / contact persons | sc4sap |
| BUT0ID | BP identification numbers | sc4sap |

## Released CDS views

| Name | Wraps | Source |
|---|---|---|
| I_CUSTOMER | KNA1 | local catalog |
| I_CUSTOMERCOMPANY | KNB1 | local catalog |
| I_CUSTOMERSALESAREA | KNVV | local catalog |
| I_SUPPLIER | LFA1 | local catalog |
| I_SUPPLIERCOMPANY | LFB1 | local catalog |
| I_SUPPLIERPURCHASINGORG | LFM1 | local catalog |
| I_BUSINESSPARTNER | BUT000 | local catalog |
| I_BUPAIDENTIFICATION | BUT0ID | local catalog |
| I_CONTACTPERSON | BUT051 | local catalog |

> SD reports usually need only the customer number and name. A report's CDS model may still *join* these views —
> the blocklist governs raw row extraction by the agent (SQL / data preview), not what the app itself reads.
