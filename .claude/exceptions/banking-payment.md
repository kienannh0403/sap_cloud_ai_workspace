# Banking / Payment
<!-- tier: minimal -->
<!-- action: deny -->

Bank accounts, payment runs, card data — direct financial-credential exposure.

| Name | Description | Source |
|---|---|---|
| BNKA | Bank master | sc4sap |
| KNBK | Customer bank details | sc4sap |
| LFBK | Supplier bank details | sc4sap |
| BUT0BK | Business partner bank details | sc4sap |
| T012K | House bank accounts | sc4sap |
| REGUH / REGUP | Payment program results | sc4sap |
| PAYR | Payment medium / cheques | sc4sap |
| FPLTC | Billing plan — payment cards | sc4sap |
| BSEGC | FI document payment-card segment | sc4sap |
| FPAYH / FPAYHX / FPAYP / FPAYPX | Payment medium data | sc4sap |

## Released CDS views

| Name | Wraps | Source |
|---|---|---|
| I_BUSINESSPARTNERBANK | BUT0BK | local catalog |
| I_SUPLRBANKDETAILSBYINTID | LFBK | local catalog |
| I_HOUSEBANKACCOUNTLINKAGE | T012K | local catalog |
| I_PAYMENTCARD | card tokens | local catalog |
