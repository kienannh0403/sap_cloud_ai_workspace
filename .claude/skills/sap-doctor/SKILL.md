---
name: sap-doctor
description: Health check of this workspace before SAP work or when something behaves oddly — tools (jq, curl, python, git), system-config keys, every SAP MCP server's cookie against ADT discovery (write vs read-only client), hook syntax, settings.json, integrity check, the .claude/.unlock sentinel, uncommitted changes, then a real SAP search on each server; and the cookie-refresh procedure when a cookie is dead. Use at session start / a new day (standing memory check-mcp-alive-each-session), when an SAP call returns an HTML login page or "expected element type ... but have <html>", when a hook errors, or when the user asks "kiểm tra workspace", "sap doctor", "MCP còn sống không", "cookie hết hạn".
---

# SAP Doctor

Read-only. Never sends a query or a write; never prints a cookie value (live credentials).

## Step 1 — shell checks
`bash .claude/scripts/sap-doctor.sh` — prints one line per check (PASS / WARN / FAIL / INFO) and exits 1 on any FAIL.
Quote the FAIL and WARN lines to the user verbatim; do not paraphrase a FAIL into "some issue".

## Step 2 — MCP liveness (the shell cannot see MCP tools)
For each SAP server the script listed with a PASS cookie: `SAP(action="search", target="ZCL_*", params={"maxResults": 1})`
on that server's tool (`mcp__<server>__SAP`, load with `ToolSearch` first — rule §9). A row back = alive.
Never probe with `SAP(action="system", target="INFO")` — it fails on 080 even when healthy (no data-read authorization).
Also report the MCP servers the session start said "failed to connect" or "need authentication" — the user fixes
those with `/mcp` or the claude.ai connector settings; the agent cannot reconnect a server.

## Step 3 — cookie refresh (only when a cookie FAILs)
The agent cannot log in (SSO is the user's). Tell the user, per dead server (URL / client / cookie file from `.mcp.json`):
1. Close Chrome first (`Get-Process chrome` → 0) — a running Chrome makes vsp panic `close of closed channel`. Ask; never kill it.
2. Run from the workspace root, in the background (never pipe through `head`, it kills the poll):
   ```
   env -u SAP_COOKIE_FILE ./tools/vsp/vsp.exe --url "<SAP_URL>" --client <SAP_CLIENT> --mode hyperfocused \
     --browser-auth --browser-auth-timeout 5m \
     --browser-exec "C:/Program Files/Google/Chrome/Application/chrome.exe" \
     --cookie-save "<SAP_COOKIE_FILE>" -v
   ```
   Success line: `Authentication successful! Extracted 2 cookies`.
3. Restart VS Code / Claude Code (or `/mcp reconnect <server>` in a real terminal) — vsp reads the cookie file only at start.
4. Re-run Step 1 and Step 2.
Full background and older failure modes: memory `sap-cloud-dev-connection`.

## Step 4 — report
One short table: check · status · what the user must do (only for FAIL/WARN). A WARN for `.claude/.unlock` or
uncommitted changes is information, not a blocker. SAP work waits until the write server (080) is PASS in Step 1 and alive in Step 2.
