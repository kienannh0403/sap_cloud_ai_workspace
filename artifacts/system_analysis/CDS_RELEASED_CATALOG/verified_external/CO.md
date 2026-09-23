# CO — verified external (CO-PC-PCP / CO-PC-ACT / CO-PC-ML / CO-OM)

Nguồn: xem `README.md` cùng thư mục. Đối chiếu 2026-09-23 với `catalog_all.csv`. Trong catalog, các view này đều
rơi vào folder `CO_other` hoặc `CO-OM_Cost-Center-Accounting` (component `CO-PC-*` không phải phân hệ ưu tiên
Sheet1).

## Cost component split — PLANNED có API, ACTUAL không có CDS released (kết luận chính thức từ SAP)

- **`I_ProductCostEstimate`** (header Cost Estimate, ~CK13N) — released `CO-PC-PCP-2CL`. Field: `CostEstimate`
  (NUMC), `Product`, `Plant`, `CostingVariant` (**CHAR4**, = KLVAR), `CostingVersion` (NUMC), `CostingType`,
  `ValuationVariant`, `CostEstimateStatus`, `CostEstimateValidityStartDate/EndDate`, `CostingLotSize` (QUAN),
  `CostComponentStructure`, `ControllingArea`, `CompanyCode`, `Ledger`. Assoc `_ProductCostEstimateItem`,
  `_CostingVariant`, `_CostingVersion`.
  - ⚠️ **`CostingVariant` chỉ CHAR4** — nhãn costing variant trong FS đôi khi dài hơn 4 ký tự hoặc không khớp mã
    KLVAR thật trên tenant → luôn xác nhận mã thật trên hệ thống trước khi lọc, đừng suy mã từ nhãn FS.
  - ⚠️ **Validity của estimate thường NGẮN** (theo tháng) — báo cáo theo NĂM phải chọn estimate có
    **validity GIAO với năm** (`ValidityStart <= 31/12 AND ValidityEnd >= 01/01`), không phải khoá theo "ngày
    cuối tháng báo cáo" — nếu không, tháng nằm ngoài validity hẹp của estimate sẽ ra rỗng.
- **`I_ProdCostEstCostCompRawDex`** ("Prod Cost Est Cost Comp Raw Data Ext") — released `CO-PC-PCP-2CL`. Fact
  view join `I_ProductCostEstimate` qua `_ProductCostEstimate`.
  - 🔴 **KHÔNG có field `CostComponentName`.** Amount lưu theo cột pivot `CostComponentCostField1Amt` ...
    `CostComponentCostField120Amt` (120 cột CURR), mỗi cột ứng với **VỊ TRÍ**, không phải **SỐ cost component**
    thật. Mapping vị trí → số nằm trong customizing (TCKH3), **KHÔNG expose ra CDS released nào**. Unpivot theo
    vị trí rồi join `I_CostComponentStdVH` (value help số↔tên) sẽ ra **sai số và trống tên**.
  - 🟢 **Cách đúng**: gọi FUNCTION read-only **`GetBreakdownByCompView`** trên BO **`I_ProductCostEstimateTP`**
    (entity `ProductCostEstimate`) qua EML, param `CostComponentView` (vd `'01'` = COGM, xem
    `I_CostComponentView.CostCompIsForCOGM`). Kết quả `D_CostEstGetBrkdwnByCompViewR` → assoc `_CostComponents`
    → `D_CostEstCostComponentR` { `CostComponent`, `CostComponentName`, `TotalAmountInCoCodeCrcy`,
    `FixedAmountInCoCodeCrcy` }. 7 key BO cần truyền: `CostingReferenceObject`, `CostEstimate`, `CostingType`,
    `CostingDate`, `CostingVersion`, `ValuationVariant`, `CostIsEnteredManually`. Kết quả phân cấp — **test
    trong ADT thật**, harness không parse được EML lồng nhau.
- **`I_CostComponentStdVH`** — released `CO-PC-PCP-2CL`. Value help: `CostComponent` (NUMC) ↔
  `CostComponentName`, `CostComponentStructure`, assoc `_CostComponentText`.
- **`I_ActlCostGMatlValueChainItem`**, **`I_ActualCostingRunResult`**, **`I_ActualCostingActivityResult`** —
  released `CO-PC-ACT-2CL`. ⚠️ **Đối chiếu 2026-09-23: cả 3 view chỉ có trong sheet Fields của xlsx, KHÔNG có
  trong sheet CDS** → không nằm trong `views.csv` của catalog dù đã released thật.
  - 🔴 **KẾT LUẬN CHÍNH THỨC TỪ SAP** (SAP Community, câu trả lời SAP xác nhận nguyên văn): *"If you are
    requesting data for cost component split for each material and its movements, no CDS view exists for this
    purpose."* → 2602 **KHÔNG có CDS released cho ACTUAL costing cost-component split** (bảng nền `MLCD` đã đổi
    tên `MLDOC`/`MLDOCCCS` nhưng không có VDM/CDS expose). Nếu FS đòi breakdown cost component cho **actual**
    (không phải planned) → đây là **blocker thật**, không phải thiếu tra cứu. Lựa chọn: dùng Cost Estimate
    (planned) làm proxy nếu nghiệp vụ chấp nhận, downgrade về tổng amount không breakdown, hoặc escalate.
- **`I_MaterialLedgerCube_Lit`** — released `CO-PC-ML-2CL`, **có trong** `catalog_all.csv` (folder `CO_other`).
  Field: `Material`, `MaterialGroup`, `MaterialGroupName`, `Plant`, `Ledger`, `FiscalYear/Period/YearPeriod`,
  `ValuationArea`, `AmountInCompanyCodeCurrency`, `AmountInGroupCurrency`, `InventoryQty`, `PostingDate`,
  `CompanyCode`, `ControllingArea`, `CostCenter`, `ProfitCenter`, `GLAccount`. Phân biệt receipt/consumption qua
  `BusinessTransactionType`/`MaterialLedgerProcessType` (verify giá trị thật trên tenant, đừng đoán).
  **`MaterialGroup` (MATKL) của Product KHÔNG có trên `I_Product`** (chỉ `ProductGroup`=Division,
  `PackagingMaterialGroup`) — chỉ xuất hiện ở đây và ở BOM item view.
- **`I_InventoryPriceByKeyDate`** — released `CO-PC-ML-2CL`, **PARAMETERIZED** (`P_CalendarDate`) và
  **DEPRECATED** → dùng successor **`I_InventoryPriceByKeyDate_2`** (cũng chỉ ở sheet Fields, không ở CDS).
  Field: `ActualPrice`, `StandardPrice`, `InventoryPrice`, `MaterialPriceControl` (S/V), `Material`,
  `ValuationArea`, `Currency`, `Ledger`, `FiscalYear/Period/YearPeriod`, `CostEstimate`.
- **`I_MfgOrderActlPlanTgtLdgrCost`** — released `CO-PC-OBJ-ORD-2CL` (từ S/4HANA Cloud 2111). **PARAMETERIZED**:
  5 param bắt buộc `P_FromFiscalYearPeriod`/`P_ToFiscalYearPeriod` (format `fins_fyearperiod` = YYYYPPP),
  `P_Ledger`, `P_CurrencyRole` (mặc định `'10'`), `P_TargetCostVariant` (mặc định `'000'`). **KHÔNG có
  PostingDate** — lọc kỳ chỉ qua param. Đơn vị = **`UnitOfMeasure`** (không phải `BaseUnit`). Field:
  `ActualQtyInCostSourceUnit`, `PlanQtyInCostSourceUnit`, `TargetQtyInCostSourceUnit`,
  `DebitActlCostInDspCrcy`, `CreditActlCostInDspCrcy`, `PartnerCostCenter`, `PartnerCostCtrActivityType`,
  `Order`/`OrderItem`/`OrderOperation`, `Plant`, `Product`, `WorkCenter`. **KHÔNG breakdown theo cost
  component** — chỉ theo `GLAccount` + Order/Operation + Partner.

## `#PUBLIC_LOCAL_API` KHÔNG đồng nghĩa với released C1 (bẫy quan trọng, tổng quát cho mọi module)

Khi tìm view cho "Manage Cost Rates – Actual": `I_CostCenterActivityType` chỉ là master data (sai mục đích).
`I_ActualCostRate` và `I_AccountingCostRate_2` **tồn tại và có annotation `#PUBLIC_LOCAL_API`** nhưng **KHÔNG có
trong `released-objects-index.json`** → gọi trong class ABAP Cloud báo lỗi "use not permitted". View **đúng**
là **`I_ActualCostRateTP`** (`CO-OM-2CL`, transactional_interface, field `CostCenter`/`ActivityType`/
`CostRateFixedAmount`/`Currency`/`ValidityStartDate/EndDate`). Đối chiếu 2026-09-23: cả 3 view này (đúng lẫn sai)
đều **không có** trong `catalog_all.csv` của xlsx — vì đều thuộc dạng transactional-interface/TP, catalog xlsx
này hình như chỉ liệt view "view" thường, không có nhóm TP.

**Bài học tổng quát:** annotation `#PUBLIC_LOCAL_API` trên source KHÔNG đủ để kết luận view dùng được trong ABAP
Cloud — chỉ `released-objects-index.json` (hoặc View Browser ADT tương đương) mới là nguồn xác thực. Luôn kiểm
`vsp source DDLS <tên>` xem `with parameters` + `lifecycle.contract.type` **trước khi code**, đừng suy từ tên
hay annotation.

## Cross-module: PIR thuộc PP, không phải CO

Xem `PP.md` cùng thư mục — nhiều báo cáo giá thành/kế hoạch (CO) cần dữ liệu PIR nhưng bản thân PIR là view của
phân hệ PP (`PP-VDM-2CL`).
