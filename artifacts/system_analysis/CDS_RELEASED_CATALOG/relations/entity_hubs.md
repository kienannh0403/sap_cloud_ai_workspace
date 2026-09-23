# Entity nghiệp vụ → phân hệ dùng nó

Generated 2026-09-21. Với mỗi entity: số view mỗi folder (chỉ hiện folder >= 2 view). Dùng khi biết cần *dữ liệu gì* mà chưa biết *view nào*: tra entity, chọn folder có nhiều view nhất.

## DOC

| Entity | Data element | Folder (số view) |
|---|---|---|
| Billing Document | VBELN_VF |  |
| Delivery | VBELN_VL | LE (9), LO_other (3), SD_other (2), PP_other (2), MM-PUR_Purchasing (2), MM-IM_Inventory-Management (2) |
| Document Condition (pricing) | KNUMV | SD-SLS_Sales (21), MM-PUR_Purchasing (9), CRM (5), LE (3), LO_other (2) |
| Inspection Lot | QPLOS | QM (19), LE (5), PP-SFC_Shop-Floor-Control (3), PP_other (2), LO_other (2) |
| Order (production / maintenance / internal) | AUFNR | SD-SLS_Sales (25), LE (9), FI-GL_General-Ledger (9), PP_other (8), PM_other (5), MM-PUR_Purchasing (5), FI_other (4), SD_other (3), MM_other (2), MM-IM_Inventory-Management (2) |
| Purchasing Document | EBELN, EBELP | MM-PUR_Purchasing (36), MM-IM_Inventory-Management (4), PP_other (2), MM_other (2) |
| SD/LE Document (generic VBELN) | VBELN | SD_other (4), CO_other (3), PS_Project-System (2), MM_other (2), LE (2) |
| Sales Document | POSNR_VA, VBELN_VA, VDM_SALES_ORDER | SD-SLS_Sales (30), FI-GL_General-Ledger (9), SD_other (6), PS_Project-System (5), SD-BIL_Billing (4), PSM (2), PM_other (2), FI_other (2) |

## MASTER

| Entity | Data element | Folder (số view) |
|---|---|---|
| Activity Type | LSTAR | FI-GL_General-Ledger (16), MM-PUR_Purchasing (4), PSM (2), MM_other (2), CA (2) |
| Address | AD_ADDRNUM | SD-SLS_Sales (16), BC (8), MM-PUR_Purchasing (6), FI_other (3), CA (3), SD_other (2), SD-BIL_Billing (2), PP_other (2), LO_other (2) |
| Batch | CHARG_D | SD-SLS_Sales (11), PP_other (8), LE (8), MM-PUR_Purchasing (7), SCM (6), MM-IM_Inventory-Management (6), QM (4), PP-SFC_Shop-Floor-Control (3), SD_other (2), LO_other (2) |
| Business Partner | BU_PARTNER | SD-SLS_Sales (15), FI_other (10), AP (9), SLC (8), FIN (8), CA (8), LO_other (7), SCM (4), MM-PUR_Purchasing (3), BC (3) |
| Cost Center | KOSTL | SD-SLS_Sales (10), FI-GL_General-Ledger (7), SD_other (5), MM-PUR_Purchasing (5), CA (5), LE (4), QM (3), MM-IM_Inventory-Management (3), FIN (3), PP-SFC_Shop-Floor-Control (2) |
| Customer | KUNAG, KUNNR, KUNRE, KUNWE | SD-SLS_Sales (37), LO_other (26), SD_other (18), FI_other (10), LE (7), FI-GL_General-Ledger (7), SD-BIL_Billing (4), PSM (2), MM-PUR_Purchasing (2), FI-AP_Accounts-Payable (2) |
| Equipment | EQUNR | LO_other (11), PM_other (7), EAM-OBJ_Technical-Objects (6), QM (4), FI-GL_General-Ledger (4), PP_other (3), CRM (2) |
| Fixed Asset | ANLN1 | MM-PUR_Purchasing (5), FI-GL_General-Ledger (4), FI-AA_Asset-Accounting (4), MM_other (2) |
| G/L Account | FIS_RACCT, SAKNR | FI-GL_General-Ledger (22), MM-PUR_Purchasing (8), FI_other (7), CO_other (6), MM_other (4), LO_other (4), LE (4), MM-IM_Inventory-Management (3), SD-BIL_Billing (2), QM (2) |
| Grant | GM_GRANT_NBR | FI-GL_General-Ledger (14), MM-PUR_Purchasing (4), PSM (3), MM_other (2), FIN (2) |
| Material / Product | MATNR, PRODUCTNUMBER | LO-MD-MM_Material-Master (37), PP_other (22), MM-PUR_Purchasing (17), LO_other (17), SD_other (14), SD-SLS_Sales (12), FI-GL_General-Ledger (10), LE (9), SCM (8), PP-MRP_MRP (8) |
| Material Group | MATKL | MM-PUR_Purchasing (18), SD-SLS_Sales (11), SD_other (6), LE (4), PP_other (3), PP-SFC_Shop-Floor-Control (2), MM-IM_Inventory-Management (2) |
| Personnel | PERNR_D | SD-SLS_Sales (13), FI-GL_General-Ledger (9), LO_other (7), FI_other (3), SD_other (2), SD-BIL_Billing (2), PSM (2), MM_other (2), MM-PUR_Purchasing (2), CA (2) |
| Profitability Segment | RKEOBJNR_CHAR, RKEOBJNR_NUMC | SD-SLS_Sales (11), FI-GL_General-Ledger (5), LE (4), MM-PUR_Purchasing (3), SD_other (2), MM-IM_Inventory-Management (2), FI_other (2) |
| Supplier | LIFNR, MD_SUPPLIER | MM-PUR_Purchasing (22), LO_other (21), SD-SLS_Sales (14), PP_other (6), LE (6), FI-GL_General-Ledger (5), FI_other (4), PP-SFC_Shop-Floor-Control (3), CO_other (3), SD_other (2) |
| Task List (routing) group | PLNNR | PP_other (15), QM (6), PM_other (5), PP-SFC_Shop-Floor-Control (3) |
| WBS Element | PS_POSID, PS_POSID_EDIT, PS_PSP_PNR, PS_S4_PSPNR | CA (13), SD-SLS_Sales (12), PP_other (8), CRM (8), MM-PUR_Purchasing (6), FI-GL_General-Ledger (6), SCM (5), PS_Project-System (5), MM-IM_Inventory-Management (5), PP-MRP_MRP (4) |

## ORG

| Entity | Data element | Folder (số view) |
|---|---|---|
| Business Area | GSBER | SD-SLS_Sales (21), SD_other (10), FI_other (10), PP-SFC_Shop-Floor-Control (7), PP_other (5), MM_other (4), MM-PUR_Purchasing (4), LE (4), FI-GL_General-Ledger (4), QM (2) |
| Chart of Accounts | KTOPL | FI-GL_General-Ledger (18), FI_other (5), CO_other (2), CA (2) |
| Company Code | BUKRS, FIS_BUKRS | FI_other (57), FI-GL_General-Ledger (55), CA (47), MM-PUR_Purchasing (24), FIN (20), LO_other (15), MM_other (11), MM-IM_Inventory-Management (9), LO-MD-MM_Material-Master (9), FI-AR_Accounts-Receivable (9) |
| Controlling Area | FIS_KOKRS, KOKRS | FI-GL_General-Ledger (52), SD-SLS_Sales (20), CA (10), CO_other (9), PP_other (7), EC (7), PP-SFC_Shop-Floor-Control (6), CRM (6), SD_other (5), MM-PUR_Purchasing (4) |
| Distribution Channel | VTWEG | SD-SLS_Sales (45), SD_other (21), LO_other (10), SD-BIL_Billing (5), LE (5), FI_other (5), FI-GL_General-Ledger (5), LO-MD-MM_Material-Master (3), PSM (2), EAM-OBJ_Technical-Objects (2) |
| Division | SPART | SD-SLS_Sales (45), SD_other (17), LO_other (12), SD-BIL_Billing (5), LE (5), FI-GL_General-Ledger (5), FI_other (4), LO-MD-MM_Material-Master (2), EAM-OBJ_Technical-Objects (2) |
| Functional Area | FKBER | FI-GL_General-Ledger (9), PP_other (5), PP-SFC_Shop-Floor-Control (4), MM-PUR_Purchasing (4), PS_Project-System (3), LE (3), FIN (3), MM_other (2), FI_other (2) |
| Plant | WERKS_D | PP_other (89), QM (22), MM-IM_Inventory-Management (20), LO-MD-MM_Material-Master (20), PP-MRP_MRP (17), LE (14), FI-GL_General-Ledger (12), LO_other (10), PP-SFC_Shop-Floor-Control (8), MM_other (6) |
| Profit Center | PRCTR | SD-SLS_Sales (12), FI_other (9), SD_other (7), MM-PUR_Purchasing (6), CRM (6), MM_other (5), PP_other (4), PP-SFC_Shop-Floor-Control (4), LE (4), EC (4) |
| Purchasing Organization | EKORG | MM-PUR_Purchasing (26), LO_other (9), PP_other (3), MM_other (3) |
| Sales Group | VKGRP | SD-SLS_Sales (22), CRM (19), SD_other (18), LO_other (7), LE (5), EAM-OBJ_Technical-Objects (2) |
| Sales Office | VKBUR | SD-SLS_Sales (22), SD_other (20), CRM (19), LE (9), LO_other (7), EAM-OBJ_Technical-Objects (2) |
| Sales Organization | VKORG | SD-SLS_Sales (45), SD_other (22), CRM (20), LO_other (13), SD-BIL_Billing (7), FI_other (6), LE (5), FI-GL_General-Ledger (5), QM (3), LO-MD-MM_Material-Master (3) |
| Segment | FB_SEGMENT | FI-GL_General-Ledger (16), PSM (2), FI_other (2), FIN (2), EC (2) |
| Shipping Point | VSTEL | LE (13), SD-SLS_Sales (8), SD_other (7) |
| Storage Location | LGORT_D | MM-IM_Inventory-Management (14), SD-SLS_Sales (8), MM-PUR_Purchasing (6), LE (5), SD_other (4), LO-MD-MM_Material-Master (4), PP_other (3), LO_other (3), QM (2) |
| Valuation Area | BWKEY | LO-MD-MM_Material-Master (9), CO_other (8), FI-GL_General-Ledger (7), MM-IM_Inventory-Management (4), LO_other (2), CA (2) |

## CONFIG

| Entity | Data element | Folder (số view) |
|---|---|---|
| Fiscal Year | FIS_GJAHR_NO_CONV, GJAHR | FI-GL_General-Ledger (27), SD-SLS_Sales (22), CA (18), MM_other (17), FI_other (10), MM-IM_Inventory-Management (6), SD_other (5), FI-AR_Accounts-Receivable (3), PSM (2), CO_other (2) |
| Incoterms | INCO1 | SD-SLS_Sales (22), MM-PUR_Purchasing (20), LO_other (5), SD_other (4), LE (4), SD-BIL_Billing (3) |
| Movement Type | BWART | MM-IM_Inventory-Management (14), SD-SLS_Sales (5), LE (5), PP_other (3), QM (2) |
| Payment Terms | DZTERM | SD-SLS_Sales (26), SD_other (14), LO_other (5), CA (3), SD-BIL_Billing (2), FI_other (2) |
| Sales Document Type | AUART | SD-SLS_Sales (19), SD_other (13), FI-GL_General-Ledger (5), PSM (2) |
| Tax Code | MWSKZ | MM-PUR_Purchasing (14), SD-SLS_Sales (11), FI_other (11), MM_other (7), CA (5), LO_other (4), SD-BIL_Billing (3), CRM (2) |
