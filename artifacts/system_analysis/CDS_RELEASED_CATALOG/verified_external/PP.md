# PP — verified external (PIR, PP-VDM)

Nguồn: xem `README.md` cùng thư mục. Đối chiếu 2026-09-23: toàn bộ view PIR dưới đây có trong `catalog_all.csv`,
folder `PP-MRP_MRP` — xác nhận việc gán bằng **từ khoá tên view** (`match_basis=keyword`, xem `module_map.md`)
cho `PP-MRP` trong catalog này là **đúng hướng**, các view PIR thật đúng là PP-VDM/MRP.

## View landscape PIR (Planned Independent Requirement, ~ MD63) — tất cả released `PP-VDM-2CL`

| View | Mô tả | Dùng khi |
|---|---|---|
| `I_PlndIndepRqmtByIntKey` | Header PIR (key nội bộ) | Filter theo Version, RequirementPlan, Plant, Product |
| `I_PlndIndepRqmtItemByIntKey` | Item PIR (flat, theo `WorkingDayDate`) | Lấy planned qty theo ngày; join header lấy Version |
| `I_PlndIndepRqmtItemHistory` | Item history dạng phẳng, có `ForecastYearMonth` trực tiếp | **View tốt nhất cho pivot theo tháng** — không cần join header |
| `I_ActivePlndIndepRqmt` / `I_ActivePlndIndepRqmtItem` | Header/item — chỉ version ACTIVE | Chỉ cần PIR đã activate |
| `I_PlndIndepRqmtType` / `I_PlndIndepRqmtTypeText` | Loại PIR + text | Value help |

**Write BO**: `I_PlndIndepRqmtTp` (BDEF, released `PP-MP-DEM-2CL`) — **KHÔNG có trong `catalog_all.csv`** (catalog
xlsx này chỉ có CDS view thường, không có behavior-projection/TP). Với mọi nhu cầu **ghi** PIR, tra riêng qua ADT
BDEF search, đừng trông đợi tìm thấy trong catalog view-only này.

## Field map (tên field thật, đã verify — không đoán)

| Ý nghĩa | Field | View | Ghi chú |
|---|---|---|---|
| Material | `Product` | cả 5 view | CHAR, map MATNR |
| Plant | `Plant` | cả 5 view | |
| Version (AOP/FC...) | `PlndIndepRqmtVersion` | header views | CHAR2 — **mã thật khác theo tenant**, xác nhận trên hệ thống, đừng đoán từ nhãn FS |
| Cờ Active | `PlndIndepRqmtIsActive` | `ByIntKey`, `ItemHistory` | space=inactive, `'X'`=active |
| Requirements Plan | `RequirementPlan` | cả 5 view | |
| Số lượng kế hoạch | `PlannedQuantity` | item views | QUAN |
| Kỳ tháng/năm (pivot) | `ForecastYearMonth` | **chỉ** `ItemHistory` | NUMC6, format YYYYMM |
| Kỳ ngày cụ thể | `WorkingDayDate` | `ItemByIntKey`, `ActivePlndIndepRqmtItem` | DATS |
| Loại kỳ (tháng/tuần) | `ForecastPeriodType` | `ItemHistory` | 'M'/'W' theo tài liệu chuẩn — **verify giá trị thật trên tenant trước khi lọc** (một tenant lưu PIR theo ngày, lọc `='M'` ra rỗng dù dữ liệu tồn tại) |
| Số lượng rút | `WithdrawalQuantity` | item views | |
| Cờ xoá | `PlndIndepRqmtIsToBeDeleted` | header/ItemHistory | |
| ĐVT | `BaseUnit` | item views | |

## Bẫy tổng quát

- **`ProductionVersion` (VERID) KHÔNG có ở bất kỳ view PIR nào** (header lẫn item) — PIR không gắn 1 production
  version cụ thể theo thiết kế chuẩn SAP. Yêu cầu FS kiểu "tổng theo mọi production version" thực chất chỉ là
  GROUP BY Product+Plant+Period+Version, không phải join Production Version.
- **`I_PlndIndepRqmtItemHistory` không liệt kê `PlndIndepRqmtVersion` như scalar field trực tiếp** trong một số
  bản catalog — field này thật ra ở header view; nếu không thấy trực tiếp, join tường minh với
  `I_PlndIndepRqmtByIntKey` qua `PlndIndepRqmtInternalId` trước khi kết luận field không tồn tại.
- **Đừng giả định giá trị code** (Version, PeriodType...) giống tài liệu mẫu — luôn lấy giá trị thật đang tồn tại
  trên dữ liệu của tenant trước khi viết filter, một filter "đúng theo tài liệu" có thể lọc mất 100% dữ liệu thật.

## Liên quan

- `I_ProductionVersion` — released `PP-VDM-MD-2CL`. Key material = **`Material`** (Product chỉ là assoc).
- Cost cube liên quan production order (`I_MfgOrderActlPlanTgtLdgrCost`) — xem `CO.md` cùng thư mục.
