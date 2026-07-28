"""
Service layer cho business logic
"""
from typing import Tuple, Dict, Any
from lasotuvi.Lich_HND import S2L, L2S
from lasotuvi.AmDuong import (
    ngayThangNamCanChi,
    thienCan,
    diaChi,
    timCuc,
    nguHanh
)
from lasotuvi.DiaBan import diaBan, cungDiaBan
from lasotuvi.App import lapDiaBan
from api.models import (
    BirthInfoRequest,
    LunarDateResponse,
    CanChiResponse,
    CungInfo,
    DiaBanResponse,
    ChartResponse
)


class TuViService:
    """Service xử lý các tính toán Tử Vi"""
    
    @staticmethod
    def convert_solar_to_lunar(
        ngay: int,
        thang: int,
        nam: int,
        timezone: int = 7
    ) -> LunarDateResponse:
        """
        Chuyển đổi ngày dương lịch sang âm lịch
        
        Args:
            ngay: Ngày dương lịch
            thang: Tháng dương lịch
            nam: Năm dương lịch
            timezone: Múi giờ
            
        Returns:
            LunarDateResponse
        """
        result = S2L(ngay, thang, nam, timezone)
        
        return LunarDateResponse(
            ngay_am=result[0],
            thang_am=result[1],
            nam_am=result[2],
            thang_nhuan=(result[3] == 1) if len(result) > 3 else False
        )
    
    @staticmethod
    def get_can_chi(
        ngay: int,
        thang: int,
        nam: int,
        duong_lich: bool = True,
        timezone: int = 7
    ) -> CanChiResponse:
        """
        Lấy Can Chi của ngày
        
        Args:
            ngay: Ngày
            thang: Tháng
            nam: Năm
            duong_lich: True nếu là dương lịch
            timezone: Múi giờ
            
        Returns:
            CanChiResponse
        """
        can_thang, can_nam, chi_nam = ngayThangNamCanChi(
            ngay, thang, nam, duong_lich, timezone
        )
        
        return CanChiResponse(
            can_nam=can_nam,
            chi_nam=chi_nam,
            can_thang=can_thang,
            ten_can_nam=thienCan[can_nam]['tenCan'],
            ten_chi_nam=diaChi[chi_nam]['tenChi']
        )
    
    @staticmethod
    def create_dia_ban(birth_info: BirthInfoRequest) -> DiaBanResponse:
        """
        Tạo địa bàn từ thông tin sinh
        
        Args:
            birth_info: Thông tin sinh
            
        Returns:
            DiaBanResponse
        """
        # Chuyển đổi sang âm lịch nếu cần
        if birth_info.duong_lich:
            lunar = S2L(
                birth_info.ngay,
                birth_info.thang,
                birth_info.nam,
                birth_info.timezone
            )
            ngay_am, thang_am, nam_am = lunar[0], lunar[1], lunar[2]
        else:
            ngay_am = birth_info.ngay
            thang_am = birth_info.thang
            nam_am = birth_info.nam
        
        # Tạo địa bàn
        db = lapDiaBan(
            diaBan,
            nn=ngay_am,
            tt=thang_am,
            nnnn=nam_am,
            gioSinh=birth_info.gio,
            gioiTinh=birth_info.gioi_tinh,
            duongLich=False,  # Đã chuyển sang âm lịch rồi
            timeZone=birth_info.timezone
        )
        
        # Chuyển đổi sang response model
        thap_nhi_cung = []
        for i in range(1, 13):
            cung = db.thapNhiCung[i]
            cung_info = CungInfo(
                cung_so=cung.cungSo,
                cung_ten=cung.cungTen,
                cung_chu=getattr(cung, 'cungChu', None),
                hanh_cung=cung.hanhCung,
                cung_am_duong=cung.cungAmDuong,
                cung_sao=cung.cungSao,
                cung_dai_han=getattr(cung, 'cungDaiHan', None),
                cung_tieu_han=getattr(cung, 'cungTieuHan', None),
                cung_than=cung.cungThan,
                tuan_trung=getattr(cung, 'tuanTrung', False),
                triet_lo=getattr(cung, 'trietLo', False)
            )
            thap_nhi_cung.append(cung_info)
        
        # Lấy thông tin cục
        can_chi = TuViService.get_can_chi(
            ngay_am, thang_am, nam_am, False, birth_info.timezone
        )
        cuc_info = timCuc(db.cungMenh, can_chi.can_nam)
        cuc_data = nguHanh(cuc_info)
        
        return DiaBanResponse(
            thang_sinh_am_lich=db.thangSinhAmLich,
            gio_sinh_am_lich=db.gioSinhAmLich,
            cung_menh=db.cungMenh,
            cung_than=db.cungThan,
            cuc=cuc_data['cuc'],
            ten_cuc=cuc_data['tenCuc'],
            thap_nhi_cung=thap_nhi_cung
        )
    
    @staticmethod
    def generate_full_chart(birth_info: BirthInfoRequest) -> ChartResponse:
        """
        Tạo lá số hoàn chỉnh
        
        Args:
            birth_info: Thông tin sinh
            
        Returns:
            ChartResponse
        """
        # Lấy ngày âm lịch
        if birth_info.duong_lich:
            lunar = TuViService.convert_solar_to_lunar(
                birth_info.ngay,
                birth_info.thang,
                birth_info.nam,
                birth_info.timezone
            )
        else:
            lunar = LunarDateResponse(
                ngay_am=birth_info.ngay,
                thang_am=birth_info.thang,
                nam_am=birth_info.nam,
                thang_nhuan=False
            )
        
        # Lấy Can Chi
        can_chi = TuViService.get_can_chi(
            lunar.ngay_am,
            lunar.thang_am,
            lunar.nam_am,
            duong_lich=False,
            timezone=birth_info.timezone
        )
        
        # Tạo địa bàn
        dia_ban = TuViService.create_dia_ban(birth_info)
        
        return ChartResponse(
            birth_info=birth_info,
            lunar_date=lunar,
            can_chi=can_chi,
            dia_ban=dia_ban
        )
    
    @staticmethod
    def analyze_palace(cung_data: dict) -> dict:
        """
        Analyze a palace for strength and characteristics
        
        Args:
            cung_data: Palace data from dia ban
            
        Returns:
            Analysis dict with strength, stars, aspects
        """
        from api.models import PalaceAnalysis
        
        # Get stars in palace
        sao_list = cung_data.get('cung_sao', [])
        main_stars = []
        support_stars = []
        
        for sao in sao_list:
            sao_ten = sao.get('saoTen', '')
            sao_loai = sao.get('saoLoai', 0)
            
            # Main stars (Chính tinh): type 1
            if sao_loai == 1:
                main_stars.append(sao_ten)
            # Support stars
            elif sao_loai in [2, 3, 4, 5]:
                support_stars.append(sao_ten)
        
        # Determine strength based on stars
        strength = "Normal"
        if len(main_stars) >= 2:
            strength = "Strong"
        elif len(main_stars) >= 3:
            strength = "Very Strong"
        elif len(main_stars) == 0:
            strength = "Weak"
        
        # Analyze aspects
        positive_aspects = []
        negative_aspects = []
        
        # Check for specific beneficial stars
        beneficial_stars = ['Tử vi', 'Thiên phủ', 'Thái dương', 'Tham lang', 'Thiên cơ']
        harmful_stars = ['Linh tinh', 'Hỏa tinh', 'Đà la', 'Kình dương', 'Thiên không']
        
        for sao in sao_list:
            sao_ten = sao.get('saoTen', '')
            if sao_ten in beneficial_stars:
                positive_aspects.append(f"Có sao {sao_ten} tốt")
            if sao_ten in harmful_stars:
                negative_aspects.append(f"Có sao {sao_ten} xấu")
        
        return PalaceAnalysis(
            cung_so=cung_data.get('cung_so', 0),
            cung_ten=cung_data.get('cung_ten', ''),
            cung_chu=cung_data.get('cung_chu', ''),
            main_stars=main_stars,
            support_stars=support_stars,
            element=cung_data.get('hanh_cung', ''),
            strength=strength,
            positive_aspects=positive_aspects,
            negative_aspects=negative_aspects
        )
    
    @staticmethod
    def get_palace_by_type(dia_ban: dict, palace_name: str) -> dict:
        """
        Get palace by its name (chu)
        
        Args:
            dia_ban: Dia ban data
            palace_name: Palace name like "Mệnh", "Quan lộc", etc.
            
        Returns:
            Palace data dict
        """
        for cung in dia_ban.get('thap_nhi_cung', []):
            if palace_name in cung.get('cung_chu', ''):
                return cung
        return {}
    
    @staticmethod
    def analyze_chart(birth_info) -> dict:
        """
        Generate detailed chart analysis
        
        Args:
            birth_info: BirthInfoRequest
            
        Returns:
            ChartAnalysisResponse
        """
        from api.models import ChartAnalysisResponse
        
        # Generate full chart first
        chart = TuViService.generate_full_chart(birth_info)
        dia_ban_dict = chart.dia_ban.model_dump()
        
        # Analyze key palaces
        life_palace = TuViService.get_palace_by_type(dia_ban_dict, "Mệnh")
        career_palace = TuViService.get_palace_by_type(dia_ban_dict, "Quan lộc")
        wealth_palace = TuViService.get_palace_by_type(dia_ban_dict, "Tài Bạch")
        
        life_analysis = TuViService.analyze_palace(life_palace) if life_palace else None
        career_analysis = TuViService.analyze_palace(career_palace) if career_palace else None
        wealth_analysis = TuViService.analyze_palace(wealth_palace) if wealth_palace else None
        
        # Overall strength
        overall_strength = "Balanced"
        if life_analysis:
            strength_val = getattr(life_analysis, 'strength', 'Normal')
            if strength_val in ["Strong", "Very Strong"]:
                overall_strength = "Strong"
        
        # Lucky elements based on Cục
        cuc = dia_ban_dict.get('cuc', 0)
        lucky_elements = []
        if cuc in [2, 6]:  # Hỏa
            lucky_elements = ["Hỏa", "Mộc"]
        elif cuc in [3, 7]:  # Thổ
            lucky_elements = ["Thổ", "Hỏa"]
        elif cuc in [4, 8]:  # Kim
            lucky_elements = ["Kim", "Thổ"]
        elif cuc in [5, 9]:  # Thủy
            lucky_elements = ["Thủy", "Kim"]
        
        unlucky_elements = []
        if "Hỏa" in lucky_elements:
            unlucky_elements.append("Thủy")
        if "Thủy" in lucky_elements:
            unlucky_elements.append("Thổ")
        
        # Major life events (placeholder - would need more complex logic)
        major_events = [
            {"age": 20, "event": "Khởi đầu sự nghiệp", "type": "career"},
            {"age": 30, "event": "Thành tựu tài chính", "type": "wealth"},
            {"age": 40, "event": "Ổn định gia đình", "type": "family"},
        ]
        
        return ChartAnalysisResponse(
            birth_info=birth_info,
            life_palace_analysis=life_analysis,
            career_palace_analysis=career_analysis,
            wealth_palace_analysis=wealth_analysis,
            overall_strength=overall_strength,
            lucky_elements=lucky_elements,
            unlucky_elements=unlucky_elements,
            major_life_events=major_events
        )
