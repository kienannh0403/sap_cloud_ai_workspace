"""Error codex — look up an SAP / tooling error by what is on the screen, and keep the codex free of duplicates.

One JSON file per ROOT CAUSE in entries/. Two causes may share a message key (e.g. HTTP 412): `find` returns both.
Schema and the update rules (same cause → add an occurrence, never a new file): README.md.

Run from the workspace root:
    python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py find "412"            # by message key / text
    python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py show <id>
    python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py check                # schema + duplicate warnings
    python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py list
Exit (check): 0 = clean · 1 = schema error · 3 = possible duplicate to review.
Idea and base schema: StormShynn/sap-error-codex (MIT); evidence / occurrences / source fields added here.
"""
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENTRIES = ROOT / "entries"
MODULES = {"RAP / ABAP Cloud", "CDS / Fiori Elements", "Fiori / UI5", "Integration / OData", "Tooling / MCP",
           "Transport & Release", "Basis / Auth"}
SEVERITIES = {"Blocker", "High", "Medium", "Low"}
REQUIRED = {"title": str, "module": str, "severity": str, "verified": bool, "msgKeys": list, "symptom": str,
            "rootCause": str, "solutions": list, "prevention": str, "evidence": list, "occurrences": list,
            "refs": list, "source": str, "createdAt": str, "updatedAt": str}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load():
    out = {}
    for path in sorted(ENTRIES.glob("*.json")):
        out[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    return out


def norm(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def find(term, entries):
    """Rank: exact message key > key contains term > title/symptom/cause contains term."""
    t = norm(term)
    hits = []
    for eid, e in entries.items():
        keys = [norm(k) for k in e["msgKeys"]]
        if t in keys:
            rank = 0
        elif any(t in k or k in t for k in keys if k):
            rank = 1
        elif t in norm(" ".join([e["title"], e["symptom"], e["rootCause"]])):
            rank = 2
        else:
            continue
        hits.append((rank, eid, e))
    return sorted(hits, key=lambda h: (h[0], h[1]))


def check(entries):
    errors, dupes = [], []
    for eid, e in entries.items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", eid):
            errors.append(f"{eid}: file name must be kebab-case")
        for field, ftype in REQUIRED.items():
            if not isinstance(e.get(field), ftype):
                errors.append(f"{eid}: field '{field}' missing or not {ftype.__name__}")
        if e.get("module") not in MODULES:
            errors.append(f"{eid}: module '{e.get('module')}' not in {sorted(MODULES)}")
        if e.get("severity") not in SEVERITIES:
            errors.append(f"{eid}: severity '{e.get('severity')}' not in {sorted(SEVERITIES)}")
        if not e.get("msgKeys"):
            errors.append(f"{eid}: msgKeys empty — the codex is searched by them")
        if e.get("verified") and not e.get("evidence"):
            errors.append(f"{eid}: verified=true needs at least one evidence entry")
        if not any(s.get("recommended") for s in e.get("solutions", [])):
            errors.append(f"{eid}: no solution marked recommended")
        for d in ("createdAt", "updatedAt"):
            if isinstance(e.get(d), str) and not DATE.match(e[d]):
                errors.append(f"{eid}: {d} must be YYYY-MM-DD")
        for occ in e.get("occurrences", []):
            if not {"target", "date"} <= set(occ):
                errors.append(f"{eid}: each occurrence needs target + date")
    ids = sorted(entries)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            shared = {norm(k) for k in entries[a]["msgKeys"]} & {norm(k) for k in entries[b]["msgKeys"]}
            if not shared:
                continue
            ratio = difflib.SequenceMatcher(None, norm(entries[a]["rootCause"]), norm(entries[b]["rootCause"])).ratio()
            if ratio >= 0.55:
                dupes.append(f"{a} ~ {b}: share {sorted(shared)}, root causes {ratio:.0%} alike — same cause? merge "
                             f"into one entry (add an occurrence) or make the causes clearly different")
    return errors, dupes


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2 or sys.argv[1] not in {"find", "show", "check", "list"}:
        print(__doc__)
        sys.exit(2)
    entries = load()
    cmd = sys.argv[1]
    if cmd == "find":
        term = " ".join(sys.argv[2:])
        hits = find(term, entries)
        if not hits:
            print(f"codex: nothing for '{term}' — new error: after the root cause is proven, add an entry (README.md)")
            return
        print(f"codex: {len(hits)} entr{'y' if len(hits) == 1 else 'ies'} for '{term}'")
        for rank, eid, e in hits:
            mark = "verified" if e["verified"] else "NOT verified"
            print(f"- {eid}  [{e['module']}, {e['severity']}, {mark}, seen {len(e['occurrences'])}x]\n    {e['title']}")
    elif cmd == "show":
        eid = sys.argv[2] if len(sys.argv) > 2 else ""
        if eid not in entries:
            sys.exit(f"no entry '{eid}'")
        print(json.dumps(entries[eid], ensure_ascii=False, indent=2))
    elif cmd == "list":
        for eid, e in entries.items():
            print(f"{'V' if e['verified'] else ' '} {e['module']:<22} {eid}")
        print(f"{len(entries)} entries, {sum(e['verified'] for e in entries.values())} verified")
    else:
        errors, dupes = check(entries)
        for line in errors:
            print("ERROR  " + line)
        for line in dupes:
            print("DUPE?  " + line)
        print(f"codex check: {len(entries)} entries, {len(errors)} error(s), {len(dupes)} possible duplicate(s)")
        sys.exit(1 if errors else 3 if dupes else 0)


if __name__ == "__main__":
    main()
