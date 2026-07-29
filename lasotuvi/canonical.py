"""Stable, engine-neutral chart model used by analysis and API layers."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CanonicalStar:
    """One normalized star independent of an upstream engine's display language."""

    key: str
    name: str
    source_name: str
    legacy_id: int
    star_type: str
    category: int | None = None
    brightness: str | None = None
    mutagen: str | None = None
    element: str | None = None
    is_auspicious: bool | None = None


@dataclass(frozen=True, slots=True)
class CanonicalPalace:
    """One of the twelve palaces, indexed by earthly branch (Zi=1 ... Hai=12)."""

    index: int
    key: str
    name: str
    branch_key: str
    branch_name: str
    branch_element: str
    yin_yang: int
    stem: int
    stem_name: str
    stars: tuple[CanonicalStar, ...]
    is_body_palace: bool = False
    da_xian_age: int | None = None
    da_xian_end_age: int | None = None
    annual_ages: tuple[int, ...] = ()
    xiao_xian_branch: str | None = None
    is_xun: bool = False
    is_triet: bool = False

    @property
    def major_star_keys(self) -> frozenset[str]:
        return frozenset(star.key for star in self.stars if star.star_type == "major")

    @property
    def star_keys(self) -> frozenset[str]:
        return frozenset(star.key for star in self.stars)


@dataclass(frozen=True, slots=True)
class CanonicalChart:
    """Canonical birth chart consumed by deterministic business logic."""

    palaces: tuple[CanonicalPalace, ...]
    life_palace_index: int
    body_palace_index: int
    lunar_birth_month: int
    lunar_birth_hour: int
    five_elements_class: int
    five_elements_class_name: str
    gender: int
    time_index: int
    solar_date: str
    lunar_date: str
    chinese_date: str
    year_stem_key: str | None = None
    year_branch_key: str | None = None
    soul_master: str | None = None
    body_master: str | None = None
    source_engine: str = "py-iztro"

    def __post_init__(self) -> None:
        indices = {palace.index for palace in self.palaces}
        if indices != set(range(1, 13)):
            raise ValueError("canonical chart must contain exactly branch indices 1..12")
        if self.life_palace_index not in indices or self.body_palace_index not in indices:
            raise ValueError("life/body palace index must identify a canonical palace")

    def palace(self, index: int) -> CanonicalPalace:
        """Return a palace by its 1-based earthly-branch index."""
        for palace in self.palaces:
            if palace.index == index:
                return palace
        raise KeyError(f"unknown palace index: {index}")

    def palace_by_key(self, key: str) -> CanonicalPalace | None:
        """Return a palace by a canonical key such as ``life`` or ``career``."""
        for palace in self.palaces:
            if palace.key == key:
                return palace
        return None

    @staticmethod
    def related_palace_indices(index: int) -> dict[str, int | tuple[int, int, int]]:
        """Return the opposite and trine branches forming san fang si zheng."""
        if not 1 <= index <= 12:
            raise ValueError("palace index must be in 1..12")
        opposite = (index - 1 + 6) % 12 + 1
        trine_1 = (index - 1 + 4) % 12 + 1
        trine_2 = (index - 1 + 8) % 12 + 1
        return {
            "opposite": opposite,
            "trine_1": trine_1,
            "trine_2": trine_2,
            "all_related": (opposite, trine_1, trine_2),
        }
