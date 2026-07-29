# Lộ trình / Roadmap

## Tiếng Việt

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

---

## English

This file tracks only current work; historical API milestones are archived in [API improvement archive](API_IMPROVEMENTS_SUMMARY.md).

### Completed stabilization

- [x] Canonical py-iztro chart model and adapter.
- [x] Isolated, restartable py-iztro runtime with timeout and readiness checks.
- [x] Python 3.12/3.13 GitHub Actions checks.
- [x] Single-source packaging metadata in `pyproject.toml`.
- [x] Ruff, Black, and Pyright quality gates.
- [x] Generic production error responses, request IDs, and configurable CORS.
- [x] Gregorian/lunar request-boundary validation.

### Domain correctness

- [ ] Complete or retire the experimental ephemeris calendar conversion functions.
- [ ] Add authoritative leap-month fixtures and explicit leap-month chart semantics.
- [ ] Add golden charts for boundary dates and both early and late Zi periods.
- [ ] Expand the interpretation knowledge base to all 14 major stars across 12 palaces.
- [ ] Tighten formation rules for brightness, conjunction, trine, and opposition.

### Reliability and operations

- [ ] Add load tests for worker contention, timeout, and restart behavior.
- [ ] Migrate API tests from Starlette TestClient when the httpx2 client stabilizes.
- [ ] Publish coverage history from CI instead of committing generated artifacts.
- [ ] Add container and deployment configuration when a target platform is selected.
- [ ] Add rate limiting or authentication only when deployment requirements need them.

### Documentation

- [ ] Document an authoritative source for every star-placement rule.
- [ ] Add an architecture diagram: calendar → canonical chart → analysis → API.
