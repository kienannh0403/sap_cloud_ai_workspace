"""render_target.py - build the handbook page of a report/function from its handbook.json.

    python .claude/scripts/handbook/render_target.py <TARGET>      # one target
    python .claude/scripts/handbook/render_target.py --all         # every artifacts/targets/*/handbook.json

Source : artifacts/targets/<TARGET>/handbook.json   (schema: .claude/common/handbook-target.md)
Output : artifacts/handbook/<target>.html          (<target> = lowercase, '_' -> '-')
Also   : rewrites the nav of every handbook page (static links + one link per target) and the
         generated "Báo cáo / chức năng" card block on index.html. Local page, no network, no JS.
"""
import json
import re
import sys
from html import escape
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
TARGETS = ROOT / "artifacts" / "targets"
HB = ROOT / "artifacts" / "handbook"
PILL = {"PASS": "pill-ok", "FAIL": "pill-dgr", "WAIT": "pill-wrn", "ACCEPTED": "pill-off",
        "ok": "pill-ok", "wrn": "pill-wrn", "dgr": "pill-dgr", "acc": "pill-acc", "off": "pill-off"}
EXTERNAL = "sửa ngoài workspace"
PREVIEW_ITEMS = {"handbook": "Trang handbook", "test": "Chạy thử báo cáo", "atc": "ATC toàn target",
                 "index": "INDEX.md", "notes": "Notes", "snapshot": "Snapshot source", "objects": "Object liên quan"}
RESULT_TEXT = {"PASS": "PASS", "FAIL": "FAIL", "WAIT": "chờ user", "ACCEPTED": "PASS — unverified, user-accepted"}
STATIC_NAV = [("index.html", "Trang chủ"), ("mcp.html", "MCP"), ("cds-catalog.html", "CDS released"),
              ("workspace-build.html", "Dựng workspace")]


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
def nav_html(current, targets):
    links = [STATIC_NAV[0]] + [(f"{slug(t)}.html", t) for t in targets] + STATIC_NAV[1:]
    items = "\n".join(f'      <a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == current else ""}>{e(t)}</a>'
                      for h, t in links)
    return f'<nav aria-label="Trang">\n{items}\n    </nav>'


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
        atc = v.get("atc") or {}
        atc_cell = pill("ok" if atc.get("result") == "0 findings" else ("wrn" if atc else "off"),
                       atc.get("result", "chưa chạy"))
        src = e(v.get("source"))
        if v.get("source") == EXTERNAL:
            src = pill("wrn", EXTERNAL) + (f'<br>{e(v["period"])}' if v.get("period") else "")
        ver_rows.append([f'<b>{e(v["version"])}</b>', e(v.get("date")), src,
                         "<br>".join(f"• {e(c)}" for c in v.get("changes", [])), atc_cell])
        if atc:
            fnd = atc.get("findings", [])
            body = table(["Object", "Priority", "Check", "Message", "Xử lý"],
                         [[f'<span class="mono">{e(f.get("object"))}</span>', e(f.get("priority")), e(f.get("check")),
                           e(f.get("message")), e(f.get("status"))] for f in fnd]) if fnd else "<p>0 finding.</p>"
            meta = " · ".join(e(x) for x in (atc.get("date"), atc.get("variant"), atc.get("scope")) if x)
            atc_blocks.append(f'<h3>Version {e(v["version"])} — ATC {meta}</h3>{body}')
        pv = v.get("preview") or {}
        if pv:
            snap = v.get("snapshot") or {}
            meta = f' · snapshot {e(snap.get("taken"))} ({len(snap.get("objects", {}))} object)' if snap else ""
            preview_blocks.append(
                f'<h3>Version {e(v["version"])} — preview {e(pv.get("date"))}{meta}</h3>' + table(
                    ["Mục", "Trạng thái", "Bằng chứng / lý do"],
                    [[e(PREVIEW_ITEMS.get(i.get("item"), i.get("item"))),
                      pill("ok", "đã làm") if i.get("status") == "done" else pill("wrn", "không làm được"),
                      f'<span class="mono">{e(i.get("evidence"))}</span>' + (f'<br>{e(i["note"])}' if i.get("note") else "")]
                     for i in pv.get("items", [])]))
        for a in v.get("tests", []):
            cases = a.get("cases", [])
            cnt = {k: sum(1 for c in cases if c.get("result") == k) for k in ("PASS", "FAIL", "WAIT", "ACCEPTED")}
            head = (f'<h3>Version {e(v["version"])} — {e(a.get("title"))} — {cnt["PASS"]} PASS / {cnt["FAIL"]} FAIL'
                    f'{" / " + str(cnt["WAIT"]) + " chờ user" if cnt["WAIT"] else ""}'
                    f'{" / " + str(cnt["ACCEPTED"]) + " user-accepted" if cnt["ACCEPTED"] else ""}</h3>'
                    f'<p>{e(a.get("summary"))}</p>')
            test_blocks.append(head + table(
                ["ID", "Nhóm", "Case", "Nguồn spec", "Input", "Mong đợi", "Thực tế", "Kết quả", "Evidence"],
                [[f'<span class="mono">{e(c.get("id"))}</span>', e(c.get("group")), e(c.get("case")), e(c.get("source")),
                  e(c.get("input")), e(c.get("expected")), e(c.get("actual")), pill(c.get("result", "WAIT")),
                  f'<span class="mono">{e(c.get("evidence"))}</span>'] for c in cases]))

    page = f"{slug(t)}.html"
    return f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t)} — Sổ tay ABAP_CLOUD_AI</title>
<link rel="stylesheet" href="assets/site.css">
<style>.objmap{{max-width:none;display:block}}</style>
</head>
<body>
<!-- GENERATED by .claude/scripts/handbook/render_target.py from artifacts/targets/{e(t)}/handbook.json — edit the JSON, not this file -->
<div class="topbar">
  <div class="inner">
    <a class="home" href="index.html">Sổ tay ABAP_CLOUD_AI</a>
    {nav_html(page, targets)}
  </div>
</div>

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
  <section id="kiem-thu"><h2>Kiểm thử</h2>{"".join(test_blocks) or "<p>Chưa có test case.</p>"}</section>

  <footer><p><span class="mono">artifacts/handbook/{page}</span> · nguồn <span class="mono">artifacts/targets/{e(t)}/handbook.json</span></p></footer>
</div>
</body>
</html>
'''


def sync_site(targets, data):
    for f in HB.glob("*.html"):
        s = f.read_text(encoding="utf-8")
        s2 = re.sub(r'<nav aria-label="Trang">.*?</nav>', lambda _: nav_html(f.name, targets), s, count=1, flags=re.S)
        if f.name == "index.html":
            cards = "".join(
                f'\n      <a class="card" href="{slug(t)}.html">'
                f'<span class="pill {PILL.get(data[t].get("status", {}).get("pill", "off"), "pill-off")}">'
                f'{e(data[t].get("status", {}).get("text", "—"))}</span>'
                f'<span class="t">{e(t)} — {e(data[t].get("title", ""))}</span>'
                f'<span class="d">{e(data[t].get("purpose", ""))}</span>'
                f'<span class="p">artifacts/targets/{e(t)}/ · {e(data[t].get("updated", ""))}</span></a>'
                for t in targets)
            block = (f'<!-- targets:start -->\n  <section id="bao-cao">\n    <h2>Báo cáo / chức năng</h2>\n'
                     f'    <div class="cards">{cards or "<p>Chưa có target nào.</p>"}\n    </div>\n  </section>\n'
                     f'  <!-- targets:end -->')
            if "<!-- targets:start -->" in s2:
                s2 = re.sub(r"<!-- targets:start -->.*?<!-- targets:end -->", lambda _: block, s2, flags=re.S)
            else:
                s2 = s2.replace('  <section id="tra-cuu">', f"  {block}\n\n  <section id=\"tra-cuu\">", 1)
        if s2 != s:
            f.write_text(s2, encoding="utf-8")


def main(argv):
    all_json = sorted(TARGETS.glob("*/handbook.json"))
    data = {p.parent.name: json.loads(p.read_text(encoding="utf-8")) for p in all_json}
    targets = sorted(data)
    if not argv:
        sys.exit(__doc__)
    wanted = targets if argv[0] == "--all" else argv[:1]
    for t in wanted:
        if t not in data:
            sys.exit(f"no artifacts/targets/{t}/handbook.json")
        out = HB / f"{slug(t)}.html"
        out.write_text(render(data[t], targets), encoding="utf-8")
        print(f"written {out.relative_to(ROOT)}")
    sync_site(targets, data)
    print(f"nav + index cards synced ({len(targets)} target(s))")


if __name__ == "__main__":
    main(sys.argv[1:])
