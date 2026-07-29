# Lộ trình

[English version](TODO.en.md)

Tài liệu này chỉ theo dõi công việc hiện tại. Các mốc API lịch sử được lưu tại [Lưu trữ cải tiến API](API_IMPROVEMENTS_SUMMARY.md).

### Ổn định đã hoàn thành

- [x] Mô hình lá số py-iztro chuẩn và adapter.
- [x] Thời gian chạy py-iztro cô lập, có thể khởi động lại, kèm timeout và readiness check.
- [x] Kiểm tra GitHub Actions cho Python 3.12/3.13.
- [x] Metadata đóng gói một nguồn tại `pyproject.toml`.
- [x] Cổng chất lượng Ruff, Black và Pyright.
- [x] Phản hồi lỗi production tổng quát, request ID và CORS có cấu hình.
- [x] Xác thực biên đầu vào lịch dương/âm.

### Tính đúng đắn domain

- [ ] Hoàn thiện hoặc loại bỏ các hàm đổi lịch thiên văn thử nghiệm.
- [ ] Thêm fixture tháng nhuận có thẩm quyền và ngữ nghĩa lá số cho tháng nhuận.
- [ ] Thêm lá số chuẩn cho ngày biên và cả hai khoảng giờ Tý đầu/cuối.
- [ ] Mở rộng knowledge base diễn giải cho toàn bộ 14 chính tinh trên 12 cung.
- [ ] Siết chặt quy tắc cách cục về độ sáng, hội chiếu và tam hợp/xung chiếu.

### Độ tin cậy và vận hành

- [ ] Thêm kiểm thử tải cho tranh chấp worker, timeout và khởi động lại.
- [ ] Chuyển kiểm thử API khỏi Starlette TestClient khi httpx2 client ổn định.
- [ ] Xuất lịch sử coverage từ CI thay vì commit artifact sinh tự động.
- [ ] Thêm cấu hình container và triển khai khi đã chọn nền tảng đích.
- [ ] Chỉ thêm rate limiting hoặc xác thực khi yêu cầu triển khai cần đến.

### Tài liệu

- [ ] Ghi nguồn có thẩm quyền cho từng quy tắc an sao.
- [ ] Thêm sơ đồ kiến trúc: lịch → lá số chuẩn → phân tích → API.
