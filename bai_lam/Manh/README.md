# Phần dữ liệu của Mạnh

Toàn bộ dữ liệu đã được chuyển đổi từ các file `.md` gốc sang cấu trúc thư mục từng bài (`Bxxx_ten_bai/`) chuẩn `OUTPUT_CONTRACT.md` (giống định dạng `bai_lam/Tuan/`): mọi phiên bản của cùng một bài (Hán, Dịch âm, Dịch nghĩa, Dịch thơ) được **gộp chung trong 1 cặp `dong_hang.tsv` và `dong_hang.xlsx`** (sheet `DONG_HANG`), kèm `text/*.txt`, `nguon.tsv`, `qa.tsv`, `notes.xlsx` (kiểm bằng M.E.D Levenshtein) và `README.md`.

- **`CPO_03/` (*Ngô Thì Nhậm toàn tập 1*, `source_4.pdf`):** 44 bài (`B001`–`B031`: 31 bài văn xuôi 3 cột `Hán`/`Dịch âm`/`Dịch nghĩa`; `B032`–`B044`: 13 bài Phú 4 cột `Hán`/`Dịch âm`/`Dịch nghĩa`/`Dịch thơ`), tổng **1.603 hàng**. Toàn bộ 44 file `.md` gốc đã chuyển vào `done/CPO_03/`.
- **`CPO_04/` (*Thơ văn Phan Huy Ích 2*, `source_5.pdf`):** 75 bài thơ (`B001`–`B075`, 4 cột `Hán`/`Dịch âm`/`Dịch nghĩa`/`Dịch thơ`), tổng **722 hàng**. Toàn bộ 75 file `.md` gốc đã chuyển vào `done/CPO_04/`.
- **Tổng cộng:** **119 bài**, **2.325 hàng** dóng hàng. Chi tiết xem `TODO.tsv` và `notes.xlsx` trong từng thư mục.
