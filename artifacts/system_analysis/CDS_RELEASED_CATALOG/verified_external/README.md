# Verified external — kiến thức đối chiếu từ dự án khác

**Nguồn:** `C:\Users\anltk2\OneDrive\FIS dự án\SAP-CODE-GEN\sap-abap-codegen-pkg\docs\sap-knowledge\modules\*.md`
(pack tri thức của các "module-agent" trong dự án SAP-CODE-GEN — dự án khác, tenant khác: `my440257` client 100,
xưng "NFG"). Đọc 2026-09-23 theo yêu cầu của anh, hạn mục 8 file: `README.md`, `_template.md`, `FI.md`, `CO.md`,
`LE.md`, `MM.md`, `PM.md`, `PP.md`, `QM.md`, `SD.md`.

**Vì sao đáng tin hơn xlsx:** các fact trong này được xác minh bằng `released-objects-index.json` (danh sách released
chính thức của SAP), đọc source thật qua ADT/vsp, hoặc test EML/action sống trên tenant — không phải suy luận từ
tên view như phần lớn `modules/` (xem cột `match_basis` = `component/alias/keyword/top-level` ở đó). Coi các file
trong `verified_external/` là **bằng chứng mạnh hơn một bậc**, nhưng vẫn là **tenant khác** — field/association vẫn
nên xác nhận lại trên `my437569`/`my437557` trước khi đưa vào TS.

**Đã lọc bỏ khi đưa vào đây:**
- Toàn bộ custom Z-view của dự án NFG (`ZI_NFG_*`) — đây là đối tượng Z của **dự án khác**, không phải released
  chuẩn SAP, không thuộc phạm vi danh mục này.
- Giá trị customizing/business cụ thể của NFG (mã costing variant, tên report ZCO04/ZSD07/ZAP06...) — không
  transfer sang tenant khác. Chỉ giữ lại: tên view, application component, trạng thái released, tên field thật,
  association, và **bẫy tổng quát** (loại bẫy sẽ lặp lại ở tenant bất kỳ).

**Đối chiếu với `catalog_all.csv`** (script `cross_check.py` trong thư mục này, chạy `python -X utf8
artifacts/system_analysis/CDS_RELEASED_CATALOG/verified_external/cross_check.py`): phát hiện quan trọng nhất —
**một số view đã verify released lại KHÔNG có trong sheet CDS** của file xlsx (chỉ có ở sheet Fields, hoặc không
có ở đâu cả nếu là BDEF/TP). Chi tiết ở mỗi file phân hệ bên dưới và ở `INDEX.md` §Giới hạn phạm vi.

## File trong thư mục này
| File | Phân hệ | Điểm chính |
|---|---|---|
| `FI.md` | FI-GL, BC-SRV-ADR | Journal Entry header/item field thật; Address nằm ở BC không phải FI |
| `CO.md` | CO-PC-PCP/ACT/ML/OM | Cost component split PLANNED có API riêng, ACTUAL **không có CDS released** (SAP xác nhận); `#PUBLIC_LOCAL_API` ≠ released C1 |
| `PP.md` | PP-VDM (PIR) | View landscape PIR đầy đủ + field map; write BO không có trong catalog view-only |
| `LE-TM.md` | LE-SHP-GF, TM-FRM* | Freight Order execution pattern (EML ReportEvent), datetime type TM |
| `QM.md` | QM-QN | Tên view thật `I_QltyNotification` (không phải `I_QualityNotification`) + field SAI hay đoán nhầm |
