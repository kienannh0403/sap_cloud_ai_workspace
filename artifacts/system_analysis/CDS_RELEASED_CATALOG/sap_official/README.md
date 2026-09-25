# SAP official released CDS list (Public Cloud)

**Source:** SAP Cloudification Repository — `github.com/SAP/abap-atc-cr-cv-s4hc`, file `src/objectReleaseInfoLatest.json`
(S/4HANA Cloud Public Edition, latest). SAP last updated it **2026-09-04** (commit "PUC update with latest info #188").
Downloaded **2026-09-25**. This is the list ATC's cloud-readiness check uses: C1 release (use in Cloud Development).

| File | What | Origin |
|---|---|---|
| `objectReleaseInfo_DDLS.json` | every DDLS entry in SAP's JSON (8,111) | downloaded, filtered to `tadirObject == "DDLS"` |
| `descriptions_080.json` | description + package for 8,060 of them | ADT `quickSearch` (objectType `DDLS`) on tenant my437569/080, 2026-09-25 |
| `released_ddls_public_cloud.csv` | flat list, one row per DDLS | **generated** by `../build_catalog.py`, do not hand-edit |

State counts: released 7,893 · deprecated 213 (`successors` = view to use instead) · notToBeReleased 5.

CSV columns: `name, state, application_component, software_component, successors, in_080, package, in_user_file,
description, data_category`. `in_user_file` = view is on the CDS sheet of the user's xlsx; `description` comes from
that xlsx when present, otherwise from 080; `data_category` only from the xlsx.

**Caveats**
- 50 released views are not on tenant 080 (`in_080 = no`), so 080 is on an older release than SAP's list. Don't use them.
- Names are upper case (TADIR key); the CamelCase name comes from the DDLS source.

**Refresh** — `refresh_sap_official.py` (in the catalog folder) does everything:
- `python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/refresh_sap_official.py --check` — compares the date of
  SAP's last commit on the JSON with `sap_last_update` here (~1 s, exit 10 = newer list available).
- without `--check` — if newer: download, filter DDLS, read descriptions on 080 for views that have none (needs a live
  `tools/vsp/cookies_dev.txt`; if dead the catalog still rebuilds, only those descriptions stay empty), run
  `build_catalog.py`, append newly released / no-longer-released views to `changelog.md`. `--force` = even if not newer.
