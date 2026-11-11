# Ngữ liệu trực tuyến có thể dùng để giảm OCR

Danh sách này chỉ là điểm bắt đầu. Mỗi bản lấy từ web phải được so với đúng bài, đúng ấn bản và đúng người dịch trong PDF trước khi đưa vào `text/`.

| Mã | Bài / nhóm bài | Phần liên quan | Nguồn | Trạng thái |
|---|---|---|---|---|
| CPO_03 | Bút hải tùng đàm | Tuấn, PDF 44–203 | [Trang tác giả Ngô Thì Nhậm trên Thi Viện](https://www.thivien.net/Ng%C3%B4-Th%C3%AC-Nh%E1%BA%ADm/author-14GcnhLjD2ajP0MTgtX13Q) | Có danh mục và nhiều bài, cần đối chiếu từng bài |
| CPO_03 | Xuân mộ 春暮 | Bút hải tùng đàm | [Thi Viện](https://www.thivien.net/Ng%C3%B4-Th%C3%AC-Nh%E1%BA%ADm/Xu%C3%A2n-m%E1%BB%99/poem-_dMOlzb-UpEIjw8m8dm81Q) | Có chữ Hán và bản dịch, cần xác nhận đúng bản trong sách |
| CPO_03 | Phụng nghĩ trấn thủ tiễn đốc đồng 奉擬鎮守餞督同 | Bút hải tùng đàm | [Thi Viện](https://www.thivien.net/Ng%C3%B4-Th%C3%AC-Nh%E1%BA%ADm/Ph%E1%BB%A5ng-ngh%C4%A9-tr%E1%BA%A5n-th%E1%BB%A7-ti%E1%BB%85n-%C4%91%E1%BB%91c-%C4%91%E1%BB%93ng/poem-rELFgP9of-BkyxHjCYn6yg) | Có bài và bản dịch, cần xác nhận người dịch |
| CPO_03 | Thạch Long tuyền | Bút hải tùng đàm | [Bản dịch Nguyễn Sĩ Lâm](https://www.thivien.net/B%E1%BA%A3n-d%E1%BB%8Bch-c%E1%BB%A7a-Nguy%E1%BB%85n-S%C4%A9-L%C3%A2m/reply-SdALrlg8daTfB8oNiho-Nw) | Có nhiều bản dịch, phải chọn đúng bản |
| CPO_05 | Quốc tộ | Tổng tập văn học Việt Nam 1, PDF 217 | Tìm theo tiêu đề và đối chiếu PDF | Chưa chốt URL và bản dịch trong sách |
| CPO_02 | Hoàng Việt văn tuyển | Tuấn, PDF 19–161 | [Từ điển Hán Nôm](https://hvdic.thivien.net/hv/ho%C3%A0ng%20vi%E1%BB%87t%20văn%20tuyển) | Mới xác nhận thư mục, chưa có text đủ dùng |

## Quy trình nhập text từ web

1. Ghi tên bài, URL, người đăng hoặc người dịch và trang PDF vào `nguon.tsv`.
2. Đối chiếu tiêu đề, số câu, chữ Hán, phiên âm và bản dịch với PDF.
3. Chỉ chép đúng phiên bản khớp sách vào `text/`. Không trộn nhiều bản dịch.
4. Giữ bản tải hoặc bản chép ban đầu trong `ocr/` hoặc ghi rõ nguồn web trong ghi chú để truy vết.
5. Dóng hàng và kiểm tra lại theo ảnh PDF trước khi xuất TSV/XLSX.
