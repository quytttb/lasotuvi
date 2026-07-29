"""Logic-layer tests against engine-neutral canonical fixtures."""

from lasotuvi.analysis import FORMATION_RULES, MAJOR_STAR_KEYS, ChartAnalyzer
from lasotuvi.canonical import CanonicalChart, CanonicalPalace, CanonicalStar


def _star(key: str, name: str = "Test star", star_type: str = "major") -> CanonicalStar:
    return CanonicalStar(
        key=key,
        name=name,
        source_name=name,
        legacy_id=1,
        star_type=star_type,
        category=1 if star_type == "major" else 2,
    )


def _chart(
    stars_by_index: dict[int, tuple[CanonicalStar, ...]],
    *,
    life_index: int = 1,
    year_branch: str = "zi",
) -> CanonicalChart:
    branch_keys = (
        "zi",
        "chou",
        "yin",
        "mao",
        "chen",
        "si",
        "wu",
        "wei",
        "shen",
        "you",
        "xu",
        "hai",
    )
    branch_names = (
        "Tý",
        "Sửu",
        "Dần",
        "Mão",
        "Thìn",
        "Tỵ",
        "Ngọ",
        "Mùi",
        "Thân",
        "Dậu",
        "Tuất",
        "Hợi",
    )
    palaces = tuple(
        CanonicalPalace(
            index=index,
            key="life" if index == life_index else f"palace_{index}",
            name="Mệnh" if index == life_index else f"Cung {index}",
            branch_key=branch_keys[index - 1],
            branch_name=branch_names[index - 1],
            branch_element="Thổ",
            yin_yang=1 if index % 2 else -1,
            stem=1,
            stem_name="Giáp",
            stars=stars_by_index.get(index, ()),
        )
        for index in range(1, 13)
    )
    return CanonicalChart(
        palaces=palaces,
        life_palace_index=life_index,
        body_palace_index=life_index,
        lunar_birth_month=1,
        lunar_birth_hour=1,
        five_elements_class=2,
        five_elements_class_name="Thủy Nhị Cục",
        gender=1,
        time_index=0,
        solar_date="2000-1-1",
        lunar_date="",
        chinese_date="",
        year_branch_key=year_branch,
    )


def test_related_palaces_san_fang_si_zheng():
    related = CanonicalChart.related_palace_indices(2)
    assert related["opposite"] == 8
    assert set(related["all_related"]) == {6, 8, 10}


def test_detect_formation_from_canonical_keys():
    chart = _chart(
        {
            1: (_star("qi_sha"),),
            5: (_star("po_jun"),),
            7: (_star("tan_lang"),),
        }
    )
    codes = {item["code"] for item in ChartAnalyzer(chart).detect_formations()}
    assert "killings_breaker_ambition" in codes


def test_life_palace_interpretations_seeded():
    chart = _chart({1: (_star("zi_wei", "Tử vi"),)})
    readings = ChartAnalyzer(chart).interpret_palace("life")
    assert readings
    assert readings[0]["star"] == "zi_wei"
    assert readings[0]["interpretation"]


def test_elemental_interaction_is_appended_without_changing_base_rule():
    chart = _chart({1: (_star("zi_wei", "Tử vi"),)})
    reading = ChartAnalyzer(chart, life_element="Thổ").interpret_palace("Mệnh")[0]
    assert "Tương tác Ngũ Hành" in reading["interpretation"]


def test_taboo_palaces_use_canonical_year_branch():
    assert ChartAnalyzer(_chart({}, year_branch="wu")).get_taboo_palaces() == ["chou", "wu"]


def test_formation_rules_use_major_star_keys():
    for required in FORMATION_RULES.values():
        assert required <= MAJOR_STAR_KEYS
