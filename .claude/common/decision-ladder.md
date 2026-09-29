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
| 5 | Is there a released CDS view / API / class? | `artifacts/system_analysis/CDS_RELEASED_CATALOG/`, [Skill: find-released-cds-view], [Skill: released-abap-classes] | consume the released object instead of rebuilding it |
| 6 | Can the framework do it declaratively? | [Skill: cds-analytical-views], [Skill: rap] | annotation / association / CDS expression / managed RAP feature covers it — no ABAP |
| 7 | Can an existing Z object be extended? | [Skill: z-object-catalog] + ripple check on its dependents | adding a field/association to an existing Z CDS/class beats a near-duplicate new one |
| 8 | Only then: build new, minimal | the TS | nothing above fits — build exactly what the requirement needs |

### Sub-ladder for a calculated field

CDS expression (CASE, cast, built-in function) → association to a released view (+ `@ObjectModel.text`) →
virtual element ([Skill: cds-virtual-element]) → custom entity + query provider ([Skill: rap-query-provider]).
Take the first that can express the rule.

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
