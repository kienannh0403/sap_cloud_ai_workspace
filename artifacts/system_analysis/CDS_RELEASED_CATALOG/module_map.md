# Module map — component → folder

Generated 2026-09-21 by `build_catalog.py` (do not hand-edit).

## Cách gán (thứ tự ưu tiên; mỗi view thuộc đúng 1 folder)

1. **component** — component của view bằng hoặc nằm dưới component trong Sheet1 (vd `SD-SLS-SO` → `SD-SLS`). Độ tin cậy cao.
2. **alias** — Sheet1 ghi component không tồn tại trong file; gán sang component cùng nội dung, đã đối chiếu tên view: `PM-EQM-EQ*` → `EAM-OBJ`; `PM-EQM-FL*` → `EAM-OBJ`; `PPM-SCL*` → `PS`.
3. **keyword** — Sheet1 ghi component không tồn tại và không có alias; gán theo từ khoá trong tên view, chỉ trong `PP-*` (bỏ `PP-KAB*`): `PP-SFC`: /MANUFACTURINGORDER|PRODUCTIONORDER|PRODORD|CONFIRMATION|SHOPFLOOR|ORDEROPERATION/; `PP-MRP`: /MRP|PLANNEDORDER|PLNDORDER|PLNDINDEPRQMT|DEPDNTRQMT|DEPENDENTREQ|PLANNINGSTRATEGY|FORECAST/. **Suy luận, độ tin cậy thấp hơn.**
4. **top-level** — phần còn lại gom theo module gốc: `<TOP>_other` nếu module đó đã có folder ưu tiên, ngược lại folder tên `<TOP>`.

## Phân hệ ưu tiên (Sheet1) và kết quả

| Component (Sheet1) | Phân hệ | Folder | Số view |
|---|---|---|---:|
| FI-GL | General Ledger | FI-GL_General-Ledger | 233 |
| FI-AP | Accounts Payable | FI-AP_Accounts-Payable | 11 |
| FI-AR | Accounts Receivable | FI-AR_Accounts-Receivable | 23 |
| FI-AA | Asset Accounting | FI-AA_Asset-Accounting | 9 |
| CO-OM | Cost Center Accounting | CO-OM_Cost-Center-Accounting | 5 |
| MM-PUR | Purchasing | MM-PUR_Purchasing | 115 |
| MM-IM | Inventory Management | MM-IM_Inventory-Management | 73 |
| SD-SLS | Sales | SD-SLS_Sales | 191 |
| SD-BIL | Billing | SD-BIL_Billing | 34 |
| PP-SFC | Shop Floor Control | PP-SFC_Shop-Floor-Control | 23 |
| PP-MRP | MRP | PP-MRP_MRP | 71 |
| LO-MD-BOM | Bill of Material | LO-MD-BOM_Bill-of-Material | 9 |
| LO-MD-MM | Material Master | LO-MD-MM_Material-Master | 102 |
| EAM-WCM | Work Clearance Management | EAM-WCM_Work-Clearance-Management | 0 |
| EAM-OBJ | Technical Objects | EAM-OBJ_Technical-Objects | 28 |
| PS | Project System | PS_Project-System | 95 |

## Mọi component trong file

| Component | Số view | Folder | Cách gán |
|---|---:|---|---|
| AP-MD-BP | 18 | AP | top-level |
| AP-MD-BP-RAP | 25 | AP | top-level |
| BC-DOC-TTL | 2 | BC | top-level |
| BC-DWB-DIC | 2 | BC | top-level |
| BC-SEC-USR-ADM | 2 | BC | top-level |
| BC-SRV-ADR | 36 | BC | top-level |
| BC-SRV-APS-EXT-FLD | 3 | BC | top-level |
| BC-SRV-APS-IAM | 9 | BC | top-level |
| BC-SRV-ASF-FYV | 5 | BC | top-level |
| BC-SRV-ASF-UOM | 9 | BC | top-level |
| BC-SRV-BP | 2 | BC | top-level |
| BC-SRV-BSF-CUR | 10 | BC | top-level |
| BC-SRV-BUM | 2 | BC | top-level |
| BC-SRV-TIM-TZ | 8 | BC | top-level |
| CA-ATP | 1 | CA | top-level |
| CA-ATP-OVD | 2 | CA | top-level |
| CA-ATP-PAL | 26 | CA | top-level |
| CA-CL | 55 | CA | top-level |
| CA-CPD-SS | 1 | CA | top-level |
| CA-DMS | 33 | CA | top-level |
| CA-EPT-SUB | 2 | CA | top-level |
| CA-FL-SRV | 1 | CA | top-level |
| CA-GTF-CSC | 2 | CA | top-level |
| CA-GTF-CSC-EDO-CH | 2 | CA | top-level |
| CA-GTF-CSC-EDO-CO | 3 | CA | top-level |
| CA-GTF-CSC-EDO-GR | 1 | CA | top-level |
| CA-GTF-CSC-EDO-HU | 1 | CA | top-level |
| CA-GTF-CSC-EDO-IN-EW | 1 | CA | top-level |
| CA-GTF-CSC-EDO-IN-IV | 1 | CA | top-level |
| CA-GTF-CSC-EDO-IT | 2 | CA | top-level |
| CA-GTF-DF | 13 | CA | top-level |
| CA-GTF-FXU-FI-AR | 2 | CA | top-level |
| CA-GTF-FXU-FI-CO | 1 | CA | top-level |
| CA-GTF-GL-CAL | 20 | CA | top-level |
| CA-GTF-TRB | 1 | CA | top-level |
| CA-GTF-VDM | 11 | CA | top-level |
| CA-JVA | 38 | CA | top-level |
| CA-JVA-JVA | 1 | CA | top-level |
| CA-TS-S4 | 14 | CA | top-level |
| CA-WFD | 5 | CA | top-level |
| CA-WFD-BL | 9 | CA | top-level |
| CM-CAT | 2 | CM | top-level |
| CM-CTX | 1 | CM | top-level |
| CM-DOC | 9 | CM | top-level |
| CM-GF | 9 | CM | top-level |
| CM-LT | 31 | CM | top-level |
| CM-TSK | 1 | CM | top-level |
| CO-OM | 4 | CO-OM_Cost-Center-Accounting | component |
| CO-OM-CCA-AVC | 1 | CO-OM_Cost-Center-Accounting | component |
| CO-PC-ACT | 2 | CO_other | top-level |
| CO-PC-ML | 3 | CO_other | top-level |
| CO-PC-OBJ-ORD | 5 | CO_other | top-level |
| CO-PC-OBJ-PER | 2 | CO_other | top-level |
| CO-PC-PCP | 22 | CO_other | top-level |
| CRM-S4-ANA-CDS | 10 | CRM | top-level |
| CRM-S4-BF-CM | 4 | CRM | top-level |
| CRM-S4-REP-RFW | 90 | CRM | top-level |
| CRM-S4-SRV-SVO-FIO | 3 | CRM | top-level |
| EC-PCA-MD | 8 | EC | top-level |
| FI | 2 | FI_other | top-level |
| FI-AA | 3 | FI-AA_Asset-Accounting | component |
| FI-AA-IS | 6 | FI-AA_Asset-Accounting | component |
| FI-AP-AP-B | 8 | FI-AP_Accounts-Payable | component |
| FI-AP-AP-Q | 1 | FI-AP_Accounts-Payable | component |
| FI-AP-IS | 2 | FI-AP_Accounts-Payable | component |
| FI-AR-AR-C | 7 | FI-AR_Accounts-Receivable | component |
| FI-AR-IS | 16 | FI-AR_Accounts-Receivable | component |
| FI-CA | 283 | FI_other | top-level |
| FI-CA-INV | 23 | FI_other | top-level |
| FI-FIO-AP | 1 | FI_other | top-level |
| FI-FIO-GL-HIE | 6 | FI_other | top-level |
| FI-FM | 12 | FI_other | top-level |
| FI-GL-GL | 12 | FI-GL_General-Ledger | component |
| FI-GL-GL-A | 26 | FI-GL_General-Ledger | component |
| FI-GL-GL-AAC | 1 | FI-GL_General-Ledger | component |
| FI-GL-GL-F | 1 | FI-GL_General-Ledger | component |
| FI-GL-GL-N | 19 | FI-GL_General-Ledger | component |
| FI-GL-IS | 162 | FI-GL_General-Ledger | component |
| FI-GL-OC | 12 | FI-GL_General-Ledger | component |
| FI-LOC-AA | 4 | FI_other | top-level |
| FI-LOC-AA-RU | 4 | FI_other | top-level |
| FI-LOC-BUP | 1 | FI_other | top-level |
| FI-LOC-CIT | 2 | FI_other | top-level |
| FI-LOC-CM-CN | 8 | FI_other | top-level |
| FI-LOC-EPI-CN | 6 | FI_other | top-level |
| FI-LOC-FI-CH-QR | 1 | FI_other | top-level |
| FI-LOC-FI-CL | 2 | FI_other | top-level |
| FI-LOC-FI-IN | 2 | FI_other | top-level |
| FI-LOC-FI-JP | 5 | FI_other | top-level |
| FI-LOC-FI-KR | 7 | FI_other | top-level |
| FI-LOC-FI-MX | 4 | FI_other | top-level |
| FI-LOC-FI-PH | 3 | FI_other | top-level |
| FI-LOC-GAI-CN | 9 | FI_other | top-level |
| FI-LOC-LO-BR | 6 | FI_other | top-level |
| FI-LOC-LO-HR | 1 | FI_other | top-level |
| FI-LOC-LO-IN | 4 | FI_other | top-level |
| FI-LOC-SAF-PL | 1 | FI_other | top-level |
| FI-LOC-TIM-CN | 10 | FI_other | top-level |
| FI-LOC-TXS | 1 | FI_other | top-level |
| FI-LOC-VAT-GEN | 2 | FI_other | top-level |
| FI-RA | 36 | FI_other | top-level |
| FI-TXL-EXT | 9 | FI_other | top-level |
| FI-TXL-TGM | 3 | FI_other | top-level |
| FIN-CS-COR-MON | 12 | FIN | top-level |
| FIN-CS-EA | 2 | FIN | top-level |
| FIN-CS-MD | 294 | FIN | top-level |
| FIN-FSCM-CLM | 3 | FIN | top-level |
| FIN-FSCM-CLM-BAM | 6 | FIN | top-level |
| FIN-FSCM-COL | 8 | FIN | top-level |
| FIN-FSCM-CR | 23 | FIN | top-level |
| FIN-FSCM-DM | 15 | FIN | top-level |
| FIN-FSCM-FQM | 5 | FIN | top-level |
| FIN-FSCM-TRM | 125 | FIN | top-level |
| FIN-FSCM-TRM-CR | 6 | FIN | top-level |
| FIN-FSCM-TRM-MR | 5 | FIN | top-level |
| FIN-IE-FS | 10 | FIN | top-level |
| FS-CM | 3 | FS | top-level |
| FT-ITR-CLS | 1 | FT | top-level |
| LE-DSD | 10 | LE | top-level |
| LE-SHP-FIO-ANA | 1 | LE | top-level |
| LE-SHP-GF | 101 | LE | top-level |
| LE-TRA | 4 | LE | top-level |
| LO-AB | 33 | LO_other | top-level |
| LO-ARM | 11 | LO_other | top-level |
| LO-ARM-INS | 2 | LO_other | top-level |
| LO-GT-CHB | 9 | LO_other | top-level |
| LO-HU | 4 | LO_other | top-level |
| LO-MD-BOM | 9 | LO-MD-BOM_Bill-of-Material | component |
| LO-MD-BP | 48 | LO_other | top-level |
| LO-MD-MM | 102 | LO-MD-MM_Material-Master | component |
| LO-MD-PL | 4 | LO_other | top-level |
| LO-MD-SN | 14 | LO_other | top-level |
| LO-RFM-MD-ART | 1 | LO_other | top-level |
| LO-WTY-FIO | 32 | LO_other | top-level |
| MM | 60 | MM_other | top-level |
| MM-IM-GF | 13 | MM-IM_Inventory-Management | component |
| MM-IM-RS | 4 | MM-IM_Inventory-Management | component |
| MM-IM-VDM-PI | 24 | MM-IM_Inventory-Management | component |
| MM-IM-VDM-RSV | 3 | MM-IM_Inventory-Management | component |
| MM-IM-VDM-SGM | 29 | MM-IM_Inventory-Management | component |
| MM-IV-INT-WF | 1 | MM_other | top-level |
| MM-IV-LIV | 24 | MM_other | top-level |
| MM-PUR | 2 | MM-PUR_Purchasing | component |
| MM-PUR-ANA | 24 | MM-PUR_Purchasing | component |
| MM-PUR-GF-MAS | 2 | MM-PUR_Purchasing | component |
| MM-PUR-HUB-CTR | 5 | MM-PUR_Purchasing | component |
| MM-PUR-HUB-FND | 4 | MM-PUR_Purchasing | component |
| MM-PUR-HUB-PO | 6 | MM-PUR_Purchasing | component |
| MM-PUR-HUB-PR | 3 | MM-PUR_Purchasing | component |
| MM-PUR-HUB-RFQ | 10 | MM-PUR_Purchasing | component |
| MM-PUR-OA-CON | 5 | MM-PUR_Purchasing | component |
| MM-PUR-OA-SCH | 5 | MM-PUR_Purchasing | component |
| MM-PUR-PO | 14 | MM-PUR_Purchasing | component |
| MM-PUR-REQ | 12 | MM-PUR_Purchasing | component |
| MM-PUR-RFQ | 14 | MM-PUR_Purchasing | component |
| MM-PUR-SQ-QTA | 5 | MM-PUR_Purchasing | component |
| MM-PUR-SVC-SES | 4 | MM-PUR_Purchasing | component |
| PLM-WUI-OBJ-ECN | 3 | PLM | top-level |
| PM | 7 | PM_other | top-level |
| PM-EQM-EQ | 20 | EAM-OBJ_Technical-Objects | alias |
| PM-EQM-FL | 8 | EAM-OBJ_Technical-Objects | alias |
| PM-EQM-SF-MPC | 5 | PM_other | top-level |
| PM-EQM-SF-WA | 3 | PM_other | top-level |
| PM-PRM-MP | 12 | PM_other | top-level |
| PM-WOC-MN | 22 | PM_other | top-level |
| PM-WOC-MO | 20 | PM_other | top-level |
| PP-BD-WKC | 1 | PP_other | top-level |
| PP-FIO | 6 | PP-MRP_MRP | keyword |
| PP-KAB | 1 | PP_other | top-level |
| PP-KAB-VDM | 84 | PP_other | top-level |
| PP-MRP | 3 | PP-MRP_MRP | component |
| PP-PMR-ENG | 6 | PP-MRP_MRP | keyword |
| PP-VDM | 56 | PP-MRP_MRP | keyword |
| PP-VDM | 23 | PP-SFC_Shop-Floor-Control | keyword |
| PP-VDM | 93 | PP_other | top-level |
| PP-VDM-MD | 121 | PP_other | top-level |
| PPM-SCL-BIL | 31 | PS_Project-System | alias |
| PPM-SCL-DMN | 24 | PS_Project-System | alias |
| PPM-SCL-STR | 40 | PS_Project-System | alias |
| PSM | 13 | PSM | top-level |
| PSM-FM-BU | 2 | PSM | top-level |
| PSM-FM-IS | 2 | PSM | top-level |
| PSM-FM-MD | 4 | PSM | top-level |
| PSM-FM-UP | 8 | PSM | top-level |
| PSM-GM-GTE | 1 | PSM | top-level |
| PSM-GM-GTE-MD | 5 | PSM | top-level |
| QM | 3 | QM | top-level |
| QM-CA | 2 | QM | top-level |
| QM-IM | 73 | QM | top-level |
| QM-PT | 77 | QM | top-level |
| QM-QN | 18 | QM | top-level |
| RE-FX | 20 | RE | top-level |
| RE-FX-BD | 12 | RE | top-level |
| RE-FX-CN | 16 | RE | top-level |
| RE-FX-IP | 1 | RE | top-level |
| RE-FX-RA | 2 | RE | top-level |
| SCM-EWM-DLP | 11 | SCM | top-level |
| SCM-EWM-WOP | 30 | SCM | top-level |
| SD-ANA | 17 | SD_other | top-level |
| SD-ANA-SP | 5 | SD_other | top-level |
| SD-BF | 2 | SD_other | top-level |
| SD-BF-CM | 24 | SD_other | top-level |
| SD-BF-MD | 16 | SD_other | top-level |
| SD-BF-PD | 4 | SD_other | top-level |
| SD-BF-PR | 35 | SD_other | top-level |
| SD-BF-TX | 2 | SD_other | top-level |
| SD-BIL-GF | 16 | SD-BIL_Billing | component |
| SD-BIL-IL | 3 | SD-BIL_Billing | component |
| SD-BIL-IV-BP | 4 | SD-BIL_Billing | component |
| SD-BIL-IV-PC | 3 | SD-BIL_Billing | component |
| SD-BIL-PBD | 8 | SD-BIL_Billing | component |
| SD-CRF | 2 | SD_other | top-level |
| SD-CRF-ORG | 16 | SD_other | top-level |
| SD-MD-CM | 57 | SD_other | top-level |
| SD-MD-MM | 19 | SD_other | top-level |
| SD-SLS | 16 | SD-SLS_Sales | component |
| SD-SLS-CMR | 16 | SD-SLS_Sales | component |
| SD-SLS-GF | 86 | SD-SLS_Sales | component |
| SD-SLS-OA-CCO | 17 | SD-SLS_Sales | component |
| SD-SLS-OA-SCH | 9 | SD-SLS_Sales | component |
| SD-SLS-PBS | 5 | SD-SLS_Sales | component |
| SD-SLS-QUT | 11 | SD-SLS_Sales | component |
| SD-SLS-RE | 6 | SD-SLS_Sales | component |
| SD-SLS-SO | 25 | SD-SLS_Sales | component |
| SLC-ACT | 22 | SLC | top-level |
| SLC-CAT | 10 | SLC | top-level |
| SLC-EVL | 47 | SLC | top-level |
| SLC-SUP | 23 | SLC | top-level |
| SUS-INT | 27 | SUS | top-level |
| SUS-PFM-INT | 5 | SUS | top-level |
| TM | 57 | TM | top-level |
| TM-FRM | 18 | TM | top-level |
| TM-FRS | 1 | TM | top-level |
| TM-MD-ORG | 3 | TM | top-level |
