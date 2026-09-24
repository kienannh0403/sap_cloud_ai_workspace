# Customer-specific (Z/Y) sensitive tables
<!-- tier: minimal -->
<!-- action: warn -->

Z/Y tables or views that hold PII or prices. Add each concrete name here when it is created — decide at DDIC
design time (skill `ddic-foundation`). Only concrete names or narrow prefixes; never a bare `Z*`.

| Name | Description | Source |
|---|---|---|
| ZHR_* / ZPA_* | Typical HR extensions | sc4sap |
| ZCUST_* / ZKNA_* | Customer-master extensions | sc4sap |
| ZLFA_* / ZVEND_* | Supplier-master extensions | sc4sap |
