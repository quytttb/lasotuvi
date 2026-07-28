"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""

from lasotuvi.lunar_calendar import lunar_to_solar, solar_to_lunar, julian_day_from_date

HEAVENLY_STEMS = [
    {
        "id": 0,
        "initial": None,
        "stem_name": None,
        "five_element": None,
        "element_id": None,
        "earth_plate_position": None,
        "yin_yang": None,
    },
    {
        "id": 1,
        "initial": "G",
        "stem_name": "Giáp",
        "five_element": "M",
        "element_id": 2,
        "earth_plate_position": 3,
        "yin_yang": 1,
    },
    {
        "id": 2,
        "initial": "A",
        "stem_name": "Ất",
        "five_element": "M",
        "element_id": 2,
        "earth_plate_position": 4,
        "yin_yang": -1,
    },
    {
        "id": 3,
        "initial": "B",
        "stem_name": "Bính",
        "five_element": "H",
        "element_id": 4,
        "earth_plate_position": 6,
        "yin_yang": 1,
    },
    {
        "id": 4,
        "initial": "D",
        "stem_name": "Đinh",
        "five_element": "H",
        "element_id": 4,
        "earth_plate_position": 7,
        "yin_yang": -1,
    },
    {
        "id": 5,
        "initial": "M",
        "stem_name": "Mậu",
        "five_element": "O",
        "element_id": 5,
        "earth_plate_position": 6,
        "yin_yang": 1,
    },
    {
        "id": 6,
        "initial": "K",
        "stem_name": "Kỷ",
        "five_element": "O",
        "element_id": 5,
        "earth_plate_position": 7,
        "yin_yang": -1,
    },
    {
        "id": 7,
        "initial": "C",
        "stem_name": "Canh",
        "five_element": "K",
        "element_id": 1,
        "earth_plate_position": 9,
        "yin_yang": 1,
    },
    {
        "id": 8,
        "initial": "T",
        "stem_name": "Tân",
        "five_element": "K",
        "element_id": 1,
        "earth_plate_position": 10,
        "yin_yang": -1,
    },
    {
        "id": 9,
        "initial": "N",
        "stem_name": "Nhâm",
        "five_element": "T",
        "element_id": 3,
        "earth_plate_position": 12,
        "yin_yang": 1,
    },
    {
        "id": 10,
        "initial": "Q",
        "stem_name": "Quý",
        "five_element": "T",
        "element_id": 3,
        "earth_plate_position": 1,
        "yin_yang": -1,
    },
]


EARTHLY_BRANCHES = [
    {"id": 0, "branch_name": "Hem có", "element_name": ":D", "yin_yang": 0},
    {
        "id": 1,
        "branch_name": "Tý",
        "element_name": "T",
        "life_master": "Tham lang",
        "body_master": "Linh tinh",
        "yin_yang": 1,
    },
    {
        "id": 2,
        "branch_name": "Sửu",
        "element_name": "O",
        "life_master": "Cự môn",
        "body_master": "Thiên tướng",
        "yin_yang": -1,
    },
    {
        "id": 3,
        "branch_name": "Dần",
        "element_name": "M",
        "life_master": "Lộc tồn",
        "body_master": "Thiên lương",
        "yin_yang": 1,
    },
    {
        "id": 4,
        "branch_name": "Mão",
        "element_name": "M",
        "life_master": "Văn khúc",
        "body_master": "Thiên đồng",
        "yin_yang": -1,
    },
    {
        "id": 5,
        "branch_name": "Thìn",
        "element_name": "O",
        "life_master": "Liêm trinh",
        "body_master": "Văn xương",
        "yin_yang": 1,
    },
    {
        "id": 6,
        "branch_name": "Tỵ",
        "element_name": "H",
        "life_master": "Vũ khúc",
        "body_master": "Thiên cơ",
        "yin_yang": -1,
    },
    {
        "id": 7,
        "branch_name": "Ngọ",
        "element_name": "H",
        "life_master": "Phá quân",
        "body_master": "Hỏa tinh",
        "yin_yang": 1,
    },
    {
        "id": 8,
        "branch_name": "Mùi",
        "element_name": "O",
        "life_master": "Vũ khúc",
        "body_master": "Thiên tướng",
        "yin_yang": -1,
    },
    {
        "id": 9,
        "branch_name": "Thân",
        "element_name": "K",
        "life_master": "Liêm trinh",
        "body_master": "Thiên lương",
        "yin_yang": 1,
    },
    {
        "id": 10,
        "branch_name": "Dậu",
        "element_name": "K",
        "life_master": "Văn khúc",
        "body_master": "Thiên đồng",
        "yin_yang": -1,
    },
    {
        "id": 11,
        "branch_name": "Tuất",
        "element_name": "O",
        "life_master": "Lộc tồn",
        "body_master": "Văn xương",
        "yin_yang": 1,
    },
    {
        "id": 12,
        "branch_name": "Hợi",
        "element_name": "T",
        "life_master": "Cự môn",
        "body_master": "Thiên cơ",
        "yin_yang": -1,
    },
]


def to_lunar_ymd(nn, tt, nnnn, is_solar=True, timezone=7):
    """Summary

    Args:
        nn (TYPE): ngay
        tt (TYPE): thang
        nnnn (TYPE): nam
        is_solar (bool, optional): bool
        timezone (int, optional): +7 Vietnam

    Returns:
        TYPE: Description

    Raises:
        Exception: Description
    """
    is_leap_month = 0
    # if nnnn > 1000 and nnnn < 3000 and nn > 0 and \
    if nn > 0 and nn < 32 and tt < 13 and tt > 0:
        if is_solar is True:
            [nn, tt, nnnn, is_leap_month] = solar_to_lunar(nn, tt, nnnn, timezone=timezone)
        return [nn, tt, nnnn, is_leap_month]
    else:
        raise Exception("Ngày, tháng, năm không chính xác.")


def day_stem_branch(nn, tt, nnnn, is_solar=True, timezone=7, is_leap_month=False):
    """Tính Can Chi của ngày.

    Công thức toán học (không có trong tài liệu Tử Vi truyền thống):
    - Can ngày = (Julian Day + 9) % 10 + 1
    - Chi ngày = (Julian Day + 1) % 12 + 1

    Lưu ý: Tài liệu Tử Vi chỉ đề cập phối hợp Can Chi (Giáp Tý, Ất Sửu...)
    nhưng không nêu công thức toán học. Code này sử dụng thuật toán hiện đại
    để tính tự động.

    Args:
        nn (int): Ngày
        tt (int): Tháng
        nnnn (int): Năm
        is_solar (bool, optional): True nếu là dương lịch, False âm lịch
        timezone (int, optional): Múi giờ (mặc định 7 cho Việt Nam)
        is_leap_month (bool, optional): Có phải là tháng nhuận không?

    Returns:
        list: [day_stem, day_branch] - Can và Chi của ngày (1-10, 1-12)
    """
    if is_solar is False:
        [nn, tt, nnnn] = lunar_to_solar(nn, tt, nnnn, is_leap_month, timezone)
    jd = julian_day_from_date(nn, tt, nnnn)
    # Công thức tính Can Chi từ số ngày Julian
    day_stem = (jd + 9) % 10 + 1
    day_branch = (jd + 1) % 12 + 1
    return [day_stem, day_branch]


def hour_stem_branch(day_stem, gio):
    """Phần này có lẽ chưa cần thiết và sẽ bổ sung sau.

    Args:
        day_stem (int): Can của ngày cần xem, 1: Giáp, 2: Ất, 3: Bính,...
        gio (int): Chi của giờ, 1: Tý, 2: Sửu,...

    Returns:
        TYPE: Description
    """
    return False


def month_year_stem_branch(nn, tt, nnnn, is_solar=True, timezone=7):
    """Chuyển đổi năm, tháng âm/dương lịch sang Can Chi.

    Công thức toán học (không có trong tài liệu Tử Vi truyền thống):
    - Can tháng = (năm × 12 + tháng + 3) % 10 + 1
    - Can năm = (năm + 6) % 10 + 1
    - Chi năm = (năm + 8) % 12 + 1

    Lưu ý: Để tính Can Chi ngày, dùng hàm day_stem_branch() vì cần chuyển đổi
    qua số ngày Julian.

    Tài liệu Tử Vi: Chỉ đề cập cách phối hợp Can Chi theo chu kỳ 60 năm
    (Giáp Tý, Ất Sửu, Bính Dần...) nhưng không nêu công thức toán học.

    Args:
        nn (int): Ngày
        tt (int): Tháng
        nnnn (int): Năm
        is_solar (bool, optional): True nếu là dương lịch, False âm lịch
        timezone (int, optional): Múi giờ

    Returns:
        list: [month_stem, year_stem, year_branch]
    """
    if is_solar is True:
        [nn, tt, nnnn, is_leap_month] = to_lunar_ymd(nn, tt, nnnn, timezone=timezone)
    # Can của tháng
    month_stem = (nnnn * 12 + tt + 3) % 10 + 1
    # Can chi của năm
    birth_year_stem = (nnnn + 6) % 10 + 1
    year_branch = (nnnn + 8) % 12 + 1

    return [month_stem, birth_year_stem, year_branch]


def five_element(element_name):
    """
    Args:
        element_name (string): Tên Hành trong ngũ hành, Kim hoặc K, Moc hoặc M,
        Thuy hoặc T, Hoa hoặc H, Tho hoặc O

    Returns:
        Dictionary: ID của Hành, tên đầy đủ của Hành, số Cục của Hành

    Raises:
        Exception: Description
    """
    if element_name in ["Kim", "K"]:
        return {"id": 1, "element_name": "Kim", "bureau": 4, "bureau_name": "Kim tứ Cục", "css": "hanhKim"}
    elif element_name == "Moc" or element_name == "M":
        return {"id": 2, "element_name": "Mộc", "bureau": 3, "bureau_name": "Mộc tam Cục", "css": "hanhMoc"}
    elif element_name == "Thuy" or element_name == "T":
        return {"id": 3, "element_name": "Thủy", "bureau": 2, "bureau_name": "Thủy nhị Cục", "css": "hanhThuy"}
    elif element_name == "Hoa" or element_name == "H":
        return {"id": 4, "element_name": "Hỏa", "bureau": 6, "bureau_name": "Hỏa lục Cục", "css": "hanhHoa"}
    elif element_name == "Tho" or element_name == "O":
        return {"id": 5, "element_name": "Thổ", "bureau": 5, "bureau_name": "Thổ ngũ Cục", "css": "hanhTho"}
    else:
        raise Exception(
            "Tên Hành phải thuộc Kim (K), Mộc (M), Thủy (T), \
             Hỏa (H) hoặc Thổ (O)"
        )


def generation_control(element_a, element_b):
    """
    Args:
        element_a (TYPE): Description
        element_b (TYPE): Description

    Returns:
        TYPE: Description
    """
    GENERATION_CONTROL_MATRIX = [
        [None, None, None, None, None, None],
        [None, 0, -1, 1, -1j, 1j],
        [None, -1j, 0, 1j, 1, -1],
        [None, 1j, 1, 0, 1, -1j],
        [None, -1, 1j, -1j, 0, 1],
        [None, 1, -1j, -1, 1j, 0],
    ]
    return GENERATION_CONTROL_MATRIX[element_a][element_b]


def nayin_element(branch: int, stem: int, as_natal_name=False):
    """Sử dụng Ngũ Hành nạp âm để tính Hành của năm.

    Args:
        branch (int): Earthly branch index (Zi=1 ... Hai=12)
        stem (int): Heavenly stem index (Jia=1 ... Gui=10)

    Returns:
        Trả về chữ viết tắt Hành của năm (K, T, H, O, M)
    """
    natal_element_name = {
        "K1": "HẢI TRUNG KIM",
        "T1": "GIÁNG HẠ THỦY",
        "H1": "TÍCH LỊCH HỎA",
        "O1": "BÍCH THƯỢNG THỔ",
        "M1": "TANG ÐỐ MỘC",
        "T2": "ÐẠI KHÊ THỦY",
        "H2": "LƯ TRUNG HỎA",
        "O2": "THÀNH ÐẦU THỔ",
        "M2": "TÒNG BÁ MỘC",
        "K2": "KIM BẠCH KIM",
        "H3": "PHÚ ÐĂNG HỎA",
        "O3": "SA TRUNG THỔ",
        "M3": "ÐẠI LÂM MỘC",
        "K3": "BẠCH LẠP KIM",
        "T3": "TRƯỜNG LƯU THỦY",
        "K4": "SA TRUNG KIM",
        "T4": "THIÊN HÀ THỦY",
        "H4": "THIÊN THƯỢNG HỎA",
        "O4": "LỘ BÀN THỔ",
        "M4": "DƯƠNG LIỄU MỘC",
        "T5": "TRUYỀN TRUNG THỦY",
        "H5": "SƠN HẠ HỎA",
        "O5": "ÐẠI TRẠCH THỔ",
        "M5": "THẠCH LỰU MỘC",
        "K5": "KIẾM PHONG KIM",
        "H6": "SƠN ÐẦU HỎA",
        "O6": "ỐC THƯỢNG THỔ",
        "M6": "BÌNH ÐỊA MỘC",
        "K6": "XOA XUYẾN KIM",
        "T6": "ÐẠI HẢI THỦY",
    }
    matranNapAm = [
        [0, "G", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "N", "Q"],
        [1, "K1", False, "T1", False, "H1", False, "O1", False, "M1", False],
        [2, False, "K1", False, "T1", False, "H1", False, "O1", False, "M1"],
        [3, "T2", False, "H2", False, "O2", False, "M2", False, "K2", False],
        [4, False, "T2", False, "H2", False, "O2", False, "M2", False, "K2"],
        [5, "H3", False, "O3", False, "M3", False, "K3", False, "T3", False],
        [6, False, "H3", False, "O3", False, "M3", False, "K3", False, "T3"],
        [7, "K4", False, "T4", False, "H4", False, "O4", False, "M4", False],
        [8, False, "K4", False, "T4", False, "H4", False, "O4", False, "M4"],
        [9, "T5", False, "H5", False, "O5", False, "M5", False, "K5", False],
        [10, False, "T5", False, "H5", False, "O5", False, "M5", False, "K5"],
        [11, "H6", False, "O6", False, "M6", False, "K6", False, "T6", False],
        [12, False, "H6", False, "O6", False, "M6", False, "K6", False, "T6"],
    ]
    try:
        nh = matranNapAm[branch][stem]
        if nh[0] in ["K", "M", "T", "H", "O"]:
            if as_natal_name is True:
                return natal_element_name[nh]
            else:
                return nh[0]
    except (KeyError, IndexError) as e:
        raise Exception(nayin_element.__doc__) from e


def shift_palace(start_palace, *args):
    """Dịch chuyển cung theo số bước.

    Theo tài liệu Tử Vi:
    Dùng để tính vị trí các cung và sao bằng cách dịch chuyển từ vị trí ban đầu.

    Args:
        start_palace (int): Vị trí cung ban đầu (1-12)
        *args: Các số bước cần dịch (có thể âm hoặc dương)

    Returns:
        int: Vị trí cung sau khi dịch (1-12)
    """
    shifted_palace = int(start_palace)
    for soCungDich in args:
        shifted_palace += int(soCungDich)
    if shifted_palace % 12 == 0:  # Sửa 'is' thành '==' (SyntaxWarning)
        return 12
    return shifted_palace % 12


def palace_distance(cung1, cung2, chieu=1):
    """Tính khoảng cách giữa 2 cung.

    Args:
        cung1 (int): Cung thứ nhất (1-12)
        cung2 (int): Cung thứ hai (1-12)
        chieu (int): 1 = thuận (nam), -1 = nghịch (nữ)

    Returns:
        int: Khoảng cách giữa 2 cung
    """
    if chieu == 1:  # Sửa 'is' thành '==' (SyntaxWarning) - Con trai, chiều dương
        return (cung1 - cung2 + 12) % 12
    else:
        return (cung2 - cung1 + 12) % 12


def find_element_bureau(life_palace_index, birth_year_stem):
    """Tìm Cục (Ngũ Hành Cục) theo cung Mệnh và Can năm sinh.

    Theo tài liệu Tử Vi:
    1. Xác định Can của cung Dần dựa vào Can năm sinh:
       - Giáp/Kỷ: Khởi Bính Dần
       - Ất/Canh: Khởi Mậu Dần
       - Bính/Tân: Khởi Canh Dần
       - Đinh/Nhâm: Khởi Nhâm Dần
       - Mậu/Quý: Khởi Giáp Dần
    2. Tính thuận đến cung Mệnh để biết Can của cung Mệnh
    3. Xác định Ngũ Hành Cục: Thủy nhị (2), Mộc tam (3), Kim tứ (4), Thổ ngũ (5), Hỏa lục (6)

    Args:
        life_palace_index (int): Vị trí cung Mệnh (1-12)
        birth_year_stem (int): Can của năm sinh (1-10)

    Returns:
        str: Tên Ngũ Hành Nạp Âm của cục
    """
    first_month_stem = (birth_year_stem * 2 + 1) % 10
    life_month_stem = ((life_palace_index - 3) % 12 + first_month_stem) % 10
    if life_month_stem == 0:
        life_month_stem = 10
    return nayin_element(life_palace_index, life_month_stem)


def find_zi_wei_position(cuc, ngaySinhAmLich):
    """Tìm vị trí sao Tử Vi theo Cục và ngày sinh âm lịch.

    Theo tài liệu Tử Vi (Thơ của Bạch Ngọc Thiềm tiên sinh):
    - Hỏa lục cục (số 6): Ngày mồng 1 ở Dậu (10), cộng 6 ở Tuất (11)
    - Thổ ngũ cục (số 5): Áp dụng quy tắc tương tự
    - Các cục khác: Theo quy tắc "Kê, Mã, Trư, Long, Ngưu, Hổ hậu"
      (Dậu 10, Ngọ 7, Hợi 12, Thìn 5, Sửu 2, Dần 3)

    Giải thuật:
    1. Khởi cung Dần (3)
    2. Cộng số Cục lần lượt cho đến khi >= ngày sinh
    3. Tính sai lệch: Lẻ thì đi lùi, Chẵn thì đi tiến

    Args:
        cuc (int): Số cục (2, 3, 4, 5, 6)
        ngaySinhAmLich (int): Ngày sinh âm lịch (1-30)

    Returns:
        int: Vị trí cung của sao Tử Vi (1-12)

    Raises:
        Exception: Nếu cục không hợp lệ
    """
    cungDan = 3  # Vị trí cung Dần ban đầu là 3
    initial_bureau = cuc
    if cuc not in [2, 3, 4, 5, 6]:  # Tránh trường hợp infinite loop
        raise Exception("Số cục phải là 2, 3, 4, 5, 6")
    while cuc < ngaySinhAmLich:
        cuc += initial_bureau
        cungDan += 1  # Dịch vị trí cung Dần
    saiLech = cuc - ngaySinhAmLich
    if saiLech % 2 == 1:  # Sửa 'is' thành '==' (SyntaxWarning)
        saiLech = -saiLech  # Nếu sai lệch là chẵn thì tiến, lẻ thì lùi
    return shift_palace(cungDan, saiLech)


def find_growth_stage_start(bureau):
    """Tìm vị trí sao Tràng Sinh theo số Cục.

    Theo tài liệu Tử Vi:
    - Hỏa lục cục (6) → Tràng Sinh ở Dần (3)
    - Kim tứ cục (4) → Tràng Sinh ở Tỵ (6)
    - Thủy nhị (2) hoặc Thổ ngũ (5) → Tràng Sinh ở Thân (9)
    - Mộc tam cục (3) → Tràng Sinh ở Hợi (12)

    Vòng Tràng Sinh (12 sao theo thứ tự thuận/nghịch):
    Tràng Sinh → Mộc Dục → Quan Đới → Lâm Quan → Đế Vượng → Suy →
    Bệnh → Tử → Mộ → Tuyệt → Thai → Dưỡng

    *LƯU Ý:* Theo cụ Thiên Lương:
    - Nam: Đếm thuận (theo chiều kim đồng hồ)
    - Nữ: Đếm nghịch (ngược chiều kim đồng hồ)

    Args:
        bureau (int): Số cục (2, 3, 4, 5, 6)

    Returns:
        int: Vị trí cung của sao Tràng Sinh (3, 6, 9, hoặc 12)

    Raises:
        Exception: Nếu số cục không hợp lệ
    """
    if bureau == 6:  # Hỏa lục cục
        return 3  # Tràng sinh ở Dần
    elif bureau == 4:  # Kim tứ cục
        return 6  # Tràng sinh ở Tỵ
    elif bureau == 2 or bureau == 5:  # Thủy nhị cục, Thổ ngũ cục
        return 9  # Tràng sinh ở Thân
    elif bureau == 3:  # Mộc tam cục
        return 12  # Tràng sinh ở Hợi
    else:
        # print bureau
        raise Exception("Không tìm được cung an sao Trường sinh")


def find_fire_bell_positions(birth_year_branch, birth_hour_label, gender, year_stem_yin_yang):
    """Tìm vị trí sao Hỏa Tinh và Linh Tinh.

    Theo tài liệu Tử Vi:
    Khởi cung tùy theo nhóm Chi năm sinh:
    - Dần-Ngọ-Tuất (3, 7, 11): Hỏa khởi Sửu (2), Linh khởi Mão (4)
    - Tý-Thìn-Thân (1, 5, 9): Hỏa khởi Dần (3), Linh khởi Hợi (11)
    - Tị-Dậu-Sửu (6, 10, 2): Hỏa khởi Hợi (11), Linh khởi Mão (4)
    - Hợi-Mão-Mùi (12, 4, 8): Hỏa khởi Dậu (10), Linh khởi Hợi (11)

    Cách an: Khởi giờ Tý ở vị trí đã định:
    - Hỏa Tinh: Tính thuận đến giờ sinh (nếu Dương nam/Âm nữ)
    - Linh Tinh: Tính ngược đến giờ sinh (nếu Dương nam/Âm nữ)

    Args:
        birth_year_branch (int): Chi năm sinh (1-12)
        birth_hour_label (int): Giờ sinh (1-12)
        gender (int): 1 = Nam, -1 = Nữ
        year_stem_yin_yang (int): 1 = Dương, -1 = Âm

    Returns:
        list: [viTriHoaTinh, viTriLinhTinh]
    """
    # Xác định cung khởi đầu theo nhóm chi năm
    if birth_year_branch in [3, 7, 11]:  # Dần, Ngọ, Tuất
        khoiCungHoaTinh = 2
        khoiCungLinhTinh = 4
    elif birth_year_branch in [1, 5, 9]:  # Tý, Thìn, Thân
        khoiCungHoaTinh = 3
        khoiCungLinhTinh = 11
    elif birth_year_branch in [6, 10, 2]:  # Tị, Dậu, Sửu
        khoiCungHoaTinh = 11
        khoiCungLinhTinh = 4
    elif birth_year_branch in [12, 4, 8]:  # Hợi, Mão, Mùi
        khoiCungHoaTinh = 10
        khoiCungLinhTinh = 11
    else:
        raise Exception("Không thể khởi cung tìm Hỏa-Linh")

    # Tính vị trí theo âm dương nam nữ
    if (gender * year_stem_yin_yang) == -1:  # Âm nam hoặc Dương nữ
        viTriHoaTinh = shift_palace(khoiCungHoaTinh + 1, (-1) * birth_hour_label)
        viTriLinhTinh = shift_palace(khoiCungLinhTinh - 1, birth_hour_label)
    elif (gender * year_stem_yin_yang) == 1:  # Dương nam hoặc Âm nữ
        viTriHoaTinh = shift_palace(khoiCungHoaTinh - 1, birth_hour_label)
        viTriLinhTinh = shift_palace(khoiCungLinhTinh + 1, (-1) * birth_hour_label)

    return [viTriHoaTinh, viTriLinhTinh]


def find_tian_kui(year_stem):
    """Tìm vị trí sao Thiên Khôi và Thiên Việt.

    Theo tài liệu Tử Vi:
    Thiên Khôi và Thiên Việt là các sao quý nhân, an theo Can năm sinh.

    Ma trận tra cứu theo Can:
    - Giáp (1) → Khôi ở Sửu (2), Việt ở Mùi
    - Ất (2) → Khôi ở Tý (1), Việt ở Thân
    - Bính (3) → Khôi ở Hợi (12), Việt ở Dậu
    - ...và các Can còn lại

    Args:
        year_stem (int): Can của năm sinh (1-10)

    Returns:
        int: Vị trí cung của sao Thiên Khôi
    """
    khoiViet = [None, 2, 1, 12, 10, 8, 1, 8, 7, 6, 4]
    try:
        return khoiViet[year_stem]
    except IndexError as e:
        raise Exception("Không tìm được vị trí Khôi-Việt") from e


def find_tian_guan_tian_fu(year_stem):
    """Tìm vị trí sao Thiên Quan và Thiên Phúc.

    Theo tài liệu Tử Vi:
    An theo Can năm sinh.

    Khẩu quyết:
    - Thiên Quan: "Giáp dương Nhâm khuyển Ất long nghi..."
    - Thiên Phúc: "Giáp ái kim kê Ất ái hầu..."

    Lưu ý: Kết hợp với Thanh Long, Hóa Khoa → "Đệ nhất Giải Thần"

    Args:
        year_stem (int): Can của năm sinh (1-10)

    Returns:
        list: [viTriThienQuan, viTriThienPhuc]
    """
    # Giáp dương Nhâm khuyển Ất long nghi
    # Mậu thổ Canh chư Quý mã thượng
    # Kỳ nhân quý hiển khả tiên tri
    thienQuan = [None, 8, 5, 6, 3, 4, 10, 12, 10, 11, 7]

    # Giáp ái kim kê Ất ái hầu
    # Đinh chư Bính thử Kỷ hổ đầu
    # Tân quý phùng xà phúc lộc nhiêu
    thienPhuc = [None, 10, 9, 1, 12, 4, 3, 7, 6, 7, 6]
    try:
        return thienQuan[year_stem], thienPhuc[year_stem]
    except IndexError as e:
        raise Exception("Không tìm được Quan-Phúc") from e


def find_gu_shen(year_branch):
    if year_branch in [12, 1, 2]:
        return 3
    elif year_branch in [3, 4, 5]:
        return 6
    elif year_branch in [6, 7, 8]:
        return 9
    else:
        return 12


def find_tian_ma(year_branch):
    demNghich = year_branch % 4
    if demNghich == 1:
        return 3
    elif demNghich == 2:
        return 12
    elif demNghich == 3:
        return 9
    elif demNghich == 0:
        return 6
    else:
        raise Exception("Không tìm được Thiên mã")


def find_po_sui(year_branch):
    demNghich = year_branch % 3
    if demNghich == 0:
        return 6
    elif demNghich == 1:
        return 10
    elif demNghich == 2:
        return 2
    else:
        raise Exception("Không tìm được Phá toái")


def find_triet(year_stem):
    # Giáp Kỷ, Thân Dậu cung
    if year_stem in [1, 6]:
        return 9, 10

    # Ất Canh, Ngọ Mùi cung
    elif year_stem in [2, 7]:
        return 7, 8

    # Bính Tân, Thìn Tị cung
    elif year_stem in [3, 8]:
        return 5, 6

    # Đinh Nhâm, Dần Mão cung
    elif year_stem in [4, 9]:
        return 3, 4

    # Mậu Quý, Tý Sửu cung
    elif year_stem in [5, 10]:
        return 1, 2
    else:
        raise Exception("Không tìm được Triệt")


def find_luu_tru(year_stem):
    maTranLuuHa = [None, 10, 11, 8, 5, 6, 7, 9, 4, 12, 3]
    maTranThienTru = [None, 6, 7, 1, 6, 7, 9, 3, 7, 10, 11]
    try:
        return maTranLuuHa[year_stem], maTranThienTru[year_stem]
    except IndexError as e:
        raise Exception("Không tìm được Lưu - Trù") from e
