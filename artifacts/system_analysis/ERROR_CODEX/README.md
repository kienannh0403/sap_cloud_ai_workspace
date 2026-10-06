# Error Codex — lỗi đã gặp, tra theo mã lỗi

Mỗi **nguyên nhân gốc** là một file `entries/<id>.json`. Tra theo thứ có trên màn hình (message ID, HTTP status,
tên exception, dòng log), không theo tiêu đề. Ý tưởng và schema gốc: [StormShynn/sap-error-codex](https://github.com/StormShynn/sap-error-codex)
(MIT); workspace thêm `evidence`, `occurrences`, `source`. Bắt đầu 2026-10-06 với 12 lỗi **đã verify** của chính
workspace (memory + `notes/` của target); lỗi của repo kia chỉ thêm khi mình thật sự gặp và kiểm chứng.

```bash
python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py find "<mã lỗi hoặc đoạn text>"
python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py show <id>
python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py check     # chạy sau mọi lần thêm / sửa entry
python -X utf8 artifacts/system_analysis/ERROR_CODEX/codex.py list
```

## Khi nào ghi — và ghi thế nào (không bao giờ trùng)

Triage ([Skill: sap-analyze-symptom]) và `/sap-dev-bug-fix` **tra codex trước**. Khi nguyên nhân gốc đã được chứng minh:

| Trường hợp | Làm gì |
|---|---|
| Cùng mã lỗi, **cùng nguyên nhân** với một entry | KHÔNG tạo file. Thêm 1 dòng `occurrences` (`target`, `date`, `note`), sửa `updatedAt`; cách sửa lần này chạy thật mà entry còn `verified: false` → nâng `true` + thêm `evidence`; có cách sửa tốt hơn → bổ sung `solutions` |
| Cùng mã lỗi, **nguyên nhân khác** (vd 412 do ETag ≠ 412 do `reported` thiếu `failed`) | Entry MỚI cho nguyên nhân mới, dùng chung `msgKeys` — `find` trả về cả hai |
| Mã lỗi chưa có | Entry mới |

Sau đó `codex.py check` phải exit 0: exit 1 = sai schema; exit 3 = hai entry chung `msgKeys` và nguyên nhân giống
nhau ≥ 55% → xem lại, gộp nếu là một. **Một lỗi gặp ≥ 3 lần ở các target khác nhau** (`occurrences`) = thiếu phòng
ngừa → đề xuất patch skill / rule cho user duyệt (rule §14), không tự sửa.

Phân vai: codex = lỗi dùng lại được giữa các target, tra theo mã · `targets/<T>/notes/` = chi tiết riêng của target
(codex trỏ tới qua `evidence` / `occurrences`) · memory = quy tắc làm việc, không chép lại nội dung lỗi.

## Schema

| Trường | Ý nghĩa |
|---|---|
| `title` | Dòng mô tả cái người dùng **thấy**, không phải cái mình đoán là nguyên nhân |
| `module` | `RAP / ABAP Cloud` · `CDS / Fiori Elements` · `Fiori / UI5` · `Integration / OData` · `Tooling / MCP` · `Transport & Release` · `Basis / Auth` |
| `severity` | `Blocker` · `High` · `Medium` · `Low` |
| `verified` | `true` chỉ khi cách sửa đã chạy trên hệ thống thật và có `evidence`; `false` = từ tài liệu / blog — kiểm trước khi dùng |
| `msgKeys` | Mọi chuỗi người ta sẽ tìm: message ID, HTTP status, exception, đoạn log nguyên văn |
| `symptom` | Dòng log / màn hình quyết định, nguyên văn |
| `rootCause` | Vì sao. Chưa chắc thì ghi rõ "Not verified" và liệt kê khả năng |
| `solutions[]` | `label`, `body`, `recommended` (ít nhất 1 cái `true`) |
| `prevention` | Đổi gì để không lặp lại |
| `evidence[]` | Đường dẫn note / odata_verify / memory / lần chạy chứng minh |
| `occurrences[]` | `{target, date, note?}` mỗi lần gặp |
| `refs[]`, `source` | Nguồn ngoài; `own` hoặc tên repo nguồn |
| `createdAt`, `updatedAt` | `YYYY-MM-DD` |

Không ghi hostname, user, số TR thật hay dữ liệu kinh doanh vào entry.
