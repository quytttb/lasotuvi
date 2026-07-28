"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""
import time

from lasotuvi.stem_branch import (
    day_stem_branch,
    EARTHLY_BRANCHES,
    to_lunar_ymd,
    month_year_stem_branch,
    five_element,
    nayin_element,
    generation_control,
    HEAVENLY_STEMS,
    find_element_bureau,
)
from lasotuvi.lunar_calendar import julian_day_from_date


class HeavenPlate:
    """Heaven plate / chart meta derived from birth data and earth plate."""

    def __init__(
        self,
        day: int,
        month: int,
        year: int,
        birth_hour: int,
        gender: int,
        name: str,
        earth_plate,
        is_solar: bool = True,
        timezone: int = 7,
    ):
        super().__init__()
        self.gender = 1 if gender == 1 else -1
        self.gender_label = "Nam" if gender == 1 else "Nữ"

        hour_branch = EARTHLY_BRANCHES[birth_hour]
        hour_stem = ((julian_day_from_date(day, month, year) - 1) * 2 % 10 + birth_hour) % 10
        if hour_stem == 0:
            hour_stem = 10
        self.birth_hour_branch = hour_branch
        self.birth_hour_stem = hour_stem
        self.birth_hour_label = "{} {}".format(
            HEAVENLY_STEMS[hour_stem]["stem_name"], hour_branch["branch_name"]
        )

        self.timezone = timezone
        self.today = time.strftime("%d/%m/%Y")
        self.solar_day, self.solar_month, self.solar_year, self.name = day, month, year, name
        if is_solar:
            self.lunar_day, self.lunar_month, self.lunar_year, self.is_leap_month = to_lunar_ymd(
                self.solar_day, self.solar_month, self.solar_year, True, self.timezone
            )
        else:
            self.lunar_day = self.solar_day
            self.lunar_month = self.solar_month
            self.lunar_year = self.solar_year

        self.month_stem, self.year_stem, self.year_branch = month_year_stem_branch(
            self.lunar_day, self.lunar_month, self.lunar_year, False, self.timezone
        )
        self.month_branch = self.lunar_month
        self.month_stem_name = HEAVENLY_STEMS[self.month_stem]["stem_name"]
        self.year_stem_name = HEAVENLY_STEMS[self.year_stem]["stem_name"]
        self.month_branch_name = EARTHLY_BRANCHES[self.lunar_month]["branch_name"]
        self.year_branch_name = EARTHLY_BRANCHES[self.year_branch]["branch_name"]

        self.day_stem, self.day_branch = day_stem_branch(
            self.solar_day, self.solar_month, self.solar_year, is_solar, timezone
        )
        self.day_stem_name = HEAVENLY_STEMS[self.day_stem]["stem_name"]
        self.day_branch_name = EARTHLY_BRANCHES[self.day_branch]["branch_name"]

        palace_yin_yang = 1 if (earth_plate.life_palace % 2 == 1) else -1
        self.year_stem_yin_yang = "Dương" if (self.year_branch % 2 == 1) else "Âm"
        if palace_yin_yang * self.gender == 1:
            self.life_yin_yang_status = "Âm dương thuận lý"
        else:
            self.life_yin_yang_status = "Âm dương nghịch lý"

        bureau_key = find_element_bureau(earth_plate.life_palace, self.year_stem)
        self.bureau_element_id = five_element(bureau_key)["id"]
        self.bureau_name = five_element(bureau_key)["bureau_name"]

        # Prefer traditional: life master by life-palace branch; body master by year branch
        self.life_master = EARTHLY_BRANCHES[earth_plate.life_palace]["life_master"]
        self.body_master = EARTHLY_BRANCHES[self.year_branch]["body_master"]

        self.nayin = nayin_element(self.year_branch, self.year_stem)
        natal_element_id = five_element(self.nayin)["id"]
        relation = generation_control(natal_element_id, self.bureau_element_id)
        if relation == 1:
            self.generation_control_status = "Bản Mệnh sinh Cục"
        elif relation == -1:
            self.generation_control_status = "Bản Mệnh khắc Cục"
        elif relation == -1j:
            self.generation_control_status = "Cục khắc Bản Mệnh"
        elif relation == 1j:
            self.generation_control_status = "Cục sinh Bản mệnh"
        else:
            self.generation_control_status = "Cục hòa Bản Mệnh"

        self.natal_element_name = nayin_element(self.year_branch, self.year_stem, True)
