#!/usr/bin/env python3
"""Released-object check for draft ABAP / CDS / BDEF source, before it is pushed to SAP.

Finds every standard SAP object a draft names (classes, interfaces, exception classes, XCO, CDS views, BDEFs,
called function modules) and looks it up in the local copy of SAP's official release list:
  artifacts/system_analysis/CDS_RELEASED_CATALOG/sap_official/objectReleaseInfo_DDLS.json   (CDS views)
  artifacts/system_analysis/CDS_RELEASED_CATALOG/released_objects/*.csv                      (CLAS, INTF, BDEF, FUNC...)
Catches "not released / deprecated" before Push, instead of in ATC (Gate 4) after activation. It does not replace
ATC: it only knows names, not statements or field-level release.

Usage (workspace root):
  python -X utf8 .claude/scripts/released_check.py <file-or-folder> [...] [--all] [--json]
    --all   also list the objects that are released (default: only problems + a count)
Exit: 0 = nothing to fix · 1 = a deprecated / not released / unknown object · 2 = usage or missing index.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

CATALOG = Path("artifacts/system_analysis/CDS_RELEASED_CATALOG")
DDLS_JSON = CATALOG / "sap_official" / "objectReleaseInfo_DDLS.json"
OBJECT_DIR = CATALOG / "released_objects"
SOURCE_SUFFIXES = {".abap", ".asddls", ".asbdef", ".ddlx", ".asddlxs", ".srvd", ".acds", ".txt"}

# Prefixes that are only ever SAP objects: an unknown name here is a real finding wherever it appears.
STRONG = re.compile(r"\b((?:CL|CX|IF|XCO)_[A-Z0-9_]+)\b", re.IGNORECASE)
# CDS-style prefixes clash with ABAP parameter names (i_matnr, c_max, r_result...): an unknown name is only a
# finding when it sits where a data source / BO is expected.
WEAK_PREFIX = re.compile(r"^(?:I|C|A|D|E|P|R)_[A-Z0-9_]+$", re.IGNORECASE)
NAME = r"([A-Z][A-Z0-9_]*)"
SOURCE_POSITION = re.compile(
    r"\b(?:FROM|JOIN|PROJECTION\s+ON|ASSOCIATION(?:\s*\[[^\]]*\])?\s+TO(?:\s+PARENT)?|COMPOSITION(?:\s*\[[^\]]*\])?\s+OF"
    r"|ENTITIES\s+OF|ENTITY|TYPE\s+(?:TABLE|STRUCTURE|REQUEST|RESPONSE)\s+FOR\s+\w+(?:\s+\w+)?|EXPOSE)\s+" + NAME,
    re.IGNORECASE,
)
ANY_WEAK = re.compile(r"\b((?:I|C|A|D|E|P|R)_[A-Z0-9_]+)\b", re.IGNORECASE)
CALL_FUNCTION = re.compile(r"\bCALL\s+FUNCTION\s+'([A-Z0-9_/]+)'", re.IGNORECASE)


def load_index():
    if not DDLS_JSON.exists() or not OBJECT_DIR.exists():
        sys.exit(f"released index missing: {DDLS_JSON} / {OBJECT_DIR} — run build_object_index.py (see its INDEX.md)")
    index = {}
    for obj in json.loads(DDLS_JSON.read_text(encoding="utf-8"))["objects"]:
        succ = ";".join(s.get("objectKey", "") for s in obj.get("successors", []))
        index.setdefault(obj["objectKey"].upper(), []).append(("DDLS", obj["state"], succ))
    for path in sorted(OBJECT_DIR.glob("*.csv")):
        with path.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                index.setdefault(row["object_key"].upper(), []).append(
                    (row["object_type"], row["state"], row["successors"]))
    return index


def strip_code(line: str, in_block: bool):
    """Remove comments and literals; return (code, still_in_block_comment)."""
    if in_block:
        end = line.find("*/")
        if end < 0:
            return "", True
        line, in_block = line[end + 2:], False
    if line.lstrip().startswith("*"):  # ABAP full-line comment
        return "", False
    line = re.sub(r"/\*.*?\*/", " ", line)
    if "/*" in line:
        line, in_block = line[: line.index("/*")], True
    line = re.sub(r"'(?:[^']|'')*'|`[^`]*`|\|[^|]*\|", " ", line)  # literals, string templates
    line = re.split(r'"|//', line, maxsplit=1)[0]  # ABAP end-of-line / CDS comment
    return line, in_block


def scan_file(path: Path, index):
    findings = []
    in_block = False
    for no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for fm in CALL_FUNCTION.findall(raw):  # function name lives inside a literal
            findings.append((no, fm.upper(), "function"))
        code, in_block = strip_code(raw, in_block)
        if not code.strip():
            continue
        positioned = {m.upper() for m in SOURCE_POSITION.findall(code)}
        for name in STRONG.findall(code):
            findings.append((no, name.upper(), "strong"))
        for name in ANY_WEAK.findall(code):
            up = name.upper()
            if up in index or up in positioned:
                findings.append((no, up, "source" if up in positioned else "weak"))
        for up in positioned:  # data source with any non-Z name (e.g. a view without a prefix)
            if not WEAK_PREFIX.match(up) and not STRONG.fullmatch(up) and not up.startswith(("Z", "Y", "$")):
                if up in index:
                    findings.append((no, up, "source"))
    seen, unique = set(), []
    for item in findings:
        if (item[0], item[1]) not in seen:
            seen.add((item[0], item[1]))
            unique.append(item)
    return unique


def judge(name, how, index):
    """Return (status, type, successor) — status: released / deprecated / notToBeReleased / not-released / skip."""
    hits = index.get(name)
    if hits:
        best = next((h for h in hits if h[1] == "released"), hits[0])
        return best[1], best[0], best[2]
    if how == "weak":  # unknown i_xxx / c_xxx outside a source position = a local name, not a finding
        return "skip", "", ""
    return "not-released", "", ""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Check draft source against SAP's released-object list.")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--all", action="store_true", help="also list released objects")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    index = load_index()
    files = []
    for p in args.paths:
        if p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in SOURCE_SUFFIXES)
        elif p.is_file():
            files.append(p)
        else:
            print(f"[skip] not found: {p}", file=sys.stderr)
    if not files:
        print("No source file to check.", file=sys.stderr)
        sys.exit(2)

    rows, released = [], set()
    for f in files:
        for no, name, how in scan_file(f, index):
            status, otype, succ = judge(name, how, index)
            if status == "skip":
                continue
            if status == "released":
                released.add(name)
                if not args.all:
                    continue
            rows.append({"file": str(f), "line": no, "name": name, "type": otype or "?",
                         "state": status, "successor": succ})

    problems = [r for r in rows if r["state"] != "released"]
    if args.json:
        print(json.dumps({"files": len(files), "released": sorted(released), "problems": problems,
                          "rows": rows}, indent=1))
    else:
        print(f"released_check: {len(files)} file(s), {len(released)} distinct released object(s), "
              f"{len(problems)} problem(s)")
        for r in rows:
            mark = "  ok " if r["state"] == "released" else "  !! "
            hint = f" -> use {r['successor']}" if r["successor"] else ""
            if r["state"] == "not-released":
                hint = " (not in SAP's list: not released for ABAP Cloud, or a wrong name)"
            print(f"{mark}{r['file']}:{r['line']}  {r['name']}  [{r['type']}] {r['state']}{hint}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
