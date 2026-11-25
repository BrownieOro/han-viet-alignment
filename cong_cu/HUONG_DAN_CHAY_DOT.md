# Chạy OCR theo đợt có lưu tiến độ

Đây là công cụ dòng lệnh dành cho người vận hành xử lý nhiều trang; giao diện web vẫn dùng theo `HUONG_DAN_CV06.md`. Cần Python 3 và `pdfinfo`, `pdftoppm` (Poppler). Cấu hình `gemini_keys.txt` tại thư mục dự án, mỗi dòng một key; nếu dòng có nhãn, phần cuối sau khoảng trắng là key. File này bị Git bỏ qua; không đưa key hoặc log chứa key vào kho.

```bash
python3 cong_cu/ocr_checkpoint.py --pdf inputs/source_4.pdf \
  --output bai_lam/Tran/vi_du --start 520 --end 525 \
  --work CPO_03 --section 'Nghi Luan 520-525'
node cong_cu/tao_nhap_cv06.js bai_lam/Tran/vi_du
```

Ảnh và OCR được ghi theo từng trang; chạy lại đúng lệnh sẽ bỏ qua trang đã có đủ ảnh và text, tiếp tục trang thiếu. Không đổi nguồn, phạm vi hoặc thông tin đợt trong cùng thư mục. Có thể thêm `--skip 522 524` sau khi xem nguồn để bỏ qua các trang chỉ có nội dung ngoài phạm vi. Dịch vụ có thể tính request lỗi hoặc request timeout; không có bảo đảm chính xác một request thành công cho mỗi trang.

Với trang chứa ranh giới phân công, thêm `--review 586` để giữ toàn bộ OCR của trang trong mục chưa phân loại, không tự nhập vào bản sạch. Sau khi kiểm ranh giới, chỉ chuyển phần thuộc phạm vi của mình vào dự án.

Khi key gặp lỗi quyền hoặc hạn mức, chương trình thử key tiếp theo; lỗi quá tải/kết nối được thử lại giới hạn rồi dừng an toàn. Chương trình không biết trạng thái thanh toán, nên mỗi thành viên cần xác nhận key thuộc project có gói phù hợp. `nhat_ky.jsonl` ghi số thứ tự key và trạng thái, không ghi key. Bản tách ở 03 là bản nháp, còn có thể thiếu hoặc lẫn tiểu dẫn, chú thích, bản tiếp nối; phải kiểm `can_phan_loai`, `ghi_chu_phan_loai` và đối chiếu ảnh. Không ghi đè dự án đã tồn tại hoặc bản sửa thủ công.
