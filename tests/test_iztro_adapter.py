"""Contract tests for the py-iztro canonical adapter."""

import pytest

from lasotuvi.iztro_adapter import (
    PALACE_NAME_MAP,
    STAR_NAME_MAP,
    build_canonical_chart,
    get_astro_data,
    hour_branch_to_iztro_time_index,
    iztro_time_index_to_hour_branch,
    shutdown_iztro_runtime,
    to_canonical,
)


def test_hour_branch_mapping_documents_both_zi_segments():
    assert hour_branch_to_iztro_time_index(1) == 0
    assert hour_branch_to_iztro_time_index(7) == 6
    assert hour_branch_to_iztro_time_index(12) == 11
    assert iztro_time_index_to_hour_branch(0) == 1
    assert iztro_time_index_to_hour_branch(12) == 1


def test_name_maps_accept_vietnamese_chinese_and_english():
    assert STAR_NAME_MAP["tử vi"] == "zi_wei"
    assert STAR_NAME_MAP["紫微"] == "zi_wei"
    assert STAR_NAME_MAP["emperor"] == "zi_wei"
    assert PALACE_NAME_MAP["mệnh"] == "life"
    assert PALACE_NAME_MAP["命"] == "life"
    assert PALACE_NAME_MAP["soul"] == "life"


@pytest.mark.integration
def test_to_canonical_full_smoke():
    raw = get_astro_data("1990-8-15", 6, 1)
    chart = to_canonical(
        raw,
        time_index=6,
        lunar_birth_month=6,
        lunar_birth_hour=7,
        gender=1,
    )
    assert len(chart.palaces) == 12
    assert chart.life_palace_index == 2
    assert chart.body_palace_index == 2
    assert chart.five_elements_class == 6
    assert chart.year_branch_key == "wu"
    assert all(not star.key.startswith("iztro_star_") for p in chart.palaces for star in p.stars)
    assert any(star.mutagen for palace in chart.palaces for star in palace.stars)


@pytest.mark.integration
def test_build_canonical_chart_uses_api_hour_branch():
    chart = build_canonical_chart(15, 8, 1990, 7, 1, lunar_birth_month=6)
    assert chart.time_index == 6
    assert chart.lunar_birth_hour == 7


@pytest.mark.integration
def test_runtime_can_restart_cleanly():
    shutdown_iztro_runtime()
    first = get_astro_data("1990-8-15", 6, 1)
    shutdown_iztro_runtime()
    second = get_astro_data("1990-8-15", 6, 1)
    assert first["solarDate"] == second["solarDate"] == "1990-8-15"


def test_to_canonical_rejects_incomplete_upstream_data():
    with pytest.raises(ValueError, match="exactly 12 palaces"):
        to_canonical({"palaces": []})
