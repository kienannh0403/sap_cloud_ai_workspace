// fiori-ui-check — read-only UI run of a deployed SAP Fiori Elements (OData V4) app in headless Chrome.
// No external libs: Node >= 22 (global WebSocket/fetch) drives Chrome over the DevTools Protocol.
//
// node ui_check.mjs --url <app index.html URL> --cookies <Netscape cookie file> --out <dir> --steps <steps.json>
//                   [--langs VI,EN] [--chrome <chrome.exe>] [--width 1440] [--height 900] [--wait 20000]
// no deployed app yet → preview mode (generated Fiori Elements app over the published service, see preview_server.mjs):
// node ui_check.mjs --service /sap/opu/odata4/sap/<binding>/srvd/sap/<srvd>/0001/ --host https://<host> [--client 100]
//                   [--entity <EntitySet>] [--table ResponsiveTable|GridTable] --cookies … --out … --steps … --wait 30000
//
// steps.json: [{ "do": "<type>", ... }], one screenshot after every step. Types:
//   fill        {field, value}      type into a filter field like a user (focus + text + Enter)
//   fill_date   {field, date}       date "YYYY-MM-DD", typed in the logon language's date format
//   go                              trigger the filter bar search, wait for the table
//   rows        {props:[...]}       row count + distinct values of the listed properties (no other data)
//   columns                         visible column headers of the table
//   actions                         toolbar buttons of the table: text + enabled (never pressed)
//   value_help  {field}             open the field's value help (F4), count entries, close it
//   scroll_right                    scroll the table to its last column
//   open_row    {index}             open the object page of that row (navigation arrow)
//   back                            browser back
//   facets                          object page section titles + header title
//   eval        {js, name}          free read-only JS (rejected if it looks like it presses/executes something)
//   wait        {ms}
// Output in --out: <lang>_<nn>_<step>.png, <lang>_log.json, summary.json. Cookies are never printed.
import { spawn } from "node:child_process";
import { readFileSync, writeFileSync, mkdirSync, rmSync } from "node:fs";
import { join } from "node:path";

const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) =>
  (v.startsWith("--") ? a.push([v.slice(2), all[i + 1]]) : a, a), []));
for (const k of ["cookies", "out", "steps"]) if (!args[k]) { console.error(`missing --${k}`); process.exit(3); }
if (!args.url && !(args.service && args.host)) { console.error("give --url <deployed app> or --service <OData V4 path> --host <https://host> [--client 100] [--entity X] [--table GridTable]"); process.exit(3); }

// PREVIEW MODE (no deployed app): start preview_server.mjs and point the run at it
let previewProc = null;
if (!args.url) {
  const { fileURLToPath } = await import("node:url");
  const { dirname } = await import("node:path");
  const server = join(dirname(fileURLToPath(import.meta.url)), "preview_server.mjs");
  const pArgs = [server, "--host", args.host, "--client", args.client || "100", "--cookies", args.cookies,
    "--service", args.service, "--port", args.port || String(8700 + Math.floor(Math.random() * 200))];
  if (args.entity) pArgs.push("--entity", args.entity);
  if (args.table) pArgs.push("--table", args.table);
  previewProc = spawn(process.execPath, pArgs, { stdio: ["ignore", "pipe", "pipe"] });
  const ready = await new Promise((resolve, reject) => {
    let err = "";
    previewProc.stdout.on("data", (d) => { try { resolve(JSON.parse(d.toString().trim().split("\n")[0])); } catch { /* wait */ } });
    previewProc.stderr.on("data", (d) => { err += d; });
    previewProc.on("exit", (c) => reject(new Error(`preview server exited ${c}: ${err.slice(0, 300)}`)));
  });
  args.url = ready.url;
  console.error(`preview mode: ${ready.url} (entity ${ready.entity}, table ${args.table || "ResponsiveTable"})`);
}
const CHROME = args.chrome || "C:/Program Files/Google/Chrome/Application/chrome.exe";
const LANGS = (args.langs || "VI,EN").split(",");
const W = +(args.width || 1440), H = +(args.height || 900), LOAD_WAIT = +(args.wait || 20000);
const steps = JSON.parse(readFileSync(args.steps, "utf8"));
const FORBIDDEN = /firePress|\.press\(|invokeAction|execute|\.click\(|EditFlow|onCallAction|submitBatch|\bdelete\b|\bcreate\b/i;
for (const s of steps) if (s.do === "eval" && FORBIDDEN.test(s.js)) {
  console.error(`step eval '${s.name || ""}' rejected: looks like it triggers an action — this skill is read-only`); process.exit(3);
}
mkdirSync(args.out, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// framework / preview-mode noise: counted, not listed (Component-preload + FLP metrics only exist in preview mode)
const NOISE = /PropertyInfoValidator|fallback locale|S\/CUBE is not yet supported|Permissions policy violation|favicon|Component-preload|sap-metrics-only|status of 404 \(Not Found\)|status of 403 \(Forbidden\)/;
const HTTP_NOISE = /favicon|Component-preload\.js|sap-metrics-only/;

// in-page helpers (FE V4 / sap.ui.mdc), injected once per page
const HELPERS = `window.__uic = {
  all: (cls) => sap.ui.core.Element.registry.filter((c) => c.isA(cls)),
  fb: () => __uic.all("sap.ui.mdc.FilterBar")[0],
  table: () => __uic.all("sap.ui.mdc.Table").find((t) => t.getDomRef()),
  field: (f) => __uic.all("sap.ui.mdc.FilterField").find((c) => c.getId().endsWith("::FilterField::" + f)
      || (c.getPropertyKey && c.getPropertyKey() === f)),
  msgs: () => sap.ui.getCore().getMessageManager().getMessageModel().getData().map((m) => m.type + ": " + m.message).slice(0, 10),
  dialogs: () => [...document.querySelectorAll(".sapMDialog")].filter((d) => d.offsetParent).map((d) => d.innerText.replace(/\\s+/g, " ").slice(0, 200)),
}`;

async function runLang(lang) {
  const port = 9300 + Math.floor(Math.random() * 600);
  const profile = join(args.out, `.profile_${lang}`);
  const chrome = spawn(CHROME, ["--headless=new", "--disable-gpu", `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`, `--window-size=${W},${H}`, `--lang=${lang.toLowerCase()}`, "about:blank"], { stdio: "ignore" });
  let target;
  for (let i = 0; i < 60 && !target; i++) {
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === "page"); }
    catch { await sleep(250); }
  }
  if (!target) throw new Error("Chrome did not start (check --chrome)");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener("open", r));
  let id = 0; const pending = new Map();
  const log = { lang, console: [], noise: 0, exceptions: [], http: [], steps: [] };
  ws.addEventListener("message", (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; }
    const push = (t) => (NOISE.test(t) ? log.noise++ : log.console.push(t.slice(0, 400)));
    if (m.method === "Runtime.consoleAPICalled" && ["error", "warning"].includes(m.params.type))
      push(`${m.params.type}: ` + m.params.args.map((a) => a.value ?? a.description ?? "").join(" "));
    if (m.method === "Log.entryAdded" && m.params.entry.level === "error") push("log: " + m.params.entry.text);
    if (m.method === "Runtime.exceptionThrown")
      log.exceptions.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 300));
    if (m.method === "Network.responseReceived" && m.params.response.status >= 400 && !HTTP_NOISE.test(m.params.response.url))
      log.http.push(`${m.params.response.status} ${m.params.response.url.slice(0, 200)}`);
  });
  const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const evaluate = async (js) => {
    const r = await send("Runtime.evaluate", { expression: js, awaitPromise: true, returnByValue: true });
    return r.result?.exceptionDetails ? { error: r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text } : r.result?.result?.value;
  };
  const key = async (k, code, vk) => { for (const type of ["keyDown", "keyUp"])
    await send("Input.dispatchKeyEvent", { type, key: k, code, windowsVirtualKeyCode: vk, text: type === "keyDown" && k === "Enter" ? "\r" : undefined }); };
  const shot = async (n) => writeFileSync(join(args.out, `${lang}_${String(n).padStart(2, "0")}.png`),
    Buffer.from((await send("Page.captureScreenshot", { format: "png" })).result.data, "base64"));

  for (const d of ["Network", "Runtime", "Log", "Page"]) await send(`${d}.enable`);
  const host = new URL(args.url).hostname;
  for (const line of readFileSync(args.cookies, "utf8").split(/\r?\n/)) {
    if (!line || (line.startsWith("#") && !line.startsWith("#HttpOnly_"))) continue;
    const f = line.replace(/^#HttpOnly_/, "").split("\t");
    if (f.length < 7 || !host.endsWith(f[0].replace(/^\./, ""))) continue;
    await send("Network.setCookie", { name: f[5], value: f[6], domain: f[0], path: f[2], secure: f[3] === "TRUE", httpOnly: line.startsWith("#HttpOnly_") });
  }
  const url = new URL(args.url); url.searchParams.set("sap-language", lang);
  await send("Page.navigate", { url: url.toString() });
  await sleep(LOAD_WAIT);
  const loaded = await evaluate(`typeof sap !== "undefined" && !!sap.ui.core.Element.registry ? (${HELPERS}, "ui5 ready") : (document.title + " | " + document.body.innerText.slice(0, 200))`);
  log.steps.push({ step: "load", result: loaded, msgs: await evaluate("window.__uic ? __uic.msgs() : []") });
  await shot(0);

  for (const [i, s] of steps.entries()) {
    let res;
    const fieldFocus = (f) => `(() => { const c = __uic.field(${JSON.stringify(f)}); const d = c && c.getFocusDomRef(); if (!d) return "no field ${f}"; d.focus(); return "ok"; })()`;
    switch (s.do) {
      case "fill": case "fill_date": {
        res = await evaluate(fieldFocus(s.field));
        if (res === "ok") {
          const text = s.do === "fill" ? String(s.value) : await evaluate(
            `sap.ui.core.format.DateFormat.getDateInstance().format(new Date(${JSON.stringify(s.date)} + "T00:00:00"))`);
          await send("Input.insertText", { text }); await key("Enter", "Enter", 13);
          res = `typed '${text}'`;
        }
        await sleep(s.wait ?? 1500); break;
      }
      case "go":
        res = await evaluate(`(() => { const fb = __uic.fb(); if (!fb) return "no filter bar"; fb.triggerSearch(); return "search triggered"; })()`);
        await sleep(s.wait ?? 15000); break;
      case "rows":
        res = await evaluate(`(() => { const t = __uic.table(); const rb = t && t.getRowBinding(); const ctx = rb ? rb.getAllCurrentContexts() : [];
          const props = ${JSON.stringify(s.props || [])};
          return { rows: ctx.length, count: rb && rb.getCount ? rb.getCount() : null,
                   distinct: Object.fromEntries(props.map((p) => [p, [...new Set(ctx.map((x) => x.getProperty(p)))].slice(0, 10)])) }; })()`);
        break;
      case "columns":
        res = await evaluate(`(() => { const t = __uic.table(); return t ? t.getColumns().map((c) => c.getHeader()) : "no table"; })()`); break;
      case "actions":
        res = await evaluate(`(() => { const t = __uic.table(); if (!t) return "no table";
          return [...t.getDomRef().querySelectorAll(".sapMTB button")].filter((b) => b.offsetParent && b.innerText.trim())
            .map((b) => b.innerText.trim() + (b.getAttribute("aria-disabled") === "true" || b.disabled ? " (disabled)" : " (enabled)")); })()`); break;
      case "value_help": {
        res = await evaluate(fieldFocus(s.field));
        if (res === "ok") {
          await key("F4", "F4", 115); await sleep(s.wait ?? 5000);
          res = await evaluate(`(() => { const pop = [...document.querySelectorAll(".sapMPopover, .sapMDialog")].filter((p) => p.offsetParent);
            const items = pop.flatMap((p) => [...p.querySelectorAll(".sapMLIB, .sapUiTableRow:not(.sapUiTableRowHidden)")]).filter((x) => x.innerText.trim());
            return { open: pop.length, entries: items.length, first: items.slice(0, 5).map((x) => x.innerText.replace(/\\s+/g, " ").slice(0, 80)) }; })()`);
          await shot(`${String(i + 1).padStart(2, "0")}_vh`);
          await key("Escape", "Escape", 27); await sleep(800);
        }
        break;
      }
      case "scroll_right":
        res = await evaluate(`(() => { const t = __uic.table(); const s = t && [...t.getDomRef().querySelectorAll("div")].find((d) => d.scrollWidth > d.clientWidth + 100 && getComputedStyle(d).overflowX !== "visible");
          if (!s) return "no horizontal scroll"; s.scrollLeft = s.scrollWidth; return "scrolled"; })()`);
        await sleep(1500); break;
      case "open_row":
        res = await evaluate(`(() => { const t = __uic.table(); if (!t) return "no table"; const r = t.getDomRef();
          const icons = [...r.querySelectorAll(".sapUiTableActionIcon")].filter((x) => x.offsetParent);
          const rows = [...r.querySelectorAll("tr.sapMListTblRow")].filter((x) => x.offsetParent)
            .map((tr) => tr.querySelector("td.sapMListTblCell") || tr);
          const el = icons[${s.index ?? 0}] || rows[${s.index ?? 0}]; if (!el) return "no row ${s.index ?? 0}";
          el.dispatchEvent(new MouseEvent("click", { bubbles: true })); return "navigated"; })()`);
        await sleep(s.wait ?? 12000);
        res = { res, hash: await evaluate("location.hash.slice(0, 300)") }; break;
      case "back":
        res = await evaluate("history.back(), 'back'"); await sleep(s.wait ?? 6000); break;
      case "facets":
        res = await evaluate(`(() => ({ header: [...document.querySelectorAll(".sapUxAPObjectPageHeaderTitle, .sapFDynamicPageTitle")].filter((x) => x.offsetParent).map((x) => x.innerText.replace(/\\s+/g, " ").slice(0, 120)),
          sections: [...new Set([...document.querySelectorAll(".sapUxAPObjectPageSectionTitle, .sapUxAPObjectPageSubSectionTitle, .sapUxAPAnchorBar button, .sapUxAPObjectPageSectionHeader .sapMTitle, .sapUxAPObjectPageSubSectionHeader .sapMTitle")]
            .filter((x) => x.offsetParent).map((x) => x.innerText.trim()))].filter(Boolean),
          fields: [...document.querySelectorAll(".sapUxAPObjectPageLayout .sapMLabel")].filter((x) => x.offsetParent).length }))()`); break;
      case "eval":
        res = await evaluate(s.js); await sleep(s.wait ?? 1500); break;
      case "wait":
        await sleep(s.ms ?? 2000); res = "waited"; break;
      default:
        res = `unknown step type '${s.do}'`;
    }
    log.steps.push({ step: `${i + 1} ${s.do} ${s.field || s.name || ""}`.trim(), result: res ?? null, msgs: await evaluate("__uic.msgs()"), dialogs: await evaluate("__uic.dialogs()") });
    await shot(i + 1);
  }
  writeFileSync(join(args.out, `${lang}_log.json`), JSON.stringify(log, null, 1));
  ws.close(); chrome.kill(); await sleep(500);
  try { rmSync(profile, { recursive: true, force: true }); } catch { /* Chrome may still hold files */ }
  return { lang, steps: log.steps.length, console: log.console.length, framework_noise: log.noise,
           exceptions: log.exceptions.length, http_errors: log.http };
}

const summary = [];
for (const lang of LANGS) summary.push(await runLang(lang));
writeFileSync(join(args.out, "summary.json"), JSON.stringify(summary, null, 1));
console.log(JSON.stringify(summary));
if (previewProc) previewProc.kill();
