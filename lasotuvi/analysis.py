"""Deterministic chart formations, taboo palaces, and interpretation rules."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from lasotuvi.canonical import CanonicalChart, CanonicalPalace

DATA_DIR = Path(__file__).parent / "data"
INTERPRETATIONS_PATH = DATA_DIR / "interpretations.json"

MAJOR_STAR_KEYS = frozenset(
    {
        "zi_wei",
        "lian_zhen",
        "tian_tong",
        "wu_qu",
        "tai_yang",
        "tian_ji",
        "tian_fu",
        "tai_yin",
        "tan_lang",
        "ju_men",
        "tian_xiang",
        "tian_liang",
        "qi_sha",
        "po_jun",
    }
)

FORMATION_RULES: dict[str, frozenset[str]] = {
    "emperor_treasury_military_minister": frozenset(
        {"zi_wei", "tian_fu", "wu_qu", "tian_xiang"}
    ),
    "killings_breaker_ambition": frozenset({"qi_sha", "po_jun", "tan_lang"}),
    "advisor_moon_harmony_elder": frozenset(
        {"tian_ji", "tai_yin", "tian_tong", "tian_liang"}
    ),
    "gate_sun": frozenset({"ju_men", "tai_yang"}),
}

ELEMENTS = ("kim", "thuy", "moc", "hoa", "tho")

_TABOO_PALACES: dict[str, list[str]] = {
    "zi": ["yin", "shen", "zi", "wu"],
    "chou": ["chou", "wu"],
    "yin": ["yin", "shen", "si", "hai"],
    "mao": ["mao", "you", "si", "hai"],
    "chen": ["chen", "xu", "si", "hai"],
    "si": ["chen", "xu", "si", "hai"],
    "wu": ["chou", "wu"],
    "wei": ["si", "hai"],
    "shen": ["wu", "shen", "yin"],
    "you": ["you", "hai"],
    "xu": ["si", "xu", "chen"],
    "hai": ["you", "hai"],
}

_BRANCH_ALIASES = {
    "tý": "zi",
    "zi": "zi",
    "sửu": "chou",
    "suu": "chou",
    "chou": "chou",
    "dần": "yin",
    "dan": "yin",
    "yin": "yin",
    "mão": "mao",
    "mao": "mao",
    "thìn": "chen",
    "thin": "chen",
    "chen": "chen",
    "tỵ": "si",
    "si": "si",
    "ngọ": "wu",
    "ngo": "wu",
    "wu": "wu",
    "mùi": "wei",
    "mui": "wei",
    "wei": "wei",
    "thân": "shen",
    "than": "shen",
    "shen": "shen",
    "dậu": "you",
    "dau": "you",
    "you": "you",
    "tuất": "xu",
    "tuat": "xu",
    "xu": "xu",
    "hợi": "hai",
    "hoi": "hai",
    "hai": "hai",
}


def load_interpretations() -> dict[str, Any]:
    if not INTERPRETATIONS_PATH.exists():
        return {"formations": {}, "palaces": {}, "star_metadata": {}}
    with INTERPRETATIONS_PATH.open(encoding="utf-8") as file:
        return json.load(file)


class ChartAnalyzer:
    """Apply deterministic rules to a :class:`CanonicalChart`."""

    def __init__(
        self,
        chart: CanonicalChart,
        year_stem: str | None = None,
        year_branch: str | None = None,
        life_element: str | None = None,
        destiny_element: str | None = None,
    ) -> None:
        self.chart = chart
        self.knowledge = load_interpretations()
        self.year_stem = year_stem or chart.year_stem_key
        self.year_branch = year_branch or chart.year_branch_key
        self.life_element = self._normalize_element(life_element)
        self.destiny_element = self._normalize_element(destiny_element)

    @staticmethod
    def _normalize_element(element: str | None) -> str | None:
        if not element:
            return None
        normalized = element.casefold()
        if "kim" in normalized:
            return "kim"
        if "thủy" in normalized or "thuy" in normalized:
            return "thuy"
        if "mộc" in normalized or "moc" in normalized:
            return "moc"
        if "hỏa" in normalized or "hoa" in normalized:
            return "hoa"
        if "thổ" in normalized or "tho" in normalized:
            return "tho"
        return None

    @staticmethod
    def _evaluate_elemental_interaction(base_element: str, target_element: str) -> str:
        """Return the five-element relationship of target relative to base."""
        if not base_element or not target_element:
            return "binh_hoa"
        if base_element == target_element:
            return "vuong"
        try:
            base_idx = ELEMENTS.index(base_element)
            target_idx = ELEMENTS.index(target_element)
        except ValueError:
            return "binh_hoa"
        if (target_idx + 1) % 5 == base_idx:
            return "tuong"
        if (base_idx + 1) % 5 == target_idx:
            return "huu"
        if (target_idx + 2) % 5 == base_idx:
            return "tu_khac"
        if (base_idx + 2) % 5 == target_idx:
            return "tu"
        return "binh_hoa"

    def star_keys_in_palaces(self, palace_indices: list[int] | tuple[int, ...]) -> set[str]:
        keys: set[str] = set()
        for index in palace_indices:
            keys.update(self.chart.palace(index).star_keys)
        return keys

    def _has_stars_in_palace(self, star_keys: set[str], branch_index: int) -> bool:
        return star_keys.issubset(self.chart.palace(branch_index).star_keys)

    @staticmethod
    def _is_emperor_ministers(stars_in_life: set[str]) -> bool:
        return {"zi_wei", "zuo_fu", "you_bi"}.issubset(stars_in_life)

    @staticmethod
    def _is_empty_life_major_stars(stars_in_life: set[str]) -> bool:
        return not bool(stars_in_life & MAJOR_STAR_KEYS)

    def detect_formations(self) -> list[dict[str, str]]:
        """Identify formations in the life palace's san fang si zheng frame."""
        life_index = self.chart.life_palace_index
        related = self.chart.related_palace_indices(life_index)
        related_indices = related["all_related"]
        assert isinstance(related_indices, tuple)
        frame_indices = (life_index, *related_indices)
        stars_in_frame = self.star_keys_in_palaces(frame_indices)
        stars_in_life = self.star_keys_in_palaces((life_index,))

        detected = [
            code for code, required in FORMATION_RULES.items() if required.issubset(stars_in_frame)
        ]
        if self._is_emperor_ministers(stars_in_life):
            detected.append("emperor_ministers")
        if life_index in (3, 9) and FORMATION_RULES[
            "advisor_moon_harmony_elder"
        ].issubset(stars_in_frame):
            detected.append("ji_yue_tong_liang_yin_shen")
        if FORMATION_RULES["gate_sun"].issubset(stars_in_frame) and (
            self._has_stars_in_palace({"ju_men", "tai_yang"}, 3)
            or self._has_stars_in_palace({"ju_men", "tai_yang"}, 9)
        ):
            detected.append("ju_ri_yin_shen")
        if self._is_empty_life_major_stars(stars_in_life):
            detected.append("empty_life_major_stars")

        catalog = self.knowledge.get("formations", {})
        return [
            {
                "code": code,
                "name": catalog[code]["name"],
                "description": catalog[code]["description"],
            }
            for code in detected
            if code in catalog
        ]

    def get_taboo_palaces(self) -> list[str]:
        """Return canonical branch keys of taboo palaces for the birth-year branch."""
        if not self.year_branch:
            return []
        branch = _BRANCH_ALIASES.get(self.year_branch.casefold(), self.year_branch.casefold())
        return list(_TABOO_PALACES.get(branch, ()))

    def _resolve_palace(self, palace_name_or_key: str) -> CanonicalPalace | None:
        normalized = palace_name_or_key.casefold().removesuffix("_palace")
        for palace in self.chart.palaces:
            if normalized in (palace.key.casefold(), palace.name.casefold()):
                return palace
        return None

    def interpret_palace(self, palace_name_or_key: str) -> list[dict[str, str]]:
        """Return knowledge-base readings for canonical stars in one palace."""
        palace = self._resolve_palace(palace_name_or_key)
        if palace is None:
            return []
        palace_kb = self.knowledge.get("palaces", {}).get(f"{palace.key}_palace", {})
        star_meta_kb = self.knowledge.get("star_metadata", {})

        interaction_descriptions = {
            "vuong": "Bản Mệnh đồng hành với Sao (Vượng), Mệnh hoàn toàn làm chủ được Sao, hưởng trọn tính chất tốt.",
            "tuong": "Hành Sao sinh Bản Mệnh (Tướng), Sao phò tá đắc lực cho Mệnh, rất tốt.",
            "huu": "Bản Mệnh sinh Hành Sao (Hưu), Mệnh bị tiết khí, tổn hao để nuôi Sao.",
            "tu": "Bản Mệnh khắc Hành Sao (Tù), Sao bị suy yếu, Mệnh khống chế được nhưng vất vả.",
            "tu_khac": "Hành Sao khắc Bản Mệnh (Tử), Sao gây bất lợi, nguy hiểm cho Mệnh.",
        }

        readings: list[dict[str, str]] = []
        for star in palace.stars:
            text = palace_kb.get(star.key)
            if not text:
                continue
            interaction_info = ""
            if self.life_element:
                star_element = star.element or star_meta_kb.get(star.key, {}).get("element")
                if star_element:
                    interaction = self._evaluate_elemental_interaction(
                        self.life_element, star_element
                    )
                    description = interaction_descriptions.get(interaction)
                    if description:
                        interaction_info = f" [Tương tác Ngũ Hành: {description}]"
            readings.append(
                {"star": star.key, "interpretation": f"{text}{interaction_info}"}
            )
        return readings

    def interpret_all_palaces(self) -> dict[str, list[dict[str, str]]]:
        """Map stable Vietnamese palace display names to their readings."""
        result: dict[str, list[dict[str, str]]] = {}
        for palace in self.chart.palaces:
            readings = self.interpret_palace(palace.key)
            if readings:
                result[palace.name] = readings
        return result


__all__ = ["ChartAnalyzer", "FORMATION_RULES", "MAJOR_STAR_KEYS", "load_interpretations"]
