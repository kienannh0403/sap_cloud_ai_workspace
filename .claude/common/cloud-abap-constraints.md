# Cloud ABAP Constraints (Tier 3)

**Load when**: `SAP_VERSION=S4_CLOUD_PUBLIC` (always true in this workspace — see `system-config.md`) AND the
task writes, reviews, or designs ABAP/CDS code. Adapted from sc4sap `common/cloud-abap-constraints.md`
(MIT, v0.6.18). Every replacement class below was checked on 2026-09-23 with
`sap-docs-upstream` `sap_get_object_details(system_type="public_cloud")` against SAP's API release-state
repository (SAP/abap-atc-cr-cv-s4hc). "Released (A)" = found, state `released`, Clean Core level A.
Anything not marked that way is **unverified** — check it the same way before using it.

**Draft check before Push:** `python -X utf8 .claude/scripts/released_check.py <draft file or build/ folder>`
looks up every standard class, interface, CDS view, BDEF and called function module the draft names in the local
copy of SAP's list (`CDS_RELEASED_CATALOG/`), and prints deprecated ones with their successor. Exit 0 = nothing to
fix. It knows names only — ATC (activation-guard Gate 4) still decides on statements.

Classic features on the left are **not available** in ABAP for Cloud Development; propose the right-hand
equivalent instead (fail fast — do not try to "make it work").

## Prohibited statements / features

| Category | Classic ABAP | Cloud ABAP |
|---|---|---|
| File system | `OPEN/CLOSE/READ/TRANSFER DATASET` | Not available |
| DB access | `EXEC SQL`, native `CURSOR`, `CLIENT SPECIFIED`; SELECT on SAP tables | Released CDS views only (rule §3) |
| System access | `CALL 'C-function'`, `SYSTEM-CALL` | Not available |
| Screens | Dynpro (`CALL SCREEN`, `PF-STATUS`, `LOOP AT SCREEN`), selection screens, `WRITE` lists | Fiori Elements / UI5 on RAP |
| Reports | Executable programs + event blocks (`START-OF-SELECTION`, `INITIALIZATION`, …) | Class with `if_oo_adt_classrun` (dev test) or RAP app / Application Job |
| Legacy syntax | `WITH HEADER LINE`, `TABLES` declarations, `ADD/SUBTRACT/MULTIPLY/DIVIDE` | Modern syntax (rule §3) |
| Enhancements | `ENHANCEMENT-POINT`, user exits, modifications | Released BAdIs (Developer / Key User extensibility) |
| Debug | `BREAK-POINT` in code | ADT debugger |
| Regex | POSIX `REGEX` | `PCRE` |

## API replacements

| Need | Classic | Cloud replacement | Release check |
|---|---|---|---|
| Parallel processing | `CALL FUNCTION … STARTING NEW TASK` | `CL_ABAP_PARALLEL` | Released (A) |
| System date/time/timezone | `sy-datum`, `sy-uzeit`, `sy-zonlo` | `CL_ABAP_CONTEXT_INFO=>get_system_date( )` / `get_system_time( )` / `get_user_time_zone( )` | Released (A) |
| Date/time formatting | `CONVERT_DATE_TO_EXTERNAL`, `DATE_CHECK_PLAUSIBILITY` | `CL_ABAP_DATFM` (+ `cl_abap_timefm`, `cl_abap_tstmp`) | `CL_ABAP_DATFM` Released (A); others unverified |
| Factory / holiday calendar | `FACTORYDATE_CONVERT_TO_DATE`, `HOLIDAY_CHECK_AND_GET_INFO` | `CL_FHC_CALENDAR_RUNTIME` | Released (A) |
| General calendar | `MONTH_NAMES_GET`, `DATE_GET_WEEK` | `CL_SCAL_UTILS` | Released (A) |
| Call stack | `SYSTEM_CALLSTACK` | `XCO_CP_CALL_STACK` | Released (A) |
| DDIC metadata | SELECT on DD02L/DD03L… | `XCO_CP_ABAP_DICTIONARY` family | unverified |
| Excel read/write | `GUI_UPLOAD`, `ALSM_EXCEL_TO_INTERNAL_TABLE` | `XCO_CP_XLSX` | Released (A) |
| Exchange rates | SELECT TCURR | `CL_EXCHANGE_RATES` | Released (A) |
| Unit of measure | `UNIT_CONVERSION_SIMPLE` | `CL_UOM_CONVERSION`, `CL_UOM_MAINTENANCE` | Released (A) |
| Number ranges | SNRO, `NUMBER_GET_NEXT` | `CL_NUMBERRANGE_RUNTIME`, `CL_NUMBERRANGE_OBJECTS` + "Manage Number Range Intervals" app | Released (A) |
| Locks | `ENQUEUE_*` / `DEQUEUE_*` | `CL_ABAP_LOCK_OBJECT_FACTORY` (RAP handles locks itself for BOs) | Released (A) |
| Background jobs | SM36, `JOB_OPEN/SUBMIT/CLOSE` | Application Job: `CL_APJ_DT_CREATE_CONTENT` (template), `CL_APJ_RT_API` (schedule) | Released (A) |
| XML | `SMUM_XML_PARSE` | `CL_SXML_STRING_READER` / writer, transformations | Released (A). *sc4sap's `cl_demo_xml_access` is NOT released — removed* |
| SOAP consumer | SPROXY / SOAMANAGER | Outbound service + communication scenario, `CL_SOAP_DESTINATION_PROVIDER` | Released (A) |
| RFC / HTTP out | SM59 destinations | Communication scenario + arrangement, `CL_HTTP_DESTINATION_PROVIDER` | unverified (see skill `btp-abap-environment`) |
| Translation | SE63 | "Maintain Translations" app, `XCO_CP_I18N` | Released (A) |
| Forms / printing | SAPscript, SmartForms, `OPEN_FORM` | Adobe Forms service + output management, `CL_PRINT_QUEUE_UTILS` | Released (A) |
| Change documents | SELECT CDHDR/CDPOS | Change document object + generated class; read via released CDS | unverified |
| Memory | `EXPORT/IMPORT … MEMORY ID` | `EXPORT/IMPORT … DATA BUFFER / INTERNAL TABLE` | language statement — see `abap-docs-cloud` |
| Authorization / roles | PFCG, SU01 | IAM app, business catalog, restriction types, DCL (skill `authorization-iam`) | n/a |
| Transport | SE09/SE10 | ADT transport organizer — **never create/modify a TR** (rule §2) | n/a |

## Program structure

No freestyle reports. Put logic in a class method. To run a class in ADT, implement `if_oo_adt_classrun`
(test/dev utility only — not a user-facing app):

```abap
CLASS zcl_demo_run DEFINITION PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_oo_adt_classrun.
ENDCLASS.

CLASS zcl_demo_run IMPLEMENTATION.
  METHOD if_oo_adt_classrun~main.
    out->write( |Hello from { cl_abap_context_info=>get_system_date( ) }| ).
  ENDMETHOD.
ENDCLASS.
```

## Redirect table

| User asks for | Build instead | Workflow |
|---|---|---|
| Report / list | RAP read-only app (Fiori Elements List Report) over released CDS | `/sap-dev-fs-analytic` → `/sap-dev-create-report` |
| CRUD screen | RAP managed BO + Fiori Elements | `/sap-dev-fs-analytic-transactional-app` → `/sap-dev-create-transactional-app` |
| Batch job | Application Job template + catalog | skill `released-abap-classes` |
| Interface / integration | Communication scenario + service binding / outbound service | `/sap-dev-api-inbound`, `/sap-dev-api-outbound` |
| Standard-logic change | Released BAdI (skill `badi-enhancement`) | — |
