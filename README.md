# Sách Hán–Việt

[Web](https://brownieoro.github.io/han-viet-alignment/) · [Phân công & tiến độ](https://docs.google.com/document/d/1svQTK-oO5F3AU4UTfdqMaXqJ1LDLaNN7C_ViSBzRsh8/edit?tab=t.0)

## Chạy và cấu hình

- Web dùng ngay, không cài đặt. Chọn sách hoặc **+ Input** để mở PDF/ảnh; file thêm chỉ ở trình duyệt, không tự push lên repo.
- OCR: chọn **Hán phồn thể / Tiếng Việt**, bố cục **tự động / Hán cột dọc**; chạy trang đang xem hoặc nhập khoảng **số trang PDF**. Kết quả là text thô, có thể sửa và tải `.txt`.
- OCR trên web dùng Tesseract.js; lần đầu cần mạng để tải core/mô hình. Chưa xác nhận chất lượng OCR Hán để chạy batch.
- Chạy local: cài Python 3, mở `MO_TOOL.cmd`, vào `http://127.0.0.1:7070/`. Cấu hình PaddleOCR tùy chọn: xem [hướng dẫn](cong_cu/README.md). [Giao diện nâng cao](https://brownieoro.github.io/han-viet-alignment/advanced.html) để thử box/dóng hàng.
- Mã giao diện: `index.html`; nút input/OCR: `quick_tools.js`. Ngôn ngữ, layout, đường dẫn worker/core nằm trong `quick_tools.js`.

## Lưu kết quả

Chưa có database chung. Push code, PDF mẫu, text và kết quả test vào repo; ghi nguồn/trang và cấu hình đi kèm. Giữ OCR thô riêng với text đã sửa. Ghi chú trên web lưu theo trình duyệt: xuất file rồi push nếu cần chia sẻ.

[Quy cách đầu ra](OUTPUT_CONTRACT.md) · [Mẫu tìm text](mau/TIM_TEXT.md) · [Mốc mapping tham khảo](MAPPING.tsv).

Sáu PDF nguồn nằm trong `inputs/`. Thư viện: [PDF.js](assets/pdfjs/LICENSE), [Tesseract.js](assets/tesseract/LICENSE.md).
