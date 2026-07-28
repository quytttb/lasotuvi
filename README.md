# LasoTuVi

Mã nguồn mở an sao lá số Tử Vi (Python 3.12+) với REST API FastAPI và frontend Next.js.

Repo này phát triển độc lập. Không đồng bộ và không phụ thuộc vào các fork/upstream đã ngừng duy trì.

## Tính năng

- An sao đầy đủ: địa bàn 12 cung, chính tinh / phụ tinh, chất lượng sao
- Đổi lịch dương ↔ âm, Can Chi
- REST API (FastAPI + Pydantic v2) với OpenAPI docs
- Frontend scaffold: Next.js 15 + React 19 + TypeScript + Tailwind
- Bộ test hiện đại (pytest)

## Yêu cầu

- Python ≥ 3.12
- Node.js ≥ 20 (cho frontend)

## Cài đặt nhanh

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-api.txt -r requirements-dev.txt
```

### Chạy API

```bash
./run_api.sh
# hoặc
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

### Chạy frontend

```bash
cd frontend
./setup.sh   # hoặc: npm install
npm run dev
```

Mở http://localhost:3000 (cấu hình API URL trong `frontend/.env.local`).

## Cấu trúc

```
lasotuvi/     # Engine an sao (AmDuong, DiaBan, Sao, lịch…)
api/          # FastAPI service layer + endpoints
frontend/     # Next.js client
tests/        # pytest
```

## Tài liệu thêm

- [QUICKSTART.md](QUICKSTART.md) — hướng dẫn chạy nhanh
- [API_README.md](API_README.md) — chi tiết endpoints

## Thư viện Python

```bash
pip install -e .
```

Hoặc dùng trực tiếp:

```python
from lasotuvi.App import lapDiaBan

# xem demo.py
```

## Giấy phép

MIT. Engine an sao kế thừa từ dự án mã nguồn mở gốc của doanguyen (2016); bản này được hiện đại hóa và duy trì độc lập tại [quytttb/lasotuvi](https://github.com/quytttb/lasotuvi).
