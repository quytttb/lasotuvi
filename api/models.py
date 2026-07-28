"""Pydantic models for API request/response validation (English keys, API v2)."""
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


MIAO_WANG_LABELS = {
    "M": "Miếu",
    "V": "Vượng",
    "Đ": "Đắc",
    "D": "Đắc",
    "B": "Bình",
    "H": "Hãm",
}

STAR_CATEGORY_LABELS = {
    1: "major_star",
    2: "minor_star",
    3: "noble_star",
    4: "authority_star",
    5: "blessing_star",
    6: "literary_star",
    7: "pavilion_star",
    8: "peach_blossom_star",
    11: "malefic_star",
    12: "defeat_star",
    13: "obscure_star",
    14: "lust_star",
    15: "punishment_star",
    16: "minor_star",
}


class BirthInfoRequest(BaseModel):
    """Birth data used to generate a chart."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "day": 15,
                "month": 8,
                "year": 1990,
                "hour": 7,
                "gender": 1,
                "is_solar": True,
                "timezone": 7,
                "name": "Nguyễn Văn A",
                "view_year": 2026,
            }
        },
    )

    day: int = Field(..., ge=1, le=31, description="Birth day (1-31)")
    month: int = Field(..., ge=1, le=12, description="Birth month (1-12)")
    year: int = Field(..., ge=1900, le=2100, description="Birth year")
    hour: int = Field(..., ge=1, le=12, description="Birth hour branch index (1=Zi ... 12=Hai)")
    gender: Literal[1, -1] = Field(..., description="1=male, -1=female")
    is_solar: bool = Field(True, description="True if Gregorian date, False if lunar")
    timezone: int = Field(7, ge=-12, le=14, description="Timezone offset (default +7 VN)")
    name: Optional[str] = Field(None, max_length=100, description="Optional display name")
    view_year: Optional[int] = Field(
        None,
        ge=1900,
        le=2200,
        description="Year used for monthly luck overlay (Gregorian)",
    )

    @field_validator("hour")
    @classmethod
    def validate_hour(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("hour must be 1-12 (Zi=1 ... Hai=12)")
        return v


class LunarDateResponse(BaseModel):
    day: int
    month: int
    year: int
    is_leap_month: bool = False


class SolarDateResponse(BaseModel):
    day: int
    month: int
    year: int


class StemBranchPair(BaseModel):
    stem: int
    branch: int
    stem_name: str
    branch_name: str
    label: str


class StemBranchResponse(BaseModel):
    """Full stem–branch for year/month/day/hour."""

    year_stem: int
    year_branch: int
    month_stem: int
    year_stem_name: str
    year_branch_name: str

    month_branch: Optional[int] = None
    month_stem_name: Optional[str] = None
    month_branch_name: Optional[str] = None
    day_stem: Optional[int] = None
    day_branch: Optional[int] = None
    day_stem_name: Optional[str] = None
    day_branch_name: Optional[str] = None
    hour_stem: Optional[int] = None
    hour_branch: Optional[int] = None
    hour_stem_name: Optional[str] = None
    hour_branch_name: Optional[str] = None
    year: Optional[StemBranchPair] = None
    month: Optional[StemBranchPair] = None
    day: Optional[StemBranchPair] = None
    hour: Optional[StemBranchPair] = None


class StarInfo(BaseModel):
    id: int
    name: str
    element: Optional[str] = None
    category: Optional[int] = None
    category_label: Optional[str] = None
    miao_wang: Optional[str] = None
    miao_wang_label: Optional[str] = None
    direction: Optional[str] = None
    yin_yang: Optional[Any] = None
    is_chang_sheng: bool = False
    is_auspicious: Optional[bool] = None
    palace_position: Optional[int] = None


class StarInterpretation(BaseModel):
    """Reading for one star in a palace (from the interpretation knowledge base)."""

    star: str
    interpretation: str


class ChartFormation(BaseModel):
    """Detected chart formation / pattern (cách cục)."""

    code: str
    name: str
    description: str


class PalaceInfo(BaseModel):
    index: int = Field(..., ge=1, le=12)
    branch_name: str
    palace_name: Optional[str] = None
    palace_element: str
    yin_yang: int
    stem: Optional[int] = None
    stem_name: Optional[str] = None
    stars: list[StarInfo] = []
    interpretations: list[StarInterpretation] = []
    da_xian_age: Optional[int] = None
    xiao_xian_branch: Optional[str] = None
    yue_xian: Optional[int] = None
    is_body_palace: bool = False
    is_xun: bool = False
    is_triet: bool = False


class ChartMeta(BaseModel):
    ben_ming_name: Optional[str] = None
    nayin: Optional[str] = None
    year_yin_yang: Optional[str] = None
    life_yin_yang_status: Optional[str] = None
    ming_zhu: Optional[str] = None
    shen_zhu: Optional[str] = None
    sheng_ke_status: Optional[str] = None
    wu_xing_ju_name: Optional[str] = None
    wu_xing_ju: Optional[int] = None
    view_year: Optional[int] = None
    view_year_branch: Optional[str] = None


class EarthPlateResponse(BaseModel):
    lunar_birth_month: int
    lunar_birth_hour: int
    life_palace: int
    body_palace: int
    wu_xing_ju: int
    wu_xing_ju_name: str
    palaces: list[PalaceInfo]
    formations: list[ChartFormation] = []
    chart_meta: Optional[ChartMeta] = None


class ChartResponse(BaseModel):
    birth_info: BirthInfoRequest
    lunar_date: LunarDateResponse
    stem_branch: StemBranchResponse
    earth_plate: EarthPlateResponse
    formations: list[ChartFormation] = []
    chart_meta: Optional[ChartMeta] = None
    generated_at: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class BatchChartRequest(BaseModel):
    charts: list[BirthInfoRequest] = Field(..., min_length=1, max_length=10)


class BatchChartResponse(BaseModel):
    total: int
    successful: int
    failed: int
    results: list[ChartResponse | ErrorResponse]
    generated_at: datetime = Field(default_factory=datetime.now)


class PalaceAnalysis(BaseModel):
    index: int
    branch_name: str
    palace_name: str
    major_stars: list[str]
    support_stars: list[str]
    element: str
    strength: str
    positive_aspects: list[str]
    negative_aspects: list[str]


class ChartAnalysisResponse(BaseModel):
    birth_info: BirthInfoRequest
    life_palace_analysis: Optional[PalaceAnalysis] = None
    career_palace_analysis: Optional[PalaceAnalysis] = None
    wealth_palace_analysis: Optional[PalaceAnalysis] = None
    overall_strength: str
    lucky_elements: list[str]
    unlucky_elements: list[str]
    major_life_events: list[dict]
    generated_at: datetime = Field(default_factory=datetime.now)


class StarCatalogItem(BaseModel):
    id: int
    name: str
    element: Optional[str] = None
    category: Optional[int] = None
    category_label: Optional[str] = None
    direction: Optional[str] = None
    yin_yang: Optional[Any] = None
    is_chang_sheng: bool = False
    description: Optional[str] = None
    meaning: Optional[str] = None


class StarCatalogResponse(BaseModel):
    total: int
    items: list[StarCatalogItem]
    miao_wang: dict[str, str] = MIAO_WANG_LABELS
    category_labels: dict[int, str] = STAR_CATEGORY_LABELS
