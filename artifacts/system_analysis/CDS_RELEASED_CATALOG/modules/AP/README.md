# AP

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `AP` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**43 view** · data category: (none) 31, Dimension 12 · loại: basic 17, dimension 12, text 12, value_help 2 · 1 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| AP-MD-BP | 18 | top-level |
| AP-MD-BP-RAP | 25 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_BUSINESSPARTNER | Business Partner | AP-MD-BP | Dimension | 121 |
| I_BUSPARTADDRESS | Business Partner Address | AP-MD-BP | Dimension | 15 |
| I_BUPAIDENTIFICATION | Business Partner Identification | AP-MD-BP | Dimension | 12 |
| I_PAYMENTCARD | Core View for Payment Card | AP-MD-BP |  | 10 |
| I_PAYMENTCARDTYPE | Core View for table CCARD | AP-MD-BP |  | 10 |
| I_BUSINESSPARTNERTOBPROLE_2 | Business Partner assignment to BP Role | AP-MD-BP | Dimension | 9 |
| I_BUSINESSPARTNERINDUSTRY | Core View for BUT0IS | AP-MD-BP | Dimension | 8 |
| I_BUSINESSPARTNERTAXNUMBER | Core view for Tax Number | AP-MD-BP | Dimension | 7 |
| I_BUSINESSPARTNERTOBPROLE | Business Partner assignment to BP Role | AP-MD-BP | Dimension | 7 |
| I_CONTACTPERSONDEPARTMENTT | Department of Contact Person Textview | AP-MD-BP |  | 4 |
| I_CONTACTPERSONFUNCTIONT | Function of Contact Person Textview | AP-MD-BP |  | 4 |
| I_BUSINESSPARTNERPRINTFORMATT | Business Partner Category - Text | AP-MD-BP-RAP |  | 4 |
| I_BUSPARTINDUSTRYKEY | Business Partner Industry Key | AP-MD-BP-RAP | Dimension | 4 |
| I_BUSINESSPARTNERADDRESSTYPET | Business Partner Address Types Text | AP-MD-BP-RAP |  | 3 |
| I_BUSINESSPARTNERPRINTFORMAT | Business Partner Print Format | AP-MD-BP-RAP |  | 3 |
| I_BUSPARTCATEGORY | Business Partner Category | AP-MD-BP-RAP | Dimension | 3 |
| I_BUSINESSPARTNERSTANDARDUSAGE | Basic View for Business Partner Standard Usage | AP-MD-BP |  | 2 |
| I_CONTACTPERSONDEPARTMENT | Value Help for Dept of Contact Person | AP-MD-BP | Dimension | 2 |
| I_CONTACTPERSONFUNCTION | Value Help for Func of Contact Person | AP-MD-BP | Dimension | 2 |
| I_PAYMENTCARDLOCK | View for Payment Card Lock | AP-MD-BP |  | 2 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Business Partner | 9 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| BC | 0 | 1 | 0 | Business Partner |
| CA | 0 | 1 | 0 | Business Partner |
| FIN | 0 | 1 | 0 | Business Partner |
| FI_other | 0 | 1 | 0 | Business Partner |
| LO_other | 0 | 1 | 0 | Business Partner |
| MM-PUR_Purchasing | 0 | 1 | 0 | Business Partner |
| SCM | 0 | 1 | 0 | Business Partner |
| SD-SLS_Sales | 0 | 1 | 0 | Business Partner |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
