"""Tests for the chart interpretation engine."""
from lasotuvi.analysis import ChartAnalyzer, FORMATION_RULES, MAJOR_STAR_IDS
from lasotuvi.chart_builder import build_earth_plate
from lasotuvi.earth_plate import EarthPlate


def test_related_palaces_san_fang_si_zheng():
    plate = EarthPlate(lunar_birth_month=1, lunar_birth_hour=1)
    related = plate.get_related_palaces(2)
    assert related["opposite"] == 8
    assert set(related["all_related"]) == {6, 8, 10}


def test_detect_killings_breaker_ambition_sample():
    plate = build_earth_plate(15, 8, 1990, 7, 1, True, 7)
    analyzer = ChartAnalyzer(plate)
    codes = {f["code"] for f in analyzer.detect_formations()}
    assert "killings_breaker_ambition" in codes


def test_life_palace_interpretations_seeded():
    plate = build_earth_plate(15, 8, 1990, 7, 1, True, 7)
    analyzer = ChartAnalyzer(plate)
    readings = analyzer.interpret_palace("Mệnh")
    assert readings
    assert all("star" in r and "interpretation" in r for r in readings)


def test_formation_rules_use_major_star_ids():
    for required in FORMATION_RULES.values():
        assert required <= MAJOR_STAR_IDS
