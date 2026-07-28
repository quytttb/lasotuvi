"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""

from datetime import date

import ephem

LUNAR_contract = tuple[date, bool]  # [date, thang_nhuan]


def solar_to_lunar_ephem(solar_date: ephem.Date, location: ephem.Observer, timezone: int) -> LUNAR_contract:
    solar_date += timezone * ephem.hour  # so we are working in the correct timezone

    lunar_leap = False

    previous_new_moon_date = ephem.previous_new_moon(solar_date)
    lunar_day = solar_date.day - ephem.Date(previous_new_moon_date).datetime().day + 1

    # Dong chi nam truoc
    previous_winter_solstice = ephem.previous_winter_solstice(solar_date)
    # Dong chi nam sau
    next_winter_solstice = ephem.next_winter_solstice(solar_date)

    days_in_lunar_year = ephem.previous_new_moon(next_winter_solstice) - ephem.previous_new_moon(
        previous_winter_solstice
    )

    diff = int(days_in_lunar_year / 29.0)

    lunarMonth = diff + 11

    lunarYear = solar_date.year

    # TODO: Implement find_lunar_month_between() function
    # Currently commented out as it's not implemented
    # if days_in_lunar_year > 365:
    #     lunar_leap = lunarMonth == find_lunar_month_between(
    #         previous_winter_solstice, next_winter_solstice
    #     )

    # print(days_in_lunar_year, previous_winter_solstice, next_winter_solstice)
    return tuple(date(lunarYear, lunarMonth, lunar_day), lunar_leap)


def lunar_to_solar_ephem(amlich: LUNAR_contract, location: ephem.Observer) -> LUNAR_contract:
    return amlich, location


def find_new_moon_between(start_date: ephem.Date, end_date: ephem.Date) -> int:
    newMoon = []
    while start_date < end_date:
        newMoon.append(ephem.next_new_moon(start_date))
        start_date += 29.5
    return newMoon


def find_solar_terms_between(start_date: ephem.Date, end_date: ephem.Date) -> list:
    solar_terms = []
    for degree in range(0, 330, 30):
        term = when_is_sun_at_degrees_longitude(start_date, degree)
        if term < end_date:
            solar_terms.append(term)
    return solar_terms


def when_is_sun_at_degrees_longitude(date: date, degrees: int) -> ephem.Date:
    # Thanks to Brandon Rhode @ https://answers.launchpad.net/pyephem/+question/110832

    # Find out the sun's current longitude.

    sun = ephem.Sun(date)
    current_longitude = sun.hlong - ephem.pi

    # Find approximately the right time of year.

    target_longitude = degrees * ephem.degree
    difference = (target_longitude - current_longitude) % ephem.twopi
    t0 = date + 365.25 * difference / ephem.twopi

    # Zero in on the exact moment.

    def f(t):
        sun.compute(t)
        longitude = sun.hlong - ephem.pi
        return ephem.degrees(target_longitude - longitude).znorm

    return ephem.Date(ephem.newton(f, t0, t0 + ephem.minute))
