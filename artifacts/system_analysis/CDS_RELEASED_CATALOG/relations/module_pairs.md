# Quan hệ giữa các phân hệ ưu tiên (chung entity nghiệp vụ)

Generated 2026-09-25. Nguồn: cột *Data element* của sheet Fields. Hai phân hệ **liên quan** khi cùng có >= 2 view chứa cùng một entity (Sales Document, Material, Company Code...). Đây là bằng chứng **dùng chung khoá dữ liệu**, KHÔNG phải association CDS đã kiểm chứng.

Sắp theo số entity DOC, rồi MASTER, rồi ORG. Chỉ hiện cặp có >= 1 DOC hoặc >= 2 MASTER.

| Phân hệ A | Phân hệ B | DOC | MASTER | ORG | DOC entity chung | MASTER entity chung |
|---|---|---:|---:|---:|---|---|
| SD-SLS_Sales | SD-BIL_Billing | 3 | 11 | 11 | Document Condition (pricing), Order (production / maintenance / internal), Sales Document | Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| MM-PUR_Purchasing | MM-IM_Inventory-Management | 3 | 8 | 5 | Delivery, Order (production / maintenance / internal), Purchasing Document | Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| MM-PUR_Purchasing | SD-BIL_Billing | 2 | 12 | 6 | Document Condition (pricing), Order (production / maintenance / internal) | Address, Batch, Business Partner, Cost Center, Customer, G/L Account, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| MM-PUR_Purchasing | SD-SLS_Sales | 2 | 11 | 5 | Document Condition (pricing), Order (production / maintenance / internal) | Address, Batch, Business Partner, Cost Center, Customer, Material / Product, Material Group, Personnel, Profitability Segment, Supplier, WBS Element |
| FI-GL_General-Ledger | SD-BIL_Billing | 2 | 8 | 7 | Order (production / maintenance / internal), Sales Document | Cost Center, Customer, G/L Account, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| FI-GL_General-Ledger | CO-OM_Cost-Center-Accounting | 2 | 7 | 6 | Order (production / maintenance / internal), Sales Document | Activity Type, Cost Center, Customer, G/L Account, Personnel, Supplier, WBS Element |
| FI-GL_General-Ledger | SD-SLS_Sales | 2 | 7 | 6 | Order (production / maintenance / internal), Sales Document | Cost Center, Customer, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| CO-OM_Cost-Center-Accounting | SD-BIL_Billing | 2 | 6 | 5 | Order (production / maintenance / internal), Sales Document | Cost Center, Customer, G/L Account, Personnel, Supplier, WBS Element |
| CO-OM_Cost-Center-Accounting | SD-SLS_Sales | 2 | 5 | 4 | Order (production / maintenance / internal), Sales Document | Cost Center, Customer, Personnel, Supplier, WBS Element |
| SD-BIL_Billing | PS_Project-System | 2 | 2 | 3 | SD/LE Document (generic VBELN), Sales Document | Material / Product, WBS Element |
| FI-GL_General-Ledger | MM-PUR_Purchasing | 1 | 11 | 5 | Order (production / maintenance / internal) | Activity Type, Cost Center, Customer, Fixed Asset, G/L Account, Grant, Material / Product, Personnel, Profitability Segment, Supplier, WBS Element |
| MM-IM_Inventory-Management | SD-BIL_Billing | 1 | 8 | 5 | Order (production / maintenance / internal) | Batch, Cost Center, G/L Account, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| CO-OM_Cost-Center-Accounting | MM-PUR_Purchasing | 1 | 7 | 6 | Order (production / maintenance / internal) | Activity Type, Cost Center, Customer, G/L Account, Personnel, Supplier, WBS Element |
| MM-IM_Inventory-Management | SD-SLS_Sales | 1 | 7 | 4 | Order (production / maintenance / internal) | Batch, Cost Center, Material / Product, Material Group, Profitability Segment, Supplier, WBS Element |
| FI-GL_General-Ledger | MM-IM_Inventory-Management | 1 | 6 | 4 | Order (production / maintenance / internal) | Cost Center, G/L Account, Material / Product, Profitability Segment, Supplier, WBS Element |
| CO-OM_Cost-Center-Accounting | MM-IM_Inventory-Management | 1 | 4 | 4 | Order (production / maintenance / internal) | Cost Center, G/L Account, Supplier, WBS Element |
| FI-GL_General-Ledger | PS_Project-System | 1 | 3 | 3 | Sales Document | Grant, Material / Product, WBS Element |
| SD-SLS_Sales | PS_Project-System | 1 | 2 | 2 | Sales Document | Material / Product, WBS Element |
| CO-OM_Cost-Center-Accounting | PS_Project-System | 1 | 1 | 4 | Sales Document | WBS Element |
| MM-PUR_Purchasing | PP-SFC_Shop-Floor-Control | 0 | 7 | 6 | — | Batch, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| SD-BIL_Billing | PP-SFC_Shop-Floor-Control | 0 | 7 | 5 | — | Batch, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| MM-IM_Inventory-Management | PP-SFC_Shop-Floor-Control | 0 | 7 | 4 | — | Batch, Cost Center, G/L Account, Material / Product, Material Group, Supplier, WBS Element |
| SD-SLS_Sales | PP-SFC_Shop-Floor-Control | 0 | 6 | 4 | — | Batch, Cost Center, Material / Product, Material Group, Supplier, WBS Element |
| FI-GL_General-Ledger | PP-SFC_Shop-Floor-Control | 0 | 5 | 5 | — | Cost Center, G/L Account, Material / Product, Supplier, WBS Element |
| CO-OM_Cost-Center-Accounting | PP-SFC_Shop-Floor-Control | 0 | 4 | 6 | — | Cost Center, G/L Account, Supplier, WBS Element |
| MM-PUR_Purchasing | PS_Project-System | 0 | 3 | 4 | — | Grant, Material / Product, WBS Element |
| MM-PUR_Purchasing | LO-MD-BOM_Bill-of-Material | 0 | 3 | 2 | — | Material / Product, Material Group, Supplier |
| FI-AP_Accounts-Payable | CO-OM_Cost-Center-Accounting | 0 | 3 | 1 | — | Customer, G/L Account, Supplier |
| FI-AP_Accounts-Payable | MM-PUR_Purchasing | 0 | 3 | 1 | — | Customer, G/L Account, Supplier |
| FI-AP_Accounts-Payable | SD-BIL_Billing | 0 | 3 | 1 | — | Customer, G/L Account, Supplier |
| FI-GL_General-Ledger | FI-AP_Accounts-Payable | 0 | 3 | 1 | — | Customer, G/L Account, Supplier |
| MM-IM_Inventory-Management | LO-MD-BOM_Bill-of-Material | 0 | 3 | 1 | — | Material / Product, Material Group, Supplier |
| PP-SFC_Shop-Floor-Control | LO-MD-BOM_Bill-of-Material | 0 | 3 | 1 | — | Material / Product, Material Group, Supplier |
| SD-BIL_Billing | LO-MD-BOM_Bill-of-Material | 0 | 3 | 1 | — | Material / Product, Material Group, Supplier |
| SD-SLS_Sales | LO-MD-BOM_Bill-of-Material | 0 | 3 | 1 | — | Material / Product, Material Group, Supplier |
| FI-GL_General-Ledger | EAM-OBJ_Technical-Objects | 0 | 2 | 4 | — | Equipment, Material / Product |
| PP-SFC_Shop-Floor-Control | PS_Project-System | 0 | 2 | 4 | — | Material / Product, WBS Element |
| MM-IM_Inventory-Management | PS_Project-System | 0 | 2 | 3 | — | Material / Product, WBS Element |
| FI-GL_General-Ledger | PP-MRP_MRP | 0 | 2 | 2 | — | Material / Product, WBS Element |
| MM-PUR_Purchasing | PP-MRP_MRP | 0 | 2 | 2 | — | Material / Product, WBS Element |
| PP-SFC_Shop-Floor-Control | PP-MRP_MRP | 0 | 2 | 2 | — | Material / Product, WBS Element |
| SD-BIL_Billing | PP-MRP_MRP | 0 | 2 | 2 | — | Material / Product, WBS Element |
| SD-SLS_Sales | PP-MRP_MRP | 0 | 2 | 2 | — | Material / Product, WBS Element |
| FI-AP_Accounts-Payable | MM-IM_Inventory-Management | 0 | 2 | 1 | — | G/L Account, Supplier |
| FI-AP_Accounts-Payable | PP-SFC_Shop-Floor-Control | 0 | 2 | 1 | — | G/L Account, Supplier |
| FI-GL_General-Ledger | LO-MD-BOM_Bill-of-Material | 0 | 2 | 1 | — | Material / Product, Supplier |
| MM-IM_Inventory-Management | PP-MRP_MRP | 0 | 2 | 1 | — | Material / Product, WBS Element |
| PP-MRP_MRP | PS_Project-System | 0 | 2 | 1 | — | Material / Product, WBS Element |
| FI-AP_Accounts-Payable | SD-SLS_Sales | 0 | 2 | 0 | — | Customer, Supplier |
