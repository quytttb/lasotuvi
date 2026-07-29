"""Adapter from :mod:`py_iztro` output to the engine-neutral canonical model."""
from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from lasotuvi.canonical import CanonicalChart, CanonicalPalace, CanonicalStar


def _normalized(value: str) -> str:
    return " ".join(value.strip().casefold().replace("宫", "").split())


_BRANCH_ROWS = (
    (1, "zi", "Tý", "Thủy", 1, ("Tý", "Ty", "子", "zi")),
    (2, "chou", "Sửu", "Thổ", -1, ("Sửu", "Suu", "丑", "chou")),
    (3, "yin", "Dần", "Mộc", 1, ("Dần", "Dan", "寅", "yin")),
    (4, "mao", "Mão", "Mộc", -1, ("Mão", "Mao", "卯", "mao")),
    (5, "chen", "Thìn", "Thổ", 1, ("Thìn", "Thin", "辰", "chen")),
    (6, "si", "Tỵ", "Hỏa", -1, ("Tỵ", "Ty", "巳", "si")),
    (7, "wu", "Ngọ", "Hỏa", 1, ("Ngọ", "Ngo", "午", "wu")),
    (8, "wei", "Mùi", "Thổ", -1, ("Mùi", "Mui", "未", "wei")),
    (9, "shen", "Thân", "Kim", 1, ("Thân", "Than", "申", "shen")),
    (10, "you", "Dậu", "Kim", -1, ("Dậu", "Dau", "酉", "you")),
    (11, "xu", "Tuất", "Thổ", 1, ("Tuất", "Tuat", "戌", "xu")),
    (12, "hai", "Hợi", "Thủy", -1, ("Hợi", "Hoi", "亥", "hai")),
)

BRANCH_NAME_MAP: dict[str, str] = {}
_BRANCH_BY_KEY: dict[str, tuple[int, str, str, int]] = {}
for index, key, name, element, yin_yang, aliases in _BRANCH_ROWS:
    _BRANCH_BY_KEY[key] = (index, name, element, yin_yang)
    for alias in (key, name, *aliases):
        BRANCH_NAME_MAP[_normalized(alias)] = key


_STEM_ROWS = (
    (1, "jia", "Giáp", ("Giáp", "甲", "jia")),
    (2, "yi", "Ất", ("Ất", "乙", "yi")),
    (3, "bing", "Bính", ("Bính", "丙", "bing")),
    (4, "ding", "Đinh", ("Đinh", "丁", "ding")),
    (5, "wu", "Mậu", ("Mậu", "戊", "wu")),
    (6, "ji", "Kỷ", ("Kỷ", "己", "ji")),
    (7, "geng", "Canh", ("Canh", "庚", "geng")),
    (8, "xin", "Tân", ("Tân", "辛", "xin")),
    (9, "ren", "Nhâm", ("Nhâm", "壬", "ren")),
    (10, "gui", "Quý", ("Quý", "癸", "gui")),
)

STEM_NAME_MAP: dict[str, str] = {}
_STEM_BY_KEY: dict[str, tuple[int, str]] = {}
for index, key, name, aliases in _STEM_ROWS:
    _STEM_BY_KEY[key] = (index, name)
    for alias in (key, name, *aliases):
        STEM_NAME_MAP[_normalized(alias)] = key


_PALACE_ROWS = (
    ("life", "Mệnh", ("Mệnh", "Mệnh Cung", "命", "命宫", "soul")),
    ("parents", "Phụ mẫu", ("Phụ Mẫu", "父母", "parents")),
    ("fortune", "Phúc đức", ("Phúc Đức", "福德", "spirit")),
    ("property", "Điền trạch", ("Điền Trạch", "田宅", "property")),
    ("career", "Quan lộc", ("Quan Lộc", "官禄", "career")),
    ("friends", "Nô bộc", ("Nô Bộc", "仆役", "friends")),
    ("travel", "Thiên di", ("Thiên Di", "迁移", "surface")),
    ("health", "Tật Ách", ("Tật Ách", "疾厄", "health")),
    ("wealth", "Tài Bạch", ("Tài Bạch", "财帛", "wealth")),
    ("children", "Tử tức", ("Tử Nữ", "Tử Tức", "子女", "children")),
    ("spouse", "Phu thê", ("Phu Thê", "夫妻", "spouse")),
    ("siblings", "Huynh đệ", ("Huynh Đệ", "兄弟", "siblings")),
)

PALACE_NAME_MAP: dict[str, str] = {}
_PALACE_DISPLAY: dict[str, str] = {}
for key, display, aliases in _PALACE_ROWS:
    _PALACE_DISPLAY[key] = display
    for alias in (key, display, *aliases):
        PALACE_NAME_MAP[_normalized(alias)] = key


# key, stable Vietnamese display, legacy API id, element, aliases (VI / CN / EN)
_STAR_ROWS = (
    ("zi_wei", "Tử vi", 1, "tho", ("Tử Vi", "紫微", "emperor")),
    ("lian_zhen", "Liêm trinh", 2, "hoa", ("Liêm Trinh", "廉贞", "judge")),
    ("tian_tong", "Thiên đồng", 3, "thuy", ("Thiên Đồng", "天同", "fortunate")),
    ("wu_qu", "Vũ khúc", 4, "kim", ("Vũ Khúc", "武曲", "general")),
    ("tai_yang", "Thái Dương", 5, "hoa", ("Thái Dương", "太阳", "sun")),
    ("tian_ji", "Thiên cơ", 6, "moc", ("Thiên Cơ", "天机", "advisor")),
    ("tian_fu", "Thiên phủ", 7, "tho", ("Thiên Phủ", "天府", "empress")),
    ("tai_yin", "Thái âm", 8, "thuy", ("Thái Âm", "太阴", "moon")),
    ("tan_lang", "Tham lang", 9, "thuy", ("Tham Lang", "贪狼", "wolf")),
    ("ju_men", "Cự môn", 10, "thuy", ("Cự Môn", "巨门", "advocator")),
    ("tian_xiang", "Thiên tướng", 11, "thuy", ("Thiên Tướng", "天相", "minister")),
    ("tian_liang", "Thiên lương", 12, "tho", ("Thiên Lương", "天梁", "sage")),
    ("qi_sha", "Thất sát", 13, "kim", ("Thất Sát", "七杀", "marshal")),
    ("po_jun", "Phá quân", 14, "thuy", ("Phá Quân", "破军", "rebel")),
    ("lu_cun", "Lộc tồn", 27, None, ("Lộc Tồn", "禄存", "money")),
    ("tuo_luo", "Đà la", 51, None, ("Đà La", "陀罗", "tangled")),
    ("qing_yang", "Kình dương", 52, None, ("Kình Dương", "擎羊", "driven")),
    ("di_kong", "Địa không", 53, None, ("Địa Không", "地空", "ideologue")),
    ("di_jie", "Địa kiếp", 54, None, ("Địa Kiếp", "地劫", "fickle")),
    ("ling_xing", "Linh tinh", 55, None, ("Linh Tinh", "铃星", "spark")),
    ("huo_xing", "Hỏa tinh", 56, None, ("Hỏa Tinh", "火星", "impulsive")),
    ("wen_chang", "Văn xương", 57, None, ("Văn Xương", "文昌", "scholar")),
    ("wen_qu", "Văn Khúc", 58, None, ("Văn Khúc", "文曲", "artist")),
    ("tian_kui", "Thiên khôi", 59, None, ("Thiên Khôi", "天魁", "assistant")),
    ("tian_yue", "Thiên việt", 60, None, ("Thiên Việt", "天钺", "aide")),
    ("zuo_fu", "Tả phù", 61, None, ("Tả Phù", "左辅", "officer")),
    ("you_bi", "Hữu bật", 62, None, ("Hữu Bật", "右弼", "helper")),
    ("long_chi", "Long trì", 63, None, ("Long Trì", "龙池", "talented")),
    ("feng_ge", "Phượng các", 64, None, ("Phụng Các", "Phượng Các", "凤阁", "refined")),
    ("san_tai", "Tam thai", 65, None, ("Tam Thai", "三台", "senior")),
    ("ba_zuo", "Bát tọa", 66, None, ("Bát Tọa", "八座", "dignified")),
    ("en_guang", "Ân quang", 67, None, ("Ân Quang", "恩光", "grateful")),
    ("tian_gui", "Thiên quý", 68, None, ("Thiên Quý", "天贵", "noble")),
    ("tian_ku", "Thiên khốc", 69, None, ("Thiên Khốc", "天哭", "upset")),
    ("tian_xu", "Thiên hư", 70, None, ("Thiên Hư", "天虚", "frail")),
    ("tian_de", "Thiên đức", 71, None, ("Thiên Đức", "天德", "blessed")),
    ("yue_de", "Nguyệt đức", 72, None, ("Nguyệt Đức", "月德", "peaceful")),
    ("tian_xing", "Thiên hình", 73, None, ("Thiên Hình", "天刑", "serious")),
    ("tian_yao", "Thiên riêu", 74, None, ("Thiên Diêu", "Thiên Riêu", "天姚", "social")),
    ("hong_luan", "Hồng loan", 79, None, ("Hồng Loan", "红鸾", "attractive")),
    ("tian_xi", "Thiên hỷ", 80, None, ("Thiên Hỷ", "天喜", "cheerful")),
    ("jie_shen", "Giải thần", 83, None, ("Giải Thần", "解神", "considery")),
    ("tai_fu", "Thai phụ", 84, None, ("Đài Phụ", "Thai Phụ", "台辅", "honorable")),
    ("feng_gao", "Phong cáo", 85, None, ("Phong Cáo", "封诰", "awarded")),
    ("tian_cai", "Thiên tài", 86, None, ("Thiên Tài", "天才", "gifted")),
    ("tian_shou", "Thiên thọ", 87, None, ("Thiên Thọ", "天寿", "ageless")),
    ("tian_shang", "Thiên thương", 88, None, ("Thiên Thương", "天伤", "wounded")),
    ("tian_shi", "Thiên sứ", 89, None, ("Thiên Sứ", "天使", "heaven")),
    ("gu_chen", "Cô thần", 96, None, ("Cô Thần", "孤辰", "alone")),
    ("gua_su", "Quả tú", 97, None, ("Quả Tú", "寡宿", "lonely")),
    ("tian_ma", "Thiên mã", 98, None, ("Thiên Mã", "天马", "horse")),
    ("po_sui", "Phá toái", 99, None, ("Phá Toái", "破碎", "broken")),
    ("tian_guan", "Thiên quan", 100, None, ("Thiên Quan", "天官", "solemn")),
    ("tian_fu_blessing", "Thiên phúc", 101, None, ("Thiên Phúc", "天福", "lucky")),
    ("tian_chu", "Thiên trù", 103, None, ("Thiên Trù", "天厨", "gourmet")),
    ("hua_gai", "Hoa cái", 105, None, ("Hoa Cái", "华盖", "religious")),
    ("tian_kong", "Thiên không", 108, None, ("Thiên Không", "天空", "utopian")),
    ("xian_chi", "Hàm trì", None, None, ("Hàm Trì", "咸池", "passionate")),
    ("kong_wang", "Không vong", None, None, ("Không Vong", "空亡", "bottomless")),
    ("nian_jie", "Niên giải", None, None, ("Niên Giải", "年解", "considery(Y)")),
    ("fei_lian", "Phi liêm", 33, None, ("Phi Liêm", "蜚廉", "instigated")),
    ("tian_yue_month", "Thiên nguyệt", None, None, ("Thiên Nguyệt", "天月", "sickly")),
    ("tian_wu", "Thiên vu", None, None, ("Thiên Vu", "天巫", "psychic")),
    ("jie_lu", "Triệt lộ", None, None, ("Triệt Lộ", "截路", "intercepted")),
    ("xun_kong", "Tuần không", None, None, ("Tuần Không", "旬空", "fancied")),
    ("yin_sha", "Âm sát", None, None, ("Âm Sát", "阴煞", "gloomy")),
)

STAR_NAME_MAP: dict[str, str] = {}
_STAR_DETAILS: dict[str, tuple[str, int | None, str | None]] = {}
for key, display, legacy_id, element, aliases in _STAR_ROWS:
    _STAR_DETAILS[key] = (display, legacy_id, element)
    for alias in (key, display, *aliases):
        STAR_NAME_MAP[_normalized(alias)] = key


_BRIGHTNESS_MAP = {
    "miếu": "M",
    "庙": "M",
    "miao": "M",
    "vượng": "V",
    "旺": "V",
    "wang": "V",
    "đắc": "Đ",
    "得": "Đ",
    "de": "Đ",
    "lợi": "Đ",
    "利": "Đ",
    "li": "Đ",
    "bình": "B",
    "平": "B",
    "ping": "B",
    "hãm": "H",
    "hạn": "H",  # spelling currently emitted by py-iztro vi-VN
    "陷": "H",
    "xian": "H",
    "bất": "H",
    "不": "H",
    "bu": "H",
}

_MUTAGEN_MAP = {
    "lộc": "hua_lu",
    "禄": "hua_lu",
    "focused": "hua_lu",
    "quyền": "hua_quan",
    "权": "hua_quan",
    "responsible": "hua_quan",
    "khoa": "hua_ke",
    "科": "hua_ke",
    "skillful": "hua_ke",
    "kỵ": "hua_ji",
    "忌": "hua_ji",
    "negative": "hua_ji",
}

_TYPE_CATEGORY = {
    "major": 1,
    "soft": 2,
    "lucun": 3,
    "tianma": 3,
    "flower": 8,
    "tough": 11,
    "helper": 5,
    "adjective": 2,
}

# pythonmonkey owns a process-global JavaScript runtime and is not safe when
# separate FastAPI worker threads repeatedly initialize Astro. Keep all native
# runtime access on one dedicated thread and reuse one Astro instance.
_IZTRO_EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="py-iztro")
_ASTRO_INSTANCE: Any = None


def hour_branch_to_iztro_time_index(hour_branch: int) -> int:
    """Map API branch 1..12 to iztro 0..11, choosing early Zi for branch 1.

    iztro additionally accepts 12 for late Zi (23:00~00:00). The public API only
    carries a two-hour branch, so it cannot distinguish the two Zi segments.
    """
    if not 1 <= hour_branch <= 12:
        raise ValueError("hour branch must be in 1..12")
    return hour_branch - 1


def iztro_time_index_to_hour_branch(time_index: int) -> int:
    """Map iztro 0..12 back to an API branch; both Zi segments become branch 1."""
    if not 0 <= time_index <= 12:
        raise ValueError("iztro time index must be in 0..12")
    return 1 if time_index in (0, 12) else time_index + 1


def _gender_label(gender: int | str) -> str:
    if gender in (1, "1", "male", "nam", "男"):
        return "男"
    if gender in (-1, "-1", "female", "nữ", "女"):
        return "女"
    raise ValueError("gender must be 1/male or -1/female")


def get_astro_data(
    date: str,
    time_index: int,
    gender: int | str,
    *,
    is_solar: bool = True,
) -> Any:
    """Generate a py-iztro model using stable Vietnamese source labels."""
    if not 0 <= time_index <= 12:
        raise ValueError("iztro time index must be in 0..12")

    def generate() -> Any:
        global _ASTRO_INSTANCE
        try:
            from py_iztro import Astro
        except ImportError as exc:  # pragma: no cover - broken deployment only
            raise RuntimeError("py-iztro is required for chart generation") from exc
        if _ASTRO_INSTANCE is None:
            _ASTRO_INSTANCE = Astro()
        method = _ASTRO_INSTANCE.by_solar if is_solar else _ASTRO_INSTANCE.by_lunar
        return method(date, time_index, _gender_label(gender), language="vi-VN")

    return _IZTRO_EXECUTOR.submit(generate).result()


def _as_mapping(raw: Any) -> Mapping[str, Any]:
    if isinstance(raw, Mapping):
        return raw
    if hasattr(raw, "model_dump"):
        return raw.model_dump(by_alias=True)
    raise TypeError("iztro data must be a mapping or Pydantic model")


def _branch_key(value: str) -> str:
    key = BRANCH_NAME_MAP.get(_normalized(value))
    if key is None:
        raise ValueError(f"unknown earthly branch from iztro: {value!r}")
    return key


def _stem_key(value: str) -> str:
    key = STEM_NAME_MAP.get(_normalized(value))
    if key is None:
        raise ValueError(f"unknown heavenly stem from iztro: {value!r}")
    return key


def _stable_unknown_id(key: str) -> int:
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()
    return 1000 + int(digest[:7], 16)


def _star_key(source_name: str) -> str:
    normalized = _normalized(source_name)
    known = STAR_NAME_MAP.get(normalized)
    if known:
        return known
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]
    return f"iztro_star_{digest}"


def _canonical_star(raw_star: Mapping[str, Any]) -> CanonicalStar:
    source_name = str(raw_star.get("name") or "")
    key = _star_key(source_name)
    display, legacy_id, element = _STAR_DETAILS.get(key, (source_name, None, None))
    star_type = str(raw_star.get("type") or "adjective")
    category = _TYPE_CATEGORY.get(star_type)
    brightness_raw = str(raw_star.get("brightness") or "").strip()
    mutagen_raw = str(raw_star.get("mutagen") or "").strip()
    brightness = _BRIGHTNESS_MAP.get(_normalized(brightness_raw)) if brightness_raw else None
    mutagen = _MUTAGEN_MAP.get(_normalized(mutagen_raw)) if mutagen_raw else None
    is_auspicious = None if category is None else category < 10
    return CanonicalStar(
        key=key,
        name=display,
        source_name=source_name,
        legacy_id=legacy_id or _stable_unknown_id(key),
        star_type=star_type,
        category=category,
        brightness=brightness,
        mutagen=mutagen,
        element=element,
        is_auspicious=is_auspicious,
    )


def _parse_bureau(value: str) -> int:
    match = re.search(r"\d+", value)
    if match:
        return int(match.group())
    normalized = _normalized(value)
    words = {"nhị": 2, "tam": 3, "tứ": 4, "ngũ": 5, "lục": 6}
    for word, number in words.items():
        if word in normalized:
            return number
    raise ValueError(f"unknown five elements class from iztro: {value!r}")


def _parse_lunar_month(value: str) -> int:
    match = re.search(r"(?:年|[-/])(闰|閏)?([正一二三四五六七八九十]{1,2})月", value)
    if not match:
        return 0
    month_text = match.group(2)
    months = {
        "正": 1,
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
        "十一": 11,
        "十二": 12,
    }
    return months.get(month_text, 0)


def _year_pillar(chinese_date: str) -> tuple[str | None, str | None]:
    first = chinese_date.split(" - ", 1)[0].strip()
    parts = first.split()
    if len(parts) >= 2:
        return STEM_NAME_MAP.get(_normalized(parts[0])), BRANCH_NAME_MAP.get(
            _normalized(parts[1])
        )
    if len(first) >= 2:
        return STEM_NAME_MAP.get(_normalized(first[0])), BRANCH_NAME_MAP.get(
            _normalized(first[1])
        )
    return None, None


def to_canonical(
    raw: Any,
    *,
    time_index: int | None = None,
    lunar_birth_month: int | None = None,
    lunar_birth_hour: int | None = None,
    gender: int | None = None,
) -> CanonicalChart:
    """Normalize a py-iztro Pydantic model or aliased model dump."""
    data = _as_mapping(raw)
    raw_palaces = data.get("palaces") or []
    if len(raw_palaces) != 12:
        raise ValueError("iztro chart must contain exactly 12 palaces")

    chinese_date = str(data.get("chineseDate") or "")
    year_stem_key, year_branch_key = _year_pillar(chinese_date)
    year_branch_index = _BRANCH_BY_KEY[year_branch_key][0] if year_branch_key else None

    palaces: list[CanonicalPalace] = []
    for raw_palace_value in raw_palaces:
        raw_palace = _as_mapping(raw_palace_value)
        palace_source_name = str(raw_palace.get("name") or "")
        palace_key = PALACE_NAME_MAP.get(_normalized(palace_source_name))
        if palace_key is None:
            raise ValueError(f"unknown palace from iztro: {palace_source_name!r}")

        branch_key = _branch_key(str(raw_palace.get("earthlyBranch") or ""))
        branch_index, branch_name, branch_element, yin_yang = _BRANCH_BY_KEY[branch_key]
        stem_key = _stem_key(str(raw_palace.get("heavenlyStem") or ""))
        stem_index, stem_name = _STEM_BY_KEY[stem_key]

        stars: list[CanonicalStar] = []
        for group in ("majorStars", "minorStars", "adjectiveStars"):
            for raw_star in raw_palace.get(group) or []:
                stars.append(_canonical_star(_as_mapping(raw_star)))

        decadal = _as_mapping(raw_palace.get("decadal") or {})
        age_range = tuple(int(value) for value in (decadal.get("range") or []))
        annual_ages = tuple(int(value) for value in (raw_palace.get("ages") or []))
        xiao_xian_branch = None
        if annual_ages and year_branch_index:
            xiao_index = (year_branch_index + annual_ages[0] - 2) % 12 + 1
            xiao_xian_branch = _BRANCH_ROWS[xiao_index - 1][2]

        star_keys = {star.key for star in stars}
        palaces.append(
            CanonicalPalace(
                index=branch_index,
                key=palace_key,
                name=_PALACE_DISPLAY[palace_key],
                branch_key=branch_key,
                branch_name=branch_name,
                branch_element=branch_element,
                yin_yang=yin_yang,
                stem=stem_index,
                stem_name=stem_name,
                stars=tuple(stars),
                is_body_palace=bool(raw_palace.get("isBodyPalace")),
                da_xian_age=age_range[0] if age_range else None,
                da_xian_end_age=age_range[1] if len(age_range) > 1 else None,
                annual_ages=annual_ages,
                xiao_xian_branch=xiao_xian_branch,
                is_xun="xun_kong" in star_keys,
                is_triet=False,
            )
        )

    palaces.sort(key=lambda palace: palace.index)
    life_branch = str(data.get("earthlyBranchOfSoulPalace") or "")
    body_branch = str(data.get("earthlyBranchOfBodyPalace") or "")
    life_index = _BRANCH_BY_KEY[_branch_key(life_branch)][0]
    body_index = _BRANCH_BY_KEY[_branch_key(body_branch)][0]

    raw_gender = str(data.get("gender") or "").casefold()
    canonical_gender = gender if gender in (1, -1) else (-1 if raw_gender in ("nữ", "女") else 1)
    resolved_time_index = 0 if time_index is None else time_index
    resolved_hour = lunar_birth_hour or iztro_time_index_to_hour_branch(resolved_time_index)
    lunar_date = str(data.get("lunarDate") or "")
    resolved_month = lunar_birth_month or _parse_lunar_month(lunar_date)
    bureau_name = str(data.get("fiveElementsClass") or "")

    return CanonicalChart(
        palaces=tuple(palaces),
        life_palace_index=life_index,
        body_palace_index=body_index,
        lunar_birth_month=resolved_month,
        lunar_birth_hour=resolved_hour,
        five_elements_class=_parse_bureau(bureau_name),
        five_elements_class_name=bureau_name,
        gender=canonical_gender,
        time_index=resolved_time_index,
        solar_date=str(data.get("solarDate") or ""),
        lunar_date=lunar_date,
        chinese_date=chinese_date,
        year_stem_key=year_stem_key,
        year_branch_key=year_branch_key,
        soul_master=str(data.get("soul") or "") or None,
        body_master=str(data.get("body") or "") or None,
    )


def build_canonical_chart(
    day: int,
    month: int,
    year: int,
    hour_branch: int,
    gender: int,
    *,
    is_solar: bool = True,
    lunar_birth_month: int | None = None,
) -> CanonicalChart:
    """Generate an iztro chart and immediately normalize it for application use."""
    time_index = hour_branch_to_iztro_time_index(hour_branch)
    raw = get_astro_data(
        f"{year}-{month}-{day}",
        time_index,
        gender,
        is_solar=is_solar,
    )
    return to_canonical(
        raw,
        time_index=time_index,
        lunar_birth_month=lunar_birth_month,
        lunar_birth_hour=hour_branch,
        gender=gender,
    )


__all__ = [
    "BRANCH_NAME_MAP",
    "PALACE_NAME_MAP",
    "STAR_NAME_MAP",
    "STEM_NAME_MAP",
    "build_canonical_chart",
    "get_astro_data",
    "hour_branch_to_iztro_time_index",
    "iztro_time_index_to_hour_branch",
    "to_canonical",
]
