"""End-to-end Phase 1 smoke from birth data through deterministic analysis."""
from lasotuvi.analysis import ChartAnalyzer
from lasotuvi.iztro_adapter import build_canonical_chart


def test_birth_to_canonical_formations_taboo_and_interpretations():
    chart = build_canonical_chart(15, 8, 1990, 7, 1, lunar_birth_month=6)
    analyzer = ChartAnalyzer(chart)

    assert {item["code"] for item in analyzer.detect_formations()} == {
        "killings_breaker_ambition"
    }
    assert analyzer.get_taboo_palaces() == ["chou", "wu"]
    assert analyzer.interpret_palace("life")
    assert any(star.brightness for palace in chart.palaces for star in palace.stars)
    assert any(star.mutagen for palace in chart.palaces for star in palace.stars)
