"""Service layer for Zi Wei Dou Shu chart calculations."""
from __future__ import annotations

from datetime import date
from typing import Any, Optional

from lasotuvi.analysis import ChartAnalyzer
from lasotuvi.stem_branch import (
    day_stem_branch,
    EARTHLY_BRANCHES,
    month_year_stem_branch,
    five_element,
    HEAVENLY_STEMS,
    find_wu_xing_ju,
)
from lasotuvi.chart_builder import build_earth_plate
from lasotuvi.earth_plate import EarthPlate
from lasotuvi.lunar_calendar import julian_day_from_date, lunar_to_solar, solar_to_lunar
from lasotuvi.heaven_plate import HeavenPlate

from api.models import (
    MIAO_WANG_LABELS,
    STAR_CATEGORY_LABELS,
    BirthInfoRequest,
    ChartAnalysisResponse,
    ChartFormation,
    ChartMeta,
    ChartResponse,
    EarthPlateResponse,
    LunarDateResponse,
    PalaceAnalysis,
    PalaceInfo,
    SolarDateResponse,
    StarCatalogItem,
    StarCatalogResponse,
    StarInfo,
    StarInterpretation,
    StemBranchPair,
    StemBranchResponse,
)
from api.star_catalog import SAO_CATALOG

HOUR_BRANCH_RANGES: dict[int, str] = {
    1: "23h - 1h",
    2: "1h - 3h",
    3: "3h - 5h",
    4: "5h - 7h",
    5: "7h - 9h",
    6: "9h - 11h",
    7: "11h - 13h",
    8: "13h - 15h",
    9: "15h - 17h",
    10: "17h - 19h",
    11: "19h - 21h",
    12: "21h - 23h",
}

_STEM_OF_YIN: dict[int, int] = {
    1: 3,
    2: 5,
    3: 7,
    4: 9,
    5: 1,
    6: 3,
    7: 5,
    8: 7,
    9: 9,
    10: 1,
}


def _pair(stem: int, branch: int) -> StemBranchPair:
    stem_name = HEAVENLY_STEMS[stem]["stem_name"]
    branch_name = EARTHLY_BRANCHES[branch]["branch_name"]
    return StemBranchPair(
        stem=stem,
        branch=branch,
        stem_name=stem_name,
        branch_name=branch_name,
        label=f"{stem_name} {branch_name}",
    )


def _normalize_star(raw: dict[str, Any]) -> StarInfo:
    star_id = int(raw.get("star_id") or raw.get("id") or 0)
    name = raw.get("name") or raw.get("saoTen") or ""
    category = raw.get("category", raw.get("saoLoai"))
    try:
        category_int = int(category) if category is not None else None
    except (TypeError, ValueError):
        category_int = None

    miao_wang = raw.get("miao_wang") or raw.get("saoDacTinh")
    if miao_wang == "D":
        miao_wang = "Đ"

    is_auspicious: Optional[bool] = None
    if category_int is not None:
        is_auspicious = category_int < 10

    return StarInfo(
        id=star_id,
        name=name,
        element=raw.get("element") or raw.get("saoNguHanh"),
        category=category_int,
        category_label=STAR_CATEGORY_LABELS.get(category_int) if category_int is not None else None,
        miao_wang=miao_wang,
        miao_wang_label=MIAO_WANG_LABELS.get(miao_wang) if miao_wang else None,
        direction=raw.get("direction") or raw.get("saoPhuongVi") or None,
        yin_yang=raw.get("yin_yang", raw.get("saoAmDuong")),
        is_chang_sheng=bool(raw.get("is_chang_sheng") or raw.get("vongTrangSinh")),
        is_auspicious=is_auspicious,
        palace_position=raw.get("palace_position") or raw.get("saoViTriCung"),
    )


def palace_stems(year_stem: int) -> dict[int, int]:
    """Stem of each palace via Five Tigers escape (Ngũ Hổ Độn)."""
    stem_yin = _STEM_OF_YIN[year_stem]
    result: dict[int, int] = {}
    for i in range(1, 13):
        offset = (i - 3 + 12) % 12
        result[i] = ((stem_yin - 1 + offset) % 10) + 1
    return result


def yue_xian_map(
    xiao_xian_palace: int,
    birth_month: int,
    birth_hour_branch: int,
) -> dict[int, int]:
    """Return {palace_index: month_number} for monthly luck overlay."""
    month_1_palace = (
        (xiao_xian_palace - 1 - (birth_month - 1) + (birth_hour_branch - 1) + 120) % 12
    ) + 1
    result: dict[int, int] = {}
    for month in range(1, 13):
        palace = ((month_1_palace - 1 + (month - 1) + 120) % 12) + 1
        result[palace] = month
    return result


class TuViService:
    """Zi Wei chart service."""

    @staticmethod
    def convert_solar_to_lunar(
        day: int, month: int, year: int, timezone: int = 7
    ) -> LunarDateResponse:
        result = solar_to_lunar(day, month, year, timezone)
        return LunarDateResponse(
            day=result[0],
            month=result[1],
            year=result[2],
            is_leap_month=(result[3] == 1) if len(result) > 3 else False,
        )

    @staticmethod
    def convert_lunar_to_solar(
        day: int,
        month: int,
        year: int,
        is_leap_month: bool = False,
        timezone: int = 7,
    ) -> SolarDateResponse:
        result = lunar_to_solar(day, month, year, 1 if is_leap_month else 0, timezone)
        return SolarDateResponse(day=result[0], month=result[1], year=result[2])

    @staticmethod
    def get_stem_branch(
        day: int,
        month: int,
        year: int,
        is_solar: bool = True,
        timezone: int = 7,
        hour: Optional[int] = None,
    ) -> StemBranchResponse:
        if is_solar:
            lunar = solar_to_lunar(day, month, year, timezone)
            lunar_day, lunar_month, lunar_year = lunar[0], lunar[1], lunar[2]
            solar_day, solar_month, solar_year = day, month, year
        else:
            lunar_day, lunar_month, lunar_year = day, month, year
            solar = lunar_to_solar(lunar_day, lunar_month, lunar_year, 0, timezone)
            solar_day, solar_month, solar_year = solar[0], solar[1], solar[2]

        month_stem, year_stem, year_branch = month_year_stem_branch(
            lunar_day, lunar_month, lunar_year, False, timezone
        )
        month_branch = lunar_month
        day_stem, day_branch = day_stem_branch(
            solar_day, solar_month, solar_year, True, timezone
        )

        hour_branch = hour
        hour_stem = None
        if hour_branch is not None:
            hour_stem = (
                (julian_day_from_date(solar_day, solar_month, solar_year) - 1) * 2 % 10
                + hour_branch
            ) % 10
            if hour_stem == 0:
                hour_stem = 10

        year_pair = _pair(year_stem, year_branch)
        month_pair = _pair(month_stem, month_branch)
        day_pair = _pair(day_stem, day_branch)
        hour_pair = _pair(hour_stem, hour_branch) if hour_stem and hour_branch else None

        return StemBranchResponse(
            year_stem=year_stem,
            year_branch=year_branch,
            month_stem=month_stem,
            year_stem_name=year_pair.stem_name,
            year_branch_name=year_pair.branch_name,
            month_branch=month_branch,
            month_stem_name=month_pair.stem_name,
            month_branch_name=month_pair.branch_name,
            day_stem=day_stem,
            day_branch=day_branch,
            day_stem_name=day_pair.stem_name,
            day_branch_name=day_pair.branch_name,
            hour_stem=hour_stem,
            hour_branch=hour_branch,
            hour_stem_name=hour_pair.stem_name if hour_pair else None,
            hour_branch_name=hour_pair.branch_name if hour_pair else None,
            year=year_pair,
            month=month_pair,
            day=day_pair,
            hour=hour_pair,
        )

    @staticmethod
    def _resolve_lunar(birth: BirthInfoRequest) -> tuple[int, int, int, bool]:
        if birth.is_solar:
            lunar = solar_to_lunar(birth.day, birth.month, birth.year, birth.timezone)
            return lunar[0], lunar[1], lunar[2], bool(lunar[3] == 1)
        return birth.day, birth.month, birth.year, False

    @staticmethod
    def _build_chart_meta(
        birth: BirthInfoRequest,
        lunar_day: int,
        lunar_month: int,
        lunar_year: int,
        plate: EarthPlate,
        year_stem: int,
        year_branch: int,
        view_year: Optional[int],
    ) -> ChartMeta:
        if birth.is_solar:
            d, m, y = birth.day, birth.month, birth.year
        else:
            solar = lunar_to_solar(lunar_day, lunar_month, lunar_year, 0, birth.timezone)
            d, m, y = solar[0], solar[1], solar[2]

        heaven = HeavenPlate(
            d,
            m,
            y,
            birth.hour,
            birth.gender,
            birth.name or "",
            plate,
            is_solar=True,
            timezone=birth.timezone,
        )

        view_year_branch = None
        if view_year is not None:
            chi = ((view_year - 4) % 12) + 1
            view_year_branch = EARTHLY_BRANCHES[chi]["branch_name"]

        return ChartMeta(
            ben_ming_name=getattr(heaven, "ben_ming_name", None),
            nayin=getattr(heaven, "nayin", None),
            year_yin_yang=getattr(heaven, "year_stem_yin_yang", None),
            life_yin_yang_status=getattr(heaven, "life_yin_yang_status", None),
            ming_zhu=EARTHLY_BRANCHES[plate.life_palace]["ming_zhu"],
            shen_zhu=EARTHLY_BRANCHES[year_branch]["shen_zhu"],
            sheng_ke_status=getattr(heaven, "sheng_ke_status", None),
            wu_xing_ju_name=getattr(heaven, "wu_xing_ju_name", None),
            wu_xing_ju=five_element(find_wu_xing_ju(plate.life_palace, year_stem))["wu_xing_ju"],
            view_year=view_year,
            view_year_branch=view_year_branch,
        )

    @staticmethod
    def create_earth_plate(birth: BirthInfoRequest) -> EarthPlateResponse:
        lunar_day, lunar_month, lunar_year, _ = TuViService._resolve_lunar(birth)

        plate = build_earth_plate(
            birth.day,
            birth.month,
            birth.year,
            birth.hour,
            birth.gender,
            birth.is_solar,
            birth.timezone,
        )

        month_stem, year_stem, year_branch = month_year_stem_branch(
            lunar_day, lunar_month, lunar_year, False, birth.timezone
        )
        stems = palace_stems(year_stem)

        view_year = birth.view_year or date.today().year
        view_branch = ((view_year - 4) % 12) + 1
        view_branch_name = EARTHLY_BRANCHES[view_branch]["branch_name"]

        xiao_xian_palace = plate.life_palace
        for i in range(1, 13):
            if getattr(plate.palaces[i], "xiao_xian_branch", None) == view_branch_name:
                xiao_xian_palace = i
                break

        month_map = yue_xian_map(xiao_xian_palace, lunar_month, birth.hour)

        analyzer = ChartAnalyzer(plate)
        formations = [ChartFormation(**f) for f in analyzer.detect_formations()]
        palace_readings = analyzer.interpret_all_palaces()

        palaces: list[PalaceInfo] = []
        for i in range(1, 13):
            palace = plate.palaces[i]
            raw_stars = getattr(palace, "stars", []) or []
            stars = [_normalize_star(s if isinstance(s, dict) else s.__dict__) for s in raw_stars]
            stem = stems[i]
            palace_name = getattr(palace, "palace_name", None)
            readings = palace_readings.get(palace_name or "", [])
            palaces.append(
                PalaceInfo(
                    index=palace.index,
                    branch_name=palace.branch_name,
                    palace_name=palace_name,
                    palace_element=palace.palace_element,
                    yin_yang=palace.yin_yang,
                    stem=stem,
                    stem_name=HEAVENLY_STEMS[stem]["stem_name"],
                    stars=stars,
                    interpretations=[StarInterpretation(**r) for r in readings],
                    da_xian_age=getattr(palace, "da_xian_age", None),
                    xiao_xian_branch=getattr(palace, "xiao_xian_branch", None),
                    yue_xian=month_map.get(i),
                    is_body_palace=bool(getattr(palace, "is_body_palace", False)),
                    is_xun=bool(getattr(palace, "is_xun", False)),
                    is_triet=bool(getattr(palace, "is_triet", False)),
                )
            )

        wu_xing_ju_key = find_wu_xing_ju(plate.life_palace, year_stem)
        wu_xing_ju_data = five_element(wu_xing_ju_key)
        chart_meta = TuViService._build_chart_meta(
            birth, lunar_day, lunar_month, lunar_year, plate, year_stem, year_branch, view_year
        )

        return EarthPlateResponse(
            lunar_birth_month=plate.lunar_birth_month,
            lunar_birth_hour=plate.lunar_birth_hour,
            life_palace=plate.life_palace,
            body_palace=plate.body_palace,
            wu_xing_ju=wu_xing_ju_data["wu_xing_ju"],
            wu_xing_ju_name=wu_xing_ju_data["wu_xing_ju_name"],
            palaces=palaces,
            formations=formations,
            chart_meta=chart_meta,
        )

    @staticmethod
    def generate_full_chart(birth: BirthInfoRequest) -> ChartResponse:
        lunar_day, lunar_month, lunar_year, is_leap = TuViService._resolve_lunar(birth)
        lunar = LunarDateResponse(
            day=lunar_day, month=lunar_month, year=lunar_year, is_leap_month=is_leap
        )
        stem_branch = TuViService.get_stem_branch(
            birth.day,
            birth.month,
            birth.year,
            is_solar=birth.is_solar,
            timezone=birth.timezone,
            hour=birth.hour,
        )
        earth_plate = TuViService.create_earth_plate(birth)
        return ChartResponse(
            birth_info=birth,
            lunar_date=lunar,
            stem_branch=stem_branch,
            earth_plate=earth_plate,
            formations=earth_plate.formations,
            chart_meta=earth_plate.chart_meta,
        )

    @staticmethod
    def get_star_catalog() -> StarCatalogResponse:
        items = [
            StarCatalogItem(
                id=s["id"],
                name=s["ten"],
                element=s.get("ngu_hanh"),
                category=s.get("loai"),
                category_label=STAR_CATEGORY_LABELS.get(s["loai"]) if s.get("loai") is not None else None,
                direction=s.get("phuong_vi"),
                yin_yang=s.get("am_duong"),
                is_chang_sheng=bool(s.get("vong_trang_sinh")),
                description=s.get("mo_ta"),
                meaning=s.get("y_nghia"),
            )
            for s in SAO_CATALOG
        ]
        return StarCatalogResponse(total=len(items), items=items)

    @staticmethod
    def get_hour_branch_info() -> dict[str, Any]:
        hours = []
        for i in range(1, 13):
            hours.append(
                {
                    "id": i,
                    "name": EARTHLY_BRANCHES[i]["branch_name"],
                    "time_range": HOUR_BRANCH_RANGES[i],
                    "ming_zhu": EARTHLY_BRANCHES[i]["ming_zhu"],
                    "shen_zhu": EARTHLY_BRANCHES[i]["shen_zhu"],
                }
            )
        return {
            "title": "Earthly Branches — birth hours",
            "description": "12 traditional two-hour periods (Zi starts at 23h)",
            "hours": hours,
        }

    @staticmethod
    def analyze_palace(palace_data: dict) -> PalaceAnalysis:
        star_list = palace_data.get("stars", [])
        major_stars: list[str] = []
        support_stars: list[str] = []

        for star in star_list:
            if isinstance(star, StarInfo):
                name, category = star.name, star.category or 0
            elif isinstance(star, dict):
                name = star.get("name") or ""
                category = star.get("category") or 0
            else:
                continue
            if category == 1:
                major_stars.append(name)
            elif category in [2, 3, 4, 5, 6, 7, 8]:
                support_stars.append(name)

        strength = "Normal"
        if len(major_stars) == 0:
            strength = "Weak"
        elif len(major_stars) >= 3:
            strength = "Very Strong"
        elif len(major_stars) >= 2:
            strength = "Strong"

        beneficial = {"Tử vi", "Thiên phủ", "Thái Dương", "Tham lang", "Thiên cơ"}
        harmful = {"Linh tinh", "Hỏa tinh", "Đà la", "Kình dương", "Thiên không"}
        positive, negative = [], []
        for star in star_list:
            name = star.name if isinstance(star, StarInfo) else star.get("name", "")
            if name in beneficial:
                positive.append(f"Has beneficial star {name}")
            if name in harmful:
                negative.append(f"Has malefic star {name}")

        return PalaceAnalysis(
            index=palace_data.get("index", 0),
            branch_name=palace_data.get("branch_name", ""),
            palace_name=palace_data.get("palace_name", "") or "",
            major_stars=major_stars,
            support_stars=support_stars,
            element=palace_data.get("palace_element", ""),
            strength=strength,
            positive_aspects=positive,
            negative_aspects=negative,
        )

    @staticmethod
    def get_palace_by_name(earth_plate: dict, palace_name: str) -> dict:
        for palace in earth_plate.get("palaces", []):
            if palace_name in (palace.get("palace_name") or ""):
                return palace
        return {}

    @staticmethod
    def analyze_chart(birth: BirthInfoRequest) -> ChartAnalysisResponse:
        chart = TuViService.generate_full_chart(birth)
        plate = chart.earth_plate.model_dump()

        life = TuViService.get_palace_by_name(plate, "Mệnh")
        career = TuViService.get_palace_by_name(plate, "Quan lộc")
        wealth = TuViService.get_palace_by_name(plate, "Tài Bạch")

        life_a = TuViService.analyze_palace(life) if life else None
        career_a = TuViService.analyze_palace(career) if career else None
        wealth_a = TuViService.analyze_palace(wealth) if wealth else None

        overall = "Balanced"
        if life_a and life_a.strength in ("Strong", "Very Strong"):
            overall = "Strong"

        wu_xing_ju = plate.get("wu_xing_ju", 0)
        lucky: list[str] = []
        if wu_xing_ju in (2, 6):
            lucky = ["Hỏa", "Mộc"]
        elif wu_xing_ju in (3, 7):
            lucky = ["Thổ", "Hỏa"]
        elif wu_xing_ju in (4, 8):
            lucky = ["Kim", "Thổ"]
        elif wu_xing_ju in (5, 9):
            lucky = ["Thủy", "Kim"]

        unlucky: list[str] = []
        if "Hỏa" in lucky:
            unlucky.append("Thủy")
        if "Thủy" in lucky:
            unlucky.append("Thổ")

        events = []
        for palace in plate.get("palaces", []):
            age = palace.get("da_xian_age")
            if age is not None:
                events.append(
                    {
                        "age": age,
                        "event": f"Da xian — {palace.get('palace_name') or palace.get('branch_name')}",
                        "type": "da_xian",
                        "palace_index": palace.get("index"),
                    }
                )
        events.sort(key=lambda x: x["age"])

        return ChartAnalysisResponse(
            birth_info=birth,
            life_palace_analysis=life_a,
            career_palace_analysis=career_a,
            wealth_palace_analysis=wealth_a,
            overall_strength=overall,
            lucky_elements=lucky,
            unlucky_elements=unlucky,
            major_life_events=events,
        )
