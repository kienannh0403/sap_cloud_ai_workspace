# Document Creation Pattern — creating a standard SAP document from custom code (Tier 4)

Loaded when a TS row or a build step **creates or changes a standard SAP document** (sales order, material document,
journal entry, billing document, production order confirmation…) from custom code: a RAP action, an Excel upload,
an inbound API handler (`/sap-dev-api-inbound`), an application job. Not for Z tables only — saving into our own
table is ordinary RAP (`rap`). Adapted from StormShynn/sap-abap-agent `docs/sap-knowledge/document-creation-pattern.md`
(MIT), corrected for Public Cloud: that source put released BAPIs first; SAP's list says otherwise (below).

## 1. Choose the interface — first match wins, verify each in the index

| # | Interface | Use when | Check in |
|---|---|---|---|
| 1 | **EML on a released BDEF** — `MODIFY ENTITIES OF <I_xxxTP> ENTITY … CREATE / EXECUTE` | the document's BO has a released BDEF with the operation you need | `CDS_RELEASED_CATALOG/released_objects/BDEF.csv`, then read the BDEF on ADT for its operations, actions and numbering |
| 2 | **Standard OData / SOAP API** over a Communication Arrangement | no released BDEF, the BDEF lacks the operation, or the number is needed synchronously but the BDEF uses late numbering | decision ladder rung 5b; api.sap.com filtered on S/4HANA Cloud Public Edition; [Skill: odata] |
| 3 | **Released function module** | only when it is in `released_objects/FUGR.csv` with state `released` | 41 released in total (2026-09-04), mostly technical (`BAPI_TRANSACTION_COMMIT`, `BALW_*`) |

Classic document BAPIs are **not** released for Public Cloud; SAP names the BDEF that replaces them — e.g.
`BAPI_GOODSMVT_CREATE` → `I_MATERIALDOCUMENTTP`, `BAPI_ACC_DOCUMENT_POST` → `I_JOURNALENTRYTP` (`notToBeReleased`,
`successors` column of `FUGR.csv`). Never plan on a BAPI because it is familiar; never read or write the standard
table directly (rule §3). Nothing fits → decision ladder sub-ladder 5c/5d.

## 2. Nine mandatory steps, whatever the trigger

1. **Validate input** before calling SAP: mandatory fields, types and lengths, master data exists (read via released
   CDS), business rules from the FS. Reject early with a message per row — not one generic error for the batch.
2. **Map** input → interface parameters (EML entity / API payload). Keep the mapping in its own method or class
   (`ZCL_<target>_*`) so it can be unit-tested without SAP ([Skill: abap-unit-testing], `CL_ABAP_TESTDOUBLE` for the
   call, `CL_BOTD_*` for a BO).
3. **Call** the interface.
4. **Read the errors where they actually are**: EML → `FAILED` + `REPORTED` (messages per `%cid` / key); OData/SOAP →
   HTTP status **and** the message body; released FM → its `RETURN` table (type E/A = error). A call without an
   exception is not a success.
5. **Commit or roll back, in the right place**:
   - inside a RAP handler or saver (action, determination, validation): **never** `COMMIT ENTITIES` / `COMMIT WORK` —
     the framework commits the whole LUW, and EML on a standard BO joins that same LUW (`IN LOCAL MODE` is only for
     changing our own BO without its authorization/feature checks);
   - outside RAP (application job, `IF_OO_ADT_CLASSRUN`, inbound handler not running inside a BO): `COMMIT ENTITIES`
     then check `sy-subrc` and the `RESPONSE OF` failed/reported; `ROLLBACK ENTITIES` on error before anything else;
   - OData/SOAP API: the remote call commits its own LUW — design so that a later failure in our code does not leave
     the remote document orphaned (record it, see step 8).
6. **Capture the document number**. EML on a late-numbering BO gives only `%pid` before save — the final key exists
   only in the save phase (`CONVERT KEY OF … FROM %pid`, or `MAPPED` of `COMMIT ENTITIES` outside RAP), never inside
   an action handler. Need it at once inside a RAP action → rung 5b.
7. **Prevent duplicates (idempotency)**: a retry, a double click or a re-sent inbound message must not create a
   second document. Key the call on a business key (external reference, upload file + row, inbound message ID),
   store it with the resulting document number in our Z log table, and look it up before calling again.
8. **Log the outcome** per document: business key, document number or error messages, timestamp, user. Reuse the
   project's log objects before building one ([Skill: z-object-catalog]; an inbound API logs through `Z_API_FWK`).
9. **Return a result the caller can act on**: per row / per message — created number, or the exact SAP message —
   never only "done" or "error".

## 3. How the TS records it

A TS row that creates a document states: interface chosen (# above + object name + its state from the index),
business key used for idempotency, where the result is logged, and the commit point. Missing any of these is a TS
gap — go back to the user (rule §6), do not decide it while coding.
