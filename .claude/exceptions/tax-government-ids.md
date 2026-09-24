# Tax / Government IDs
<!-- tier: minimal -->
<!-- action: deny -->

VAT registration numbers, BP tax numbers (Vietnam: the customer / supplier tax code, MST).

| Name | Description | Source |
|---|---|---|
| BUT0TX | BP tax numbers | sc4sap |
| KNAS / LFAS | Customer / supplier VAT registration | sc4sap |
| DFKKBPTAXNUM | BP tax numbers (FI-CA) | sc4sap |

## Released CDS views

| Name | Wraps | Source |
|---|---|---|
| I_BUSINESSPARTNERTAXNUMBER | BUT0TX | local catalog |
| I_BUSPARTADDRDEPDNTTAXNMBR | address-dependent tax numbers | local catalog |
| I_CUSTSLSAREAADDRDEPDNTTAXINFO | sales-area tax info | local catalog |
