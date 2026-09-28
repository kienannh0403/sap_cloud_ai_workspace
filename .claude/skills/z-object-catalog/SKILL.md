---
name: z-object-catalog
description: Inventory of the project's existing Z/Y objects (domains, data elements, tables, CDS views, classes, message classes, number ranges, services, BDEFs) per SAP package, kept in artifacts/system_analysis/Z_OBJECT_CATALOG/, so FS analysis and builds reuse what already exists instead of minting duplicates. Use to (a) build or refresh the inventory ("quét package", "cập nhật kho object Z", after a build finishes a target), and (b) look up reuse candidates before designing or creating any new Z object — the fs-analytic TS Coding Implementation Plan, the create-transactional-app reuse probe (Step 0.pre), a new domain/data element/utility class. Triggers include "kho object Z", "object Z có sẵn", "dùng lại", "reuse", "đã có domain nào", "tránh tạo trùng".
---

# Z Object Catalog — reuse before you create

## Why
Each build used to search only its own package, so the same meaning got a second domain (`ZD_STATUS` vs
`ZD_ACTIVE_FLAG`), a second utility class, a second CDS view over the same released source. The catalog lists what
exists across the project's packages once, so the question "does this already exist?" is answered from a file.

## A. Build / refresh (read-only on SAP)
1. Packages to scan: the user's list, or the roots already in `scan_state.json`. Never guess package names — search
   (`SAP(action="search", target="ZFPT*")`) or ask. Local playground packages (`$TMP`, the `ZLOCAL` tree) only if asked.
2. `python .claude/scripts/z_catalog/build_z_catalog.py <PKG> [<PKG> ...]` — recursive into sub-packages, uses the
   write server's cookie (`WRITE_SERVERS`); `--server sap_gm2_cus_ro` to read client 100 instead. Cookie rejected →
   [Skill: sap-doctor] first.
3. Output: `artifacts/system_analysis/Z_OBJECT_CATALOG/objects.csv` + `INDEX.md` + `scan_state.json`. A re-scan
   replaces only the scanned packages. Quote the script's summary line to the user.
4. Refresh after every build that created objects (the target's package) and whenever the user asks.

## B. Look up before creating
1. Read `INDEX.md` (scan dates — a scan older than ~30 days or missing the target package → say so, offer a refresh).
2. Filter `objects.csv` by `reuse_group` and by meaning, not only by name: domains/data elements by the business
   meaning and value set, classes by what they do, CDS views by their released source and grain.
3. Each hit is a **candidate**. Before writing "reuse X" into a TS or a ledger, read X's real definition on SAP
   (domain fixed values, data element type/length, class public methods, CDS source) — rule §2, never infer from the
   name or description. A candidate in another team's package: reuse is fine for DDIC types and released-to-package
   objects; if the package interface does not expose it, report it instead of copying it.
4. Record the decision: in the TS §9 row ("reuse ZD_STATUS — fixed values A/I checked on 080 <date>") or the build
   ledger (reused vs newly created). No candidate → say "catalog checked <date>, nothing comparable".

## Limits
The catalog is a snapshot: objects created after the last scan are invisible until the next scan. Descriptions come
from SAP short texts and can be empty or misleading — that is why step B3 exists.
