"""Build the per-module CDS released-view catalog from the xlsx released-CDS list.

Run from the workspace root:
    python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/build_catalog.py

Reads   .claude/Documents/CDSView_Released_updated (1).xlsx   (sheets: CDS, Fields, Sheet1)
Writes  artifacts/system_analysis/CDS_RELEASED_CATALOG/{modules,relations,_fields_only}/ + catalog_all.csv
        + module_map.md
Deterministic: re-running overwrites the generated files only. INDEX.md and process_flows.md are
hand-written and are NOT touched by this script.
"""
import collections
import csv
import datetime
import glob
import os
import re
import shutil

import openpyxl

SRC_GLOB = ".claude/Documents/CDSView_Released_updated*.xlsx"
OUT = "artifacts/system_analysis/CDS_RELEASED_CATALOG"
MIN_VIEWS = 2  # a module "uses" an entity only when >= MIN_VIEWS of its views expose it
TODAY = datetime.date.today().isoformat()

# Sheet1 components that do not exist verbatim in the CDS sheet, mapped to the component family that
# really holds the equivalent views (verified by view names, see module_map.md). basis = "alias".
ALIASES = {"PM-EQM-EQ": "EAM-OBJ", "PM-EQM-FL": "EAM-OBJ", "PPM-SCL": "PS"}

# Sheet1 components with no component of their own in the file: assigned by view-name keywords within
# PP-* components. basis = "keyword" (inferred, lower confidence). Order matters: first match wins.
KEYWORD_RULES = [
    ("PP-SFC", r"MANUFACTURINGORDER|PRODUCTIONORDER|PRODORD|CONFIRMATION|SHOPFLOOR|ORDEROPERATION"),
    ("PP-MRP", r"MRP|PLANNEDORDER|PLNDORDER|PLNDINDEPRQMT|DEPDNTRQMT|DEPENDENTREQ|PLANNINGSTRATEGY|FORECAST"),
]

# data element -> (entity, tier). Tiers: ORG (organisational unit), MASTER (master data object),
# DOC (business document), CONFIG (customizing / period key). Curated from the 150 most frequent
# multi-module data elements of the Fields sheet.
ENTITY_MAP = {}
def _e(entity, tier, *des):
    for d in des:
        ENTITY_MAP[d] = (entity, tier)
_e("Company Code", "ORG", "BUKRS", "FIS_BUKRS")
_e("Plant", "ORG", "WERKS_D")
_e("Storage Location", "ORG", "LGORT_D")
_e("Sales Organization", "ORG", "VKORG")
_e("Distribution Channel", "ORG", "VTWEG")
_e("Division", "ORG", "SPART")
_e("Sales Office", "ORG", "VKBUR")
_e("Sales Group", "ORG", "VKGRP")
_e("Purchasing Organization", "ORG", "EKORG")
_e("Controlling Area", "ORG", "KOKRS", "FIS_KOKRS")
_e("Profit Center", "ORG", "PRCTR")
_e("Business Area", "ORG", "GSBER")
_e("Valuation Area", "ORG", "BWKEY")
_e("Shipping Point", "ORG", "VSTEL")
_e("Chart of Accounts", "ORG", "KTOPL")
_e("Functional Area", "ORG", "FKBER")
_e("Segment", "ORG", "FB_SEGMENT")
_e("Material / Product", "MASTER", "MATNR", "PRODUCTNUMBER")
_e("Business Partner", "MASTER", "BU_PARTNER")
_e("Customer", "MASTER", "KUNNR", "KUNAG", "KUNWE", "KUNRE")
_e("Supplier", "MASTER", "LIFNR", "MD_SUPPLIER")
_e("Batch", "MASTER", "CHARG_D")
_e("Material Group", "MASTER", "MATKL")
_e("Personnel", "MASTER", "PERNR_D")
_e("Equipment", "MASTER", "EQUNR")
_e("Fixed Asset", "MASTER", "ANLN1")
_e("Cost Center", "MASTER", "KOSTL")
_e("G/L Account", "MASTER", "SAKNR", "FIS_RACCT")
_e("Activity Type", "MASTER", "LSTAR")
_e("WBS Element", "MASTER", "PS_S4_PSPNR", "PS_PSP_PNR", "PS_POSID_EDIT", "PS_POSID")
_e("Task List (routing) group", "MASTER", "PLNNR")
_e("Profitability Segment", "MASTER", "RKEOBJNR_CHAR", "RKEOBJNR_NUMC")
_e("Grant", "MASTER", "GM_GRANT_NBR")
_e("Address", "MASTER", "AD_ADDRNUM")
_e("Sales Document", "DOC", "VBELN_VA", "VDM_SALES_ORDER", "POSNR_VA")
_e("Delivery", "DOC", "VBELN_VL")
_e("Billing Document", "DOC", "VBELN_VF")
_e("SD/LE Document (generic VBELN)", "DOC", "VBELN")
_e("Purchasing Document", "DOC", "EBELN", "EBELP")
_e("Order (production / maintenance / internal)", "DOC", "AUFNR")
_e("Inspection Lot", "DOC", "QPLOS")
_e("Document Condition (pricing)", "DOC", "KNUMV")
_e("Fiscal Year", "CONFIG", "GJAHR", "FIS_GJAHR_NO_CONV")
_e("Tax Code", "CONFIG", "MWSKZ")
_e("Payment Terms", "CONFIG", "DZTERM")
_e("Incoterms", "CONFIG", "INCO1")
_e("Sales Document Type", "CONFIG", "AUART")
_e("Movement Type", "CONFIG", "BWART")
TIERS = ["DOC", "MASTER", "ORG"]  # scored tiers; CONFIG is listed but not scored

TOP_DESC = {  # only components whose meaning is certain; everything else stays unlabelled
    "FI-CA": "Contract Accounts Receivable and Payable", "FIN-FSCM-TRM": "Treasury and Risk Management",
    "LE": "Logistics Execution", "QM": "Quality Management", "TM": "Transportation Management",
    "SCM-EWM": "Extended Warehouse Management", "RE-FX": "Flexible Real Estate Management",
    "PSM-FM": "Public Sector – Funds Management", "CA-JVA": "Joint Venture Accounting",
    "CA-DMS": "Document Management", "CA-CL": "Classification", "SLC": "Supplier Lifecycle Management",
    "PM": "Plant Maintenance", "BC": "Basis / cross-application services", "CA": "Cross-Application",
}


def slug(text):
    return re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")


def kind_of(name, category):
    if name.endswith(("TEXT", "TXT")):
        return "text"
    if "STDVH" in name or name.endswith("VH"):
        return "value_help"
    return (category or "basic").lower()


def main():
    src = glob.glob(SRC_GLOB)[0]
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)

    sheet1 = [r for r in wb["Sheet1"].iter_rows(min_row=2, values_only=True) if r[0]]
    priority = {comp: f"{comp}_{slug(vi)}" for comp, vi in sheet1}
    vi_name = {comp: vi for comp, vi in sheet1}

    cds_rows = list(wb["CDS"].iter_rows(min_row=2, values_only=True))
    uniq = {}
    for r in cds_rows:  # exact duplicate rows exist (464); keep the first
        uniq.setdefault(r[1], r)

    fields = list(wb["Fields"].iter_rows(min_row=2, values_only=True))
    n_fields = collections.Counter()
    n_depr = collections.Counter()
    view_de = collections.defaultdict(set)
    f_comp = {}
    for v, comp, fname, _ft, de, _det, _dt, _ln, status, _succ in fields:
        if comp and v not in f_comp:
            f_comp[v] = comp
        if not fname:
            continue
        n_fields[v] += 1
        if status in ("DEPRECATED", "DECOMMISSIONED"):
            n_depr[v] += 1
        if de:
            view_de[v].add(de)

    def prefix_hit(comp, key):
        return comp == key or comp.startswith(key + "-")

    def assign(comp, name):
        for key in sorted(priority, key=len, reverse=True):
            if prefix_hit(comp, key):
                return priority[key], "component", key
        for pre, key in ALIASES.items():
            if key in priority and prefix_hit(comp, pre):
                return priority[key], "alias", key
        if comp.startswith("PP-") and not comp.startswith("PP-KAB"):  # Kanban is neither MRP nor SFC
            for key, rx in KEYWORD_RULES:
                if key in priority and re.search(rx, name):
                    return priority[key], "keyword", key
        return None, None, None

    assigned = {}
    for name, r in uniq.items():
        assigned[name] = assign(r[4], name)

    top_with_priority = {uniq[n][4].split("-")[0] for n, a in assigned.items() if a[0]}
    for name, r in uniq.items():
        if not assigned[name][0]:
            top = r[4].split("-")[0]
            folder = f"{top}_other" if top in top_with_priority else top
            assigned[name] = (folder, "top-level", None)

    def entities_of(v):
        return sorted({ENTITY_MAP[d][0] for d in view_de.get(v, ()) if d in ENTITY_MAP})

    records = []
    for name, r in uniq.items():
        folder, basis, key = assigned[name]
        records.append({
            "view": name, "description": r[3] or "", "end_user_description": r[2] or "",
            "component": r[4], "data_category": r[5] or "", "kind": kind_of(name, r[5]),
            "n_fields": n_fields.get(name, 0), "n_deprecated_fields": n_depr.get(name, 0),
            "key_entities": "; ".join(entities_of(name)), "match_basis": basis, "folder": folder,
        })
    records.sort(key=lambda x: (x["folder"], x["component"], x["view"]))
    by_folder = collections.defaultdict(list)
    for rec in records:
        by_folder[rec["folder"]].append(rec)
    for comp, fname in priority.items():  # priority folders always exist, even when empty
        by_folder.setdefault(fname, [])

    # ---- entity usage per folder ----
    ent_tier = {e: t for e, t in ENTITY_MAP.values()}
    usage = {f: collections.Counter() for f in by_folder}
    for f, recs in by_folder.items():
        for rec in recs:
            for e in rec["key_entities"].split("; "):
                if e:
                    usage[f][e] += 1
    uses = {f: {e for e, n in c.items() if n >= MIN_VIEWS} for f, c in usage.items()}

    def pair_keys(a, b):
        shared = uses[a] & uses[b]
        return {t: sorted(e for e in shared if ent_tier[e] == t) for t in TIERS + ["CONFIG"]}

    folders = sorted(by_folder)
    pairs = {}
    for i, a in enumerate(folders):
        for b in folders[i + 1:]:
            k = pair_keys(a, b)
            if k["DOC"] or k["MASTER"] or k["ORG"]:
                pairs[(a, b)] = k

    def neighbours(f, limit=8):
        rows = []
        for (a, b), k in pairs.items():
            if f in (a, b):
                other = b if a == f else a
                rows.append((len(k["DOC"]), len(k["MASTER"]), len(k["ORG"]), other, k))
        rows.sort(key=lambda x: (-x[0], -x[1], -x[2], x[3]))
        return rows[:limit]

    # ---- write outputs (generated dirs are wiped first) ----
    for sub in ("modules", "relations", "_fields_only"):
        shutil.rmtree(os.path.join(OUT, sub), ignore_errors=True)
        os.makedirs(os.path.join(OUT, sub))

    cols = ["view", "description", "end_user_description", "component", "data_category", "kind",
            "n_fields", "n_deprecated_fields", "key_entities", "match_basis"]

    def write_csv(path, recs, columns):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
            w.writeheader()
            w.writerows(recs)

    write_csv(os.path.join(OUT, "catalog_all.csv"), records, ["folder"] + cols)

    prio_by_folder = {v: k for k, v in priority.items()}
    for f, recs in sorted(by_folder.items()):
        d = os.path.join(OUT, "modules", f)
        os.makedirs(d)
        write_csv(os.path.join(d, "views.csv"), recs, cols)
        comp_count = collections.Counter((r["component"], r["match_basis"]) for r in recs)
        cat = collections.Counter(r["data_category"] or "(none)" for r in recs)
        kinds = collections.Counter(r["kind"] for r in recs)
        depr_views = sum(1 for r in recs if r["n_deprecated_fields"])
        core = sorted((r for r in recs if r["kind"] not in ("text", "value_help")),
                      key=lambda r: -r["n_fields"])[:20]
        pk = prio_by_folder.get(f)
        title = f"{f} — {vi_name[pk]}" if pk else f
        lines = [f"# {title}", "",
                 f"Generated {TODAY} from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. "
                 "Do not hand-edit; re-run the script.", ""]
        if pk:
            lines += [f"Phân hệ ưu tiên (Sheet1): component `{pk}` = **{vi_name[pk]}**.", ""]
        else:
            top = f.split("_")[0]
            lines += [f"Nhóm còn lại của module `{top}` (không thuộc phân hệ ưu tiên nào trong Sheet1)."
                      + (f" `{top}`: {TOP_DESC[top]}." if top in TOP_DESC else ""), ""]
        if not recs:
            lines += ["**Không có view nào** trong file cho phân hệ này (không component nào khớp). "
                      "Đừng đoán view — tìm trực tiếp trên hệ thống hoặc qua sap-docs.", ""]
        else:
            lines += [f"**{len(recs)} view** · data category: " + ", ".join(f"{k} {v}" for k, v in cat.most_common())
                      + " · loại: " + ", ".join(f"{k} {v}" for k, v in kinds.most_common())
                      + f" · {depr_views} view có field DEPRECATED/DECOMMISSIONED.", "",
                      "## Component trong nhóm", "", "| Component | Số view | Cách gán |", "|---|---:|---|"]
            lines += [f"| {c} | {n} | {b} |" for (c, b), n in sorted(comp_count.items())]
            if any(b in ("alias", "keyword") for (_c, b) in comp_count):
                lines += ["", "> `alias` = component khác tên trong Sheet1 nhưng cùng nội dung (xem `module_map.md`); "
                          "`keyword` = **suy luận theo tên view**, độ tin cậy thấp hơn `component`."]
            lines += ["", "## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)", "",
                      "| View | Mô tả | Component | Category | Field |", "|---|---|---|---|---:|"]
            lines += [f"| {r['view']} | {r['description']} | {r['component']} | {r['data_category'] or ''} | {r['n_fields']} |"
                      for r in core]
            ents = usage[f].most_common()
            lines += ["", f"## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= {MIN_VIEWS} view)", "",
                      "| Tier | Entity | Số view |", "|---|---|---:|"]
            lines += [f"| {ent_tier[e]} | {e} | {n} |" for e, n in ents if n >= MIN_VIEWS]
            nb = neighbours(f)
            if nb:
                lines += ["", "## Phân hệ liên quan (chung entity)", "",
                          "| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |", "|---|---:|---:|---:|---|"]
                for nd, nm, no, other, k in nb:
                    lines.append(f"| {other} | {nd} | {nm} | {no} | {', '.join(k['DOC'] + k['MASTER']) or '—'} |")
        lines += ["", "## Cách dùng", "",
                  "1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).",
                  "2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống "
                  "(`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.",
                  "3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.", ""]
        with open(os.path.join(d, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines))

    # ---- relations ----
    rel = os.path.join(OUT, "relations")
    with open(os.path.join(rel, "module_pairs.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["module_a", "module_b", "n_doc", "n_master", "n_org", "doc_entities", "master_entities", "org_entities"])
        for (a, b), k in sorted(pairs.items(), key=lambda x: (-len(x[1]["DOC"]), -len(x[1]["MASTER"]), x[0])):
            w.writerow([a, b, len(k["DOC"]), len(k["MASTER"]), len(k["ORG"]),
                        "; ".join(k["DOC"]), "; ".join(k["MASTER"]), "; ".join(k["ORG"])])

    prio_folders = [priority[k] for k in priority]
    lines = ["# Quan hệ giữa các phân hệ ưu tiên (chung entity nghiệp vụ)", "",
             f"Generated {TODAY}. Nguồn: cột *Data element* của sheet Fields. Hai phân hệ **liên quan** khi cùng có "
             f">= {MIN_VIEWS} view chứa cùng một entity (Sales Document, Material, Company Code...). "
             "Đây là bằng chứng **dùng chung khoá dữ liệu**, KHÔNG phải association CDS đã kiểm chứng.", "",
             "Sắp theo số entity DOC, rồi MASTER, rồi ORG. Chỉ hiện cặp có >= 1 DOC hoặc >= 2 MASTER.", "",
             "| Phân hệ A | Phân hệ B | DOC | MASTER | ORG | DOC entity chung | MASTER entity chung |",
             "|---|---|---:|---:|---:|---|---|"]
    shown = []
    for i, a in enumerate(prio_folders):
        for b in prio_folders[i + 1:]:
            k = pairs.get((min(a, b), max(a, b)))
            if k and (k["DOC"] or len(k["MASTER"]) >= 2):
                shown.append((len(k["DOC"]), len(k["MASTER"]), len(k["ORG"]), a, b, k))
    shown.sort(key=lambda x: (-x[0], -x[1], -x[2], x[3], x[4]))
    lines += [f"| {a} | {b} | {d} | {m} | {o} | {', '.join(k['DOC']) or '—'} | {', '.join(k['MASTER']) or '—'} |"
              for d, m, o, a, b, k in shown]
    with open(os.path.join(rel, "module_pairs.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")

    lines = ["# Entity nghiệp vụ → phân hệ dùng nó", "",
             f"Generated {TODAY}. Với mỗi entity: số view mỗi folder (chỉ hiện folder >= {MIN_VIEWS} view). "
             "Dùng khi biết cần *dữ liệu gì* mà chưa biết *view nào*: tra entity, chọn folder có nhiều view nhất.", ""]
    de_of = collections.defaultdict(list)
    for de, (e, _t) in ENTITY_MAP.items():
        de_of[e].append(de)
    for tier in TIERS + ["CONFIG"]:
        lines += [f"## {tier}", "", "| Entity | Data element | Folder (số view) |", "|---|---|---|"]
        for e in sorted(x for x in de_of if ent_tier[x] == tier):
            hubs = sorted(((usage[f][e], f) for f in usage if usage[f][e] >= MIN_VIEWS), reverse=True)
            lines.append(f"| {e} | {', '.join(sorted(de_of[e]))} | "
                         + ", ".join(f"{f} ({n})" for n, f in hubs[:10]) + " |")
        lines.append("")
    with open(os.path.join(rel, "entity_hubs.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))

    # ---- module_map.md: rules + every component -> folder ----
    comp_folder = collections.defaultdict(collections.Counter)
    for rec in records:
        comp_folder[rec["component"]][(rec["folder"], rec["match_basis"])] += 1
    lines = ["# Module map — component → folder", "", f"Generated {TODAY} by `build_catalog.py` (do not hand-edit).", "",
             "## Cách gán (thứ tự ưu tiên; mỗi view thuộc đúng 1 folder)", "",
             "1. **component** — component của view bằng hoặc nằm dưới component trong Sheet1 (vd `SD-SLS-SO` → `SD-SLS`). Độ tin cậy cao.",
             "2. **alias** — Sheet1 ghi component không tồn tại trong file; gán sang component cùng nội dung, đã đối chiếu tên view: "
             + "; ".join(f"`{a}*` → `{b}`" for a, b in ALIASES.items()) + ".",
             "3. **keyword** — Sheet1 ghi component không tồn tại và không có alias; gán theo từ khoá trong tên view, chỉ trong "
             "`PP-*` (bỏ `PP-KAB*`): " + "; ".join(f"`{k}`: /{rx}/" for k, rx in KEYWORD_RULES)
             + ". **Suy luận, độ tin cậy thấp hơn.**",
             "4. **top-level** — phần còn lại gom theo module gốc: `<TOP>_other` nếu module đó đã có folder ưu tiên, "
             "ngược lại folder tên `<TOP>`.", "",
             "## Phân hệ ưu tiên (Sheet1) và kết quả", "", "| Component (Sheet1) | Phân hệ | Folder | Số view |", "|---|---|---|---:|"]
    lines += [f"| {c} | {vi_name[c]} | {priority[c]} | {len(by_folder[priority[c]])} |" for c in priority]
    lines += ["", "## Mọi component trong file", "", "| Component | Số view | Folder | Cách gán |", "|---|---:|---|---|"]
    for comp in sorted(comp_folder):
        for (fo, ba), n in sorted(comp_folder[comp].items()):
            lines.append(f"| {comp} | {n} | {fo} | {ba} |")
    with open(os.path.join(OUT, "module_map.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")

    # ---- views only in the Fields sheet ----
    only = sorted(set(n_fields) - set(uniq))
    write_csv(os.path.join(OUT, "_fields_only", "views.csv"),
              [{"view": v, "component": f_comp.get(v, ""), "n_fields": n_fields[v], "n_deprecated_fields": n_depr.get(v, 0)}
               for v in only], ["view", "component", "n_fields", "n_deprecated_fields"])
    with open(os.path.join(OUT, "_fields_only", "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Views chỉ có trong sheet Fields\n\n"
                 f"{len(only)} view xuất hiện trong sheet **Fields** nhưng **không** có trong sheet **CDS** "
                 f"({sum(1 for v in only if not f_comp.get(v))} view không có cả component). "
                 "File không nói chúng có released hay không, nên **không** đưa vào các folder phân hệ. "
                 "Chỉ dùng để tra field; muốn dùng view thì verify release trên hệ thống trước.\n")

    # ---- console summary for verification ----
    print("unique views:", len(uniq), "| duplicate rows dropped:", len(cds_rows) - len(uniq))
    print("folders:", len(by_folder), "| views assigned:", sum(len(v) for v in by_folder.values()))
    basis = collections.Counter(r["match_basis"] for r in records)
    print("match basis:", dict(basis))
    for f in sorted(by_folder):
        print(f"  {f:38s} {len(by_folder[f]):4d}")
    print("fields-only views:", len(only), "| module pairs with shared keys:", len(pairs))


if __name__ == "__main__":
    main()
