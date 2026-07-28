"""
(c) 2006 Ho Ngoc Duc.
Astronomical algorithms from "Astronomical Algorithms" by Jean Meeus, 1998.

Vietnamese lunar/solar calendar conversion helpers used by the chart engine.
"""

import math


def julian_day_from_date(dd, mm, yy):
    """Tính số ngày Julian từ ngày/tháng/năm (Julian Day Number).

    Công thức từ "Astronomical Algorithms" by Jean Meeus (1998).
    Julian Day là số ngày kể từ 1/1/4713 BC (lịch Julian) đến ngày dd/mm/yyyy.

    Args:
        dd: Ngày
        mm: Tháng
        yy: Năm

    Returns:
        int: Số ngày Julian

    Ví dụ:
        julian_day_from_date(1, 1, 2000) = 2451545
    """
    a = int((14 - mm) / 12.0)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = (
        dd
        + int((153 * m + 2) / 5.0)
        + 365 * y
        + int(y / 4.0)
        - int(y / 100.0)
        + int(y / 400.0)
        - 32045
    )
    if jd < 2299161:
        jd = dd + int((153 * m + 2) / 5.0) + 365 * y + int(y / 4.0) - 32083
    return jd


def julian_day_to_date(jd):
    """Chuyển số ngày Julian về ngày/tháng/năm.

    Phân biệt lịch Gregory (sau 5/10/1582) và lịch Julian (trước đó).

    Args:
        jd (int): Số ngày Julian

    Returns:
        list: [ngày, tháng, năm]
    """
    if jd > 2299160:
        # Sau 5/10/1582: Lịch Gregory (Gregorian calendar)
        a = jd + 32044
        b = int((4 * a + 3) / 146097.0)
        c = a - int((b * 146097) / 4.0)
    else:
        b = 0
        c = jd + 32082
    d = int((4 * c + 3) / 1461.0)
    e = c - int((1461 * d) / 4.0)
    m = int((5 * e + 2) / 153.0)
    day = e - int((153 * m + 2) / 5.0) + 1
    month = m + 3 - 12 * int(m / 10.0)
    year = b * 100 + d - 4800 + int(m / 10.0)
    return [day, month, year]


def new_moon(k):
    """Tính thời điểm trăng non (sóc) thứ k sau trăng non ngày 1/1/1900 13:52 UTC.

    Công thức từ "Astronomical Algorithms" by Jean Meeus (1998), Chapter 49.
    Sử dụng các tham số thiên văn như độ lệch tâm quỹ đạo mặt trăng,
    bất thường trung bình của mặt trời và mặt trăng.

    Args:
        k (int): Số thứ tự trăng non (k=0 là 1/1/1900)

    Returns:
        float: Số ngày Julian của thời điểm trăng non
               Ví dụ: 2415079.9758617813 cho k=2
    2414961.935157746 for k=-2."""
    # Time in Julian centuries from 1900 January 0.5
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = math.pi / 180.0
    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 = Jd1 + 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    # Mean new moon
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    # Sun's mean anomaly
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    # Moon's mean anomaly
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    # Moon's argument of latitude
    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 = C1 - 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(dr * 2 * Mpr)
    C1 = C1 - 0.0004 * math.sin(dr * 3 * Mpr)
    C1 = C1 + 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    C1 = C1 - 0.0074 * math.sin(dr * (M - Mpr)) + 0.0004 * math.sin(dr * (2 * F + M))
    C1 = C1 - 0.0004 * math.sin(dr * (2 * F - M)) - 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 = C1 + 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))
    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2
    jd_new = Jd1 + C1 - deltat
    return jd_new


def sun_longitude(jdn):
    """def sun_longitude(jdn): Compute the longitude of the sun at any time.
    Parameter: floating number jdn, the number of days since 1/1/4713 BC noon.
    """
    T = (jdn - 2451545.0) / 36525.0
    # Time in Julian centuries
    # from 2000-01-01 12:00:00 GMT
    T2 = T * T
    dr = math.pi / 180.0  # degree to radian
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    # mean anomaly, degree
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    # mean longitude, degree
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL += (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = L0 + DL  # true longitude, degree
    L = L * dr
    L = L - math.pi * 2 * (float(L / (math.pi * 2)))
    # Normalize to (0, 2*math.pi)
    return L


def get_sun_longitude_old(dayNumber, timezone):
    """def get_sun_longitude(dayNumber, timezone):
    Compute sun position at midnight of the day with the given Julian day number.
    The time zone if the time difference between local time, UTC: 7.0 for UTC+7:00

    The function returns a number between 0 and 11. From the day after March
    equinox and the 1st major term after March equinox, 0 is returned.
    After that, return 1, 2, 3 ..."""
    return int(sun_longitude(dayNumber - 0.5 - timezone / 24.0) / math.pi * 6)


def get_sun_longitude(jdn, timezone):
    T = (jdn - 2451545.5 - timezone / 24.0) / 36525.0
    T2 = T**2
    dr = math.pi / 180.0
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL = DL + (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = L0 + DL
    omega = 125.04 - 1934.136 * T
    L = L - 0.00569 - 0.00478 * math.sin(omega * dr)
    L = L * dr
    L = L - math.pi * 2 * (math.floor(L / (math.pi * 2)))
    return int(L / math.pi * 6)


def get_new_moon_day(k, timezone):
    """def get_new_moon_day(k, timezone): Compute the day of the k-th new moon
    in the given time zone. The time zone if the time difference between local
    time and UTC: 7.0 for UTC+7:00."""
    return int(new_moon(k) + 0.5 + timezone / 24.0)


def get_lunar_month_11(yy, timezone):
    """def get_lunar_month_11(yy, timezone):  Find the day that starts the luner month
    11of the given year for the given time zone."""
    # off = julian_day_from_date(31, 12, yy) \
    #            - 2415021.076998695
    off = julian_day_from_date(31, 12, yy) - 2415021.0
    k = int(off / 29.530588853)
    nm = get_new_moon_day(k, timezone)
    sunLong = get_sun_longitude(nm, timezone)
    # sun longitude at local midnight
    if sunLong >= 9:
        nm = get_new_moon_day(k - 1, timezone)
    return nm


# print get_lunar_month_11(1992, 7)
def get_leap_month_offset(a11, timezone):
    """def get_leap_month_offset(a11, timezone): Find the index of the leap month
    after the month starting on the day a11."""
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1  # start with month following lunar month 11
    arc = get_sun_longitude(get_new_moon_day(k + i, timezone), timezone)
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(get_new_moon_day(k + i, timezone), timezone)
        if not (arc != last and i < 14):
            break
    return i - 1


def solar_to_lunar(dd, mm, yy, timezone=7):
    """def solar_to_lunar(dd, mm, yy, timezone = 7): Convert solar date dd/mm/yyyy to
    the corresponding lunar date."""
    dayNumber = julian_day_from_date(dd, mm, yy)
    k = int((dayNumber - 2415021.076998695) / 29.530588853)
    monthStart = get_new_moon_day(k + 1, timezone)
    if monthStart > dayNumber:
        monthStart = get_new_moon_day(k, timezone)
    # alert(dayNumber + " -> " + monthStart)
    a11 = get_lunar_month_11(yy, timezone)
    b11 = a11
    if a11 >= monthStart:
        lunarYear = yy
        a11 = get_lunar_month_11(yy - 1, timezone)
    else:
        lunarYear = yy + 1
        b11 = get_lunar_month_11(yy + 1, timezone)
    lunarDay = dayNumber - monthStart + 1
    diff = int((monthStart - a11) / 29.0)

    lunarLeap = 0
    lunarMonth = diff + 11

    if b11 - a11 > 365:
        leapMonthDiff = get_leap_month_offset(a11, timezone)
        if diff >= leapMonthDiff:
            lunarMonth = diff + 10
            if diff == leapMonthDiff:
                lunarLeap = 1
    if lunarMonth > 12:
        lunarMonth = lunarMonth - 12
    if lunarMonth >= 11 and diff < 4:
        lunarYear -= 1
    # print [lunarDay, lunarMonth, lunarYear, lunarLeap]
    return [lunarDay, lunarMonth, lunarYear, lunarLeap]


def lunar_to_solar(lunarD, lunarM, lunarY, lunarLeap, tZ=7):
    """def lunar_to_solar(lunarD, lunarM, lunarY, lunarLeap, tZ = 7): Convert a lunar date
    to the corresponding solar date."""
    if lunarM < 11:
        a11 = get_lunar_month_11(lunarY - 1, tZ)
        b11 = get_lunar_month_11(lunarY, tZ)
    else:
        a11 = get_lunar_month_11(lunarY, tZ)
        b11 = get_lunar_month_11(lunarY + 1, tZ)
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunarM - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        leapOff = get_leap_month_offset(a11, tZ)
        leapM = leapOff - 2
        if leapM < 0:
            leapM += 12
        if lunarLeap != 0 and lunarM != leapM:
            return [0, 0, 0]
        elif lunarLeap != 0 or off >= leapOff:
            off += 1
    monthStart = get_new_moon_day(k + off, tZ)
    return julian_day_to_date(monthStart + lunarD - 1)
