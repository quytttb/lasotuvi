# Roadmap

[Bản tiếng Việt](TODO.md)

This file tracks only current work. Historical API milestones are archived in [the API improvement archive](API_IMPROVEMENTS_SUMMARY.en.md).

## Completed stabilization

- [x] Canonical py-iztro chart model and adapter.
- [x] Isolated, restartable py-iztro runtime with timeout and readiness checks.
- [x] Python 3.12/3.13 GitHub Actions checks.
- [x] Single-source packaging metadata in `pyproject.toml`.
- [x] Ruff, Black, and Pyright quality gates.
- [x] Generic production error responses, request IDs, and configurable CORS.
- [x] Gregorian/lunar request-boundary validation.

## Domain correctness

- [ ] Complete or retire the experimental ephemeris calendar conversion functions.
- [ ] Add authoritative leap-month fixtures and explicit leap-month chart semantics.
- [ ] Add golden charts for boundary dates and both early and late Zi periods.
- [ ] Expand the interpretation knowledge base to all 14 major stars across 12 palaces.
- [ ] Tighten formation rules for brightness, conjunction, trine, and opposition.

## Reliability and operations

- [ ] Add load tests for worker contention, timeout, and restart behavior.
- [ ] Migrate API tests from Starlette TestClient when the httpx2 client stabilizes.
- [ ] Publish coverage history from CI instead of committing generated artifacts.
- [ ] Add container and deployment configuration when a target platform is selected.
- [ ] Add rate limiting or authentication only when deployment requirements need them.

## Documentation

- [ ] Document an authoritative source for every star-placement rule.
- [ ] Add an architecture diagram: calendar → canonical chart → analysis → API.
