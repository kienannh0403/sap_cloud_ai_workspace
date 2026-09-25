# AP

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `AP` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**88 view** · data category: (none) 76, Dimension 12 · loại: basic 60, text 14, dimension 12, value_help 2 · 3 view có field DEPRECATED/DECOMMISSIONED · 45 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| AP-MD-BP | 34 | top-level |
| AP-MD-BP-RAP | 54 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_BUSINESSPARTNER | Business Partner | AP-MD-BP | Dimension | 121 |
| I_BPCONTACTTOADDRESS | Business Partner Contact To Address | AP-MD-BP |  | 41 |
| I_BPCONTACTTOFUNCANDDEPT | Business Partner Contact To Function and Department | AP-MD-BP |  | 30 |
| I_BPADDRESSINDEPENDENTMOBILE | Root view for AddrIndMob | AP-MD-BP |  | 21 |
| I_BPADDRESSINDEPENDENTPHONE | Core view for address independent phone | AP-MD-BP |  | 21 |
| I_BPADDRESSINDEPENDENTEMAIL | Root View for Address Independent Email for BP app | AP-MD-BP |  | 18 |
| I_BPRELATIONSHIP_2 | Interface view for BUT050 | AP-MD-BP |  | 17 |
| I_BPADDRESSINDEPENDENTFAX | BP Address independent Fax | AP-MD-BP-RAP |  | 17 |
| I_BUSPARTADDRESS | Business Partner Address | AP-MD-BP | Dimension | 15 |
| I_BPADDRESSINDEPENDENTWEBSITE | BP Address independent Website | AP-MD-BP-RAP |  | 14 |
| I_BUPAIDENTIFICATION | Business Partner Identification | AP-MD-BP | Dimension | 12 |
| I_BPCONTACT | Business Partner Contact | AP-MD-BP |  | 11 |
| I_BPCURRENTDEFAULTADDRESS | Business Partner Current Default Address | AP-MD-BP |  | 11 |
| I_PAYMENTCARD | Core View for Payment Card | AP-MD-BP |  | 10 |
| I_PAYMENTCARDTYPE | Core View for table CCARD | AP-MD-BP |  | 10 |
| I_BUSINESSPARTNERTOBPROLE_2 | Business Partner assignment to BP Role | AP-MD-BP | Dimension | 9 |
| I_BPADDRDEPDNTINTLLOCNUMBER | Business Partner Address-Dependent ILN | AP-MD-BP |  | 8 |
| I_BPDATACONTROLLER | Business Partner Data Controller | AP-MD-BP |  | 8 |
| I_BUSINESSPARTNERADDRESSUSAGE | Busineess Partner Address Usage Core View | AP-MD-BP |  | 8 |
| I_BUSINESSPARTNERINDUSTRY | Core View for BUT0IS | AP-MD-BP | Dimension | 8 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Business Partner | 23 |
| MASTER | Address | 11 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| BC | 0 | 2 | 0 | Address, Business Partner |
| CA | 0 | 2 | 0 | Address, Business Partner |
| FI_other | 0 | 2 | 0 | Address, Business Partner |
| LO_other | 0 | 2 | 0 | Address, Business Partner |
| MM-PUR_Purchasing | 0 | 2 | 0 | Address, Business Partner |
| RE | 0 | 2 | 0 | Address, Business Partner |
| SD-BIL_Billing | 0 | 2 | 0 | Address, Business Partner |
| SD-SLS_Sales | 0 | 2 | 0 | Address, Business Partner |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
