# Nhóm Hán–Việt — bắt đầu ở đây

**Chưa rõ cần điền gì? Mở [TEMPLATES.md](TEMPLATES.md): 3 mẫu cần dùng theo từng việc.** Không cần tạo đủ mọi tệp ngay khi chỉ đang tìm text.

**Đang tìm text trên mạng?** Mỗi người chỉ điền một file `bai_lam/Ten/TIM_TEXT.md` đã tạo sẵn: tên bài, link, trang và dán các bản tìm được. Chưa cần tách thành nhiều file. Xem [cách xác nhận bản xa nhau](TIM_TEXT_VA_MAPPING.md) và [mapping điền sẵn](MAPPING.tsv). Chỉ áp dụng contract đóng gói khi đã xử lý xong bài.

## Dùng tool HTML

**Contract đã chốt:** [OUTPUT_CONTRACT.md](OUTPUT_CONTRACT.md). Trong bài, nút “Xuất gói bài theo contract” tạo ZIP gồm bảng TSV/XLSX, nguồn, QA và text sạch.

**Có sẵn 6 PDF và OCR một ảnh:** mở MO_TOOL.cmd → mục Input. Chọn PDF/trang hoặc tải một ảnh, chọn Hán/Việt rồi OCR. Kết quả tạo bài mới cùng box để sửa; không tự coi là dữ liệu đã dóng đúng. OCR chạy trên máy, cần môi trường PaddleOCR đã cài; HTML mở riêng vẫn dùng biên tập nhưng không chạy OCR.

**Mở [index.html](index.html) bằng trình duyệt. Không cần cài gì.**

Đây là một file HTML duy nhất, đã gộp toàn bộ mã giao diện; có nút Tạo bài/Dán dữ liệu, Nhập TSV/Excel và Nhập thư mục ngay đầu trang. Chép riêng index.html sang máy khác vẫn dùng được. Muốn tự đọc output trong repo mỗi 15 giây thì mở MO_TOOL.cmd; HTML mở riêng vẫn cần chọn file/thư mục.

Chọn tên → chọn phần sách → Thêm bài → nhập/dán dữ liệu → xuất TSV hoặc Excel .xlsx. Tool có sẵn phân công, trạng thái và chỗ ghi nguồn/lỗi. Dữ liệu tự lưu trên trình duyệt hiện tại; dùng Xuất/Nhập bản sao JSON để chuyển máy hoặc gửi nhóm. Chưa có đồng bộ trực tuyến. Khi nhập, ID bài đã có được bỏ qua, không ghi đè; giữ riêng bản nhận kiểm nếu cần đối chiếu thay đổi.

Các file bên dưới vẫn dùng được nếu nhóm thích làm bằng Excel/thư mục.

### Gán chữ trực tiếp trên box ảnh

Mở một bài → phần **Ảnh nguồn & box chữ** → thêm ảnh trang/crop (PNG/JPG…). Kéo để vẽ box, chọn box rồi gán Hán/âm/nghĩa/thơ hoặc chú thích. Có thể kéo box, đổi kích thước góc dưới phải, sửa chữ, xóa box và đưa chữ vào hàng dóng chỉ định.

Nút Nhập JSON OCR nhận kết quả bbox/text của scanner cũ hoặc nhãn box xuất từ tool. Chọn đúng ảnh trang và loại nội dung trước khi nhập OCR. Ảnh lưu trong IndexedDB trên máy; box/chữ nằm trong bản sao JSON. Chuyển máy phải gửi thêm ảnh và chọn lại ảnh cùng tên. Bản này chưa mở PDF trực tiếp; dùng ảnh trang/crop. Nhãn và quan hệ dịch vẫn cần người kiểm.

1. Mở **[PHAN_CONG.tsv](PHAN_CONG.tsv)** bằng Excel, tìm tên mình và chọn một bài trong phần được giao.
2. Tìm text đúng bài trên Thi Viện/nguồn khác, đối chiếu PDF. Bản nào thiếu mới OCR bản đó.
3. Sửa text, dóng các bản cùng nghĩa và lưu vào thư mục tên mình trong **[bai_lam](bai_lam)**.
4. Cập nhật theo_doi.tsv của mình, đổi người kiểm rồi sửa lỗi.

**Làm từng bài đến xong. Không kiểm kê hết sách trước, không OCR hàng loạt.**

| Chỗ mở | Dùng để làm gì |
|---|---|
| [PHAN_CONG.tsv](PHAN_CONG.tsv) | Phần sách, trang PDF và người kiểm từng người |
| [QUY_UOC.md](QUY_UOC.md) | Cách lưu nguồn, text và file dóng chung |
| [bai_lam](bai_lam) | Bốn thư mục đã tạo sẵn |
| [mau](mau) | Mẫu ghi nguồn và tám hàng thơ bốn bản đã dóng thủ công |
| [tai_lieu](tai_lieu) | Kết quả thử, nguồn và hướng dẫn công cụ khi cần |
| cong_cu/ | Script thử nghiệm; không cần chạy để bắt đầu làm bài |

## Người làm và người kiểm

Mỗi người tự lấy text → sửa → dóng phần mình. Máy hỗ trợ OCR và gợi ý; người xác nhận đúng bản, sửa chữ sai và kiểm cùng nghĩa.

**Lâm kiểm Tuấn; Tuấn kiểm Mạnh; Mạnh kiểm Trân; Trân kiểm Lâm.** Chủ phần sửa lỗi của mình.

Phần ban đầu khoảng 412–434 trang/người, chưa bảo đảm công sửa bằng nhau. Cân lại bằng số cặp hợp lệ và công sửa thực tế; chuyển nguyên bài cùng các bản và ghi lại trong bảng phân công.

Mục tiêu mỗi người tối thiểu 2.000 cặp hợp lệ, nhóm 8.000 theo thông báo. Thơ bốn bản thống kê riêng, chưa tự quy đổi một hàng thành ba cặp. **Hạn nộp: nhóm điền.**

[Docs kế hoạch chung](https://docs.google.com/document/d/1svQTK-oO5F3AU4UTfdqMaXqJ1LDLaNN7C_ViSBzRsh8).
