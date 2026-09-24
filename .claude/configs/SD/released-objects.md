# SD — released objects (read / write / extend)

Evidence legend: see [README.md](README.md). All "Released (A)" rows checked 2026-09-23, `system_type=public_cloud`.

## 1. Read — released CDS views (replaces sc4sap `tables.md`)

| Business object | View | Classic table | Evidence |
|---|---|---|---|
| Sales document (all categories) | `I_SalesDocument` / `I_SalesDocumentItem` | VBAK / VBAP | local catalog |
| Sales order | `I_SalesOrder` / `I_SalesOrderItem` / `I_SalesOrderScheduleLine` | VBAK / VBAP / VBEP | local catalog |
| Partners | `I_SalesDocumentPartner`, `I_SalesOrderPartner` | VBPA | local catalog |
| Quotation / inquiry / contract | `I_SalesQuotation`, `I_SalesInquiry`, `I_SalesContract` | VBAK | local catalog |
| Returns / credit / debit memo request | `I_CustomerReturn`, `I_CreditMemoRequest`, `I_DebitMemoRequest` | VBAK | local catalog |
| Outbound delivery | `I_OutboundDelivery`, `I_DeliveryDocument` / `I_DeliveryDocumentItem` | LIKP / LIPS | local catalog |
| Billing document | `I_BillingDocument` / `I_BillingDocumentItem` | VBRK / VBRP | Released (A); only in `_fields_only/` of the local catalog |
| Document flow | `I_SDDocumentMultiLevelProcFlow` | VBFA | local catalog |
| Status | `I_OverallSDProcessStatus` | VBUK texts | local catalog |
| Pricing elements | `I_SalesDocItemPricingElement`, `I_SalesOrderItemPricingElement` | PRCD_ELEMENTS | local catalog — **row reads denied by blocklist** |
| Org / master | `I_SalesOrganization`, `I_DistributionChannel`, `I_Division`, `I_SalesArea`, `I_SalesDocumentType`, `I_SDDocumentCategory`, `I_ShippingPoint`, `I_CustomerSalesArea` | TVKO, TVTW, TSPA, TVTA, TVAK, … | local catalog |

More: `artifacts/system_analysis/CDS_RELEASED_CATALOG/modules/{SD-SLS_Sales,SD-BIL_Billing,SD_other,LE}/views.csv`.

## 2. Write — released RAP business objects via EML (replaces sc4sap `bapi.md`)

Use `MODIFY ENTITIES OF <BO>` / `READ ENTITIES OF <BO>` from custom code (rule §3: EML or released API only).

| BO (BDEF) | Purpose | Evidence |
|---|---|---|
| `I_SalesOrderTP` | Sales order create / change | Released (A), SD-SLS-API-2CL |
| `I_SalesOrderWithoutChargeTP` | Free-of-charge order | Released (A) |
| `I_SalesQuotationTP` | Quotation | Released (A) |
| `I_SalesContractTP` | Contract | Released (A) |
| `I_SalesSchedulingAgreementTP` | Scheduling agreement | Released (A) |
| `I_CustomerReturnTP` | Returns order | Released (A) |
| `I_CreditMemoRequestTP` / `I_DebitMemoRequestTP` | Credit / debit memo request | Released (A) |
| `I_OutboundDeliveryTP` / `I_OutboundDeliveryTP_2` | Outbound delivery | Released (A), LE-SHP-API-2CL |
| `I_CustomerReturnsDeliveryTP` | Returns delivery | Released (A) |
| `I_BillingDocumentTP` | Billing document | Released (A), SD-BIL-BD-2CL |
| `I_BillingDocumentRequestTP` | Billing document request (external billing data) | Released (A) |

Also released: action-parameter BDEFs `D_SalesDocCreateWithRefDocP`, `D_SalesDocUpdatePricesP`,
`D_OutbDelivCrteDelivFrmSlsDocP`, `D_BillgDocCrteCanclnDocP`, … (full list: `sap_search_objects(object_type="BDEF",
app_component="SD-SLS" | "SD-BIL" | "LE-SHP")`). Read the BDEF on the tenant before coding against an action.

External callers (not ABAP): OData / SOAP APIs on SAP Business Accelerator Hub (e.g. Sales Order OData API) —
*unverified here*; the release repository above does not list them. Use `/sap-dev-api-inbound` / `-outbound`.

## 3. Extend — released enhancement spots and BAdIs (replaces sc4sap `enhancements.md`)

Implement in ADT (developer extensibility) or in "Custom Logic" app (key-user). Skill: `badi-enhancement`.

| Enhancement spot | Area | Evidence |
|---|---|---|
| `ES_SD_SLS_EXTEND` | Sales documents — main spot | Released (A) |
| `ES_SD_SLS_DEV_EXTEND` | Sales documents — developer extensibility | Released (A) |
| `ES_SD_SALESCONTRACT_EXTEND` | Contracts | Released (A) |
| `ES_EDI_SD_ORDER_EXTEND` | Inbound EDI sales orders | Released (A) |
| `ES_SD_BIL_EXTEND` | Billing | Released (A) |
| `ES_PF_BILLING_DT` | Billing (PF) | Released (A) |
| `ES_LE_SHP_EXTEND` | Deliveries — successor of on-prem `LE_SHP_DELIVERY_PROC` / `LE_SHP_GOODSMOVEMENT` (both *notToBeReleased*) | Released (A) |

BAdI interfaces seen (all Released (A)) — pick by what the requirement changes:

| Need | Sales (`IF_SD_SLS_*`) | Delivery (`IF_LE_SHP_*`) | Billing (`IF_SD_BIL_*`) |
|---|---|---|---|
| Check before save | `CHECK_BEFORE_SAVE`, `CHECK_HEAD`, `CHECK_ITEM`, `CHECK_DELETE_ITEM` | `DELIVERY_FIN_CHECK` | — |
| Change field values | `MODIFY_HEAD`, `MODIFY_ITEM`, `MODIFY_HEAD_BUSINESS`, `MODIFY_ITEM_BUSINESS`, `MODIFY_ITEM_REQDATE`, `MODIFY_*_TAX` | `MODIFY_HEAD`, `MODIFY_ITEM`, `MODIFY_POST_GM` | — |
| Field properties (hide / read-only) | `FIELDPROP_HEAD`, `FIELDPROP_ITEM`, `FIELDPROP_DELIVSCHED` | `FIELDPROP_HEAD`, `FIELDPROP_ITEM` | — |
| Copy control / data transfer | `COPY_RQMT_*`, `DATA_TRANSFER_HEAD/ITEM` | `SUPPRESS_DEL_SPLIT` | `DATA_TRANSFER` |
| Numbering / cancellation / print | — | — | `FLEX_NUMBERING`, `FLEX_CANCELLATION`, `PRINT_STANDARD_HEAD/ITEM` |

Which BAdI definition belongs to which interface, and its filter values: read the enhancement spot on the
tenant (`SAP(action="read", target="ENHS ES_SD_SLS_EXTEND")`) — *not captured here*.
