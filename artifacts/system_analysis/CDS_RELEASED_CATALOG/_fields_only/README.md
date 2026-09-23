# Views chỉ có trong sheet Fields

1914 view xuất hiện trong sheet **Fields** nhưng **không** có trong sheet **CDS** (1450 view không có cả component). File không nói chúng có released hay không, nên **không** đưa vào các folder phân hệ. Chỉ dùng để tra field; muốn dùng view thì verify release trên hệ thống trước.

**Cập nhật 2026-09-23 — một số view ở đây ĐÃ verify released thật** (nguồn ngoài, xem
`../verified_external/`), dù không có ở sheet CDS: `I_TaxCodeRate` (FI), `I_ActlCostGMatlValueChainItem`,
`I_ActualCostingRunResult`, `I_ActualCostingActivityResult`, `I_InventoryPriceByKeyDate_2` (CO),
`I_BillingDocument`/`I_BillingDocumentItem` (SD, mức `[Unverified]` — chỉ là candidate ở nguồn ngoài, chưa
chắc). Kết luận: **"chỉ ở Fields, không ở CDS" không đồng nghĩa "chưa được xác nhận released"** — trước khi
loại một view vì lý do này, kiểm `verified_external/` xem đã có ai xác nhận chưa.
