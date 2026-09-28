"""build_z_catalog.py - inventory of the Z/Y objects in SAP packages, for reuse (skill z-object-catalog).

    python .claude/scripts/z_catalog/build_z_catalog.py <PKG> [<PKG> ...] [--server sap_cloud_dev] [--no-recurse]
    python .claude/scripts/z_catalog/build_z_catalog.py --from-xml <PKG>=<file.xml> [...]     # offline / test

Reads each package (and its sub-packages, recursively) with the ADT repository node structure
(POST /sap/bc/adt/repository/nodestructure?parent_type=DEVC/K&parent_name=<PKG>) using the server's cookie file
from .mcp.json. Read-only: one CSRF fetch + one POST per package, no data query, no write.
Output (artifacts/system_analysis/Z_OBJECT_CATALOG/):
  objects.csv   package, type, name, description, reuse_group     (merged: a re-scan replaces only the scanned packages)
  INDEX.md      counts per package / type, scan date, the reuse groups
Reuse groups: ddic-type (DOMA, DTEL), ddic-table (TABL, structures), cds (DDLS), class (CLAS, INTF), message (MSAG),
number-range (NROB), service (SRVD, SRVB), behavior (BDEF), other.
"""
import csv
import datetime
import http.cookiejar
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "artifacts" / "system_analysis" / "Z_OBJECT_CATALOG"
FIELDS = ["package", "type", "name", "description", "reuse_group"]
GROUPS = {"DOMA": "ddic-type", "DTEL": "ddic-type", "TABL": "ddic-table", "TTYP": "ddic-table",
          "DDLS": "cds", "DCLS": "cds", "DDLX": "cds", "CLAS": "class", "INTF": "class", "MSAG": "message",
          "NROB": "number-range", "SRVD": "service", "SRVB": "service", "BDEF": "behavior"}


def fail(msg):
    print(msg)
    sys.exit(2)


def group_of(obj_type):
    return GROUPS.get(obj_type.split("/")[0], "other")


def parse_nodes(xml_text):
    """Return [(type, name, description)] from a nodestructure response (namespace-agnostic).
    ADT answers an empty body for a package with no objects and no sub-packages."""
    if not xml_text.strip():
        return []
    tree = ET.fromstring(xml_text)
    rows = []
    for node in tree.iter():
        if node.tag.split("}")[-1] != "SEU_ADT_REPOSITORY_OBJ_NODE":
            continue
        f = {c.tag.split("}")[-1]: (c.text or "").strip() for c in node}
        if f.get("OBJECT_NAME") and f.get("OBJECT_TYPE"):
            rows.append((f["OBJECT_TYPE"], f["OBJECT_NAME"], f.get("DESCRIPTION", "")))
    return rows


def load_netscape_cookies(path):
    """Lenient Netscape cookie-file reader. vsp writes domains without a leading dot but with the
    include-subdomains flag TRUE, which http.cookiejar.MozillaCookieJar rejects as invalid."""
    jar = http.cookiejar.CookieJar()
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("#HttpOnly_"):
            line = line[len("#HttpOnly_"):]
        elif not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 7:
            continue
        domain, _, cpath, secure, expires, name, value = parts
        jar.set_cookie(http.cookiejar.Cookie(
            0, name, value, None, False, domain.lstrip("."), True, False, cpath, True,
            secure.upper() == "TRUE", int(expires) if expires.isdigit() and int(expires) > 0 else None,
            False, None, None, {}))
    return jar


class Adt:
    def __init__(self, server):
        cfg_path = ROOT / ".mcp.json"
        if not cfg_path.is_file():
            fail("no .mcp.json in the workspace root")
        env = (json.loads(cfg_path.read_text(encoding="utf-8")).get("mcpServers", {}).get(server) or {}).get("env", {})
        if not env.get("SAP_URL") or not env.get("SAP_COOKIE_FILE"):
            fail(f"server {server}: no SAP_URL / SAP_COOKIE_FILE in .mcp.json")
        self.url, self.client = env["SAP_URL"].rstrip("/"), env.get("SAP_CLIENT", "")
        try:
            jar = load_netscape_cookies(env["SAP_COOKIE_FILE"])
        except OSError as exc:
            fail(f"cannot load cookie file of {server}: {exc}")
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        req = urllib.request.Request(self._u("/sap/bc/adt/discovery"), headers={"X-CSRF-Token": "Fetch", "Accept": "*/*"})
        with self.opener.open(req, timeout=30) as resp:
            if "atomsvc" not in resp.headers.get("Content-Type", ""):
                fail(f"server {server}: cookie rejected (got {resp.headers.get('Content-Type')}) - run skill sap-doctor")
            self.token = resp.headers.get("x-csrf-token", "")

    def _u(self, path, **query):
        if self.client:
            query["sap-client"] = self.client
        return f"{self.url}{path}?{urllib.parse.urlencode(query, safe='/*')}"

    def package_nodes(self, pkg):
        req = urllib.request.Request(
            self._u("/sap/bc/adt/repository/nodestructure", parent_type="DEVC/K", parent_name=pkg,
                    withShortDescriptions="true"),
            data=b"", method="POST", headers={"X-CSRF-Token": self.token, "Accept": "*/*"})
        with self.opener.open(req, timeout=60) as resp:
            return resp.read().decode("utf-8", errors="replace")


def scan(roots, fetch, recurse):
    seen, rows, queue = set(), [], [r.upper() for r in roots]
    while queue:
        pkg = queue.pop(0)
        if pkg in seen:
            continue
        seen.add(pkg)
        for obj_type, name, desc in parse_nodes(fetch(pkg)):
            if obj_type.startswith("DEVC"):
                if recurse and name.upper() not in seen:
                    queue.append(name.upper())
                continue
            if name[:1].upper() in ("Z", "Y", "/"):
                rows.append({"package": pkg, "type": obj_type, "name": name, "description": desc,
                             "reuse_group": group_of(obj_type)})
    return seen, rows


def write(scanned, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "objects.csv"
    keep = []
    if csv_path.is_file():
        with csv_path.open(encoding="utf-8", newline="") as fh:
            keep = [r for r in csv.DictReader(fh) if r["package"] not in scanned]
    allrows = sorted(keep + rows, key=lambda r: (r["package"], r["type"], r["name"]))
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, FIELDS)
        w.writeheader()
        w.writerows(allrows)

    today = datetime.date.today().isoformat()
    state_path = OUT / "scan_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.is_file() else {}
    state.update({p: today for p in scanned})
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    pkgs = sorted({r["package"] for r in allrows} | set(state))
    by_group = {}
    for r in allrows:
        by_group.setdefault(r["reuse_group"], []).append(r)
    lines = ["# Z object catalog - reuse inventory", "",
             "Generated by `.claude/scripts/z_catalog/build_z_catalog.py` - do not edit by hand; re-scan instead.",
             "Use: skill `z-object-catalog`. A hit is a CANDIDATE: read its real source/definition on SAP before reusing (rule §2).",
             "", f"{len(allrows)} object(s) in {len(pkgs)} package(s).", "",
             "| Package | Objects | Last scan |", "|---|---|---|"]
    lines += [f"| {p} | {sum(1 for r in allrows if r['package'] == p)} | {state.get(p, '-')} |" for p in pkgs]
    lines += ["", "| Reuse group | Objects |", "|---|---|"]
    lines += [f"| {g} | {len(v)} |" for g, v in sorted(by_group.items())]
    lines += ["", "Full list: `objects.csv` (package, type, name, description, reuse_group).", ""]
    (OUT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"written {len(rows)} object(s) from {len(scanned)} package(s); catalog now {len(allrows)} object(s) -> "
          f"{OUT.relative_to(ROOT).as_posix()}/")


def main(argv):
    if not argv:
        fail(__doc__)
    recurse, server, xml_map, roots = True, None, {}, []
    it = iter(argv)
    for a in it:
        if a == "--no-recurse":
            recurse = False
        elif a == "--server":
            server = next(it, None)
        elif a == "--from-xml":
            spec = next(it, "")
            pkg, _, file = spec.partition("=")
            xml_map[pkg.upper()] = Path(file).read_text(encoding="utf-8")
            roots.append(pkg)
        elif a.startswith("-"):
            fail(f"unknown option {a}\n{__doc__}")
        else:
            roots.append(a)
    if xml_map:
        fetch = lambda p: xml_map.get(p, "<root/>")
    else:
        if not server:
            m = re.search(r"^WRITE_SERVERS=([^,\s]+)", (ROOT / ".claude/common/system-config.md").read_text(encoding="utf-8"), re.M)
            server = m.group(1) if m else "sap_cloud_dev"
        fetch = Adt(server).package_nodes
    scanned, rows = scan(roots, fetch, recurse)
    write(scanned, rows)


if __name__ == "__main__":
    main(sys.argv[1:])
