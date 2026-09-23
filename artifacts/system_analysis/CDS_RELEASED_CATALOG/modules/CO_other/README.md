# CO_other

Generated 2026-09-21 from `.claude/Documents/CDSView_Released_updated (1).xlsx` by `build_catalog.py`. Do not hand-edit; re-run the script.

Nhóm còn lại của module `CO` (không thuộc phân hệ ưu tiên nào trong Sheet1).

**34 view** · data category: (none) 19, Cube 6, Dimension 6, Fact 3 · loại: value_help 9, text 8, cube 6, dimension 5, basic 3, fact 3 · 1 view có field DEPRECATED/DECOMMISSIONED.

## Component trong nhóm

| Component | Số view | Cách gán |
|---|---:|---|
| CO-PC-ACT | 2 | top-level |
| CO-PC-ML | 3 | top-level |
| CO-PC-OBJ-ORD | 5 | top-level |
| CO-PC-OBJ-PER | 2 | top-level |
| CO-PC-PCP | 22 | top-level |

## View chính (heuristic: bỏ TEXT/value help, xếp theo số field)

| View | Mô tả | Component | Category | Field |
|---|---|---|---|---:|
| I_PRODCOSTESTCOSTCOMPRAWDEX | Prod Cost Est Cost Comp Raw Data Ext | CO-PC-PCP | Fact | 135 |
| I_PRODUCTCOSTESTIMATE | Product Cost Estimate | CO-PC-PCP | Fact | 104 |
| I_MATERIALLEDGERCUBE_LIT | Line Item for Material Ledger - Cube | CO-PC-ML | Cube | 78 |
| I_MFGORDERACTLPLANTGTLDGRCOST | Manufacturing Order Actual Plan Target Ledger Specific Cost | CO-PC-OBJ-ORD | Cube | 74 |
| I_MFGORDEREVTBSDWIPVARIANCE | Event-Based WIP and Variance of Manufacturing Order | CO-PC-OBJ-ORD | Cube | 62 |
| I_TRANSBSDMATLVALUECHAINITEM | Transaction-Based Material Value Chain Item | CO-PC-ACT | Fact | 39 |
| I_PCCACTLTGTCOSTCUBE | Actual and Target Costs for PCC - Cube | CO-PC-OBJ-PER | Cube | 38 |
| I_MATLINVTRYLDGRQTYSTRUCTURE | Matl Invtry Ledger with Qty Structure | CO-PC-ACT |  | 31 |
| I_INVENTORYPRICEBYKEYDATE | Inventory Price By KeyDate | CO-PC-ML | Cube | 31 |
| I_PCCEVTBSDWIPVARIANCECUBE | WIP and Variance for Event-Based PCC - Cube | CO-PC-OBJ-PER | Cube | 30 |
| I_COSTINGVERSION | Costing Version | CO-PC-PCP | Dimension | 9 |
| I_COSTINGTYPE | Costing Type | CO-PC-PCP | Dimension | 8 |
| I_COSTINGVALUATIONVARIANT | Valuation Variant in Costing | CO-PC-PCP | Dimension | 6 |
| I_COSTORIGINGROUP | Cost Origin Group | CO-PC-PCP | Dimension | 6 |
| I_COSTINGOVERHEADGROUP | Costing Overhead Group | CO-PC-PCP | Dimension | 5 |
| I_EVENTBASEDPROCESSINGKEY | Event-Based Posting Processing Key | CO-PC-OBJ-ORD |  | 3 |
| I_SLSORDPROJVALUATIONSTRATEGY | Valuation Strategy | CO-PC-PCP |  | 2 |

## Entity nghiệp vụ xuất hiện (từ data element, ngưỡng >= 2 view)

| Tier | Entity | Số view |
|---|---|---:|
| ORG | Controlling Area | 9 |
| ORG | Valuation Area | 8 |
| MASTER | Material / Product | 7 |
| ORG | Company Code | 7 |
| MASTER | G/L Account | 6 |
| ORG | Plant | 6 |
| DOC | SD/LE Document (generic VBELN) | 3 |
| MASTER | Supplier | 3 |
| MASTER | WBS Element | 3 |
| CONFIG | Fiscal Year | 2 |
| ORG | Chart of Accounts | 2 |

## Phân hệ liên quan (chung entity)

| Phân hệ | DOC | MASTER | ORG | Entity chung (DOC / MASTER) |
|---|---:|---:|---:|---|
| MM_other | 1 | 4 | 3 | SD/LE Document (generic VBELN), G/L Account, Material / Product, Supplier, WBS Element |
| LE | 1 | 4 | 2 | SD/LE Document (generic VBELN), G/L Account, Material / Product, Supplier, WBS Element |
| SD_other | 1 | 3 | 1 | SD/LE Document (generic VBELN), Material / Product, Supplier, WBS Element |
| PS_Project-System | 1 | 2 | 2 | SD/LE Document (generic VBELN), Material / Product, WBS Element |
| FI-GL_General-Ledger | 0 | 4 | 5 | G/L Account, Material / Product, Supplier, WBS Element |
| FI_other | 0 | 4 | 4 | G/L Account, Material / Product, Supplier, WBS Element |
| MM-IM_Inventory-Management | 0 | 4 | 4 | G/L Account, Material / Product, Supplier, WBS Element |
| MM-PUR_Purchasing | 0 | 4 | 3 | G/L Account, Material / Product, Supplier, WBS Element |

## Cách dùng

1. Tìm view trong `views.csv` (cột `key_entities` cho biết view chứa Customer / Material / Company Code...).
2. View nằm trong file = nguồn user cung cấp là *released*; lần đầu dùng vẫn verify trên hệ thống (`SAP(action=read, target=DDLS <tên>)`) trước khi đưa vào TS.
3. Không tìm thấy ở đây thì mới ra các folder liên quan (bảng trên), rồi mới tra ngoài.
