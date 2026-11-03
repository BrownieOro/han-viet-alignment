# Contract đầu ra — v1 (dùng chung cả nhóm)

**Một bài/đoạn = một thư mục. Không đặt tên theo khoảng trang.** Khoảng trang và nguồn nằm trong nguon.tsv.

```text
bai_lam/Tuan/CPO_03/B001_ten_bai/
├── dong_hang.tsv
├── dong_hang.xlsx
├── nguon.tsv
├── qa.tsv
├── mapping.tsv              # nếu có mapping; metadata, không phải cột dóng
├── chu_thich.tsv            # chú thích của nhóm
├── text/
│   ├── han.txt
│   └── viet.txt             # văn xuôi
│       # thơ: thay viet.txt bằng dich_am.txt, dich_nghia.txt, dich_tho.txt
└── ocr/                     # chỉ khi đã OCR
    └── boxes.json           # chữ thô/box; giữ riêng với text đã sửa
```

| Tệp | Quy định cố định |
|---|---|
| dong_hang.tsv | UTF-8, không tiêu đề; tab thật; mỗi hàng một đơn vị cùng nghĩa |
| dong_hang.xlsx | Sheet DONG_HANG; hàng 1 là tên cột; dữ liệu từ hàng 2 giống TSV |
| nguon.tsv | Có tiêu đề: Phiên bản, Nguồn, Trang PDF, Người dịch, Ghi chú |
| qa.tsv | Có tiêu đề: Hàng, Cờ tự động, Người kiểm; không có cờ chưa có nghĩa đã đúng |
| text/*.txt | Text đã sửa, từng phiên bản riêng, cùng thứ tự với hàng dóng |

Tool kèm mapping.tsv, chu_thich.tsv và annotations.json để nhóm kiểm tra/truy vết; các metadata này không thay đổi hai/bốn cột bắt buộc của file dóng. Không có mapping/chú thích thì các bảng metadata chỉ có tiêu đề.

**Văn xuôi:** đúng hai cột `Hán`, `Việt`.

**Thơ có đủ bản:** đúng bốn cột `Hán`, `Dịch âm`, `Dịch nghĩa`, `Dịch thơ`.

Không ID, tên bài, số trang, ghi chú trong cột dóng. Không ô gộp, công thức, hàng trống; không tab/xuống dòng trong một vế. Cho phép gộp câu để giữ nghĩa. Thơ thiếu bản: lưu riêng và ghi Cần hỏi, chưa xuất như bài đủ bốn bản.

Nguồn web phải được đối chiếu đúng bài và đúng bản dịch trong sách. Có thể kết hợp text web và OCR. Không tự tạo bản dịch bị thiếu. Không tính một hàng thơ thành ba cặp khi chưa được xác nhận.

Nút **Xuất gói bài theo contract** trong tool tạo các tệp cùng tên này trong một ZIP. Chữ text và bảng dóng lấy từ phiên bản đang biên tập; nhãn box giữ riêng. Điền nguồn rõ cho từng bản trong trường nguồn/ghi chú trước khi nộp. Nhận xét QA lưu riêng trong trình duyệt; output trong repo không bị tool sửa đè.

Khi gộp nộp: chỉ lấy bài đã kiểm/sửa, kiểm trùng và thống kê số cặp hợp lệ; thêm một báo cáo chung về số dòng/cặp, tự kiểm, nguồn và công cụ. Đây là quy ước nội bộ để làm thống nhất, áp dụng yêu cầu guideline và thông báo thơ bốn bản.
