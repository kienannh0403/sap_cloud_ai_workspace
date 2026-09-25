"""build_xdp.py - Adobe form (XFA 3.3 .xdp) + sample data XML from a JSON spec, then binding check.

    python build_xdp.py <spec.json> --out-dir <dir>

Writes <name>.xdp and <name>_data.xml, then runs check_xdp.py on the pair (exit 1 if a binding is broken).
Spec schema: see references/spec-schema.md. All sizes in mm, font sizes in pt.
"""
import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.stdout.reconfigure(encoding="utf-8")

PAPER = {"A4": (297, 210), "A3": (420, 297), "A5": (210, 148)}   # long, short
GREY = "217,217,217"


class Ctx:
    def __init__(self, spec):
        self.spec = spec
        pg = spec.get("page", {})
        self.font = pg.get("font", "Arial")
        self.base = pg.get("base_size", 10)
        long_, short = PAPER[pg.get("size", "A4")]
        self.landscape = pg.get("orientation", "portrait") == "landscape"
        self.pw, self.ph = (long_, short) if self.landscape else (short, long_)
        self.stock, self.long, self.short = pg.get("size", "A4").lower(), long_, short
        m = pg.get("margins", {})
        self.ml, self.mr, self.mt, self.mb = (m.get(k, 10) for k in ("left", "right", "top", "bottom"))
        self.cw = self.pw - self.ml - self.mr                         # content width
        self.hdr_h = spec.get("page_header", {}).get("height", 0)
        self.ftr_h = spec.get("page_footer", {}).get("height", 0)
        self.uid = 0

    def name(self, prefix):
        self.uid += 1
        return f"{prefix}{self.uid}"

    def fnt(self, size=None, bold=False, italic=False):
        return (f'<font typeface="{self.font}" size="{size or self.base}pt"'
                f'{" weight=" + chr(34) + "bold" + chr(34) if bold else ""}'
                f'{" posture=" + chr(34) + "italic" + chr(34) if italic else ""}/>')


def mm(v):
    return f"{round(v, 2)}mm"


MARGIN = '<margin topInset="0.5mm" bottomInset="0.5mm" leftInset="0.8mm" rightInset="0.8mm"/>'


def border(fill=None, thickness=0.15):
    f = f'<fill><color value="{fill}"/></fill>' if fill else ""
    return f'<border><edge thickness="{thickness}mm"/>{f}</border>'


def ref(path, absolute=False):
    return ("$record." if absolute else "$.") + path


# ------------------------------------------------------------------ body blocks
def blk_text(c, b):
    return (f'<draw name="{c.name("Text")}" w="{mm(c.cw)}" h="{mm(b.get("h", 8))}"><ui><textEdit/></ui>'
            f'<value><text>{escape(b["text"])}</text></value>'
            f'{c.fnt(b.get("size"), b.get("bold", False), b.get("italic", False))}'
            f'<margin topInset="{b.get("space_before", 0)}mm"/>'
            f'<para hAlign="{b.get("align", "left")}" vAlign="{b.get("valign", "middle")}"/></draw>')


def blk_field(c, b):
    name = b["bind"].split(".")[-1]
    return (f'<field name="{name}" w="{mm(b.get("w", c.cw))}" minH="{mm(b.get("h", 7))}">'
            f'<ui><textEdit multiLine="1"/></ui>{c.fnt(b.get("size"), b.get("bold", False), b.get("italic", False))}'
            f'<para hAlign="{b.get("align", "left")}" vAlign="middle"/>'
            f'<bind match="dataRef" ref="{ref(b["bind"])}"/></field>')


def blk_info(c, b):
    cols = b.get("columns", 2)
    w = c.cw / cols
    cells = []
    for cap, fname in b["items"]:
        cells.append(
            f'<field name="{fname}" w="{mm(w)}" minH="{mm(b.get("row_h", 7))}"><ui><textEdit multiLine="1"/></ui>'
            f'{c.fnt(b.get("size"))}<para vAlign="middle"/>'
            f'<caption reserve="{mm(b.get("caption_width", 55))}">{c.fnt(b.get("size"), bold=True)}'
            f'<para vAlign="middle"/><value><text>{escape(cap)}</text></value></caption>'
            f'<bind match="dataRef" ref="$.{fname}"/></field>')
    return (f'<subform name="{b["bind"]}" layout="lr-tb" w="{mm(c.cw)}"><bind match="dataRef" ref="$.{b["bind"]}"/>'
            f'<margin bottomInset="{b.get("space_after", 2)}mm"/>{"".join(cells)}</subform>')


def blk_write_line(c, b):
    lw = b.get("label_w", 70)
    return (f'<subform name="{c.name("WriteLine")}" layout="lr-tb" w="{mm(c.cw)}"><bind match="none"/>'
            f'<draw name="Label" w="{mm(lw)}" h="10mm"><ui><textEdit/></ui><value><text>{escape(b["text"])}</text></value>'
            f'{c.fnt(b.get("size"))}<para vAlign="bottom"/></draw>'
            f'<draw name="Line" w="{mm(c.cw - lw)}" h="10mm"><ui><textEdit/></ui><border><edge presence="hidden"/>'
            f'<edge presence="hidden"/><edge stroke="dotted" thickness="0.3mm"/><edge presence="hidden"/></border></draw>'
            f'</subform>')


def blk_signatures(c, b):
    items = b["items"]
    w = c.cw / len(items)
    cells = "".join(
        f'<draw name="Sign{i + 1}" w="{mm(w)}" h="{mm(b.get("h", 30))}"><ui><textEdit/></ui>'
        f'<value><text>{escape(t)}</text></value>{c.fnt(b.get("size"), bold=True)}'
        f'<para hAlign="center" vAlign="top"/></draw>' for i, t in enumerate(items))
    return (f'<subform name="Signatures" layout="lr-tb" w="{mm(c.cw)}"><bind match="none"/>'
            f'<keep intact="contentArea"/><margin topInset="{b.get("space_before", 6)}mm"/>{cells}</subform>')


# ------------------------------------------------------------------ table
def tbl_cell(c, col, size, bold=False, span=None, min_h=5):
    sp = f' colSpan="{span}"' if span else ""
    if not col.get("name"):   # blank cell for handwriting
        return (f'<draw name="{c.name("Blank")}" w="{mm(col["w"])}" minH="{mm(min_h)}"{sp}><ui><textEdit/></ui>'
                f'{border()}</draw>')
    return (f'<field name="{col["name"]}" w="{mm(col["w"])}" minH="{mm(min_h)}"{sp}><ui><textEdit multiLine="1"/></ui>'
            f'{c.fnt(size, bold)}{MARGIN}<para hAlign="{col.get("align", "left")}" vAlign="middle"/>{border()}'
            f'<bind match="dataRef" ref="$.{col["name"]}"/></field>')


def tbl_head(c, t, size):
    cols, h = t["columns"], t.get("header_h", 12)
    groups = {g["start"]: g for g in t.get("header_groups", [])}
    gh = t.get("group_title_h", 5)

    def draw(text, w, hh):
        return (f'<draw name="{c.name("H")}" w="{mm(w)}" h="{mm(hh)}"><ui><textEdit multiLine="1"/></ui>'
                f'<value><text>{escape(text)}</text></value>{c.fnt(size, bold=True)}{MARGIN}'
                f'<para hAlign="center" vAlign="middle"/>{border(t.get("header_fill", GREY))}</draw>')
    cells, i = [], 0
    while i < len(cols):
        if i in groups:
            g = groups[i]
            sub = cols[i:i + g["span"]]
            gw = sum(x["w"] for x in sub)
            inner = "".join(draw(x["title"], x["w"], h - gh) for x in sub)
            cells.append(f'<subform name="{c.name("HG")}" layout="tb" w="{mm(gw)}" colSpan="{g["span"]}">'
                         f'{draw(g["title"], gw, gh)}<subform name="Cols" layout="lr-tb" w="{mm(gw)}">{inner}</subform>'
                         f'</subform>')
            i += g["span"]
        else:
            cells.append(draw(cols[i]["title"], cols[i]["w"], h))
            i += 1
    return f'<subform name="HeaderRow" layout="row">{"".join(cells)}</subform>'


def tbl_sum_row(c, t, size, label, label_is_field):
    span = label["span"]
    cols = t["columns"]
    lw = sum(x["w"] for x in cols[:span])
    if label_is_field:
        first = tbl_cell(c, {"name": label["field"], "w": lw, "align": "left"}, size, bold=True, span=span)
    else:
        first = (f'<draw name="{c.name("Label")}" w="{mm(lw)}" minH="5mm" colSpan="{span}"><ui><textEdit/></ui>'
                 f'<value><text>{escape(label["text"])}</text></value>{c.fnt(size, bold=True)}{MARGIN}'
                 f'<para vAlign="middle"/>{border()}</draw>')
    rest = "".join(tbl_cell(c, x, size, bold=True) for x in cols[span:])
    return f'<subform name="{c.name("SumRow")}" layout="row">{first}{rest}</subform>'


def blk_table(c, t):
    size = t.get("font_size", c.base)
    cols = t["columns"]
    total_w = sum(x["w"] for x in cols)
    if abs(total_w - c.cw) > 0.01:
        sys.exit(f"table '{t['bind']}': column widths sum to {total_w}mm, content width is {c.cw}mm")
    widths = " ".join(mm(x["w"]) for x in cols)
    min_h = t.get("row_min_h", 5)
    row = (f'<subform name="Row" layout="row"><occur min="0" max="-1"/><keep intact="contentArea"/>'
           f'<bind match="dataRef" ref="$.{t["row"]}[*]"/>'
           + "".join(tbl_cell(c, x, size, min_h=min_h) for x in cols) + "</subform>")
    head = tbl_head(c, t, size)

    def table(name, bind, body, extra=""):
        b = f'<bind match="dataRef" ref="$.{bind}"/>' if bind else '<bind match="none"/>'
        return (f'<subform name="{name}" layout="table" columnWidths="{widths}" w="{mm(c.cw)}">{b}{extra}'
                f'{body}</subform>')

    g = t.get("group")
    if not g:   # flat table: header repeats via overflow leader of the table itself
        body = table(t["bind"], t["bind"], head + row, '<overflow leader="HeaderRow"/>')
        parts = [body]
    else:       # grouped: header table is the overflow leader of the outer container
        grp = (f'<subform name="{g["row"]}" layout="tb" w="{mm(c.cw)}"><occur min="0" max="-1"/>'
               f'<bind match="dataRef" ref="$.{g["row"]}[*]"/>'
               + table("GroupTbl", None, tbl_sum_row(c, t, size, {"span": g["label_span"], "field": g["label"]}, True),
                       '<keep next="contentArea"/>')
               + table(t["bind"], t["bind"], row) + "</subform>")
        parts = [table("THead", None, head),
                 f'<subform name="{g["bind"]}" layout="tb" w="{mm(c.cw)}"><bind match="dataRef" ref="$.{g["bind"]}"/>'
                 f'{grp}</subform>']
    tot = t.get("total")
    if tot:
        parts.append(table("TotalTbl", tot["bind"],
                           tbl_sum_row(c, t, size, {"span": tot["label_span"], "text": tot["label"]}, False),
                           '<keep intact="contentArea"/>'))
    if not g and not tot:
        return parts[0]
    lead = '<overflow leader="THead"/>' if g else ""
    return (f'<subform name="{c.name("TableBlock")}" layout="tb" w="{mm(c.cw)}"><bind match="none"/>{lead}'
            f'{"".join(parts)}</subform>')


BLOCKS = {"text": blk_text, "field": blk_field, "info": blk_info, "table": blk_table,
          "write_line": blk_write_line, "signatures": blk_signatures}


# ------------------------------------------------------------------ page area
def page_item(c, it):
    x, y = c.ml + it.get("x", 0), c.mt + it.get("y", 0)
    geo = f'x="{mm(x)}" y="{mm(y)}" w="{mm(it["w"])}" h="{mm(it["h"])}"'
    name = it["bind"].split(".")[-1]
    if it["type"] == "image":
        return (f'<field name="{name}" {geo}><ui><imageEdit data="embed"/></ui>'
                f'<value><image aspect="fit" contentType="{it.get("content_type", "image/png")}"/></value>'
                f'<bind match="dataRef" ref="{ref(it["bind"], True)}"/></field>')
    return (f'<field name="{name}" {geo}><ui><textEdit/></ui>'
            f'{c.fnt(it.get("size"), it.get("bold", False), it.get("italic", False))}'
            f'<para hAlign="{it.get("align", "left")}" vAlign="middle"/>'
            f'<bind match="dataRef" ref="{ref(it["bind"], True)}"/></field>')


def page_number(c, f):
    pn = f["page_number"]
    fmt = pn.get("format", "x/y")
    js = {"x/y": 'xfa.layout.page(this) + "/" + xfa.layout.pageCount()',
          "Trang x/y": '"Trang " + xfa.layout.page(this) + "/" + xfa.layout.pageCount()',
          "x": "xfa.layout.page(this)"}[fmt]
    y = c.ph - c.mb - f.get("height", 5)
    # layout:ready + JavaScript: page numbers only exist after layout (calculate/FormCalc fails)
    return (f'<field name="PageNo" x="{mm(c.ml)}" y="{mm(y)}" w="{mm(c.cw)}" h="{mm(f.get("height", 5))}">'
            f'<ui><textEdit/></ui>{c.fnt(pn.get("size"))}<para hAlign="{pn.get("align", "right")}"/>'
            f'<event activity="ready" ref="$layout" name="event__layout_ready">'
            f'<script contentType="application/x-javascript" runAt="both">this.rawValue = {js};</script></event>'
            f'<bind match="none"/></field>')


def build_xdp(spec):
    c = Ctx(spec)
    items = "".join(page_item(c, it) for it in spec.get("page_header", {}).get("items", []))
    if spec.get("page_footer", {}).get("page_number"):
        items += page_number(c, spec["page_footer"])
    ca_y = c.mt + c.hdr_h
    ca_h = c.ph - ca_y - c.mb - c.ftr_h
    body = "\n  ".join(BLOCKS[b["type"]](c, b) for b in spec["body"])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<?xfa generator="pdf-form-template" APIVersion="3.3"?>
<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/">
<template xmlns="http://www.xfa.org/schema/xfa-template/3.3/">
<?formServer defaultPDFRenderFormat acrobat10.0dynamic?>
<subform name="Form" layout="tb" locale="{spec.get("locale", "vi_VN")}" restoreState="auto">
  <pageSet>
    <pageArea name="Page1" id="Page1">
      <medium stock="{c.stock}" short="{mm(c.short)}" long="{mm(c.long)}"{' orientation="landscape"' if c.landscape else ''}/>
      <contentArea x="{mm(c.ml)}" y="{mm(ca_y)}" w="{mm(c.cw)}" h="{mm(ca_h)}"/>
      {items}
    </pageArea>
  </pageSet>
  {body}
</subform>
</template>
</xdp:xdp>
'''


# ------------------------------------------------------------------ sample XML
def to_xml(tag, val, spec_dir, ind=1):
    pad = "  " * ind
    if isinstance(val, dict):
        inner = "\n".join(to_xml(k, v, spec_dir, ind + 1) for k, v in val.items())
        return f"{pad}<{tag}>\n{inner}\n{pad}</{tag}>"
    if isinstance(val, list):
        return "\n".join(to_xml(tag, v, spec_dir, ind) for v in val)
    s = "" if val is None else str(val)
    if s.startswith("@file:"):
        p = Path(s[6:])
        s = base64.b64encode((p if p.is_absolute() else spec_dir / p).read_bytes()).decode()
    return f"{pad}<{tag}>{escape(s)}</{tag}>"


def build_xml(spec, spec_dir):
    root = spec.get("data_root", "Form")
    inner = "\n".join(to_xml(k, v, spec_dir) for k, v in spec["sample"].items())
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<{root}>\n{inner}\n</{root}>\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    spec_path = Path(a.spec)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    xdp, xml = out / f"{spec['name']}.xdp", out / f"{spec['name']}_data.xml"
    xdp.write_text(build_xdp(spec), encoding="utf-8")
    xml.write_text(build_xml(spec, spec_path.parent), encoding="utf-8")
    print(f"written: {xdp}, {xml}")
    return subprocess.call([sys.executable, str(Path(__file__).with_name("check_xdp.py")), str(xdp), str(xml)])


if __name__ == "__main__":
    sys.exit(main())
