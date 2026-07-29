# AGENTS.md

## Project overview

LasoTuVi is a Python 3.12+ Zi Wei Dou Shu chart engine with a FastAPI v2 API.

- `lasotuvi/`: domain engine, calendar conversion, chart construction, and analysis
- `api/`: FastAPI routes, Pydantic schemas, service adapters, and star catalog
- `tests/`: pytest unit and API tests
- `docs/`: domain terminology and naming conventions
- `lasotuvi/data/interpretations.json`: interpretation knowledge base

## Setup and common commands

Create and activate a virtual environment, then install all dependency groups:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-api.txt -r requirements-dev.txt
```

Use these checks while developing:

```bash
pytest
pytest tests/test_api.py
pytest tests/test_api.py::TestChartGeneration::test_generate_full_chart
ruff check .
black --check .
pyright
```

Pytest defaults to parallel execution and generates coverage reports. Add `-n 0` when
debugging a test serially. Run the API with `./run_api.sh`; its interactive docs are at
`http://localhost:8000/docs`.

## Coding conventions

- Follow Python 3.12, PEP 8, and the configured 100-character line length.
- Add type hints to new or changed public interfaces where practical.
- Keep the engine independent of FastAPI. API-specific validation and serialization belong
  in `api/`; reusable chart and calendar logic belongs in `lasotuvi/`.
- Use Pinyin for stars and domain-specific names, stable English for chart structure, and
  PEP 8 identifiers. Do not introduce literal English star names or unaccented Vietnamese
  identifiers. Follow `docs/NAMING.md` and `docs/TERMINOLOGY.md` for the authoritative maps.
- API v2 uses English JSON keys. Keep route response models, `api/services.py`, tests, and API
  documentation synchronized when a schema changes.
- Preserve deprecated compatibility aliases unless a task explicitly removes them.
- Keep user-facing Vietnamese/Han-Viet display strings and machine-facing identifiers
  distinct.

## Testing expectations

- Add or update tests for every behavior change. Prefer focused tests near the affected
  module and include API tests for externally visible schema or status-code changes.
- For calendar and star-placement changes, cover known dates and boundary cases; do not
  replace established expected values solely to make a failing test pass.
- Validate both male (`gender=1`) and female (`gender=-1`) paths when direction-dependent
  chart logic changes.
- When editing `interpretations.json`, keep it valid JSON and verify the relevant analyzer
  and API tests.
- Before handing off a change, run the smallest relevant test first, then the full suite and
  configured lint/type checks when feasible. Report any check that could not be run.

## Change discipline

- Keep changes narrowly scoped and do not modify unrelated working-tree changes.
- Avoid generated artifacts such as coverage output, caches, and virtual environments.
- Update `README.md`, `API_README.md`, or domain docs when public behavior, endpoints,
  terminology, or setup changes.
- Treat astrology terminology and placement rules as domain logic: preserve existing
  behavior unless the requested change is backed by tests or a clearly documented rule.
