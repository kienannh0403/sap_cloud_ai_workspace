---
name: package-to-process
description: Reverse-engineer a custom Z package on SAP Public Cloud into an end-to-end business-process document for consultants and key users — which apps/services/reports it offers, which business documents flow through it (e.g. request → order → goods movement → invoice), with a Mermaid flowchart and sequence diagram and one table per step (actor, app/service, Z objects, released SAP objects read or written). Read-only. Use when the user asks "package này làm quy trình gì", "vẽ quy trình từ package", "tài liệu nghiệp vụ cho package Z", "business process của các object Z", "package to process", or needs to onboard someone onto an existing custom solution. For a single object's technical deep-dive use /sap-dev-code-analysis instead.
---

# Package → Process

Output is for people who know the business, not the code: process first, objects second.

## Step 1 — inventory
1. `artifacts/system_analysis/Z_OBJECT_CATALOG/objects.csv` for the package ([Skill: z-object-catalog]); package not
   scanned or scan older than ~30 days → run the catalog script for it first (read-only).
2. Entry points = what a user or another system can call: service bindings (`SRVB`) and their service definitions
   (`SRVD`) — each exposed entity set is a candidate app/API; application jobs; RAP BOs (`BDEF`) with actions;
   classes registered as inbound/outbound APIs (Z_API_FWK handler classes).
   Everything else (DDIC, helper classes, CDS without a service) is supporting material.
3. Cookie dead → [Skill: sap-doctor]. Never read business data for this; structure and source only.

## Step 2 — trace each entry point (read sources, do not guess from names)
For every entry point: `SAP(action="read", …)` the service definition → projection → root view → BDEF / behavior
pool; note (a) released SAP views/BOs read (`I_…`), (b) released BOs written via EML (`MODIFY ENTITIES OF I_…`),
(c) Z tables written, (d) actions/determinations/validations with their business meaning, (e) calls to other entry
points. `analyze type=callees` / `references` help find the chain. Record for each fact the object and line it came from.

## Step 3 — group into processes
Group entry points by the business document they create or change (sales order, delivery, purchase requisition,
production order, journal entry, asset…) and order them by document flow. Use the matching `sap-process-*` skill as the
reference for the standard flow, and mark where the custom package plugs into it (before / after / instead of a
standard step). A step whose purpose the sources do not reveal → an open question, not an invented purpose.

## Step 4 — write the document
`artifacts/system_analysis/PACKAGE_PROCESS/<PACKAGE>/process_<yyyymmdd>.md` (Vietnamese, SAP terms in brackets):
1. Purpose of the package (one paragraph) and the processes found.
2. Per process: Mermaid `flowchart LR` (actors, apps, documents, SAP standard steps shaded differently from Z steps),
   Mermaid `sequenceDiagram` for the main path, a step table: # · actor · app/service · action · Z objects ·
   released SAP objects read/written · source reference.
3. Object map: every Z object of the package → the process step(s) using it; objects used by no process → listed as
   "không thuộc quy trình nào" (candidates for cleanup, the user decides).
4. Open questions.
Validate the Mermaid blocks parse (balanced brackets, no raw `(`/`)` inside node labels — quote them). Offer the
handbook: a report the user wants kept can be linked from `artifacts/handbook/index.html` on request.
