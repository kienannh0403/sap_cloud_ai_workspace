# LE + TM — verified external (LE-SHP-GF, TM-FRM*)

Nguồn: xem `README.md` cùng thư mục. Trong catalog này: LE-SHP-GF nằm ở folder `LE`, TM-FRM* nằm ở folder `TM`
(cả hai top-level, không phải phân hệ ưu tiên Sheet1).

## Outbound Delivery (LE-SHP)

`I_OutboundDelivery` / `I_OutboundDeliveryItem` — released `LE-SHP-GF-2CL`, **có trong** `catalog_all.csv`.
`I_OverallProofOfDelivSts` / `I_ProofOfDeliveryStatus` có trong catalog nguồn nhưng field-level chưa verify.
**Không tìm thấy field released chuẩn nào cho "số tờ khai hải quan xuất khẩu" trên delivery** — coi đây là gap
thật (custom field/nhập tay), đừng tìm mãi giả định có view chuẩn.

## Transportation Management (TM embedded) — khác component, gắn chặt với Outbound Delivery

View đọc (read-only interface, released, `TM-FRM*`): `I_TransportationOrder_2` (header FO), `I_TransportationOrderItem_2`,
`I_TransportationOrderStop_2` (điểm dừng), `I_TransportationOrderStage_2` (chặng), `I_TransportationOrderBP_2`
(business partner, gồm carrier), `I_TransportationOrderEvent` (event). Tất cả **có trong** `catalog_all.csv`,
folder `TM`.

View ghi/action (behavior-enabled "TP", released `TM-FRM-FRO-2CL`): `I_FreightOrderTP`, `I_FreightOrderItemTP`,
`I_FreightOrderStopTP`, `I_FreightOrderStageTP`, `I_FreightOrderBPTP`, `I_FreightOrderDocRefTP` (candidate link
FO↔Delivery), `I_FreightOrderItemDocRefTP`. ⚠️ **Đối chiếu 2026-09-23: KHÔNG view nào trong nhóm TP này có trong
`catalog_all.csv`** — cùng giới hạn như write-BO của PIR (`PP.md`): catalog xlsx không có behavior
projection/TP, chỉ có CDS view đọc thường. Với nhu cầu ghi/action trên Freight Order, tra thẳng ADT/BDEF, đừng
tìm trong catalog này.

## Pattern ghi execution/check-in-out đã verify sống (EML)

Action **`ReportEvent`** trên BO **`I_FreightOrderTP`** (package `RAP_TM_FO_API`, entity root `FreightOrder`),
deep param **`D_TranspOrdReportEventP`**: `TranspOrdEventCode` (giá trị từ view released
**`I_TranspOrdEventCode_2`** — `EP_CHECK_IN`/`EP_CHECK_OUT`/`EP_ARRIVAL`/`EP_DEPARTURE`/`EP_LOAD_*`/`EP_UNLOAD_*`),
`TransportationOrderStopUUID` (optional), `TranspOrdEvtActualDateTime`, `TranspOrdEvtEstimatedDateTime`.

- **Key EML = `TransportationOrderUUID`** (RAW16), **KHÔNG phải** số FO (CHAR10) — phải map số FO
  (`I_TransportationOrder_2.TransportationOrder`) → UUID trước.
- **Kiểu datetime của TM = ABAP built-in `timestamp`** (domain `TZNTSTMPS`, DEC15,0) — **KHÔNG phải** `utclong`,
  **KHÔNG phải** `timestampl` (DEC21,7); cả hai đều bị ADT reject. Tách date/time bằng
  `CONVERT TIME STAMP ts TIME ZONE tz INTO DATE d TIME t` (ABAP) hoặc `tstmp_to_dats`/`tstmp_to_tims` **4 tham
  số** trong CDS (`ts, timezone, client, on_error` — bản 2 tham số báo lỗi "parameters 2 <> 4"). Field payload
  phải kiểu built-in `t`/`d` — data element `TIMS`/`DATS` **không được phép** trong class ABAP Cloud.
  **Bài học tổng quát: xác nhận kiểu ABAP built-in thật của field datetime bằng F2 trên data element trước khi
  viết code convert — đừng suy kiểu từ tên field.**
- **Cross-BO write trong save-phase là bất hợp pháp**: `MODIFY ENTITIES` + `COMMIT ENTITIES` sang một BO khác
  (vd từ trong determination của BO A gọi sang BO B) → lỗi `BEHAVIOR_STATEMENT_ILLEGAL` (cấm COMMIT ở đó). Phải
  chạy ở **LUW riêng, sau khi commit gốc** (background/async).

## Pattern đọc/flatten cho báo cáo (tham khảo app Fiori, KHÔNG select view app trực tiếp)

App "Manage Freight Orders" dùng view `C_FrtOrdManagement` — **không released**, không được select trực tiếp;
thay bằng association to-one **FILTER** trên view released:
- `_SourceStop` = `I_TransportationOrderStop_2` on UUID + `TranspOrdStopSequencePosition = 'F'` (điểm đầu);
  `_DestinationStop` = `= 'L'` (điểm cuối) → field `LocationId` (Plant xuất/nhận), `TranspOrdStopPlanTranspDteTme`.
- Biển số xe chính: `_AvrItem` = `I_TransportationOrderItem_2` on UUID + `TranspOrdItemCategory = 'AVR'`
  (Active Vehicle Resource) → `TranspEquipmentPlateNumber` (PVR=rơ-moóc, DRI=tài xế).

## Chưa xác định (đừng đoán tên view)

Container ID và "Means of Transport / biển số xe" ở mức resource/equipment: chưa tìm thấy view cụ thể trong lần
đọc nguồn này — cần tra riêng, không suy đoán tên `I_HandlingUnit*` hay tương tự cho tới khi xác nhận.
