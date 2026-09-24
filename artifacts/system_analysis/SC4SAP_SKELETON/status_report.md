# Báo cáo — Workspace Public Cloud theo khung sc4sap

Cập nhật: 2026-09-24 · Nguồn sự thật: `artifacts/scratchpads/SC4SAP_SKELETON/ledger.md`
Khung tham chiếu: sc4sap v0.6.18 (MIT), bản clone `artifacts/scratchpads/SC4SAP_SKELETON/sc4sap_repo/`.
Không đụng object SAP, package hay TR nào trong toàn bộ task này.
Bản HTML: `artifacts/handbook/workspace-build.html`.

**Ký hiệu tình trạng:** ✅ Xong · 🟡 Dở dang · ⬜ Chưa làm

## 1. Tổng quan

| Nhóm | Mục đích | Số việc | Tình trạng |
|---|---|---|---|
| A | Các quyết định của anh trước khi build | 4 | ✅ 4/4 |
| B | Dọn bản copy của workspace cũ | 4 | ✅ 3/4 · 🟡 B3 |
| C | Nền an toàn (git, memory, hook, MCP) | 5 | ✅ 5/5 |
| D | Chuẩn bị nguồn tham chiếu sc4sap | 1 | ✅ 1/1 |
| E | Build khung theo sc4sap cho Public Cloud | 10 | ✅ 10/10, commit `b659c5a` |
| F | Đóng việc | 3 | ⬜ 0/3 (F2 làm được một phần) |
| G | Việc phụ: catalog CDS released | 1 | ✅ 1/1 (còn 3 câu hỏi mở) |
| H | Đổi rule thường trực: ATC | 1 | ✅ 1/1 |

---

## 2. Chi tiết từng nhóm

### Nhóm A — Quyết định của anh (✅ 4/4)

Mục đích: chốt phạm vi trước khi build, để không phải đoán.

| # | Việc | Anh đã chọn | Tình trạng |
|---|---|---|---|
| A1 | Danh sách module cho lần build đầu | 2026-09-21: **chỉ SD**. 2026-09-23 mở rộng thành **11 module** (xem E10) | ✅ |
| A2 | Ngành / quốc gia | **vn**, không chọn ngành | ✅ |
| A3 | Mức blocklist dữ liệu: minimal / standard / strict | **standard**: minimal (chặn) + dữ liệu giao dịch (hỏi); bỏ phần log audit và workflow | ✅ |
| A4 | Xác nhận `C:\WORK_SPACE` là workspace mới | "đây là work space mới"; workspace cũ giữ lại 11 target cũ | ✅ |

### Nhóm B — Dọn bản copy (✅ 3/4 · 🟡 1)

Mục đích: bản copy không mang theo rác, secret hay đường dẫn phụ thuộc workspace cũ.

| # | Việc | Nội dung đã làm | Tình trạng |
|---|---|---|---|
| B1 | Bỏ `.venv_markitdown` (371 MB) | Anh xoá ngày 21. Ngày 23 cài lại theo yêu cầu (346 MB, markitdown 0.1.8), chuyển thử HTML → md đạt. **Vẫn thiếu `scripts/office_to_md.py`** nên skill convert chưa đọc được DOCX/XLSX | ✅ (còn treo phần script) |
| B2 | Soát secret trong `.mcp.json` | Không có password (dùng cookie). Phát hiện API key của `sap-docs` nằm thẳng trong args, nên đã chặn không cho vào git (C1) | ✅ |
| B3 | Xoá `.claude/.unlock` cũ, chỉ tạo lại khi cần sửa `.claude/` | Anh đã xoá rồi tạo lại cho nhóm E. **Hiện `.unlock` vẫn còn**, lock đang tắt | 🟡 chờ anh xoá (gộp với F3) |
| B4 | Tách vsp.exe và cookie khỏi workspace cũ | `.mcp.json` trỏ `C:/WORK_SPACE/tools/vsp/`; mỗi tenant một file cookie (`cookies_dev.txt` cho 080, `cookies_cus.txt` cho 100). Cookie refresh lại ngày 23 | ✅ |

### Nhóm C — Nền an toàn (✅ 5/5)

Mục đích: có điểm rollback, memory riêng, hook hoạt động đúng, MCP chạy được.

| # | Việc | Nội dung đã làm | Tình trạng |
|---|---|---|---|
| C1 | `git init` + commit baseline | Commit `b167a9d` (374 file), không có secret trong HEAD. Hook chặn tạo `.gitignore` ở root, nên quy tắc ignore nằm ở `.git/info/exclude` (không đi theo repo) | ✅ |
| C2 | Memory riêng cho workspace | `autoMemoryDirectory` = `~/.claude/auto-memory/Work_space` (phải nằm ngoài workspace). Chép 18 memory cần thiết, sửa 7 cái cho hợp workspace mới | ✅ |
| C3 | `jq` có sẵn, matcher hook khớp tên server | jq 1.8.2 có sẵn. Lúc đó server 100 **không** bị hook nào chặn ghi. Đã vá ở E7 | ✅ |
| C4 | Test hook chặn (Z/Y, package, TR) | 10 payload giả: đúng hết, trừ lỗ hổng `edit` bỏ qua kiểm Z/Y. **Đã vá ngày 21**: `edit` giờ cũng bắt buộc Z/Y | ✅ |
| C5 | MCP sống | `search ZCL_*` chạy trên cả hai server (21/09); kiểm lại sau restart ngày 23 | ✅ |

### Nhóm D — Nguồn tham chiếu (✅ 1/1)

| # | Việc | Nội dung đã làm | Tình trạng |
|---|---|---|---|
| D1 | Clone sc4sap (chỉ đọc) | `git clone --depth 1` vào `artifacts/scratchpads/SC4SAP_SKELETON/sc4sap_repo/` (git bỏ qua thư mục này). Đã đọc `common/`, `exceptions/`, `configs/`, `hooks/`, `tests/` | ✅ |

### Nhóm E — Build khung (✅ 10/10, commit `b659c5a`)

Mục đích: lấy khung của sc4sap (config theo tầng, blocklist dữ liệu, hook, kiểm tra tự động) và viết lại cho Public Cloud.

| # | Việc | Nội dung đã làm | Bằng chứng | Tình trạng |
|---|---|---|---|---|
| E1 | Thư mục khung | `.claude/common/`, `configs/`, `exceptions/`, `scripts/`. Đặt trong `.claude/` vì hook chặn file mới ở root | — | ✅ |
| E2 | Tách rule theo tầng | Giữ §1–§14 tại chỗ, thêm §15 + `context-loading-protocol.md` (4 tầng nạp). `CLAUDE.md` tự nạp `system-config.md`; 6 agent có khối "Mandatory baseline" | 0/60 file tham chiếu `§N` bị gãy | ✅ |
| E3 | File cấu hình hệ thống | `common/system-config.md`: Public Cloud, 11 module, vn, DEV, blocklist standard, 080 ghi, 100 chỉ đọc. Hook đọc trực tiếp file này | Release/FPS để trống có chủ đích (080 không đọc được) | ✅ |
| E4 | Ràng buộc ABAP Cloud | `common/cloud-abap-constraints.md`: câu lệnh cấm, API thay thế, bảng chuyển hướng workflow | 20 class tra kho release: 19 released, bỏ `CL_DEMO_XML_ACCESS` | ✅ |
| E5 | Config SD | `configs/SD/`: README, released-objects, functional | 43 BDEF + 7 enhancement spot + 58 BAdI interface released | ✅ |
| E6 | Blocklist dữ liệu | `exceptions/README.md` + 9 file: 8 file chặn (dữ liệu cá nhân, bank, địa chỉ, user, HR, thuế, giá, Z nhạy cảm), 1 file hỏi (chứng từ giao dịch) | Tên view đối chiếu catalog + sap-docs, tên không kiểm được thì bỏ | ✅ |
| E7 | Hook | 5 hook mới (xem 3.1), đăng ký trong `settings.json`; kiểm TR dùng lại `pre-cud-guard.sh` | Chạy thử 34/34; sau restart chạy thật | ✅ |
| E8 | Script kiểm tra toàn vẹn | `bash .claude/scripts/integrity-check.sh`: 6 phép kiểm (skill, agent, tham chiếu, hook, tầng config) | 6/6 PASS; test âm bắt đúng lỗi | ✅ |
| E9 | Ghi chú theo target | Rule §4/§14: kiến thức riêng của từng báo cáo vào `artifacts/system_analysis/<TARGET>/notes/`. Sửa skill scratchpad/handoff + 2 command | Memory cập nhật, không tạo trùng | ✅ |
| E10 | Mở rộng ra 11 module | Thêm FI, CO, MM, PP, QM, PM, PS, TM, EWM, TR (xem 3.2) | integrity 6/6; bật module không có README bị bắt | ✅ |

**Git:** commit `b659c5a` (2026-09-24), đã merge vào `main` và **push lên GitHub** `kienannh0403/sap_cloud_ai_workspace` (private) — `main` = `2ecda22`. Không commit `.claude/Documents/` (xlsx, chờ anh quyết) và `artifacts/scratchpads/_session/` (snapshot tự sinh).

### Nhóm F — Đóng việc (⬜ 0/3)

Mục đích: kiểm tra lần cuối, ghi tài liệu, khoá lại `.claude/`.

| # | Việc | Nội dung | Tình trạng |
|---|---|---|---|
| F1 | Chạy integrity check sau mọi thay đổi `.claude/` | Script đã chạy 6/6 PASS sau lần sửa cuối, **nhưng chưa ghi vào dòng F1 của ledger** | ⬜ (chỉ còn ghi ledger) |
| F2 | Handbook + `SC4SAP_SKELETON/INDEX.md` | Handbook **đã có**: `artifacts/handbook/workspace-build.html`, đã link từ trang chủ. **INDEX.md chưa có** (rule §4 bắt buộc) | 🟡 một phần |
| F3 | Anh xoá `.claude/.unlock` | Chờ xong F1, F2 và các sửa `.claude/` còn lại | ⬜ việc của anh |

### Nhóm G — Catalog CDS released (✅ 1/1)

| # | Việc | Nội dung đã làm | Tình trạng |
|---|---|---|---|
| G1 | Catalog CDS released theo module | `artifacts/system_analysis/CDS_RELEASED_CATALOG/`: 4.025 view chia 41 folder, quan hệ giữa các module, trang handbook `cds-catalog.html`. Ngày 23 bổ sung `verified_external/` (FI, CO, PP, LE-TM, QM đã verify thật ở dự án khác). Đã commit (`c283cda`) | ✅ |

**Câu hỏi mở của G1:** (a) Sheet1 có đúng danh sách module anh muốn ưu tiên không; (b) file xlsx đang nằm trong `.claude/Documents/`, trái rule §4; (c) sửa skill `find-released-cds-view` để tra catalog này trước (cần `.unlock`).

### Nhóm H — Rule thường trực (✅ 1/1)

| # | Việc | Nội dung đã làm | Tình trạng |
|---|---|---|---|
| H1 | ATC bắt buộc (Gate 4) | Mỗi lần create/edit/delete phải có 0 lỗi ATC **mới** (chỉ tính dòng mình sửa, mọi package). Sửa skill `activation-guard` và 8 file đang ghi "3 gate". Đã commit (`8d59813`) | ✅ |

## 2b. Cập nhật 2026-09-24 — sau nhóm E

Tất cả đã commit và push lên GitHub `kienannh0403/sap_cloud_ai_workspace` (private).

| Việc | Nội dung | Commit | Tình trạng |
|---|---|---|---|
| Đưa repo lên GitHub | Merge commit "Initial commit" của GitHub (giữ README của workspace), push `main`; không force, không có secret trong lịch sử | `2ecda22` | ✅ |
| README tiếng Việt | Viết lại toàn bộ theo workspace hiện tại; bỏ ghi chú fork và link repo ngoài | `387d4d1` | ✅ |
| Miễn TR cho cây ZLOCAL | `$TMP` + `ZLOCAL` và 17 package con/cháu (đọc trên 080), danh sách `LOCAL_NO_TR_PACKAGES` trong `system-config.md`; package mới dưới ZLOCAL phải thêm tên. Chạy thử 12/12 | `c103b9f` | ✅ |
| Naming convention theo sheet dự án | Skill theo `artifacts/naming_convention/`: CDS/RAP `Z<prefix>_<module>_<tcode>`, service `_O2/_O4`, thêm communication / IAM / job / launchpad `_UI5R` / form; 23/23 dòng sheet có trong skill | `6206795` | ✅ |
| reviewer-lead + sửa tools của agent | (anh làm) agent `reviewer-lead` + Phase 2.5 cho `/sap-dev-create-*`; agent consultant trỏ đúng MCP | `de0eac2` | ✅ |
| README + CLAUDE.md theo reviewer-lead | Badge 7 subagent, sơ đồ có bước duyệt; `CLAUDE.md` bỏ dòng fork, liệt kê MCP đang dùng thật | `7c0a5f6`, `40b0325` | ✅ |

---

## 3. Chi tiết bổ sung cho nhóm E

### 3.1 Hook mới

| Hook | Khi nào chạy | Làm gì | Thử thật sau restart |
|---|---|---|---|
| `tier-readonly-guard.sh` | Trước mọi lệnh MCP SAP | Chặn create/edit/delete trên client 100. Nếu tier khác DEV thì chặn mọi thao tác ghi | `edit` trên 100 → bị chặn |
| `block-forbidden-tables.sh` | Trước MCP `query` và Bash `datapreview` | Dữ liệu cá nhân, giá, HR, bank, thuế: **chặn**. Chứng từ bán, giao, hoá đơn, mua, kế toán: **hỏi anh** | Lệnh `echo … KNA1` và query `I_Customer` → bị chặn |
| `activation-verify.sh` | Sau khi ghi object trên 080 | Nhắc chạy đủ 4 gate activation-guard | Chạy thử OK |
| `session-start.sh` | Mở, resume, sau compact | Tóm tắt cấu hình, cảnh báo `.unlock`, chỉ ledger/handoff gần nhất | Đã hiện ở đầu phiên |
| `pre-compact.sh` | Trước compact | Snapshot vào `artifacts/scratchpads/_session/` (giữ 10 bản), nhắc chạy handoff | Chạy thử OK |

### 3.2 Mười một module

Anh chọn "10 module Public Cloud", cộng SD là 11. Bỏ Ariba, BW, HCM vì không có module ABAP trên Public Cloud.

| Module | File | Điều cần nhớ |
|---|---|---|
| SD | README + released-objects + functional | Pricing element bị chặn đọc; đơn bán hàng và hoá đơn phải hỏi anh |
| FI | README + released-objects | BO bút toán `I_JournalEntryTP` nằm ở AC-INT. **VN eInvoice: `I_VN_EDocInvoice` released** |
| CO | README + released-objects | `I_ActualCostRate` có annotation nhưng không dùng được; ghi qua `I_ActualCostRateTP` |
| MM | README + released-objects | **`I_PurchaseOrder` KHÔNG released** → `I_PurchaseOrderAPI01`. `ME_PROCESS_PO_CUST` → `ES_MMPUR_PROCESS_PO_CLOUD` |
| PP | README + released-objects | Đơn sản xuất đọc qua `I_ManufacturingOrder`; BOM dùng họ `…DEX_2/_3`; `WORKORDER_UPDATE` → `ES_COBADICFL_MFGORDER` |
| QM | README | Tên view là `I_QltyNotification`, không phải `I_QualityNotification` |
| PM | README | **`I_MaintenanceOrder` KHÔNG released** → `I_MaintenanceOrderBasic` |
| PS | README | Không còn PS cổ điển: Enterprise Projects (PPM-SCL). `I_Project`/`I_WBSElement*` không released |
| TM | README | Chỉ đọc qua họ view TP; catalog local không có TP |
| EWM | README | Thay cho WM; chỉ 1 BO released |
| TR | README | Treasury; vài view deprecated, đã ghi bản thay thế |

Thay đổi đi kèm:
- Agent consultant chỉ đọc README của module mà FS đụng tới.
- Blocklist thêm view PO và hoá đơn nhà cung cấp, ở mức hỏi xác nhận.

### 3.3 Kết nối và memory (ngày 23)

- **Cookie:** refresh cả hai tenant (100: 17:14, 080: 17:17). Sau restart, `search ZCL_*` chạy được trên cả hai server.
- **Memory mới:** `hook-live-test-no-real-sensitive-query`.
- **Memory đã sửa:**
  - `phutai-go-cus-connection`: chặn ghi trên client 100 giờ do hook đảm nhận.
  - `artifacts-per-tcode-layout`: `notes/` đã vào rule.

### 3.4 File thay đổi (commit `b659c5a`)

- **Mới:**
  - `.claude/common/` (3), `.claude/configs/` (11 module), `.claude/exceptions/` (10).
  - 7 file trong `.claude/hooks/`, 2 file trong `.claude/scripts/`.
- **Sửa:** `sap-dev-rule.md`, `settings.json`, `CLAUDE.md`, 6 agent, skill scratchpad/handoff, 2 command, ledger.
- **Handbook:** thêm `workspace-build.html`; sửa `index.html`, `mcp.html`, `cds-catalog.html` (thêm link).

---

## 4. Việc còn treo (gom từ tất cả các nhóm)

| # | Việc | Thuộc nhóm | Ai | Ghi chú |
|---|---|---|---|---|
| 1 | ~~Commit + push nhóm E~~ — xong: `main` = `2ecda22` trên GitHub `kienannh0403/sap_cloud_ai_workspace` | E | — | Đã xong 2026-09-24 |
| 2 | Tạo `SC4SAP_SKELETON/INDEX.md` | F2 | Em | Rule §4 bắt buộc |
| 3 | Ghi kết quả integrity vào dòng F1 | F1 | Em | Đã có 6/6 PASS |
| 4 | Xoá `.claude/.unlock` | B3, F3 | **Anh** | Sau khi xong mục 1–3 và 5 |
| 5 | ~~Sửa `tools:` của 2 agent consultant~~ — xong trong commit `de0eac2` (2026-09-24): agent trỏ `sap_cloud_dev` / `sap_gm2_cus_ro` / `sap-docs-upstream`; kèm thêm `reviewer-lead` + Phase 2.5 | ngoài ledger | — | Đã xong |
| 6 | Kiểm phần *unverified* trong `configs/` trên tenant | E5, E10 | Em | Chưa object nào đọc thử trên 080 |
| 7 | `country/vn.md` | A2 | Anh quyết | Mới có `I_VN_EDocInvoice` trong FI README |
| 8 | 2 hook cũ: đường dẫn tương đối, `timeout: 5000` (giây) | C3 | Em, khi anh đồng ý | Hook mới đã dùng `$CLAUDE_PROJECT_DIR` |
| 9 | File xlsx nằm trong `.claude/Documents/` | G1 | Anh quyết | Đề xuất chuyển sang `artifacts/` |
| 10 | Thiếu `scripts/office_to_md.py` | B1 | Anh quyết | Skill convert chưa đọc được DOCX/XLSX |
| 11 | `.gitignore` thật (hiện ở `.git/info/exclude`) | C1 | Anh | Hook chặn em tạo file ở root |
| 12 | Xác nhận Sheet1 của catalog; sửa skill `find-released-cds-view` | G1 | Anh / Em | Skill cần `.unlock` |
| 13 | Thư mục `artifacts/scratchpads/_session/` | E7 | — | Hook `pre-compact` tự tạo; có thể đưa vào ignore |

## 5. Đề xuất thứ tự tiếp theo

1. Em sửa mục 8, 12 nếu anh muốn, trong lúc `.unlock` còn mở, rồi chạy integrity check.
2. Em làm F1 và INDEX.md (F2).
3. Commit + push phần nhóm F lên GitHub.
4. Anh xoá `.claude/.unlock`.

## 6. Ghi chú quá trình

- Lần đầu làm nhóm E ở auto mode bị chặn (`[Self-Modification]`). Em làm lại ở manual mode; thư mục staging tạm đã xoá.
- Khi thử hook, em đã gửi query `I_Customer` thật lên 080 vì tưởng cookie đã chết, nhưng server còn sống. Hook đã chặn, và 080 không có quyền đọc dữ liệu, nên không lộ gì. Đã ghi thành memory `hook-live-test-no-real-sensitive-query`.
