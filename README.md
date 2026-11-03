# Nhóm Hán–Việt: bắt đầu ở đây

## Bây giờ mỗi người làm gì?

1. Nhận phần sách đã chia trong Docs. Chọn **một bài hoặc đoạn ngắn** để làm trước.
2. Tìm text của đúng bài trên Thi Viện/nguồn khác. So với PDF: đúng bài, đúng bản dịch thì dùng; thiếu bản nào mới OCR bản đó.
3. Mở PDF cạnh text OCR, sửa chữ sai và bỏ số trang/chú thích. Lưu riêng Hán, dịch âm, dịch nghĩa, dịch thơ; văn xuôi chỉ cần Hán và Việt.
4. Ghép các câu/đoạn cùng nghĩa trong cùng bài. Thơ đủ bốn bản thì đủ bốn cột. Không ghép theo số dòng một cách máy móc.
5. Đổi phần cho bạn kiểm, sửa lỗi rồi mới tính vào số cặp hợp lệ và gộp nộp.

**Không cần kiểm kê xong hết sách mới bắt đầu. Làm cuốn chiếu theo bài.**

## Phần nào máy làm, phần nào làm tay?

| Công việc | Máy hỗ trợ | Người phải xác nhận |
|---|---|---|
| Đọc PDF | Đếm, render từng trang, OCR, giữ bbox và confidence | Đúng tác phẩm/phạm vi, các bản tương ứng |
| Tìm text web | Có thể tìm/lấy text | Đúng bản dịch và đủ nội dung như PDF |
| Sửa OCR | Đánh dấu confidence thấp, ít text, nghi mất dấu | Chữ Hán/Việt đúng theo ảnh; đặc biệt tên riêng và số |
| Tách các bản | Có thể dùng nhãn/bố cục làm gợi ý | Ranh giới bài, Hán/âm/nghĩa/thơ, bỏ đúng chú thích |
| Dóng câu | Có thể gợi ý ghép sau khi tách đúng bài | Hai/bốn vế cùng nội dung, gộp/tách khi dịch khác cấu trúc |
| Đóng gói | Kiểm số cột, dòng trống, trùng, TSV khớp XLSX | Nội dung đúng và lỗi đã sửa |

Script hiện tại **quét OCR và khoanh vùng cần xem**, chưa tự dóng cả sách. Không cần gõ lại mọi trang từ đầu; sửa trên text máy nhận dạng.

## Quét toàn bộ 6 PDF

Trên máy đang làm, từ thư mục repo:

```powershell
python -X utf8 scan_all.py --workers 6
```

Mặc định đọc 6 file `source_1.pdf` đến `source_6.pdf` trong thư mục `../source-inventory/`. Có thể đổi bằng `--sources DUONG_DAN`. Lần đầu tải mô hình nếu máy chưa có; yêu cầu Python 3.11 và các thư viện trong requirements.txt. Cấu hình đã chạy dùng CPU, không yêu cầu GPU.

- `data/audit/pages/<nguồn>/<trang>.json`: mọi box/text/confidence của từng mô hình; giữ nguyên.
- `data/audit/pages/<nguồn>/<trang>.txt`: bản xem nhanh, chưa phải text sạch.
- `data/audit/all_pages.csv`: tất cả trang đã xử lý.
- `data/audit/review_pages.csv`: trang có dấu hiệu cần xem.
- `data/audit/summary.json`: tiến độ và số trang theo nguồn.

Script tự lưu sau mỗi trang, cập nhật báo cáo mỗi 25 trang. Chạy lại sẽ bỏ qua trang đã thành công. Có thể thử nhỏ bằng `--limit 2 --out data/smoke`.

## Hiểu đúng các cờ

| Cờ | Làm gì tiếp |
|---|---|
| RAT_IT_TEXT | Mở ảnh: trang trắng/bìa thì bỏ khỏi nội dung; có chữ mà OCR ít thì chạy lại/chỉnh ảnh |
| NHIEU_BOX_CONF_THAP / CONF_TRUNG_BINH_THAP | Đối chiếu và sửa các box yếu; confidence không phải tỷ lệ lỗi thật |
| NGHI_MAT_DAU_VIET | So bản Việt với ảnh, tìm text sẵn trước khi gõ lại |
| CAN_XEP_THU_TU_COT_DOC | Kiểm thứ tự cột Hán; thứ tự y/x chỉ là bản xem nhanh, có thể sai |
| OCR_FAILED | Xem lỗi, sửa môi trường/ảnh rồi chạy lại |

Các ngưỡng là heuristic cho rà soát, **không đo CER, không phát hiện hết lỗi chữ/nghĩa**. Trang ngoài phạm vi tác phẩm cũng được quét để không bỏ sót file; cờ ở bìa/mục lục không tự động có nghĩa dữ liệu hỏng. Bản xem nhanh trộn kết quả hai mô hình theo bbox có thể bỏ/gộp nhầm dòng, luôn giữ raw_by_model để tra lại.

## Nguồn và phạm vi

| Mã quét | File | Trang PDF |
|---|---|---:|
| CPO01_HAN | Tang thương ngẫu lục, Hán | 138 |
| CPO01_VI | Tang thương ngẫu lục, Việt | 237 |
| CPO02 | Hoàng Việt văn tuyển | 166 |
| CPO03 | Ngô Thì Nhậm toàn tập 1 | 882 |
| CPO04 | Thơ văn Phan Huy Ích 2 | 160 |
| CPO05 | Tổng tập văn học Việt Nam 1 | 461 |

Tổng 2.044 trang, không phải 2.044 trang nội dung hay số cặp hợp lệ. PDF, OCR đầy đủ và dữ liệu máy nằm ngoài Git để không đẩy tài liệu nguồn lên mạng.

## Tham khảo pipeline trước

Đã thử https://github.com/tien02/SinoViet-Corpus ở commit `2fd25d8708e7cf583e912fcbf1042bbad1195d4a`. Repo này dùng cấu hình Đại Nam Thực Lục, không phù hợp để chạy nguyên lệnh all cho sách nhóm mình. Repo riêng này viết công cụ audit CPU cho dữ liệu CPO, không chép toàn bộ repo tham khảo. Mẫu trước gồm tám câu thơ đã sửa/dóng thủ công; không được coi là bằng chứng dóng tự động thành công.
