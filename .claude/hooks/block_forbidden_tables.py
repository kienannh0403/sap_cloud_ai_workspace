"""PreToolUse: refuse business-data reads of blocklisted tables / CDS views.

Called by block-forbidden-tables.sh with the hook JSON on stdin. Sources:
  - .claude/common/system-config.md   BLOCKLIST_PROFILE (minimal | standard | strict)
  - .claude/exceptions/*.md           (README.md excluded) tier/action tags + table rows
Covers the vsp SAP tool (action="query", SQL in params) and Bash curl calls to
/sap/bc/adt/datapreview/freestyle. action=deny -> "deny", action=warn -> "ask".
Adapted from sc4sap scripts/hooks/block-forbidden-tables.mjs.
"""
import json
import os
import re
import sys

TIER_ORDER = {"minimal": 1, "standard": 2, "strict": 3}
IDENT = r"[A-Za-z_/][A-Za-z0-9_/]*"


def load_profile(root):
    path = os.path.join(root, ".claude", "common", "system-config.md")
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return "strict"  # unknown config -> strictest reading
    block = re.search(r"^```env\s*$(.*?)^```", text, re.M | re.S)
    m = re.search(r"^BLOCKLIST_PROFILE=(\S*)", block.group(1) if block else "", re.M)
    return (m.group(1) if m else "strict").lower()


def to_regex(name):
    esc = re.escape(name.upper()).replace(r"\*", "[A-Z0-9_/]*").replace(r"\#", "[0-9]")
    return re.compile("^" + esc + "$")


def load_blocklist(root, profile):
    max_tier = TIER_ORDER.get(profile, 3)
    entries = []  # (regex, name, category, action)
    folder = os.path.join(root, ".claude", "exceptions")
    if not os.path.isdir(folder):
        return entries
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".md") or fn.lower() == "readme.md":
            continue
        text = open(os.path.join(folder, fn), encoding="utf-8").read()
        tier = (re.search(r"<!--\s*tier:\s*(\w+)", text) or [None, "minimal"])[1].lower()
        action = (re.search(r"<!--\s*action:\s*(\w+)", text) or [None, "deny"])[1].lower()
        if TIER_ORDER.get(tier, 1) > max_tier:
            continue
        title = (re.search(r"^#\s+(.+)$", text, re.M) or [None, fn])[1].strip()
        for line in text.splitlines():
            if not line.startswith("|"):
                continue
            first = line.strip("|").split("|")[0].strip().strip("`")
            if not first or set(first) <= set("-: ") or first.lower() in ("name", "table", "view", "pattern"):
                continue
            for tok in re.split(r"[/,]", first):
                tok = tok.strip().strip("`").split(" ")[0]
                if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*[*#]*|[A-Za-z]#+", tok):
                    entries.append((to_regex(tok), tok.upper(), title, action))
    return entries


def sql_sources(payload):
    """Return the SQL-ish strings to inspect, or [] when the call reads no business data."""
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}
    if tool == "Bash":
        cmd = ti.get("command", "")
        return [cmd] if "datapreview" in cmd else []
    if str(ti.get("action", "")).lower() != "query":
        return []
    params = ti.get("params") or {}
    out = [v for k, v in params.items() if isinstance(v, str) and k.lower() in ("sql_query", "sql", "query", "statement")]
    if isinstance(ti.get("target"), str):
        out.append(ti["target"])
    return out


def referenced_names(sql):
    names = set()
    for m in re.finditer(r"\b(?:FROM|JOIN)\s+(" + IDENT + ")", sql, re.I):
        names.add(m.group(1).upper())
    return names


def main():
    payload = json.load(sys.stdin)
    sources = sql_sources(payload)
    if not sources:
        return
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    profile = load_profile(root)
    entries = load_blocklist(root, profile)
    hits = []
    for src in sources:
        for name in referenced_names(src):
            for rx, pat, cat, action in entries:
                if rx.match(name):
                    hits.append((name, pat, cat, action))
    if not hits:
        return
    decision = "deny" if any(h[3] == "deny" for h in hits) else "ask"
    detail = "; ".join(sorted({f"{n} ({c}, {a})" for n, _, c, a in hits}))
    reason = (
        f"Data-extraction blocklist (profile '{profile}', .claude/exceptions/): {detail}. "
        + ("Refuse the row extraction and offer aggregates without sensitive columns, a Fiori screenshot, "
           "or the functional owner." if decision == "deny" else
           "Protected business data: confirm with the user that this scoped read is needed.")
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # fail open: a broken parser must not block all SAP reads
        print(json.dumps({"systemMessage": f"block-forbidden-tables: parser error, check skipped ({exc})"}))
