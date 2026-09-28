"""drift_check.py - detect changes made to a target's SAP objects outside this workspace.

    python .claude/scripts/handbook/drift_check.py <TARGET> [--dir <snapshot dir>]
    python .claude/scripts/handbook/drift_check.py <TARGET> [--dir <snapshot dir>] --record <VERSION>

Input : artifacts/targets/<TARGET>/build/snapshot/<yyyymmdd>/<OBJECT>.<ext>  (default: today's folder)
        one file per Z object, source exactly as SAP returned it (skill target-refresh step 2)
Base  : "snapshot" of the newest version in artifacts/targets/<TARGET>/handbook.json that has one
Output: object list changed / added / removed; unified diff written to <snapshot dir>/drift.diff
--record <VERSION> : store this snapshot (date, dir, sha256 per object) into that version of handbook.json

Sources are compared after normalising line ends and trailing blanks, so a CRLF/LF or
pretty-print whitespace difference is not reported as a change.
Exit: 0 no drift · 1 drift · 2 no baseline yet (first snapshot of the target) · 3 usage / input error
"""
import datetime
import difflib
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
TARGETS = ROOT / "artifacts" / "targets"


def fail(msg):
    print(msg)
    sys.exit(3)


def normalise(raw):
    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n")).strip("\n") + "\n"


def load_sources(folder):
    return {f.stem.upper(): normalise(f.read_bytes())
            for f in sorted(folder.iterdir()) if f.is_file() and f.name != "drift.diff"}


def rel(path):
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_args(argv):
    if not argv or argv[0].startswith("-"):
        fail(__doc__)
    opts = {"target": argv[0], "dir": None, "record": None}
    rest = argv[1:]
    while rest:
        key = rest.pop(0)
        if key not in ("--dir", "--record") or not rest:
            fail(f"unknown or incomplete option '{key}'\n{__doc__}")
        opts[key[2:]] = rest.pop(0)
    return opts


def main(argv):
    opts = parse_args(argv)
    tdir = TARGETS / opts["target"]
    hb_path = tdir / "handbook.json"
    if not hb_path.is_file():
        fail(f"no {rel(hb_path)} - create the target record first (.claude/common/handbook-target.md)")
    hb = json.loads(hb_path.read_text(encoding="utf-8"))

    snap_dir = Path(opts["dir"]) if opts["dir"] else tdir / "build" / "snapshot" / datetime.date.today().strftime("%Y%m%d")
    if not snap_dir.is_absolute():
        snap_dir = ROOT / snap_dir
    if not snap_dir.is_dir():
        fail(f"snapshot folder {snap_dir} not found - pull the sources first (skill target-refresh step 2)")
    now = load_sources(snap_dir)
    if not now:
        fail(f"snapshot folder {snap_dir} is empty")
    now_hash = {n: sha(s) for n, s in now.items()}

    base_ver = next((v for v in hb.get("versions", []) if v.get("snapshot")), None)
    status = 2
    if base_ver is None:
        print(f"NO BASELINE - no version of {opts['target']} has a snapshot yet; this snapshot becomes the baseline")
    else:
        base = base_ver["snapshot"]
        old_hash = base.get("objects", {})
        changed = sorted(n for n in now_hash if n in old_hash and now_hash[n] != old_hash[n])
        added = sorted(n for n in now_hash if n not in old_hash)
        removed = sorted(n for n in old_hash if n not in now_hash)
        print(f"baseline: version {base_ver.get('version')} snapshot {base.get('taken')} ({base.get('dir')})")
        if not (changed or added or removed):
            print(f"NO DRIFT - {len(now_hash)} object(s) identical to the baseline")
            status = 0
        else:
            status = 1
            print(f"DRIFT - changed {len(changed)} · added {len(added)} · removed {len(removed)}")
            for label, names in (("changed", changed), ("added", added), ("removed", removed)):
                for n in names:
                    print(f"  {label:8} {n}")
            old_dir = ROOT / base.get("dir", "")
            old_src = load_sources(old_dir) if base.get("dir") and old_dir.is_dir() else {}
            diff = []
            for n in changed + added + removed:
                a = old_src.get(n, "") if n not in added else ""
                b = now.get(n, "")
                if n in changed and n not in old_src:
                    diff.append(f"### {n}: baseline source file missing in {base.get('dir')} - hash differs, no text diff\n")
                    continue
                diff.extend(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                                                 f"{n} @ {base.get('taken')}", f"{n} @ now"))
            out = snap_dir / "drift.diff"
            out.write_text("".join(diff), encoding="utf-8")
            print(f"diff written: {rel(out)}")

    if opts["record"]:
        ver = next((v for v in hb.get("versions", []) if v.get("version") == opts["record"]), None)
        if ver is None:
            fail(f"version {opts['record']} not found in handbook.json - add the version block first")
        ver["snapshot"] = {"taken": datetime.date.today().isoformat(),
                           "dir": rel(snap_dir), "objects": now_hash}
        hb_path.write_text(json.dumps(hb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"snapshot recorded into version {opts['record']} ({len(now_hash)} object(s))")
    sys.exit(status)


if __name__ == "__main__":
    main(sys.argv[1:])
