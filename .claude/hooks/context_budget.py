"""UserPromptSubmit + Stop: context-size budget for this session (token budget, user 2026-11-16).

Why: in session 624dbb89 (ZGL02) 395M of the tokens were the conversation re-read from cache on each of 1,563
turns (~250k per turn) - about 70% of the cost, far more than any single tool output. Shorter sessions are the
biggest saving. The user works ONE report per session (2026-11-16), so at a fix boundary: notes + INDEX.md, then /compact.

Context size = input + cache_creation + cache_read tokens of the last main-thread assistant turn in the transcript.
It fires when the size first reaches CONTEXT_BUDGET_TOKENS, then again every CONTEXT_BUDGET_STEP above it
(system-config.md env block), once per level per session:
  UserPromptSubmit -> additionalContext to the agent (finish the current fix, record notes, propose /compact)
  Stop             -> systemMessage to the user (Vietnamese, rule §13)
Never blocks; any error -> silent pass.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_hook import ROOT, cfg_int, emit, read_input, session_dir  # noqa: E402


def last_context_tokens(path, tail_bytes=1_500_000):
    with open(path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - tail_bytes))
        lines = f.read().decode("utf-8", errors="replace").splitlines()
    for line in reversed(lines):
        if '"usage"' not in line:
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("type") != "assistant" or o.get("isSidechain"):
            continue
        u = (o.get("message") or {}).get("usage") or {}
        n = sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
        if n:
            return n
    return 0


def active_target(window_s=6 * 3600):
    """The target folder with the most recently modified file (last 6 h), else None - names it in the hint."""
    best, best_t = None, 0.0
    base = ROOT / "artifacts" / "targets"
    if not base.is_dir():
        return None
    for d in base.iterdir():
        if not d.is_dir():
            continue
        for sub in (d, d / "build", d / "notes"):
            try:
                for p in sub.iterdir():
                    if p.is_file() and p.stat().st_mtime > best_t:
                        best, best_t = d.name, p.stat().st_mtime
            except OSError:
                pass
    import time
    return best if best and time.time() - best_t < window_s else None


def main():
    try:
        data = read_input()
        event = data.get("hook_event_name", "")
        tp = data.get("transcript_path", "")
        if event not in ("UserPromptSubmit", "Stop") or not tp or not os.path.isfile(tp):
            return
        budget, step = cfg_int("CONTEXT_BUDGET_TOKENS", 120000), max(cfg_int("CONTEXT_BUDGET_STEP", 40000), 1)
        ctx = last_context_tokens(tp)
        level = 0 if ctx < budget else 1 + (ctx - budget) // step
        sid = re.sub(r"[^A-Za-z0-9_-]", "_", str(data.get("session_id", "nosession")))
        state = session_dir("context-budget") / f"{sid}_{event}.txt"
        try:
            done = int(state.read_text())
        except (OSError, ValueError):
            done = 0
        if level <= done:
            if level < done:  # context shrank (compaction): re-arm the lower levels
                state.write_text(str(level))
            return
        state.write_text(str(level))
        k = f"{ctx // 1000}k"
        t = active_target()
        tname = t or "<TARGET>"
        compact = (f"/compact giữ: trạng thái {tname}, quyết định đã chốt, lỗi đã gặp, việc đang dở; "
                   "bỏ: đoạn source và output tool cũ")
        if event == "UserPromptSubmit":
            emit({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": (
                f"context-budget: this session's context is ~{k} tokens (budget {budget // 1000}k); every turn re-reads "
                "all of it. The user works ONE report per session, so the remedy is /compact, not a new session. Do "
                "the user's current request, but stop at the next boundary (a fix/update through its 4 gates, TS done, "
                f"a target-refresh done) instead of starting the next one: record the outcome in "
                f"artifacts/targets/{tname}/notes/ + INDEX.md (what changed, where, why, test result), then tell the "
                f"user to run: {compact}. After the compact, re-read only the source region the next request needs "
                "(grep the freshly pulled source) - never reuse a source excerpt from before the compact, it may be "
                "stale. Keep tool output small (.claude/common/lean-sap-io.md).")}})
        else:
            emit({"systemMessage": (
                f"⚠ Context phiên này ~{k} token (ngưỡng {budget // 1000}k) — mỗi lượt đều đọc lại toàn bộ. "
                f"Xong lần fix hiện tại thì để em ghi notes/INDEX.md, rồi anh chạy: {compact}")})
    except Exception as e:  # advisory: never break the turn
        sys.stderr.write(f"context_budget: {e}\n")


if __name__ == "__main__":
    main()
    sys.exit(0)
