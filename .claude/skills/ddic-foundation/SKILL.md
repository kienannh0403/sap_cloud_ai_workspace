---
name: ddic-foundation
description: Create the ABAP Cloud DDIC foundation layer for a brand-new transactional app — Domain, Data Element, Structure, database Table (persist + draft), Number Range, Message Class — using source-code syntax (`define domain`, `define data element`, `define table`, `define table entity`). Use when a TS's Coding Implementation Plan has DDIC rows to build before the RAP tree, or when asked for ABAP Cloud dictionary syntax. Triggers include "tạo domain mới", "tạo data element", "tạo bảng DB ABAP Cloud", "DDIC ABAP Cloud", "define table syntax", "define domain", "bảng draft cho RAP", "admin field cho table", "DDIC foundation", "CDS table entity". For the RAP layer on top (BDEF, behavior pool, draft behavior) use rap; for CDS view modeling use cds-view-entities.
---

# DDIC Foundation — ABAP Cloud Dictionary Objects

The persistence layer beneath a RAP business object. This skill owns the DDIC objects themselves; [Skill: rap] owns everything from the BDEF upward.

Full syntax templates, the complete built-in type table, and the classic-vs-CDS table comparison live in [references/ddic-syntax.md](references/ddic-syntax.md) — read it when writing the source. This body holds the decisions and the rules that are easy to get wrong.

Build order is fixed by dependency: **Domain → Data Element → Structure → Number Range → Message Class → Table (persist) → Table (draft)**.

## Step 0 — Reuse before you create (mandatory)

Do not mint a new Domain/Data Element/Table until you have checked for something reusable. `sap-dev-rule.md` §2 requires a global name check before creating; this is the concrete form of it.

1. **SAP released Data Elements first.** If a field is a standard business key or quantity, use the released data element (`MATNR`, `KUNNR`, …) rather than a Z clone. Confirm it via MCP, do not assume the name.
2. **Then existing Z/Y objects in the target package.** Search the package and **read the actual source/structure** of what you find — never infer intent from the name. Two differently-named domains that both encode "Active/Inactive" is a real and common duplication.
3. **Only then create new.** If the package is empty or has no comparable object, say so and fall back to the [Skill: naming-convention] defaults — do not invent a "house convention" from zero samples.

> Why this step is not optional: a previous scaffold on this kind of task fabricated the admin data element name `AB_CREATED_BY` instead of the real `ABP_CREATION_USER`, and used the on-premise XML (DD01V) paradigm instead of ABAP Cloud's source-code `define domain` — both because it reasoned from general knowledge instead of checking. The table below exists to stop the first half of that; this step stops the rest.

## SAP-released admin data elements — use these exact names

Never hand-type an approximation of these. They are what RAP's managed runtime and draft framework expect.

| Data element | Type | Purpose |
|---|---|---|
| `sysuuid_x16` | `raw(16)` | UUID key for a RAP managed BO |
| `abp_creation_user` | `char(12)` | Created by |
| `abp_creation_tstmpl` | `utclong` | Created at (UTC) |
| `abp_locinst_lastchange_user` | `char(12)` | Last changed by (local instance) |
| `abp_locinst_lastchange_tstmpl` | `utclong` | Last changed at (local instance) |
| `abp_lastchange_tstmpl` | `utclong` | Last changed at (total ETag) |

The two `lastchange` timestamps are not interchangeable: the `locinst_` one is the local ETag for optimistic locking on that instance, `abp_lastchange_tstmpl` is the total ETag covering the composition tree. Take whichever the TS specifies; if the TS is silent, ask rather than pick.

These are `utclong` — see the overflow trap in [Skill: cds-virtual-element] before doing arithmetic on them anywhere.

## Do you actually need a Domain?

| Need | Object | Rule |
|---|---|---|
| A reusable value range (enum) shared by ≥2 data elements | **Domain** + Data Element | This is the only case that justifies a Domain |
| A semantic label + type for one or two fields | **Data Element** on a built-in type | Skip the Domain; `abap.char( 1 )` etc. is enough |
| Persistence for a RAP managed BO | **Table** (classic `define table` or CDS `define table entity`) | See the comparison in the reference |
| A flat parameter/mapper record, no persistence | **Structure** | Not a table — different length limit, see [Skill: naming-convention] |

## Rules that fail activation or ATC if broken

1. **`@DataClassification.level` is mandatory on every Data Element** in ABAP Cloud. Missing it is an ATC error. Values: `#BUSINESS_INFORMATION` · `#CRITICAL` · `#PERSONAL` · `#NONE`. Pick `#PERSONAL` for anything identifying a person and `#CRITICAL` for credentials/financially sensitive values — this is a data-protection classification, not decoration.
2. **`key client : abap.clnt not null` is always the first key** of a classic `define table`. Never `MANDT`.
3. **`not null` belongs on key fields only.** Non-key fields must not carry it.
4. **`@AbapCatalog.tableCategory : #TRANSPARENT`** is the only table category available on ABAP Cloud.
5. **`abap.dec( total, decimals )` — `total` includes the decimal places.** `abap.dec( 16, 2 )` is 14 integer digits + 2 decimals, not 16 + 2.
6. **Name lengths bite here.** A database table name is capped at **16 characters including prefix** — roughly half the 30 that classes, CDS views, data elements and structures get. `ZA_ProductionOrder` (18) does not fit; `ZA_ProdOrder` does. Check [Skill: naming-convention] "Giới hạn độ dài" **before** proposing a table name: renaming a table after the CDS/BDEF/service tree is built on it means reworking the whole chain. Note the trap that a DDIC **structure** is also object type `TABL` but gets 30, not 16.

## Draft table

A draft-enabled RAP BO needs one draft table per entity, mirroring the persist table's fields plus the draft-admin include:

```abap
  "%admin" : include sych_bdl_draft_admin_inc;
```

Mirror means the same fields, same types — but the draft table's key is not `not null`-constrained the way the persist key is, and the draft table carries no `client` semantics of its own beyond the mirrored field. Get the exact shape from [references/ddic-syntax.md](references/ddic-syntax.md). The `with draft;` BDEF header and the implicitly-provided draft actions are [Skill: rap]'s territory.

## Naming

All prefixes come from [Skill: naming-convention] (FPT standard: `DO_` domain, `DE_` data element, `ST_` structure, `TT_` table type, `NR_` number range, `MC_` message class, `ZA_`/`ZD_` persist/draft tables). An explicit name in the TS or from the user always wins over the default. Do not use prefixes from other conventions (`ZDOM_`/`ZDE_`/`ZTB_`) — they are not this project's standard.

## After each object

DDIC metadata objects have no abaplint target, so there is no lint gate for them — go straight from create to activate. Then run [Skill: activation-guard]'s 3 gates **per object**, not once at the end of Step 0: this layer sits at the bottom of the longest dependency chain in the workspace (DDIC → CDS → BDEF → behavior pool → projection → service), which is exactly where one quietly-broken object cascades upward.

## References

- [references/ddic-syntax.md](references/ddic-syntax.md) — full `define domain` / `define data element` / `define table` / `define table entity` templates, built-in type table, classic-vs-CDS comparison
- [Skill: rap] — BDEF, behavior pool, draft behavior, save sequence
- [Skill: cds-view-entities] — the CDS layer above these tables
- [Skill: naming-convention] — prefixes and length limits
