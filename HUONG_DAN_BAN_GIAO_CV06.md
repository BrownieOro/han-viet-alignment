# CV06 — Quy ước bàn giao cho nhóm

Quy ước dưới đây áp dụng cấu trúc khuyến nghị của giảng viên và xác nhận bổ sung về thơ bốn bản. Thống nhất nguồn, bài và phạm vi giữa các thành viên trước khi gộp; số trang dưới đây là số thứ tự PDF, không nhất thiết là số in trên sách.

```text
CV06_<MA_TAC_PHAM>/
├── 01_nguon/
│   ├── han/
│   └── viet/
├── 02_ocr_tho/
│   ├── han/
│   └── viet/
├── 03_text_sach/
│   ├── han.txt
│   ├── viet.txt          # văn xuôi
│   ├── dich_am.txt       # thơ nếu có
│   ├── dich_nghia.txt    # thơ nếu có
│   └── dich_tho.txt      # thơ nếu có
├── 04_dong_hang/
│   ├── <MA_TAC_PHAM>_parallel.tsv
│   └── <MA_TAC_PHAM>_parallel.xlsx
└── README.md
```

- 01 và 02: giữ theo trang PDF, ví dụ `0001.png` và `0001.txt`. Nếu trang chứa nhiều phiên bản, ghi rõ trong README hoặc tách phiên bản sao cho không đè tên. Ghi nguồn text lấy từ mạng riêng, không gọi là OCR.
- 03: sau khi làm sạch và tổng hợp theo đúng thứ tự, dùng **một file cho mỗi bản**. Văn xuôi Hán–Việt thường có `han.txt` và `viet.txt`; thơ đủ bản có `han.txt`, `dich_am.txt`, `dich_nghia.txt`, `dich_tho.txt`. Không tự tạo bản dịch bị thiếu. File theo trang có thể giữ riêng làm trung gian để truy nguyên.
- 04: văn xuôi Hán–Việt xuất TSV và XLSX **hai cột Hán | Việt**; thơ đủ bốn bản xuất **Hán | Dịch âm | Dịch nghĩa | Dịch thơ**. Hai định dạng phải chứa cùng dữ liệu. Nếu một tập có cả hai loại thì giữ các bảng hai và bốn cột riêng, ghi phạm vi trong README; đây là cách tổ chức nhóm đề xuất, cần hỏi giảng viên nếu cần chốt tên file khi nộp.
- Mỗi hàng cần được kiểm tương ứng nội dung. Không coi việc xếp tự động hoặc OCR là đã kiểm. Với thơ thiếu bản, ghi rõ chưa có bản nào và hỏi giảng viên cách bàn giao/tính chỉ tiêu.
- README ghi tên nguồn/URL, người dịch nếu biết, trang PDF, người làm, công cụ/phương pháp, thống kê, phạm vi đã kiểm và hạn chế. Những chỗ không chắc phải được ghi lại.
- Các gói theo khoảng trang của từng người là dữ liệu trung gian; nhóm tổng hợp theo tác phẩm, loại văn bản và phiên bản trước khi dóng hàng. Khi trùng số trang giữa các nguồn khác nhau phải giữ thông tin nguồn để tránh đè file.

Tool xuất file tổng hợp theo từng bản trong mỗi gói khoảng trang, kèm file theo trang để truy nguyên. Nhóm vẫn cần gộp các gói theo đúng thứ tự và nguồn, kiểm nội dung chưa phân loại trước khi bàn giao. Nếu một trang chứa nhiều bản, gói trung gian giữ một ảnh và một OCR thô toàn trang; cấu trúc theo bản ở trên là cấu trúc tổng hợp cuối, không nên nhân bản OCR. Xem thêm `OUTPUT_CONTRACT.md` cho metadata kiểm tra.
