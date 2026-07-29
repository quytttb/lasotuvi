# LasoTuVi

Open-source Zi Wei Dou Shu (Purple Star Astrology) chart engine — Python 3.12–3.13,
FastAPI.

This repository is maintained independently (not synced with abandoned upstream forks).

## Features

- Full star placement: 12 palaces, major/minor stars, miao_wang (Miao/Wang/…)
- Solar ↔ lunar conversion, full stem–branch (year/month/day/hour)
- REST API v2 (**English JSON keys**, breaking)
- Chart formations (cách cục) and palace star interpretations
- Client-friendly star fields: `miao_wang`, `category_label`, `is_auspicious`
- Monthly luck via `view_year`
- Star catalog: `GET /info/stars`
- Modern pytest suite

## Terminology

Sino-Vietnamese domain terms (Hán Việt ↔ 繁體 ↔ English): see [docs/TERMINOLOGY.md](docs/TERMINOLOGY.md).  
Code naming (PEP 8 English): see [docs/NAMING.md](docs/NAMING.md).

## Requirements

- Python 3.12 or 3.13

## Quick start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### API

```bash
./run_api.sh
# or
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Readiness (including chart runtime): http://localhost:8000/ready

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

## Layout

```
lasotuvi/          # Engine (stem_branch, earth_plate, stars, chart_builder, analysis, …)
api/               # FastAPI v2
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

## Runtime configuration

Chart generation runs py-iztro/PythonMonkey in one isolated subprocess. This avoids sharing
the JavaScript runtime between request threads and lets the API terminate a timed-out worker.

- `LASOTUVI_IZTRO_TIMEOUT_SECONDS` — chart deadline, default `15`
- `LASOTUVI_IZTRO_BUSY_TIMEOUT_SECONDS` — maximum wait for the single worker, default `2`
- `LASOTUVI_CORS_ORIGINS` — comma-separated origins, default `*`
- `LASOTUVI_CORS_ALLOW_CREDENTIALS` — enable credentials only with explicit origins

## License

MIT. Chart engine originally by doanguyen (2016); this fork modernized and maintained independently at [quytttb/lasotuvi](https://github.com/quytttb/lasotuvi).
