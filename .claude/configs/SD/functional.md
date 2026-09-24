# SD — configuration, apps, workflow (key-user side)

**Everything in this file is *unverified*** — general S/4HANA Cloud Public Edition knowledge, not checked against
the release repository (these are not ABAP objects) nor against the tenant. It exists so a consultant knows
*where* things live; it is not a source for IDs. Never put an SSCUI ID or Fiori app ID in a TS from memory —
ask the functional owner or look it up in the tenant / SAP Fiori apps reference library
(skill `sap-fiori-apps-reference`).

## Configuration (replaces SPRO / sc4sap `spro.md`)

- Customizing is done in **"Manage Your Solution" → Configure Your Solution**, as self-service configuration UIs
  (SSCUI), by the key user / functional consultant — not by the developer, and never via code.
- Typical SD areas: sales document types, item categories, schedule line categories, copy control, pricing
  procedures and condition types, output determination (Output Management), credit management, partner
  determination. Business process detail: skills `sap-process-o2c-*`.
- Developer consequence: a TS must name the config it depends on as an **assumption to confirm**, and the code
  reads configuration values through released CDS views (e.g. `I_SalesDocumentType`), never hard-codes them.

## Apps (replaces tcodes / sc4sap `tcodes.md`)

- Classic tcodes (VA01/VA02/VA03, VL01N, VF01…) are replaced by Fiori apps (Manage Sales Orders, Manage Outbound
  Deliveries, Create Billing Documents, …). Some SAP GUI-for-HTML transactions remain as Fiori tiles — check
  the tenant's app finder.
- Custom UIs are Fiori Elements apps on RAP (workflows `/sap-dev-create-report`, `/sap-dev-create-transactional-app`).

## Workflow (replaces SAP Business Workflow / sc4sap `workflows.md`)

- Approvals for sales documents use **flexible workflow** (preconditions + steps configured by the key user in
  the "Manage Workflows …" apps). Custom preconditions/agent determination go through released BAdIs of the
  workflow scenario — check with `sap_search_objects` before promising one.
- Real-world example (community, not verified here): sales order approval for high manual discounts —
  https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-members/sales-order-approval-for-high-manual-discounts-using-flexible-workflow-in/ba-p/14474085

## Country (vn)

No Vietnam-specific SD content captured (e-invoice, tax code handling). `SAP_COUNTRY=vn` is set in
`system-config.md`, but there is no `country/vn.md` yet — ask before assuming any localization rule.
