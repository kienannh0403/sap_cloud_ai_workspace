"""PostToolUse: shrink bulky tool output BEFORE it enters the conversation (token budget, user 2026-11-16).

Measured on session 624dbb89 (ZGL02, 1,563 turns): every output stays in context and is re-read on every later
turn, so a big output is paid for again and again. Nothing is lost - the full output is always saved to a file
first and the replacement names that file.

  SAP edit (vsp EDITSOURCE, action=edit*) - result JSON is rewritten:
      oldString / newString dropped (they echo the agent's own call)
      syntaxWarnings: the full list of the WHOLE object came back on every edit. First edit of an object in a
        session -> grouped by message text ("Lines 5909,5927 (2x): <text>"); later edits -> only the warnings that
        are NEW against the previous edit of that object in this session, plus counts.
      every other key (success, activation messages, errors, matchCount ...) is kept verbatim.
  SAP query (SQL)   - output over TOOL_OUTPUT_CAP_SQL chars -> head + tail + file path.
  other SAP actions - output over TOOL_OUTPUT_CAP_SAP chars -> head + tail + file path.
  Bash / PowerShell - stdout over TOOL_OUTPUT_CAP_BASH chars (stderr over half of it) -> head + tail + file path.
      Opt-out for one command: put the comment  #full-output  in it.

Caps come from the env block of .claude/common/system-config.md. Fail open: any error -> original output.
Full outputs: artifacts/scratchpads/_session/tool-output/ (git-ignored, pruned after 7 days).
"""
import collections
import datetime
import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from lib_hook import cfg_int, emit, prune, read_input, rel, session_dir  # noqa: E402

OUT_DIR = session_dir("tool-output")
STATE_DIR = session_dir("tool-output-state")
LINE_RE = re.compile(r"^\s*Line (\d+):\s*(.*)$", re.S)


def save_full(tag, payload):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]
    path = OUT_DIR / f"{stamp}_{re.sub(r'[^A-Za-z0-9_-]', '_', tag)[:60]}.txt"
    text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=1)
    path.write_text(text, encoding="utf-8")
    if datetime.datetime.now().minute % 10 == 0:
        prune(OUT_DIR)
        prune(STATE_DIR)
    return rel(path)


def cap_text(text, cap, path):
    head, tail = int(cap * 0.7), int(cap * 0.25)
    nl = text.rfind("\n", 0, head)  # snap both cut points to line boundaries when one is near
    head = nl + 1 if nl > head * 0.6 else head
    nl = text.find("\n", len(text) - tail)
    tail = len(text) - nl - 1 if 0 <= nl < len(text) - tail * 0.6 else tail
    cut = text[head:len(text) - tail]
    marker = (f"\n\n[... output-shrink: {len(cut):,} of {len(text):,} chars / {cut.count(chr(10)):,} lines cut. "
              f"Full output: {path} - grep it or read a slice (sed -n 'a,bp'). "
              f"Add #full-output to a Bash command to opt out. ...]\n\n")
    return text[:head] + marker + text[len(text) - tail:]


# --- MCP response shape: list of content blocks / {"content": [...]} / plain string -------------------------
def mcp_text(resp):
    blocks = resp.get("content") if isinstance(resp, dict) else resp
    if isinstance(blocks, str):
        return blocks, None
    if isinstance(blocks, list):
        texts = [i for i, b in enumerate(blocks) if isinstance(b, dict) and b.get("type") == "text"]
        if len(texts) == 1:
            return blocks[texts[0]].get("text", ""), texts[0]
    return None, None


def mcp_replace(resp, idx, new_text):
    if isinstance(resp, str):
        return new_text
    if isinstance(resp, dict) and isinstance(resp.get("content"), str):
        return {**resp, "content": new_text}
    blocks = list(resp.get("content") if isinstance(resp, dict) else resp)
    blocks[idx] = {**blocks[idx], "text": new_text}
    return {**resp, "content": blocks} if isinstance(resp, dict) else blocks


def parse_msg(w):
    m = LINE_RE.match(str(w))
    return (int(m.group(1)), m.group(2).strip()) if m else (None, str(w).strip())


def group(parsed):
    groups = collections.OrderedDict()
    for ln, t in parsed:
        groups.setdefault(t, []).append(ln)
    return [(f"Lines {','.join(str(x) for x in ls if x is not None)} ({len(ls)}x): {t}" if any(ls) else f"({len(ls)}x) {t}")
            for t, ls in groups.items()]


def shrink_edit(data, text, path):
    try:
        r = json.loads(text)
    except ValueError:
        return None
    if not isinstance(r, dict) or not ({"oldString", "newString", "syntaxWarnings"} & set(r)):
        return None
    out = {k: v for k, v in r.items() if k not in ("oldString", "newString", "syntaxWarnings", "syntaxErrors")}
    if "oldString" in r or "newString" in r:
        out["note"] = "output-shrink: oldString/newString omitted (they echo your own call)"
    warns = r.get("syntaxWarnings") or []
    parsed = [parse_msg(w) for w in warns]
    obj = str(r.get("objectName") or data.get("tool_input", {}).get("target") or "object")
    server = data.get("tool_name", "").split("__")[1] if "__" in data.get("tool_name", "") else "sap"
    key = re.sub(r"[^A-Za-z0-9_-]", "_", f"{data.get('session_id', 'nosession')}_{server}_{obj}".upper())
    state = STATE_DIR / f"{key}.json"
    prev = json.loads(state.read_text(encoding="utf-8")) if state.is_file() else None
    if warns or prev is None:
        state.write_text(json.dumps([t for _, t in parsed], ensure_ascii=False), encoding="utf-8")
    known = set(prev or []) | {t for _, t in parsed}
    errs = r.get("syntaxErrors") or []
    if errs:
        if [str(e) for e in errs] == [str(w) for w in warns]:
            out["syntaxErrors_note"] = (f"syntaxErrors = the same {len(errs)} entries as syntaxWarnings (vsp repeats the "
                                        "warning list when it refuses an edit over warnings) - not repeated.")
        else:  # lossless: every distinct text with all its lines, texts never seen as a warning first
            pe = [parse_msg(e) for e in errs]
            fresh = [t for _, t in pe if t not in known]
            out["syntaxErrors_grouped"] = group(sorted(pe, key=lambda x: x[1] in known))
            out["syntaxErrors_note"] = (f"{len(errs)} entries, {len(set(fresh))} distinct texts not among this object's "
                                        "known warnings (listed first) - quote these exactly (rule §5).")
    if warns:
        if prev is None:
            out["syntaxWarnings_grouped"] = group(parsed)
            out["syntaxWarnings_note"] = (f"{len(warns)} warnings ({len(out['syntaxWarnings_grouped'])} distinct texts), "
                                          "first edit of this object in this session - assess every distinct text "
                                          "(activation-guard Gate 1).")
        else:
            left = collections.Counter(prev)
            new = []
            for (ln, t), raw in zip(parsed, warns):
                if left[t] > 0:
                    left[t] -= 1
                else:
                    new.append(raw)
            out["syntaxWarnings_new"] = new
            out["syntaxWarnings_note"] = (f"{len(warns)} warnings: {len(warns) - len(new)} unchanged vs the previous "
                                          f"edit of this object in this session (not repeated), {len(new)} NEW listed, "
                                          f"{sum(left.values())} gone.")
    else:
        out["syntaxWarnings_note"] = "0 warnings"
    out["full_output"] = path
    return json.dumps(out, ensure_ascii=False, indent=1)


def handle_sap(data):
    resp = data.get("tool_response")
    text, idx = mcp_text(resp)
    if text is None:
        return None
    action = str(data.get("tool_input", {}).get("action", "")).lower()
    if text.lstrip()[:200].lower().startswith("<html") and "samlrequest" in text[:20000].lower():
        server = data.get("tool_name", "").split("__")[1] if "__" in data.get("tool_name", "") else "?"
        path = save_full(f"sap_{action}_login_page", text)
        return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedMCPToolOutput": mcp_replace(resp, idx, (
            f"output-shrink: SAP returned its SAML login page instead of data - the session cookie of MCP server "
            f"'{server}' has expired. Nothing was read or changed. Ask the user to refresh the cookie "
            f"([Skill: sap-doctor], cookie-refresh procedure), then retry. Full page: {path}"))}}
    if action.startswith("edit"):
        if len(text) < 1500:
            return None
        path = save_full(f"sap_{action}", text)
        new = shrink_edit(data, text, path)
    else:
        cap = cfg_int("TOOL_OUTPUT_CAP_SQL", 4000) if action == "query" else cfg_int("TOOL_OUTPUT_CAP_SAP", 15000)
        if len(text) <= cap:
            return None
        new = cap_text(text, cap, save_full(f"sap_{action}", text))
    if not new or len(new) >= len(text):
        return None
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedMCPToolOutput": mcp_replace(resp, idx, new)}}


def handle_shell(data):
    cmd = str(data.get("tool_input", {}).get("command", ""))
    if "#full-output" in cmd.replace(" ", ""):
        return None
    resp = data.get("tool_response")
    if not isinstance(resp, dict):
        return None
    cap = cfg_int("TOOL_OUTPUT_CAP_BASH", 6000)
    changed = dict(resp)
    for field, limit in (("stdout", cap), ("stderr", cap // 2), ("output", cap)):
        v = resp.get(field)
        if isinstance(v, str) and len(v) > limit:
            changed[field] = cap_text(v, limit, save_full(f"{data.get('tool_name', 'shell')}_{field}", v))
    if changed == resp:
        return None
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedToolOutput": changed}}


def main():
    try:
        data = read_input()
        name = data.get("tool_name", "")
        result = handle_shell(data) if name in ("Bash", "PowerShell") else handle_sap(data) if name.endswith("__SAP") else None
        if result:
            emit(result)
    except Exception as e:  # fail open: never break a tool call over a shrink problem
        sys.stderr.write(f"tool_output_shrink: {e}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
