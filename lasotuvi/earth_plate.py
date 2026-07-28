"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""

from lasotuvi.stem_branch import EARTHLY_BRANCHES, shift_palace, palace_distance


class Palace:
    """One of the twelve earthly-branch palaces on the earth plate."""

    def __init__(self, palace_id: int):
        palace_element = [
            None,
            "Thủy",
            "Thổ",
            "Mộc",
            "Mộc",
            "Thổ",
            "Hỏa",
            "Hỏa",
            "Thổ",
            "Kim",
            "Kim",
            "Thổ",
            "Thủy",
        ]
        self.index = palace_id
        self.palace_element = palace_element[palace_id]
        self.stars: list = []
        self.yin_yang = -1 if (self.index % 2 == 0) else 1
        self.branch_name = EARTHLY_BRANCHES[self.index]["branch_name"]
        self.is_body_palace = False
        self.palace_name: str | None = None
        self.major_period_age: int | None = None
        self.annual_luck_branch: str | None = None
        self.is_xun = False
        self.is_triet = False

    def add_star(self, star):
        apply_star_brightness(self.index, star)
        self.stars.append(star.__dict__)
        return self

    def set_palace_name(self, palace_name: str):
        self.palace_name = palace_name
        return self

    def set_major_period(self, age: int):
        self.major_period_age = age
        return self

    def set_annual_luck(self, offset: int):
        self.annual_luck_branch = EARTHLY_BRANCHES[offset + 1]["branch_name"]
        return self

    def mark_body_palace(self):
        self.is_body_palace = True

    def mark_xun(self):
        self.is_xun = True

    def mark_triet(self):
        self.is_triet = True


class EarthPlate:
    """Earth plate (地盤): twelve palaces with placed stars."""

    def __init__(self, lunar_birth_month: int, lunar_birth_hour: int):
        super().__init__()
        self.lunar_birth_month = lunar_birth_month
        self.lunar_birth_hour = lunar_birth_hour
        self.palaces = [Palace(i) for i in range(13)]
        self.assign_palace_names()
        self.assign_body_palace_flag()

    def palace_layout(self, lunar_birth_month: int, lunar_birth_hour: int):
        self.body_palace = shift_palace(3, lunar_birth_month - 1, lunar_birth_hour - 1)
        self.life_palace = shift_palace(3, lunar_birth_month - 1, -(lunar_birth_hour) + 1)
        parents_palace = shift_palace(self.life_palace, 1)
        spirit_palace = shift_palace(self.life_palace, 2)
        property_palace = shift_palace(self.life_palace, 3)
        career_palace = shift_palace(self.life_palace, 4)
        self.servants_palace = shift_palace(self.life_palace, 5)
        travel_palace = shift_palace(self.life_palace, 6)
        self.health_palace = shift_palace(self.life_palace, 7)
        wealth_palace = shift_palace(self.life_palace, 8)
        children_palace = shift_palace(self.life_palace, 9)
        spouse_palace = shift_palace(self.life_palace, 10)
        siblings_palace = shift_palace(self.life_palace, 11)

        return [
            {"palace_id": 1, "palace_name": "Mệnh", "palace_index": self.life_palace},
            {"palace_id": 2, "palace_name": "Phụ mẫu", "palace_index": parents_palace},
            {"palace_id": 3, "palace_name": "Phúc đức", "palace_index": spirit_palace},
            {"palace_id": 4, "palace_name": "Điền trạch", "palace_index": property_palace},
            {"palace_id": 5, "palace_name": "Quan lộc", "palace_index": career_palace},
            {"palace_id": 6, "palace_name": "Nô bộc", "palace_index": self.servants_palace},
            {"palace_id": 7, "palace_name": "Thiên di", "palace_index": travel_palace},
            {"palace_id": 8, "palace_name": "Tật Ách", "palace_index": self.health_palace},
            {"palace_id": 9, "palace_name": "Tài Bạch", "palace_index": wealth_palace},
            {"palace_id": 10, "palace_name": "Tử tức", "palace_index": children_palace},
            {"palace_id": 11, "palace_name": "Phu thê", "palace_index": spouse_palace},
            {"palace_id": 12, "palace_name": "Huynh đệ", "palace_index": siblings_palace},
        ]

    def assign_palace_names(self):
        for item in self.palace_layout(self.lunar_birth_month, self.lunar_birth_hour):
            self.palaces[item["palace_index"]].set_palace_name(item["palace_name"])
        return self

    def assign_major_periods(self, bureau: int, gender: int):
        for palace in self.palaces:
            distance = palace_distance(palace.index, self.life_palace, gender)
            palace.set_major_period(bureau + distance * 10)
        return self

    def assign_annual_luck(self, annual_luck_start: int, gender: int, year_branch: int):
        zi_palace_ref = shift_palace(annual_luck_start, -gender * (year_branch - 1))
        for palace in self.palaces:
            distance = palace_distance(palace.index, zi_palace_ref, gender)
            palace.set_annual_luck(distance)
        return self

    def assign_body_palace_flag(self):
        self.palaces[self.body_palace].mark_body_palace()

    def place_stars(self, index: int, *args):
        for star in args:
            self.palaces[index].add_star(star)
        return self

    def assign_xun(self, *args):
        for palace_index in args:
            self.palaces[palace_index].mark_xun()
        return self

    def assign_triet(self, *args):
        for palace_index in args:
            self.palaces[palace_index].mark_triet()
        return self

    def get_related_palaces(self, index: int) -> dict:
        """Return opposite (xung chiếu) and trine (tam hợp) palace indices.

        Together with ``index`` itself these form *san fang si zheng*
        (三方四正): the four-palace frame used when reading a palace.
        """
        zero_indexed = index - 1
        opposite = (zero_indexed + 6) % 12 + 1
        trine_1 = (zero_indexed + 4) % 12 + 1
        trine_2 = (zero_indexed + 8) % 12 + 1

        return {
            "opposite": opposite,
            "trine_1": trine_1,
            "trine_2": trine_2,
            "all_related": [opposite, trine_1, trine_2],
        }


def apply_star_brightness(palace_index: int, star) -> None:
    brightness_matrix = {
        1: ["Tử vi", "B", "Đ", "M", "B", "V", "M", "M", "Đ", "M", "B", "V", "B"],
        2: ["Liêm trinh", "V", "Đ", "V", "H", "M", "H", "V", "Đ", "V", "H", "M", "H"],
        3: ["Thiên đồng", "V", "H", "M", "Đ", "H", "Đ", "H", "H", "M", "H", "H", "Đ"],
        4: ["Vũ khúc", "V", "M", "V", "Đ", "M", "H", "V", "M", "V", "Đ", "M", "H"],
        5: ["Thái dương", "H", "Đ", "V", "V", "V", "M", "M", "Đ", "H", "H", "H", "H"],
        6: ["Thiên cơ", "Đ", "Đ", "H", "M", "M", "V", "Đ", "Đ", "V", "M", "M", "H"],
        8: ["Thái âm", "V", "Đ", "H", "H", "H", "H", "H", "Đ", "V", "M", "M", "M"],
        9: ["Tham lang", "H", "M", "Đ", "H", "V", "H", "H", "M", "Đ", "H", "V", "H"],
        10: ["Cự môn", "V", "H", "V", "M", "H", "H", "V", "H", "Đ", "M", "H", "Đ"],
        11: ["Thiên tướng", "V", "Đ", "M", "H", "V", "Đ", "V", "Đ", "M", "H", "V", "Đ"],
        12: ["Thiên lương", "V", "Đ", "V", "V", "M", "H", "M", "Đ", "V", "H", "M", "H"],
        13: ["Thất sát", "M", "Đ", "M", "H", "H", "V", "M", "Đ", "M", "H", "H", "V"],
        14: ["Phá quân", "M", "V", "H", "H", "Đ", "H", "M", "V", "H", "H", "Đ", "H"],
        51: ["Đà la", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H"],
        52: ["Kình dương", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H"],
        55: ["Linh tinh", "H", "H", "Đ", "Đ", "Đ", "Đ", "Đ", "H", "H", "H", "H", "H"],
        56: ["Hỏa tinh", "H", "H", "Đ", "Đ", "Đ", "Đ", "Đ", "H", "H", "H", "H", "H"],
        57: ["Văn xương", "H", "Đ", "H", "Đ", "H", "Đ", "H", "Đ", "H", "H", "Đ", "Đ"],
        58: ["Văn khúc", "H", "Đ", "H", "Đ", "H", "Đ", "H", "Đ", "H", "H", "Đ", "Đ"],
        53: ["Địa không", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ"],
        54: ["Địa kiếp", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ", "H", "H", "Đ"],
        95: ["Hóa kỵ", None, "Đ", None, None, "Đ", None, None, "Đ", None, None, "Đ", None],
        36: ["Đại hao", None, None, "Đ", "Đ", None, None, None, None, "Đ", "Đ", None, None],
        30: ["Tiểu Hao", None, None, "Đ", "Đ", None, None, None, None, "Đ", "Đ", None, None],
        69: ["Thiên khốc", "Đ", "Đ", None, "Đ", None, None, "Đ", "Đ", None, "Đ", None, None],
        70: ["Thiên hư", "Đ", "Đ", None, "Đ", None, None, "Đ", "Đ", None, "Đ", None, None],
        98: ["Thiên mã", None, None, "Đ", None, None, "Đ", None, None, None, None, None, None],
        73: ["Thiên Hình", None, None, "Đ", "Đ", None, None, None, None, "Đ", "Đ", None, None],
        74: ["Thiên riêu", None, None, "Đ", "Đ", None, None, None, None, None, "Đ", "Đ", None],
    }
    if star.star_id in brightness_matrix:
        level = brightness_matrix[star.star_id][palace_index]
        if level in ["M", "V", "Đ", "B", "H"]:
            star.set_brightness(level)
