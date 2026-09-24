"""Workspace integrity check (rule §14). Run: bash .claude/scripts/integrity-check.sh

Checks, each reported PASS/FAIL with the offending items:
  1. every skill's frontmatter `name:` equals its directory name
  2. every `[Skill: x]` reference resolves to .claude/skills/x/SKILL.md
  3. every subagent's frontmatter `name:` equals its filename
  4. every `[Agent: y]` reference resolves to .claude/agents/y.md
  5. every hook command in .claude/settings.json points to an existing file
  6. the tiered reference layer exists: common/ (3 files), exceptions/ (tier tag in each), configs/<MODULE>/
     for each SAP_ACTIVE_MODULES entry
Exit code 0 = all PASS, 1 = at least one FAIL. Idea from sc4sap tests/validation/*.test.ts.
"""
import json
import os
import re
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
CL = os.path.join(ROOT, ".claude")
# Placeholders used when the rules *explain* the reference syntax, not real references.
PLACEHOLDERS = {"x", "y", "name", "<name>", "skill-name", "agent-name", "...", "…"}
REF_RE = {"Skill": re.compile(r"\[Skill:\s*([^\]\s]+)\s*\]"), "Agent": re.compile(r"\[Agent:\s*([^\]\s]+)\s*\]")}

results = []


def check(title, problems):
    results.append((title, problems))


def frontmatter_name(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return None
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    n = re.search(r"^name:\s*(.+?)\s*$", m.group(1), re.M)
    return n.group(1).strip("'\"") if n else None


def md_files():
    for base in (CL,):
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if d not in ("Documents", "node_modules", ".git")]
            for fn in fns:
                if fn.endswith(".md"):
                    yield os.path.join(dp, fn)
    for fn in ("CLAUDE.md", "README.md"):
        p = os.path.join(ROOT, fn)
        if os.path.isfile(p):
            yield p


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


# 1 + 2 skills
skills_dir = os.path.join(CL, "skills")
skills = sorted(d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d)))
bad = []
for d in skills:
    n = frontmatter_name(os.path.join(skills_dir, d, "SKILL.md"))
    if n != d:
        bad.append(f"{d}: name={n!r}")
check(f"skill name == directory ({len(skills)} skills)", bad)

# 3 agents
agents_dir = os.path.join(CL, "agents")
agents = sorted(f[:-3] for f in os.listdir(agents_dir) if f.endswith(".md"))
bad = []
for a in agents:
    n = frontmatter_name(os.path.join(agents_dir, a + ".md"))
    if n != a:
        bad.append(f"{a}.md: name={n!r}")
check(f"agent name == filename ({len(agents)} agents)", bad)

# 2 + 4 references
known = {"Skill": set(skills), "Agent": set(agents)}
counts = {"Skill": 0, "Agent": 0}
bad = {"Skill": [], "Agent": []}
for path in md_files():
    text = open(path, encoding="utf-8", errors="replace").read()
    for kind, rx in REF_RE.items():
        for m in rx.finditer(text):
            ref = m.group(1).strip("`")
            if ref.lower() in PLACEHOLDERS:
                continue
            counts[kind] += 1
            if ref not in known[kind]:
                line = text.count("\n", 0, m.start()) + 1
                bad[kind].append(f"{rel(path)}:{line} -> [{kind}: {ref}]")
check(f"[Skill: x] references resolve ({counts['Skill']} refs)", bad["Skill"])
check(f"[Agent: y] references resolve ({counts['Agent']} refs)", bad["Agent"])

# 5 hooks in settings.json
bad = []
n_hooks = 0
try:
    settings = json.load(open(os.path.join(CL, "settings.json"), encoding="utf-8"))
    for event, groups in (settings.get("hooks") or {}).items():
        for g in groups:
            for h in g.get("hooks", []):
                n_hooks += 1
                cmd = h.get("command", "")
                m = re.search(r"(\.claude/hooks/[^\s\"']+)", cmd)
                if not m:
                    bad.append(f"{event}: cannot find a .claude/hooks path in {cmd!r}")
                elif not os.path.isfile(os.path.join(ROOT, m.group(1))):
                    bad.append(f"{event}: missing file {m.group(1)}")
except (OSError, ValueError) as exc:
    bad.append(f"settings.json unreadable: {exc}")
check(f"hook commands point to existing files ({n_hooks} hooks)", bad)

# 6 tiered reference layer
bad = []
for f in ("system-config.md", "context-loading-protocol.md", "cloud-abap-constraints.md"):
    if not os.path.isfile(os.path.join(CL, "common", f)):
        bad.append(f"missing .claude/common/{f}")
exc_dir = os.path.join(CL, "exceptions")
if not os.path.isfile(os.path.join(exc_dir, "README.md")):
    bad.append("missing .claude/exceptions/README.md")
for f in sorted(os.listdir(exc_dir)) if os.path.isdir(exc_dir) else []:
    if f.endswith(".md") and f != "README.md":
        if not re.search(r"<!--\s*tier:\s*(minimal|standard|strict)\s*-->", open(os.path.join(exc_dir, f), encoding="utf-8").read()):
            bad.append(f"exceptions/{f}: no valid tier tag")
modules = ""
try:
    cfg = open(os.path.join(CL, "common", "system-config.md"), encoding="utf-8").read()
    m = re.search(r"^SAP_ACTIVE_MODULES=(.*)$", cfg, re.M)
    modules = m.group(1).strip() if m else ""
except OSError:
    pass
for mod in filter(None, re.split(r"[,\s]+", modules)):
    if not os.path.isfile(os.path.join(CL, "configs", mod, "README.md")):
        bad.append(f"module {mod} active but .claude/configs/{mod}/README.md missing")
check(f"reference layer (common/, exceptions/, configs/ for modules={modules or '-'})", bad)

# report
failed = 0
for title, problems in results:
    if problems:
        failed += 1
        print(f"FAIL  {title}")
        for p in problems:
            print(f"        - {p}")
    else:
        print(f"PASS  {title}")
print(f"\nintegrity-check: {len(results) - failed}/{len(results)} PASS")
sys.exit(1 if failed else 0)
