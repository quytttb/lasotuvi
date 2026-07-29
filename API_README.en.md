# LasoTuVi API v2

[Bản tiếng Việt](API_README.md)

LasoTuVi REST API v2 provides Zi Wei Dou Shu chart data. JSON keys are English, which is a breaking change from v1.

## Breaking changes from v1

| v1 | v2 |
|---|---|
| `ngay` / `thang` / `nam` / `gio` | `day` / `month` / `year` / `hour` |
| `gioi_tinh` / `duong_lich` / `nam_xem` | `gender` / `is_solar` / `view_year` |
| `can_chi` / `dia_ban` / `thien_ban` | `stem_branch` / `earth_plate` / `chart_meta` |
| `thap_nhi_cung` / `cung_sao` | `palaces` / `stars` |
| `cung_menh` / `dac_tinh` | `life_palace` / `miao_wang` |
| `GET /info/sao` | `GET /info/stars` |
| `POST /calendar/can-chi` | `POST /calendar/stem-branch` |

## Quick start

```bash
uv sync --locked --extra api
./run_api.sh
```

The interactive documentation, liveness endpoint, and readiness endpoint are available at http://localhost:8000/docs, http://localhost:8000/health, and http://localhost:8000/ready.

## Main endpoints

- `POST /chart/generate` — full chart.
- `POST /chart/earth-plate` — earth plate only.
- `POST /chart/analyze` — palace analysis.
- `POST /chart/batch` — up to 10 charts.
- `POST /calendar/solar-to-lunar`, `POST /calendar/lunar-to-solar`, and `POST /calendar/stem-branch`.
- `GET /info/stars`, `/info/elements`, `/info/stem-branch`, and `/info/hour-branches`.

Every response includes `X-Request-ID` and `X-Process-Time`; internal exception details are logged but never returned in 500/503 responses.

## Production configuration

Set `LASOTUVI_CORS_ORIGINS` to a comma-separated list of client origins. Credentialed CORS is disabled by default and cannot be combined with a wildcard origin.

## Interpretation fields

`POST /chart/generate` and `POST /chart/earth-plate` include `formations` on the chart and earth plate, and `interpretations` on every palace. The engine is `lasotuvi.analysis.ChartAnalyzer`; the knowledge base is `lasotuvi/data/interpretations.json`.

See the [terminology reference](docs/TERMINOLOGY.en.md) and [naming conventions](docs/NAMING.en.md).
