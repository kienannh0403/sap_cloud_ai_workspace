---
name: naming-convention
description: Kiểm tra, đề xuất và tạo tên chuẩn cho các đối tượng ABAP (Dictionary, CDS, RAP), OData service, Communication (outbound service, scenario, system, arrangement), IAM (IAM app, business catalog, business role), Application Job, Launchpad app, Form và Package theo naming convention của dự án. Sử dụng khi người dùng yêu cầu tạo object mới, cấu trúc project hoặc review tên/mã nguồn.
---

# Naming Convention Skill

## Mục tiêu (Goal)
Đảm bảo mọi object (ABAP, CDS/RAP, service, communication, IAM, job, Fiori, form, package) được đặt tên đúng quy định của dự án. Khi đề xuất tên, luôn giải thích ngắn gọn vì sao dùng prefix/suffix đó.

## Nguồn & thứ tự ưu tiên
- **Nguồn chính:** sheet "Naming convention" của dự án (`artifacts/documents/naming_convention/Naming_convention.xlsx`, bản chép + hiệu chỉnh: `artifacts/documents/naming_convention/naming_convention_sheet.md`, nhận 2026-09-24). Các mục gắn *(sheet)* bên dưới lấy từ đây.
- Mục gắn *(chuẩn cũ)* là quy tắc mặc định có từ trước, **giữ lại vì sheet không nói tới** (bảng DB, domain/data element, class thường, package, Space/Page, giới hạn độ dài).
- **Ưu tiên:** tên TS/FS/user chỉ định tường minh > sheet > chuẩn cũ. Nếu TS/user đã chốt một tên/scheme khác (VD bảng `ZTB_*`/`ZTB_*_D`, hay suffix theo node `_H`/`_FG`/`_RM`) thì tên đó THẮNG — không "sửa lại" cho khớp skill này; chỉ dùng mặc định khi tên chưa được chỉ định.

## Mẫu tên chung cho CDS/RAP *(sheet)*
`Z<prefix>_<module>_<tcode>[_<node>]` — **prefix loại entity đứng trước module**, rồi tới tcode/tên chức năng, cuối cùng là node (nếu có).
Lý do (sheet): khi ADT tự sinh class (behavior pool…) tên sẽ dễ đọc và dễ search hơn so với để module đứng đầu.
VD: `ZR_SD_ZSD01`, `ZI_SD_ZSD01_ITEM`, `ZC_SD_ZSD01_ITEM`, `ZCE_FA_ZGL01`.

## Quy tắc

### 1. ABAP Dictionary & class *(chuẩn cũ)*
- **Database table:** dữ liệu thật (persistent) `ZA_`, bảng draft `ZD_` (VD `ZA_Invoice`, `ZD_Invoice`).
- **Class / Interface / Exception:** `ZCL_`, `ZIF_`, `ZCX_`.
- **Khác:** Domain `ZDO_`, Data Element `ZDE_`, Table Type `ZTT_`, Structure `ZST_`, Number Range `ZNR_`, Message Class `ZMC_`.

### 2. CDS & RAP *(sheet)*
| Object | Prefix | Mẫu | Ví dụ |
|---|---|---|---|
| Base CDS view entity (BO root) / root BDEF | `ZR` | `ZR_<module>_<tcode>` | `ZR_SD_ZSD01` |
| CDS view entity (interface, node con) | `ZI` | `ZI_<module>_<tcode>[_<node>]` | `ZI_SD_ZSD01_ITEM` |
| Projection view / projection BDEF | `ZC` | `ZC_<module>_<tcode>[_<node>]` | `ZC_SD_ZSD01_ITEM` |
| Metadata extension | — | **giống hệt tên CDS entity** nó chú thích | `ZC_SD_ZSD01_ITEM` |
| Custom entity | `ZCE` | `ZCE_<module>_<tcode>` | `ZCE_FA_ZGL01` |
| Behavior pool | `ZBP_` | `ZBP_` + tên root **bỏ chữ Z đầu** | `ZBP_R_SD_ZSD01` |

Handler / saver class (local, trong behavior pool) *(chuẩn cũ)*: `LHC_<entity>`, `LSC_<entity>`.

### 3. Business Service (OData) *(sheet)*
- **Service Definition:** `ZUI_` nếu chỉ dùng cho UI, `ZAPI_` nếu chỉ dùng cho API; **không prefix** nếu dùng chung cho nhiều service binding (VD `ZTRAVEL`).
- **Service Binding:** `ZUI_` / `ZAPI_` + hậu tố **`_O2`** (OData V2) hoặc **`_O4`** (OData V4) — chữ **O**, không phải số 0.
  VD `ZUI_TRAVEL_O4`, `ZUI_TRAVEL_O2`, `ZAPI_TRAVEL_O4`, `ZAPI_TRAVEL_O2`.
- App Fiori mới: dùng **UI O4** (O2 hạn chế annotation; SAP khuyến nghị O4 cho UI). API: O2 hay O4 tuỳ use case.

### 4. Integration / Communication *(sheet)*
| Object | Mẫu | Ví dụ |
|---|---|---|
| Outbound Service | `ZOB_<tên>_REST` | `ZOB_EINVOICE_REST` |
| Communication Scenario | `ZSCE_<tên>` | `ZSCE_EINVOICE` |
| Communication System | `ZSYS_<tên>` | `ZSYS_EINVOICE` |
| Communication Arrangement | `ZARR_<tên>` | `ZARR_EINVOICE` |

### 5. IAM & Fiori *(sheet, trừ Space/Page)*
| Object | Mẫu | Ví dụ | Ghi chú |
|---|---|---|---|
| Business Role | `ZBR_<tên>` | `ZBR_EINVOICE` | Một role chứa nhiều business catalog, space |
| Business Catalog | `ZBC_<tên>` | `ZBC_EINVOICE` | Mỗi app một business catalog |
| IAM app (External app) | `ZIAM_<tên>_EXT` | `ZIAM_EINV_EXT` | ADT tự thêm `_EXT` khi chọn loại External app |
| Launchpad app | `Z<tcode hoặc tên chức năng>_UI5R` | `ZSD01_UI5R`, `ZBARCODE_UI5R` | |
| Space / Page *(chuẩn cũ)* | `ZSP_` / `ZPA_` | — | Sheet không quy định |

### 6. Application Job *(sheet)*
| Object | Mẫu | Ví dụ |
|---|---|---|
| Application Job Template | `ZJOB_TPL_<tên>` | `ZJOB_TPL_EINV` |
| Application Job Catalog Entry | `ZJOB_<tên>` | `ZJOB_EINV` |
| IAM app cho Job Catalog Entry | `ZJOB_<tên>_SAJC` | `ZJOB_EINV_SAJC` |
| Class implement job | `ZCL_JOB_<tên>` | `ZCL_JOB_EINV` |
| Application Log object (ghi log success/error khi chạy job) | `ZJOB_LOG_<tên>` | `ZJOB_LOG_EINV` |
| Business Catalog cho job | `ZBC_JOB_<tên>` | `ZBC_JOB_EINV` |
| Business Role cho job | `ZBR_JOB_<tên>` | `ZBR_JOB_EINV` |

### 7. Form / template *(sheet)*
| Loại | Mẫu | Ví dụ | Ghi chú |
|---|---|---|---|
| Form, template (form in / PDF) | `<SYSTEM>_F_<tcode>` | `DEV_F_ZSD01`, `TEST_F_ZSD01`, `PRD_F_ZSD01` | Tiền tố là tên hệ thống |
| Excel form | `<tcode>_EXC` (sheet: `Z<tcode, chức năng>_EXC`) | `ZSD01_EXC`, `ZMFGBOM_EXC` | Tên **Template** trong app "Upload Template file excel" (tool `ZCL_EXPORT_EXCEL_XLSX`). Tcode đã có `Z` thì không thêm `Z` nữa. Không theo hệ thống → dùng chung một tên cho DEV/TEST/PRD. Giới hạn 20 ký tự (`ZTB_UPLOAD_TMPL-TEMPLATE`); Report Name trong app = tcode, ≤ 10 ký tự |

### 8. Package hierarchy *(chuẩn cũ)*
- `ZFPT`: root package.
- `ZFPT_CORE`: core function.
- `ZFPT_INT`: integration (package con VD `ZEBANKING`, `ZINVOICE`).
- `ZFPT_EH`: enhancement (package con theo module VD `ZEH_FI`, `ZEH_SD`).
- `ZFPT_REPORT`: report & function (package con theo module VD `ZREPORT_FI`, `ZREPORT_SD`, `ZREPORT_HR`…).
- Package thử nghiệm / cá nhân nằm dưới `ZLOCAL` (miễn TR — xem `LOCAL_NO_TR_PACKAGES` trong `.claude/common/system-config.md`).

### 9. Giới hạn độ dài tên (kiểm TRƯỚC khi đề xuất tên) *(chuẩn cũ)*

Đếm ký tự **trước** khi đưa ra tên, không đợi activation fail rồi sửa. Prefix tính vào độ dài.

| Loại object | Giới hạn | Ghi chú |
|---|---|---|
| **Database table** (transparent — sinh ra physical DB object) | **≤ 16 ký tự** | Chật nhất. `ZA_` đã ăn 3 → chỉ còn 13 cho tên nghiệp vụ |
| DDIC Structure (TABCLASS `INTTAB` — không sinh physical table) | ≤ 30 ký tự | **KHÔNG** bị giới hạn 16 như table — dù cùng loại object `TABL` |
| Repository object nói chung (Class, Interface, CDS view, Data Element, Domain, Table Type, Service Definition/Binding, Behavior Pool...) | ≤ 30 ký tự | — |

Prefix và namespace **tính vào** giới hạn (`/1CN/CDPSAPDLV01` = đúng 16; `/1ISLM/CL_BEI_LATE_PAYMT_CLSTR` = đúng 30).

**Hệ quả:** cặp bảng `ZA_*` / `ZD_*` là chỗ dễ vỡ nhất. Ví dụ `ZA_ProductionOrder` = 18 ký tự → **vượt 16**. Tên nghiệp vụ dài phải viết tắt **ngay ở bước TS** (VD `ZA_ProdOrder` = 12), không để tới lúc tạo object mới phát hiện — đổi tên bảng sau đó kéo theo sửa cả cây CDS/BDEF/service đã build lên trên. Bảng draft `ZD_*` cùng độ dài prefix nên cùng ngân sách ký tự.

Mẫu `Z<prefix>_<module>_<tcode>_<node>` (mục 2) cũng phải đếm ký tự: node dài + tcode dài dễ vượt 30 (VD behavior pool thêm `ZBP_` vào trước tên root). Giới hạn riêng của object IAM / communication / application job / application log **chưa đo trên hệ thống** — *unverified*; nếu tên dài gần 30, thử tạo trên DEV và đọc lỗi thật trước khi chốt.

> **Nguồn giới hạn 16/30:** đo thực nghiệm trên hệ thống DEV (`my437569`, client 080) qua ADT repository search, ngày 2026-07-29 — không phải trích dẫn tài liệu SAP. Không tìm được trang SAP Help/ABAP Keyword Documentation nào phát biểu 2 con số này. Kết quả đo (gộp nhiều slice truy vấn, tên duy nhất): `TABL/DT` 6124 tên → dài nhất **16**, 1564 tên (26%) nằm đúng ở 16, **không có tên nào >16** · `TABL/DS` (structure) 4009 tên → dài nhất **30** · `CLAS/OC` 4211 tên → dài nhất **30** · `DDLS/DF` 4140 tên → dài nhất **30**. Cụm dồn đúng ở mốc là dấu hiệu giới hạn cứng. Đây là bằng chứng thực nghiệm mạnh nhưng vẫn là suy luận từ mẫu quan sát — nếu một tên đã chốt trong TS chỉ vượt mốc 1–2 ký tự, xác nhận bằng cách thử tạo trên DEV và đọc lỗi thật trước khi bắt user đổi tên.

## Thay đổi so với chuẩn cũ (2026-09-24)
| Mục | Trước | Nay (sheet) |
|---|---|---|
| CDS / RAP | theo tên nghiệp vụ: `ZR_Customer`, `ZI_Customer`, `ZC_Customer` | theo module + tcode: `ZR_SD_ZSD01`, `ZI_SD_ZSD01_ITEM`, `ZC_SD_ZSD01_ITEM` |
| Behavior pool | `ZBP_Customer` | `ZBP_R_SD_ZSD01` (= `ZBP_` + tên root bỏ `Z`) |
| Custom entity | `ZCE_Customer` | `ZCE_<module>_<tcode>` (`ZCE_FA_ZGL01`) |
| Service Definition | luôn có `ZUI_`/`ZAPI_` | được **bỏ prefix** khi dùng chung nhiều binding |
| Business Role | `BR_` | `ZBR_` |
| Mới | — | Communication (`ZOB_`, `ZSCE_`, `ZSYS_`, `ZARR_`), `ZBC_`, `ZIAM_…_EXT`, Launchpad `_UI5R`, Application Job (`ZJOB_*`, `ZCL_JOB_`, `ZBC_JOB_`, `ZBR_JOB_`), Form `<SYSTEM>_F_<tcode>`, Excel form `<tcode>_EXC` (2026-09-25) |

## Ví dụ (Examples)
- **User:** "Tôi muốn làm app ZSD01 (module SD) có bảng header/item, RAP model và Fiori app, kèm job chạy đêm."
- **AI Response:** Theo naming convention của dự án:
  1. Package: package con theo module dưới `ZFPT_REPORT` (VD `ZREPORT_SD`) — hoặc `ZLOCAL` nếu chỉ thử nghiệm.
  2. Table *(chuẩn cũ, ≤16 ký tự)*: `ZA_SD01_HEAD` / `ZD_SD01_HEAD`, `ZA_SD01_ITEM` / `ZD_SD01_ITEM`.
  3. Root CDS & BDEF: `ZR_SD_ZSD01`; node item: `ZI_SD_ZSD01_ITEM`.
  4. Projection CDS & BDEF: `ZC_SD_ZSD01`, `ZC_SD_ZSD01_ITEM`; metadata extension cùng tên.
  5. Behavior pool: `ZBP_R_SD_ZSD01`.
  6. Service Definition: `ZUI_SD_ZSD01` (chỉ dùng cho UI); Service Binding: `ZUI_SD_ZSD01_O4` (UI dùng O4).
  7. Launchpad app: `ZSD01_UI5R`; Business Catalog `ZBC_SD_ZSD01`; Business Role `ZBR_SD_ZSD01`.
  8. Job: template `ZJOB_TPL_SD01`, catalog entry `ZJOB_SD01`, IAM app `ZJOB_SD01_SAJC`, class `ZCL_JOB_SD01`, log object `ZJOB_LOG_SD01`, catalog/role `ZBC_JOB_SD01` / `ZBR_JOB_SD01`.
