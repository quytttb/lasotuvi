# API v2 — English schema (breaking)

LasoTuVi REST API for Zi Wei Dou Shu charts.

## Breaking changes from v1

| v1 | v2 |
|----|----|
| `ngay` / `thang` / `nam` / `gio` | `day` / `month` / `year` / `hour` |
| `gioi_tinh` / `duong_lich` / `nam_xem` | `gender` / `is_solar` / `view_year` |
| `can_chi` / `dia_ban` / `thien_ban` | `stem_branch` / `earth_plate` / `chart_meta` |
| `thap_nhi_cung` / `cung_sao` | `palaces` / `stars` |
| `cung_menh` / `dac_tinh` | `life_palace` / `miao_wang` |
| `GET /info/sao` | `GET /info/stars` |
| `POST /calendar/can-chi` | `POST /calendar/stem-branch` |

Version: **2.0.0**

## Quick start

```bash
uv sync --locked --extra api
./run_api.sh
```

Install [uv](https://docs.astral.sh/uv/) to use the reviewed dependency set in `uv.lock`.
`pip install -e ".[api]"` remains available when a locked environment is not required.

- Docs: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness: http://localhost:8000/ready

## Main endpoints

- `POST /chart/generate` — full chart
- `POST /chart/earth-plate` — earth plate only
- `POST /chart/analyze` — palace analysis
- `POST /chart/batch` — up to 10 charts
- `POST /calendar/solar-to-lunar` / `lunar-to-solar`
- `POST /calendar/stem-branch`
- `GET /info/stars` / `/info/elements` / `/info/stem-branch` / `/info/hour-branches`

All responses include `X-Request-ID` and `X-Process-Time`. Pass an `X-Request-ID` request
header to preserve an existing trace identifier. Internal exception details are logged but
are not returned in 500/503 responses.

For production, set `LASOTUVI_CORS_ORIGINS` to the comma-separated client origins. Credentialed
CORS is disabled by default and cannot be combined with the wildcard origin.

## Interpretation fields (v2)

`POST /chart/generate` and `POST /chart/earth-plate` include:

| Field | Location | Meaning |
|-------|----------|---------|
| `formations` | chart + earth plate | Detected chart patterns (cách cục): `{code, name, description}` |
| `interpretations` | each palace | Star readings from KB: `{star, interpretation}` |

Engine: `lasotuvi.analysis.ChartAnalyzer`. Knowledge base: `lasotuvi/data/interpretations.json`.

See [docs/TERMINOLOGY.md](docs/TERMINOLOGY.md) §12 and [docs/NAMING.md](docs/NAMING.md) for vocabulary.
