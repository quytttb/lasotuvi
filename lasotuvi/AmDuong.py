"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""

from lasotuvi.Lich_HND import L2S, S2L, jdFromDate

thienCan = [
    {
        "id": 0,
        "chuCaiDau": None,
        "tenCan": None,
        "nguHanh": None,
        "nguHanhID": None,
        "vitriDiaBan": None,
        "amDuong": None,
    },
    {
        "id": 1,
        "chuCaiDau": "G",
        "tenCan": "Giáp",
        "nguHanh": "M",
        "nguHanhID": 2,
        "vitriDiaBan": 3,
        "amDuong": 1,
    },
    {
        "id": 2,
        "chuCaiDau": "A",
        "tenCan": "Ất",
        "nguHanh": "M",
        "nguHanhID": 2,
        "vitriDiaBan": 4,
        "amDuong": -1,
    },
    {
        "id": 3,
        "chuCaiDau": "B",
        "tenCan": "Bính",
        "nguHanh": "H",
        "nguHanhID": 4,
        "vitriDiaBan": 6,
        "amDuong": 1,
    },
    {
        "id": 4,
        "chuCaiDau": "D",
        "tenCan": "Đinh",
        "nguHanh": "H",
        "nguHanhID": 4,
        "vitriDiaBan": 7,
        "amDuong": -1,
    },
    {
        "id": 5,
        "chuCaiDau": "M",
        "tenCan": "Mậu",
        "nguHanh": "O",
        "nguHanhID": 5,
        "vitriDiaBan": 6,
        "amDuong": 1,
    },
    {
        "id": 6,
        "chuCaiDau": "K",
        "tenCan": "Kỷ",
        "nguHanh": "O",
        "nguHanhID": 5,
        "vitriDiaBan": 7,
        "amDuong": -1,
    },
    {
        "id": 7,
        "chuCaiDau": "C",
        "tenCan": "Canh",
        "nguHanh": "K",
        "nguHanhID": 1,
        "vitriDiaBan": 9,
        "amDuong": 1,
    },
    {
        "id": 8,
        "chuCaiDau": "T",
        "tenCan": "Tân",
        "nguHanh": "K",
        "nguHanhID": 1,
        "vitriDiaBan": 10,
        "amDuong": -1,
    },
    {
        "id": 9,
        "chuCaiDau": "N",
        "tenCan": "Nhâm",
        "nguHanh": "T",
        "nguHanhID": 3,
        "vitriDiaBan": 12,
        "amDuong": 1,
    },
    {
        "id": 10,
        "chuCaiDau": "Q",
        "tenCan": "Quý",
        "nguHanh": "T",
        "nguHanhID": 3,
        "vitriDiaBan": 1,
        "amDuong": -1,
    },
]


diaChi = [
    {"id": 0, "tenChi": "Hem có", "tenHanh": ":D", "amDuong": 0},
    {
        "id": 1,
        "tenChi": "Tý",
        "tenHanh": "T",
        "menhChu": "Tham lang",
        "thanChu": "Linh tinh",
        "amDuong": 1,
    },
    {
        "id": 2,
        "tenChi": "Sửu",
        "tenHanh": "O",
        "menhChu": "Cự môn",
        "thanChu": "Thiên tướng",
        "amDuong": -1,
    },
    {
        "id": 3,
        "tenChi": "Dần",
        "tenHanh": "M",
        "menhChu": "Lộc tồn",
        "thanChu": "Thiên lương",
        "amDuong": 1,
    },
    {
        "id": 4,
        "tenChi": "Mão",
        "tenHanh": "M",
        "menhChu": "Văn khúc",
        "thanChu": "Thiên đồng",
        "amDuong": -1,
    },
    {
        "id": 5,
        "tenChi": "Thìn",
        "tenHanh": "O",
        "menhChu": "Liêm trinh",
        "thanChu": "Văn xương",
        "amDuong": 1,
    },
    {
        "id": 6,
        "tenChi": "Tỵ",
        "tenHanh": "H",
        "menhChu": "Vũ khúc",
        "thanChu": "Thiên cơ",
        "amDuong": -1,
    },
    {
        "id": 7,
        "tenChi": "Ngọ",
        "tenHanh": "H",
        "menhChu": "Phá quân",
        "thanChu": "Hỏa tinh",
        "amDuong": 1,
    },
    {
        "id": 8,
        "tenChi": "Mùi",
        "tenHanh": "O",
        "menhChu": "Vũ khúc",
        "thanChu": "Thiên tướng",
        "amDuong": -1,
    },
    {
        "id": 9,
        "tenChi": "Thân",
        "tenHanh": "K",
        "menhChu": "Liêm trinh",
        "thanChu": "Thiên lương",
        "amDuong": 1,
    },
    {
        "id": 10,
        "tenChi": "Dậu",
        "tenHanh": "K",
        "menhChu": "Văn khúc",
        "thanChu": "Thiên đồng",
        "amDuong": -1,
    },
    {
        "id": 11,
        "tenChi": "Tuất",
        "tenHanh": "O",
        "menhChu": "Lộc tồn",
        "thanChu": "Văn xương",
        "amDuong": 1,
    },
    {
        "id": 12,
        "tenChi": "Hợi",
        "tenHanh": "T",
        "menhChu": "Cự môn",
        "thanChu": "Thiên cơ",
        "amDuong": -1,
    },
]


def ngayThangNam(nn, tt, nnnn, duongLich=True, timeZone=7):
    """Summary

    Args:
        nn (TYPE): ngay
        tt (TYPE): thang
        nnnn (TYPE): nam
        duongLich (bool, optional): bool
        timeZone (int, optional): +7 Vietnam

    Returns:
        TYPE: Description

    Raises:
        Exception: Description
    """
    thangNhuan = 0
    # if nnnn > 1000 and nnnn < 3000 and nn > 0 and \
    if nn > 0 and nn < 32 and tt < 13 and tt > 0:
        if duongLich is True:
            [nn, tt, nnnn, thangNhuan] = S2L(nn, tt, nnnn, timeZone=timeZone)
        return [nn, tt, nnnn, thangNhuan]
    else:
        raise Exception("Ngày, tháng, năm không chính xác.")


def canChiNgay(nn, tt, nnnn, duongLich=True, timeZone=7, thangNhuan=False):
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
        duongLich (bool, optional): True nếu là dương lịch, False âm lịch
        timeZone (int, optional): Múi giờ (mặc định 7 cho Việt Nam)
        thangNhuan (bool, optional): Có phải là tháng nhuận không?

    Returns:
        list: [canNgay, chiNgay] - Can và Chi của ngày (1-10, 1-12)
    """
    if duongLich is False:
        [nn, tt, nnnn] = L2S(nn, tt, nnnn, thangNhuan, timeZone)
    jd = jdFromDate(nn, tt, nnnn)
    # Công thức tính Can Chi từ số ngày Julian
    canNgay = (jd + 9) % 10 + 1
    chiNgay = (jd + 1) % 12 + 1
    return [canNgay, chiNgay]


def canChiGio(canNgay, gio):
    """Phần này có lẽ chưa cần thiết và sẽ bổ sung sau.

    Args:
        canNgay (int): Can của ngày cần xem, 1: Giáp, 2: Ất, 3: Bính,...
        gio (int): Chi của giờ, 1: Tý, 2: Sửu,...

    Returns:
        TYPE: Description
    """
    return False


def ngayThangNamCanChi(nn, tt, nnnn, duongLich=True, timeZone=7):
    """Chuyển đổi năm, tháng âm/dương lịch sang Can Chi.

    Công thức toán học (không có trong tài liệu Tử Vi truyền thống):
    - Can tháng = (năm × 12 + tháng + 3) % 10 + 1
    - Can năm = (năm + 6) % 10 + 1
    - Chi năm = (năm + 8) % 12 + 1

    Lưu ý: Để tính Can Chi ngày, dùng hàm canChiNgay() vì cần chuyển đổi
    qua số ngày Julian.

    Tài liệu Tử Vi: Chỉ đề cập cách phối hợp Can Chi theo chu kỳ 60 năm
    (Giáp Tý, Ất Sửu, Bính Dần...) nhưng không nêu công thức toán học.

    Args:
        nn (int): Ngày
        tt (int): Tháng
        nnnn (int): Năm
        duongLich (bool, optional): True nếu là dương lịch, False âm lịch
        timeZone (int, optional): Múi giờ

    Returns:
        list: [canThang, canNam, chiNam]
    """
    if duongLich is True:
        [nn, tt, nnnn, thangNhuan] = ngayThangNam(nn, tt, nnnn, timeZone=timeZone)
    # Can của tháng
    canThang = (nnnn * 12 + tt + 3) % 10 + 1
    # Can chi của năm
    canNamSinh = (nnnn + 6) % 10 + 1
    chiNam = (nnnn + 8) % 12 + 1

    return [canThang, canNamSinh, chiNam]


def nguHanh(tenHanh):
    """
    Args:
        tenHanh (string): Tên Hành trong ngũ hành, Kim hoặc K, Moc hoặc M,
        Thuy hoặc T, Hoa hoặc H, Tho hoặc O

    Returns:
        Dictionary: ID của Hành, tên đầy đủ của Hành, số Cục của Hành

    Raises:
        Exception: Description
    """
    if tenHanh in ["Kim", "K"]:
        return {"id": 1, "tenHanh": "Kim", "cuc": 4, "tenCuc": "Kim tứ Cục", "css": "hanhKim"}
    elif tenHanh == "Moc" or tenHanh == "M":
        return {"id": 2, "tenHanh": "Mộc", "cuc": 3, "tenCuc": "Mộc tam Cục", "css": "hanhMoc"}
    elif tenHanh == "Thuy" or tenHanh == "T":
        return {"id": 3, "tenHanh": "Thủy", "cuc": 2, "tenCuc": "Thủy nhị Cục", "css": "hanhThuy"}
    elif tenHanh == "Hoa" or tenHanh == "H":
        return {"id": 4, "tenHanh": "Hỏa", "cuc": 6, "tenCuc": "Hỏa lục Cục", "css": "hanhHoa"}
    elif tenHanh == "Tho" or tenHanh == "O":
        return {"id": 5, "tenHanh": "Thổ", "cuc": 5, "tenCuc": "Thổ ngũ Cục", "css": "hanhTho"}
    else:
        raise Exception(
            "Tên Hành phải thuộc Kim (K), Mộc (M), Thủy (T), \
             Hỏa (H) hoặc Thổ (O)"
        )


def sinhKhac(hanh1, hanh2):
    """
    Args:
        hanh1 (TYPE): Description
        hanh2 (TYPE): Description

    Returns:
        TYPE: Description
    """
    matranSinhKhac = [
        [None, None, None, None, None, None],
        [None, 0, -1, 1, -1j, 1j],
        [None, -1j, 0, 1j, 1, -1],
        [None, 1j, 1, 0, 1, -1j],
        [None, -1, 1j, -1j, 0, 1],
        [None, 1, -1j, -1, 1j, 0],
    ]
    return matranSinhKhac[hanh1][hanh2]


def nguHanhNapAm(diaChi, thienCan, xuatBanMenh=False):
    """Sử dụng Ngũ Hành nạp âm để tính Hành của năm.

    Args:
        diaChi (integer): Số thứ tự của địa chi (Tý=1, Sửu=2,...)
        thienCan (integer): Số thứ tự của thiên can (Giáp=1, Ất=2,...)

    Returns:
        Trả về chữ viết tắt Hành của năm (K, T, H, O, M)
    """
    banMenh = {
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
        nh = matranNapAm[diaChi][thienCan]
        if nh[0] in ["K", "M", "T", "H", "O"]:
            if xuatBanMenh is True:
                return banMenh[nh]
            else:
                return nh[0]
    except (KeyError, IndexError) as e:
        raise Exception(nguHanhNapAm.__doc__) from e


def dichCung(cungBanDau, *args):
    """Dịch chuyển cung theo số bước.

    Theo tài liệu Tử Vi:
    Dùng để tính vị trí các cung và sao bằng cách dịch chuyển từ vị trí ban đầu.

    Args:
        cungBanDau (int): Vị trí cung ban đầu (1-12)
        *args: Các số bước cần dịch (có thể âm hoặc dương)

    Returns:
        int: Vị trí cung sau khi dịch (1-12)
    """
    cungSauKhiDich = int(cungBanDau)
    for soCungDich in args:
        cungSauKhiDich += int(soCungDich)
    if cungSauKhiDich % 12 == 0:  # Sửa 'is' thành '==' (SyntaxWarning)
        return 12
    return cungSauKhiDich % 12


def khoangCachCung(cung1, cung2, chieu=1):
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


def timCuc(viTriCungMenhTrenDiaBan, canNamSinh):
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
        viTriCungMenhTrenDiaBan (int): Vị trí cung Mệnh (1-12)
        canNamSinh (int): Can của năm sinh (1-10)

    Returns:
        str: Tên Ngũ Hành Nạp Âm của cục
    """
    canThangGieng = (canNamSinh * 2 + 1) % 10
    canThangMenh = ((viTriCungMenhTrenDiaBan - 3) % 12 + canThangGieng) % 10
    if canThangMenh == 0:
        canThangMenh = 10
    return nguHanhNapAm(viTriCungMenhTrenDiaBan, canThangMenh)


def timTuVi(cuc, ngaySinhAmLich):
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
    cucBanDau = cuc
    if cuc not in [2, 3, 4, 5, 6]:  # Tránh trường hợp infinite loop
        raise Exception("Số cục phải là 2, 3, 4, 5, 6")
    while cuc < ngaySinhAmLich:
        cuc += cucBanDau
        cungDan += 1  # Dịch vị trí cung Dần
    saiLech = cuc - ngaySinhAmLich
    if saiLech % 2 == 1:  # Sửa 'is' thành '==' (SyntaxWarning)
        saiLech = -saiLech  # Nếu sai lệch là chẵn thì tiến, lẻ thì lùi
    return dichCung(cungDan, saiLech)


def timTrangSinh(cucSo):
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
        cucSo (int): Số cục (2, 3, 4, 5, 6)

    Returns:
        int: Vị trí cung của sao Tràng Sinh (3, 6, 9, hoặc 12)

    Raises:
        Exception: Nếu số cục không hợp lệ
    """
    if cucSo == 6:  # Hỏa lục cục
        return 3  # Tràng sinh ở Dần
    elif cucSo == 4:  # Kim tứ cục
        return 6  # Tràng sinh ở Tỵ
    elif cucSo == 2 or cucSo == 5:  # Thủy nhị cục, Thổ ngũ cục
        return 9  # Tràng sinh ở Thân
    elif cucSo == 3:  # Mộc tam cục
        return 12  # Tràng sinh ở Hợi
    else:
        # print cucSo
        raise Exception("Không tìm được cung an sao Trường sinh")


def timHoaLinh(chiNamSinh, gioSinh, gioiTinh, amDuongNamSinh):
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
        chiNamSinh (int): Chi năm sinh (1-12)
        gioSinh (int): Giờ sinh (1-12)
        gioiTinh (int): 1 = Nam, -1 = Nữ
        amDuongNamSinh (int): 1 = Dương, -1 = Âm

    Returns:
        list: [viTriHoaTinh, viTriLinhTinh]
    """
    # Xác định cung khởi đầu theo nhóm chi năm
    if chiNamSinh in [3, 7, 11]:  # Dần, Ngọ, Tuất
        khoiCungHoaTinh = 2
        khoiCungLinhTinh = 4
    elif chiNamSinh in [1, 5, 9]:  # Tý, Thìn, Thân
        khoiCungHoaTinh = 3
        khoiCungLinhTinh = 11
    elif chiNamSinh in [6, 10, 2]:  # Tị, Dậu, Sửu
        khoiCungHoaTinh = 11
        khoiCungLinhTinh = 4
    elif chiNamSinh in [12, 4, 8]:  # Hợi, Mão, Mùi
        khoiCungHoaTinh = 10
        khoiCungLinhTinh = 11
    else:
        raise Exception("Không thể khởi cung tìm Hỏa-Linh")

    # Tính vị trí theo âm dương nam nữ
    if (gioiTinh * amDuongNamSinh) == -1:  # Âm nam hoặc Dương nữ
        viTriHoaTinh = dichCung(khoiCungHoaTinh + 1, (-1) * gioSinh)
        viTriLinhTinh = dichCung(khoiCungLinhTinh - 1, gioSinh)
    elif (gioiTinh * amDuongNamSinh) == 1:  # Dương nam hoặc Âm nữ
        viTriHoaTinh = dichCung(khoiCungHoaTinh - 1, gioSinh)
        viTriLinhTinh = dichCung(khoiCungLinhTinh + 1, (-1) * gioSinh)

    return [viTriHoaTinh, viTriLinhTinh]


def timThienKhoi(canNam):
    """Tìm vị trí sao Thiên Khôi và Thiên Việt.

    Theo tài liệu Tử Vi:
    Thiên Khôi và Thiên Việt là các sao quý nhân, an theo Can năm sinh.

    Ma trận tra cứu theo Can:
    - Giáp (1) → Khôi ở Sửu (2), Việt ở Mùi
    - Ất (2) → Khôi ở Tý (1), Việt ở Thân
    - Bính (3) → Khôi ở Hợi (12), Việt ở Dậu
    - ...và các Can còn lại

    Args:
        canNam (int): Can của năm sinh (1-10)

    Returns:
        int: Vị trí cung của sao Thiên Khôi
    """
    khoiViet = [None, 2, 1, 12, 10, 8, 1, 8, 7, 6, 4]
    try:
        return khoiViet[canNam]
    except IndexError as e:
        raise Exception("Không tìm được vị trí Khôi-Việt") from e


def timThienQuanThienPhuc(canNam):
    """Tìm vị trí sao Thiên Quan và Thiên Phúc.

    Theo tài liệu Tử Vi:
    An theo Can năm sinh.

    Khẩu quyết:
    - Thiên Quan: "Giáp dương Nhâm khuyển Ất long nghi..."
    - Thiên Phúc: "Giáp ái kim kê Ất ái hầu..."

    Lưu ý: Kết hợp với Thanh Long, Hóa Khoa → "Đệ nhất Giải Thần"

    Args:
        canNam (int): Can của năm sinh (1-10)

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
        return thienQuan[canNam], thienPhuc[canNam]
    except IndexError as e:
        raise Exception("Không tìm được Quan-Phúc") from e


def timCoThan(chiNam):
    if chiNam in [12, 1, 2]:
        return 3
    elif chiNam in [3, 4, 5]:
        return 6
    elif chiNam in [6, 7, 8]:
        return 9
    else:
        return 12


def timThienMa(chiNam):
    demNghich = chiNam % 4
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


def timPhaToai(chiNam):
    demNghich = chiNam % 3
    if demNghich == 0:
        return 6
    elif demNghich == 1:
        return 10
    elif demNghich == 2:
        return 2
    else:
        raise Exception("Không tìm được Phá toái")


def timTriet(canNam):
    # Giáp Kỷ, Thân Dậu cung
    if canNam in [1, 6]:
        return 9, 10

    # Ất Canh, Ngọ Mùi cung
    elif canNam in [2, 7]:
        return 7, 8

    # Bính Tân, Thìn Tị cung
    elif canNam in [3, 8]:
        return 5, 6

    # Đinh Nhâm, Dần Mão cung
    elif canNam in [4, 9]:
        return 3, 4

    # Mậu Quý, Tý Sửu cung
    elif canNam in [5, 10]:
        return 1, 2
    else:
        raise Exception("Không tìm được Triệt")


def timLuuTru(canNam):
    maTranLuuHa = [None, 10, 11, 8, 5, 6, 7, 9, 4, 12, 3]
    maTranThienTru = [None, 6, 7, 1, 6, 7, 9, 3, 7, 10, 11]
    try:
        return maTranLuuHa[canNam], maTranThienTru[canNam]
    except IndexError as e:
        raise Exception("Không tìm được Lưu - Trù") from e
