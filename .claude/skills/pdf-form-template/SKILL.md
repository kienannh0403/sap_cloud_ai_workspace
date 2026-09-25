---
name: pdf-form-template
description: Draw an Adobe print form (XFA .xdp template with data binding) plus a matching sample data XML from the "Form in / Mẫu báo cáo" sample in an FS, for Adobe Forms Service (ADS) on S/4HANA Public Cloud / SAP BTP. Spec-driven — page header (logo, company/plant name + address), title, label/value blocks, tables with blank handwriting columns, 2-level column headers, asset-class style groups with subtotals and a grand total, signature block, page x/y — and a binding check that every field resolves against the sample XML. Use when an FS has a PDF/print form mock-up to build, when the user asks for a .xdp / Adobe form / form PDF / form in / XML data for a form, or when a form preview in Adobe Designer shows script errors or empty tables. Excel exports use excel-form-template instead.
---

# PDF form template (Adobe XFA .xdp + sample XML)

Produces **files only** — `<name>.xdp` (template) and `<name>_data.xml` (sample data whose structure *is* the
data contract ABAP must fill). No SAP call, no upload.

## Gate: no form sample in the FS → no form
Draw only when the FS has a printed-form sample (image/mock-up of the output document, e.g. section "Form in",
"Mẫu báo cáo"). An ALV screen mock-up or "cho phép export" is not a sample. None found → tell the user and
produce nothing (user rule, 2026-09-25). Never invent a layout.

## Read the FS
- `.doc` — and `.docx` files that are really old binary Word (`file` says "Composite Document File"; Word
  refuses "format does not match the extension") — copy to `.doc`, open with Word COM, `SaveAs2(..., 16)`
  to a real `.docx`, then unzip `word/document.xml` + `word/media/*`. Keep this in the session scratchpad.
- Read the form sample image(s) with the Read tool; map every `(n)` marker to the FS field table.
- Take font, sizes, margins, header/footer rules from the FS "Các qui định chung" table.

## Workflow
1. **Spec** — write `artifacts/targets/<TARGET>/forms/<name>.spec.json` per `references/spec-schema.md`
   (worked example: `references/example-spec.json`). Name: [Skill: naming-convention] §7 Form `<SYSTEM>_F_<tcode>`.
   Column widths: take the proportions from the sample image, scale to the content width.
   Fields the FS says the user fills in by hand after printing → `"name": null` (blank bordered cell).
   Sample data: realistic values from the FS screenshots; amounts obey the FS formulas; logos via `@file:`.
2. **Build + check:**
   ```
   python .claude/skills/pdf-form-template/scripts/build_xdp.py artifacts/targets/<TARGET>/forms/<name>.spec.json --out-dir artifacts/targets/<TARGET>/forms
   ```
   Exit 0 = every `dataRef` resolves and every data leaf is bound. Fix the spec until it passes.
3. **Hand over** — layout summary, the XML structure (it is the ABAP contract), decisions taken beyond the
   FS, and the preview steps: open the `.xdp` in Adobe Designer → **File → Form Properties → Preview → Data
   File** = the `_data.xml` → Preview PDF. The form is proven only by that preview (rule §11) — ask for it.

## XFA rules learned the hard way (the builder already applies them)
- Page numbers: JavaScript in the `layout:ready` event (`xfa.layout.page(this)`, `runAt="both"`). A
  FormCalc `calculate` with `xfa.layout.page($)` fails in Acrobat: "Argument mismatch".
- `defaultPDFRenderFormat acrobat10.0dynamic` — a static preview does not add rows from data.
- Empty tables in preview usually mean **no preview data file configured**, not a binding error.
- Repeating header: flat table → `<overflow leader="HeaderRow"/>` on the table; grouped table → header in
  its own table subform `THead`, leader on the outer block.
- XFA tables have `colSpan` but no row span: a 2-level header is a cell subform (`colSpan=n`) holding the
  group title over an `lr-tb` row of the sub-titles.
- Separate `layout="table"` subforms sharing the same `columnWidths` keep group/total rows aligned with data rows.
- Pass numbers/dates as formatted strings and compute subtotals/totals in ABAP; the form only displays.
- Tables too wide for the FS font size: keep FS sizes for title/header, shrink only the table font, and say so.
