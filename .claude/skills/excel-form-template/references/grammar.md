# Template grammar — FIS "Tools Export Excel" (UM v0.2, verified against code)

Source of truth: `artifacts/documents/UM_Excel_Tool/UM_SAP-PUBLIC-CLOUD_ToolsExportExcel_v0.2.docx`,
which was corrected against the live code on 080 (2026-09-25):

| Piece | Object (package) |
|---|---|
| Parser (upload → mapping rows) | `ZBP_R_UPLOAD_TMPL` → `lhc__file->getdatafile` (`ZMAPPING_EXPORT`) |
| Renderer | `ZCL_EXPORT_EXCEL_XLSX->EXPORT_EXCEL` (`ZEXCEL_EXPORT`) |
| Style builder | `ZCL_GET_STYLE_TMPL_EXPORT_N->BUILD_STYLE` (`ZEXCEL_EXPORT`) |
| Tables | `ZTB_UPLOAD_TMPL` (uploaded file), `ZTB_TMPL_EXPORT` (parsed mapping) |
| Upload app | "Upload Template file excel" — `ZR_UPLOAD_TMPL` / `ZUI_UPLOAD_TMPL` |

Package `ZEXCEL_UPLOAD` (`ZR_EX_TMPL_HDR`) is a separate prototype — the renderer never reads it.

## 1. Sheet layout
- Only the **first worksheet** is parsed. Max **100 columns** (`ZST_EXCELMAPPING` = C0001…C0100) → 99 data columns (B…CV).
- **Row 1** = column widths (numbers) from column B; A1 blank. A column with no width keeps Excel's default.
- **Column A** = row marker (upper-cased by the parser). A row with column A empty is **skipped but still
  counts** → it becomes an empty row in the output.
- **Output shift**: row 1 and column A are dropped → template **B2 becomes output A1** (row −1, col −1).
- Max **255 template rows** (`ROW_NUM` INT1).

## 2. Column-A markers
The parser does `SPLIT <A> AT '_' INTO layout itemname levelname zlevelvalue …`.

| Marker | Meaning |
|---|---|
| `HEADER` | Header row. No border. Fields read from the flat part of the it_data row. |
| `ITEM` | Item **column-title** row (itemname empty). Always bordered. Flat fields. Several consecutive `ITEM` rows are allowed (multi-line titles). |
| `ITEM_<Table>` | Item **data** row: printed once per line of nested table `<Table>`. Always bordered. |
| `ITEM_<Table>_<LevelField>_<LevelValue>` | Leveled data row: for each line, `<LevelField>` value selects the row whose `<LevelValue>` matches. |
| `FOOTER` | Footer row. No border. Shifted down by the number of printed item lines. |

Hard rules that follow from the `SPLIT`:
- `<Table>` and `<LevelField>` must **not contain `_`** (`TAB_1` → itemname `TAB`, levelname `1` — broken).
- The whole marker is upper-cased, so the level value compared is UPPERCASE; the data value is compared
  **as-is** (`READ TABLE … zlevelvalue = <value>`) → level data must be UPPERCASE. No match → the table's
  first level row is used.
- `<LevelValue>` ≤ 10 chars (`ZLEVELVALUE` CHAR 10). One level field per table (the renderer takes the first).
- A table has **one** data row (non-leveled) or one row **per level value**. Extra rows for the same
  table/level are never printed but still shift the footer.
- Any other marker (e.g. `TITLE`) is stored but never rendered.
- The code does not require all three of HEADER / ITEM / FOOTER.

## 3. Cell syntax (columns B+)
```
<FIELD>/<STYLE><MERGE><COLORS>
```
Parser regexes (value upper-cased first):

| Part | Regex in code | Rule |
|---|---|---|
| FIELD | `<([^>/]+)>` (first match) | Component name in it_data, case-insensitive, ≤ 30 chars (ABAP component). A cell with no `<…>` is taken as a field *name*, never printed as text. |
| STYLE | `/<([^>]+)>` | `<WEIGHT 2><SIZE 2 digits><ALIGN 2>` — see below. |
| MERGE | `-<(\d+)>` horizontal · `\|<(\d+)>` vertical | Number of **additional** cols/rows (`-<8>` spans 9 cols). ≤ 255. Both may appear. |
| COLORS | `([A-Z]{1,2})$` | At the **very end**. 1 letter = background; 2 letters = background + font. |

**STYLE detail** (`BUILD_STYLE`):
- Weight, matched as prefix: `BN` bold · `BI` bold+italic · `NN` normal · `NI` italic.
- Size: regex `[A-Z]{2}([0-9]{2})` → **exactly 2 digits**: `08`, `09`, `10`, `16`. `BN9CC` → size not read.
- Align (substring match, first hit wins, in this order): `LC` `LT` `LB` `CC` `RC` `RT` `RB`.
  Anything else (`CT`, `CB`, `CL`…) → vertical center, horizontal Excel default. Treat those as errors.
- Always: font **Times New Roman**, default font color black, **wrap text on**.

**Colors** (background and font use the same letters): `B` Blue · `R` Red · `Y` Yellow · `G` Green ·
`P` Purple · `W` White · `O` Orange · `K` Black. No color → no fill, black font.

Examples:

| Cell | Meaning |
|---|---|
| `<NAME>/<BN10LC>-<8>BR` | bold 10, left/center, +8 cols, blue fill, red font |
| `<TITLE_REPORT>/<BN16CC>-<6>` | bold 16 centered title over 7 cols |
| `<HEADER01>/<BN10CC>\|<1>Y` | bold 10 centered, +1 row down, yellow fill (2-line column title) |
| `<AMOUNT>/<NN10RC>` | normal 10, right/center |
| `<SIGN07>/<NI08CC>-<1>` | italic 8 centered over 2 cols |

## 4. Rendering rules (`EXPORT_EXCEL`)
- Instance method: `NEW zcl_export_excel_xlsx( )->export_excel( … )`.
- Signature: `iv_template TYPE char72`, `iv_report TYPE char72`, `it_data TYPE ANY TABLE`,
  **`iv_generate TYPE zde_char1` (mandatory, no default)**, EXPORTING `lv_context TYPE zde_attachment_tmpl`.
- **One it_data row = one sheet** (`Sheet1`, `Sheet2`, … orange tab).
- Flat components feed HEADER / ITEM-title / FOOTER cells; a table component named `<Table>` feeds
  `ITEM_<Table>` rows.
- Values are written with XCO `write_from` in the component's own type — pass pre-formatted strings for
  amounts/dates (rounding, separators, `dd.MM.yyyy`).
- A token with no matching component prints nothing (no error). In HEADER the merge is still applied.
- `iv_generate = abap_false` → empty workbook. `abap_true` → loads the file uploaded with
  **Report Name = `GEN`** and the same Template as the base (logo / pre-built layout), then writes on top.
  No GEN file → `lo_excel` unbound → **short dump**.

## 5. Upload app limits
- **Report Name ≤ 10 chars** (`ZTB_TMPL_EXPORT-REPORT_NAME` CHAR 10) even though the app accepts 50 —
  a longer name uploads fine but exports an empty file.
- **Template ≤ 20 chars** (`ZTB_UPLOAD_TMPL-TEMPLATE` CHAR 20).
- Re-uploading a file on the same record deletes and re-parses its mapping rows.
- Report Name `GEN` is **not parsed** — it only stores the base file for `iv_generate`.
- Status stays `I` after upload (code never sets success) — check the "View data" tab instead.

## 6. Known code defects (report, don't work around silently)
1. `iv_generate = abap_true` without a GEN upload → dump.
2. Report Name > 10 chars → silent empty export.
3. Upload status never leaves `I`.
