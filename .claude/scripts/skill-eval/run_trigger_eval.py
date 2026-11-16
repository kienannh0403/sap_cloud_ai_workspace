"""run_trigger_eval.py - does each realistic request auto-activate the right skill? (idea from obra/superpowers
"writing-skills": test a skill against a real agent run, not by re-reading it).

For every case in cases.json it starts a headless Claude Code run in this workspace and records the FIRST skill the
model invokes. Safe by construction: --tools Skill (no Bash/Edit/Write/Read), --strict-mcp-config with no MCP
server (no SAP connection at all), no session saved; the run is killed as soon as the first Skill call appears.
Each case costs one model turn (plus the skill body when one is loaded).

  python -X utf8 .claude/scripts/skill-eval/run_trigger_eval.py                 # all cases
  python -X utf8 .claude/scripts/skill-eval/run_trigger_eval.py --only rap-bdef,odata --model sonnet
  python -X utf8 .claude/scripts/skill-eval/run_trigger_eval.py --jobs 4

Claude CLI: --claude, else $CLAUDE_BIN, else `claude` on PATH, else the newest VS Code extension's native binary.
Result: artifacts/system_analysis/SKILL_EVAL/run_<yyyymmdd_hhmm>.json + one console line per case.
Exit: 0 all pass · 1 at least one FAIL · 2 setup error (CLI not found, every case errored).
"""
import argparse
import datetime
import glob
import json
import os
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "artifacts" / "system_analysis" / "SKILL_EVAL"


def find_claude(explicit):
    for c in (explicit, os.environ.get("CLAUDE_BIN"), shutil.which("claude")):
        if c and Path(c).exists():
            return c
    home = Path.home()
    hits = sorted(glob.glob(str(home / ".vscode" / "extensions" / "anthropic.claude-code-*" / "resources" /
                                "native-binary" / "claude*")), reverse=True)
    return hits[0] if hits else None


def run_case(claude, case, model, timeout):
    cmd = [claude, "-p", case["prompt"], "--output-format", "stream-json", "--verbose",
           "--tools", "Skill", "--strict-mcp-config", "--no-session-persistence"]
    if model:
        cmd += ["--model", model]
    invoked, text, err = [], [], None
    try:
        p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             stdin=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    except OSError as e:
        return {"id": case["id"], "error": f"cannot start CLI: {e}", "invoked": []}
    timer = threading.Timer(timeout, p.kill)
    timer.start()
    try:
        for line in p.stdout:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") == "assistant":
                for blk in ev.get("message", {}).get("content", []):
                    if blk.get("type") == "tool_use" and blk.get("name") == "Skill":
                        invoked.append(str(blk.get("input", {}).get("skill", "")).split(":")[-1])
                    elif blk.get("type") == "text":
                        text.append(blk.get("text", ""))
                if invoked:
                    p.kill()
                    break
            elif ev.get("type") == "result":
                if ev.get("is_error"):
                    err = str(ev.get("result") or ev.get("subtype"))[:300]
                break
    finally:
        timer.cancel()
        if p.poll() is None:
            p.kill()
        p.wait()
    if not invoked and not text and err is None and p.returncode not in (0, None):
        err = (p.stderr.read() or f"exit {p.returncode}")[:300]
    return {"id": case["id"], "invoked": invoked, "answer_head": " ".join(text)[:200], "error": err}


def verdict(case, r):
    if r.get("error"):
        return "ERROR"
    first = r["invoked"][0] if r["invoked"] else None
    expect, forbid = case.get("expect", []), case.get("forbid", [])
    if first in forbid:
        return "FAIL"
    if not expect:
        return "PASS" if first is None else "FAIL"
    return "PASS" if first in expect else "FAIL"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated case ids")
    ap.add_argument("--model", help="model alias/id for the runs (default: the CLI's default)")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--claude")
    a = ap.parse_args()

    claude = find_claude(a.claude)
    if not claude:
        print("Claude CLI not found - pass --claude or set CLAUDE_BIN (exit 2)")
        return 2
    cases = json.loads((Path(__file__).parent / "cases.json").read_text(encoding="utf-8"))["cases"]
    if a.only:
        want = set(a.only.split(","))
        cases = [c for c in cases if c["id"] in want]
    print(f"{len(cases)} case(s) · CLI {claude} · model {a.model or 'default'}")

    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        results = list(ex.map(lambda c: run_case(claude, c, a.model, a.timeout), cases))

    rows, counts = [], {"PASS": 0, "FAIL": 0, "ERROR": 0}
    for c, r in zip(cases, results):
        v = verdict(c, r)
        counts[v] += 1
        got = r["invoked"][0] if r["invoked"] else "(none)"
        print(f"{v:5} {c['id']:18} expect={'|'.join(c.get('expect', [])) or '(none)':40} got={got}"
              + (f"  error={r['error']}" if r.get("error") else ""))
        rows.append({**c, **r, "verdict": v})
    print(f"PASS {counts['PASS']} · FAIL {counts['FAIL']} · ERROR {counts['ERROR']}")

    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"run_{datetime.datetime.now():%Y%m%d_%H%M}.json"
    out.write_text(json.dumps({"model": a.model or "default", "counts": counts, "results": rows},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {out.relative_to(ROOT)}")
    if counts["ERROR"] == len(cases):
        return 2
    return 1 if counts["FAIL"] or counts["ERROR"] else 0


if __name__ == "__main__":
    sys.exit(main())
