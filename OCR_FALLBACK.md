# Khi OCR không trả kết quả

## Thứ tự xử lý

1. Kiểm tra PDF có text có thể chọn được không. Nếu có, lấy text đó và vẫn đối chiếu ảnh.
2. Tìm đúng bài trên Thi Viện hoặc nguồn Hán Nôm khác theo tiêu đề Hán, tên tác giả và câu mở đầu.
3. So khớp tiêu đề, số câu, bản dịch và người dịch với PDF. Ghi URL vào `nguon.tsv`.
4. Nếu nguồn mạng khớp, dùng text mạng làm bản nháp rồi kiểm từng dòng với PDF.
5. Nếu không có nguồn mạng, OCR từng trang thay vì chạy cả khoảng dài.
6. Khi Gemini báo timeout hoặc quá tải, đổi model một lần, giảm độ phân giải ảnh và thử lại sau. Không coi timeout là kết quả rỗng.
7. Trang vẫn không đọc được thì ghi vị trí vào `qa.tsv` và giữ ảnh/PDF để người khác kiểm thủ công.

## Quy tắc dữ liệu

- Không ghi đè text đã sửa bằng kết quả OCR mới.
- Lưu OCR thô riêng trong `ocr/`.
- Text dùng để dóng hàng nằm trong `text/`.
- Ghi rõ bản nào lấy từ PDF, bản nào lấy từ website.
- Không chép bản dịch trên mạng vào output nếu chưa xác nhận nó là đúng bản trong sách.
- Khi không chắc chữ Hán, giữ nguyên trạng thái cần kiểm và không tự đoán.
