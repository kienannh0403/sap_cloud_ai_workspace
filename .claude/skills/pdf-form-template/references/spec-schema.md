# Spec schema — `build_xdp.py`

One UTF-8 JSON file per form. Sizes in **mm**, font sizes in **pt**. Worked example (FS ZMFGLSX "Lệnh sản
xuất", approved in Designer preview 2026-09-25): `example-spec.json`.

```jsonc
{
  "name": "DEV_F_ZMFGLSX",                 // file base name; naming-convention §7 Form: <SYSTEM>_F_<tcode>
  "locale": "vi_VN",
  "data_root": "Form",                     // root element of the data XML (default Form)
  "page": { "size": "A4|A3|A5", "orientation": "landscape|portrait", "font": "Arial", "base_size": 10,
            "margins": { "left": 10, "right": 10, "top": 5, "bottom": 5 } },
  "page_header": { "height": 25,           // repeated on every page, above the content area
    "items": [                             // x/y relative to the top-left margin corner
      { "type": "image", "bind": "Header.Logo", "x": 0, "y": 0, "w": 30, "h": 22, "content_type": "image/png" },
      { "type": "field", "bind": "Header.PlantName", "x": 35, "y": 2, "w": 200, "h": 7, "size": 11, "bold": true } ] },
  "page_footer": { "height": 5, "page_number": { "format": "x/y | Trang x/y | x", "align": "right" } },
  "body": [ /* blocks, top to bottom — see below */ ],
  "sample": { /* data XML as JSON; "@file:<path>" = base64 of that file (logos) */ }
}
```
`bind` in `page_header` is absolute from the data root (`$record.…`); in `body` it is relative to the root.

## Body blocks
| type | keys | renders |
|---|---|---|
| `text` | `text`, `size`, `bold`, `italic`, `align`, `valign`, `h`, `space_before` | static text (title, section heading) — not data |
| `field` | `bind` (e.g. `Header.PeriodText`), `align`, `italic`, `bold`, `h`, `w` | one data field |
| `info` | `bind` (data node), `columns`, `caption_width`, `row_h`, `items: [[caption, field], …]` row-major | label/value grid (captions bold) |
| `table` | see below | data table, header row repeats on every page |
| `write_line` | `text`, `label_w` | caption + dotted line for handwriting |
| `signatures` | `items: [titles]`, `h` | signature titles in equal columns, never split across pages |

## `table`
```jsonc
{ "type": "table", "bind": "Operations", "row": "Operation",   // rows = $.Operations.Operation[*]
  "font_size": 10, "row_min_h": 8, "header_h": 12, "header_fill": "217,217,217",
  "columns": [ { "name": "OperationNo", "title": "Mã công đoạn", "w": 17, "align": "left|center|right" },
               { "name": null, "title": "Ngày thực tế thực hiện", "w": 22 } ],   // name null = blank cell (handwriting)
  "header_groups": [ { "title": "Đầu kỳ", "start": 16, "span": 3 } ],           // optional 2-level header
  "group": { "bind": "Groups", "row": "Group", "label": "GroupText", "label_span": 14 },  // optional
  "total": { "bind": "Total", "label": "Tổng cộng", "label_span": 14 } }                 // optional
```
- Column widths **must sum to the content width** (page width − left − right margin) — the build stops otherwise.
- `group`: data `Groups/Group[*]` each holding `GroupText` + one value per column after `label_span`
  (same names as the columns) + the rows `<bind>/<row>[*]`. Group line = label over the first `label_span`
  columns + subtotals, bold, kept with its first row.
- `total`: data `Total` with one value per column after `label_span`; static label.
- Subtotals/totals are computed in ABAP and passed as formatted strings — the form never sums.
