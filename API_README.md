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
pip install -r requirements.txt -r requirements-api.txt
./run_api.sh
```

- Docs: http://localhost:8000/docs

## Main endpoints

- `POST /chart/generate` — full chart
- `POST /chart/earth-plate` — earth plate only
- `POST /chart/analyze` — palace analysis
- `POST /chart/batch` — up to 10 charts
- `POST /calendar/solar-to-lunar` / `lunar-to-solar`
- `POST /calendar/stem-branch`
- `GET /info/stars` / `/info/elements` / `/info/stem-branch` / `/info/hour-branches`

## Interpretation fields (v2)

`POST /chart/generate` and `POST /chart/earth-plate` include:

| Field | Location | Meaning |
|-------|----------|---------|
| `formations` | chart + earth plate | Detected chart patterns (cách cục): `{code, name, description}` |
| `interpretations` | each palace | Star readings from KB: `{star, interpretation}` |

Engine: `lasotuvi.analysis.ChartAnalyzer`. Knowledge base: `lasotuvi/data/interpretations.json`.

See [docs/TERMINOLOGY.md](docs/TERMINOLOGY.md) §12 and [docs/NAMING.md](docs/NAMING.md) for vocabulary.
