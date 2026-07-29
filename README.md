# LasoTuVi

## Tiếng Việt

LasoTuVi là bộ máy lập lá số Tử Vi Đẩu Số mã nguồn mở, hỗ trợ Python 3.12–3.13 và API FastAPI. Kho mã này được duy trì độc lập, không đồng bộ với các nhánh nguồn đã ngừng phát triển.

### Tính năng

- An đủ sao trên 12 cung, gồm chính tinh, phụ tinh và mức Miếu/Vượng/Đắc/Bình/Hãm.
- Đổi lịch dương ↔ âm, tính Can Chi năm/tháng/ngày/giờ.
- API REST v2 với khóa JSON bằng tiếng Anh (thay đổi không tương thích v1).
- Phát hiện cách cục và diễn giải sao theo cung.
- Trường dữ liệu sao thân thiện với ứng dụng khách: `miao_wang`, `category_label`, `is_auspicious`.
- Xem hạn theo năm qua `view_year`; danh mục sao tại `GET /info/stars`.
- Bộ kiểm thử pytest hiện đại.

### Thuật ngữ

Đối chiếu thuật ngữ Hán Việt ↔ 繁體中文 ↔ English: [Thuật ngữ](docs/TERMINOLOGY.md).
Quy ước đặt tên trong mã nguồn: [Quy ước đặt tên](docs/NAMING.md).

### Yêu cầu và khởi động nhanh

- Python 3.12 hoặc 3.13.

```bash
uv sync --locked --extra dev
```

Tệp `uv.lock` được lưu trong kho là bộ phụ thuộc đã được CI rà soát. Cài [uv](https://docs.astral.sh/uv/) để dùng đúng bộ phụ thuộc đã khóa. Lệnh cũ `pip install -e ".[dev]"` vẫn dùng được, nhưng sẽ phân giải các phiên bản tương thích tại thời điểm cài đặt thay vì dùng bộ khóa đã rà soát.

Để chủ động cập nhật phụ thuộc, chạy `uv lock --upgrade`, xem lại thay đổi trong tệp khóa, rồi chạy kiểm thử và kiểm tra bảo mật. CI kiểm tra mọi nhóm phụ thuộc đã khóa bằng `pip-audit`.

### API

```bash
./run_api.sh
# hoặc
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Readiness (bao gồm thời gian chạy lập lá số): http://localhost:8000/ready

Ví dụ phần thân yêu cầu cho `POST /chart/generate`:

```json
{
  "day": 15,
  "month": 8,
  "year": 1990,
  "hour": 7,
  "gender": 1,
  "is_solar": true,
  "timezone": 7,
  "name": "Ví dụ",
  "view_year": 2026
}
```

### Cấu trúc thư mục

```
lasotuvi/          # Bộ máy (stem_branch, earth_plate, stars, chart_builder, analysis, …)
api/               # FastAPI v2
tests/             # Kiểm thử
docs/              # Tài liệu thuật ngữ và quy ước
```

### Thư viện Python

```bash
pip install -e .
```

```python
from lasotuvi.chart_builder import build_earth_plate
from lasotuvi.heaven_plate import HeavenPlate

plate = build_earth_plate(15, 8, 1990, 7, 1, True, 7)
heaven = HeavenPlate(15, 8, 1990, 7, 1, "Tên", plate)
```

### Cấu hình thời gian chạy

Việc lập lá số chạy py-iztro/PythonMonkey trong một tiến trình con cô lập. Cách này tránh dùng chung thời gian chạy JavaScript giữa các luồng yêu cầu và cho phép API dừng worker quá thời hạn.

- `LASOTUVI_IZTRO_TIMEOUT_SECONDS` — thời hạn lập lá số, mặc định `15` giây.
- `LASOTUVI_IZTRO_BUSY_TIMEOUT_SECONDS` — thời gian chờ worker đơn tối đa, mặc định `2` giây.
- `LASOTUVI_CORS_ORIGINS` — các origin phân tách bằng dấu phẩy, mặc định `*`.
- `LASOTUVI_CORS_ALLOW_CREDENTIALS` — chỉ bật credentials khi khai báo origin cụ thể.

### Giấy phép

MIT. Bộ máy lập lá số ban đầu do doanguyen phát triển (2016); nhánh này được hiện đại hóa và duy trì độc lập tại [quytttb/lasotuvi](https://github.com/quytttb/lasotuvi).

---

## English

LasoTuVi is an open-source Zi Wei Dou Shu chart engine for Python 3.12–3.13 with a FastAPI API. This repository is maintained independently and is not synchronized with abandoned upstream forks.

### Features

- Full placement across 12 palaces, including major and minor stars and Miao/Wang/De/Ping/Xian brightness.
- Solar ↔ lunar conversion and year/month/day/hour stem–branch calculation.
- REST API v2 with English JSON keys (breaking from v1).
- Chart-formation detection and palace-level star interpretations.
- Client-friendly star fields: `miao_wang`, `category_label`, and `is_auspicious`.
- Yearly-luck view through `view_year` and a star catalog at `GET /info/stars`.

### Requirements and setup

Python 3.12 or 3.13 is required. Run `uv sync --locked --extra dev` to install the reviewed dependency set from `uv.lock`; `pip install -e ".[dev]"` remains supported but resolves dependencies at installation time. To update dependencies intentionally, run `uv lock --upgrade`, review the lockfile, then run tests and audits.

### API and library

Start the API with `./run_api.sh` or `uvicorn api.main:app --reload --host 0.0.0.0 --port 8000`. Interactive documentation is available at http://localhost:8000/docs. Install the Python library with `pip install -e .`.

### Runtime configuration

Chart generation runs py-iztro/PythonMonkey in an isolated subprocess. `LASOTUVI_IZTRO_TIMEOUT_SECONDS` defaults to `15`; `LASOTUVI_IZTRO_BUSY_TIMEOUT_SECONDS` defaults to `2`; `LASOTUVI_CORS_ORIGINS` defaults to `*`; and `LASOTUVI_CORS_ALLOW_CREDENTIALS` should be enabled only with explicit origins.

### License

MIT. The original chart engine was created by doanguyen (2016); this fork is modernized and independently maintained at [quytttb/lasotuvi](https://github.com/quytttb/lasotuvi).
