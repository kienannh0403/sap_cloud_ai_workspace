# Naming convention — chép từ sheet của dự án

Nguồn: `artifacts/naming_convention/Naming_convention.xlsx` (Sheet1). Bản gốc là Google Sheet
`1ZmZhOR6gyAEIYUH45ZApxDapzDtNf5JaQ82wfZEBvGw`, tab "Naming convention". Anh gửi file ngày 2026-09-24.
Skill đang áp dụng: `.claude/skills/naming-convention/SKILL.md`.

| STT | Development Object | Prefix | Suffix | Sample | Note |
|---|---|---|---|---|---|
| 1 | Outbound Service | ZOB | REST | ZOB_EINVOICE_REST | |
| 2 | Communication Scenario | ZSCE | | ZSCE_EINVOICE | |
| 3 | Communication System | ZSYS | | ZSYS_EINVOICE | |
| 4 | Communication Arrangement | ZARR | | ZARR_EINVOICE | |
| 5 | Business Role | ZBR | | ZBR_EINVOICE | Role chứa nhiều BC, Space |
| 6 | Business Catalog | ZBC | | ZBC_EINVOICE | Tương ứng với mỗi app |
| 7 | IAM app (External app) | ZIAM | EXT | ZIAM_EINV_EXT | |
| 8 | Application Job Template | ZJOB_TPL | | ZJOB_TPL_EINV | |
| 9 | Application Job Catalog Entry | ZJOB | | ZJOB_EINV | |
| 10 | IAM app (Application Job Catalog Entry) | ZJOB | SAJC | ZJOB_EINV_SAJC | |
| 11 | Class implement job | ZCL_JOB | | ZCL_JOB_EINV | |
| 12 | Application Log object | ZJOB_LOG | | ZJOB_LOG_EINV | Object này dùng để ghi log khi chạy job (success, error) |
| 13 | Business Catalog for job | ZBC_JOB | | ZBC_JOB_EINV | |
| 14 | Business Role for job | ZBR_JOB | | ZBR_JOB_EINV | |
| 15 | Launchpad App | Z<tcode, tên chức năng> | UI5R | ZSD01_UI5R, ZBARCODE_UI5R | |
| 16 | Base CDS view entity (BO Root) | ZR | | ZR_SD_ZSD01; ZBP_R_SD_ZSD01 | Đặt tên module sau prefix entity. Nên để prefix là CDS entity thay vì module, vì khi create class tự động sẽ ra tên dễ đọc, search thuận tiện hơn. Mẫu: `<prefix>_<module>_<tcode>` |
| 17 | CDS view entity | ZI | | ZI_SD_ZSD01_ITEM | |
| 18 | Projection view | ZC | | ZC_SD_ZSD01_ITEM | |
| 19 | Metadata extension | | | ZC_SD_ZSD01_ITEM | Đặt tên giống CDS entity |
| 20 | Service Define | ZUI, ZAPI hoặc none | | ZUI_TRAVEL_O4 / ZAPI_TRAVEL_O4 / ZTRAVEL | Service define dùng chung cho nhiều service binding thì không cần prefix. Chỉ dùng cho UI thì ZUI, API thì ZAPI |
| 21 | Service Binding | ZUI, ZAPI | O2 / O4 ⚠️ | ZUI_TRAVEL_O2 / ZUI_TRAVEL_O4 / ZAPI_TRAVEL_O2 / ZAPI_TRAVEL_O4 ⚠️ | App nên dùng UI O4, vì O2 hạn chế annotation; SAP recommend O4 cho UI. API dùng O2 hay O4 tuỳ use case |
| 22 | Custom entity | ZCE | | ZCE_FA_ZGL01 | Mẫu: `Z<prefix>_<module>_<tcode>` |
| 23 | Form, template | <system_name> | | DEV_F_ZSD01 / TEST_F_ZSD01 / PRD_F_ZSD01 | Mẫu: `<prefix>_F_<tcode>` |

## ⚠️ Hai chỗ đã hiệu chỉnh so với file xlsx

1. **Dòng 21, cột Suffix:** trong xlsx ô này hiện là `2025-02-04`, do Excel tự đổi chuỗi kiểu "O2/O4" thành ngày.
   Anh xác nhận ngày 2026-09-24: hậu tố là **`_O2` / `_O4` (chữ O)**.
2. **Dòng 21, cột Sample:** xlsx ghi `ZAPI_TRAVEL_02 / ZAPI_TRAVEL_04` (số 0), đây là lỗi gõ.
   Đã sửa thành `ZAPI_TRAVEL_O2 / ZAPI_TRAVEL_O4`, cũng theo xác nhận của anh.

Các ô còn lại chép nguyên văn; chỉ sửa chính tả trong cột Note cho dễ đọc, không đổi nghĩa.
