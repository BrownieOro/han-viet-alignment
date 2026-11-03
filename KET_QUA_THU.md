# Kết quả thử phân bố trên cả sáu PDF

Đã OCR 33 trang mẫu trong phạm vi nội dung. Đây là rà soát bằng cờ heuristic, không phải đo tỷ lệ lỗi thật. Đợt quét 2.044 trang đang chạy riêng; xem tiến độ trong data/audit/review.html.

| Nguồn | Trang đã thử | Trang có cờ chất lượng | Trang cần kiểm thứ tự cột |
|---|---|---:|---:|
| CPO01_HAN | 14, 45, 80, 110, 136 | 0/5 | 5 |
| CPO01_VI | 17, 60, 120, 180, 228 | 5/5 | 0 |
| CPO02 | 19, 55, 100, 113, 140, 160 | 6/6 | 0 |
| CPO03 | 44, 209, 326, 520, 586, 740, 850 | 6/7 | 0 |
| CPO04 | 4, 25, 47, 90, 150 | 5/5 | 0 |
| CPO05 | 213, 270, 330, 390, 450 | 0/5 | 0 |

## Quyết định trước mắt

- Tang thương bản Hán: kiểm thứ tự cột dọc, không coi thứ tự text OCR hiện tại là đúng.
- Tang thương bản Việt, Hoàng Việt, Ngô Thì Nhậm, Phan Huy Ích: nhiều mẫu nghi mất dấu Việt; tìm text có sẵn hoặc thử công cụ Việt khác trước khi sửa hàng loạt.
- Hoàng Việt phần Hán và một số trang Phan Huy Ích: có cờ nhiều box confidence thấp, cần đối chiếu ảnh.
- Không có cờ vẫn phải kiểm tra nội dung. Báo cáo không chứng nhận cuốn nào đạt chất lượng.

Mở data/sample/review.html để xem từng trang mẫu; data/audit/review.html cho đợt quét toàn bộ.
