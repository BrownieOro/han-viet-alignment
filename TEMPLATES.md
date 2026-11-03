# Cuối cùng dùng template nào?

Chỉ có **3 mẫu cần điền**, tùy việc đang làm. Không phải mỗi bài làm đủ cả ba ngay từ đầu.

| Đang làm gì? | Dùng mẫu nào? | Điền gì? |
|---|---|---|
| Tìm text trên mạng | `bai_lam/Ten/TIM_TEXT.md` | Tên bài, link/người dịch, trang PDF nếu biết, dán các bản tìm được. Có bản nào ghi bản đó. Một người dùng một file, thêm mục cho từng bài. |
| Theo dõi công việc | `bai_lam/Ten/theo_doi.tsv` | Một dòng mỗi bài: đang làm tới đâu, đường dẫn, số hàng và vấn đề cần hỏi. Chưa biết số hàng thì để trống. |
| Chốt nguồn cho bài đã xử lý | `mau/nguon.tsv` | Phiên bản, link/tên file, trang PDF, người dịch và ghi chú; lưu cùng bài. Khi xuất gói bằng tool, kiểm lại nguon.tsv được sinh từ thông tin đã nhập, bổ sung từng bản nếu nguồn khác nhau. |

**Dùng HTML thì nhập các thông tin tương ứng trong tool, không phải nhập lại vào template chỉ để đủ file.** Cần đưa dữ liệu về repo thì xuất gói bài hoặc bản sao và lưu đúng phần người làm. Mẫu Markdown/TSV dành cho người tìm nguồn/làm ngoài tool.

## Các thứ còn lại không phải form bắt ai điền thêm

- `MAPPING.tsv`: đã có các mốc đối chiếu. Chỉ bổ sung khi Hán/Việt nằm xa nhau hoặc khác thứ tự; ghi Cần xác nhận nếu chưa chắc. Không dịch hay tự ghép câu ở bước này.
- `OUTPUT_CONTRACT.md`: quy cách đầu ra thống nhất, không phải báo cáo phải viết.
- `dong_hang.tsv`, `dong_hang.xlsx`, `text/`, `qa.tsv`: tool xuất từ dữ liệu đã nhập và đánh giá của người kiểm. Tự động kiểm định dạng không thay kiểm nghĩa.
- Báo cáo nộp: **một báo cáo chung của nhóm**, tổng hợp sau; không yêu cầu mỗi bài viết một báo cáo riêng.

## Luồng ngắn nhất

**Tìm bài → ghi TIM_TEXT → nhận xử lý trong tool → sửa/dóng → kiểm chéo → xuất gói bài.** Cập nhật theo dõi khi tiến độ thay đổi. Chưa cần OCR nếu đã tìm được đúng text và đúng bản.
