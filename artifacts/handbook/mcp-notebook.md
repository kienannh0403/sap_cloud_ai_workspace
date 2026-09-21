# Sổ tay MCP — workspace ABAP_CLOUD_AI

> Ghi lại **làm được gì qua MCP, làm thế nào, và bẫy ở đâu** — cộng nhật ký theo từng báo cáo.
> Phần 1–3 là tra cứu, dùng lại cho mọi target. Phần 4 là nhật ký, ghi thêm khi làm target mới.
>
> Cập nhật lần cuối: **2026-08-19**.
> Nguồn chi tiết của từng target vẫn là `artifacts/system_analysis/<TARGET>/INDEX.md` — sổ tay này không thay thế.

---

## 1. Môi trường

| | |
|---|---|
| Hệ thống | S/4HANA Public Cloud, host `my437569.s4hana.cloud.sap`, client `080`, system `GM2` |
| Vai trò | **DEV** — mọi connection trong workspace này được coi là DEV |
| User | `CB9980000022` |
| MCP đọc/ghi ABAP | `sap_cloud_dev` (vsp / mcp-abap-adt-go), tool `SAP` |
| MCP tài liệu | `sap-docs` — `search`, `fetch`, `sap_search_objects`, `abap_feature_matrix`… |
| MCP tài liệu (dự phòng) | `sap-docs-upstream` — cùng bộ tool, endpoint của Marian Zeis |
| MCP `cds-kb` | ⚠️ **chết** — xem §1.2 |
| Package local, **không cần TR** | `ZANLTK2`, `$TMP` (allowlist trong `.claude/hooks/pre-cud-guard.sh`) |
| Mọi package khác | **transportable → bắt buộc TR**, và agent không bao giờ được tạo/sửa/xoá TR |

### Cookie — hai đường đọc, hai cookie khác nhau

Đây là chỗ gây mất thời gian nhiều nhất.

- **MCP `sap_cloud_dev`** giữ cookie riêng, đọc **một lần lúc vsp startup**. Refresh file cookie **không** làm MCP tỉnh lại → phải `/mcp reconnect sap_cloud_dev` trong terminal thật, hoặc restart Claude Code.
- **`curl` + ADT REST** dùng `tools/vsp/cookies.txt`. Đây là đường duy nhất đọc được những loại object MCP không hỗ trợ.
- Hai cái này **trôi lệch nhau**. Đã gặp cả hai chiều: MCP còn sống mà curl đã hết hạn (2026-08-13), và curl vừa refresh mà MCP vẫn dùng cookie cũ (2026-07-30).

**Dấu hiệu cookie hết hạn:** request trả **HTTP 200** nhưng body là trang HTML SAML login, không phải source. Kiểm bằng `head -c 20 <file> | grep "<html"`.

**Lệnh refresh — copy nguyên, đừng mò lại** (chi tiết đầy đủ trong memory `sap-cloud-dev-connection`):

```bash
cd "c:/Users/anltk2/OneDrive/FIS dự án/ABAP_CLOUD_AI/MCP_PhuTAI_GO_DEV"
./tools/vsp/vsp.exe --url https://my437569.s4hana.cloud.sap --client 080 --user CB9980000022 \
  --browser-auth --browser-auth-timeout 5m \
  --browser-exec "C:/Program Files/Google/Chrome/Application/chrome.exe" \
  --cookie-save tools/vsp/cookies.txt
```

Ba điều **bắt buộc**, thiếu là mất 30 phút:

1. `--browser-exec` trỏ **Chrome**. Bỏ đi thì vsp auto-detect Edge và panic `close of closed channel` (chromedp `allocate.go`) ngay sau dòng `SSO redirect in progress`. Xác nhận 2026-08-11 và lại 2026-09-03.
2. `--browser-auth-timeout 5m` — mặc định 2m không đủ để login SSO tay.
3. **Không** pipe qua `head` (SIGPIPE giết vsp giữa lúc poll) và **không** để `SAP_COOKIE_FILE` trong env của lệnh này (vsp abort: *only one authentication method*). Chạy `run_in_background: true` rồi đọc file output.

Thành công khi thấy: `Authentication successful! Extracted 2 cookies` + `Cookies saved to ...`.

Kiểm cookie mới bằng curl (`cd tools/vsp` trước, path tương đối — path non-ASCII curl gửi thiếu cookie im lặng):

```bash
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" -b cookies.txt \
  "https://my437569.s4hana.cloud.sap/sap/bc/adt/discovery"
```

`200 application/atomsvc+xml` = sống. `200 text/html` = vẫn là trang SAML → chưa được.

Xong rồi **mới** restart VS Code. Restart trước khi có cookie mới là vô nghĩa — MCP chỉ nạp lại đúng file cookie hết hạn đó.

### 1.2 `cds-kb` — server đã chết, không phải lỗi config

Kiểm 2026-08-18: endpoint trong `.mcp.json` (`https://cds-kb-mcp-production.up.railway.app/sse`) trả **404 `{"status":"error","code":404,"message":"Application not found"}`** ở cả `/`, `/sse` và `/mcp`. Đây là 404 ở tầng Railway — deployment không còn tồn tại, **không** phải app đang sleep hay sai đường dẫn.

Hệ quả: server vẫn "connect" được (supergateway khởi động bình thường) nhưng **tool list rỗng** — `ToolSearch` không tìm thấy `mcp__cds-kb__*` nào. Đừng suy ra là cấu hình sai.

Cách tra CDS view released khi thiếu `cds-kb`:

- `mcp__sap-docs__sap_search_objects` với `object_type="DDLS"`, `clean_core_level="A"` — tra được release state.
- `mcp__sap-docs__search` cho tài liệu, `sap_accelerator_hub_search` cho API.
- `SAP(action="search", target="I_*")` trên hệ thống thật — thấy đúng cái tenant GM2 có.

Muốn dùng lại `cds-kb` thì phải redeploy [cds-kb-mcp](https://github.com/dovoanhtruong/cds-kb-mcp) và sửa URL trong `.mcp.json`.

---

## 2. Tra cứu: tool `SAP` của `sap_cloud_dev`

Cú pháp: `SAP(action=..., target="TYPE NAME", params={...})`.

### 2.1 `action="read"` — loại object hỗ trợ

Danh sách này do chính tool trả về khi gọi sai:

```
CLAS, PROG, INTF, FUNC, FUGR, INCL, DDLS, BDEF, SRVD,
TABL, TABL_CONTENTS, DEVC, MSAG, TRAN, TYPE_INFO, STRUCT, CDS_DEPS
```

**KHÔNG hỗ trợ** — đã gặp lỗi thật, phải đi bằng curl + ADT:

| Loại | Việc cần | Đường thay thế |
|---|---|---|
| `DDLX` | metadata extension (UI annotation) | `GET /sap/bc/adt/ddic/ddlx/sources/<name>/source/main` |
| `DCLS` | access control (DCL) | `GET /sap/bc/adt/acm/dcl/sources/<name>/source/main` |
| `SRVB` | service binding (lấy URL của service) | mở trong ADT — nhanh hơn |
| `SCO1` | communication scenario | mở trong ADT |

`TYPE_INFO` từng trả **HTTP 406**; đọc data element phải curl với `Accept: application/vnd.sap.adt.dataelements.v2+xml`.

### 2.2 Đọc class lớn — đừng kéo cả file

```
SAP(action="read", target="CLAS ZBP_R_ZMFGKH01", params={"include": "implementations"})
SAP(action="read", target="CLAS CL_HTTP_DESTINATION_PROVIDER", params={"method": "CREATE_BY_COMM_ARRANGEMENT"})
```

`include` nhận `implementations`, `definitions`, `macros`, `testclasses`. Đọc cả class standard thường ra 50KB+; dùng `method` khi chỉ cần một chữ ký.

Sửa class lớn: **không** gửi lại full source — dùng CLONE + EDITSOURCE (memory `abap-edit-large-class-clone-editsource`).

**Class rất lớn (>150 KB) sẽ overflow và spill ra file — dùng luôn cái đó.** `read CLAS ZCL_FA_ENITY_ZGL02_3` (255 KB / 5.297 dòng) trả lỗi *"exceeds maximum allowed tokens"* kèm đường dẫn `.claude/projects/<proj>/<session>/tool-results/mcp-sap_cloud_dev-SAP-<ts>.txt`. Đừng đọc lại tràn context — **phân tích bằng `awk`/`grep`/`sed` trên chính file đó**: đếm construct, dò SELECT-trong-LOOP, ghép cặp SORT ↔ BINARY SEARCH. Nhanh hơn và không tốn context.

Hai lưu ý khi làm việc trên file spill:

- File chứa **source + dependency context** của MCP. Với ZGL02, class thật là dòng **151–4580**; từ 4580 trở đi là định nghĩa các class/interface khác. Phải chặn `NR>=151 && NR<=4580` trong awk, không thì trích lẫn.
- Statement ABAP trải nhiều dòng: `READ TABLE x INTO y` ở dòng này, `BINARY SEARCH` ở dòng khác. Grep một dòng sẽ ra rỗng. Phải nhớ `READ TABLE` gần nhất phía trên rồi mới in khi gặp `BINARY SEARCH`.

### 2.3 `action="search"`

`target="Z*ZMFGKH01*"` hoặc `target="I_PRODUCTPLANT*"`. Trả cả object SAP standard, kèm `PackageName` — rất tiện để biết một view thuộc VDM nào.

Trả `null` = **không có object nào khớp** (đã dùng để chứng minh `Z_API_FWK*` không tồn tại trên hệ thống này).

### 2.4 `action="analyze"`

| `type` | Dùng để | Trạng thái |
|---|---|---|
| `syntax_check` | kiểm cú pháp mà **không** đụng object; cần `object_url` + `content` | đã dùng nhiều, đã calibrate — xem §3.2 |
| `inactive_objects` | bằng chứng duy nhất cho việc object đã active thật | đã dùng, xem §3.1 |
| `health` | ATC count + có test hay không, theo `package` hoặc object | ✅ **chạy được** (2026-08-19, ZGL02) |
| `references` | liệt kê component của object + **cây package** | ✅ chạy được |
| `impact` | ripple check | ⚠️ chạy nhưng **vô dụng** — xem dưới |
| `callers`, `callees`, `call_graph`, `object_structure` | where-used | ❌ **403** — xem dưới |
| `cds_impact` | — | ❌ **type này KHÔNG tồn tại** |

Ba điều đã calibrate ngày 2026-08-19, khi review ZGL02:

- **`cds_impact` là tên sai.** Bảng cũ của sổ tay này ghi nó — gọi thì trả `No handler found for action="analyze"` (thông báo gây nhầm, tưởng cả action sai). Lấy danh sách type thật bằng `SAP(action="help", target="analyze")`.
- **Cả họ `/sap/bc/adt/cai/*` bị 403** với user này: `callers`/`callees`/`call_graph` → `/sap/bc/adt/cai/callgraph`, `object_structure` → `/sap/bc/adt/cai/objectexplorer/objects`. Đây là giới hạn quyền, không phải lỗi cú pháp. **Gate 3 (ripple/where-used) của [Skill: activation-guard] không dùng được đường này** — phải where-used trong Eclipse.
- **`impact` trả `entries: null` kể cả với object đang được dùng thật.** Đã test đối chứng: `ZCL_FA_ENITY_ZGL02_3` (custom entity trỏ trực tiếp vào, chắc chắn đang dùng) cũng trả `null` y như class nghi là code chết. → **`null` KHÔNG có nghĩa "không ai dùng"**, nó có nghĩa "tool không biết". Luôn test đối chứng trên một object chắc chắn đang dùng trước khi kết luận gì từ `impact`.
- `health` chạy được nhưng phần `boundaries` có `scanned_objects: 0` → kết quả `CLEAN` ở đó **vô nghĩa**, đừng đọc là "không có vi phạm".

### 2.5 Action có trong danh sách nhưng không chạy

`action="grep"` được tool liệt kê trong "Valid actions" nhưng gọi thì trả **`No handler found`**. Muốn grep source thì kéo source về rồi grep tại chỗ.

### 2.6 Tạo/sửa DDIC table

Chuỗi bắt buộc (memory `ddic-table-create-edit-via-mcp`):

1. `create` với `params.fields` là **JSON array** — truyền `source` bị từ chối
2. `edit target="TABL ..."` **không có handler** → phải `LOCK` → `UPDATE_SOURCE` → `ACTIVATE`
3. `ACTIVATE` **nhả lock** → tái dùng lock handle sẽ ra HTTP 423
4. `CLONE` không hỗ trợ TABL
5. Tham chiếu đơn vị trong `define table` phải **đủ tên bảng**: `'ztb_x.unit'`, viết `'unit'` sẽ bị hiểu thành tên bảng

---

## 3. Ba cái bẫy đã calibrate

Cả ba đều là loại "tool báo thành công nhưng thực tế không phải".

### 3.1 `ACTIVATE` trả `success:true` khi object vẫn inactive

`SAP(action="edit", target="ACTIVATE")` trả `{"success": true, "messages": []}` cho cả object **không** activate được.

- Bằng chứng duy nhất về trạng thái: `analyze` + `inactive_objects` — object vừa đụng **không được** xuất hiện trong danh sách.
- Muốn biết **lý do** thì `syntax_check` (bắt buộc có `content`), nó mới đưa message thật.
- Đã bắt được ca thật: table `ZTB_ZMFGKH01_A` báo activate thành công nhưng vẫn inactive; nguyên nhân là annotation unit thiếu tên bảng.

### 3.2 `syntax_check` **chỉ** báo error, **không** báo warning

Calibrate hai chiều ngày 2026-08-13:

| Input | Kết quả |
|---|---|
| ABAP sai cú pháp (`THIS IS NOT ABAP AT ALL ###`) | 4 finding, tất cả `severity: "E"` → tool **có** báo |
| Warning chắc chắn có: gán `'ABCDEFGHIJ'` vào `DATA lv TYPE c LENGTH 3` | **`null`** → warning **không** được trả về |

⇒ Kết quả `null` chỉ chứng minh **không có error**. Không được nói "sạch". Đã có ca thật: user gặp warning `Non-canonical structure of element nam…` trong đoạn code tool này đã "pass".

Mẹo dùng: `object_url` chỉ cần là **một object cùng loại đang tồn tại** — check nội dung class console vào URL của một class Z bất kỳ vẫn chạy và **không** thay đổi gì trên hệ thống. Nhớ đặt tên class trong `content` khớp URL.

### 3.3 `action="query"` trả 0 dòng một cách im lặng

User `CB9980000022` **không có quyền đọc business data** (`S_ABPLNGVS`). Mọi view, kể cả `I_CompanyCode`, trả `"Rows": []`.

⇒ **Kết quả rỗng không bao giờ là bằng chứng.** Đã chặn việc chốt câu hỏi Q3 của ZPM01_EX và mọi test end-to-end phụ thuộc dữ liệu.

Đọc master data **trong code ABAP** thì khác: dùng `WITH PRIVILEGED ACCESS` để không phụ thuộc quyền người dùng cuối (tiền lệ đang active: `ZBP_R_TBUPLOAD_ZMA01`).

---

## 4. Nhật ký theo từng báo cáo

### ZMFGKH01 — Tạo lệnh sản xuất từ Excel · package `ZMFGKH01`
**2026-08-11 → 2026-08-13 · [INDEX](../system_analysis/ZMFGKH01/INDEX.md) · [diagram](../walkthroughs/ZMFGKH01/upload-flow.html)**

Làm qua MCP:

| Việc | Cách |
|---|---|
| Tạo table `ZTB_ZMFGKH01_A` (package `ZANLTK2`) | `create` + `fields` JSON → `LOCK`/`UPDATE_SOURCE`/`ACTIVATE` → 3 gate `activation-guard` |
| Đọc BDEF `ZC_ZMFGKH01`, `ZR_ZMFGKH01` | `read BDEF` — xác nhận `use create;` đã mở và **active** |
| Đọc DDLS `ZC_ZMFGKH01`, `ZR_ZMFGKH01`, `ZTB_ZMFGKH01` | `read DDLS` / `read TABL` — đối chiếu 11 field payload |
| Đọc DCL của cả 2 view | **curl** (MCP không hỗ trợ DCLS) → `grant select … where TRUE` |
| Tìm class Excel sẵn có | `search Z*EXCEL*`, `Z*UPLOAD*` → tìm ra `ZBP_R_TBUPLOAD_ZMA01` đang dùng XCO xlsx → **dùng lại pattern đó** thay vì tự viết parser |
| Xác minh 5 view master data cho 9 check | `search` + curl đọc source, grep tên element |
| Xác minh `I_ProductionOrderTP` / `R_ProductionOrderTP` / `A_ProductionOrder_4` | `read BDEF` → phát hiện `late numbering` và 2 contract khác nhau |
| Xác minh bgPF, APJ, HTTP client, XCO JSON | `read CLAS/INTF` từng interface trước khi viết code |
| Kiểm mọi đoạn ABAP trước khi giao | `analyze syntax_check` — nhiều lượt |

Không CUD gì trong package `ZMFGKH01` — toàn bộ ABAP được **gen ra cho user tự dán**, vì package transportable cần TR.

Ngoài MCP: deploy UI5, đọc BSP qua ADT filestore để chẩn đoán deploy 400.

### ZPM01_EX — Sổ chi tiết công nợ phải trả NCC, NV · package `ZPM01_EX`
**2026-07-28 · [INDEX](../system_analysis/ZPM01_EX/INDEX.md)**

- `/sap-dev-code-analysis` toàn package → `analysis_report.md` (38KB), 20 defect `R-01`…`R-20`
- Áp FS V1.1 → tạo `ZCL_ZI_FA_ZPM01_EX_V11` trong **`ZANLTK2`** (local, khỏi TR), ACTIVE, ATC 31 finding / 0 error / 0 warning → `changelog_FS_V1.1.md`
- Production class **chưa đụng**; custom entity vẫn trỏ class cũ ⇒ app đang chạy chưa đổi hành vi
- Bị chặn bởi §3.3: không kiểm chứng được `9999999998` là G/L account hay Supplier

### ZRM01 + ZRM01_EX — Sổ chi tiết công nợ phải thu khách hàng
**2026-07-30 · [INDEX ZRM01](../system_analysis/ZRM01/INDEX.md) · [INDEX ZRM01_EX](../system_analysis/ZRM01_EX/INDEX.md)**

- Code review **read-only** toàn 2 package: 8 object có source + 2 UI5 app + metadata service binding. **Không CUD gì.**
- Kết luận rủi ro CAO: 7 finding Cao / 10 Trung bình / 7 Thấp
- **Toàn bộ đọc qua `curl` + ADT REST, không qua MCP** — vì MCP còn giữ cookie cũ sau khi refresh (đúng ca §1)

### ZMFGLSX — Review tầng authorization · package `ZMFGLSX`

**2026-08-18 · [INDEX](../system_analysis/ZMFGLSX/INDEX.md)**

- Review **read-only** tầng phân quyền. **Không CUD gì**, không tạo TR.
- Đọc qua **MCP**: 3 view (`DDLS ZMFG_I/R/C_ZMFGLSX`), `BDEF ZMFG_R_ZMFGLSX`, `DEVC ZMFGLSX`, `analyze inactive_objects`, `search ZMFG*`.
- Đọc qua **curl + ADT** (MCP không hỗ trợ, đúng §2.1): 2 `DCLS`, `SIA6 ZIAM_ZMFGLSX_EXT`, `SIA1 ZBC_ZMFGLSX`, `SUSH`, package attributes, behavior pool include `implementations`.
- Kết luận: DCL **có, active, code đúng template SAP — nhưng không chạy** vì cả 3 view khai `#NOT_REQUIRED`. IAM app khai `auths` rỗng. `get_global_authorizations` thân rỗng → CUD không chặn.
- Bẫy đáng ghi: field `CompanyCode` thực ra chứa `head.ProductionPlant` → map vào `C_ARPL_WRK/WERKS` là **đúng nội dung**, đừng "sửa" nó.

Hai endpoint ADT mới dùng lần đầu, đáng ghi lại:

| Việc | Endpoint |
|---|---|
| Tra auth object / bất kỳ type không có trong MCP | `/sap/bc/adt/repository/informationsystem/search?operation=quickSearch&query=Z*&objectType=SUSO` |
| Biết type nào **tạo được** trên tenant | `/sap/bc/adt/repository/informationsystem/objecttypes?operation=createableTypes` — trả về theo **group** (`APSIAM`, `APSCLOUDIAM`), member type nằm trong phần description của group, không phải `namedItem` riêng |

### ZGL02 — Code review Bảng cân đối số phát sinh · package `ZGL02`

**2026-08-19 · [INDEX](../system_analysis/ZGL02/INDEX.md)**

- Code review **read-only**. **Không CUD gì**, không tạo TR.
- Đọc qua **MCP**: `DEVC ZGL02`, 3 `DDLS` (`ZFA_R_ZGL02` custom entity, `ZI_GLACC_CL_ZGL02`, `ZFA_I_DISPLAY_SUBTOTAL`), `SRVD ZFA_UI_ZGL02`, `TABL ZTB_ZGL02_PDF`, `CLAS ZCL_FA_ENITY_ZGL02_3`, `analyze health/references/impact`.
- **Không đọc được**: `DDLX ZFA_R_ZGL02`, `SIA1 ZBC_ZGL02`, `SIA6 ZIAM_ZGL02_EXT` — MCP không hỗ trợ 3 loại này, mà curl thì cookie **hết hạn giữa session** (đúng ca §1: MCP còn sống, curl đã chết).
- Kiến trúc: **Custom Entity + RAP Query Provider**, không BDEF, không DCLS. Cây package đúng Rule 5: `ZCUSTOM_DEVELOPMENT → ZFPT → ZFPT_REPORT → ZFI_FA → ZGL02`.
- Kết quả: **4 finding CAO**, 10 TB, 6 THẤP. ATC 212 info / 0 error / 0 warning. **0 unit test.**

Hai bẫy kỹ thuật đáng nhớ, cả hai đều **sai âm thầm**:

| Bẫy | Cách phát hiện |
|---|---|
| `BINARY SEARCH` sai key: bảng nạp `ORDER BY accountgroup, supplier, glaccount, currency` nhưng đọc `WITH KEY supplier, currency, reversalreferencedocument` → thiếu field dẫn đầu, và có field không nằm trong ORDER BY | Ghép cặp **từng bảng**: nơi nạp (`SORT` **hoặc** `ORDER BY … INTO TABLE`) ↔ key của `READ TABLE`. `ORDER BY` thay được `SORT` nên đừng vội kết luận chỉ vì thiếu câu `SORT` |
| `DELETE <bảng> INDEX sy-tabix` **trên chính bảng đang `LOOP AT`** → index dịch, dòng kế tiếp bị bỏ qua | Xem `LOOP AT x` rồi tìm `DELETE x INDEX` trong thân loop |

Và một bẫy về RAP query provider: `get_paging( )->get_page_size( )`/`get_offset( )` **được gọi** nhưng biến `top`/`skip` không dùng ở đâu. Vì option đã được `get_`, framework **không** báo *"Query not fully covered"* — service cứ trả full result set. Muốn kiểm thì grep xem biến nhận giá trị đó có được dùng lại hay không, đừng chỉ grep tên API.

### ZGL02 — Flow dữ liệu · package `ZGL02`

**2026-08-19 · [INDEX](../system_analysis/ZGL02/INDEX.md) · [data_flow.md](../system_analysis/ZGL02/data_flow.md)**

- Phân tích flow **read-only**, tiếp sau lần code review cùng ngày. Không CUD gì.
- Đọc thêm: 3 view khung TK, khối kết chuyển, 3 LOOP lắp dòng, đường XML→ADS, signature 2 sub-method. Tất cả bằng `awk`/`sed` trên file spill (xem §2.2).

**Kiến trúc thật — và đây là lý do phải làm flow chứ không dừng ở code review:**

```
1 GET → lt_header (ĐÚNG 1 dòng) → attachment (PDF) + attachment_exc (Excel)
```

`lt_data` (chi tiết + subtotal + tổng cộng) **không bao giờ ra khỏi method**. Nó chỉ nhúng vào Excel qua `item = lt_data` và vào `lv_xml` cho ADS. Entity khai **37 field**, dòng trả về điền **10**.

**Hệ quả: 3 finding của lần review phải hạ mức.** F-03 (paging), F-06 (sort), F-07 (requested_fields) đều dựa trên giả định entity trả nhiều dòng. Kết quả có 1 dòng nên cả ba vô hại — chỉ còn là 3 biến đọc ra không dùng. Đã sửa trong `code_review.md` §3.1.

Bài học rút ra cho lần sau: **soi chất lượng trước khi biết flow thì dễ chấm sai mức độ.** Một `set_data( lt_x )` mà không biết `lt_x` có bao nhiêu dòng thì mọi kết luận về paging/sort đều là suy đoán.

Hai chỗ đáng ghi về cách dữ liệu chạy:

| Chỗ | Điều đáng nhớ |
|---|---|
| Số TK **331/131/141** | **Không** lấy từ GL line item. Ở LOOP 3 cả 6 field số bị **ghi đè** từ `lt_zpm02_da_331[ 1 ]` / `lt_zrm02_da_131[ 1 ]` / `lt_zrm02_da_141[ 1 ]` (L1246-1271) — tức từ logic sổ công nợ. Nên bug F-01/F-02 trong 2 sub-method ảnh hưởng trực tiếp lên bảng cân đối |
| Rẽ nhánh A/B/C/D | Không phải 4 nhánh khác nhau về nghiệp vụ. Là 2×2 (`INCL_WA` rỗng/có × `lt_check` rỗng/có), và **B chỉ là A bỏ mệnh đề `accountingdocument NOT IN`**, D cũng vậy với C |

Và một cái bẫy đọc code: `CASE lv_display_subtotal` ở dòng **288 bị comment**, dễ kết luận filter `DISPLAY_SUBTOTAL` là field chết. Nhưng có `CASE` thứ hai ở dòng **1306** dùng nó lọc `lt_data` thật. Tìm hết mọi chỗ dùng một biến trước khi gọi nó là chết.

### Bảo trì kết nối — 2026-09-03

- Đổi tên workspace `ABAP_CLOUD_AI\ABAP_CLOUD_AI` → `MCP_PhuTAI_GO_DEV`; session `/resume` cũ đã migrate (xem `workspace-maintenance.md`).
- Cookie hết hạn từ 2026-08-24. Refresh thành công bằng lệnh ở §1 (Chrome, 5m) — `Extracted 2 cookies` ngay lần đầu.
- `.mcp.json` đổi `SAP_COOKIE` → **`SAP_COOKIE_FILE`** (trỏ `tools/vsp/cookies.txt`). Đúng hơn bản cũ: `SAP_COOKIE` **không** tồn tại trong binary vsp — chỉ có `SAP_COOKIE_FILE` và `SAP_COOKIE_STRING` (kiểm bằng `grep -ao 'SAP_[A-Z_]*' vsp.exe | sort -u`).
- Xác nhận lại thứ tự đúng: **refresh cookie → kiểm bằng curl → rồi mới restart**. Restart trước đó 2 lần đều vô nghĩa.
- `cds-kb` vẫn 404 (§1.2). `sap-docs` + `sap-docs-upstream` bình thường.

### Chưa làm gì trên hệ thống

| Target | Trạng thái thật |
|---|---|
| `ZPM03` | FS đã đọc (docx), plan gap-analysis đã viết rồi **bỏ**, chưa đụng object nào |
| `ZPM01` | chỉ có file FS trong `FS/ZPM01/` |
| `ZPM01_TEST` | thử convert FS bằng markitdown, không phải việc trên hệ thống |

---

## 5. Đọc tài liệu ngoài hệ thống

| Việc | Cách |
|---|---|
| Tài liệu SAP Help / SAPUI5 | MCP `sap-docs` → `search` rồi `fetch` theo `id`. Query **bằng tiếng Anh**, corpus là tiếng Anh |
| Source runtime UI5 (sap.fe, sap.m) | `WebFetch` `https://ui5.sap.com/<version>/resources/<path>-dbg.js` — đã dùng để đọc `FPMHelper` và chốt cách FE resolve chuỗi `press` |
| ABAP Keyword Documentation | **không đọc được** bằng WebFetch — trang là SPA, chỉ trả về header |
| File FS `.doc` (OLE2, Word 97) | `antiword -m UTF-8.txt <file>` — có sẵn ở `/mingw64/bin/antiword`. Máy này **không** có LibreOffice / pandoc / catdoc |
| File `.docx` / `.xlsx` | python `zipfile` + `ElementTree` đọc trực tiếp; `scripts/office_to_md.py` mà skill nhắc tới **không tồn tại** |

Hai bẫy môi trường:

- Python phải chạy `python -X utf8` — đường dẫn workspace có `dự án`, stdout cp1252 của Windows Python sẽ dump.
- `/tmp` **không dùng chung** giữa công cụ mingw (`curl`, `grep`, `antiword`) và Python bản Windows. Hoặc giữ cả pipeline trong công cụ mingw, hoặc ghi vào scratchpad dir.

---

## 6. Quy ước ghi tiếp

Khi làm một báo cáo mới, thêm một khối vào §4 theo đúng khuôn:

```
### <TARGET> — <tên báo cáo> · package `<PKG>`
**<ngày> · [INDEX](../system_analysis/<TARGET>/INDEX.md)**

- object nào đã đọc, đã tạo, đã sửa — và bằng action MCP nào
- có CUD gì lên hệ thống không; nếu có thì TR nào
- cái gì bị chặn, vì sao
```

Hai nguyên tắc để sổ tay này còn đáng tin:

1. **Chỉ ghi việc đã làm thật.** "Đã đọc BDEF" khác "đã đọc source class". Ghi đúng cái đã chạy.
2. **Kết quả rỗng / thành công của tool phải kèm cách kiểm.** Xem §3 — cả ba bẫy đều là tool nói thành công.

---

## 7. Đọc metadata object (`changedAt` / `changedBy`) — MCP không làm được

**Bài học 2026-09-14, điều tra `ZC_EINVOICE_HEAD`.**

MCP `SAP(action="read")` chỉ trả **source text**, bóc mất toàn bộ `adtcore:*`. Muốn biết
object bị sửa/tạo lúc nào, ai sửa → **GET thẳng object URI bằng curl, BỎ `/source/main`**:

```bash
U=https://my437569.s4hana.cloud.sap
curl -s -b tools/vsp/cookies.txt "$U/sap/bc/adt/bo/behaviordefinitions/<n>?sap-client=080" \
  | tr '>' '>\n' | grep -oE 'adtcore:(createdAt|changedAt|changedBy)="[^"]*"'
```

URI theo loại: `ddic/ddl/sources/<n>` (DDLS) · `ddic/ddlx/sources/<n>` (DDLX) ·
`acm/dcl/sources/<n>` (DCLS) · `ddic/srvd/sources/<n>` (SRVD) ·
`businessservices/bindings/<n>` (SRVB) · `bo/behaviordefinitions/<n>` (BDEF) ·
`packages/<n>` (DEVC — XML còn cho biết **superpackage**).

Mấy đường **bị chặn**, đừng mất thời gian: `system list_transports` và `get_transport_info`
→ `blocked by safety configuration`; `analyze object_structure` → `403`;
`system INFO` → `No authorization to view data`.

### `createdAt` nhảy = object bị xóa rồi tạo lại

Dấu vết quyết định của vụ này: 7 BDEF có `createdAt` nhảy từ `2026-06-01` (đối chiếu bản
cache local Eclipse) sang `2026-08-14`, `changedAt` dồn trong **55 giây**. Đó là chữ ký của
một thao tác hàng loạt, không phải sửa tay.

### Object xóa hẳn thì KHÔNG còn metadata

GET object URI → 404, kể cả `?version=inactive` và `/objectstructure`;
`objectproperties/values` → `ExceptionUnprocessableEntity`. Còn tên trong `search` chỉ là
**TADIR shell** — dấu hiệu: `Description` rỗng + **không có entry `STOB/DO`** đi kèm.

### Luôn xem cả cây package trước khi kết luận "mất"

Sai lầm đắt nhất hôm đó: kết luận "toàn bộ app mất, phải phục hồi từ PRD" khi mới chỉ nhìn
**một** package. Thực tế app đã được refactor sang `ZFPT_EINV` với tên mới
(`ZC_EINVOICE_HEAD` → `ZC_EINV_HDR`), package cũ bị bỏ có chủ đích.

Đọc superpackage từ XML của `packages/<n>`, rồi liệt kê từng package con:

```bash
TOK=$(curl -s -D - -o /dev/null -b tools/vsp/cookies.txt -H "X-CSRF-Token: Fetch" \
      "$U/sap/bc/adt/discovery?sap-client=080" | tr -d '\r' \
      | awk 'tolower($1)=="x-csrf-token:"{print $2}')
curl -s -b tools/vsp/cookies.txt -H "X-CSRF-Token: $TOK" -X POST --data-binary "" \
  "$U/sap/bc/adt/repository/nodestructure?parent_type=DEVC/K&parent_name=<PKG>&withShortDescriptions=true&sap-client=080"
```

**Trước khi nói một object "bị mất", phải tìm object kế nhiệm ở package anh em.**

### Cookie chết ≠ MCP chết

`cookies.txt` trên đĩa hết hạn (curl trả `text/html` thay vì `atomsvc+xml`) trong khi MCP
vẫn chạy tốt — vsp giữ session riêng trong RAM. Refresh bằng `--browser-auth` thì curl dùng
được ngay, **không cần** restart MCP. Xem memory `sap-cloud-dev-connection`.

---

## 8. Syntax check bản gốc TRƯỚC khi đề xuất sửa

**Bài học 2026-09-14, `ZR_ZMFGKH01_N_H` (ZMFGKH01_N).**

`analyze syntax_check` nhận `content` inline — **không cần lock, không ghi gì lên hệ thống**, nên
dùng được cả trong plan mode và trước khi bàn giao code:

```
SAP(action="analyze", params={"type":"syntax_check",
    "object_url":"/sap/bc/adt/ddic/ddl/sources/<n>", "content":"<toàn bộ source>"})
```

**Luôn chạy 2 lần: bản gốc và bản sửa**, rồi so số warning. Đó là cách rẻ nhất làm Gate 1 chặt:
chứng minh được warning nào có sẵn, warning nào do mình gây ra. Lần này bản gốc trả

```
line 32  W  "CASE" expression without "ELSE" branch can produce "NULL values
```

— chính SAP chỉ ra bug, không cần đoán. Warning access control (`#CHECK` mà không có DCL) có ở
cả hai bản ⇒ không phải do sửa.

Lưu ý `syntax_check` chỉ chắc chắn về **error**; xem [[syntax-check-reports-errors-not-warnings]].
Ở đây nó có trả warning, nhưng đừng coi "không có warning" là bằng chứng sạch.

### CDS: path expression KHÔNG được đứng ở vế kết quả của CASE

```
Expression type ATOMIC_VIA_PATH not allowed in expression context CASE_EXP_SIMPLE of case
```

`case when _success.count_success is null then 0 else _success.count_success end` → **lỗi**.
`coalesce( _success.count_success, 0 )` → chết cùng lý do.

Cách vòng: để path expression làm **element độc lập**, rồi tham chiếu qua `$projection.<alias>`
trong CASE — lúc đó không còn là path expression nữa, `IS NULL` dùng được bình thường.

```abap
_success.count_success as SuccessRows,
case when $projection.SuccessRows is null then 'R' ... end as Status,
```

### Association trỏ tới view có GROUP BY thì cardinality là [0..1], không phải [1..1]

`ZI_SUCCESS_ROW_ZMGFGKH01` lọc `where ExecStatusCrit = 3` rồi `group by` ⇒ header chưa execute
thì **không có dòng** ⇒ `count_success` là **NULL, không phải 0**. Khai `[1..1]` là lời hứa sai.

Hệ quả trong CASE: `NULL = x` và `NULL <> x` đều cho *unknown* (false), và **`IS INITIAL` không
bắt NULL**. Nếu mọi nhánh đều false và CASE không có `ELSE` → kết quả NULL → cột hiển thị trống.
Đây đúng là triệu chứng "status không hiện gì".

### Thứ tự nhánh CASE: hẹp trước, rộng sau

Bug gốc: nhánh `when SuccessRows <> TotalRows then 'P'` đặt ở vị trí 2 nuốt hết mọi trường hợp
chưa execute, khiến `'R'` và `'E'` phía sau **không bao giờ tới lượt**. Lỗi logic thuần, không
cần data để chứng minh — nhưng cũng không có compiler nào báo. Khi đọc một CASE nhiều nhánh,
kiểm tra từng nhánh sau có thực sự **đạt tới được** không.
