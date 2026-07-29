"""FastAPI application — LasoTuVi REST API v2 (English JSON schema)."""

import logging
import os
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api import __version__
from api.models import (
    BatchChartRequest,
    BatchChartResponse,
    BirthInfoRequest,
    ChartAnalysisResponse,
    ChartResponse,
    EarthPlateResponse,
    ErrorResponse,
    HealthResponse,
    LunarDateResponse,
    SolarDateResponse,
    StarCatalogResponse,
    StemBranchResponse,
)
from api.services import TuViService
from lasotuvi.iztro_adapter import (
    IztroRuntimeError,
    initialize_iztro_runtime,
    shutdown_iztro_runtime,
)

logger = logging.getLogger(__name__)


def _environment_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    return default if value is None else value.casefold() in {"1", "true", "yes", "on"}


def _cors_origins() -> list[str]:
    value = os.getenv("LASOTUVI_CORS_ORIGINS", "*")
    return [origin.strip() for origin in value.split(",") if origin.strip()]


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger.info("LasoTuVi API v%s starting", __version__)
    initialize_iztro_runtime()
    try:
        yield
    finally:
        shutdown_iztro_runtime()
        logger.info("LasoTuVi API shutting down")


app = FastAPI(
    title="LasoTuVi API",
    description="""
## Zi Wei Dou Shu (Purple Star Astrology) Chart API

Breaking v2 schema: English field names throughout.

### Features
* Solar ↔ lunar calendar conversion
* Full stem–branch (year / month / day / hour)
* Complete earth plate with structured stars (miao_wang, category)
* Chart formations (cách cục) and palace star interpretations
* Chart meta: natal element, life/body masters, generation/control
* Monthly luck via `view_year`
* Star reference catalog

### Usage
`POST /chart/generate` with birth info. Optional `view_year` for monthly luck.
    """,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={"name": "LasoTuVi Project", "url": "https://github.com/quytttb/lasotuvi"},
    license_info={
        "name": "MIT",
        "url": "https://github.com/quytttb/lasotuvi/blob/master/LICENSE",
    },
)

cors_origins = _cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=(
        _environment_flag("LASOTUVI_CORS_ALLOW_CREDENTIALS") and "*" not in cors_origins
    ),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    start = perf_counter()
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    request.state.request_id = request_id
    response = await call_next(request)
    duration = perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.6f}"
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "%s %s status=%s duration=%.6fs request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration,
        request_id,
    )
    return response


@app.exception_handler(IztroRuntimeError)
async def iztro_exception_handler(request: Request, exc: IztroRuntimeError) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    logger.error("Chart engine error request_id=%s: %s", request_id, exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"error": "Chart engine unavailable", "request_id": request_id},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    logger.exception("Unhandled API error request_id=%s", request_id, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal Server Error", "request_id": request_id},
    )


@app.get("/", tags=["Meta"])
async def root():
    return {
        "message": "Welcome to LasoTuVi API",
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "chart_generation": "/chart/generate",
            "solar_to_lunar": "/calendar/solar-to-lunar",
            "lunar_to_solar": "/calendar/lunar-to-solar",
            "stem_branch": "/calendar/stem-branch",
            "star_catalog": "/info/stars",
        },
    }


@app.get("/health", response_model=HealthResponse, tags=["Meta"])
async def health_check():
    return HealthResponse(status="healthy", version=__version__)


@app.get("/ready", response_model=HealthResponse, tags=["Meta"])
def readiness_check():
    initialize_iztro_runtime()
    return HealthResponse(status="ready", version=__version__)


@app.post("/calendar/solar-to-lunar", response_model=LunarDateResponse, tags=["Calendar"])
async def solar_to_lunar(day: int, month: int, year: int, timezone: int = 7):
    try:
        return TuViService.convert_solar_to_lunar(day, month, year, timezone)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/calendar/lunar-to-solar", response_model=SolarDateResponse, tags=["Calendar"])
async def lunar_to_solar(
    day: int,
    month: int,
    year: int,
    is_leap_month: bool = False,
    timezone: int = 7,
):
    try:
        return TuViService.convert_lunar_to_solar(day, month, year, is_leap_month, timezone)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/calendar/stem-branch", response_model=StemBranchResponse, tags=["Calendar"])
async def get_stem_branch(
    day: int,
    month: int,
    year: int,
    is_solar: bool = True,
    timezone: int = 7,
    hour: int | None = None,
):
    try:
        return TuViService.get_stem_branch(day, month, year, is_solar, timezone, hour)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# Backward-compatible alias
@app.post(
    "/calendar/can-chi", response_model=StemBranchResponse, tags=["Calendar"], deprecated=True
)
async def get_can_chi_alias(
    day: int | None = None,
    month: int | None = None,
    year: int | None = None,
    ngay: int | None = None,
    thang: int | None = None,
    nam: int | None = None,
    is_solar: bool = True,
    duong_lich: bool | None = None,
    timezone: int = 7,
    hour: int | None = None,
    gio: int | None = None,
):
    """Deprecated: use `/calendar/stem-branch`."""
    d = day if day is not None else ngay
    m = month if month is not None else thang
    y = year if year is not None else nam
    if d is None or m is None or y is None:
        raise HTTPException(status_code=422, detail="day/month/year required")
    solar = is_solar if duong_lich is None else duong_lich
    h = hour if hour is not None else gio
    return TuViService.get_stem_branch(d, m, y, solar, timezone, h)


@app.post("/chart/earth-plate", response_model=EarthPlateResponse, tags=["Chart"])
def generate_earth_plate(birth_info: BirthInfoRequest):
    try:
        return TuViService.create_earth_plate(birth_info)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/chart/dia-ban", response_model=EarthPlateResponse, tags=["Chart"], deprecated=True)
def generate_dia_ban_alias(birth_info: BirthInfoRequest):
    """Deprecated: use `/chart/earth-plate`."""
    return generate_earth_plate(birth_info)


@app.post("/chart/generate", response_model=ChartResponse, tags=["Chart"])
def generate_chart(birth_info: BirthInfoRequest):
    try:
        start = perf_counter()
        chart = TuViService.generate_full_chart(birth_info)
        logger.debug("Chart generated in %.3fs", perf_counter() - start)
        return chart
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/chart/analyze", response_model=ChartAnalysisResponse, tags=["Chart", "Analysis"])
def analyze_chart(birth_info: BirthInfoRequest):
    return TuViService.analyze_chart(birth_info)


@app.post("/chart/batch", response_model=BatchChartResponse, tags=["Chart", "Batch"])
def generate_batch_charts(batch_request: BatchChartRequest):
    results = []
    successful = failed = 0
    for birth_info in batch_request.charts:
        try:
            results.append(TuViService.generate_full_chart(birth_info))
            successful += 1
        except Exception:
            logger.exception("Batch chart generation failed")
            results.append(ErrorResponse(error="Chart generation failed"))
            failed += 1
    return BatchChartResponse(
        total=len(batch_request.charts),
        successful=successful,
        failed=failed,
        results=results,
    )


@app.get("/info/hour-branches", tags=["Info"])
async def get_hour_branches():
    return TuViService.get_hour_branch_info()


@app.get("/info/gio-chi", tags=["Info"], deprecated=True)
async def get_gio_chi_alias():
    """Deprecated: use `/info/hour-branches`."""
    return TuViService.get_hour_branch_info()


@app.get("/info/stars", response_model=StarCatalogResponse, tags=["Info"])
async def get_star_catalog():
    return TuViService.get_star_catalog()


@app.get("/info/sao", response_model=StarCatalogResponse, tags=["Info"], deprecated=True)
async def get_sao_alias():
    """Deprecated: use `/info/stars`."""
    return TuViService.get_star_catalog()


@app.get("/info/elements", tags=["Info"])
async def get_elements_info():
    from lasotuvi.stem_branch import five_element

    elements = []
    for key in ("K", "M", "T", "H", "O"):
        elem = five_element(key)
        elements.append(
            {
                "id": elem["id"],
                "key": key,
                "name": elem["element_name"],
                "wu_xing_ju": elem["wu_xing_ju"],
                "wu_xing_ju_name": elem["wu_xing_ju_name"],
            }
        )
    return {
        "title": "Five Elements (Ngũ Hành)",
        "elements": elements,
        "cycle": {
            "generation": "Wood → Fire → Earth → Metal → Water → Wood",
            "control": "Wood → Earth → Water → Fire → Metal → Wood",
        },
    }


@app.get("/info/stem-branch", tags=["Info"])
async def get_stem_branch_info():
    from lasotuvi.stem_branch import EARTHLY_BRANCHES, HEAVENLY_STEMS

    stems = []
    for i in range(1, 11):
        can = HEAVENLY_STEMS[i]
        stems.append(
            {
                "id": i,
                "name": can["stem_name"],
                "element": can.get("five_element"),
            }
        )
    branches = []
    for i in range(1, 13):
        chi = EARTHLY_BRANCHES[i]
        branches.append(
            {
                "id": i,
                "name": chi["branch_name"],
                "ming_zhu": chi.get("ming_zhu"),
                "shen_zhu": chi.get("shen_zhu"),
                "element": chi.get("element_name"),
            }
        )
    return {
        "title": "Heavenly Stems & Earthly Branches",
        "heavenly_stems": {"count": 10, "items": stems},
        "earthly_branches": {"count": 12, "items": branches},
    }


@app.get("/info/can-chi", tags=["Info"], deprecated=True)
async def get_can_chi_info_alias():
    return await get_stem_branch_info()


@app.get("/stats", tags=["Info"])
async def get_stats():
    return {
        "api_version": __version__,
        "status": "operational",
        "schema": "english_v2_breaking",
        "features": [
            "Solar ↔ Lunar conversion",
            "Full stem–branch",
            "Earth plate + chart meta",
            "Structured stars + miao_wang",
            "Chart formations + palace interpretations",
            "Monthly luck via view_year",
            "Star catalog",
            "Chart analysis",
            "Batch processing",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
