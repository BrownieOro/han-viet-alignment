# Cách lưu chung cho cả nhóm

## Mỗi bài một thư mục trong tên người làm

```text
bai_lam/Lam/                       # hoặc Tuan, Manh, Tran
├── theo_doi.tsv
└── CPO_03/
    └── B001_ten_bai/
        ├── nguon.tsv
        ├── goc/                  # text web ban đầu hoặc OCR thô
        ├── sach/                 # các bản text đã sửa
        ├── dong_hang.tsv
        └── dong_hang.xlsx
```

Chỉ tạo thư mục khi bắt đầu bài đó. Mã B001 tăng trong từng tác phẩm và người làm; đường dẫn có tên người nên không lẫn nhau. PDF nguồn lớn giữ ngoài Git, ghi link và trang trong nguon.tsv.

Text sạch: văn xuôi dùng han.txt và viet.txt; thơ dùng han.txt, dich_am.txt, dich_nghia.txt, dich_tho.txt theo các bản thực sự có. Không tự dịch thêm.

## File dóng

| Loại | Cột theo đúng thứ tự |
|---|---|
| Văn xuôi | Hán, Việt |
| Thơ đủ bốn bản | Hán, Dịch âm, Dịch nghĩa, Dịch thơ |

- TSV: UTF-8, không tiêu đề, phân cách tab thật, mỗi hàng một đơn vị nội dung.
- XLSX: sheet DONG_HANG, hàng đầu là tiêu đề trên; dữ liệu từ hàng 2 khớp TSV.
- Không thêm ID/tên bài/trang/ghi chú vào cột dóng; không ô gộp, công thức, dòng trống hoặc tab/xuống dòng trong một vế.
- Được ghép 1–n, n–1, n–m để giữ nghĩa; không chia theo số dòng máy móc.
- Thơ thiếu bản: lưu những bản có thật, ghi Cần hỏi; chưa gộp vào file bốn bản.

## Ghi nguồn và tiến độ

Copy [mau/nguon.tsv](mau/nguon.tsv) vào bài. Mỗi hàng ghi một phiên bản, link/tên file, trang PDF và người dịch nếu có. Text web phải đúng bài và đúng bản trong sách; không tính trùng với OCR.

Cập nhật theo_doi.tsv sau buổi làm. Số hàng nháp chưa phải số cặp hợp lệ. Ghi hàng lỗi và trang nguồn trong Ghi chú; người làm sửa rồi gửi kiểm lại.

Trạng thái: **Đang lấy text / Đang sửa / Đang dóng / Chờ kiểm / Cần sửa / Xong / Cần hỏi**. Chỉ ghi Xong sau khi kiểm và sửa lỗi cụ thể.

## Gộp nộp

Gộp phần Xong theo tác phẩm và loại đầu ra; kiểm trùng, TSV khớp XLSX, đủ text sạch, nguồn, OCR thô nếu có và báo cáo số cặp/số dòng/QA/công cụ. Chốt số cặp hợp lệ sau QA; thơ bốn bản thống kê riêng.
