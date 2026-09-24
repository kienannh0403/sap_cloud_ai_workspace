# Authentication / Authorization / Security
<!-- tier: minimal -->
<!-- action: deny -->

Logon data, password hashes, role assignments, destinations with credentials, key material.

| Name | Description | Source |
|---|---|---|
| USR01 / USR02 / USH02 / USR21 | User master / logon / password history | sc4sap |
| AGR_1251 / AGR_USERS | Role authorizations / assignments | sc4sap |
| RFCDES | Destinations (embedded credentials) | sc4sap |
| RSECACTB / RSECTAB / SSF_PSE_D | Secure store / PSE key material | sc4sap |

## Released CDS views

| Name | Wraps | Source |
|---|---|---|
| I_USER | USR21 | local catalog |
| I_IAMBUSINESSUSERLOGONDETAILS | logon data | local catalog |
| I_IAMBUSINESSUSERBUSINESSROLE | role assignment | local catalog |
