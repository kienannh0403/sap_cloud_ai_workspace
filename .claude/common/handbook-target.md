# Per-target folder and handbook record (rule §4)

## Folder — everything about one report/function in one place
```
artifacts/targets/<TARGET>/          <TARGET> = tcode / app / API name
├── INDEX.md          agent entry point (~2 KB): status, open questions, decisions beyond spec, blockers, file map
├── handbook.json     the user-facing record → rendered into artifacts/handbook/<target>.html
├── fs/               FS as received + fs_markdown.md + extracted images
├── ts/               TS.md
├── build/            ledger (scratchpad.md), drafts, final_source.md, review_verdict.md, ui_checklist.md,
│                     odata_verify/, unit_test/, repro/, handoff_<yyyymmdd>.md
├── forms/            form specs + .xdp/.xlsx + sample data (pdf-/excel-form-template)
├── ddlx/             Metadata Extension sources waiting for manual creation in ADT
├── analysis/         code-analysis / code-review reports
├── ui5/              UI5 project, if any
├── test/             screenshots / exported files the user sent as evidence
├── notes/<topic>.md  per-target findings, each linked from INDEX.md
└── walkthrough*.md   walkthrough.md / walkthrough_bugfix.md / walkthrough_inbound.md …
```
Shared, not per target: `artifacts/handbook/`, `artifacts/documents/` (UM, naming convention),
`artifacts/system_analysis/CDS_RELEASED_CATALOG/`, `artifacts/scratchpads/_session/` (hooks).

## handbook.json — one per target, newest version first
```jsonc
{
  "target": "ZAA01", "title": "Báo cáo tình hình tăng giảm TSCĐ",
  "kind": "Báo cáo | Chức năng | API inbound | API outbound", "module": "FI-AA",
  "status": { "text": "đang test lần 2", "pill": "ok|wrn|dgr|acc|off" },
  "updated": "2026-09-25",
  "purpose": "one paragraph from FS 'Mục đích' / TS §1",
  "objects": [ { "name": "ZR_FI_ZAA01", "type": "CDS root view", "role": "đọc TSCĐ + giá trị kỳ",
                 "uses": ["I_FixedAsset", "I_AssetClass"] } ],     // "uses" draws the diagram edges;
                                                                    // names not in objects = released sources
  "forms": [ { "name": "DEV_F_ZAA01", "type": "PDF", "files": ["forms/DEV_F_ZAA01.xdp"], "status": "preview OK" } ],
  "versions": [ {
      "version": "1.1", "date": "2026-10-02", "source": "bug-fix | create-report | change request",
      "changes": ["Sửa công thức (22) khấu hao lũy kế đầu kỳ: thêm c2 legacy data"],
      "atc": { "date": "2026-10-02", "variant": "ABAP_CLOUD_DEVELOPMENT_DEFAULT", "scope": "mọi object của target",
               "result": "0 findings | <n> findings", "findings": [ { "object": "", "priority": "", "check": "",
               "message": "", "status": "fixed | accepted by user | open" } ] },
      "tests": [ { "title": "Lần 1 — 2026-10-02", "summary": "lần đầu / what changed since the previous attempt",
                   "cases": [ { "id": "TC-01|UI-01|M-01|R-01|UT-01|REG-01", "group": "Data|UI|Manual|Tái hiện|Unit test|Hồi quy",
                                "case": "", "source": "TS §5 / FS …", "input": "", "expected": "", "actual": "",
                                "result": "PASS|FAIL|WAIT|ACCEPTED", "evidence": "build/odata_verify/…" } ] } ] } ]
}
```

## When to write it
| Event | Update |
|---|---|
| First workflow on the target (fs-analytic, code-analysis, bug-fix on an unknown object…) | create folder, `INDEX.md`, `handbook.json` (target, title, kind, module, purpose, status) |
| TS done | `forms` from TS §8, status "TS xong" |
| Every object DONE in a build | append to `objects` with its `uses` |
| Every Phase-2 / bug-fix test attempt | add a `tests` block to the current version (never rewrite older blocks) |
| Build or fix finished | open/close the version: `changes`, and **ATC over every object of the target** (not only the diff) into `atc` |

Then run `python .claude/scripts/handbook/render_target.py <TARGET>` — it writes the page and syncs the nav and
the index cards. Never hand-edit the generated page. No business data in the JSON (counts, field names,
outcomes only — `.claude/exceptions/`).
