# Công cụ thử nghiệm (không bắt buộc)

Quy trình nhóm bắt đầu từ README ở thư mục gốc. Các script ở đây chỉ hỗ trợ thử OCR, chưa tự dóng hoàn chỉnh.

- Thử phân bố nhỏ: `python cong_cu/scan_all.py --sample --workers 2 --out data/sample`
- Tạo PDF mẫu đã ghép bản tương ứng: `python cong_cu/make_small_pdf.py`
- Xem kết quả thử: `python cong_cu/make_report.py --audit data/sample`

Nguồn PDF mặc định nằm ngoài repo tại ../source-inventory/. Môi trường OCR dùng Python 3.11 và requirements.txt trong thư mục này; tạo PDF cần thêm reportlab, đã có trên máy hiện tại.

run_full_scan.ps1 và update_report.py là công cụ cũ cho quét toàn bộ, chỉ dùng khi nhóm chủ động cần; không nằm trong quy trình mặc định. Đợt quét toàn bộ trước đã dừng.
