"""skill_lint.py - static checks on skill/workflow descriptions (the text the harness matches requests against).

  python -X utf8 .claude/scripts/skill-eval/skill_lint.py [--budget 15000]

Checks
  E1 description missing / empty                         (error)
  E2 description longer than 1024 characters (Agent Skills limit; the harness may cut it)   (error)
  W1 no "when to use" cue (Use when / Use for / Triggers / Sử dụng khi / Dùng khi ...)      (warning)
  W2 the same quoted trigger phrase appears in 2+ skill descriptions (ambiguous routing)     (warning)
  W3 skill has no case in cases.json (trigger never tested)                                  (warning)
  INFO listing size: sum of name + description over every skill and workflow. The harness lists them all in
       one block with a size budget; past it, some entries are shown with a shortened or no description,
       and those skills stop auto-activating reliably. --budget is an assumed threshold, not a harness constant
       - run_trigger_eval.py is the ground truth.

Exit: 0 no error (warnings allowed) · 1 at least one error.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
CUE = re.compile(r"\b(?:use (?:when|whenever|for|this|it|in|after|before|at|on|immediately)|triggers?)\b|"
                 r"sử dụng (?:khi|workflow)|dùng khi", re.I)


def frontmatter(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\r?\n(.*?)\r?\n---", t, re.S)
    if not m:
        return {}
    fm, out, key = m.group(1), {}, None
    for line in fm.splitlines():
        km = re.match(r"^([\w-]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            out[key] = km.group(2).strip()
        elif key and line.startswith((" ", "\t")):  # folded / continued value
            out[key] = (out[key] + " " + line.strip()).strip()
    for k, v in out.items():
        if v in (">", "|", ">-", "|-"):
            out[k] = ""
        out[k] = out[k].strip().strip('"').strip("'") if out[k] else out[k]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--budget", type=int, default=15000)
    a = ap.parse_args()

    entries = []  # (kind, name, description)
    for f in sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md")):
        fm = frontmatter(f)
        entries.append(("skill", f.parent.name, fm.get("description", "")))
    for f in sorted((ROOT / ".claude" / "commands").glob("*.md")):
        fm = frontmatter(f)
        entries.append(("workflow", f.stem, fm.get("description", "")))

    cases = json.loads((Path(__file__).parent / "cases.json").read_text(encoding="utf-8"))["cases"]
    tested = {s for c in cases for s in c.get("expect", [])}

    errors, warns = [], []
    phrases = defaultdict(set)
    for kind, name, d in entries:
        if not d:
            errors.append(f"E1 {kind} {name}: description missing")
            continue
        if len(d) > 1024:
            errors.append(f"E2 {kind} {name}: description {len(d)} chars > 1024")
        if not CUE.search(d):
            warns.append(f"W1 {kind} {name}: no 'when to use' cue in the description")
        for p in re.findall(r'"([^"]{4,60})"', d):
            phrases[p.lower()].add(name)
    for p, names in sorted(phrases.items()):
        if len(names) > 1:
            warns.append(f"W2 trigger \"{p}\" in: {', '.join(sorted(names))}")
    untested = [n for k, n, _ in entries if k == "skill" and n not in tested]
    if untested:
        warns.append(f"W3 {len(untested)} skill(s) without a trigger case in cases.json: {', '.join(untested)}")

    total = sum(len(n) + len(d) for _, n, d in entries)
    longest = sorted(entries, key=lambda e: -len(e[2]))[:8]
    print(f"{sum(1 for e in entries if e[0] == 'skill')} skills + {sum(1 for e in entries if e[0] == 'workflow')} "
          f"workflows · listing size {total} chars (assumed budget {a.budget}) "
          f"{'OVER' if total > a.budget else 'ok'}")
    if total > a.budget:
        print("  longest descriptions (shorten these first): " +
              ", ".join(f"{n} {len(d)}" for _, n, d in longest))
    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    print(f"{len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
