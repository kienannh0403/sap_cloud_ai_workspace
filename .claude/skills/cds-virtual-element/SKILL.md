---
name: cds-virtual-element
description: Implement CDS virtual elements (calculated fields computed at read time, not stored in the database) via `@ObjectModel.virtualElementCalculatedBy` and an ABAP exit class implementing `IF_SADL_EXIT_CALC_ELEMENT_READ`. Use when a TS or FS analysis has decided a field must be computed in ABAP at runtime — complex derivation, cross-source lookup, context-dependent formatting — that a plain CDS expression cannot express. Triggers include "virtual element", "virtualElementCalculatedBy", "if_sadl_exit", "calculated field trong CDS view", "field tính lúc runtime không lưu DB", "thêm virtual element cho X", "computed field at read time". For simple arithmetic/CASE derivations use cds-analytical-views; for a fully code-driven read source use rap-query-provider.
---

# CDS Virtual Elements — Calculated Fields at Read Time

A virtual element is a CDS field with **no database storage**. Its value is computed in ABAP each time an OData/Fiori consumer reads the entity. This skill covers the two artifacts it always needs: the CDS declaration and the exit class.

This skill exists because [Skill: fs-logic-behavior-translator] and both FS-analysis workflows *decide* "implement as Virtual Element" during TS creation — this is the skill that implements that decision.

## Pick the right mechanism first

Virtual elements are the most expensive read-path option. Exhaust the cheaper ones first.

| Situation | Use | Why |
|---|---|---|
| Arithmetic, `CASE`, concatenation, unit/currency conversion, date functions over fields already in the source | Plain CDS expression — [Skill: cds-analytical-views] | Pushed down to the database. No ABAP, no per-row cost. |
| Value derivable by joining/associating another released CDS view | CDS association or join | Still database-side. Prefer this over an ABAP lookup. |
| Value needs ABAP logic at **read** time: multi-source derivation, released-API call, context-dependent formatting (user language, system date, role) | **Virtual element** (this skill) | Read-only, per-row, no persistence. |
| Value must be **persisted** (audited, reported on, filtered/sorted server-side at scale) | Real field + [Skill: rap] determination | Virtual elements cannot be filtered or sorted by the database. |
| The *whole* entity's data comes from code, not a table/view | Custom Entity + [Skill: rap-query-provider] | Different layer: replaces the read source entirely, not one field. |

Hard limits to state in the TS before choosing this: a virtual element **cannot be used in a database `WHERE`/`ORDER BY`**, and it is recomputed on every read.

## Step 1 — Declare in the CDS view

```abap
define view entity ZI_<Object>
  as select from <source> as items
{
  key items.<KeyField>,
      items.<Field1>,

      @ObjectModel.virtualElementCalculatedBy: 'ABAP:ZCL_<CLASS_NAME>'
      cast( '' as abap.char( 1000 ) ) as <VirtualField>
}
```

- The annotation value is `'ABAP:<CLASS_NAME>'` — the `ABAP:` prefix is part of the annotation syntax, the class itself follows [Skill: naming-convention] (`ZCL_*`).
- The `cast( ... )` is a type placeholder only; its type must match what the class writes back. Cast a literal of the target type — do not cast a real field.
- Declare it on the layer the consumer reads. If the projection/consumption view is what the service exposes, the annotation belongs there (or must be propagated).

## Step 2 — Implement the exit class

```abap
CLASS zcl_<class_name> DEFINITION PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_sadl_exit.
    INTERFACES if_sadl_exit_calc_element_read.
ENDCLASS.

CLASS zcl_<class_name> IMPLEMENTATION.

  METHOD if_sadl_exit_calc_element_read~calculate.
    DATA lt_data TYPE STANDARD TABLE OF zi_<object> WITH DEFAULT KEY.
    lt_data = CORRESPONDING #( it_original_data ).

    LOOP AT lt_data ASSIGNING FIELD-SYMBOL(<data>).
      <data>-<virtual_field> = compute_value( <data> ).
    ENDLOOP.

    ct_calculated_data = CORRESPONDING #( lt_data ).
  ENDMETHOD.

  METHOD if_sadl_exit~get_exit_info.
    rs_exit_info-def_entity = VALUE #( ( entity = 'ZI_<OBJECT>' ) ).
  ENDMETHOD.

ENDCLASS.
```

Both interfaces are required — `if_sadl_exit~get_exit_info` tells the framework which entity this exit serves.

`it_original_data` only carries the fields the consumer actually requested. If your computation needs a field the consumer did not select, request it explicitly via `@ObjectModel.virtualElement.requiredOriginalElements` on the virtual element; do not assume the field is present.

## Gotcha — `utclong` timestamps overflow into a short dump

This one does not fail at activation. It fails when a user opens the app.

Many released CDS timestamp fields are typed **`utclong`** (an internal number around 17–18 digits), **not** `DEC15` in `yyyymmddhhmmss` form. The two look alike because both read as "a date-time number".

- Passing a `utclong` into a parameter typed `p LENGTH 8 DECIMALS 0` (15 digits) overflows on assignment → `CX_SY_ARITHMETIC_OVERFLOW` → surfaces as `CX_SADL_EXIT_PROCESSING_ERROR` → **short dump on opening the app**, with a clean activation log.
- Compare two timestamps **directly** (`actual > planned`, guarded with `IS NOT INITIAL`). Do not convert to packed. To extract a date, use `CONVERT UTCLONG ... INTO DATE ... TIME ZONE ...`.
- Prefer helper methods that take `abap_bool` (decision already made at the call site) over ones typed to a concrete timestamp type — that way the helper does not depend on the field's real type.
- **Verify the field's actual type first** (F2 on the data element in ADT, or `SELECT ... INTO @DATA(...)` and read the inferred type). Never assume `utclong` vs `timestamp`.

## Performance

The class runs for **every row of every read**. Budget accordingly:

- Never exceed ~100 ms per row. Above that, the field belongs in the database (real field + determination) or in a batch-computed source.
- Batch external work: one released-API/lookup call covering all rows in `it_original_data`, not one call per row inside the `LOOP`.
- Cache derivations that repeat across rows (e.g. one text lookup per distinct key, not per row).
- Prefer a join/association over an ABAP lookup whenever the data is reachable in CDS.

## After creating both objects

This is a two-object change with a dependency (the CDS view references the class by name). Per `sap-dev-rule.md` §5, run [Skill: activation-guard]'s 3 gates after **each** object, not once at the end — and Gate 3 specifically on the projection/consumption views and service bindings above the modified view, since the annotation propagates upward.

Write the unit test with the template in [Skill: abap-unit-testing] (`references/test-class-patterns.md`) — assert on the computed value for a known input row, not merely that the field is non-initial.

## References

- Interfaces: `IF_SADL_EXIT`, `IF_SADL_EXIT_CALC_ELEMENT_READ`
- Annotations: `@ObjectModel.virtualElementCalculatedBy`, `@ObjectModel.virtualElement.requiredOriginalElements`
- [Skill: cds-analytical-views] — CDS-level expressions and annotations (the cheaper alternative)
- [Skill: rap-query-provider] — when the whole read source is code
- [Skill: naming-convention] — class and CDS naming
