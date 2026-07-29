# API LasoTuVi v2

[English version](API_README.en.md)

API REST LasoTuVi v2 cung cấp dữ liệu lá số Tử Vi Đẩu Số. Khóa JSON sử dụng tiếng Anh; đây là thay đổi không tương thích với API v1.

### Thay đổi từ v1

| v1 | v2 |
|---|---|
| `ngay` / `thang` / `nam` / `gio` | `day` / `month` / `year` / `hour` |
| `gioi_tinh` / `duong_lich` / `nam_xem` | `gender` / `is_solar` / `view_year` |
| `can_chi` / `dia_ban` / `thien_ban` | `stem_branch` / `earth_plate` / `chart_meta` |
| `thap_nhi_cung` / `cung_sao` | `palaces` / `stars` |
| `cung_menh` / `dac_tinh` | `life_palace` / `miao_wang` |
| `GET /info/sao` | `GET /info/stars` |
| `POST /calendar/can-chi` | `POST /calendar/stem-branch` |

Phiên bản: **2.0.0**

### Khởi động nhanh

```bash
uv sync --locked --extra api
./run_api.sh
```

Cài [uv](https://docs.astral.sh/uv/) để dùng bộ phụ thuộc đã rà soát trong `uv.lock`. `pip install -e ".[api]"` vẫn khả dụng khi không cần môi trường khóa.

- Tài liệu tương tác: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness: http://localhost:8000/ready

### Endpoint chính

- `POST /chart/generate` — lập lá số đầy đủ.
- `POST /chart/earth-plate` — chỉ tạo địa bàn.
- `POST /chart/analyze` — phân tích cung.
- `POST /chart/batch` — tối đa 10 lá số.
- `POST /calendar/solar-to-lunar` và `POST /calendar/lunar-to-solar`.
- `POST /calendar/stem-branch`.
- `GET /info/stars`, `/info/elements`, `/info/stem-branch`, `/info/hour-branches`.

Mọi phản hồi đều có `X-Request-ID` và `X-Process-Time`. Gửi `X-Request-ID` trong request header để giữ nguyên mã truy vết. Chi tiết ngoại lệ nội bộ được ghi log nhưng không trả về trong phản hồi 500/503.

Trong môi trường production, đặt `LASOTUVI_CORS_ORIGINS` thành danh sách origin của ứng dụng khách, phân tách bằng dấu phẩy. CORS có credentials tắt mặc định và không thể dùng cùng wildcard origin.

### Trường diễn giải (v2)

`POST /chart/generate` và `POST /chart/earth-plate` bao gồm:

| Trường | Vị trí | Ý nghĩa |
|---|---|---|
| `formations` | lá số và địa bàn | Cách cục được phát hiện: `{code, name, description}` |
| `interpretations` | mỗi cung | Diễn giải sao từ knowledge base: `{star, interpretation}` |

Bộ máy: `lasotuvi.analysis.ChartAnalyzer`. Knowledge base: `lasotuvi/data/interpretations.json`. Xem thêm [Thuật ngữ](docs/TERMINOLOGY.md) và [Quy ước đặt tên](docs/NAMING.md).
