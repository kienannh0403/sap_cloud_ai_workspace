"""Cross-check view names verified in the SAP-CODE-GEN knowledge pack against this catalog.

Run from the workspace root:
    python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/verified_external/cross_check.py

Read-only: prints where each externally-verified view landed (catalog / fields-only / absent).
Does not touch catalog_all.csv or modules/ — those stay generated only by build_catalog.py.
"""
import csv
import os

BASE = os.path.join(os.path.dirname(__file__), "..")

# name -> (external released state, source module file, note)
# "released" / "released, deprecated" / "NOT released despite #PUBLIC_LOCAL_API"
EXTERNAL = {
    "I_COMPANYCODE": ("released", "FI"), "I_JOURNALENTRY": ("released", "FI"),
    "I_OPERATIONALACCTGDOCITEM": ("released", "FI"), "I_JOURNALENTRYITEM": ("released", "FI"),
    "I_TAXCODERATE": ("released", "FI"), "I_ORGANIZATIONADDRESS": ("released", "FI"),
    "I_COUNTRY": ("released", "FI"), "I_REGION": ("released", "FI"), "I_REGIONTEXT": ("released", "FI"),
    "I_PRODUCTCOSTESTIMATE": ("released", "CO"), "I_PRODCOSTESTCOSTCOMPRAWDEX": ("released", "CO"),
    "I_COSTCOMPONENTSTDVH": ("released", "CO"), "I_ACTLCOSTGMATLVALUECHAINITEM": ("released", "CO"),
    "I_ACTUALCOSTINGRUNRESULT": ("released", "CO"), "I_ACTUALCOSTINGACTIVITYRESULT": ("released", "CO"),
    "I_MATERIALLEDGERCUBE_LIT": ("released", "CO"), "I_MFGORDERACTLPLANTGTLDGRCOST": ("released", "CO"),
    "I_SERVICECOSTRATE_2": ("released, wrong business use suspected", "CO"),
    "I_ACTUALCOSTRATETP": ("released (correct view)", "CO"),
    "I_ACTUALCOSTRATE": ("NOT released despite #PUBLIC_LOCAL_API", "CO"),
    "I_ACCOUNTINGCOSTRATE_2": ("NOT released despite #PUBLIC_LOCAL_API", "CO"),
    "I_COSTCENTERACTIVITYTYPE": ("released, wrong business use (master data only)", "CO"),
    "I_INVENTORYPRICEBYKEYDATE": ("released, DEPRECATED", "CO"),
    "I_INVENTORYPRICEBYKEYDATE_2": ("released (successor)", "CO"),
    "I_MATERIALDOCUMENTITEM_2": ("released", "CO"), "I_MATERIALDOCUMENTHEADER_2": ("released", "CO"),
    "I_PRODUCT": ("released", "CO"), "I_PRODUNIVHIERARCHYNODEBASIC": ("released", "CO"),
    "I_PRODUCTIONVERSION": ("released", "PP"), "I_PLANT": ("released", "CO"),
    "I_ACTIVEPLNDINDEPRQMT": ("released", "PP"), "I_ACTIVEPLNDINDEPRQMTITEM": ("released", "PP"),
    "I_PLNDINDEPRQMTBYINTKEY": ("released", "PP"), "I_PLNDINDEPRQMTITEMBYINTKEY": ("released", "PP"),
    "I_PLNDINDEPRQMTITEMHISTORY": ("released", "PP"), "I_PLNDINDEPRQMTTYPE": ("released", "PP"),
    "I_PLNDINDEPRQMTTYPETEXT": ("released", "PP"), "I_PLNDINDEPRQMTTP": ("released (BDEF)", "PP"),
    "I_QLTYNOTIFICATION": ("released (correct name)", "QM"),
    "I_QUALITYNOTIFICATIONITEM": ("released", "QM"),
    "I_QUALITYNOTIFICATION": ("does not exist (naming trap)", "QM"),
    "I_OUTBOUNDDELIVERY": ("released", "LE-TM"), "I_OUTBOUNDDELIVERYITEM": ("released", "LE-TM"),
    "I_TRANSPORTATIONORDER_2": ("released", "LE-TM"), "I_TRANSPORTATIONORDERITEM_2": ("released", "LE-TM"),
    "I_TRANSPORTATIONORDERSTOP_2": ("released", "LE-TM"), "I_TRANSPORTATIONORDERSTAGE_2": ("released", "LE-TM"),
    "I_TRANSPORTATIONORDERBP_2": ("released", "LE-TM"), "I_TRANSPORTATIONORDEREVENT": ("released", "LE-TM"),
    "I_TRANSPORDEVENTCODE_2": ("released", "LE-TM"), "I_TRANSPORDDOCREF_2": ("released", "LE-TM"),
    "I_FREIGHTORDERTP": ("released (BDEF)", "LE-TM"), "I_FREIGHTORDERITEMTP": ("released (BDEF)", "LE-TM"),
    "I_FREIGHTORDERSTOPTP": ("released (BDEF)", "LE-TM"), "I_FREIGHTORDERSTAGETP": ("released (BDEF)", "LE-TM"),
    "I_FREIGHTORDERBPTP": ("released (BDEF)", "LE-TM"), "I_FREIGHTORDERDOCREFTP": ("released (BDEF)", "LE-TM"),
    "I_FREIGHTORDERITEMDOCREFTP": ("released (BDEF)", "LE-TM"),
    "I_BILLINGDOCUMENT": ("[Unverified] released — only a keyword candidate in the source", "SD"),
    "I_BILLINGDOCUMENTITEM": ("[Unverified] released — only a keyword candidate in the source", "SD"),
    "I_PRODUCTTEXT": ("released", "QM"),
}


def main():
    rows = list(csv.DictReader(open(os.path.join(BASE, "catalog_all.csv"), encoding="utf-8")))
    by = {r["view"].upper(): r for r in rows}
    fo = {l.split(",", 1)[0].strip().upper()
          for l in open(os.path.join(BASE, "_fields_only", "views.csv"), encoding="utf-8").readlines()[1:]}

    in_catalog = fields_only = absent = 0
    for v, (state, src) in sorted(EXTERNAL.items()):
        if v in by:
            r = by[v]
            print(f"IN-CATALOG   {v:32s} folder={r['folder']:30s} | ext-state: {state} ({src})")
            in_catalog += 1
        elif v in fo:
            print(f"FIELDS-ONLY  {v:32s} (not in CDS sheet)              | ext-state: {state} ({src})")
            fields_only += 1
        else:
            print(f"ABSENT       {v:32s}                                  | ext-state: {state} ({src})")
            absent += 1
    print(f"\ntotal checked: {len(EXTERNAL)} | in catalog: {in_catalog} | fields-only gap: {fields_only} | absent: {absent}")


if __name__ == "__main__":
    main()
