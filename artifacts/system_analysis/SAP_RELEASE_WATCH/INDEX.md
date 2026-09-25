# SAP_RELEASE_WATCH — INDEX

**Là gì:** theo dõi những gì SAP phát hành cho S/4HANA Cloud Public Edition — object được released cho ABAP Cloud (mọi
loại), API / event / BAdI / BO interface trên API Hub, và What's New theo release — lưu bản chụp cục bộ + ghi thay đổi.
Tạo 2026-09-25 theo yêu cầu user ("không chỉ CDS mà API, object liên quan, những điều SAP mới cập nhật").

**Tự động:** hook `session-start.sh` chạy `refresh_sap_release_watch.py --check` mỗi lần mở phiên (~2 s). Có thay đổi →
hook báo, agent chạy refresh ngay và báo user những gì mới / bị deprecate (memory `sap-release-watch`).

## Nguồn

| Nguồn | Gì | Lấy bằng | Kiểm tra mới bằng |
|---|---|---|---|
| A. `SAP/abap-atc-cr-cv-s4hc` `objectReleaseInfoLatest.json` | ~37.000 object: CDS, class, interface, BDEF, BAdI, table, data element, auth object… + released / deprecated / successor | script | ngày commit GitHub |
| B. SAP Business Accelerator Hub (api.sap.com), mọi package SAP "… SAP S/4HANA Cloud Public Edition" có version release (2608.x) | API OData V2/V4, SOAP, REST · business event · BAdI · BO interface · CDS view · iFlow, kèm mô tả, trạng thái, ngày sửa | script | version + ngày sửa package `SAPS4HANACloud` |
| C. SAP Help What's New (tài liệu `ee9ee0ca4c3942068ea584d2f929b5b1`) | tính năng mới / app bị bỏ / thay đổi theo release | agent, qua MCP `sap-docs-upstream` `search` (có `versionId`, vd `2608.00`) — trang What's New là SPA, không tải thẳng được | khi B đổi số release (2608 → 2611) |

## Cách dùng
- Tìm object released: `released_objects/objects.csv` (lọc cột `type`; `deprecated` có `successors`). CDS view thì dùng
  catalog theo phân hệ `../CDS_RELEASED_CATALOG/` (script này tự refresh catalog đó).
- Tìm API / event / BAdI: `api_hub/artifacts.csv` (cột `type`, `sub_type`, `state`, `package`, `description`).
- Cái gì mới: `changelog.md` (mới nhất ở cuối), chi tiết `changes/<ngày>_<nguồn>.csv`, What's New `whats_new/<release>.md`.
- Chạy tay: `python -X utf8 artifacts/system_analysis/SAP_RELEASE_WATCH/refresh_sap_release_watch.py [--check|--force]`.

## Giới hạn
- Mô tả class/interface/BDEF đọc từ tenant 080 (cookie `tools/vsp/cookies_dev.txt`); cookie chết → refresh vẫn chạy, chỉ
  thiếu mô tả của object mới — refresh cookie rồi chạy `--force`.
- Hub không có ngày "released"; "mới" = xuất hiện so với bản chụp trước. Bản chụp đầu tiên (baseline) không có diff.
- What's New không có trong script (cần MCP) — agent tự làm khi có release mới.

## Bản đồ file
| Đường dẫn | Nội dung |
|---|---|
| `refresh_sap_release_watch.py` | kiểm tra + refresh cả hai nguồn, ghi changelog |
| `state.json` | ngày/phiên bản đã lấy lần cuối (script so với nó) |
| `released_objects/objects.csv`, `summary.md`, `descriptions_080.json` | nguồn A (sinh tự động) |
| `api_hub/artifacts.csv`, `summary.md` | nguồn B (sinh tự động) |
| `changelog.md`, `changes/` | thay đổi mỗi lần refresh |
| `whats_new/<release>.md` | tóm tắt What's New theo module đang dùng (agent viết) |
