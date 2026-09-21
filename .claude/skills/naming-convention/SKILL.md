---
name: naming-convention
description: Kiểm tra, đề xuất và tạo tên chuẩn cho các đối tượng ABAP (Dictionary, CDS, RAP), Fiori, Package và GitHub Repositories theo quy chuẩn của dự án FPT. Sử dụng khi người dùng yêu cầu tạo object mới, cấu trúc project hoặc review mã nguồn.
---

# FPT Project Naming Convention Skill

## Mục tiêu (Goal)
Đảm bảo tất cả các thành phần phần mềm (ABAP, Fiori, Packages, Git) được đặt tên tuân thủ tuyệt đối quy định của dự án. 

## Hướng dẫn (Instructions)
Khi người dùng yêu cầu tạo mới một đối tượng, hoặc nhờ kiểm tra tên của một đối tượng, hãy đối chiếu với bảng quy tắc bên dưới để đưa ra tên chính xác. Luôn giải thích ngắn gọn tại sao lại dùng Prefix/Suffix đó.

**Ưu tiên tên chỉ định tường minh (TS/user wins):** các quy tắc dưới đây là DEFAULT — nếu TS, FS, hoặc user đã chỉ định tường minh một tên/scheme khác (VD: bảng dùng `ZTB_*`/`ZTB_*_D` thay vì `ZA_`/`ZD_`, hay base name + suffix theo node `_H`/`_FG`/`_RM`), thì tên chỉ định đó THẮNG. Không "sửa lại" một tên đã được TS/user chốt cho khớp default của skill này; chỉ dùng default khi tên chưa được chỉ định.

### Quy tắc 1: ABAP Dictionary & Source Code (Eclipse Objects)
Tất cả các custom objects thường bắt đầu bằng `Z` cộng với Prefix.
* **Database Tables:** Dữ liệu thật (Persistent) dùng `ZA_` (VD: ZA_Customer). Dữ liệu nhạy (Draft) dùng `ZD_` (VD: ZD_Customer).
* **Class & Interface:** Global Class (`CL_`), Global Interface (`IF_`), Exception (`CX_`).
* **Các thành phần khác:** Domain (`DO_`), Data Element (`DE_`), Table Type (`TT_`), Structure (`ST_`), Number Range (`NR_`), Message Class (`MC_`).

### Quy tắc 2: Tầng CDS & RAP Model
* **Interface CDS Entity:** Prefix `I_` (VD: ZI_Customer)
* **Base CDS Entity / Root BDEF:** Prefix `R_` (VD: ZR_Customer)
* **Projection CDS / Projection BDEF:** Prefix `C_` (VD: ZC_Customer)
* **Custom Entity:** Prefix `CE_` (VD: ZCE_Customer)
* **Metadata Extension:** Tên giống hệt với CDS Entity liên quan (VD: ZC_Customer).
* **RAP Source Code:**
    * Behavior Pool: Prefix `BP_` (VD: ZBP_Customer)
    * Handler Class: Prefix `LHC_` (VD: ZLHC_Customer)
    * Saver Class: Prefix `LSC_` (VD: ZLSC_Customer)

### Quy tắc 3: Business Services (OData)
* **Service Definition:** Dành cho UI dùng `UI_` (VD: ZUI_Customer), dành cho API dùng `API_` (VD: ZAPI_Customer).
* **Service Binding:**
    * UI OData V2: Prefix `UI_`, Suffix `_O2` (VD: ZUI_Customer_O2)
    * UI OData V4: Prefix `UI_`, Suffix `_O4` (VD: ZUI_Customer_O4)
    * Web API V2: Prefix `API_`, Suffix `_O2` (VD: ZAPI_Customer_O2)
    * Web API V4: Prefix `API_`, Suffix `_O4` (VD: ZAPI_Customer_O4)

### Quy tắc 4: Fiori & IAM
* **Business Role:** Prefix `BR_`
* **Space:** Prefix `SP_`
* **Page:** Prefix `PA_`

### Quy tắc 5: Cấu trúc Package Hierarchy (ZFPT)
* `ZFPT`: Root Package.
* `ZFPT_CORE`: Core Function.
* `ZFPT_INT`: Integration (Package con VD: `ZEBANKING`, `ZINVOICE`).
* `ZFPT_EH`: Enhancement (Package con theo module VD: `ZEH_FI`, `ZEH_SD`).
* `ZFPT_REPORT`: Reports and Function (Package con theo module VD: `ZREPORT_FI`, `ZREPORT_SD`, `ZREPORT_HR`...).

### Quy tắc 6: Giới hạn độ dài tên (kiểm TRƯỚC khi đề xuất tên)

Đếm ký tự **trước** khi đưa ra tên, không đợi activation fail rồi sửa. Prefix tính vào độ dài.

| Loại object | Giới hạn | Ghi chú |
|---|---|---|
| **Database table** (transparent — sinh ra physical DB object) | **≤ 16 ký tự** | Chật nhất. `ZA_` đã ăn 3 → chỉ còn 13 cho tên nghiệp vụ |
| DDIC Structure (`ST_`, TABCLASS `INTTAB` — không sinh physical table) | ≤ 30 ký tự | **KHÔNG** bị giới hạn 16 như table — dù cùng loại object `TABL` |
| Repository object nói chung (Class, Interface, CDS view, Data Element, Domain, Table Type, Service Definition/Binding, Behavior Pool...) | ≤ 30 ký tự | — |

Prefix và namespace **tính vào** giới hạn (`/1CN/CDPSAPDLV01` = đúng 16; `/1ISLM/CL_BEI_LATE_PAYMT_CLSTR` = đúng 30).

**Hệ quả cho chuẩn FPT:** cặp bảng `ZA_*` / `ZD_*` là chỗ dễ vỡ nhất. Ví dụ `ZA_ProductionOrder` = 18 ký tự → **vượt 16**. Tên nghiệp vụ dài phải viết tắt **ngay ở bước TS** (VD `ZA_ProdOrder` = 12), không để tới lúc tạo object mới phát hiện — đổi tên bảng sau đó kéo theo sửa cả cây CDS/BDEF/service đã build lên trên. Lưu ý bảng draft `ZD_*` cùng độ dài prefix nên cùng ngân sách ký tự.

> **Nguồn:** đo thực nghiệm trên hệ thống DEV (`my437569`, client 080) qua ADT repository search, ngày 2026-07-29 — không phải trích dẫn tài liệu SAP. Không tìm được trang SAP Help/ABAP Keyword Documentation nào phát biểu 2 con số này. Kết quả đo (gộp nhiều slice truy vấn, tên duy nhất): `TABL/DT` 6124 tên → dài nhất **16**, 1564 tên (26%) nằm đúng ở 16, **không có tên nào >16** · `TABL/DS` (structure) 4009 tên → dài nhất **30** · `CLAS/OC` 4211 tên → dài nhất **30** · `DDLS/DF` 4140 tên → dài nhất **30**. Cụm dồn đúng ở mốc là dấu hiệu giới hạn cứng. Đây là bằng chứng thực nghiệm mạnh nhưng vẫn là suy luận từ mẫu quan sát — nếu một tên đã chốt trong TS chỉ vượt mốc 1–2 ký tự, xác nhận bằng cách thử tạo trên DEV và đọc lỗi thật trước khi bắt user đổi tên.

### Ví dụ (Examples)
- **User:** "Tôi muốn tạo một bảng chứa dữ liệu Hóa Đơn và một RAP model cho nó để làm Fiori app".
- **AI Response:** Dựa theo chuẩn dự án FPT, bạn cần tạo các object sau:
  1. Package: `ZFPT_REPORT` (hoặc `ZREPORT_FI` tùy ngữ cảnh).
  2. Table: `ZA_Invoice` (Persist), `ZD_Invoice` (Draft).
  3. Base CDS & BDEF: `ZR_Invoice`
  4. Projection CDS & BDEF: `ZC_Invoice`
  5. Metadata Extension: `ZC_Invoice`
  6. Behavior Pool: `ZBP_Invoice`
  7. Service Definition: `ZUI_Invoice`
  8. Service Binding: `ZUI_Invoice_O4` (Khuyên dùng V4 cho Fiori).
