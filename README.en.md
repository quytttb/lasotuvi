# LasoTuVi

[Bản tiếng Việt](README.md)

LasoTuVi is an open-source Zi Wei Dou Shu chart engine for Python 3.12–3.13 with a FastAPI API. This repository is maintained independently and is not synchronized with abandoned upstream forks.

## Features

- Full placement across 12 palaces, including major and minor stars and Miao/Wang/De/Ping/Xian brightness.
- Solar ↔ lunar conversion and year/month/day/hour stem–branch calculation.
- REST API v2 with English JSON keys (breaking from v1).
- Chart-formation detection and palace-level star interpretations.
- Client-friendly star fields: `miao_wang`, `category_label`, and `is_auspicious`.
- Yearly-luck view through `view_year` and a star catalog at `GET /info/stars`.

## Terminology

See the [terminology reference](docs/TERMINOLOGY.en.md) and [naming conventions](docs/NAMING.en.md).

## Requirements and setup

Python 3.12 or 3.13 is required.

```bash
uv sync --locked --extra dev
```

This installs the reviewed dependency set from `uv.lock`. `pip install -e ".[dev]"` remains supported but resolves dependencies at installation time. To update dependencies intentionally, run `uv lock --upgrade`, review the lockfile, then run tests and audits.

## API

```bash
./run_api.sh
# or
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Readiness: http://localhost:8000/ready

## Python library

```bash
pip install -e .
```

## Runtime configuration

Chart generation runs py-iztro/PythonMonkey in an isolated subprocess. `LASOTUVI_IZTRO_TIMEOUT_SECONDS` defaults to `15`; `LASOTUVI_IZTRO_BUSY_TIMEOUT_SECONDS` defaults to `2`; `LASOTUVI_CORS_ORIGINS` defaults to `*`; and `LASOTUVI_CORS_ALLOW_CREDENTIALS` should be enabled only with explicit origins.

## License

MIT. The original chart engine was created by doanguyen (2016); this fork is modernized and independently maintained at [quytttb/lasotuvi](https://github.com/quytttb/lasotuvi).
