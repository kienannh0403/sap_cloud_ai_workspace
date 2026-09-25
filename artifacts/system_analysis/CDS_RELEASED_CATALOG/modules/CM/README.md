# CM

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `CM` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**97 view** · data category: (none) 97 · loại: basic 91, text 6 · 1 view có field DEPRECATED/DECOMMISSIONED · 44 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CM-CAT-2CL | 2 | top-level |
| CM-CTX-2CL | 11 | top-level |
| CM-DOC-2CL | 24 | top-level |
| CM-GF-2CL | 9 | top-level |
| CM-INT-2CL | 2 | top-level |
| CM-LT-2CL | 48 | top-level |
| CM-TSK-2CL | 1 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_LEGALTRANSACTIONAPI01 | Legal Transaction | CM-LT-2CL |  | 27 |
| I_LGLTRANSWRKFLWEMLDEADLINE | Email Template for Workflow Deadline | CM-LT-2CL |  | 23 |
| I_LEGALCONTEXTAPI01 | Legal Context | CM-CTX-2CL |  | 22 |
| I_LEGALCATEGORYAPI01 | Legal Category | CM-CAT-2CL |  | 21 |
| I_LGLTRANSWRKFLWINSTCE | Data for Workflow Instance | CM-LT-2CL |  | 21 |
| I_LEGALDOCUMENTAPI01 | Legal Document | CM-DOC-2CL |  | 18 |
| I_LEGALTRANSACTIONBASE | Basic Data of Legal Transaction | CM-LT-2CL |  | 17 |
| I_LGLTRANSRNWLTERMNAPI01 | Lifecycle of Legal Transaction | CM-LT-2CL |  | 14 |
| I_LGLTRANSWRKFLWSTARTEDTASKDET | Legal Transaction Workflow Task Details | CM-LT-2CL |  | 14 |
| I_LGLTRANSENTITYAPI01 | Entities of Legal Transaction | CM-LT-2CL |  | 11 |
| I_LGLTRANSINTCONTACTAPI01 | Internal Contacts of Legal Transaction | CM-LT-2CL |  | 11 |
| I_LGLTRANSPARENTCATEGORYAPI01 | Parent Categories of Legal Transaction | CM-LT-2CL |  | 10 |
| I_LGLCNTNTMGMTWRKFLWLGLTRANS | Leading Object for Legal Tasks | CM-TSK-2CL |  | 10 |
| I_LGLTRANSDATESAPI01 | Dates of Legal Transaction | CM-LT-2CL |  | 9 |
| I_LGLTRANSEXTCONTACTAPI01 | External Contacts of Legal Transaction | CM-LT-2CL |  | 9 |
| I_LGLTRANSLINKEDOBJECTAPI01 | Linked Objects of Legal Transaction | CM-LT-2CL |  | 9 |
| I_LGLTRANSRELATIONSHIPAPI01 | Relationships of Legal Transaction | CM-LT-2CL |  | 9 |
| I_LGLTRANSCATEGORYAPI01 | Categories of Legal Transaction | CM-LT-2CL |  | 8 |
| I_LGLTRANSCATEGORYGROUPAPI01 | Category Groups of Legal Transaction | CM-LT-2CL |  | 6 |
| I_LGLTRANSDOCLINKAPI01 | Linked Documents of Legal Transaction | CM-LT-2CL |  | 5 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
