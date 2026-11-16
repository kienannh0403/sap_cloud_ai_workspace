"""Shared helpers for the Python hooks (tool_output_shrink.py, context_budget.py).

cfg(key, default) reads KEY=value from the ```env block of .claude/common/system-config.md - the same single
source lib-config.sh reads for the bash hooks. session_dir(name) is a folder under
artifacts/scratchpads/_session/ (git-ignored for the output folders, see .gitignore).
"""
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])
SYSTEM_CONFIG = ROOT / ".claude" / "common" / "system-config.md"


def cfg(key, default=""):
    try:
        text = SYSTEM_CONFIG.read_text(encoding="utf-8")
    except OSError:
        return default
    m = re.search(r"^```env[ \t]*\r?\n(.*?)^```", text, re.S | re.M)
    if not m:
        return default
    for line in m.group(1).splitlines():
        line = line.rstrip("\r")
        if line.startswith(key + "="):
            return line[len(key) + 1:]
    return default


def cfg_int(key, default):
    try:
        return int(cfg(key, str(default)))
    except ValueError:
        return default


def read_input():
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    return json.loads(raw) if raw.strip() else {}


def session_dir(name):
    d = ROOT / "artifacts" / "scratchpads" / "_session" / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def prune(d, days=7):
    """Delete files older than `days` in folder d (cheap housekeeping, errors ignored)."""
    limit = time.time() - days * 86400
    for p in d.iterdir():
        try:
            if p.is_file() and p.stat().st_mtime < limit:
                p.unlink()
        except OSError:
            pass


def rel(p):
    try:
        return Path(p).resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(p)


def emit(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.stdout.flush()
