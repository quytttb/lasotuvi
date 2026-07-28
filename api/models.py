"""
Pydantic models for API request/response validation
"""
from datetime import date, datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class BirthInfoRequest(BaseModel):
    """Request model cho thông tin sinh"""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "ngay": 15,
                "thang": 8,
                "nam": 1990,
                "gio": 7,
                "gioi_tinh": 1,
                "duong_lich": True,
                "timezone": 7,
                "ten": "Nguyễn Văn A"
            }
        }
    )
    
    ngay: int = Field(..., ge=1, le=31, description="Ngày sinh (1-31)")
    thang: int = Field(..., ge=1, le=12, description="Tháng sinh (1-12)")
    nam: int = Field(..., ge=1900, le=2100, description="Năm sinh (1900-2100)")
    gio: int = Field(..., ge=1, le=12, description="Giờ sinh (1-12, theo địa chi)")
    gioi_tinh: Literal[1, -1] = Field(..., description="Giới tính: 1=Nam, -1=Nữ")
    duong_lich: bool = Field(True, description="True=Dương lịch, False=Âm lịch")
    timezone: int = Field(7, ge=-12, le=14, description="Múi giờ (default: +7 VN)")
    ten: Optional[str] = Field(None, max_length=100, description="Tên người (optional)")
    
    @field_validator('gio')
    @classmethod
    def validate_gio(cls, v: int) -> int:
        """Validate giờ sinh"""
        if not 1 <= v <= 12:
            raise ValueError("Giờ sinh phải từ 1-12 (Tý=1, Sửu=2, ..., Hợi=12)")
        return v
    
    @field_validator('gioi_tinh')
    @classmethod
    def validate_gioi_tinh(cls, v: int) -> int:
        """Validate giới tính"""
        if v not in [1, -1]:
            raise ValueError("Giới tính phải là 1 (Nam) hoặc -1 (Nữ)")
        return v


class LunarDateResponse(BaseModel):
    """Response model cho ngày âm lịch"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    ngay_am: int
    thang_am: int
    nam_am: int
    thang_nhuan: bool = False


class CanChiResponse(BaseModel):
    """Response model cho Can Chi"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    can_nam: int
    chi_nam: int
    can_thang: int
    ten_can_nam: str
    ten_chi_nam: str


class CungInfo(BaseModel):
    """Thông tin một cung trong địa bàn"""
    
    cung_so: int = Field(..., ge=1, le=12)
    cung_ten: str
    cung_chu: Optional[str] = None
    hanh_cung: str
    cung_am_duong: int
    cung_sao: list[dict] = []
    cung_dai_han: Optional[int] = None
    cung_tieu_han: Optional[str] = None
    cung_than: bool = False
    tuan_trung: bool = False
    triet_lo: bool = False


class DiaBanResponse(BaseModel):
    """Response model cho địa bàn hoàn chỉnh"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    thang_sinh_am_lich: int
    gio_sinh_am_lich: int
    cung_menh: int
    cung_than: int
    cuc: int
    ten_cuc: str
    thap_nhi_cung: list[CungInfo]


class ChartResponse(BaseModel):
    """Response model cho lá số hoàn chỉnh"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    birth_info: BirthInfoRequest
    lunar_date: LunarDateResponse
    can_chi: CanChiResponse
    dia_ban: DiaBanResponse
    generated_at: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    """Error response model"""
    
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class BatchChartRequest(BaseModel):
    """Batch request for multiple charts"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    charts: list[BirthInfoRequest] = Field(..., min_length=1, max_length=10, description="List of birth info (max 10)")


class BatchChartResponse(BaseModel):
    """Batch response for multiple charts"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    total: int
    successful: int
    failed: int
    results: list[ChartResponse | ErrorResponse]
    generated_at: datetime = Field(default_factory=datetime.now)


class ChartSummary(BaseModel):
    """Summary of a chart for listing"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    ten: Optional[str]
    ngay_sinh: str
    cung_menh: int
    cuc: str
    chu_menh: str
    generated_at: datetime


class PalaceAnalysis(BaseModel):
    """Analysis of a specific palace"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    cung_so: int
    cung_ten: str
    cung_chu: str
    main_stars: list[str]
    support_stars: list[str]
    element: str
    strength: str  # "Weak", "Normal", "Strong", "Very Strong"
    positive_aspects: list[str]
    negative_aspects: list[str]


class ChartAnalysisResponse(BaseModel):
    """Detailed chart analysis"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    birth_info: BirthInfoRequest
    life_palace_analysis: PalaceAnalysis
    career_palace_analysis: PalaceAnalysis
    wealth_palace_analysis: PalaceAnalysis
    overall_strength: str
    lucky_elements: list[str]
    unlucky_elements: list[str]
    major_life_events: list[dict]
    generated_at: datetime = Field(default_factory=datetime.now)
