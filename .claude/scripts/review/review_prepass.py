"""review_prepass.py - deterministic pre-pass for /sap-dev-code-review (idea from alibaba/open-code-review:
determinism for what can be matched, the LLM only for judgement).

Scans ABAP source files already saved on disk and lists CANDIDATES with file:line. A candidate is not a finding:
the reviewer must disposition every one (finding, or "ĐÃ XEM XÉT" with a one-line reason) in the report.

  python -X utf8 .claude/scripts/review/review_prepass.py --target ZSD01
  python -X utf8 .claude/scripts/review/review_prepass.py --target ZSD01 --src path/to/zcl_x.abap --src dir/

Default --src: artifacts/targets/<TARGET>/build/review_src/ (every file in it).
Writes artifacts/targets/<TARGET>/build/review_prepass.json + review_prepass.md; console = one line per rule.

Rules (ids match the Security checklist S1-S8 of sap-dev-code-review.md where they overlap):
  P1 SELECT inside LOOP/DO/WHILE/SELECT-loop      P2 EML (READ/MODIFY/COMMIT ENTITIES) inside a loop
  P3 SELECT *                                      P4 SELECT without WHERE (not SINGLE / not UP TO)
  S1 dynamic WHERE / FROM / ORDER BY ( ... )       S3 secret-shaped name assigned a literal, URL with user:pass@
  S5 secret-shaped name inside MESSAGE / log call  S7 PUBLIC methods of a global class (list, LLM judges)
  R1 CATCH cx_root / cx_static_check broad catch   R2 empty CATCH block
  M1 legacy statement (MOVE, COMPUTE, CALL METHOD, CREATE OBJECT, CONCATENATE, REFRESH, FORM/PERFORM, ...)
  M2 method longer than --max-method-lines (default 80) source lines

Blind spots (state them in the report): pattern matching only - a SELECT reached from a loop through a helper
method call, dynamic code, macros, and CDS/BDEF sources (listed as "not scanned") are not analysed.

Exit: 0 scan done (candidates or not - they are not verdicts) · 2 input error (no source file found).
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]

SECRET = r"(?:password|passwd|pwd|secret|api_?key|token|client_?secret|private_?key|session_?id|cookie|credential)"
LEGACY = [
    (r"^MOVE\s", "MOVE -> use ="),  # MOVE-CORRESPONDING is not obsolete
    (r"^COMPUTE\b", "COMPUTE -> plain expression"),
    (r"^CALL METHOD\b", "CALL METHOD -> functional call obj->meth( )"),
    (r"^CREATE OBJECT\b", "CREATE OBJECT -> NEW #( )"),
    (r"^CONCATENATE\b", "CONCATENATE -> string template |...| or &&"),
    (r"^REFRESH\b", "REFRESH -> CLEAR"),
    (r"^(?:FORM|PERFORM)\b", "FORM/PERFORM -> methods"),
    (r"^DESCRIBE TABLE\b", "DESCRIBE TABLE -> lines( )"),
    (r"^(?:ADD|SUBTRACT|MULTIPLY|DIVIDE)\b", "arithmetic keyword -> operator / +="),
    (r"^TRANSLATE\b.*\b(?:TO UPPER|TO LOWER) CASE\b", "TRANSLATE -> to_upper( ) / to_lower( )"),
    (r"^CONDENSE\b", "CONDENSE -> condense( )"),
    (r"\bOCCURS\b|\bWITH HEADER LINE\b", "header line / OCCURS table"),
]
LOOP_OPEN = re.compile(r"^(?:LOOP\b|DO\b|WHILE\b)")
LOOP_CLOSE = re.compile(r"^(?:ENDLOOP|ENDDO|ENDWHILE|ENDSELECT)\b")
EML = re.compile(r"^(?:READ ENTITIES|READ ENTITY|MODIFY ENTITIES|MODIFY ENTITY|COMMIT ENTITIES)\b")


def statements(text):
    """Split ABAP source into statements: (start_line, raw, code). code = raw with literal contents removed,
    upper-cased, whitespace collapsed. Comments (* in column 1, " to end of line) are dropped."""
    out, raw, code, start = [], [], [], None
    quote = None  # ' ` or |
    for no, line in enumerate(text.splitlines(), 1):
        if line.startswith("*") and quote is None:
            continue
        i = 0
        while i < len(line):
            ch = line[i]
            if quote:
                raw.append(ch)
                if ch == quote:
                    if i + 1 < len(line) and line[i + 1] == quote and quote != "|":  # escaped '' or ``
                        raw.append(line[i + 1])
                        i += 2
                        continue
                    quote = None
                    code.append(ch)
                i += 1
                continue
            if ch == '"':
                break
            if start is None and not ch.isspace():
                start = no
            if ch in "'`|":
                quote = ch
                raw.append(ch)
                code.append(ch)
            elif ch == ".":
                if start is not None:
                    c = re.sub(r"\s+", " ", "".join(code)).strip().upper()
                    out.append((start, "".join(raw).strip(), c))
                raw, code, start = [], [], None
            else:
                raw.append(ch)
                code.append(ch)
            i += 1
        if quote == "|":  # string templates may span lines; ' and ` may not
            raw.append("\n")
        else:
            quote = None
            raw.append(" ")
            code.append(" ")
    return out


def is_cds(text):
    return re.search(r"^\s*(?:@|define\s+(?:root\s+)?(?:view|table|behavior|abstract|custom|service)|"
                     r"managed|unmanaged|projection)", text, re.I | re.M) is not None and \
        re.search(r"^\s*(?:CLASS|METHOD|REPORT|FUNCTION|INTERFACE)\b", text, re.I | re.M) is None


def scan(path, max_method_lines):
    text = path.read_text(encoding="utf-8", errors="replace")
    if is_cds(text):
        return None
    stmts = statements(text)
    found = []

    def add(rule, line, msg, snippet):
        found.append({"rule": rule, "file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                      "line": line, "message": msg, "snippet": snippet[:160]})

    endselects = sum(1 for _, _, c in stmts if c.startswith("ENDSELECT"))
    depth, loop_line = 0, []
    method, method_start = None, 0
    in_public, cls_public = False, False
    for idx, (line, raw, c) in enumerate(stmts):
        # method boundaries reset loop tracking
        m = re.match(r"^METHOD (\S+)", c)
        if m:
            method, method_start, depth, loop_line = m.group(1), line, 0, []
        elif c.startswith("ENDMETHOD"):
            if method and line - method_start > max_method_lines:
                add("M2", method_start, f"method {method} spans {line - method_start} lines", f"METHOD {method}")
            method = None
        # class public section
        if re.match(r"^CLASS \S+ DEFINITION\b", c):
            cls_public = " PUBLIC" in c and " DEFERRED" not in c
            in_public = False
        if c.startswith("PUBLIC SECTION"):
            in_public = cls_public
        elif re.match(r"^(?:PROTECTED SECTION|PRIVATE SECTION|ENDCLASS)", c):
            in_public = False
        elif in_public and re.match(r"^(?:CLASS-)?METHODS\b", c):
            names = re.findall(r"(?:^(?:CLASS-)?METHODS:?\s*|,\s*)([A-Z_][A-Z0-9_]*)", c)
            for n in names or ["?"]:
                add("S7", line, f"public method {n} - confirm it has a consumer", raw)

        # loops
        is_select = c.startswith("SELECT")
        if LOOP_CLOSE.match(c):
            depth = max(depth - 1, 0)
            loop_line = loop_line[:-1]
        if is_select and depth:
            add("P1", line, f"SELECT inside loop opened at line {loop_line[-1]}", raw)
        if EML.match(c) and depth:
            add("P2", line, f"EML inside loop opened at line {loop_line[-1]} - collect keys, one call", raw)
        if LOOP_OPEN.match(c):
            depth += 1
            loop_line.append(line)
        elif is_select and endselects and "SINGLE" not in c.split("FROM")[0] and " TABLE " not in f" {c} ":
            depth += 1
            loop_line.append(line)
            endselects -= 1

        # SQL shape
        if is_select:
            if re.match(r"^SELECT (?:SINGLE )?(?:DISTINCT )?\*", c) or re.search(r"\bFIELDS \*", c):
                add("P3", line, "SELECT * - list the fields needed", raw)
            if " WHERE " not in f" {c} " and "SINGLE" not in c.split("FROM")[0] and "UP TO" not in c \
                    and not re.search(r"\bFROM @", c):  # FROM @itab = internal table, not a DB read
                add("P4", line, "SELECT without WHERE - full read of the source", raw)
        # dynamic token = parenthesised single variable, e.g. WHERE (lv_where), FROM (lv_tab), SELECT (lv_fields);
        # only in SQL statements - EML "FIELDS ( a b )" and itab "DELETE lt WHERE ( ... )" are not dynamic SQL
        if re.match(r"^(?:SELECT|WITH|UPDATE|DELETE FROM|MODIFY [A-Z]\w* FROM|INSERT [A-Z]\w* FROM)", c) and \
                re.search(r"(?:^SELECT|\bWHERE|\bFROM|\bORDER BY|\bGROUP BY|\bFIELDS|\bSET)\s*\(\s*[A-Z_][\w\-~>]*\s*\)", c):
            add("S1", line, "dynamic SQL clause - confirm input cannot reach it unchecked", raw)

        # secrets
        if re.search(rf"\b\w*{SECRET}\w*\s*(?:=|TYPE \S+ VALUE)\s*['`|]", raw, re.I):
            add("S3", line, "secret-shaped name assigned a literal", raw)
        if re.search(r"\w+://[^/\s:@'`|]+:[^/\s@'`|]+@", raw):
            add("S3", line, "URL with embedded user:password", raw)
        if (c.startswith("MESSAGE") or re.search(r"->(?:ADD|ADD_MESSAGE|ADD_TEXT|ADD_ITEM)\w*\(", c)) \
                and re.search(SECRET, raw, re.I):
            add("S5", line, "secret-shaped name inside a message / log call", raw)

        # exceptions
        if re.match(r"^CATCH\b", c):
            if re.search(r"\bCX_ROOT\b|\bCX_STATIC_CHECK\b|\bCX_DYNAMIC_CHECK\b|\bCX_NO_CHECK\b", c):
                add("R1", line, "broad CATCH - confirm it logs / re-raises", raw)
            nxt = stmts[idx + 1][2] if idx + 1 < len(stmts) else ""
            if re.match(r"^(?:ENDTRY|CATCH|CLEANUP)\b", nxt) and "##NO_HANDLER" not in c:  # pragma = deliberate
                add("R2", line, "empty CATCH block - exception swallowed", raw)

        # legacy
        for pat, msg in LEGACY:
            if re.search(pat, c):
                add("M1", line, msg, raw)
                break
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", required=True)
    ap.add_argument("--src", action="append", help="file or directory (repeatable)")
    ap.add_argument("--max-method-lines", type=int, default=80)
    a = ap.parse_args()

    build = ROOT / "artifacts" / "targets" / a.target / "build"
    srcs = [Path(s) for s in a.src] if a.src else [build / "review_src"]
    files = []
    for s in srcs:
        s = s if s.is_absolute() else (Path.cwd() / s)
        files += sorted(p for p in s.rglob("*") if p.is_file()) if s.is_dir() else ([s] if s.is_file() else [])
    if not files:
        print(f"no source file found in {', '.join(map(str, srcs))} (exit 2)")
        return 2

    candidates, scanned, skipped = [], [], []
    for f in files:
        r = scan(f.resolve(), a.max_method_lines)
        (skipped if r is None else scanned).append(f.name)
        candidates += r or []

    build.mkdir(parents=True, exist_ok=True)
    result = {"target": a.target, "scanned": scanned, "not_scanned_cds_or_bdef": skipped,
              "candidates": candidates}
    (build / "review_prepass.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    rules = sorted({c["rule"] for c in candidates})
    md = [f"# Review pre-pass — {a.target}", "",
          f"Scanned: {', '.join(scanned) or '-'}  ", f"Not scanned (CDS/BDEF): {', '.join(skipped) or '-'}  ",
          f"Candidates: {len(candidates)} — every one needs a disposition in the review report "
          "(finding, or ĐÃ XEM XÉT + reason).", "",
          "| # | Rule | File:Line | Message | Code | Disposition |", "|---|---|---|---|---|---|"]
    for i, c in enumerate(candidates, 1):
        snip = c["snippet"].replace("|", "\\|")
        md.append(f"| {i} | {c['rule']} | {Path(c['file']).name}:{c['line']} | {c['message']} | `{snip}` | |")
    (build / "review_prepass.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"scanned {len(scanned)} file(s), skipped {len(skipped)} CDS/BDEF, {len(candidates)} candidate(s)")
    for r in rules:
        print(f"  {r}: {sum(1 for c in candidates if c['rule'] == r)}")
    print(f"-> {(build / 'review_prepass.md').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
