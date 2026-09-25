# EHS

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `EHS` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**50 view** · data category: (none) 50 · loại: basic 47, text 3 · 0 view có field DEPRECATED/DECOMMISSIONED · 50 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| EHS-SUS-CI | 1 | top-level |
| EHS-SUS-DG | 10 | top-level |
| EHS-SUS-FND-PC | 34 | top-level |
| EHS-SUS-SDS | 5 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_CHMLCMPLNCIDFR | Chemical Compliance Identifier | EHS-SUS-FND-PC |  | 19 |
| I_ACTIVECOMPLIANCERQMTVERSION | Active Compliance Requirement Version | EHS-SUS-CI |  | 8 |
| I_COUNTRYTRANSPORTSTATUS | Country/Region Transport Status | EHS-SUS-DG |  | 2 |
| D_CALCTDANGEROUSGOODSPOINTSR | Calculate Dngrs Goods Points Result | EHS-SUS-DG |  | 0 |
| D_CALCTDNGRSGDSPTSCATEGORYR | Calculate Dngrs Gds Pts Category Result | EHS-SUS-DG |  | 0 |
| D_CALCTDNGRSGDSPTSITMRGLNR | Calculate Dngrs Gds Pts Itm Regulation R | EHS-SUS-DG |  | 0 |
| D_CALCTDNGRSGOODSPOINTSITEMR | Calculate Dngrs Goods Points Item R | EHS-SUS-DG |  | 0 |
| D_DAGDSCLFNCLCTDAGDSPTSPAINSNR | Calculate Dangerous Goods Points Packing Instruction R | EHS-SUS-DG |  | 0 |
| D_DNGRSGDSCLASSFCTNGETDESCSR | DG Classfctn Get Description Result | EHS-SUS-DG |  | 0 |
| D_PCLGSDCGETDAGDSDOCINFOGROUPR | Grouping Information R | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDAGDSDOCINFOITEMP | Get DG Document Info Items Parameter | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDAGDSDOCINFOITEMR | Item Description R | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDAGDSDOCINFOPOINTR | 1.1.3.6 information R | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDAGDSEDIINFOITEMP | Get PCLD DG EDI Items Parameter | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDAGDSEDIINFOITEMR | Item EDI R | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDNGRSGDSDOCINFOP | DG Document Info Parameter | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDNGRSGDSDOCINFOR | DG Document Info R | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDNGRSGOODSEDIINFOP | PCLD DG Get EDI Informtion Parameter | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETDNGRSGOODSEDIINFOR | DG Document EDI R | EHS-SUS-FND-PC |  | 0 |
| D_PCLGSDCGETEUADRFORPRODSPRODP | Row GetEUADRPTSFORPRODS P | EHS-SUS-FND-PC |  | 0 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
