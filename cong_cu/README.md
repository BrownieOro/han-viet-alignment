# Backend local (tùy chọn)

Chỉ mở màn chính: chạy `MO_TOOL.cmd`, không cần cài thêm thư viện Python.

Backend PaddleOCR cho giao diện nâng cao đang thử nghiệm. Dùng Python 3.11 và môi trường riêng:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r cong_cu/requirements.txt
.venv\Scripts\python cong_cu/serve_review.py
```

Mở http://127.0.0.1:7070/advanced.html. Backend chỉ nghe trên máy, port 7070. Đóng server cũ trước khi chạy server trong môi trường riêng. Mô hình Paddle tải ở lần đầu; cấu hình engine tại `input_api.py`. Đây là OCR nháp, cần test/sửa trước khi chạy nhiều trang.

`build_ui.py` gộp các module `ui/` vào `advanced.html`; không tạo lại giao diện chính.
