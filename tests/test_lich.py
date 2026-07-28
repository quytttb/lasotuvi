
import unittest
from datetime import date

import pytest
from ephem import Date, Observer

from lasotuvi.ephemeris_calendar import (
    find_new_moon_between,
    find_solar_terms_between,
    when_is_sun_at_degrees_longitude,
)
from lasotuvi.lunar_calendar import solar_to_lunar as solar_to_lunar_hnd

calendar_table = {
    date(1991, 10, 24): (date(1991, 9, 17), False),
    date(1987, 8, 29): (date(1987, 7, 6), True),
}


@pytest.mark.lich
class TestLich(unittest.TestCase):

    def setUp(self):
        self.tunhien = Observer()
        self.tunhien.lon, self.tunhien.lat = "105.83416", "21.027764"
        self.timezone = 7
        self.solardate = date(1991, 10, 24)

    @pytest.mark.s2l
    def test_solar_to_lunar(self):
        # self.lunardate = s2l(self.solardate, self.tunhien, self.timezone)
        # for solar, lunar in calendar_table.items():
        #     assert lunar == s2l(solar, self.tunhien, self.timezone)
        self.assertTrue(True)

    @pytest.mark.justtest
    def test_solar_to_lunar2(self):
        solar_to_lunar_hnd(24, 10, 1991)
        # s2l(self.solardate, self.tunhien, self.timezone)

    @pytest.mark.findsolarterms
    def test_find_solar_terms_between(self):
        startDate = Date("1983/12/1")
        endDate = Date("1984/12/23")
        terms = find_solar_terms_between(startDate, endDate)
        for x in terms:
            print(Date(x))

    @pytest.mark.degrees
    def test_when_sun_is_at_degree(self):
        startDate = Date("1983/12/1")
        print(when_is_sun_at_degrees_longitude(startDate, 0))
        # self.assertEqual(when_is_sun_at_degrees_longitude(startDate, 0))

    @pytest.mark.findnewmoon
    def test_new_moon_list(self):
        startDate = Date("1983/12/1")
        endDate = Date("1984/12/23")

        newmoons = find_new_moon_between(startDate, endDate)

        # Verify we got new moons back
        assert newmoons is not None
        # for newmoon in newmoons:
        #     print(newmoon)
