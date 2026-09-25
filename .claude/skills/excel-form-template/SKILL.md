---
name: excel-form-template
description: Build the Excel form template (.xlsx) that an FS asks for, for the in-house FIS "Tools Export Excel" on S/4HANA Public Cloud — the mapping file uploaded in the "Upload Template file excel" app and rendered by ZCL_EXPORT_EXCEL_XLSX->EXPORT_EXCEL — plus its field dictionary (.xlsx) and the ABAP TYPES/fill/call snippet for it_data. Also lints an existing template against the real parser rules (2-digit font size, 7 align codes, 8 colors, no '_' in table/level names, Report Name ≤ 10, merge overlaps). Use when an FS, mock-up, screenshot or field list describes an Excel printout/form to export, or when the user mentions EXCEL form, form excel, template excel upload, ITEM_<table> markers, EXPORT_EXCEL, zde_attachment_tmpl, or asks why an uploaded Excel template renders wrong. For PDF/Adobe forms this skill does not apply.
---

# Excel form template (FIS Tools Export Excel)

Turns an FS form requirement into the upload template (plus, on request, a field dictionary and ABAP TYPES) a developer needs for the in-house Excel export tool.
The backend already exists on the system — this skill writes **files only** and never calls an SAP
mutation tool; the user uploads the template in the app.

**Read `references/grammar.md` before mapping any cell.** It is the UM v0.2 rule set verified against
the parser/renderer code (markers, cell syntax, rendering, limits, known defects). Never invent a
format/color/align code that is not listed there.

## Inputs to settle first (ask with [Skill: grill-me] if the FS is silent)
- **TARGET** (tcode / report the form belongs to) → output folder `artifacts/forms/<TARGET>/`.
- **Report Name** (upload app) = the tcode, **≤ 10 chars**.
- **Template name** ≤ 20 chars — default per [Skill: naming-convention] §7 (Excel form): `<tcode>_EXC` (e.g. `ZSD01_EXC`). Same name on every system, so the ABAP constant does not change between DEV/TEST/PRD.
- Which blocks **repeat** (→ nested tables) and whether any table needs **per-level row formats** (subtotal/group lines → level field + values).
- Number/date display format — the tool prints the string it is given, so formatting is done in ABAP.
- Logo or pre-built layout needed? → only via `iv_generate = abap_true` with a GEN base file (see grammar §4).

FS in DOCX/XLSX/PDF → convert with [Skill: document-markdown-converter] first; mock-up images →
[Skill: fs-vision-extractor] to get the grid as a table before mapping.

## Workflow
1. **Map the form to a grid.** Walk the mock-up top to bottom; for each output row decide the column-A marker
   (`HEADER` / `ITEM` title / `ITEM_<Table>[_<LevelField>_<Value>]` / `FOOTER`, or empty for a spacer row) and,
   per cell, the field token + style + merge + colors. Remember the **shift**: template B2 = output A1.
2. **Every printed text is a field** — captions, column titles, signatures included (a raw literal is never printed).
   Name labels `LBL_*`, `HDR_*`/`HEADER*`, `SEC_*`, `SIGN*`, `TITLE*`; data fields use business names (≤ 30 chars).
   Table and level-field names: letters/digits only, **no `_`** (`TABLE1`, `ZLEVEL`).
3. **Write the spec** `artifacts/forms/<TARGET>/<template>.spec.json` (schema in the script docstring;
   worked example: `references/example-spec.json`). Put label texts in `fields.<NAME>.text` and data
   sources (released CDS field) in `fields.<NAME>.source`. Always UTF-8 — Vietnamese text stays intact.
4. **Build + lint:**
   ```
   python .claude/skills/excel-form-template/scripts/build_form.py build artifacts/forms/<TARGET>/<template>.spec.json --out-dir artifacts/forms/<TARGET>
   ```
   Errors block the write — fix the spec and rerun until `0 error(s)`; assess every warning. Default output
   is **only** `<template>.xlsx` (the upload file) — the user's standing preference. Add `--with-fields`
   (label/data/level dictionary `.xlsx`) or `--with-types` (TYPES for it_data + label fill + `EXPORT_EXCEL`
   call `.abap`) only when the user asks for them.
5. **Hand over** (chat): upload steps — app "Upload Template file excel" → Create → Report Name / Template →
   upload `<template>.xlsx` → Create → check the "View data" tab (status stays `I`, that is normal).
   Then the checks below.
6. Record the form in `artifacts/system_analysis/<TARGET>/INDEX.md` (file map + open points).

**Linting an existing template** (user-supplied or already uploaded, e.g. "export looks wrong"):
```
python .claude/skills/excel-form-template/scripts/build_form.py lint <file.xlsx> --report <RPT> --template <TPL>
```

## Always state to the user
- Lint-clean ≠ correct: the template is only proven by a real upload + export. Ask for the exported file
  or a screenshot before calling the form done (rule §11).
- Level data must be UPPERCASE and match the marker values exactly; otherwise the first level row's format is used.
- `iv_generate` is mandatory; `abap_true` without a GEN upload dumps.
- One it_data row = one sheet.
- Code defects found in the tool (grammar §6) are reported, not patched from here.
