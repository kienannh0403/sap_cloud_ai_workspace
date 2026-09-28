---
name: ask-consultant
description: Quick functional Q&A with an SAP Public Cloud module consultant (SD, FI, CO, MM, PP, QM, PM, PS, TM, EWM, TR) answered against THIS workspace's configuration — active modules, country vn, released objects, the project's Z objects — read-only, no FS/TS needed. Use when the user asks a business/process/configuration question rather than asking to build something, e.g. "quy trình bán hàng trả lại chạy thế nào", "partner determination là gì", "báo cáo tăng giảm TSCĐ lấy từ đâu", "Public Cloud có tách cost center theo profit center không", "hỏi consultant FI", "hỏi nghiệp vụ".
---

# Ask Consultant — business questions, answered from sources

Read-only: no SAP write, no business-data query (a question that needs real data → say which released view would
answer it and ask the user before any read, `.claude/exceptions/`).

## Step 1 — route
Pick the module(s) from the question's words (billing/delivery/pricing → SD; GL/AR/AP/assets/tax → FI; cost center,
product costing → CO; purchasing/inventory → MM; production/BOM/routing → PP; inspection → QM; maintenance → PM;
project → PS; freight → TM; warehouse → EWM; cash/bank/treasury → TR). Only modules in `SAP_ACTIVE_MODULES`;
another module → say it is out of this workspace's scope. Unclear → one question to the user.

## Step 2 — read the minimum, in this order
1. `.claude/configs/<MODULE>/README.md`, then the one topic file the question needs (released-objects, functional).
2. The matching `sap-process-*` skill for process questions (O2C, supply chain, manufacturing, production planning,
   finance, project) — its `references/deep-dive.md` only when the SKILL.md does not answer it.
3. Vietnam-specific (tax, invoice, statutory, VND, fixed-asset rules) → `.claude/country/vn.md`.
4. "Which view / API gives X" → `artifacts/system_analysis/CDS_RELEASED_CATALOG/` ([Skill: find-released-cds-view]);
   "do we already have a Z object for X" → [Skill: z-object-catalog].
5. Still open and it matters → `sap-docs-upstream` search (if connected), cite the page.

## Step 3 — answer
Short, in Vietnamese, business language first, SAP terms in brackets. Every claim carries its source (config file,
skill, catalog row, SAP doc page); anything not found in a source is labelled "theo kiến thức chung, chưa kiểm trên
tenant" — never presented as the tenant's configuration (SSCUI / Fiori apps / flexible workflow of this tenant are
unverified, see the module READMEs). End with what would confirm it on the system, if relevant.

## When to hand off instead
- The question is really a requirement ("làm báo cáo …") → `/sap-dev-fs-analytic` or the matching workflow.
- A judgment-heavy analysis tied to an existing target (FS clarification, impact of a process change on ZAA01) →
  dispatch [Agent: consultant-lead] with input paths and output `artifacts/targets/<TARGET>/build/consult_<yyyymmdd>.md`,
  then read that file before answering (rule §12).
- A worthwhile answer about a specific target → one `notes/<topic>.md` in that target, linked from its INDEX.md.
