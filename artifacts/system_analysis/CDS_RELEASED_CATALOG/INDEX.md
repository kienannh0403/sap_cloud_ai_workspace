# CDS_RELEASED_CATALOG — INDEX

**Là gì:** danh mục **4.025 CDS view released** (file có 4.489 dòng, 464 dòng trùng hệt) chia theo phân hệ, mỗi phân hệ một folder,
kèm quan hệ giữa các phân hệ. Nguồn: `.claude/Documents/CDSView_Released_updated (1).xlsx` (sheet CDS, Fields, Sheet1).
Thay cho `cds-kb` MCP đang chết (xem memory `cds-kb-mcp-endpoint-dead`).

**Trạng thái (2026-09-23):** đã sinh xong, kiểm tra tổng: 41 folder, 4.025 view, mỗi view đúng 1 folder. Đã bổ
sung `verified_external/` (đối chiếu với kiến thức đã verify thật từ một dự án khác). Chưa commit git.

## Cách dùng khi làm báo cáo / chức năng
1. Xác định phân hệ của báo cáo → mở `modules/<folder>/README.md` rồi tra `views.csv` (cột `key_entities` cho biết view có Customer / Material / Company Code...).
2. Có phân hệ đó trong `verified_external/` (FI, CO, PP, LE-TM, QM) → đọc trước, đó là field/bẫy **đã verify thật**, tin cậy hơn `views.csv` (chỉ dựa vào tên).
3. Không thấy → xem bảng "Phân hệ liên quan" cuối README, hoặc `relations/entity_hubs.md` (biết *dữ liệu gì*, chưa biết *view nào*).
4. Vẫn không thấy → grep `catalog_all.csv` (mọi view, có cột `folder`); ngoài file thì mới ra sap-docs / hệ thống.
5. View trong file = *released theo nguồn user*, **chưa verify trên hệ thống**: lần đầu dùng đọc lại bằng `SAP(action=read, target=DDLS <tên>)`.

## Giới hạn phạm vi (quan trọng, phát hiện 2026-09-23 khi đối chiếu `verified_external/`)
- **Catalog chỉ có CDS view đọc thường** (sheet "CDS" của xlsx). **Không có BDEF/behavior-projection ("TP")** —
  mọi BO ghi/action (`I_PlndIndepRqmtTp`, `I_FreightOrderTP` và cả họ, `I_ActualCostRateTP`...) **hoàn toàn vắng
  mặt**, kể cả ở `_fields_only/`. Cần ghi/action → tra thẳng ADT/BDEF, đừng tìm trong catalog này.
- **"Không có trong `catalog_all.csv`" ≠ "không released".** Một số view đã verify released thật lại **chỉ có ở
  sheet Fields của xlsx**, không có ở sheet CDS: `I_TaxCodeRate`, `I_ActlCostGMatlValueChainItem`,
  `I_ActualCostingRunResult`, `I_ActualCostingActivityResult`, `I_InventoryPriceByKeyDate_2`,
  `I_BillingDocument(Item)`. Trước khi kết luận "view này không có/không released", kiểm cả `_fields_only/`.
- **Annotation `#PUBLIC_LOCAL_API` KHÔNG đồng nghĩa với released C1.** `I_ActualCostRate` và
  `I_AccountingCostRate_2` có annotation này nhưng dùng trong class ABAP Cloud báo "use not permitted" — chỉ
  `released-objects-index.json` (hoặc View Browser ADT) mới xác thực được. Xem `verified_external/CO.md`.
- **Tên view có thể khác trực giác.** Vd `I_QltyNotification` (không phải `I_QualityNotification`) — xem
  `verified_external/QM.md`. Luôn xác nhận tên tồn tại (search/read) trước khi đưa vào TS, đừng suy tên đầy đủ
  từ business term.

## Quyết định ngoài yêu cầu gốc
- 16 phân hệ ưu tiên lấy từ **Sheet1**; phần còn lại gom `<TOP>_other` hoặc `<TOP>` (25 folder).
- Sheet1 ghi 4 component **không có trong file**: `PS` → gán `PPM-SCL-*` (alias); `EAM-OBJ` → `PM-EQM-EQ/FL` (alias);
  `PP-SFC` và `PP-MRP` → gán **theo từ khoá tên view** (suy luận); `EAM-WCM` → **0 view**, folder chỉ có README.
- 1.914 view chỉ có ở sheet Fields (không có ở CDS) → tách ra `_fields_only/`, không coi là released.
- "Liên quan" = cùng >= 2 view dùng chung một entity (theo data element); bảng entity do em chọn tay (`ENTITY_MAP` trong script). Không phải association CDS.

## Câu hỏi mở
- Sheet1 có đúng là danh sách phân hệ anh muốn ưu tiên không? Có cần `EAM-WCM` (file không có view nào)?
- `I_BillingDocument`/`Item` thật ra có ở sheet Fields (released [Unverified] theo nguồn ngoài) — không thấy ở sheet CDS. `I_Material`, `I_ProductionOrder` (khác `I_ProductionVersion`, đã verify released), `I_SalesPricingCondition` vẫn chưa thấy ở đâu trong file — tra sap-docs trước khi kết luận.
- File nằm trong `.claude/Documents/` (rule §4: output không đặt trong `.claude/`); cân nhắc chuyển sang `artifacts/`.

## Bản đồ file
| Đường dẫn | Nội dung |
|---|---|
| `modules/<folder>/README.md` + `views.csv` | tóm tắt + toàn bộ view của phân hệ (sinh tự động) |
| `catalog_all.csv` | mọi view + cột `folder` |
| `module_map.md` | luật gán + bảng component → folder |
| `relations/module_pairs.md` / `.csv`, `entity_hubs.md` | quan hệ phân hệ, entity → phân hệ |
| `process_flows.md` | luồng O2C / P2P / sản xuất (kiến thức SAP, không từ file) + bẫy |
| `_fields_only/` | view chỉ có ở sheet Fields (một số đã verify released thật — xem README trong đó) |
| `verified_external/` | field/bẫy CDS **đã verify thật** đối chiếu từ dự án khác (FI, CO, PP, LE-TM, QM) — tin cậy hơn `views.csv` |
| `build_catalog.py` | sinh lại `modules/`, `catalog_all.csv`, `module_map.md`, `relations/`, `_fields_only/` khi file xlsx đổi: `python -X utf8 artifacts/system_analysis/CDS_RELEASED_CATALOG/build_catalog.py`. **Không đụng** `verified_external/`, `process_flows.md` (viết tay) |
