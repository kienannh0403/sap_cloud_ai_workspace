# FI — verified external (FI-GL, BC-SRV-ADR)

Nguồn: xem `README.md` cùng thư mục. Đối chiếu 2026-09-23 với `catalog_all.csv`.

## Journal Entry — header vs item (bẫy hay gặp)

Field "Reference" (số hoá đơn, nhãn UI = BKPF-XBLNR) chỉ có ở **header**, field "Reference Key 1/2/3" chỉ có ở
**item** — hai view khác nhau, không thể lấy cả hai từ một view:

- **`I_JournalEntry`** (header) — released `FI-GL-IS-2CL`, trong catalog: `modules/FI-GL_General-Ledger/`.
  Field xác nhận: `CompanyCode`, `FiscalYear`, `AccountingDocument`, `DocumentReferenceID` (= "Reference"),
  `DocumentDate`.
- **`I_JournalEntryItem`** (item) — released. **KHÔNG có** `DocumentReferenceID`, **KHÔNG có**
  `Reference1/2/3IDByBusinessPartner`. Field xác nhận: `CompanyCode`, `FiscalYear`, `AccountingDocument`,
  `DocumentDate`, `Supplier`, `GLAccount`, `TaxCode`, `TaxCountry`.
- **`I_OperationalAcctgDocItem`** (item FI-AP/AR/GL, dùng bởi app "Manage Supplier/Customer Line Items") —
  released. Field xác nhận: `CompanyCode`, `FiscalYear`, `AccountingDocument`, `AccountingDocumentItem`,
  `Supplier`, `DocumentDate`, `GLAccount`, `Reference1/2/3IDByBusinessPartner` (= "Reference Key 1/2/3"),
  `TaxCode`, `TaxAmount`, `TaxAmountInCoCodeCrcy`, `TaxBaseAmountInCoCodeCrcy`, `AmountInCompanyCodeCurrency`.
  **KHÔNG có** field "Reference"/"Base Amount" đơn giản: Reference phải join `I_JournalEntry` qua
  CompanyCode+FiscalYear+AccountingDocument; "Base Amount" (giá trị trước thuế) không có field tên thẳng —
  gần nhất tuỳ ngữ cảnh là `TaxBaseAmountInCoCodeCrcy` / `OriginalTaxBaseAmount` / `CashDiscountBaseAmount`.
  **Hỏi rõ nghiệp vụ** "Base Amount" nghĩa là base của dòng thuế nào trước khi chọn field.
- **`I_TaxCodeRate`** — released `FI-GL-IS-2CL`. ⚠️ **Đối chiếu 2026-09-23: có trong sheet Fields nhưng KHÔNG có
  trong sheet CDS của xlsx** → không nằm trong `modules/FI-GL_General-Ledger/views.csv` dù đã released thật.
  Coi đây là released, đừng dựa hoàn toàn vào việc "có mặt trong `catalog_all.csv`" để kết luận released hay không.

## Address KHÔNG nằm trong FI

`I_OrganizationAddress` (+ `I_Country`, `I_Region`, `I_RegionText`) — application component **`BC-SRV-ADR`**,
trong catalog nằm ở **folder `BC`**, không phải `FI-GL_*`. Field: `AddresseeName1/2` (Name1/2),
`Street`/`StreetName`/`StreetPrefixName1/2`/`StreetSuffixName1/2` (**không có** field literal "Street2"/"Street3"),
`Region` (code, join `I_RegionText` lấy mô tả), `Country` (code, assoc `_Country` → `I_Country` lấy mô tả). Join
với company code: `I_CompanyCode.AddressID = I_OrganizationAddress.AddressID`. `I_CompanyCode` released
`FI-GL-GL-N-2CL`.

**Bẫy tổng quát:** field địa chỉ (Name1/Street/Region/Country) của company/vendor/customer thường nằm ở component
`BC-SRV-ADR` chứ không phải component của module đang tra (FI/MM/SD) — nếu tìm mãi không thấy field địa chỉ trong
folder module, thử folder `BC` trước khi kết luận không có.
