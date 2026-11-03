# Sách Hán–Việt

**Mở trang: https://brownieoro.github.io/han-viet-alignment/**

1. Chọn sách và số trang. Dùng **+ Input** bên cạnh để thêm PDF/ảnh của mình (trên máy, không tự upload lên GitHub). Sáu PDF đã có sẵn trong repo, không cần tải lên lại.
2. Tự điền người làm và bài/phần/trang đang nhận.
3. Ghi chú chỗ cần xem; chỉ mở Mapping nếu cần nối sang bản ở trang/file khác.

Không có tên thành viên hay phần việc gán cứng trên giao diện chính. Ghi chú lưu trên trình duyệt; dùng Xuất/Nhập ghi chú để gửi nhau. Chưa có đồng bộ ghi chú online.

- [Quy cách đầu ra chung](OUTPUT_CONTRACT.md).
- [Công cụ nâng cao](https://brownieoro.github.io/han-viet-alignment/advanced.html): OCR/box/dóng/kiểm dữ liệu; OCR cần chạy local bằng MO_TOOL.cmd.
- [Mẫu tìm text](mau/TIM_TEXT.md): có thể ghi trực tiếp trong HTML, không cần điền trùng.
- [Các mốc mapping đã kiểm](MAPPING.tsv).

Nguồn PDF nằm trong inputs/. Thư viện hiển thị PDF dùng Mozilla PDF.js, giấy phép tại assets/pdfjs/LICENSE. Dùng web online để đọc sách và ghi chú; mở MO_TOOL.cmd nếu cần OCR chạy trên máy.

## Làm gì và hạn nào?

Mở [VIEC_CAN_LAM.md](VIEC_CAN_LAM.md): 4 việc tự nhận; 05/11 chốt mẫu input/OCR và đầu ra, 07/11 có đợt text đầu, 09/11 chốt bài thử, 11/11 kiểm chéo. Đây là mốc nội bộ.

## OCR ở đâu?

Ngay dưới trang sách: chọn Hán/Việt → Chạy OCR → text hiện trong ô Kết quả. OCR một trang trên trình duyệt bằng Tesseract.js; lần đầu tải mô hình. Nút Kết quả đã thử mở text PaddleOCR cũ, có ghi rõ nguồn, không giả làm kết quả của trang đang xem. Cần kiểm lại chữ sau OCR.

Tesseract.js: https://github.com/naptha/tesseract.js, giấy phép tại assets/tesseract/LICENSE.md. Mô hình/core được tải từ CDN; ảnh xử lý trên trình duyệt.
