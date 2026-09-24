# Sổ tay bảo trì workspace

> Các thao tác housekeeping của workspace (không thuộc target SAP nào).
> Cập nhật lần cuối: **2026-08-28**.

---

## 1. Đổi tên folder workspace → mất session cũ trong `/resume`

### Triệu chứng
Sau khi đổi tên thư mục workspace, `/resume` hiện trống hoặc chỉ còn session mới.

### Nguyên nhân
Claude Code lưu transcript theo **đường dẫn workspace đã mã hoá**:

```
~/.claude/projects/<path-đã-mã-hoá>/<session-uuid>.jsonl
```

Quy tắc mã hoá: mọi ký tự không phải chữ/số thành `-`, ký tự non-ASCII cũng thành `-`.
Ví dụ `c:\Users\anltk2\OneDrive\FIS dự án\ABAP_CLOUD_AI\MCP_PhuTAI_GO_DEV`
→ `c--Users-anltk2-OneDrive-FIS-d---n-ABAP-CLOUD-AI-MCP-PhuTAI-GO-DEV`
(`dự án` → `d---n`).

Đổi tên folder ⇒ khoá mã hoá đổi ⇒ Claude Code mở "ngăn" mới, rỗng. **Session cũ không mất**, chỉ nằm ở ngăn mang tên cũ.

### Cách khắc phục

**Bước 1 — tìm ngăn cũ**

```bash
cd ~/.claude/projects && for d in */; do
  n=$(ls -1 "$d"*.jsonl 2>/dev/null | wc -l)
  last=$(ls -t "$d"*.jsonl 2>/dev/null | head -1)
  echo "$n  $(stat -c '%y' "$last" 2>/dev/null | cut -c1-16)  $d"
done
```

**Bước 2 — copy `.jsonl` sang ngăn mới + rewrite path bên trong**

Mỗi dòng JSON có field `"cwd"` trỏ đường dẫn cũ. Trong file, backslash được escape thành `\\`.
Dùng Python (workspace có path non-ASCII → **bắt buộc `-X utf8`**), thay theo regex có ranh giới
để không phá tên anh em cùng tiền tố (ví dụ `ABAP_CLOUD_AI_SYS2`):

```python
PAT = re.compile(rb'ABAP_CLOUD_AI(\\\\|/)ABAP_CLOUD_AI(?![A-Za-z0-9_])')
new, n = PAT.subn(lambda m: b'ABAP_CLOUD_AI' + m.group(1) + b'MCP_PhuTAI_GO_DEV', data)
```

Đọc/ghi ở chế độ **bytes** (`"rb"` / `"wb"`) để không đụng encoding. Giữ mtime gốc bằng `os.utime`.

**Bước 3 — đừng quên sub-folder**

Ngoài `<uuid>.jsonl`, mỗi session có thể có `<uuid>/tool-results/` và `<uuid>/subagents/`.
Không copy thì resume thiếu kết quả tool. Copy nguyên (`cp -rn`), **không** cần rewrite.

**Bước 4 — kiểm chứng trước khi xoá**

```bash
grep -oh '"cwd":"[^"]*"' *.jsonl | sort -u          # path đã đúng chưa
python -X utf8 -c "import json,glob; ..."           # mọi dòng còn parse được không
cmp -s src dst                                      # sub-folder byte-identical
```

**Bước 5 — backup rồi mới xoá**

```bash
tar -czf ~/.claude/backups/project-sessions-<tên>-<ngày>.tar.gz <ngăn-cũ>
tar -tzf ...tar.gz | grep -vc '/$'     # số file trong archive phải khớp find -type f
rm -rf ~/.claude/projects/<ngăn-cũ>
```

### Bẫy đã gặp

| Bẫy | Chi tiết |
|---|---|
| Hook `.claude/` lock chặn cả `~/.claude/` | `workspace-write-guard.sh` match chuỗi `.claude/` trong lệnh, không phân biệt home hay workspace. `rm -rf ~/.claude/projects/...` bị chặn dù nằm ngoài workspace → cần user tự tạo `.claude/.unlock` (agent bị cấm tạo), hoặc user tự chạy lệnh. **Nhớ xoá `.unlock` sau đó.** |
| Thay chuỗi không có ranh giới | `ABAP_CLOUD_AI/ABAP_CLOUD_AI` thay thô sẽ biến `ABAP_CLOUD_AI_SYS2` thành `MCP_PhuTAI_GO_DEV_SYS2`. Bắt buộc dùng negative lookahead `(?![A-Za-z0-9_])`. |
| Heredoc `cat > file.py <<'PY'` rồi chạy | Bị auto-mode classifier chặn. Dùng Write tool tạo script, rồi mới `python -X utf8 <file>`. |
| Agent không sửa được `tools:` / `model:` của subagent | Dù đã có `.unlock`, auto-mode classifier vẫn chặn agent sửa frontmatter `tools:`/`model:` hoặc tạo file mới trong `.claude/agents/` (tự đổi quyền). Phần mô tả (prose) thì sửa được. Cách làm: agent soạn file trong `artifacts/scratchpads/_session/`, user tự copy hoặc dán vào. |

---

## 2. Session tự bị dọn sau 30 ngày

`cleanupPeriodDays` mặc định **30 ngày** (tính theo mtime file `.jsonl`); `~/.claude/settings.json`
hiện **không** set key này → đang chạy mặc định. Session quá hạn bị xoá tự động, kể cả session vừa
migrate sang ngăn mới (vì mtime được giữ nguyên theo bản gốc).

Muốn giữ lâu hơn, thêm vào `~/.claude/settings.json`:

```json
{ "cleanupPeriodDays": 365 }
```

> Quyết định 2026-08-28: **giữ mặc định 30 ngày**, dựa vào bản backup `.tar.gz` thay vì kéo dài retention.

**[Inference]** Ngày 2026-08-28 ngăn `...-UI5` mất session cuối (29/07, vừa tròn 30 ngày) ở thời điểm
không trùng bất kỳ lệnh ghi nào — nhiều khả năng do cơ chế dọn này, nhưng chưa chứng minh được trực tiếp.

---

## 3. Nhật ký

| Ngày | Việc | Kết quả |
|---|---|---|
| 2026-08-28 | Đổi tên `ABAP_CLOUD_AI\ABAP_CLOUD_AI` → `MCP_PhuTAI_GO_DEV`; migrate session | 12 session + 5 sub-folder chuyển sang ngăn mới, 9.006 path rewrite, JSON hợp lệ 100%, sub-folder byte-identical. Backup `~/.claude/backups/project-sessions-ABAP_CLOUD_AI-old-20260828.tar.gz` (7.2 MB, 31/31 file). Ngăn cũ đã xoá. |
| 2026-09-24 | Đối chiếu bài "Dây chuyền 4 agent" (cuongmeai.com) → sửa cấu hình agent + thêm `reviewer-lead` | Sửa tool SAP cũ `sap_nfg/bmw_dev` → `sap_cloud_dev`/`sap_gm2_cus_ro` (consultant-executor, activation-guard), cds-kb chết → `sap-docs-upstream` (consultant-lead), tester-lead → opus. Thêm `reviewer-lead` (opus, chỉ đọc) + Phase 2.5 "Independent Final Review" vào `/sap-dev-create-report` và `/sap-dev-create-transactional-app`. `integrity-check.sh` 6/6 PASS (7 agent). |
