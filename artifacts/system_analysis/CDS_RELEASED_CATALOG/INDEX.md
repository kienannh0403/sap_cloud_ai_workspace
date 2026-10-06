# CDS_RELEASED_CATALOG — INDEX

**Là gì:** danh mục **7.893 CDS view (DDLS) released C1** cho S/4HANA Cloud Public Edition, chia theo phân hệ (46 folder,
mỗi view đúng 1 folder), kèm quan hệ giữa các phân hệ. Thay cho `cds-kb` MCP đang chết (memory `cds-kb-mcp-endpoint-dead`).

**Nguồn (từ 2026-09-25):**
- **Tập view + trạng thái + component:** danh sách chính thức của SAP — Cloudification Repository
  `SAP/abap-atc-cr-cv-s4hc` `objectReleaseInfoLatest.json` (SAP cập nhật 2026-09-04), bản lọc DDLS ở `sap_official/`.
- **Mô tả + package:** đọc trên tenant 080 (ADT quickSearch, 2026-09-25) — `sap_official/descriptions_080.json`.
- **File xlsx của user** (`.claude/Documents/CDSView_Released_updated (1).xlsx`): chỉ còn dùng cho mô tả/data category
  (ưu tiên hơn mô tả 080 nếu có), sheet Fields (số field, `key_entities`) và Sheet1 (phân hệ ưu tiên).

**Trạng thái (2026-09-25):** đã sinh lại. 7.893 view released, trong đó 4.021 có trong xlsx, **3.872 view mới**; 50 view
chưa có trên tenant 080 (`in_080 = no`); 218 view deprecated/notToBeReleased tách ra `_deprecated/`.

## Cách dùng khi làm báo cáo / chức năng
1. Xác định phân hệ của báo cáo → mở `modules/<folder>/README.md` rồi tra `views.csv` (cột `key_entities` cho biết view có Customer / Material / Company Code...).
2. Có phân hệ đó trong `verified_external/` (FI, CO, PP, LE-TM, QM) → đọc trước, đó là field/bẫy **đã verify thật**, tin cậy hơn `views.csv` (chỉ dựa vào tên).
3. Không thấy → xem bảng "Phân hệ liên quan" cuối README, hoặc `relations/entity_hubs.md` (biết *dữ liệu gì*, chưa biết *view nào*).
4. Vẫn không thấy → grep `catalog_all.csv` (mọi view released, có cột `folder`). Không có ở đó → grep `_deprecated/views.csv`
   (view cũ → cột `successors`). Không có cả hai = **không released** cho ABAP Cloud.
5. Cột `in_080 = no` → tenant 080 chưa có view đó, không dùng. Lần đầu dùng một view vẫn đọc `SAP(action=read, target=DDLS <tên>)` để lấy field thật.

## Giới hạn phạm vi
- **Có view TP (transactional projection) dạng DDLS** (870 view tên kết thúc `TP`, vd `I_FreightOrderTP`,
  `I_PlndIndepRqmtTP`), **nhưng không có BDEF** — muốn biết action/operation được released thì đọc BDEF trên ADT.
- **`n_fields` / `key_entities` chỉ có cho view nằm trong sheet Fields của xlsx.** View mới = 0 / rỗng, không có nghĩa là
  view không có field; phần "View chính" trong README module vì vậy thiên về view cũ.
- Tên trong catalog viết HOA (khoá TADIR); tên CamelCase thật lấy từ source DDLS.
- Mô tả của view mới lấy từ 080 (tên kỹ thuật hoá, tiếng Anh); 50 view không có trên 080 thì không có mô tả.
- **Annotation `#PUBLIC_LOCAL_API` KHÔNG đồng nghĩa với released C1.** `I_ActualCostRate` và
  `I_AccountingCostRate_2` có annotation này nhưng dùng trong class ABAP Cloud báo "use not permitted" — và đúng là
  **không có** trong danh sách SAP (đối chiếu 2026-09-25). Xem `verified_external/CO.md`.
- **Tên view có thể khác trực giác.** Vd `I_QltyNotification` (không phải `I_QualityNotification`) — xem
  `verified_external/QM.md`. Luôn xác nhận tên tồn tại (search/read) trước khi đưa vào TS, đừng suy tên đầy đủ
  từ business term.

## Quyết định ngoài yêu cầu gốc
- 16 phân hệ ưu tiên lấy từ **Sheet1**; phần còn lại gom `<TOP>_other` hoặc `<TOP>` (25 folder).
- Sheet1 ghi 4 component **không có trong file**: `PS` → gán `PPM-SCL-*` (alias); `EAM-OBJ` → `PM-EQM-EQ/FL` (alias);
  `PP-SFC` và `PP-MRP` → gán **theo từ khoá tên view** (suy luận); `EAM-WCM` → **0 view**, folder chỉ có README.
- `_fields_only/` giờ chỉ còn **74 view** có trong sheet Fields nhưng SAP không released (69 không có trong danh sách SAP,
  5 deprecated). ~1.840 view trước đây nằm ở đó thực ra released, đã về folder phân hệ.
- Component lấy theo danh sách SAP (hậu tố `-2CL`, vd `SD-BIL-BD-2CL`), luật gán theo tiền tố vẫn như cũ.
- "Liên quan" = cùng >= 2 view dùng chung một entity (theo data element); bảng entity do em chọn tay (`ENTITY_MAP` trong script). Không phải association CDS.

## Câu hỏi mở
- Sheet1 có đúng là danh sách phân hệ anh muốn ưu tiên không? Có cần `EAM-WCM` (vẫn 0 view)?
- Đã trả lời (2026-09-25): `I_BillingDocument(Item)` released (SD-BIL); `I_ProductionOrder` released (PP-SFC);
  `I_Material` và `I_SalesPricingCondition` **không released** — dùng `I_Product`; giá bán: họ `*PRCGELMNT` trong folder SD (vd `I_BILLINGDOCUMENTITEMPRCGELMNT`).
- File xlsx nằm trong `.claude/Documents/` (rule §4: output không đặt trong `.claude/`); cân nhắc chuyển sang `artifacts/`.
- Làm mới: `python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/refresh_sap_official.py` (`--check` chỉ so ngày). Thay đổi ghi vào `sap_official/changelog.md`.

## Bản đồ file
| Đường dẫn | Nội dung |
|---|---|
| `modules/<folder>/README.md` + `views.csv` | tóm tắt + toàn bộ view của phân hệ (sinh tự động) |
| `catalog_all.csv` | mọi view + cột `folder` |
| `module_map.md` | luật gán + bảng component → folder |
| `relations/module_pairs.md` / `.csv`, `entity_hubs.md` | quan hệ phân hệ, entity → phân hệ |
| `process_flows.md` | luồng O2C / P2P / sản xuất (kiến thức SAP, không từ file) + bẫy |
| `_fields_only/` | view có ở sheet Fields nhưng SAP không released (74) |
| `_deprecated/` | 218 view deprecated/notToBeReleased + view thay thế (`successors`) |
| `sap_official/` | nguồn SAP (JSON lọc DDLS), mô tả đọc từ 080, `released_ddls_public_cloud.csv` (danh sách phẳng, sinh tự động), README |
| `released_objects/` | **object released ngoài CDS** (từ cùng file SAP): `CLAS.csv`, `INTF.csv`, `BDEF.csv` (RAP BO gọi bằng EML), `BADI.csv`, `FUGR.csv`, `SUSO.csv` (authorization object) + README (số lượng, cách tra). Sinh bởi `build_object_index.py`, từ 2026-10-06 |
| `verified_external/` | field/bẫy CDS **đã verify thật** đối chiếu từ dự án khác (FI, CO, PP, LE-TM, QM) — tin cậy hơn `views.csv` |
| `refresh_sap_official.py` | kiểm tra SAP có danh sách mới không, có thì tải + đọc mô tả 080 + chạy `build_catalog.py` + `build_object_index.py` + ghi `changelog.md` |
| `build_object_index.py` | sinh lại `released_objects/` (chạy riêng được: `python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/build_object_index.py`) |
| `build_catalog.py` | sinh lại `modules/`, `catalog_all.csv`, `module_map.md`, `relations/`, `_fields_only/`, `_deprecated/`, `sap_official/released_ddls_public_cloud.csv` khi nguồn đổi: `python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/build_catalog.py`. **Không đụng** `verified_external/`, `process_flows.md` (viết tay) |
