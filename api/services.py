"""Service layer for Zi Wei Dou Shu chart calculations."""
from __future__ import annotations

from datetime import date
from typing import Any, Optional

from lasotuvi.analysis import ChartAnalyzer
from lasotuvi.canonical import CanonicalChart, CanonicalStar
from lasotuvi.iztro_adapter import build_canonical_chart
from lasotuvi.stem_branch import (
    day_stem_branch,
    EARTHLY_BRANCHES,
    generation_control,
    month_year_stem_branch,
    five_element,
    HEAVENLY_STEMS,
    nayin_element,
)
from lasotuvi.lunar_calendar import julian_day_from_date, lunar_to_solar, solar_to_lunar

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


def _star_to_api(star: CanonicalStar) -> StarInfo:
    """Serialize a canonical star without exposing py-iztro's source schema."""
    return StarInfo(
        id=star.legacy_id,
        name=star.name,
        element=star.element,
        category=star.category,
        category_label=(
            STAR_CATEGORY_LABELS.get(star.category) if star.category is not None else None
        ),
        miao_wang=star.brightness,
        miao_wang_label=(MIAO_WANG_LABELS.get(star.brightness) if star.brightness else None),
        mutagen=star.mutagen,
        is_auspicious=star.is_auspicious,
    )


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
        chart: CanonicalChart,
        year_stem: int,
        year_branch: int,
        view_year: Optional[int],
    ) -> ChartMeta:
        view_year_branch = None
        if view_year is not None:
            chi = ((view_year - 4) % 12) + 1
            view_year_branch = EARTHLY_BRANCHES[chi]["branch_name"]

        nayin = nayin_element(year_branch, year_stem)
        ben_ming_name = nayin_element(year_branch, year_stem, True)
        ben_ming_element_id = five_element(nayin)["id"]
        bureau_element_id = {2: 3, 3: 2, 4: 1, 5: 5, 6: 4}[chart.five_elements_class]
        relation = generation_control(ben_ming_element_id, bureau_element_id)
        relation_labels = {
            1: "Bản Mệnh sinh Cục",
            -1: "Bản Mệnh khắc Cục",
            -1j: "Cục khắc Bản Mệnh",
            1j: "Cục sinh Bản mệnh",
            0: "Cục hòa Bản Mệnh",
        }

        life_yin_yang = chart.palace(chart.life_palace_index).yin_yang
        life_yin_yang_status = (
            "Âm dương thuận lý" if life_yin_yang * birth.gender == 1 else "Âm dương nghịch lý"
        )

        return ChartMeta(
            ben_ming_name=ben_ming_name,
            nayin=nayin,
            year_yin_yang="Dương" if year_branch % 2 == 1 else "Âm",
            life_yin_yang_status=life_yin_yang_status,
            ming_zhu=chart.soul_master or EARTHLY_BRANCHES[chart.life_palace_index]["ming_zhu"],
            shen_zhu=chart.body_master or EARTHLY_BRANCHES[year_branch]["shen_zhu"],
            sheng_ke_status=relation_labels[relation],
            wu_xing_ju_name=chart.five_elements_class_name,
            wu_xing_ju=chart.five_elements_class,
            view_year=view_year,
            view_year_branch=view_year_branch,
        )

    @staticmethod
    def create_earth_plate(birth: BirthInfoRequest) -> EarthPlateResponse:
        lunar_day, lunar_month, lunar_year, _ = TuViService._resolve_lunar(birth)
        chart = build_canonical_chart(
            birth.day,
            birth.month,
            birth.year,
            birth.hour,
            birth.gender,
            is_solar=birth.is_solar,
            lunar_birth_month=lunar_month,
        )

        _, year_stem, year_branch = month_year_stem_branch(
            lunar_day, lunar_month, lunar_year, False, birth.timezone
        )

        view_year = birth.view_year or date.today().year
        view_branch = ((view_year - 4) % 12) + 1
        view_branch_name = EARTHLY_BRANCHES[view_branch]["branch_name"]

        xiao_xian_palace = chart.life_palace_index
        for palace in chart.palaces:
            if palace.xiao_xian_branch == view_branch_name:
                xiao_xian_palace = palace.index
                break

        month_map = yue_xian_map(xiao_xian_palace, lunar_month, birth.hour)
        chart_meta = TuViService._build_chart_meta(birth, chart, year_stem, year_branch, view_year)

        year_stem_name = HEAVENLY_STEMS[year_stem]["stem_name"]
        year_branch_name = EARTHLY_BRANCHES[year_branch]["branch_name"]

        analyzer = ChartAnalyzer(
            chart,
            year_stem=year_stem_name,
            year_branch=year_branch_name,
            life_element=chart_meta.ben_ming_name,
            destiny_element=chart_meta.wu_xing_ju_name,
        )
        formations = [ChartFormation(**f) for f in analyzer.detect_formations()]
        palace_readings = analyzer.interpret_all_palaces()
        taboo_palaces = analyzer.get_taboo_palaces()

        palaces: list[PalaceInfo] = []
        for palace in chart.palaces:
            readings = palace_readings.get(palace.name, [])
            palaces.append(
                PalaceInfo(
                    index=palace.index,
                    branch_name=palace.branch_name,
                    palace_name=palace.name,
                    palace_element=palace.branch_element,
                    yin_yang=palace.yin_yang,
                    stem=palace.stem,
                    stem_name=palace.stem_name,
                    stars=[_star_to_api(star) for star in palace.stars],
                    interpretations=[StarInterpretation(**r) for r in readings],
                    da_xian_age=palace.da_xian_age,
                    xiao_xian_branch=palace.xiao_xian_branch,
                    yue_xian=month_map.get(palace.index),
                    is_body_palace=palace.is_body_palace,
                    is_xun=palace.is_xun,
                    is_triet=palace.is_triet,
                )
            )

        return EarthPlateResponse(
            lunar_birth_month=chart.lunar_birth_month,
            lunar_birth_hour=chart.lunar_birth_hour,
            life_palace=chart.life_palace_index,
            body_palace=chart.body_palace_index,
            wu_xing_ju=chart.five_elements_class,
            wu_xing_ju_name=chart.five_elements_class_name,
            palaces=palaces,
            formations=formations,
            taboo_palaces=taboo_palaces,
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
