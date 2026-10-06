"""Check SAP's official released-object list for a newer version and, if asked, refresh the CDS catalog.

Run from the workspace root:
    python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/refresh_sap_official.py --check   # only compare dates
    python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/refresh_sap_official.py           # refresh if newer
    python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/refresh_sap_official.py --force   # refresh anyway

Source: github.com/SAP/abap-atc-cr-cv-s4hc, src/objectReleaseInfoLatest.json (S/4HANA Cloud Public Edition).
Refresh = download + filter DDLS -> sap_official/objectReleaseInfo_DDLS.json, read descriptions of views not yet in
sap_official/descriptions_080.json from tenant 080 (ADT quickSearch, cookie tools/vsp/cookies_dev.txt), rebuild the
catalog with build_catalog.py, rebuild released_objects/ (classes, interfaces, BDEFs, BAdIs...) with
build_object_index.py, append what changed to sap_official/changelog.md.

Exit codes (--check): 0 = up to date, 10 = newer version available, 2 = could not reach GitHub.
"""
import argparse
import datetime
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

OUT = "artifacts/system_analysis/CDS_RELEASED_CATALOG"
SAP_DIR = os.path.join(OUT, "sap_official")
OFFICIAL = os.path.join(SAP_DIR, "objectReleaseInfo_DDLS.json")
DESC_080 = os.path.join(SAP_DIR, "descriptions_080.json")
CHANGELOG = os.path.join(SAP_DIR, "changelog.md")
REPO_PATH = "src/objectReleaseInfoLatest.json"
COMMITS_API = f"https://api.github.com/repos/SAP/abap-atc-cr-cv-s4hc/commits?path={REPO_PATH}&per_page=1"
RAW_URL = f"https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/{REPO_PATH}"
SOURCE_URL = f"https://github.com/SAP/abap-atc-cr-cv-s4hc/blob/main/{REPO_PATH}"
ADT_SEARCH = "https://my437569.s4hana.cloud.sap/sap/bc/adt/repository/informationsystem/search"
COOKIE_FILE = "tools/vsp/cookies_dev.txt"
MAX_RESULTS = 20000
TODAY = datetime.date.today().isoformat()


def fetch(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "cds-catalog-refresh", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def sap_last_update():
    commit = json.loads(fetch(COMMITS_API, timeout=15))[0]
    return commit["commit"]["committer"]["date"][:10], commit["commit"]["message"].splitlines()[0]


def local_state():
    with open(OFFICIAL, encoding="utf-8") as fh:
        return json.load(fh)


def cookie_header():
    pairs = []
    with open(COOKIE_FILE, encoding="utf-8") as fh:
        for line in fh:
            cols = line.rstrip("\r\n").split("\t")
            if len(cols) >= 7 and not line.startswith("# "):
                pairs.append(f"{cols[5]}={cols[6]}")
    return "; ".join(pairs)


def read_descriptions(names):
    """Description + package of each name found on 080, via one quickSearch per name prefix (split when capped)."""
    headers = {"Cookie": cookie_header(), "Accept": "*/*"}
    rx = re.compile(r'adtcore:type="DDLS/DF" adtcore:name="([^"]+)"'
                    r'(?: adtcore:packageName="([^"]*)")?(?: adtcore:description="([^"]*)")?')
    found = {}

    def walk(prefix):
        query = urllib.parse.urlencode({"operation": "quickSearch", "query": prefix + "*", "objectType": "DDLS",
                                        "maxResults": MAX_RESULTS, "sap-client": "080"}, safe="*")
        text = fetch(f"{ADT_SEARCH}?{query}", headers, timeout=120).decode("utf-8")
        if "<html" in text[:500].lower():
            raise RuntimeError("080 cookie expired (login page returned)")
        hits = rx.findall(text)
        if len(hits) >= MAX_RESULTS:
            for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_/":
                walk(prefix + ch)
            return
        for name, package, desc in hits:
            found[name.upper()] = {"package": package, "description": html.unescape(desc)}

    prefixes = set()
    for n in names:
        m = re.match(r"(/\w+/)?\w*?_.", n)
        prefixes.add(m.group(0) if m else n[:3])
    for p in sorted(prefixes):
        walk(p)
    return {n: found[n] for n in names if n in found}


def refresh(remote_date, remote_msg):
    old = local_state()
    raw = json.loads(fetch(RAW_URL, timeout=300))
    objects = [o for o in raw["objectReleaseInfo"] if o["tadirObject"] == "DDLS"]
    # Classes, interfaces, BDEFs, BAdIs... from the same download, so both catalogs stay on one SAP version.
    sys.path.insert(0, OUT)
    import build_object_index
    object_summary = build_object_index.build(raw["objectReleaseInfo"], remote_date)

    old_state = {o["objectKey"]: o["state"] for o in old["objects"]}
    new_state = {o["objectKey"]: o["state"] for o in objects}
    added = sorted(k for k, s in new_state.items() if s == "released" and old_state.get(k) != "released")
    dropped = sorted(k for k, s in old_state.items() if s == "released" and new_state.get(k) != "released")

    with open(OFFICIAL, "w", encoding="utf-8") as fh:
        json.dump({"source": SOURCE_URL, "sap_last_update": remote_date, "downloaded": TODAY, "objects": objects},
                  fh, indent=0)

    with open(DESC_080, encoding="utf-8") as fh:
        desc = json.load(fh)
    missing = sorted(k for k in new_state if k not in desc["views"])
    desc_note = ""
    if missing:
        try:
            got = read_descriptions(missing)
            desc["views"].update(got)
            desc["read"] = TODAY
            with open(DESC_080, "w", encoding="utf-8") as fh:
                json.dump(desc, fh, ensure_ascii=False, indent=0)
            desc_note = f"descriptions read on 080 for {len(got)} of {len(missing)} views without one"
        except Exception as exc:  # catalog still rebuilds, only descriptions of new views stay empty
            desc_note = f"descriptions NOT read ({exc}); refresh the 080 cookie and rerun with --force"

    build = subprocess.run([sys.executable, "-X", "utf8", os.path.join(OUT, "build_catalog.py")],
                           capture_output=True, text=True)
    if build.returncode != 0:
        print(build.stdout, build.stderr)
        raise SystemExit("build_catalog.py failed")
    summary = build.stdout.splitlines()[0]

    lines = [f"## {TODAY} — SAP update {remote_date} ({remote_msg})", "",
             f"- previous SAP update {old.get('sap_last_update')}; {summary}",
             f"- newly released: {len(added)}" + (f" — {', '.join(added[:40])}{' …' if len(added) > 40 else ''}" if added else ""),
             f"- no longer released: {len(dropped)}" + (f" — {', '.join(dropped[:40])}{' …' if len(dropped) > 40 else ''}" if dropped else ""),
             f"- {desc_note or 'no view without description'}",
             *(f"- released_objects/{line}" for line in object_summary), ""]
    header = "# Changelog — SAP official released CDS list\n\n" if not os.path.exists(CHANGELOG) else ""
    with open(CHANGELOG, "a", encoding="utf-8") as fh:
        fh.write(header + "\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="only report whether SAP has a newer list")
    ap.add_argument("--force", action="store_true", help="refresh even when dates match")
    args = ap.parse_args()

    local = local_state().get("sap_last_update")
    try:
        remote_date, remote_msg = sap_last_update()
    except Exception as exc:
        print(f"CDS catalog: cannot reach GitHub ({exc}); local list is SAP update {local}")
        sys.exit(2)
    newer = remote_date > (local or "")
    if args.check:
        if newer:
            print(f"CDS catalog: SAP released-object list updated {remote_date} (local copy {local}). "
                  f"Refresh: python -X utf8 {OUT}/refresh_sap_official.py")
            sys.exit(10)
        print(f"CDS catalog: up to date (SAP update {local})")
        sys.exit(0)
    if not newer and not args.force:
        print(f"CDS catalog: up to date (SAP update {local}), nothing to do")
        return
    refresh(remote_date, remote_msg)


if __name__ == "__main__":
    main()
