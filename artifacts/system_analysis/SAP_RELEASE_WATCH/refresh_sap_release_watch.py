"""Watch what SAP releases for S/4HANA Cloud Public Edition and keep local snapshots + a changelog.

Run from the workspace root:
    python -X utf8 artifacts/system_analysis/SAP_RELEASE_WATCH/refresh_sap_release_watch.py --check  # ~2 s, dates only
    python -X utf8 artifacts/system_analysis/SAP_RELEASE_WATCH/refresh_sap_release_watch.py          # refresh what changed
    python -X utf8 artifacts/system_analysis/SAP_RELEASE_WATCH/refresh_sap_release_watch.py --force  # refresh both sources

Sources
  A. Released objects (every type: CDS, class, interface, BDEF, BAdI, table, data element, auth object...):
     github.com/SAP/abap-atc-cr-cv-s4hc src/objectReleaseInfoLatest.json — the list ATC checks ABAP Cloud code against.
     -> released_objects/objects.csv, released_objects/summary.md; also triggers the CDS catalog refresh
        (../CDS_RELEASED_CATALOG/refresh_sap_official.py).
  B. SAP Business Accelerator Hub (api.sap.com), every SAP-owned "... SAP S/4HANA Cloud Public Edition" content package:
     APIs (OData V2/V4, SOAP, REST), business events, BAdIs, BO interfaces, CDS views, iFlows.
     -> api_hub/artifacts.csv, api_hub/summary.md
Every refresh appends to changelog.md and writes the full diff to changes/<date>_<source>.csv.
Descriptions of released classes / interfaces / BDEFs are read from tenant 080 (ADT quickSearch) into
released_objects/descriptions_080.json — only for names that have none yet.

Exit codes (--check): 0 = nothing new, 10 = something new (message on stdout), 2 = a source could not be reached.
"""
import argparse
import collections
import csv
import datetime
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

OUT = "artifacts/system_analysis/SAP_RELEASE_WATCH"
STATE = os.path.join(OUT, "state.json")
CHANGELOG = os.path.join(OUT, "changelog.md")
OBJ_DIR = os.path.join(OUT, "released_objects")
HUB_DIR = os.path.join(OUT, "api_hub")
CHG_DIR = os.path.join(OUT, "changes")
OBJ_CSV = os.path.join(OBJ_DIR, "objects.csv")
OBJ_DESC = os.path.join(OBJ_DIR, "descriptions_080.json")
HUB_CSV = os.path.join(HUB_DIR, "artifacts.csv")
CDS_REFRESH = "artifacts/system_analysis/CDS_RELEASED_CATALOG/refresh_sap_official.py"

REPO_PATH = "src/objectReleaseInfoLatest.json"
COMMITS_API = f"https://api.github.com/repos/SAP/abap-atc-cr-cv-s4hc/commits?path={REPO_PATH}&per_page=1"
RAW_URL = f"https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/{REPO_PATH}"
HUB = "https://api.sap.com/odata/1.0/catalog.svc"
HUB_MAIN_PACKAGE = "SAPS4HANACloud"
HUB_PACKAGE_RX = re.compile(r"^(SAPS4HANACloud|S4HANACloud)")  # SAP-owned Public Edition packages
HUB_VERSION_RX = re.compile(r"^\d{4}")                          # release-versioned (2608, 2608.1...), not partner 1.0.x
ADT_SEARCH = "https://my437569.s4hana.cloud.sap/sap/bc/adt/repository/informationsystem/search"
COOKIE_FILE = "tools/vsp/cookies_dev.txt"
DESC_TYPES = ("CLAS", "INTF", "BDEF")  # released types worth a description from 080
MAX_RESULTS = 20000
TODAY = datetime.date.today().isoformat()

OBJ_COLS = ["type", "object_type", "name", "state", "application_component", "software_component", "successors",
            "description"]
HUB_COLS = ["type", "sub_type", "name", "display_name", "state", "version", "package", "modified", "description"]
TYPE_LABEL = {
    "DDLS": "CDS view", "CLAS": "Class", "INTF": "Interface", "BDEF": "Behavior definition (RAP BO)",
    "ENHS": "BAdI (enhancement spot)", "TABL": "Table / structure", "DTEL": "Data element", "DOMA": "Domain",
    "TTYP": "Table type", "FUGR": "Function module", "SUSO": "Authorization object", "SIA2": "IAM app template",
    "RONT": "RAP object node type", "NONT": "Non-RAP node type", "CHKO": "API check object", "CHKC": "Check category",
    "CHKV": "Check variant", "DRTY": "Dependency rule type", "SMTG": "Email template", "XSLT": "Transformation",
    "SAJC": "Application job catalog", "SAJT": "Application job template", "SCO2": "Communication scenario",
}


# ---------------------------------------------------------------- helpers
def fetch(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "sap-release-watch", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def hub_json(path, timeout=300):
    sep = "&" if "?" in path else "?"
    return json.loads(fetch(f"{HUB}/{path}{sep}$format=json", timeout=timeout))["d"]


def hub_date(value):
    m = re.search(r"\d+", value or "")
    return datetime.datetime.fromtimestamp(int(m.group(0)) / 1000, datetime.UTC).date().isoformat() if m else ""


def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_state(state):
    state["checked"] = TODAY
    with open(STATE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=1, sort_keys=True)


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, rows, cols):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def diff(old_rows, new_rows, key, watch):
    """Rows added / removed / changed in one of the `watch` columns, as change records."""
    old = {key(r): r for r in old_rows}
    new = {key(r): r for r in new_rows}
    out = []
    for k in sorted(new.keys() - old.keys()):
        out.append({"change": "added", **new[k]})
    for k in sorted(old.keys() - new.keys()):
        out.append({"change": "removed", **old[k]})
    for k in sorted(new.keys() & old.keys()):
        moved = [f"{c}: {old[k].get(c, '')} -> {new[k].get(c, '')}" for c in watch
                 if (old[k].get(c) or "") != (new[k].get(c) or "")]
        if moved:
            out.append({"change": "changed", "detail": "; ".join(moved), **new[k]})
    return out


def cookie_header():
    pairs = []
    with open(COOKIE_FILE, encoding="utf-8") as fh:
        for line in fh:
            cols = line.rstrip("\r\n").split("\t")
            if len(cols) >= 7 and not line.startswith("# "):
                pairs.append(f"{cols[5]}={cols[6]}")
    return "; ".join(pairs)


def read_descriptions_080(tadir, names):
    """{name: description} for `names` of one TADIR type, one quickSearch per 4-char prefix (split when capped)."""
    headers = {"Cookie": cookie_header(), "Accept": "*/*"}
    rx = re.compile(r'adtcore:type="' + tadir + r'/[^"]*" adtcore:name="([^"]+)"'
                    r'(?: adtcore:packageName="[^"]*")?(?: adtcore:description="([^"]*)")?')
    found = {}

    def walk(prefix):
        query = urllib.parse.urlencode({"operation": "quickSearch", "query": prefix + "*", "objectType": tadir,
                                        "maxResults": MAX_RESULTS, "sap-client": "080"}, safe="*")
        text = fetch(f"{ADT_SEARCH}?{query}", headers, timeout=120).decode("utf-8")
        if "<html" in text[:500].lower():
            raise RuntimeError("080 cookie expired (login page returned)")
        hits = rx.findall(text)
        if len(hits) >= MAX_RESULTS:
            for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_/":
                walk(prefix + ch)
            return
        for name, desc in hits:
            found[name.upper()] = html.unescape(desc)

    for p in sorted({n[:4] for n in names}):
        walk(p)
    return {n: found[n] for n in names if n in found}


def short_list(names, limit=30):
    names = list(names)
    return ", ".join(names[:limit]) + (f" … (+{len(names) - limit})" if len(names) > limit else "")


# ---------------------------------------------------------------- source A: released objects
def remote_objects_date():
    commit = json.loads(fetch(COMMITS_API, timeout=15))[0]
    return commit["commit"]["committer"]["date"][:10], commit["commit"]["message"].splitlines()[0]


def refresh_objects(state, remote_date, remote_msg, log):
    raw = json.loads(fetch(RAW_URL, timeout=300))["objectReleaseInfo"]
    desc = {}
    if os.path.exists(OBJ_DESC):
        with open(OBJ_DESC, encoding="utf-8") as fh:
            desc = json.load(fh)
    rows = [{"type": o["tadirObject"], "object_type": o["objectType"], "name": o["objectKey"], "state": o["state"],
             "application_component": o.get("applicationComponent", ""),
             "software_component": o.get("softwareComponent", ""),
             "successors": "; ".join(s["objectKey"] for s in o.get("successors") or [])} for o in raw]

    need = collections.defaultdict(list)
    for r in rows:
        if r["type"] in DESC_TYPES and r["state"] == "released" and r["name"] not in desc.get(r["type"], {}):
            need[r["type"]].append(r["name"])
    desc_note = "no new class/interface/BDEF without description"
    if need:
        try:
            got = 0
            for tadir, names in need.items():
                d = read_descriptions_080(tadir, names)
                desc.setdefault(tadir, {}).update(d)
                got += len(d)
            os.makedirs(OBJ_DIR, exist_ok=True)
            with open(OBJ_DESC, "w", encoding="utf-8") as fh:
                json.dump(desc, fh, ensure_ascii=False, indent=0, sort_keys=True)
            desc_note = f"descriptions read on 080 for {got} of {sum(map(len, need.values()))} class/interface/BDEF"
        except Exception as exc:
            desc_note = f"descriptions NOT read ({exc}); refresh the 080 cookie and rerun with --force"
    for r in rows:
        r["description"] = desc.get(r["type"], {}).get(r["name"], "")
    rows.sort(key=lambda r: (r["type"], r["name"]))

    old = read_csv(OBJ_CSV)
    changes = diff(old, rows, key=lambda r: (r["type"], r["name"]), watch=["state", "successors"])
    write_csv(OBJ_CSV, rows, OBJ_COLS)
    write_summary_objects(rows, remote_date)

    if old:
        write_csv(os.path.join(CHG_DIR, f"{TODAY}_released_objects.csv"), changes, ["change", "detail"] + OBJ_COLS)
    log += [f"### Released objects — SAP update {remote_date} ({remote_msg})", ""]
    if not old:
        log += [f"- baseline: {len(rows)} objects, " + ", ".join(
            f"{t} {n}" for t, n in collections.Counter(r["type"] for r in rows if r["state"] == "released").most_common())
                + " released"]
    else:
        newly = collections.defaultdict(list)
        gone = collections.defaultdict(list)
        for c in changes:
            now_rel = c["state"] == "released" and c["change"] != "removed"
            if now_rel and (c["change"] == "added" or "state:" in c.get("detail", "")):
                newly[c["type"]].append(c["name"])
            elif not now_rel:
                gone[c["type"]].append(c["name"] + (f" → {c['successors']}" if c.get("successors") else ""))
        log.append(f"- newly released: {sum(map(len, newly.values()))}" if newly else "- newly released: 0")
        log += [f"  - {TYPE_LABEL.get(t, t)}: {short_list(v)}" for t, v in sorted(newly.items())]
        log.append(f"- deprecated / no longer released: {sum(map(len, gone.values()))}" if gone else
                   "- deprecated / no longer released: 0")
        log += [f"  - {TYPE_LABEL.get(t, t)}: {short_list(v)}" for t, v in sorted(gone.items())]
        log.append(f"- full diff: `changes/{TODAY}_released_objects.csv`")
    log += [f"- {desc_note}", ""]

    cds = subprocess.run([sys.executable, "-X", "utf8", CDS_REFRESH], capture_output=True, text=True)
    log += ["- " + (cds.stdout.strip().splitlines() or ["CDS catalog: (no output)"])[0]
            + ("" if cds.returncode == 0 else f" — FAILED: {cds.stderr.strip()[-300:]}"), ""]
    state["objects"] = {"sap_last_update": remote_date, "message": remote_msg, "downloaded": TODAY}


def write_summary_objects(rows, remote_date):
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        by[r["type"]][r["state"]] += 1
    lines = ["# Released objects — summary", "",
             f"Generated {TODAY} by `refresh_sap_release_watch.py` from SAP's `objectReleaseInfoLatest.json` "
             f"(SAP update {remote_date}). Full list: `objects.csv` (filter by `type`). Do not hand-edit.", "",
             "| Type | Meaning | released | deprecated | notToBeReleased |", "|---|---|---:|---:|---:|"]
    for t, c in sorted(by.items(), key=lambda x: -x[1]["released"]):
        lines.append(f"| {t} | {TYPE_LABEL.get(t, '')} | {c['released']} | {c['deprecated']} | {c['notToBeReleased']} |")
    lines += ["", "`deprecated` rows carry `successors` = what SAP wants used instead. CDS views have their own per-module "
              "catalog in `../CDS_RELEASED_CATALOG/`.", ""]
    with open(os.path.join(OBJ_DIR, "summary.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


# ---------------------------------------------------------------- source B: API Hub
def remote_hub_main():
    d = hub_json(f"ContentEntities.ContentPackages('{HUB_MAIN_PACKAGE}')", timeout=15)
    return d.get("Version", ""), hub_date(d.get("ModifiedAt"))


def refresh_hub(state, log):
    pkgs = hub_json("ContentEntities.ContentPackages?$select=TechnicalName,DisplayName,Version,ModifiedAt")["results"]
    pkgs = [p for p in pkgs if HUB_PACKAGE_RX.match(p["TechnicalName"]) and HUB_VERSION_RX.match(p.get("Version") or "")]
    rows = {}
    for p in pkgs:
        arts = hub_json(f"ContentEntities.ContentPackages('{p['TechnicalName']}')/Artifacts")["results"]
        for a in arts:
            rows.setdefault((a["Type"], a["Name"]), {
                "type": a["Type"], "sub_type": a.get("SubType") or "", "name": a["Name"],
                "display_name": a.get("DisplayName") or "", "state": a.get("State") or "",
                "version": a.get("Version") or "", "package": p["TechnicalName"], "modified": hub_date(a.get("ModifiedAt")),
                "description": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a.get("Description") or "")).strip()})
    rows = sorted(rows.values(), key=lambda r: (r["type"], r["name"]))

    old = read_csv(HUB_CSV)
    changes = diff(old, rows, key=lambda r: (r["type"], r["name"]), watch=["state", "version", "display_name"])
    write_csv(HUB_CSV, rows, HUB_COLS)
    write_summary_hub(rows, pkgs)
    main_version, main_modified = remote_hub_main()
    log += [f"### API Hub — package {HUB_MAIN_PACKAGE} version {main_version} (modified {main_modified})", ""]
    if not old:
        log.append(f"- baseline: {len(rows)} artifacts in {len(pkgs)} packages — " + ", ".join(
            f"{t} {n}" for t, n in collections.Counter(r["type"] for r in rows).most_common()))
    else:
        write_csv(os.path.join(CHG_DIR, f"{TODAY}_api_hub.csv"), changes, ["change", "detail"] + HUB_COLS)
        groups = collections.defaultdict(list)
        for c in changes:
            label = c["change"]
            if c["change"] == "changed" and "state:" in c.get("detail", ""):
                label = "state changed"
            elif c["change"] == "changed":
                label = "new version / renamed"
            groups[(label, c["type"])].append(f"{c['display_name'] or c['name']}")
        if not groups:
            log.append("- no artifact added, removed or changed")
        for (label, t), v in sorted(groups.items()):
            log.append(f"- {label} — {t}: {len(v)}: {short_list(v, 20)}")
        if changes:
            log.append(f"- full diff: `changes/{TODAY}_api_hub.csv`")
    log.append("")
    state["hub"] = {"main_version": main_version, "main_modified": main_modified,
                    "packages": {p["TechnicalName"]: p.get("Version") for p in pkgs}, "downloaded": TODAY}


def write_summary_hub(rows, pkgs):
    c = collections.Counter((r["type"], r["sub_type"], r["state"]) for r in rows)
    lines = ["# SAP Business Accelerator Hub — S/4HANA Cloud Public Edition", "",
             f"Generated {TODAY} by `refresh_sap_release_watch.py` from api.sap.com. Full list: `artifacts.csv`. "
             "Do not hand-edit.", "", "| Type | Sub type | State | Count |", "|---|---|---|---:|"]
    lines += [f"| {t} | {s} | {st} | {n} |" for (t, s, st), n in sorted(c.items())]
    lines += ["", "## Packages", "", "| Package | Version |", "|---|---|"]
    lines += [f"| {p['TechnicalName']} | {p.get('Version')} |" for p in sorted(pkgs, key=lambda p: p["TechnicalName"])]
    lines += ["", "`API` = OData V2/V4 / SOAP / REST service with its communication scenario on the Hub page; "
              "`Event` = business event; `BADI` = BAdI; `BOInterface` = released RAP BO interface; `CDSVIEW` = CDS view "
              "(incl. key-user / analytical); `IFlow` = integration flow.", ""]
    with open(os.path.join(HUB_DIR, "summary.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="only report whether a source has something new")
    ap.add_argument("--force", action="store_true", help="refresh both sources even when nothing looks new")
    args = ap.parse_args()
    state = load_state()

    news, unreachable = [], []
    obj_remote = hub_remote = None
    try:
        obj_remote = remote_objects_date()
        if obj_remote[0] > state.get("objects", {}).get("sap_last_update", ""):
            news.append(f"released-object list updated {obj_remote[0]} (local {state.get('objects', {}).get('sap_last_update')})")
    except Exception as exc:
        unreachable.append(f"GitHub ({exc})")
    try:
        hub_remote = remote_hub_main()
        local = state.get("hub", {})
        if hub_remote != (local.get("main_version"), local.get("main_modified")):
            news.append(f"API Hub package {HUB_MAIN_PACKAGE} {hub_remote[0]} modified {hub_remote[1]} "
                        f"(local {local.get('main_version')} / {local.get('main_modified')})")
    except Exception as exc:
        unreachable.append(f"API Hub ({exc})")

    if args.check:
        if news:
            new_release = hub_remote and hub_remote[0].split(".")[0] != (state.get("hub", {}).get("main_version") or "").split(".")[0]
            print("SAP release watch: " + "; ".join(news)
                  + (f". NEW SAP RELEASE {hub_remote[0].split('.')[0]}" if new_release else "")
                  + f". Refresh: python -X utf8 {OUT}/refresh_sap_release_watch.py")
            sys.exit(10)
        print("SAP release watch: nothing new" + (f" (unreachable: {'; '.join(unreachable)})" if unreachable else ""))
        sys.exit(2 if unreachable else 0)

    log = [f"## {TODAY}", ""]
    did = False
    if obj_remote and (args.force or obj_remote[0] > state.get("objects", {}).get("sap_last_update", "")):
        refresh_objects(state, *obj_remote, log)
        did = True
    if hub_remote and (args.force or hub_remote != (state.get("hub", {}).get("main_version"),
                                                    state.get("hub", {}).get("main_modified"))):
        refresh_hub(state, log)
        did = True
    if unreachable:
        log += [f"- unreachable: {'; '.join(unreachable)}", ""]
    save_state(state)
    if not did:
        print("SAP release watch: nothing new, nothing refreshed")
        return
    header = "" if os.path.exists(CHANGELOG) else (
        "# Changelog — SAP release watch (S/4HANA Cloud Public Edition)\n\n"
        "Newest at the bottom. Full diffs per run in `changes/`.\n\n")
    with open(CHANGELOG, "a", encoding="utf-8") as fh:
        fh.write(header + "\n".join(log) + "\n")
    print("\n".join(log))


if __name__ == "__main__":
    main()
