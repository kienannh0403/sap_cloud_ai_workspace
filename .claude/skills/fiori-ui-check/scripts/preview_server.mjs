// fiori-ui-check — local Fiori Elements (OData V4) preview of a service that has NO deployed app yet.
// Serves a generated List Report + Object Page app on http://127.0.0.1:<port>/index.html and proxies every
// /sap/... request to the SAP host with the session cookie, so the browser sees one origin (no CORS).
// UI5 is loaded from the official CDN (ui5.sap.com) — needs internet.
//
// node preview_server.mjs --host https://<host> --client 100 --cookies <Netscape cookie file>
//                         --service /sap/opu/odata4/sap/<binding>/srvd/sap/<srvd>/0001/ [--entity <EntitySet>]
//                         [--port 8765] [--table ResponsiveTable|GridTable] [--ui5 https://ui5.sap.com/resources/sap-ui-core.js]
// Prints one JSON line {"url": ..., "entity": ...} when ready. Read-only by design: the proxy refuses every
// request that is not GET/HEAD, except POST $batch whose body contains only GET requests.
import { createServer } from "node:http";
import { readFileSync } from "node:fs";

const a = Object.fromEntries(process.argv.slice(2).reduce((acc, v, i, all) =>
  (v.startsWith("--") ? acc.push([v.slice(2), all[i + 1]]) : acc, acc), []));
for (const k of ["host", "client", "cookies", "service"]) if (!a[k]) { console.error(`missing --${k}`); process.exit(3); }
const HOST = a.host.replace(/\/$/, ""), CLIENT = a.client, PORT = +(a.port || 8765);
// Git Bash (MSYS) rewrites "/sap/..." arguments into "C:/Program Files/Git/sap/..." — cut back to "/sap/"
const svc = a.service.includes("/sap/") ? a.service.slice(a.service.indexOf("/sap/")) : a.service;
const SERVICE = svc.endsWith("/") ? svc : svc + "/";
const UI5 = a.ui5 || "https://ui5.sap.com/resources/sap-ui-core.js";
// table type of the List Report: match the TS / the app to be deployed (FE default = ResponsiveTable)
const TABLE = a.table || "ResponsiveTable";
const hostname = new URL(HOST).hostname;
const COOKIE = readFileSync(a.cookies, "utf8").split(/\r?\n/).flatMap((line) => {
  if (!line || (line.startsWith("#") && !line.startsWith("#HttpOnly_"))) return [];
  const f = line.replace(/^#HttpOnly_/, "").split("\t");
  return f.length >= 7 && hostname.endsWith(f[0].replace(/^\./, "")) ? [`${f[5]}=${f[6]}`] : [];
}).join("; ");

const withParams = (path, lang) => {
  const u = new URL(HOST + path);
  if (!u.searchParams.has("sap-client")) u.searchParams.set("sap-client", CLIENT);
  if (lang && !u.searchParams.has("sap-language")) u.searchParams.set("sap-language", lang);
  return u.toString();
};
const langOf = (req) => (req.headers["accept-language"] || "en").split(/[,;-]/)[0].toUpperCase();

// entity set: explicit, or the only/first entity set of the service
let ENTITY = a.entity;
if (!ENTITY) {
  const meta = await (await fetch(withParams(SERVICE + "$metadata", "EN"), { headers: { cookie: COOKIE } })).text();
  if (!meta.includes("EntityContainer")) { console.error("cannot read $metadata (cookie dead or service not published)"); process.exit(2); }
  const sets = [...meta.matchAll(/<EntitySet Name="([^"]+)"/g)].map((m) => m[1]);
  ENTITY = sets.find((s) => !/VH$|_VH|ValueHelp|VLH$/i.test(s)) || sets[0];
}

const manifest = {
  "_version": "1.59.0",
  "sap.app": { id: "preview.app", type: "application", title: `Preview ${ENTITY}`, applicationVersion: { version: "0.0.1" },
    dataSources: { mainService: { uri: SERVICE, type: "OData", settings: { odataVersion: "4.0" } } } },
  "sap.ui5": {
    dependencies: { minUI5Version: "1.120.0", libs: { "sap.m": {}, "sap.ui.core": {}, "sap.fe.templates": {} } },
    models: { "": { dataSource: "mainService", preload: true,
      settings: { operationMode: "Server", autoExpandSelect: true, earlyRequests: true } } },
    routing: {
      routes: [ { pattern: ":?query:", name: "List", target: "List" },
                { pattern: `${ENTITY}({key}):?query:`, name: "ObjectPage", target: "ObjectPage" } ],
      targets: {
        List: { type: "Component", id: "List", name: "sap.fe.templates.ListReport",
          options: { settings: { contextPath: `/${ENTITY}`, variantManagement: "Page",
            navigation: { [ENTITY]: { detail: { route: "ObjectPage" } } },
            controlConfiguration: { "@com.sap.vocabularies.UI.v1.LineItem": { tableSettings: { type: TABLE } } } } } },
        ObjectPage: { type: "Component", id: "ObjectPage", name: "sap.fe.templates.ObjectPage",
          options: { settings: { contextPath: `/${ENTITY}`, editableHeaderContent: false } } } } } },
  "sap.fiori": { registrationIds: [], archeType: "transactional" },
};
const component = `sap.ui.define(["sap/fe/core/AppComponent"], (AppComponent) =>
  AppComponent.extend("preview.app.Component", { metadata: { manifest: "json" } }));`;
const index = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>Preview ${ENTITY}</title>
<script id="sap-ui-bootstrap" src="${UI5}" data-sap-ui-theme="sap_horizon" data-sap-ui-compat-version="edge"
  data-sap-ui-async="true" data-sap-ui-resource-roots='{"preview.app":"./app/"}'
  data-sap-ui-on-init="module:sap/ui/core/ComponentSupport" data-sap-ui-frame-options="trusted"></script>
<style>html, body { height: 100%; margin: 0; }</style></head>
<body class="sapUiBody sapUiSizeCompact"><div data-sap-ui-component data-name="preview.app" data-id="container"
  data-settings='{"id":"preview"}' data-height="100%" style="height:100%"></div></body></html>`;

const READ_ONLY_BATCH = (body) => !/^(POST|PATCH|PUT|DELETE|MERGE) /m.test(body);
createServer(async (req, res) => {
  try {
    const path = req.url.split("?")[0];
    if (path === "/" || path === "/index.html") { res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); return res.end(index); }
    if (path === "/app/manifest.json") { res.writeHead(200, { "content-type": "application/json" }); return res.end(JSON.stringify(manifest)); }
    if (path === "/app/Component.js") { res.writeHead(200, { "content-type": "application/javascript" }); return res.end(component); }
    if (!path.startsWith("/sap/")) { res.writeHead(404); return res.end(); }
    const chunks = []; for await (const c of req) chunks.push(c);
    const body = Buffer.concat(chunks);
    const isBatch = req.method === "POST" && path.endsWith("$batch");
    if (!["GET", "HEAD"].includes(req.method) && !(isBatch && READ_ONLY_BATCH(body.toString("utf8")))) {
      res.writeHead(403, { "content-type": "text/plain" });
      return res.end("fiori-ui-check preview proxy is read-only: change requests are refused");
    }
    const headers = { ...req.headers, cookie: COOKIE }; delete headers.host; delete headers["accept-encoding"]; delete headers.origin; delete headers.referer;
    const r = await fetch(withParams(req.url, langOf(req)), { method: req.method, headers, body: ["GET", "HEAD"].includes(req.method) ? undefined : body, redirect: "manual" });
    const out = {}; r.headers.forEach((v, k) => { if (!["content-encoding", "content-length", "transfer-encoding", "set-cookie"].includes(k)) out[k] = v; });
    res.writeHead(r.status, out); res.end(Buffer.from(await r.arrayBuffer()));
  } catch (e) { res.writeHead(502); res.end(String(e)); }
}).listen(PORT, "127.0.0.1", () => console.log(JSON.stringify({ url: `http://127.0.0.1:${PORT}/index.html`, entity: ENTITY })));
