# Decision Ladder — reuse before build (Tier 4, FS → TS design)

Loaded by `/sap-dev-fs-analytic` and `/sap-dev-fs-analytic-transactional-app` in Phase 3.1, when each row of the
Coding Implementation Plan is decided. Idea adapted from ponytail (MIT, github.com/dietrichgebert/ponytail) for
ABAP Cloud: the cheapest object is the one never built — less code, fewer objects, fewer ATC / Clean Core risks.

## When it applies — and when it does NOT

- **Applies:** designing the TS (Phase 3 of the fs-analytic workflows). Every planned object or piece of logic climbs
  the ladder and stops at the FIRST rung that fully satisfies the requirement.
- **Does NOT apply during a build.** `/sap-dev-create-*` builds exactly what the TS says (Iron Law §6). A builder
  that thinks "this object isn't needed" stops and goes back to the TS — it never skips or merges rows itself.
- **Never silently drops an FS requirement.** Rungs 1-3 can remove scope from the FS; that is the user's decision:
  ask via [Skill: grill-me], record the answer in the target's `INDEX.md` (decisions beyond the spec), then continue.
- Rung 0 first: understand the full FS before climbing. Lazy about solutions, never about reading.

## The ladder

| Rung | Question | Where to check | Stop here when… |
|---|---|---|---|
| 1 | Is this requirement really needed? | the FS; ask the user | the user confirms it can go (record in INDEX.md) |
| 2 | Does a standard SAP app already do it? | [Skill: sap-fiori-apps-reference] | a standard app covers it — propose it to the user instead of building |
| 3 | Is key user extensibility enough? | [Skill: abap-cloud] (tier 1: Custom Fields, Custom Logic, Custom Analytical Query, Custom CDS View) | a key user tool covers it — propose it to the user |
| 4 | Does one of our Z objects already do it? | [Skill: z-object-catalog] | reuse it (e.g. `ZCL_EXPORT_EXCEL_XLSX`, `Z_API_FWK`) |
| 5 | Is there a released CDS view / API / class? | `artifacts/system_analysis/CDS_RELEASED_CATALOG/` (CDS by module) and `artifacts/system_analysis/SAP_RELEASE_WATCH/released_objects/objects.csv` (every type: CLAS, INTF, BDEF, BAdI, function module…), [Skill: find-released-cds-view], [Skill: released-abap-classes] | consume the released object instead of rebuilding it — if what you need is NOT released, take the sub-ladder below |
| 6 | Can the framework do it declaratively? | [Skill: cds-analytical-views], [Skill: rap] | annotation / association / CDS expression / managed RAP feature covers it — no ABAP |
| 7 | Can an existing Z object be extended? | [Skill: z-object-catalog] + ripple check on its dependents | adding a field/association to an existing Z CDS/class beats a near-duplicate new one |
| 8 | Only then: build new, minimal | the TS | nothing above fits — build exactly what the requirement needs |

### Sub-ladder for a calculated field

CDS expression (CASE, cast, built-in function) → association to a released view (+ `@ObjectModel.text`) →
virtual element ([Skill: cds-virtual-element]) → custom entity + query provider ([Skill: rap-query-provider]).
Take the first that can express the rule.

### Sub-ladder when the object you need is not released

Rung 5 found the right object but its state is `notToBeReleased`, `deprecated` without a usable successor, or it is
missing from the index. Public Cloud is strict released-only. Climb in this order and stop at the first that fits
(adapted from StormShynn/sap-abap-agent `missing-released-api-mitigation.md`, MIT; SAP sources: SAP-samples
abap-platform-rap640 "Mitigating Missing Released APIs"):

| Step | Question | Where to check | Typical case |
|---|---|---|---|
| a | Is there a released alternative returning the same data? | the same index (search by area: `app_component` column); `deprecated` rows name their `successors` | `I_Material` → `I_Product`; `I_PurchaseOrder` → `I_PurchaseOrderAPI01` |
| b | Is there a standard OData / SOAP API for it (Communication Scenario)? | api.sap.com filtered on "SAP S/4HANA Cloud Public Edition"; call it over HTTP with a Communication Arrangement ([Skill: odata], [Skill: btp-abap-environment]) | the released BO cannot do it from ABAP — e.g. the document number is needed at once but the BDEF uses **late numbering** (only `%pid` in the handler, no `COMMIT ENTITIES` inside a behavior) |
| c | Is a field or a small rule on a standard object enough? | key user Custom Fields / Custom Logic, or a released BAdI (`objects.csv` rows of type `ENHS`, [Skill: badi-enhancement]) | adding a field or a check to a standard document |
| d | None of the above | — | record `[Unverified]` + an open question in the target's `INDEX.md` and ask the user / customer. Stop. |

Never, at any step: invent a "close enough" released name to make it compile; use an on-premise object because it is
familiar (`BAPI_*`, raw tables like `T156` — ATC rejects them); build a Tier-2 wrapper (exists only in Private Cloud /
on-premise); read or write a standard table directly. A TS row that took this sub-ladder writes its step in the
Ladder column, e.g. `5b — API_MATERIAL_DOCUMENT_SRV, BDEF I_MaterialDocumentTP uses late numbering` (the source
project's real case; `I_MaterialDocumentTP` is a released BDEF — check its numbering in the BDEF itself before
relying on this on our tenant).

A row that **creates or changes a standard SAP document** (any rung) also follows
`.claude/common/document-creation-pattern.md`: interface order, error reading, commit point, document number,
idempotency key and log — the TS row names each of them.

## Never cut to climb higher

The ladder removes what is unnecessary, never what is mandatory:
- authorization: DCL, AUTHORITY-CHECK, IAM app;
- validation at trust boundaries: inbound API payloads, RAP actions/validations;
- error handling and messages (TRY-CATCH, `failed` / `reported`);
- architecturally required RAP objects: BDEF, projection, service definition / binding;
- ATC and Clean Core requirements.

## How it is recorded in the TS

Every row of the Coding Implementation Plan carries a **Ladder** column: the rung taken and its evidence, e.g.
- `5 — I_BillingDocumentItem, CDS_RELEASED_CATALOG/modules/<folder>/…`
- `4 — reuse ZCL_EXPORT_EXCEL_XLSX (Z_OBJECT_CATALOG)`
- `6 — @ObjectModel.text via association _Customer`
- `8 — no released view gives <grain>; Z_OBJECT_CATALOG searched for <terms>: none`

A rung-8 row must say why rungs 4-7 did not fit (what was searched, what was missing). Architecturally required
objects (Step 2-7 RAP objects that exist only because a rung-5/6/8 object needs them) write `8 — required by #<row>`.
