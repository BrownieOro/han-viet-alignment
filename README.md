# Tool Hán–Việt

**Mọi người clone/tải repo về rồi chạy local nha. Web online chỉ để xem nhanh, mở PDF/OCR dễ lag.**

## Chạy local

1. Cài Python 3 (Windows nhớ chọn Add Python to PATH).
2. Mở `MO_TOOL.cmd`, giữ cửa sổ đó chạy. Vào http://127.0.0.1:7070/.
3. Chọn sách có sẵn hoặc **+ Input** để thêm PDF/ảnh.
4. Chọn Hán phồn thể / Tiếng Việt và bố cục tự động / Hán cột dọc. OCR trang đang xem hoặc nhập khoảng **số trang PDF**, rồi tải text về.

Màn OCR có âm Hán–Việt gợi ý từ từ điển offline. Bấm **Dóng hàng · 2/4 bản** để nạp text, xếp dòng, sửa/gộp/tách và kiểm trước khi xuất TSV/XLSX. Đây là biên tập thủ công; xếp theo dòng chưa phải ghép theo nghĩa tự động. OCR Hán/Việt vẫn đang test, chưa chốt chạy batch.

Chạy local đọc PDF từ máy. Màn chính chọn Tesseract.js để OCR trong trình duyệt, hoặc Gemini để gửi ảnh từng trang qua server Python đến Google. Với Tesseract, lần đầu vẫn cần mạng tải core/mô hình. Không cần cài bộ Paddle chỉ để mở màn chính.

## OCR bằng Gemini

Lưu API key của project **Free tier chưa bật billing** vào file `.gemini_api_key` ở thư mục gốc repo. File này bị loại khỏi Git và server đọc lại mỗi request. Trên giao diện chọn **Gemini**, để trống ô key để dùng key local, chọn model và ngôn ngữ. Có thể nhập key vào ô để dùng riêng cho phiên trang đang mở. Mặc định dùng Flash-Lite với mức suy nghĩ tối thiểu để giảm độ trễ. Bấm **Chạy OCR** cho trang hiện tại hoặc chọn **Từ trang / đến trang** rồi bấm **OCR khoảng trang**. Mỗi trang là một request thường, tối đa 50 trang/lượt và dưới 15 MB/request theo giới hạn của tool. Chạy Gemini dùng thư viện chuẩn Python, không cần cài PaddleOCR.

Key nhập trên giao diện chỉ giữ trong phiên trang đang mở; key local nằm trong `.gemini_api_key` và không được trả về trình duyệt. Ảnh và kết quả qua Gemini free tier có thể được Google dùng để cải thiện sản phẩm. Gói thanh toán và quota xem trong AI Studio, chọn đúng project/model ở Usage / Rate limits. Bộ đếm trên tool chỉ tính số lần gửi trong phiên, gồm retry.

Nút Dừng ngừng gửi trang tiếp theo, giữ kết quả request đang xử lý nếu nhận được. Nút Tiếp tục chạy từ trang chưa hoàn tất với cùng nguồn, ngôn ngữ và bố cục; có thể đổi model trước khi tiếp tục. Tiến độ nằm trong phiên trang đang mở; tải text trước khi đóng hoặc tải lại trang. Server chờ Google tối đa 30 giây cho một lần chờ mạng; giao diện dừng chờ sau 35 giây. Khi model quá tải (503) tool báo ngay, không tự gửi lại. Giới hạn phút có chỉ dẫn chờ ngắn vẫn được thử lại tối đa 2 lần. Khi timeout, Google có thể đã xử lý request dù tool chưa nhận kết quả. Dừng hẳn bằng Ctrl+C ở terminal và đóng tab.

## Sửa/config

- `index.html`: giao diện và hiển thị PDF.
- `quick_tools.js`: input, ngôn ngữ, bố cục và OCR Tesseract từng trang/khoảng trang.
- `gemini_ocr.js` + `cong_cu/gemini_ocr.py`: giao diện Gemini, request từng trang, giới hạn và xử lý lỗi.
- `hanviet.js` + `assets/hanviet/`: âm gợi ý; không thay bản phiên âm trong sách. Bấm chữ để sửa; OCR sai vẫn có thể tra ra âm.
- `alignment.html` + `alignment.js`: màn dóng 2/4 bản, bản nháp lưu trong trình duyệt. Xuất JSON để giữ nguồn, trạng thái và âm tự sửa; TSV/XLSX chỉ chứa text các bản, không chứa âm gợi ý.
- Muốn chạy cổng khác: `python cong_cu/serve_review.py --port 7072`, rồi mở http://127.0.0.1:7072/.
- `cong_cu/serve_review.py`: server local. [Cấu hình backend OCR tùy chọn](cong_cu/README.md).
- `advanced.html`: giao diện thử nghiệm box/dóng hàng, đang cần test thêm. Sửa module trong `cong_cu/ui/`, chạy `python cong_cu/build_ui.py` để cập nhật.

## Lưu bài

Chưa có database chung, làm xong push vào repo. Mỗi bài/mẫu để trong `bai_lam/Ten/ten_bai/`; ghi nguồn, trang PDF và cấu hình chạy. Giữ OCR thô riêng với text đã sửa. Ghi chú trên web lưu theo trình duyệt: xuất file rồi push để chia sẻ; **+ Input không tự upload**.

[Danh sách ngữ liệu trực tuyến](ONLINE_CORPUS.md) · [Phân công, timeline](https://docs.google.com/document/d/1svQTK-oO5F3AU4UTfdqMaXqJ1LDLaNN7C_ViSBzRsh8/edit?tab=t.0) · [Đầu ra chung](OUTPUT_CONTRACT.md) · [Mẫu tìm text](mau/TIM_TEXT.md) · [Mapping tham khảo](MAPPING.tsv).

`inputs/`: sáu PDF nguồn. `mau/`: mẫu dùng chung. `bai_lam/`: tự tạo thư mục khi có bài, không cần lập thêm file chia việc.

Giấy phép thư viện: [PDF.js](assets/pdfjs/LICENSE), [Tesseract.js](assets/tesseract/LICENSE.md).
