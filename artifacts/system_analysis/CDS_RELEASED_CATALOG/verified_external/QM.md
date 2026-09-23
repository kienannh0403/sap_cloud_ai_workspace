# QM — verified external (QM-QN, Quality Notification)

Nguồn: xem `README.md` cùng thư mục. Đối chiếu 2026-09-23: `I_QLTYNOTIFICATION` và `I_QUALITYNOTIFICATIONITEM`
**có trong** `catalog_all.csv` (folder `QM`, component `QM-QN`) — xác nhận catalog này **đã dùng đúng tên**.
`I_QUALITYNOTIFICATION` (tên trực giác, sai) **không có trong file** — khớp với phát hiện dưới đây.

## Bẫy tên view

Tên view thật là **`I_QltyNotification`** (viết tắt "Qlty"), **KHÔNG PHẢI** `I_QualityNotification` như trực
giác hay đoán. Verify từ source đã activate thật trên tenam khác, không phải suy luận.

## Field thật (verified, không đoán)

**`I_QltyNotification`** (header):
- Key/loại: `QualityNotification` (key), `NotificationType`
- Đối tượng: `Material`, `Batch`, `Customer`, `Supplier`, `ProductionOrder`, `OrderDocument` (số order tham
  chiếu — dùng làm link tới `I_SalesOrder`)
- Người/ngày: `CreatedByUser`, `CreationDate`, `LastChangedByUser`, `LastChangedDate`,
  `NotificationReportingDate`, `NotificationRequiredStartDate/EndDate`, `NotificationCompletionDate` (rỗng =
  chưa hoàn thành → suy trạng thái Open/Done)
- Text/phân loại: `NotificationText`, `NotificationCodeGroup`/`NotificationCodeID`/`NotificationCatalog`,
  `NotificationPriority`/`NotificationPriorityType`
- Số lượng: `NotificationComplaintQuantity`/`NotificationReferenceQuantity`/`NotificationInternalQuantity`/
  `NotifReturnDeliveryQuantity` + `NotificationQuantityUnit`
- Assoc: `_QltyNotificationHdrTask`

**`I_QualityNotificationItem`** (item — lưu ý tên item CÓ chữ "Quality" đầy đủ, khác header): `QualityNotification`,
`NotificationItem`, `NotificationItemText`, `Material`, `Batch`, `Plant`, `CompanyCode`, `PurchaseOrder`,
`OrderID`. Assoc: `_QltyNotificationCause`/`_QltyNotificationTask`/`_QltyNotificationActivity`/
`_NotifItmObjectPartCode`.

**Item là to-many theo QualityNotification** — KHÔNG select scalar field ở item trên view có grain=header
(gây fan-out → OData V4 "Duplicate key predicate"); lấy field ở header, hoặc qua assoc to-one riêng.

## Field SAI hay bị đoán nhầm — ĐỪNG DÙNG

`QualityNotificationType`, `QualityNotificationStatus`, `NotificationCreationDate`, `MalfunctionStartDate`,
`QualityNotificationCodeGroup`/`Code`, `ReportedByUser`, `SalesOrder` (trực tiếp trên notification — phải qua
`OrderDocument` + join, không có field tên `SalesOrder` thẳng).

## Liên quan

Tên sản phẩm: dùng `I_ProductText.ProductName` + filter `Language` — **KHÔNG phải** `I_ProductDescription`.
