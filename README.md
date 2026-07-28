# LasoTuVi

Open-source Zi Wei Dou Shu (Purple Star Astrology) chart engine — Python 3.12+, FastAPI, Next.js.

This repository is maintained independently (not synced with abandoned upstream forks).

## Features

- Full star placement: 12 palaces, major/minor stars, brightness (Miao/Wang/…)
- Solar ↔ lunar conversion, full stem–branch (year/month/day/hour)
- REST API v2 (**English JSON keys**, breaking)
- Client-friendly star fields: `brightness`, `category_label`, `is_auspicious`
- Monthly luck via `view_year`
- Star catalog: `GET /info/stars`
- Frontend scaffold: Next.js 15 + React 19 + TypeScript + Tailwind
- Modern pytest suite

## Terminology

Sino-Vietnamese domain terms (Hán Việt ↔ 繁體 ↔ English): see [docs/TERMINOLOGY.md](docs/TERMINOLOGY.md).  
Code naming (PEP 8 English): see [docs/NAMING.md](docs/NAMING.md).

## Requirements

- Python ≥ 3.12
- Node.js ≥ 20 (frontend)

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-api.txt -r requirements-dev.txt
```

### API

```bash
./run_api.sh
# or
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

Example body for `POST /chart/generate`:

```json
{
  "day": 15,
  "month": 8,
  "year": 1990,
  "hour": 7,
  "gender": 1,
  "is_solar": true,
  "timezone": 7,
  "name": "Example",
  "view_year": 2026
}
```

### Frontend

```bash
cd frontend
./setup.sh
npm run dev
```

## Layout

```
lasotuvi/          # Engine (stem_branch, earth_plate, stars, chart_builder, …)
api/               # FastAPI v2
frontend/          # Next.js client
tests/
docs/TERMINOLOGY.md
docs/NAMING.md
```

## Python library

```bash
pip install -e .
```

```python
from lasotuvi.chart_builder import build_earth_plate
from lasotuvi.heaven_plate import HeavenPlate

plate = build_earth_plate(15, 8, 1990, 7, 1, True, 7)
heaven = HeavenPlate(15, 8, 1990, 7, 1, "Name", plate)
```

## License

MIT. Chart engine originally by doanguyen (2016); this fork modernized and maintained independently at [quytttb/lasotuvi](https://github.com/quytttb/lasotuvi).
