"""render_target.py - build the handbook page of a report/function from its handbook.json.

    python .claude/scripts/handbook/render_target.py <TARGET>      # one target
    python .claude/scripts/handbook/render_target.py --all         # every artifacts/targets/*/handbook.json

Source : artifacts/targets/<TARGET>/handbook.json   (schema: .claude/common/handbook-target.md)
Output : artifacts/handbook_targets/<target>.html  (<target> = lowercase, '_' -> '-')
Also   : regenerates artifacts/handbook_targets/index.html (one card per target), the nav of every
         page there, and its own copy of the stylesheet (assets/site.css, copied from the workspace
         handbook). The report/function handbook is a site of its own: no link to or from the workspace
         handbook (artifacts/handbook/); the renderer strips any target card, target nav link or old
         target page left there. Local page, no network, no JS.
"""
import json
import re
import shutil
import sys
from html import escape
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
TARGETS = ROOT / "artifacts" / "targets"
HB = ROOT / "artifacts" / "handbook"
HBT = ROOT / "artifacts" / "handbook_targets"
CSS = "assets/site.css"  # own copy, refreshed from artifacts/handbook/assets/site.css on every render
PILL = {"PASS": "pill-ok", "FAIL": "pill-dgr", "WAIT": "pill-wrn", "ACCEPTED": "pill-off",
        "ok": "pill-ok", "wrn": "pill-wrn", "dgr": "pill-dgr", "acc": "pill-acc", "off": "pill-off"}
EXTERNAL = "sửa ngoài workspace"
PREVIEW_ITEMS = {"handbook": "Trang handbook", "test": "Chạy thử báo cáo", "atc": "ATC toàn target",
                 "index": "INDEX.md", "notes": "Notes", "snapshot": "Snapshot source", "objects": "Object liên quan"}
RESULT_TEXT = {"PASS": "PASS", "FAIL": "FAIL", "WAIT": "chờ user", "ACCEPTED": "PASS — unverified, user-accepted"}
STATIC_NAV = [("index.html", "Trang chủ"), ("mcp.html", "MCP"), ("cds-catalog.html", "CDS released"),
              ("workspace-build.html", "Dựng workspace")]
SITE_TITLE = "Sổ tay báo cáo / chức năng"


def slug(target):
    return target.lower().replace("_", "-")


def e(v):
    return escape("" if v is None else str(v))


def pill(key, text=None):
    return f'<span class="pill {PILL.get(key, "pill-off")}">{e(text or RESULT_TEXT.get(key, key))}</span>'


def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="wrap"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


# ------------------------------------------------------------------ object diagram (inline SVG)
def diagram(objects):
    names = [o["name"] for o in objects]
    ext = []
    for o in objects:
        for u in o.get("uses", []):
            if u not in names and u not in ext:
                ext.append(u)
    nodes = {n: {"name": n, "type": "released / nguồn ngoài", "uses": [], "ext": True} for n in ext}
    nodes.update({o["name"]: {**o, "ext": False} for o in objects})
    rank = {}

    def depth(n, seen=()):
        if n in rank:
            return rank[n]
        if n in seen:
            return 0
        us = [u for u in nodes[n].get("uses", []) if u in nodes]
        rank[n] = 0 if not us else 1 + max(depth(u, seen + (n,)) for u in us)
        return rank[n]
    for n in nodes:
        depth(n)
    cols = {}
    for n in nodes:
        cols.setdefault(rank[n], []).append(n)
    bw, bh, gx, gy, pad = 170, 42, 70, 14, 10
    pos = {}
    for r, ns in cols.items():
        for i, n in enumerate(ns):
            pos[n] = (pad + r * (bw + gx), pad + i * (bh + gy))
    w = pad * 2 + (max(cols) + 1) * (bw + gx) - gx
    h = pad * 2 + max(len(v) for v in cols.values()) * (bh + gy) - gy
    parts = [f'<svg class="objmap" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
             f'aria-label="Sơ đồ object">',
             '<defs><marker id="arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" '
             'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--ink-3)"/></marker></defs>']
    for n, nd in nodes.items():
        for u in nd.get("uses", []):
            if u in pos:
                x1, y1 = pos[u][0] + bw, pos[u][1] + bh / 2
                x2, y2 = pos[n][0], pos[n][1] + bh / 2
                mx = (x1 + x2) / 2
                parts.append(f'<path d="M{x1},{y1} C{mx},{y1} {mx},{y2} {x2},{y2}" '
                             f'style="fill:none;stroke:var(--ink-3);stroke-width:1.2" marker-end="url(#arr)"/>')
    for n, (x, y) in pos.items():
        nd = nodes[n]
        dash = "stroke-dasharray:4 3;" if nd["ext"] else ""
        fill = "var(--surface)" if nd["ext"] else "var(--accent-soft)"
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" '
                     f'style="fill:{fill};stroke:var(--accent);{dash}stroke-width:1.2"/>')
        parts.append(f'<text x="{x + 8}" y="{y + 17}" style="fill:var(--ink);font:600 12px var(--font-mono)">'
                     f'{e(n[:24])}</text>')
        parts.append(f'<text x="{x + 8}" y="{y + 33}" style="fill:var(--ink-3);font:11px var(--font-body)">'
                     f'{e(str(nd.get("type", ""))[:28])}</text>')
    parts.append("</svg>")
    return f'<div class="wrap">{"".join(parts)}</div>'


# ------------------------------------------------------------------ page
def nav_html(current, links):
    items = "\n".join(f'      <a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == current else ""}>{e(t)}</a>'
                      for h, t in links)
    return f'<nav aria-label="Trang">\n{items}\n    </nav>'


def target_nav(targets):
    return [("index.html", "Trang chủ")] + [(f"{slug(t)}.html", t) for t in targets]


JUMP_CSS = """
.objmap{max-width:none;display:block}
.jump{border-top:1px solid var(--rule);background:var(--surface)}
.jump .inner{max-width:1080px;margin:0 auto;padding:0.45rem clamp(1.1rem,3vw,2rem);display:flex;flex-wrap:wrap;gap:0.35rem}
.jump a{font-family:var(--font-body);font-size:var(--step--1);color:var(--ink-2);text-decoration:none;
  padding:0.28rem 0.7rem;border:1px solid var(--rule);border-radius:999px;background:var(--surface);white-space:nowrap}
.jump a:hover,.jump a:focus-visible{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
.jump a .n{font-family:var(--font-mono);color:var(--ink-3);margin-left:0.35rem}
.jump a .n.bad{color:var(--danger)}
section[id]{scroll-margin-top:8.5rem}
.facts .pill{white-space:normal;display:inline-block;max-width:100%;line-height:1.35}
.facts .v{min-width:0;overflow-wrap:anywhere}
.rec tr{position:relative}
.rec a.row{color:var(--accent);text-decoration:none;white-space:nowrap}
.rec a.row::after{content:"";position:absolute;inset:0}
.rec tbody tr:hover{background:var(--accent-soft);cursor:pointer}
.rec .more{font-size:var(--step--1);color:var(--accent);white-space:nowrap}
@media (max-width:640px){.jump .inner{flex-wrap:nowrap;overflow-x:auto}section[id]{scroll-margin-top:7rem}}
"""


def jump_html(buttons):
    """Row of section buttons inside the sticky top bar: [(anchor, label, count or None, bad?)]."""
    links = "".join(
        f'<a href="#{a}">{e(label)}'
        + (f'<span class="n{" bad" if bad else ""}">{e(n)}</span>' if n not in (None, "") else "") + "</a>"
        for a, label, n, bad in buttons)
    return f'  <nav class="jump" aria-label="Mục trong trang"><div class="inner">{links}</div></nav>\n'


def head_html(title, current, targets, buttons=None):
    return f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<link rel="stylesheet" href="{CSS}">
<style>{JUMP_CSS}</style>
</head>
<body>
<!-- GENERATED by .claude/scripts/handbook/render_target.py from artifacts/targets/*/handbook.json — edit the JSON, not this file -->
<div class="topbar">
  <div class="inner">
    <a class="home" href="index.html">{SITE_TITLE}</a>
    {nav_html(current, target_nav(targets))}
  </div>
{jump_html(buttons) if buttons else ""}</div>
'''


def atc_cell(entry):
    atc = entry.get("atc") or {}
    return pill("ok" if atc.get("result") == "0 findings" else ("wrn" if atc else "off"), atc.get("result", "chưa chạy"))


def detail_blocks(label, entry):
    """ATC, preview and test blocks of one version or one record -> (atc[], preview[], tests[])."""
    atc_b, pv_b, test_b = [], [], []
    atc = entry.get("atc") or {}
    if atc:
        fnd = atc.get("findings", [])
        body = table(["Object", "Priority", "Check", "Message", "Xử lý"],
                     [[f'<span class="mono">{e(f.get("object"))}</span>', e(f.get("priority")), e(f.get("check")),
                       e(f.get("message")), e(f.get("status"))] for f in fnd]) if fnd else "<p>0 finding.</p>"
        meta = " · ".join(e(x) for x in (atc.get("date"), atc.get("variant"), atc.get("scope")) if x)
        atc_b.append(f'<h3>{label} — ATC {meta}</h3>{body}')
    pv = entry.get("preview") or {}
    if pv:
        snap = entry.get("snapshot") or {}
        meta = f' · snapshot {e(snap.get("taken"))} ({len(snap.get("objects", {}))} object)' if snap else ""
        pv_b.append(
            f'<h3>{label} — preview {e(pv.get("date"))}{meta}</h3>' + table(
                ["Mục", "Trạng thái", "Bằng chứng / lý do"],
                [[e(PREVIEW_ITEMS.get(i.get("item"), i.get("item"))),
                  pill("ok", "đã làm") if i.get("status") == "done" else pill("wrn", "không làm được"),
                  f'<span class="mono">{e(i.get("evidence"))}</span>' + (f'<br>{e(i["note"])}' if i.get("note") else "")]
                 for i in pv.get("items", [])]))
    for a in entry.get("tests", []):
        cases = a.get("cases", [])
        cnt = {k: sum(1 for c in cases if c.get("result") == k) for k in ("PASS", "FAIL", "WAIT", "ACCEPTED")}
        head = (f'<h3>{label} — {e(a.get("title"))} — {cnt["PASS"]} PASS / {cnt["FAIL"]} FAIL'
                f'{" / " + str(cnt["WAIT"]) + " chờ user" if cnt["WAIT"] else ""}'
                f'{" / " + str(cnt["ACCEPTED"]) + " user-accepted" if cnt["ACCEPTED"] else ""}</h3>'
                f'<p>{e(a.get("summary"))}</p>')
        test_b.append(head + table(
            ["ID", "Nhóm", "Case", "Nguồn spec", "Input", "Mong đợi", "Thực tế", "Kết quả", "Evidence"],
            [[f'<span class="mono">{e(c.get("id"))}</span>', e(c.get("group")), e(c.get("case")), e(c.get("source")),
              e(c.get("input")), e(c.get("expected")), e(c.get("actual")), pill(c.get("result", "WAIT")),
              f'<span class="mono">{e(c.get("evidence"))}</span>'] for c in cases]))
    return atc_b, pv_b, test_b


def record_page_name(target, date):
    return f"{slug(target)}-kiem-tra-{date}.html"


def kinds_of(r):
    return ", ".join(r.get("kind")) if isinstance(r.get("kind"), list) else (r.get("kind") or "")


def test_cell(entry):
    cases = [c for a in entry.get("tests", []) for c in a.get("cases", [])]
    if not cases:
        return pill("off", "không có")
    n_fail = sum(1 for c in cases if c.get("result") == "FAIL")
    n_pass = sum(1 for c in cases if c.get("result") in ("PASS", "ACCEPTED"))
    return pill("dgr" if n_fail else "ok", f"{n_pass} PASS / {n_fail} FAIL")


def render_record(d, r, targets):
    """Detail page of one day of checks (records entry)."""
    t, day = d["target"], r.get("date", "")
    summary = r.get("summary", [])
    summary_html = ("<ul>" + "".join(f"<li>{e(s)}</li>" for s in summary) + "</ul>") if isinstance(summary, list) \
        else f"<p>{e(summary)}</p>"
    a, p, ts = detail_blocks(f"Ngày {e(day)}", r)
    snap = r.get("snapshot") or {}
    back = f"{slug(t)}.html#lich-su-kiem-tra"
    return head_html(f"{t} — kiểm tra {day} — {SITE_TITLE}", f"{slug(t)}.html", targets) + f'''
<div class="page">
  <header class="masthead">
    <p class="eyebrow"><a href="{back}">← {e(t)} · Lịch sử kiểm tra</a></p>
    <h1>{e(t)} — kiểm tra ngày {e(day)}</h1>
    <div class="facts">
      <div><span class="k">loại</span><span class="v">{e(kinds_of(r))}</span></div>
      <div><span class="k">áp dụng cho version</span><span class="v">{e(r.get("applies_to", "—"))}</span></div>
      <div><span class="k">kiểm thử</span><span class="v">{test_cell(r)}</span></div>
      <div><span class="k">ATC</span><span class="v">{atc_cell(r)}</span></div>
      <div><span class="k">snapshot</span><span class="v">{e(snap.get("dir", "—"))} ({len(snap.get("objects", {}))} object)</span></div>
    </div>
  </header>
  <section id="da-kiem-tra"><h2>Đã kiểm tra trong ngày</h2>{summary_html}</section>
  <section id="preview"><h2>Preview</h2>{"".join(p) or "<p>Không có preview.</p>"}</section>
  <section id="atc"><h2>ATC</h2>{"".join(a) or "<p>Không chạy ATC.</p>"}</section>
  <section id="kiem-thu"><h2>Kiểm thử</h2>{"".join(ts) or "<p>Không có test case.</p>"}</section>
  <footer><p><a href="{back}">← quay lại trang {e(t)}</a> · <span class="mono">artifacts/handbook_targets/{record_page_name(t, day)}</span>
    · nguồn <span class="mono">artifacts/targets/{e(t)}/handbook.json</span> (records, ngày {e(day)})</p></footer>
</div>
</body>
</html>
'''


def render(d, targets):
    t = d["target"]
    versions = d.get("versions", [])
    cur = versions[0] if versions else {}
    st = d.get("status", {})
    objects = d.get("objects", [])
    forms = d.get("forms", [])

    obj_rows = [[f'<span class="mono">{e(o["name"])}</span>', e(o.get("type")), e(o.get("role")),
                 e(", ".join(o.get("uses", [])))] for o in objects]
    so_do = (diagram(objects) + table(["Object", "Loại", "Vai trò", "Dùng"], obj_rows)) if objects \
        else "<p>Chưa có object nào được tạo.</p>"
    form_html = table(["Tên form", "Loại", "File", "Trạng thái"],
                      [[f'<span class="mono">{e(f["name"])}</span>', e(f.get("type")),
                        "<br>".join(f'<span class="mono">{e(x)}</span>' for x in f.get("files", [])),
                        e(f.get("status"))] for f in forms]) if forms else "<p>Không có form.</p>"

    ver_rows, atc_blocks, test_blocks, preview_blocks = [], [], [], []
    for v in versions:
        src = e(v.get("source"))
        if v.get("source") == EXTERNAL:
            src = pill("wrn", EXTERNAL) + (f'<br>{e(v["period"])}' if v.get("period") else "")
        ver_rows.append([f'<b>{e(v["version"])}</b>', e(v.get("date")), src,
                         "<br>".join(f"• {e(c)}" for c in v.get("changes", [])), atc_cell(v)])
        a, p, ts = detail_blocks(f'Version {e(v["version"])}', v)
        atc_blocks += a
        preview_blocks += p
        test_blocks += ts

    # records = checks of the target that changed no code, one entry per day — not function versions
    # one line per day on the main page; the day's detail lives on its own page (record_page)
    rec_rows = []
    for r in sorted(d.get("records", []), key=lambda r: r.get("date", ""), reverse=True):
        href = record_page_name(t, r.get("date", ""))
        rec_rows.append([f'<a class="row" href="{href}"><b>{e(r.get("date"))}</b></a>', e(kinds_of(r)),
                         e(r.get("applies_to")), test_cell(r), atc_cell(r),
                         f'<span class="more">Xem chi tiết →</span>'])
    records_html = ('<div class="rec">' + table(["Ngày", "Loại", "Áp dụng cho version", "Kiểm thử", "ATC", ""], rec_rows)
                    + "</div>") if rec_rows else "<p>Chưa có ngày kiểm tra nào.</p>"

    page = f"{slug(t)}.html"
    def fails(entries):
        return sum(1 for x in entries for a in x.get("tests", []) for c in a.get("cases", []) if c.get("result") == "FAIL")

    records = d.get("records", [])
    rec_fail = fails(records)
    buttons = [("muc-dich", "Mục đích", None, False),
               ("so-do", "Sơ đồ object", len(objects), False),
               ("form", "Form", len(forms), False),
               ("phien-ban", "Version", len(versions), False),
               ("atc", "ATC", len(atc_blocks) or None, False),
               ("preview", "Preview", len(preview_blocks) or None, False),
               ("kiem-thu", "Kiểm thử", (f"{fails(versions)} FAIL" if fails(versions) else len(test_blocks) or None),
                fails(versions) > 0),
               ("lich-su-kiem-tra", "Lịch sử kiểm tra",
                (f"{len(records)} ngày · {rec_fail} FAIL" if rec_fail else (f"{len(records)} ngày" if records else None)),
                rec_fail > 0)]
    return head_html(f"{t} — {SITE_TITLE}", page, targets, buttons) + f'''
<div class="page">
  <header class="masthead">
    <p class="eyebrow">{e(d.get("kind", ""))} · {e(d.get("module", ""))} · {e(t)}</p>
    <h1>{e(t)} — {e(d.get("title", ""))}</h1>
    <div class="facts">
      <div><span class="k">trạng thái</span><span class="v">{pill(st.get("pill", "off"), st.get("text", "—"))}</span></div>
      <div><span class="k">version</span><span class="v">{e(cur.get("version", "—"))}</span></div>
      <div><span class="k">cập nhật</span><span class="v">{e(d.get("updated", cur.get("date", "")))}</span></div>
      <div><span class="k">folder</span><span class="v">artifacts/targets/{e(t)}/</span></div>
    </div>
  </header>

  <section id="muc-dich"><h2>Mục đích</h2><p>{e(d.get("purpose", "—"))}</p></section>
  <section id="so-do"><h2>Sơ đồ object</h2>{so_do}</section>
  <section id="form"><h2>Form</h2>{form_html}</section>
  <section id="phien-ban"><h2>Version và thay đổi</h2>
    {table(["Version", "Ngày", "Nguồn", "Thay đổi", "ATC"], ver_rows) if ver_rows else "<p>Chưa có version.</p>"}</section>
  <section id="atc"><h2>Kết quả ATC theo version</h2>{"".join(atc_blocks) or "<p>Chưa chạy ATC.</p>"}</section>
  <section id="preview"><h2>Preview theo version</h2>{"".join(preview_blocks) or "<p>Chưa có preview.</p>"}</section>
  <section id="kiem-thu"><h2>Kiểm thử theo version</h2>{"".join(test_blocks) or "<p>Chưa có test case.</p>"}</section>
  <section id="lich-su-kiem-tra"><h2>Lịch sử kiểm tra hồ sơ</h2>
    <p>Mỗi ngày một dòng: các lần kiểm tra target không đổi code trong ngày (phân tích, preview, test lại, refresh) — không phải version của chức năng.</p>
    {records_html}</section>

  <footer><p><span class="mono">artifacts/handbook_targets/{page}</span> · nguồn <span class="mono">artifacts/targets/{e(t)}/handbook.json</span></p></footer>
</div>
</body>
</html>
'''


def index_html(targets, data):
    cards = "".join(
        f'\n      <a class="card" href="{slug(t)}.html">'
        f'<span class="pill {PILL.get(data[t].get("status", {}).get("pill", "off"), "pill-off")}">'
        f'{e(data[t].get("status", {}).get("text", "—"))}</span>'
        f'<span class="t">{e(t)} — {e(data[t].get("title", ""))}</span>'
        f'<span class="d">{e(data[t].get("kind", ""))} · {e(data[t].get("module", ""))} — {e(data[t].get("purpose", ""))}</span>'
        f'<span class="p">artifacts/targets/{e(t)}/ · {e(data[t].get("updated", ""))}</span></a>'
        for t in targets)
    return head_html(SITE_TITLE, "index.html", targets) + f'''
<div class="page">
  <header class="masthead">
    <p class="eyebrow">S/4HANA Public Cloud · mỗi báo cáo / chức năng một trang</p>
    <h1>{SITE_TITLE}</h1>
    <p class="standfirst">Mỗi trang sinh từ <code>artifacts/targets/&lt;TARGET&gt;/handbook.json</code>: mục đích, sơ đồ object,
      form, version, ATC, kiểm thử. Lối vào chi tiết của agent vẫn là <code>INDEX.md</code> của từng target.</p>
  </header>
  <section id="bao-cao"><h2>Báo cáo / chức năng ({len(targets)})</h2>
    <div class="cards">{cards or "<p>Chưa có target nào.</p>"}
    </div>
  </section>
  <footer><p><span class="mono">artifacts/handbook_targets/index.html</span> · sinh bởi render_target.py</p></footer>
</div>
</body>
</html>
'''


def sync_site(targets, data):
    (HBT / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HB / "assets" / "site.css", HBT / "assets" / "site.css")
    (HBT / "index.html").write_text(index_html(targets, data), encoding="utf-8")
    for f in HBT.glob("*.html"):
        s = f.read_text(encoding="utf-8")
        owner = f.name.split("-kiem-tra-")[0] + ".html" if "-kiem-tra-" in f.name else f.name  # day page → its target
        s2 = re.sub(r'<nav aria-label="Trang">.*?</nav>', lambda _: nav_html(owner, target_nav(targets)),
                    s, count=1, flags=re.S)
        if s2 != s:
            f.write_text(s2, encoding="utf-8")
    # workspace handbook: static nav only (one link to this site), no target cards, no target pages
    for f in HB.glob("*.html"):
        s = f.read_text(encoding="utf-8")
        if f.stem in {slug(t) for t in targets} and "GENERATED by .claude/scripts/handbook/render_target.py" in s:
            f.unlink()
            print(f"removed old target page {f.relative_to(ROOT)}")
            continue
        s2 = re.sub(r'<nav aria-label="Trang">.*?</nav>', lambda _: nav_html(f.name, STATIC_NAV), s, count=1, flags=re.S)
        s2 = re.sub(r"[ \t]*<!-- targets:start -->.*?<!-- targets:end -->\n*", "", s2, flags=re.S)
        if s2 != s:
            f.write_text(s2, encoding="utf-8")


def main(argv):
    all_json = sorted(TARGETS.glob("*/handbook.json"))
    data = {p.parent.name: json.loads(p.read_text(encoding="utf-8")) for p in all_json}
    targets = sorted(data)
    if not argv:
        sys.exit(__doc__)
    wanted = targets if argv[0] == "--all" else argv[:1]
    HBT.mkdir(parents=True, exist_ok=True)
    for t in wanted:
        if t not in data:
            sys.exit(f"no artifacts/targets/{t}/handbook.json")
        out = HBT / f"{slug(t)}.html"
        out.write_text(render(data[t], targets), encoding="utf-8")
        print(f"written {out.relative_to(ROOT)}")
        keep = set()
        for r in data[t].get("records", []):
            rp = HBT / record_page_name(t, r.get("date", ""))
            rp.write_text(render_record(data[t], r, targets), encoding="utf-8")
            keep.add(rp.name)
            print(f"written {rp.relative_to(ROOT)}")
        for old in HBT.glob(f"{slug(t)}-kiem-tra-*.html"):
            if old.name not in keep:
                old.unlink()
                print(f"removed {old.relative_to(ROOT)} (day no longer in records)")
    sync_site(targets, data)
    print(f"target index + nav synced ({len(targets)} target(s)); workspace handbook carries no target links")


if __name__ == "__main__":
    main(sys.argv[1:])
