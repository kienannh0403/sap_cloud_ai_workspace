# CM

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `CM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**53 view** · data category: (none) 53 · loại: basic 47, text 6 · 1 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CM-CAT | 2 | top-level |
| CM-CTX | 1 | top-level |
| CM-DOC | 9 | top-level |
| CM-GF | 9 | top-level |
| CM-LT | 31 | top-level |
| CM-TSK | 1 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_LEGALTRANSACTIONAPI01 | Legal Transaction | CM-LT |  | 27 |
| I_LGLTRANSWRKFLWEMLDEADLINE | Email Template for Workflow Deadline | CM-LT |  | 23 |
| I_LEGALCONTEXTAPI01 | Legal Context | CM-CTX |  | 22 |
| I_LEGALCATEGORYAPI01 | Legal Category | CM-CAT |  | 21 |
| I_LGLTRANSWRKFLWINSTCE | Data for Workflow Instance | CM-LT |  | 21 |
| I_LEGALDOCUMENTAPI01 | Legal Document | CM-DOC |  | 18 |
| I_LEGALTRANSACTIONBASE | Basic Data of Legal Transaction | CM-LT |  | 17 |
| I_LGLTRANSRNWLTERMNAPI01 | Lifecycle of Legal Transaction | CM-LT |  | 14 |
| I_LGLTRANSWRKFLWSTARTEDTASKDET | Legal Transaction Workflow Task Details | CM-LT |  | 14 |
| I_LGLTRANSENTITYAPI01 | Entities of Legal Transaction | CM-LT |  | 11 |
| I_LGLTRANSINTCONTACTAPI01 | Internal Contacts of Legal Transaction | CM-LT |  | 11 |
| I_LGLTRANSPARENTCATEGORYAPI01 | Parent Categories of Legal Transaction | CM-LT |  | 10 |
| I_LGLCNTNTMGMTWRKFLWLGLTRANS | Leading Object for Legal Tasks | CM-TSK |  | 10 |
| I_LGLTRANSDATESAPI01 | Dates of Legal Transaction | CM-LT |  | 9 |
| I_LGLTRANSEXTCONTACTAPI01 | External Contacts of Legal Transaction | CM-LT |  | 9 |
| I_LGLTRANSLINKEDOBJECTAPI01 | Linked Objects of Legal Transaction | CM-LT |  | 9 |
| I_LGLTRANSRELATIONSHIPAPI01 | Relationships of Legal Transaction | CM-LT |  | 9 |
| I_LGLTRANSCATEGORYAPI01 | Categories of Legal Transaction | CM-LT |  | 8 |
| I_LGLTRANSCATEGORYGROUPAPI01 | Category Groups of Legal Transaction | CM-LT |  | 6 |
| I_LGLTRANSDOCLINKAPI01 | Linked Documents of Legal Transaction | CM-LT |  | 5 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
