"""
FastAPI main application
LasoTuVi REST API - Vietnamese Astrology Chart Generation
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
from datetime import datetime

from api.models import (
    BirthInfoRequest,
    ChartResponse,
    LunarDateResponse,
    CanChiResponse,
    DiaBanResponse,
    HealthResponse,
    ErrorResponse,
    ChartAnalysisResponse,
    BatchChartRequest,
    BatchChartResponse
)
from api.services import TuViService
from api import __version__


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    print(f"🚀 LasoTuVi API v{__version__} starting up...")
    yield
    # Shutdown
    print("👋 LasoTuVi API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="LasoTuVi API",
    description="""
    ## Vietnamese Astrology Chart Generation API
    
    Powerful REST API for generating Vietnamese Tử Vi (Purple Star Astrology) charts.
    
    ### Features
    * 🌙 Solar to Lunar calendar conversion
    * 📅 Can Chi (Heavenly Stems & Earthly Branches) calculations
    * ⭐ Complete astrological chart generation
    * 🔍 Detailed palace (cung) information
    * 🎯 Star positions and qualities
    
    ### Tech Stack
    * FastAPI 0.115+
    * Pydantic v2 for validation
    * Python 3.12+
    * lasotuvi core library
    
    ### Usage
    Use the `/chart/generate` endpoint to create a complete chart from birth information.
    """,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={
        "name": "LasoTuVi Project",
        "url": "https://github.com/quytttb/lasotuvi",
    },
    license_info={
        "name": "License",
        "url": "https://github.com/quytttb/lasotuvi/blob/master/LICENSE",
    },
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    """Log all requests"""
    import time
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log request
    print(f"📝 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc)
        }
    )


# Routes
@app.get(
    "/",
    summary="Root endpoint",
    description="Welcome message and API information"
)
async def root():
    """Root endpoint"""
    return {
        "message": "🌟 Welcome to LasoTuVi API",
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "chart_generation": "/chart/generate",
            "lunar_conversion": "/calendar/solar-to-lunar",
            "can_chi": "/calendar/can-chi"
        }
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check API health status"
)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=__version__
    )


@app.post(
    "/calendar/solar-to-lunar",
    response_model=LunarDateResponse,
    summary="Convert solar to lunar date",
    description="Convert Gregorian calendar date to Vietnamese lunar calendar date",
    tags=["Calendar"]
)
async def solar_to_lunar(
    ngay: int,
    thang: int,
    nam: int,
    timezone: int = 7
):
    """
    Convert solar (Gregorian) date to lunar (Vietnamese) date
    
    **Parameters:**
    * `ngay`: Day (1-31)
    * `thang`: Month (1-12)
    * `nam`: Year (1900-2100)
    * `timezone`: Timezone offset (default: 7 for Vietnam)
    
    **Returns:**
    * Lunar date with leap month information
    """
    try:
        return TuViService.convert_solar_to_lunar(ngay, thang, nam, timezone)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date or conversion error: {str(e)}"
        )


@app.post(
    "/calendar/can-chi",
    response_model=CanChiResponse,
    summary="Get Can Chi",
    description="Get Heavenly Stems and Earthly Branches for a date",
    tags=["Calendar"]
)
async def get_can_chi(
    ngay: int,
    thang: int,
    nam: int,
    duong_lich: bool = True,
    timezone: int = 7
):
    """
    Get Can Chi (Heavenly Stems & Earthly Branches) for a date
    
    **Parameters:**
    * `ngay`: Day
    * `thang`: Month
    * `nam`: Year
    * `duong_lich`: True for solar calendar, False for lunar
    * `timezone`: Timezone offset
    
    **Returns:**
    * Can Chi information with Vietnamese names
    """
    try:
        return TuViService.get_can_chi(ngay, thang, nam, duong_lich, timezone)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error calculating Can Chi: {str(e)}"
        )


@app.post(
    "/chart/dia-ban",
    response_model=DiaBanResponse,
    summary="Generate Dia Ban",
    description="Generate the astrological chart base (Dia Ban) with 12 palaces",
    tags=["Chart"]
)
async def generate_dia_ban(birth_info: BirthInfoRequest):
    """
    Generate Dia Ban (地盤 - Earth Plate)
    
    The Dia Ban is the foundation of a Tử Vi chart, containing:
    * 12 palaces (Thập Nhị Cung)
    * Palace attributes (Five Elements, Yin/Yang)
    * Star positions
    * Life palace (Cung Mệnh) determination
    
    **Request Body:**
    * Complete birth information (date, time, gender)
    
    **Returns:**
    * Detailed Dia Ban with all 12 palaces
    """
    try:
        return TuViService.create_dia_ban(birth_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating Dia Ban: {str(e)}"
        )


@app.post(
    "/chart/generate",
    response_model=ChartResponse,
    summary="Generate Complete Chart",
    description="Generate a complete Vietnamese Tử Vi astrological chart",
    tags=["Chart"],
    status_code=status.HTTP_200_OK
)
async def generate_chart(birth_info: BirthInfoRequest):
    """
    Generate Complete Tử Vi Chart (紫微斗數)
    
    This endpoint generates a complete Vietnamese astrological chart including:
    
    **Chart Components:**
    * 📅 Lunar calendar conversion
    * 🔢 Can Chi (Heavenly Stems & Earthly Branches)
    * 🏠 12 Palaces (Thập Nhị Cung) with detailed information
    * ⭐ Star positions and qualities
    * 🎯 Life Palace (Cung Mệnh) analysis
    * 🌟 Main stars (Chính tinh) placement
    * ✨ Supporting stars (Phụ tinh) placement
    
    **Request Body Example:**
    ```json
    {
        "ngay": 15,
        "thang": 8,
        "nam": 1990,
        "gio": 7,
        "gioi_tinh": 1,
        "duong_lich": true,
        "timezone": 7,
        "ten": "Nguyễn Văn A"
    }
    ```
    
    **Returns:**
    * Complete chart with all astrological information
    * Birth info, lunar date, Can Chi, and Dia Ban
    * Timestamp of generation
    
    **Note:**
    * `gio`: Hour in Vietnamese zodiac (1=Tý, 2=Sửu, ..., 12=Hợi)
    * `gioi_tinh`: 1 for male, -1 for female
    * Chart calculation uses traditional Vietnamese Tử Vi algorithms
    """
    try:
        start_time = time.time()
        
        chart = TuViService.generate_full_chart(birth_info)
        
        elapsed = time.time() - start_time
        print(f"⏱️  Chart generated in {elapsed:.3f}s for {birth_info.ten or 'unnamed'}")
        
        return chart
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating chart: {str(e)}"
        )


# Additional utility endpoints
@app.get(
    "/info/gio-chi",
    summary="Get hour zodiac info",
    description="Get Vietnamese zodiac hour information",
    tags=["Info"]
)
async def get_gio_chi_info():
    """Get Vietnamese zodiac hour (Địa Chi) information"""
    from lasotuvi.AmDuong import diaChi
    
    gio_info = []
    for i in range(1, 13):
        gio_info.append({
            "id": i,
            "ten": diaChi[i]['tenChi'],
            "time_range": f"{(i-1)*2+23}h-{(i-1)*2+1}h" if i == 1 
                         else f"{(i-1)*2-1}h-{(i-1)*2+1}h"
        })
    
    return {
        "title": "Địa Chi - Vietnamese Zodiac Hours",
        "description": "12 traditional time periods in Vietnamese astrology",
        "hours": gio_info
    }


@app.post(
    "/chart/analyze",
    response_model=ChartAnalysisResponse,
    summary="Analyze Chart",
    description="Generate detailed analysis of a Tử Vi chart with interpretations",
    tags=["Chart", "Analysis"]
)
async def analyze_chart(birth_info: BirthInfoRequest):
    """
    Analyze a Tử Vi chart with detailed interpretations
    
    This endpoint provides in-depth analysis including:
    - Life Palace (Cung Mệnh) analysis
    - Career Palace (Quan Lộc) analysis  
    - Wealth Palace (Tài Bạch) analysis
    - Overall chart strength
    - Lucky/Unlucky elements
    - Major life events predictions
    
    **Note:** This is a basic analysis. Full interpretation requires expert knowledge.
    """
    try:
        analysis = TuViService.analyze_chart(birth_info)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing chart: {str(e)}"
        )


@app.post(
    "/chart/batch",
    response_model=BatchChartResponse,
    summary="Generate Multiple Charts",
    description="Generate multiple charts in one request (max 10)",
    tags=["Chart", "Batch"]
)
async def generate_batch_charts(batch_request: BatchChartRequest):
    """
    Generate multiple charts in batch
    
    **Limitations:**
    * Maximum 10 charts per request
    * Failed charts will be included in results with error details
    
    **Use case:**
    * Generate charts for family members
    * Compare multiple birth dates
    * Bulk chart generation
    """
    results = []
    successful = 0
    failed = 0
    
    for birth_info in batch_request.charts:
        try:
            chart = TuViService.generate_full_chart(birth_info)
            results.append(chart)
            successful += 1
        except Exception as e:
            results.append(ErrorResponse(
                error="Chart generation failed",
                detail=str(e)
            ))
            failed += 1
    
    return BatchChartResponse(
        total=len(batch_request.charts),
        successful=successful,
        failed=failed,
        results=results
    )


@app.get(
    "/info/elements",
    summary="Get Five Elements Info",
    description="Get information about Wu Xing (Five Elements)",
    tags=["Info"]
)
async def get_elements_info():
    """Get Five Elements (Ngũ Hành) information"""
    from lasotuvi.AmDuong import nguHanh as get_ngu_hanh
    
    elements = []
    for key, name in [('K', 'Kim'), ('M', 'Moc'), ('T', 'Thuy'), ('H', 'Hoa'), ('O', 'Tho')]:
        elem = get_ngu_hanh(key)
        elements.append({
            "id": elem['id'],
            "key": key,
            "name": elem['tenHanh'],
            "cuc": elem['cuc'],
            "ten_cuc": elem['tenCuc']
        })
    
    return {
        "title": "Ngũ Hành - Five Elements",
        "description": "The five elements in Vietnamese astrology",
        "elements": elements,
        "cycle": {
            "generation": "Mộc → Hỏa → Thổ → Kim → Thủy → Mộc",
            "destruction": "Mộc → Thổ → Thủy → Hỏa → Kim → Mộc"
        }
    }


@app.get(
    "/info/can-chi",
    summary="Get Can Chi Info",
    description="Get information about Heavenly Stems and Earthly Branches",
    tags=["Info"]
)
async def get_can_chi_info():
    """Get Can Chi (Thiên Can Địa Chi) information"""
    from lasotuvi.AmDuong import thienCan, diaChi
    
    can_list = []
    for i in range(1, 11):
        can = thienCan[i] if i < len(thienCan) else {}
        can_list.append({
            "id": i,
            "name": can.get('tenCan', '') if isinstance(can, dict) else '',
            "element": can.get('nguHanh', '') if isinstance(can, dict) else ''
        })
    
    chi_list = []
    for i in range(1, 13):
        chi = diaChi[i] if i < len(diaChi) else {}
        chi_list.append({
            "id": i,
            "name": chi.get('tenChi', '') if isinstance(chi, dict) else '',
            "zodiac": chi.get('con', '') if isinstance(chi, dict) else '',
            "element": chi.get('nguHanh', '') if isinstance(chi, dict) else ''
        })
    
    return {
        "title": "Thiên Can Địa Chi",
        "description": "Heavenly Stems and Earthly Branches",
        "thien_can": {
            "count": 10,
            "items": can_list
        },
        "dia_chi": {
            "count": 12,
            "items": chi_list
        }
    }


@app.get(
    "/stats",
    summary="API Statistics",
    description="Get API usage statistics",
    tags=["Info"]
)
async def get_stats():
    """Get API statistics"""
    # This is a placeholder - in production, you'd track real stats
    return {
        "api_version": __version__,
        "status": "operational",
        "endpoints": {
            "total": 15,
            "chart_generation": 4,
            "calendar": 2,
            "analysis": 1,
            "info": 5
        },
        "features": [
            "Solar to Lunar conversion",
            "Can Chi calculation",
            "Complete chart generation",
            "Chart analysis",
            "Batch processing",
            "Five Elements info",
            "Can Chi reference"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting LasoTuVi API server...")
    print(f"📚 API docs: http://localhost:8000/docs")
    print(f"📖 ReDoc: http://localhost:8000/redoc")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
