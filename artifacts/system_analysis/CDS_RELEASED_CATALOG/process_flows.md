# Luồng nghiệp vụ nối các phân hệ (kiến thức SAP, KHÔNG rút ra từ file xlsx)

Đây là kiến thức SAP chuẩn về chuỗi chứng từ, đặt cạnh dữ liệu thật của file để biết **view của bước nào nằm ở folder nào**.
Phần *bằng chứng dữ liệu* (entity dùng chung) ở `relations/module_pairs.md` và `relations/entity_hubs.md`.
Nghiệp vụ sâu hơn: các skill `sap-process-*`. Tên view cụ thể phải tra `modules/<folder>/views.csv`.

Folder ở cột phải là tên thư mục trong `modules/`.

## Order-to-Cash (O2C) — SD trọng tâm

| Bước | Chứng từ | Folder chứa view |
|---|---|---|
| Báo giá / Đơn bán / Hợp đồng / Trả hàng | Quotation, Sales Order, Contract, Returns | `SD-SLS_Sales` |
| Giá & điều kiện, tín dụng | Pricing procedure/condition, Credit | `SD_other` (SD-BF-PR, SD-BF-CM), `FIN` (FIN-FSCM-CR) |
| Giao hàng | Delivery, picking, goods issue | `LE` (LE-SHP-GF) → trừ kho ở `MM-IM_Inventory-Management` |
| Lập hoá đơn | Billing document, invoice list, billing plan | `SD-BIL_Billing` |
| Công nợ phải thu | Open item khách hàng | `FI-AR_Accounts-Receivable` |
| Hạch toán | Journal entry | `FI-GL_General-Ledger` |
| Master dùng xuyên suốt | Customer, Business Partner, Material | `LO_other` (LO-MD-BP), `AP` (AP-MD-BP), `LO-MD-MM_Material-Master` |

## Procure-to-Pay (P2P)

`MM-PUR_Purchasing` (PR → RFQ → PO) → nhập kho `MM-IM_Inventory-Management` → đối chiếu hoá đơn `MM_other` (MM-IV-LIV)
→ `FI-AP_Accounts-Payable` → `FI-GL_General-Ledger`. Supplier master ở `LO_other` (LO-MD-BP).

## Plan-to-Produce

Master `LO-MD-MM_Material-Master` + `LO-MD-BOM_Bill-of-Material` (+ routing, work center ở `PP_other`, component PP-VDM-MD)
→ `PP-MRP_MRP` (planned order, độc lập/phụ thuộc requirement) → `PP-SFC_Shop-Floor-Control` (lệnh sản xuất, xác nhận)
→ goods movement `MM-IM_Inventory-Management` → quyết toán / giá thành `CO_other` (CO-PC-*) → `FI-GL_General-Ledger`.
Lưu ý: `PP-MRP` và `PP-SFC` trong file được gán **theo từ khoá tên view** (xem `module_map.md`).

## Project / Maintenance / Kế toán

- **Dự án:** `PS_Project-System` (Enterprise Project, WBS, demand, project billing) ↔ `CO`, `SD-SLS` (billing theo dự án), `MM-PUR`.
- **Bảo trì:** `EAM-OBJ_Technical-Objects` (Equipment, Functional Location) → `PM_other` (thông báo, lệnh bảo trì) → `CO`, `MM`.
- **Sổ cái:** `FI-GL_General-Ledger` là điểm đến của gần như mọi luồng; `FI-AA_Asset-Accounting` (tài sản), `CO-OM_Cost-Center-Accounting` + `CO_other` (chi phí).

## Bẫy đã thấy khi lập catalog (từ dữ liệu file)

- Component trong file **không luôn trùng trực giác**: `I_CompanyCode`, `I_GLAccount` nằm ở `FI-GL-*` (`I_CostCenter` ở `CO-OM` theo danh sách SAP 2026-09-25);
  `I_Customer`, `I_Supplier`, `I_Plant` nằm ở `LO-MD-*` (folder `LO_other`), `I_BusinessPartner` ở `AP-MD-BP` (folder `AP`).
- Tên view có hậu tố API/phiên bản: `I_PurchaseOrderAPI01`, `I_PurchaseRequisitionAPI01`, `I_MaterialDocumentHeader_2`.
  Đừng tìm bằng tên "gọn" (`I_PurchaseOrder`) — grep theo phần thân tên.
- Không thấy trong sheet CDS: `I_Material`, `I_ProductionOrder` (khác `I_ProductionVersion`, đã verify released — xem `verified_external/PP.md`), `I_SalesPricingCondition`.
  **Không kết luận** chúng không tồn tại/không released: file chỉ là nguồn user cung cấp; tra sap-docs hoặc hệ thống trước khi kết luận.
- `I_BillingDocument` / `I_BillingDocumentItem`: **có** trong sheet Fields (nên có trong `_fields_only/`), chỉ **không** có trong sheet CDS — không phải "không tồn tại trong file" như đã ghi trước đây (sửa 2026-09-23). Nguồn ngoài xếp chúng là candidate `[Unverified]` released, chưa xác nhận chắc — xem giới hạn phạm vi ở `INDEX.md`.
