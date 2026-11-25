# Hướng dẫn sử dụng CV06

Chạy `python3 cong_cu/serve_review.py` tại thư mục dự án, mở http://127.0.0.1:7070/. Để dừng server, nhấn Ctrl+C ở cửa sổ đang chạy.

1. Chọn mã CPO, người làm, PDF và khoảng trang theo số trên trình xem PDF. Tên bài/phần và đường dẫn nguồn có thể bổ sung nếu biết. Một lượt dùng một PDF; khi đổi nguồn, xuất gói trước để lưu công việc.
2. Chạy OCR một trang hoặc khoảng trang. Gemini mặc định đọc toàn trang, kể cả khi trang có nhiều bản; thông thường mỗi trang dùng một request, nhưng retry hoặc chạy lại sẽ phát sinh thêm request. Các lựa chọn ngôn ngữ/bố cục vẫn áp dụng cho Tesseract và voting. OCR là bản thô, chưa được kiểm.
3. Bấm **Xuất 01 + 02** để lưu ảnh từng trang, OCR thô, README và `du_an.json`. Mở lại dự án bằng cách giải nén ZIP rồi chọn `du_an.json`. Nên xuất thường xuyên, nhất là trước khi đóng hoặc tải lại trang.
4. Chọn **Tiếp tục làm sạch**. Với từng trang, xem ảnh và sửa từng phần Hán, Việt, dịch âm, dịch nghĩa, dịch thơ. Quy tắc tách bản chỉ gợi ý: kiểm cả mục **Chưa phân loại** và **Chú thích / khảo dị**; chuyển chính văn về đúng bản, loại thông tin không thuộc chính văn sau khi đối chiếu. Chỉ đánh dấu đã kiểm khi thực sự đã xem toàn trang.
   Chỗ bị che, không đọc rõ hoặc không đủ căn cứ xác định thì ghi `[MASK]`, không tự đoán. Giữ OCR thô nguyên vẹn.
5. Xuất **01 + 02 + 03**. Trong `03_text_sach`, các file tổng hợp theo phiên bản chỉ chứa nội dung đã phân loại; file theo trang nằm trong `theo_trang/` để truy nguyên. Phần chưa phân loại và phần chú thích được lưu riêng trong gói, không tự nhập vào bản sạch. Cần kiểm nội dung và nối câu ngắt trang khi tổng hợp.
6. Sau khi có đủ bản tương ứng, mở trang **Dóng hàng**. Chọn văn xuôi hai cột hoặc thơ bốn cột, đưa text của từng bản vào, tách dòng rồi tạo gợi ý. Gợi ý Gemini xử lý từng khối tối đa 60 dòng mỗi bản; nạp vào bảng và đối chiếu, sửa thủ công trước khi xuất TSV và XLSX. Đây là gợi ý, không bảo đảm đúng nghĩa.

Key mặc định được đọc từ file `.gemini_api_key` ở thư mục dự án; file này không được đưa lên Git. Giao diện cũng cho nhập một key tạm thời. Danh sách `gemini_keys.txt` được bỏ qua bởi Git nhưng tool hiện **chưa tự đọc hoặc tự chuyển** giữa các key trong file đó. Kiểm tra gói và hạn mức của project trong Google AI Studio.

Không tự tạo bản dịch thiếu. Ghi nguồn, phạm vi, người làm và tình trạng kiểm trong README. Hướng dẫn cấu trúc cuối cùng xem `HUONG_DAN_BAN_GIAO_CV06.md`.
