"""Pydantic models for API request/response validation (English keys, API v2)."""

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

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
    name: str | None = Field(None, max_length=100, description="Optional display name")
    view_year: int | None = Field(
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

    @model_validator(mode="after")
    def validate_birth_date(self) -> "BirthInfoRequest":
        if self.is_solar:
            try:
                date(self.year, self.month, self.day)
            except ValueError as exc:
                raise ValueError("invalid Gregorian birth date") from exc
        elif self.day > 30:
            raise ValueError("lunar birth day must be in 1..30")
        return self


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

    month_branch: int | None = None
    month_stem_name: str | None = None
    month_branch_name: str | None = None
    day_stem: int | None = None
    day_branch: int | None = None
    day_stem_name: str | None = None
    day_branch_name: str | None = None
    hour_stem: int | None = None
    hour_branch: int | None = None
    hour_stem_name: str | None = None
    hour_branch_name: str | None = None
    year: StemBranchPair | None = None
    month: StemBranchPair | None = None
    day: StemBranchPair | None = None
    hour: StemBranchPair | None = None


class StarInfo(BaseModel):
    id: int
    name: str
    element: str | None = None
    category: int | None = None
    category_label: str | None = None
    miao_wang: str | None = None
    miao_wang_label: str | None = None
    mutagen: str | None = None
    direction: str | None = None
    yin_yang: Any | None = None
    is_chang_sheng: bool = False
    is_auspicious: bool | None = None
    palace_position: int | None = None


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
    palace_name: str | None = None
    palace_element: str
    yin_yang: int
    stem: int | None = None
    stem_name: str | None = None
    stars: list[StarInfo] = Field(default_factory=list)
    interpretations: list[StarInterpretation] = Field(default_factory=list)
    da_xian_age: int | None = None
    xiao_xian_branch: str | None = None
    yue_xian: int | None = None
    is_body_palace: bool = False
    is_xun: bool = False
    is_triet: bool = False


class ChartMeta(BaseModel):
    ben_ming_name: str | None = None
    nayin: str | None = None
    year_yin_yang: str | None = None
    life_yin_yang_status: str | None = None
    ming_zhu: str | None = None
    shen_zhu: str | None = None
    sheng_ke_status: str | None = None
    wu_xing_ju_name: str | None = None
    wu_xing_ju: int | None = None
    view_year: int | None = None
    view_year_branch: str | None = None


class EarthPlateResponse(BaseModel):
    lunar_birth_month: int
    lunar_birth_hour: int
    life_palace: int
    body_palace: int
    wu_xing_ju: int
    wu_xing_ju_name: str
    palaces: list[PalaceInfo]
    formations: list[ChartFormation] = Field(default_factory=list)
    taboo_palaces: list[str] = Field(default_factory=list)
    chart_meta: ChartMeta | None = None


class ChartResponse(BaseModel):
    birth_info: BirthInfoRequest
    lunar_date: LunarDateResponse
    stem_branch: StemBranchResponse
    earth_plate: EarthPlateResponse
    formations: list[ChartFormation] = Field(default_factory=list)
    chart_meta: ChartMeta | None = None
    generated_at: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
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
    life_palace_analysis: PalaceAnalysis | None = None
    career_palace_analysis: PalaceAnalysis | None = None
    wealth_palace_analysis: PalaceAnalysis | None = None
    overall_strength: str
    lucky_elements: list[str]
    unlucky_elements: list[str]
    major_life_events: list[dict]
    generated_at: datetime = Field(default_factory=datetime.now)


class StarCatalogItem(BaseModel):
    id: int
    name: str
    element: str | None = None
    category: int | None = None
    category_label: str | None = None
    direction: str | None = None
    yin_yang: Any | None = None
    is_chang_sheng: bool = False
    description: str | None = None
    meaning: str | None = None


class StarCatalogResponse(BaseModel):
    total: int
    items: list[StarCatalogItem]
    miao_wang: dict[str, str] = MIAO_WANG_LABELS
    category_labels: dict[int, str] = STAR_CATEGORY_LABELS
