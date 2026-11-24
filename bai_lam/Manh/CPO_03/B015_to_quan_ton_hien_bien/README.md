# TỔ QUAN TÔN HIỂN BIỆN (祖官尊顯辨)

Bài văn xuôi (45 cặp Hán–Việt) thuộc *Ngô Thì Nhậm toàn tập 1* (`CPO_03`, `source_4.pdf`, bắt đầu từ trang PDF 859), phần dữ liệu của Mạnh. Nguồn gốc được giữ nguyên tại `bai_lam/Manh/done/CPO_03/to_quan_ton_hien_bien.md`.

Trạng thái hiện tại là **đã chuyển đổi và dóng hàng sơ bộ (3 cột (Hán, Dịch âm, Dịch nghĩa))** theo `OUTPUT_CONTRACT.md` và `guidelines.pdf`. Đã làm sạch rác OCR (số trang, tiêu đề chạy trang, ký hiệu chú thích, từ rớt dòng) và tách dóng theo nghĩa từng câu/đoạn. Cần người kiểm chéo đối chiếu lại ảnh `source_4.pdf` cho các vị trí chữ Hán khuyết do OCR (ghi rõ trong `qa.tsv`) trước khi chốt hoàn thành.

Đã gộp đủ 3 bản (`han.txt`, `dich_am.txt`, `dich_nghia.txt`) vào chung `dong_hang.tsv/.xlsx` (3 cột `Hán`, `Dịch âm`, `Dịch nghĩa`), kiểm Hán–Dịch âm bằng M.E.D Levenshtein và xuất `notes.xlsx`.
