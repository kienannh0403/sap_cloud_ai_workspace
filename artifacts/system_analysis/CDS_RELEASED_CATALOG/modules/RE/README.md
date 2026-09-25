# RE

Generated 2026-09-25 by `build_catalog.py` from SAP's official release list (`sap_official/`, SAP update 2026-09-04) + descriptions read on tenant 080 + the user's xlsx. Do not hand-edit; re-run the script.

Nhóm còn lại của module `RE` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**172 view** · data category: (none) 153, Dimension 19 · loại: basic 102, text 51, dimension 19 · 0 view có field DEPRECATED/DECOMMISSIONED · 121 view mới so với file xlsx của user · 0 view chưa có trên tenant 080.

> Cột `n_fields`/`key_entities` chỉ có cho view nằm trong sheet Fields của xlsx; view mới = 0/rỗng (không phải view không có field). Đọc DDLS để biết field.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| RE-FX-2CL | 78 | top-level |
| RE-FX-BD-2CL | 58 | top-level |
| RE-FX-BP-2CL | 1 | top-level |
| RE-FX-CN-2CL | 30 | top-level |
| RE-FX-IP-2CL | 1 | top-level |
| RE-FX-RA-2CL | 4 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_RECONTRPAYMENTCASHFLOW | Real Estate Contract Payment Cash Flow | RE-FX-CN-2CL |  | 118 |
| I_RECONTROBJECTCASHFLOW | Real Estate Contract Object Cashflow | RE-FX-CN-2CL |  | 104 |
| I_REVALNASSETCASHFLOW | Real Estate Valuation Asset Cash Flow | RE-FX-2CL |  | 97 |
| I_REVALNLIABILITYCASHFLOW | Real Estate Valn Liability Cash Flow | RE-FX-2CL |  | 97 |
| I_REVALNSTRAIGHTLINECASHFLOW | RE Valuation Straightline Cash Flow | RE-FX-2CL |  | 97 |
| I_REVALNTRANSFERCASHFLOW | Real Estate Valuation Cash Flow | RE-FX-2CL |  | 97 |
| I_RECONTRACT | Real Estate Contract | RE-FX-CN-2CL |  | 89 |
| I_RECONTRCONDITION | Real Estate Conditions | RE-FX-CN-2CL |  | 84 |
| I_RECONTRACTDATA | Real Estate Contract | RE-FX-CN-2CL |  | 82 |
| I_RECONTRPOSTGTRMNOSENSTVDTA | Real Estate Posting Rule Term | RE-FX-2CL |  | 53 |
| I_REVALUATIONTERM | Real Estate Valuation Term | RE-FX-2CL |  | 51 |
| I_RECONTRRHYTHMTERM | Real Estate Rhythm Term | RE-FX-2CL |  | 43 |
| I_REUSABLEOBJECT | Real Estate Usable Object | RE-FX-BD-2CL |  | 39 |
| I_REMEASUREMENTTYPE | Real Estate Measurement Type | RE-FX-BD-2CL |  | 38 |
| I_RECONTRORGLASSGMTTERM | Real Estate Organizational Assgmt Term | RE-FX-2CL |  | 37 |
| I_RERENTABLEOBJECT | Real Estate Rentable Object | RE-FX-BD-2CL |  | 37 |
| I_REVALUATIONRULE | RE Valuation Rule | RE-FX-2CL |  | 34 |
| I_REDOCUMENTITEM | Real Estate Document Item | RE-FX-RA-2CL |  | 33 |
| I_REDOCUMENTHEADER | Real Estate Document Header | RE-FX-RA-2CL |  | 32 |
| I_REUSBLOBJADDLACCTASSGMTOBJ | RE Usable Object Addl Account Assign | RE-FX-BD-2CL |  | 31 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Company Code | 17 |
| ORG | Controlling Area | 5 |
| MASTER | Business Partner | 4 |
| MASTER | Cost Center | 3 |
| MASTER | WBS Element | 3 |
| ORG | Business Area | 2 |
| ORG | Profit Center | 2 |
| MASTER | Address | 2 |
| CONFIG | Fiscal Year | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| FI_other | 0 | 4 | 4 | Address, Business Partner, Cost Center, WBS Element |
| MM-PUR_Purchasing | 0 | 4 | 4 | Address, Business Partner, Cost Center, WBS Element |
| SD-BIL_Billing | 0 | 4 | 4 | Address, Business Partner, Cost Center, WBS Element |
| SD_other | 0 | 4 | 4 | Address, Business Partner, Cost Center, WBS Element |
| SD-SLS_Sales | 0 | 4 | 3 | Address, Business Partner, Cost Center, WBS Element |
| CA | 0 | 4 | 2 | Address, Business Partner, Cost Center, WBS Element |
| FIN | 0 | 3 | 4 | Business Partner, Cost Center, WBS Element |
| CRM | 0 | 3 | 3 | Business Partner, Cost Center, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. Mọi view ở đây là *released* theo danh sách chính thức của SAP. Cột `in_080 = no` → tenant 080 chưa có view đó (release mới hơn tenant), đừng dùng. Lần đầu dùng vẫn đọc `SAP(action=read, target=DDLS <tên>)` trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
