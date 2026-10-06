"""atc_check.py - token-lean ATC + inactive-object checks for activation-guard (Gates 2 and 4).

ATC runs on SAP exactly as through the MCP tool (same ADT API, the system's check variant); only the OUTPUT is
condensed: the full result goes to a JSON file in the target's build/atc/ folder, the console gets one line per
object plus full details of NEW findings only.

  python .claude/scripts/atc/atc_check.py baseline --target ZMA01 --label getdata --uri /sap/bc/adt/oo/classes/zcl_x
  python .claude/scripts/atc/atc_check.py run      --target ZMA01 --label getdata --uri /sap/bc/adt/oo/classes/zcl_x
  python .claude/scripts/atc/atc_check.py run      --target ZMA01 --label pkg --uri /sap/bc/adt/packages/zma01 --baseline <file.json>
  python .claude/scripts/atc/atc_check.py run      --target ZMA01 --label newview --uri ... --new      (new object: baseline = empty)
  python .claude/scripts/atc/atc_check.py inactive --names ZCL_GETDATA_PBCP,ZMA_I_*

--uri may repeat (several objects in one ATC run). Server: sap_cloud_dev from .mcp.json (URL, client, cookie file);
--server picks another entry. Git Bash rewrites "/sap/..." into a Windows path: the script repairs it.

Comparison (Gate 4 "zero NEW findings"): a finding's signature is object type + name + check + message id + message
text, WITHOUT the line number, counted as a multiset - so a pre-existing finding that only moved because lines
were inserted is "kept", a second occurrence of the same signature is "new". Baseline = --baseline file, else the
newest "<label>_baseline" file of that target, else (with --new) empty. No baseline and no --new -> exit 3.

Exit: 0 no new finding / nothing inactive · 1 NEW findings / watched object inactive · 2 SAP or session error
(login page, HTTP error, no result) - never read as a pass · 3 usage error.
"""
import argparse
import collections
import datetime
import fnmatch
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("python package 'requests' missing - pip install requests (exit 2)")

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
NS = {"atcworklist": "http://www.sap.com/adt/atc/worklist", "atcobject": "http://www.sap.com/adt/atc/object",
      "atcfinding": "http://www.sap.com/adt/atc/finding", "adtcore": "http://www.sap.com/adt/core"}
PRIO = {"1": "error", "2": "warning", "3": "info"}


def fail(code, msg):
    print(msg)
    sys.exit(code)


def fix_uri(u):
    return u[u.index("/sap/"):] if "/sap/" in u else u


def session(server):
    cfg = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"].get(server)
    if not cfg:
        fail(3, f"server '{server}' not in .mcp.json")
    env = cfg.get("env", {})
    host, client = env.get("SAP_URL", "").rstrip("/"), env.get("SAP_CLIENT", "")
    cookie_file = Path(env.get("SAP_COOKIE_FILE", ""))
    if not cookie_file.is_absolute():
        cookie_file = ROOT / cookie_file
    if not (host and client and cookie_file.is_file()):
        fail(2, f"server '{server}': SAP_URL / SAP_CLIENT / SAP_COOKIE_FILE incomplete in .mcp.json")
    s = requests.Session()
    for line in cookie_file.read_text(encoding="utf-8").splitlines():
        if not line or (line.startswith("#") and not line.startswith("#HttpOnly_")):
            continue
        f = line.replace("#HttpOnly_", "").split("\t")
        if len(f) >= 7:
            s.cookies.set(f[5], f[6], domain=f[0].lstrip("."), path=f[2])
    params = {"sap-client": client}
    r = s.get(host + "/sap/bc/adt/discovery", params=params, headers={"X-CSRF-Token": "Fetch", "Accept": "*/*"}, timeout=60)
    if r.status_code != 200 or "html" in r.headers.get("content-type", ""):
        fail(2, f"SAP session not valid on {server} (HTTP {r.status_code}, {r.headers.get('content-type')}) - refresh the cookie (skill sap-doctor)")
    s.headers["X-CSRF-Token"] = r.headers.get("x-csrf-token", "")
    return s, host, params


def check_xml(r, what):
    if r.status_code >= 300 or "html" in r.headers.get("content-type", ""):
        fail(2, f"{what}: HTTP {r.status_code} {r.headers.get('content-type')} {r.text[:300]}")


def run_atc(s, host, params, uris):
    r = s.get(host + "/sap/bc/adt/atc/customizing", params=params, headers={"Accept": "application/xml"}, timeout=60)
    check_xml(r, "atc customizing")
    variant = (re.findall(r'name="systemCheckVariant" value="([^"]*)"', r.text) or [""])[0]
    if not variant:
        fail(2, "no system check variant in ATC customizing")
    r = s.post(host + "/sap/bc/adt/atc/worklists", params={**params, "checkVariant": variant}, headers={"Accept": "text/plain"}, timeout=60)
    if r.status_code >= 300:
        fail(2, f"create worklist: HTTP {r.status_code} {r.text[:300]}")
    wl = r.text.strip()
    refs = "".join(f'<adtcore:objectReference adtcore:uri="{fix_uri(u)}"/>' for u in uris)
    body = ('<?xml version="1.0" encoding="UTF-8"?><atc:run maximumVerdicts="10000" xmlns:atc="http://www.sap.com/adt/atc">'
            '<objectSets xmlns:adtcore="http://www.sap.com/adt/core"><objectSet kind="inclusive"><adtcore:objectReferences>'
            f'{refs}</adtcore:objectReferences></objectSet></objectSets></atc:run>')
    r = s.post(host + "/sap/bc/adt/atc/runs", params={**params, "worklistId": wl}, data=body.encode(),
               headers={"Content-Type": "application/xml", "Accept": "application/xml"}, timeout=600)
    check_xml(r, "atc run")
    r = s.get(host + f"/sap/bc/adt/atc/worklists/{wl}", params={**params, "includeExemptedFindings": "false"},
              headers={"Accept": "application/atc.worklist.v1+xml"}, timeout=120)
    check_xml(r, "atc worklist")
    root = ET.fromstring(r.content)
    findings = []
    for obj in root.iter(f"{{{NS['atcobject']}}}object"):
        otype = obj.get(f"{{{NS['adtcore']}}}type", "")
        oname = obj.get(f"{{{NS['adtcore']}}}name", "")
        for f in obj.iter(f"{{{NS['atcfinding']}}}finding"):
            g = lambda k: f.get(f"{{{NS['atcfinding']}}}{k}", "")
            loc = g("location")
            m = re.search(r"start=(\d+)", loc)
            findings.append({"object": f"{otype} {oname}", "priority": g("priority"), "check": g("checkTitle"),
                             "messageId": g("messageId"), "message": g("messageTitle"),
                             "line": int(m.group(1)) if m else None, "location": loc})
    return variant, wl, findings


def sig(f):
    return f"{f['object']}|{f['check']}|{f['messageId']}|{f['message']}"


def summary_line(name, items):
    c = collections.Counter(PRIO.get(f["priority"], "info") for f in items)
    return f"{name}: {len(items)} findings ({c['error']} error, {c['warning']} warning, {c['info']} info)"


def cmd_atc(a, is_baseline):
    tdir = ROOT / "artifacts" / "targets" / a.target
    if not tdir.is_dir():
        fail(3, f"no target folder {tdir.relative_to(ROOT)}")
    out_dir = tdir / "build" / "atc"
    out_dir.mkdir(parents=True, exist_ok=True)
    s, host, params = session(a.server)
    variant, wl, findings = run_atc(s, host, params, a.uri)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    kind = "baseline" if is_baseline else "run"
    out = out_dir / f"{stamp}_{a.label}_{kind}.json"
    record = {"label": a.label, "kind": kind, "taken_at": stamp, "server": a.server, "variant": variant,
              "worklist": wl, "uris": [fix_uri(u) for u in a.uri], "findings": findings}
    out.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    by_obj = collections.defaultdict(list)
    for f in findings:
        by_obj[f["object"]].append(f)
    print(f"ATC {variant} · {', '.join(record['uris'])} · saved {out.relative_to(ROOT).as_posix()}")
    if is_baseline:
        for o in sorted(by_obj):
            print("  " + summary_line(o, by_obj[o]))
        print(f"  TOTAL {summary_line('', findings)[2:]}")
        return 0
    # comparison
    if a.baseline:
        bfile = Path(a.baseline) if Path(a.baseline).is_absolute() else ROOT / a.baseline
        base = json.loads(bfile.read_text(encoding="utf-8"))["findings"]
        bname = bfile.relative_to(ROOT).as_posix() if bfile.is_relative_to(ROOT) else str(bfile)
    else:
        cands = sorted(out_dir.glob(f"*_{a.label}_baseline.json"))
        if cands:
            base = json.loads(cands[-1].read_text(encoding="utf-8"))["findings"]
            bname = cands[-1].relative_to(ROOT).as_posix()
        elif a.new:
            base, bname = [], "empty (--new object)"
        else:
            fail(3, f"no baseline for label '{a.label}': run 'baseline' before the change, pass --baseline <file>, or --new")
    now_c, base_c = collections.Counter(map(sig, findings)), collections.Counter(map(sig, base))
    new_c, gone_c = now_c - base_c, base_c - now_c
    base_by_obj = collections.defaultdict(list)
    for f in base:
        base_by_obj[f["object"]].append(f)
    print(f"  baseline: {bname}")
    for o in sorted(set(by_obj) | set(base_by_obj)):
        n_new = sum(v for k, v in new_c.items() if k.startswith(o + "|"))
        n_gone = sum(v for k, v in gone_c.items() if k.startswith(o + "|"))
        print(f"  {summary_line(o, by_obj.get(o, []))} · baseline {len(base_by_obj.get(o, []))} · NEW {n_new} · gone {n_gone}")
    total_new = sum(new_c.values())
    print(f"  TOTAL {len(findings)} · baseline {len(base)} · NEW {total_new} · gone {sum(gone_c.values())}")
    if total_new:
        print("  NEW findings (Gate 4 FAILS until fixed or accepted by the user in writing):")
        left = collections.Counter(new_c)
        for f in findings:
            k = sig(f)
            if left[k] > 0:
                left[k] -= 1
                print(f"    - {f['object']} line {f['line']} · P{f['priority']} {f['check']} {f['messageId']}: {f['message']}")
        return 1
    return 0


def cmd_inactive(a):
    s, host, params = session(a.server)
    r = s.get(host + "/sap/bc/adt/activation/inactiveobjects", params=params, headers={"Accept": "application/xml"}, timeout=60)
    check_xml(r, "inactive objects")
    names = sorted(set(re.findall(r'adtcore:name="([^"]+)"', r.text)))
    pats = [p.strip().upper() for p in a.names.split(",") if p.strip()]
    hit = [n for n in names if any(fnmatch.fnmatch(n.strip().upper(), p) for p in pats)]
    print(f"inactive objects on {a.server}: {len(names)} in total · watched {', '.join(pats)} → {len(hit)} inactive"
          + (": " + ", ".join(hit) if hit else ""))
    return 1 if hit else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("baseline", "run"):
        p = sub.add_parser(name)
        p.add_argument("--target", required=True)
        p.add_argument("--label", required=True, help="short name of the checked object/set, ties a run to its baseline")
        p.add_argument("--uri", action="append", required=True)
        p.add_argument("--server", default="sap_cloud_dev")
        if name == "run":
            p.add_argument("--baseline")
            p.add_argument("--new", action="store_true", help="new object: empty baseline")
    p = sub.add_parser("inactive")
    p.add_argument("--names", required=True, help="comma list, * wildcard")
    p.add_argument("--server", default="sap_cloud_dev")
    a = ap.parse_args()
    if a.cmd == "inactive":
        sys.exit(cmd_inactive(a))
    sys.exit(cmd_atc(a, a.cmd == "baseline"))


if __name__ == "__main__":
    main()
