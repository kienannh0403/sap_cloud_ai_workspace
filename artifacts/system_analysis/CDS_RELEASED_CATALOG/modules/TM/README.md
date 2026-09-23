# TM

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `TM` (không thuộc phân hệ ưu tiên nào trong Sheet1). `TM`: Transportation Management.

**79 view** · data category: (none) 47, Dimension 32 · loại: basic 35, dimension 32, text 12 · 0 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| TM | 57 | top-level |
| TM-FRM | 18 | top-level |
| TM-FRS | 1 | top-level |
| TM-MD-ORG | 3 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_TRANSPORTATIONORDERITEM_2 | Transportation Order Item | TM-FRM |  | 100 |
| I_TRANSPORTATIONORDER_2 | Transportation Order | TM-FRM |  | 91 |
| I_TRANSPORTATIONORDERSTAGE_2 | Transportation Order Stage | TM-FRM |  | 37 |
| I_TRANSPORTATIONORDERSTOP_2 | Transportation Order Stop | TM-FRM |  | 36 |
| I_TRANSPORTATIONORDEREVENT | Transportation Order Event | TM-FRM |  | 23 |
| I_TRANSPORDDOCREF_2 | Transp Order Document Reference | TM-FRM |  | 13 |
| I_TRANSPORDITEMDOCREF | Transp Order Item Document Reference | TM-FRM |  | 13 |
| I_PURCHASEORDITMTRANSPSETTLMT | Purchase order Item Transportation sett | TM-FRS |  | 12 |
| I_TRANSPCOCODEBPASSGMT | Company Code and Business Partner Assgmt | TM-MD-ORG |  | 10 |
| I_TRANSPORTATIONORDERBP_2 | Transportation Order Business Partner | TM-FRM |  | 9 |
| I_TRANSPORDITEMCOMMODITYCODE | Transp Order Item Commodity Code | TM-FRM |  | 8 |
| I_TRANSPORDITEMSEAL | Transportation Order Item Seal | TM-FRM |  | 7 |
| I_TRANSPORDERCATEGORYT_2 | Transportation Order Category - Text | TM |  | 6 |
| I_TRANSPORDEXECSTATUSTEXT_2 | Transp Order Execution Status - Text | TM |  | 6 |
| I_TRANSPORDINVCGCARRIERLVLT | Transp Ord Invoicing Carrier Lvl - Text | TM |  | 6 |
| I_TRANSPORDITEMCATEGORYT_2 | Transp Order Item Category - Text | TM |  | 6 |
| I_TRANSPORDLIFECYCSTATUST_2 | Transp Order Lifecycle Status - Text | TM |  | 6 |
| I_TRANSPORDPLANNINGSTATUST_2 | Transp Order Planning Status - Text | TM |  | 6 |
| I_TRANSPORDSTAGECATEGORYT_2 | Transp Order Stage Category - Text | TM |  | 6 |
| I_TRANSPORDSTGEINVCGCARRLVLT | Transp Ord Stg Invcg Carrier Lvl - Text | TM |  | 6 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| MASTER | Business Partner | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| AP | 0 | 1 | 0 | Business Partner |
| BC | 0 | 1 | 0 | Business Partner |
| CA | 0 | 1 | 0 | Business Partner |
| FIN | 0 | 1 | 0 | Business Partner |
| FI_other | 0 | 1 | 0 | Business Partner |
| LO_other | 0 | 1 | 0 | Business Partner |
| MM-PUR_Purchasing | 0 | 1 | 0 | Business Partner |
| SCM | 0 | 1 | 0 | Business Partner |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
