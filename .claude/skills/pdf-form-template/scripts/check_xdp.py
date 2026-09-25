"""check_xdp.py <form.xdp> <data.xml> - binding check for an XFA template against a sample data file.

Checks: both files are well-formed; every <bind match="dataRef"> resolves to at least one data node
(relative refs follow the enclosing subform's binding, $record.* from the data root); every leaf of the
data file is bound by some field. Exit 1 on an unresolved ref or an unbound leaf.
"""
import re
import sys

from lxml import etree

sys.stdout.reconfigure(encoding="utf-8")
T = "{http://www.xfa.org/schema/xfa-template/3.3/}"


def main(xdp_path, xml_path):
    tmpl = etree.parse(xdp_path).getroot().find(T + "template")
    tree = etree.parse(xml_path)
    data = tree.getroot()
    stats = {"ok": 0}
    missing, used = [], set()

    def plain(e):
        return re.sub(r"\[\d+\]", "", tree.getpath(e))

    def resolve(ctx, ref):
        if ref.startswith("$record."):
            ctx, ref = [data], ref[len("$record."):]
        else:
            ref = ref[2:]
        nodes = ctx
        for part in ref.split("."):
            nodes = [ch for n in nodes for ch in n if ch.tag == part.replace("[*]", "")]
        return nodes

    def walk(el, ctx, path):
        for ch in el:
            tag = ch.tag.replace(T, "") if isinstance(ch.tag, str) else ""
            if tag not in ("subform", "field", "pageSet", "pageArea"):
                continue
            b = ch.find(T + "bind")
            nctx, p = ctx, f"{path}/{ch.get('name')}"
            if b is not None and b.get("match") == "dataRef":
                nodes = resolve(ctx, b.get("ref"))
                if nodes:
                    stats["ok"] += 1
                    for n in nodes:
                        used.update(plain(x) for x in n.iter())
                else:
                    missing.append(f"{p} -> {b.get('ref')}")
                if tag == "subform":
                    nctx = nodes
            walk(ch, nctx, p)

    walk(tmpl.find(T + "subform"), [data], "")
    unbound = sorted({plain(e) for e in data.iter() if len(e) == 0} - used)
    print(f"check: fields={len(tmpl.findall('.//' + T + 'field'))} draws={len(tmpl.findall('.//' + T + 'draw'))} "
          f"dataRef resolved={stats['ok']} unresolved={len(missing)} unbound data leaves={len(unbound)}")
    for m in missing:
        print("  UNRESOLVED", m)
    for u in unbound:
        print("  UNBOUND   ", u)
    return 1 if missing or unbound else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
