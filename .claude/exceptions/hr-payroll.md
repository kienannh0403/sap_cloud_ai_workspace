# HR / Payroll / Personnel
<!-- tier: minimal -->
<!-- action: deny -->

Highest-sensitivity category. Public Cloud does not expose HCM infotype tables to ABAP Cloud, but a SQL string
naming them is still refused.

| Name | Description | Source |
|---|---|---|
| PA0* / PA2* / PA4* / PA9* | HR infotypes (PA0002 personal data, PA0008 basic pay, PA0009 bank …) | sc4sap |
| HRP1* / HRP9* | OM / PD infotypes | sc4sap |
| PCL1 / PCL2 / PCL3 / PCL4 / PCL5 | HR clusters (PCL2 = payroll results) | sc4sap |

## Released CDS views

| Name | Wraps | Source |
|---|---|---|
| I_WORKFORCEPERSON_1 | workforce person | local catalog |
| I_PERSONWORKAGREEMENT_1 | work agreement | local catalog |
| I_PERSONWORKAGRMTPLNDWRKGTIME | planned working time | local catalog |
| I_EMPLOYEEWAGEGROUP | wage group | local catalog |
