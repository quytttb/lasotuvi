"""Chart interpretation engine: formations (cách cục) and palace readings."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent / "data"
INTERPRETATIONS_PATH = DATA_DIR / "interpretations.json"

# 14 major stars (chính tinh) — star_id 1..14
MAJOR_STAR_IDS = frozenset(range(1, 15))

# Formation rules: required major-star IDs in life palace + san fang si zheng
FORMATION_RULES: dict[str, frozenset[int]] = {
    # Tử Phủ Vũ Tướng: Zi Wei, Tian Fu, Wu Qu, Tian Xiang
    "emperor_treasury_military_minister": frozenset({1, 7, 4, 11}),
    # Sát Phá Tham: Qi Sha, Po Jun, Tan Lang
    "killings_breaker_ambition": frozenset({13, 14, 9}),
    # Cơ Nguyệt Đồng Lương: Tian Ji, Tai Yin, Tian Tong, Tian Liang
    "advisor_moon_harmony_elder": frozenset({6, 8, 3, 12}),
    # Cự Nhật: Ju Men, Tai Yang
    "gate_sun": frozenset({10, 5}),
}


def load_interpretations() -> dict[str, Any]:
    if not INTERPRETATIONS_PATH.exists():
        return {"formations": {}, "palaces": {}}
    with open(INTERPRETATIONS_PATH, encoding="utf-8") as f:
        return json.load(f)


class ChartAnalyzer:
    """Detect chart formations and attach star interpretations from the knowledge base."""

    def __init__(self, earth_plate):
        self.earth_plate = earth_plate
        self.knowledge = load_interpretations()

    def star_ids_in_palaces(self, palace_indices: list[int]) -> set[int]:
        star_ids: set[int] = set()
        for idx in palace_indices:
            palace = self.earth_plate.palaces[idx]
            for star in palace.stars:
                star_ids.add(star["star_id"])
        return star_ids

    def detect_formations(self) -> list[dict[str, str]]:
        """Identify formations from the life palace and its related palaces (tam hợp + xung)."""
        life_idx = self.earth_plate.life_palace
        related = self.earth_plate.get_related_palaces(life_idx)
        frame_indices = [life_idx] + related["all_related"]
        stars_in_frame = self.star_ids_in_palaces(frame_indices)
        stars_in_life = self.star_ids_in_palaces([life_idx])

        detected: list[str] = []
        for code, required in FORMATION_RULES.items():
            if required.issubset(stars_in_frame):
                detected.append(code)

        if not (stars_in_life & MAJOR_STAR_IDS):
            detected.append("empty_life_major_stars")

        results: list[dict[str, str]] = []
        catalog = self.knowledge.get("formations", {})
        for code in detected:
            info = catalog.get(code)
            if info:
                results.append(
                    {
                        "code": code,
                        "name": info["name"],
                        "description": info["description"],
                    }
                )
        return results

    def interpret_palace(self, palace_name: str) -> list[dict[str, str]]:
        """Return knowledge-base readings for stars present in a named palace."""
        target = None
        for palace in self.earth_plate.palaces[1:13]:
            if palace.palace_name == palace_name:
                target = palace
                break
        if not target:
            return []

        palace_kb = self.knowledge.get("palaces", {}).get(palace_name, {})
        readings: list[dict[str, str]] = []
        for star in target.stars:
            text = palace_kb.get(star["name"])
            if text:
                readings.append({"star": star["name"], "interpretation": text})
        return readings

    def interpret_all_palaces(self) -> dict[str, list[dict[str, str]]]:
        """Map palace_name → list of star interpretations."""
        result: dict[str, list[dict[str, str]]] = {}
        for palace in self.earth_plate.palaces[1:13]:
            name = palace.palace_name
            if not name:
                continue
            readings = self.interpret_palace(name)
            if readings:
                result[name] = readings
        return result
