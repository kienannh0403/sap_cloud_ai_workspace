# DDIC Foundation — Source Syntax Reference

Templates for ABAP Cloud dictionary objects. Read this when writing the source; the decisions and mandatory rules are in the parent [SKILL.md](../SKILL.md).

ABAP Cloud defines dictionary objects as **source code**, not as the XML structures (DD01V/DD04V/DD02V) that on-premise ADT and abapGit serialize. If you find yourself producing DD*V XML, you are on the wrong paradigm.

---

## Domain

```abap
@EndUserText.label : 'Order Status'
define domain ZDO_<Name> {
  type abap.char( 1 );
  value range:
    'O' : 'Open',
    'C' : 'Closed',
    'A' : 'Approved';
}
```

Only create one when the value range is shared by two or more data elements. A single-use enum is cheaper as a data element on a built-in type plus a value help.

### Built-in types

| Type | Meaning | Example |
|---|---|---|
| `abap.char( n )` | Character string | `abap.char( 40 )` |
| `abap.numc( n )` | Numeric text (keeps leading zeros) | `abap.numc( 10 )` |
| `abap.int1` / `abap.int2` / `abap.int4` / `abap.int8` | Integers | `abap.int4` |
| `abap.dec( total, dec )` | Packed decimal — `total` **includes** `dec` | `abap.dec( 16, 2 )` = 14 int + 2 dec |
| `abap.quan( total, dec )` | Quantity (needs a `abap.unit` companion field) | `abap.quan( 13, 3 )` |
| `abap.curr( total, dec )` | Currency amount (needs a `abap.cuky` companion field) | `abap.curr( 23, 2 )` |
| `abap.unit( n )` | Unit of measure key | `abap.unit( 3 )` |
| `abap.cuky` | Currency key | `abap.cuky` |
| `abap.dats` | Date `YYYYMMDD` | `abap.dats` |
| `abap.tims` | Time `HHMMSS` | `abap.tims` |
| `abap.utclong` | UTC timestamp (long) | `abap.utclong` |
| `abap.string` | Variable-length text | `abap.string` |
| `abap.xstring` | Variable-length binary | `abap.xstring` |
| `abap.raw( n )` | Fixed binary | `abap.raw( 16 )` |
| `abap.clnt` | Client | `abap.clnt` |
| `abap.lang` | Language key | `abap.lang` |

A quantity or amount field is meaningless without its unit/currency companion field in the same table — always add both.

---

## Data Element

Without a domain (preferred for single-use fields):

```abap
@EndUserText.label : 'Supplier Name'
@DataClassification.level : #BUSINESS_INFORMATION
define data element ZDE_<Name> {
  type abap.char( 80 );
}
```

With a domain:

```abap
@EndUserText.label : 'Order Status'
@DataClassification.level : #BUSINESS_INFORMATION
define data element ZDE_<Name> {
  type ZDO_<Name>;
}
```

| Annotation | Required? | Values |
|---|---|---|
| `@EndUserText.label` | Yes | The field label users see |
| `@DataClassification.level` | **Yes on ABAP Cloud** — missing is an ATC error | `#BUSINESS_INFORMATION` · `#CRITICAL` · `#PERSONAL` · `#NONE` |
| `@AbapCatalog.enhancement.category` | Optional | `#EXTENSIBLE_ANY` · `#NOT_EXTENSIBLE` |

---

## Database Table — classic `define table`

```abap
@EndUserText.label : 'Purchase Request Header'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #RESTRICTED
define table za_<name> {
  key client          : abap.clnt not null;
  key uuid            : sysuuid_x16 not null;
  request_id          : zde_<name>;
  description         : abap.char( 100 );
  amount              : abap.curr( 23, 2 );
  currency            : abap.cuky;
  quantity            : abap.quan( 13, 3 );
  unit                : abap.unit( 3 );
  created_by          : abp_creation_user;
  created_at          : abp_creation_tstmpl;
  last_changed_by     : abp_locinst_lastchange_user;
  last_changed_at     : abp_locinst_lastchange_tstmpl;
  local_last_changed_at : abp_locinst_lastchange_tstmpl;
}
```

| Annotation | Typical value | Notes |
|---|---|---|
| `@EndUserText.label` | string | Required |
| `@AbapCatalog.tableCategory` | `#TRANSPARENT` | Only category available on ABAP Cloud |
| `@AbapCatalog.deliveryClass` | `#A` | `#A` application data · `#C` customizing · `#L` temporary |
| `@AbapCatalog.dataMaintenance` | `#RESTRICTED` | `#RESTRICTED` recommended over `#ALLOWED` |
| `@AbapCatalog.enhancement.category` | `#NOT_EXTENSIBLE` | Set deliberately; `#EXTENSIBLE_ANY` if the TS calls for extension fields |
| `@AbapCatalog.buffering` | `#OFF` | Leave off unless the TS justifies buffering |

Rules: `client` first and `not null`; `not null` on key fields only; never `MANDT`.

**Child tables in a composition tree** carry the parent's UUID as a plain (non-key) field plus their own UUID key — the foreign-key shape comes from the TS's §3.1, not from a default.

---

## Database Table — CDS `define table entity`

Verified against SAP Help Portal, *Generating CDS Table Entities* (SAP BTP ABAP environment, version Cloud):

```abap
@EndUserText.label: 'My Table Entity'
@ClientHandling.type: #CLIENT_INDEPENDENT
@AbapCatalog.deliveryClass: #LOCAL_DATA
define table entity ZMY_CDS_TABLE_ENTITY
{
  key key_field : abap.int1;
  data_field : abap.int1 null;
}
```

Differences from classic `define table` that matter:

- Syntax is `define table entity <NAME> { … }`. There is **no** `as select from`. (A source claiming `define root view entity … as select from root table` is wrong — that is view-entity syntax, not table-entity syntax.)
- Client handling is declared by the **`@ClientHandling.type` annotation**, not by an explicit `key client : abap.clnt` field.
- Non-key fields take an explicit **`null`** suffix.
- `@AbapCatalog.deliveryClass` is used here too; the verified example shows `#LOCAL_DATA`.

`[unverified]` The exact annotation value for a client-dependent table entity (presumably `#CLIENT_DEPENDENT`) and the full annotation set for a draft-capable table entity were not confirmed — the verified SAP example only covers the client-independent case. Confirm in ADT before using, or use classic `define table`, which is fully covered above.

**Which to use**: classic `define table` is the safe default for this workspace — the workflows, the admin-field table, and the draft include are all expressed against it. Reach for `define table entity` only when the TS explicitly calls for it.

---

## Draft table

One draft table per draft-enabled entity. Same field list as the persist table, plus the draft-admin include:

```abap
@EndUserText.label : 'Purchase Request Header - Draft'
@AbapCatalog.enhancement.category : #NOT_EXTENSIBLE
@AbapCatalog.tableCategory : #TRANSPARENT
@AbapCatalog.deliveryClass : #A
@AbapCatalog.dataMaintenance : #RESTRICTED
define table zd_<name> {
  key client          : abap.clnt not null;
  key uuid            : sysuuid_x16 not null;
  request_id          : zde_<name>;
  description         : abap.char( 100 );
  amount              : abap.curr( 23, 2 );
  currency            : abap.cuky;
  quantity            : abap.quan( 13, 3 );
  unit                : abap.unit( 3 );
  created_by          : abp_creation_user;
  created_at          : abp_creation_tstmpl;
  last_changed_by     : abp_locinst_lastchange_user;
  last_changed_at     : abp_locinst_lastchange_tstmpl;
  "%admin"            : include sych_bdl_draft_admin_inc;
}
```

The `"%admin"` include is what makes it a draft table — the BDEF's `draft table zd_<name>;` clause will not activate without it. Everything above the table (`with draft;`, the draft actions, `%is_draft`/`%tky`) belongs to [Skill: rap].

---

## Number Range Object and Message Class

`[unverified]` These two are not DDL-source objects and no verified source template was available when writing this reference.

- **Number Range Object** — needed only when the TS specifies number-range-based numbering rather than BDEF-managed `numbering : managed`. Create via ADT / the MCP object-creation path and read back the created object to confirm its shape; do not hand-write a source file from guesswork.
- **Message Class** — create with the exact message numbers and texts the TS's §5/§10 requires. Verify the created messages by reading them back, since the behavior pool will reference them by number.

For both: create, activate, read back, then run [Skill: activation-guard]. If the TS does not specify one of them, it is not in scope — per `sap-dev-rule.md` §6 do not invent it.
