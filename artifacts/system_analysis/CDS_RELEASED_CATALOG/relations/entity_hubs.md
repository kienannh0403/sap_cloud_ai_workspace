# Entity nghiệp vụ → phân hệ dùng nó

Generated 2026-09-25. Với mỗi entity: số view mỗi folder (chỉ hiện folder >= 2 view). Dùng khi biết cần *dữ liệu gì* mà chưa biết *view nào*: tra entity, chọn folder có nhiều view nhất.

## DOC

| Entity | Data element | Folder (số view) |
|---|---|---|
| Billing Document | VBELN_VF | SD-BIL_Billing (19), SD_other (4), CA (2) |
| Delivery | VBELN_VL | LE (9), MM-PUR_Purchasing (5), LO_other (3), SD_other (2), PP_other (2), MM-IM_Inventory-Management (2) |
| Document Condition (pricing) | KNUMV | SD-SLS_Sales (21), MM-PUR_Purchasing (13), SD-BIL_Billing (8), CRM (6), SD_other (3), LO_other (3), LE (3) |
| Inspection Lot | QPLOS | QM (22), LE (5), PP-SFC_Shop-Floor-Control (4), PP_other (2), LO_other (2) |
| Order (production / maintenance / internal) | AUFNR | SD-SLS_Sales (25), PM_other (15), LE (9), PP_other (8), FI-GL_General-Ledger (7), MM-PUR_Purchasing (6), SD_other (5), SD-BIL_Billing (5), FI_other (5), FIN (3) |
| Purchasing Document | EBELN, EBELP | MM-PUR_Purchasing (68), MM-IM_Inventory-Management (4), PP_other (2), PM_other (2), MM_other (2), FI_other (2), FIN (2), CO_other (2) |
| SD/LE Document (generic VBELN) | VBELN | CO_other (7), SD_other (4), SD-BIL_Billing (2), PS_Project-System (2), MM_other (2), LE (2), FI_other (2) |
| Sales Document | POSNR_VA, VBELN_VA, VDM_SALES_ORDER | SD-SLS_Sales (30), SD_other (11), FI-GL_General-Ledger (11), SD-BIL_Billing (9), PS_Project-System (5), FI_other (3), PSM (2), PM_other (2), FIN (2), CO_other (2) |

## MASTER

| Entity | Data element | Folder (số view) |
|---|---|---|
| Activity Type | LSTAR | FI-GL_General-Ledger (14), CO-OM_Cost-Center-Accounting (12), MM-PUR_Purchasing (5), PM_other (4), FI_other (4), CO_other (4), PSM (2), MM_other (2), FIN (2), CA (2) |
| Address | AD_ADDRNUM | BC (24), SD-SLS_Sales (16), AP (11), SD-BIL_Billing (9), MM-PUR_Purchasing (9), CA (6), FI_other (3), SD_other (2), RE (2), PP_other (2) |
| Batch | CHARG_D | SD-SLS_Sales (11), SCM (11), MM-PUR_Purchasing (11), PP_other (9), LO_other (8), LE (8), SD_other (7), MM-IM_Inventory-Management (6), SD-BIL_Billing (5), PP-SFC_Shop-Floor-Control (5) |
| Business Partner | BU_PARTNER | AP (23), SD-SLS_Sales (15), FIN (14), FI_other (12), SLC (8), SD-BIL_Billing (8), SCM (8), CA (8), LO_other (7), BC (6) |
| Cost Center | KOSTL | SD-SLS_Sales (10), FIN (9), CO-OM_Cost-Center-Accounting (9), SD_other (7), FI_other (7), SD-BIL_Billing (6), MM-PUR_Purchasing (6), CRM (6), LE (4), CA (4) |
| Customer | KUNAG, KUNNR, KUNRE, KUNWE | SD-SLS_Sales (37), LO_other (29), SD_other (25), SD-BIL_Billing (22), FI_other (14), FI-GL_General-Ledger (9), LE (8), CA (7), FIN (5), MM-PUR_Purchasing (3) |
| Equipment | EQUNR | PM_other (15), LO_other (11), CRM (8), EAM-OBJ_Technical-Objects (7), QM (5), FI-GL_General-Ledger (5), PP_other (4) |
| Fixed Asset | ANLN1 | MM-PUR_Purchasing (6), FI_other (6), FI-GL_General-Ledger (4), MM_other (2), FIN (2) |
| G/L Account | FIS_RACCT, SAKNR | FI-GL_General-Ledger (25), MM-PUR_Purchasing (9), FI_other (9), SD-BIL_Billing (8), CO_other (8), CO-OM_Cost-Center-Accounting (5), MM_other (4), LO_other (4), LE (4), MM-IM_Inventory-Management (3) |
| Grant | GM_GRANT_NBR | FIN (15), FI-GL_General-Ledger (14), MM-PUR_Purchasing (5), FI_other (5), PSM (3), PS_Project-System (2), MM_other (2) |
| Material / Product | MATNR, PRODUCTNUMBER | MM-PUR_Purchasing (44), LO-MD-MM_Material-Master (42), LO_other (38), SD_other (23), PP_other (23), CRM (17), CO_other (16), FI-GL_General-Ledger (13), SD-SLS_Sales (12), SCM (12) |
| Material Group | MATKL | MM-PUR_Purchasing (41), SD-SLS_Sales (11), SD_other (10), SD-BIL_Billing (6), LO-MD-BOM_Bill-of-Material (6), PM_other (5), PP-SFC_Shop-Floor-Control (4), LE (4), PP_other (3), MM-IM_Inventory-Management (2) |
| Personnel | PERNR_D | SD-SLS_Sales (13), FI-GL_General-Ledger (11), SD-BIL_Billing (9), LO_other (7), MM-PUR_Purchasing (5), FI_other (5), FIN (3), SD_other (2), PSM (2), MM_other (2) |
| Profitability Segment | RKEOBJNR_CHAR, RKEOBJNR_NUMC | SD-SLS_Sales (11), FI-GL_General-Ledger (6), SD-BIL_Billing (5), SD_other (4), MM-PUR_Purchasing (4), LE (4), MM-IM_Inventory-Management (2), FI_other (2) |
| Supplier | LIFNR, MD_SUPPLIER | MM-PUR_Purchasing (60), LO_other (27), SD-SLS_Sales (14), FI_other (12), SD-BIL_Billing (9), CO_other (8), FI-GL_General-Ledger (7), PP_other (6), LE (6), PP-SFC_Shop-Floor-Control (5) |
| Task List (routing) group | PLNNR | PP_other (15), PM_other (9), QM (6), PP-SFC_Shop-Floor-Control (5), CO_other (2) |
| WBS Element | PS_POSID, PS_POSID_EDIT, PS_PSP_PNR, PS_S4_PSPNR | CA (13), SD-SLS_Sales (12), CRM (12), PS_Project-System (11), PP_other (9), CO_other (9), SCM (7), MM-PUR_Purchasing (7), FIN (7), FI_other (6) |

## ORG

| Entity | Data element | Folder (số view) |
|---|---|---|
| Business Area | GSBER | SD-SLS_Sales (21), FI_other (19), SD_other (12), PP-SFC_Shop-Floor-Control (12), PM_other (7), MM-PUR_Purchasing (6), FIN (6), SD-BIL_Billing (5), PP_other (5), MM_other (4) |
| Chart of Accounts | KTOPL | FI-GL_General-Ledger (17), FI_other (9), FIN (6), CO_other (2), CA (2) |
| Company Code | BUKRS, FIS_BUKRS | FI_other (96), CA (77), FI-GL_General-Ledger (59), MM-PUR_Purchasing (57), FIN (32), LO_other (18), CO_other (18), RE (17), MM_other (16), CO-OM_Cost-Center-Accounting (14) |
| Controlling Area | FIS_KOKRS, KOKRS | FI-GL_General-Ledger (33), CO-OM_Cost-Center-Accounting (33), SD-SLS_Sales (20), CO_other (17), CRM (13), FI_other (11), PP-SFC_Shop-Floor-Control (10), PM_other (9), CA (9), SD_other (8) |
| Distribution Channel | VTWEG | SD-SLS_Sales (47), SD_other (30), SD-BIL_Billing (15), LO_other (15), FI-GL_General-Ledger (8), FI_other (7), LE (6), LO-MD-MM_Material-Master (4), PSM (2), FIN (2) |
| Division | SPART | SD-SLS_Sales (46), SD_other (27), LO_other (16), SD-BIL_Billing (15), FI-GL_General-Ledger (8), LE (7), FI_other (6), LO-MD-MM_Material-Master (2), FIN (2), EAM-OBJ_Technical-Objects (2) |
| Functional Area | FKBER | FIN (10), PP-SFC_Shop-Floor-Control (7), FI-GL_General-Ledger (7), PP_other (5), PM_other (5), MM-PUR_Purchasing (5), FI_other (5), PS_Project-System (4), CO-OM_Cost-Center-Accounting (4), LE (3) |
| Plant | WERKS_D | PP_other (95), QM (24), LO_other (24), MM-IM_Inventory-Management (22), LO-MD-MM_Material-Master (21), PP-MRP_MRP (19), MM-PUR_Purchasing (18), LE (18), PP-SFC_Shop-Floor-Control (15), FI-GL_General-Ledger (14) |
| Profit Center | PRCTR | FI_other (18), CRM (13), SD-SLS_Sales (12), FIN (10), SD_other (9), MM-PUR_Purchasing (8), PP-SFC_Shop-Floor-Control (7), CO_other (6), SD-BIL_Billing (5), PM_other (5) |
| Purchasing Organization | EKORG | MM-PUR_Purchasing (65), LO_other (12), LO-MD-BOM_Bill-of-Material (6), PM_other (5), PP_other (3), MM_other (3), CO_other (2) |
| Sales Group | VKGRP | CRM (31), SD_other (22), SD-SLS_Sales (22), LO_other (8), SD-BIL_Billing (6), LE (5), EAM-OBJ_Technical-Objects (2), CO_other (2) |
| Sales Office | VKBUR | CRM (31), SD_other (27), SD-SLS_Sales (22), LE (9), LO_other (8), SD-BIL_Billing (6), EAM-OBJ_Technical-Objects (2), CO_other (2) |
| Sales Organization | VKORG | SD-SLS_Sales (47), SD_other (33), CRM (32), SD-BIL_Billing (24), LO_other (18), FI_other (8), FI-GL_General-Ledger (8), LE (6), LO-MD-MM_Material-Master (4), CA (4) |
| Segment | FB_SEGMENT | FI-GL_General-Ledger (20), FIN (7), FI_other (5), PSM (2), EC (2), CO_other (2), CO-OM_Cost-Center-Accounting (2) |
| Shipping Point | VSTEL | LE (14), SD_other (10), SD-SLS_Sales (8), SD-BIL_Billing (5) |
| Storage Location | LGORT_D | MM-IM_Inventory-Management (14), SD-SLS_Sales (8), MM-PUR_Purchasing (8), SD_other (7), LE (7), SD-BIL_Billing (5), LO_other (5), LO-MD-MM_Material-Master (4), PP_other (3), QM (2) |
| Valuation Area | BWKEY | CO_other (14), LO-MD-MM_Material-Master (10), FI-GL_General-Ledger (10), MM-IM_Inventory-Management (4), LO_other (2), FI_other (2), FIN (2), CA (2) |

## CONFIG

| Entity | Data element | Folder (số view) |
|---|---|---|
| Fiscal Year | FIS_GJAHR_NO_CONV, GJAHR | FI-GL_General-Ledger (30), SD-SLS_Sales (22), FI_other (22), MM_other (21), CA (20), FIN (11), SD_other (8), MM-IM_Inventory-Management (8), CO_other (7), SD-BIL_Billing (5) |
| Incoterms | INCO1 | MM-PUR_Purchasing (27), SD-SLS_Sales (22), SD_other (10), SD-BIL_Billing (8), LO_other (5), LE (4), FI_other (2) |
| Movement Type | BWART | MM-IM_Inventory-Management (14), SD-SLS_Sales (5), LE (5), MM-PUR_Purchasing (4), PP_other (3), QM (2), PP-SFC_Shop-Floor-Control (2) |
| Payment Terms | DZTERM | SD-SLS_Sales (26), SD_other (16), SD-BIL_Billing (7), LO_other (5), FI_other (3), CA (3) |
| Sales Document Type | AUART | SD-SLS_Sales (24), SD_other (19), FI-GL_General-Ledger (6), PSM (2) |
| Tax Code | MWSKZ | MM-PUR_Purchasing (22), FI_other (21), SD-SLS_Sales (13), SD-BIL_Billing (12), CA (10), MM_other (7), LO_other (4), CRM (3), FIN (2) |
