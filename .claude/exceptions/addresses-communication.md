# Addresses / Communication
<!-- tier: minimal -->
<!-- action: deny -->

Central address management — street, phone, fax, e-mail, URLs.

| Name | Description | Source |
|---|---|---|
| ADRC | Address | sc4sap |
| ADRP | Person | sc4sap |
| ADR2 / ADR3 / ADR6 / ADR12 | Phone / fax / e-mail / URL | sc4sap |
| ADRCT / ADRT | Address / communication notes | sc4sap |

## Released CDS views

| Name | Wraps | Source |
|---|---|---|
| I_BUSPARTADDRESS | BUT020 + ADRC | local catalog |
| I_ORGANIZATIONADDRESS | ADRC | local catalog |
| I_PERSONADDRESS | ADRC / ADRP | local catalog |
| I_PERSONWORKPLACEADDRESS | ADRC / ADRP | local catalog |
| I_WORKPLACEADDRESS | ADRC | local catalog |
| I_WORKFORCEPERSONADDRESS | workforce address | local catalog |
