"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""
from lasotuvi.stem_branch import five_element


class Star:
    """Summary
    Args:
        star_id (int): 1, 2, ...
        name (TYPE): Tử vi, Tham lang,...
        element (TYPE): K, M, T, H, O
        category (str, optional): Sao tốt < 10, sau xấu > 10
            1: Chính tinh, 2: Phụ tinh nói chung
            3: Quý tinh, 4: Quyền tinh, 5: Phúc tinh, 6: Văn tinh
            7: Đài các tinh, 8: Đào hoa tinh

            11: Sát tinh, 12: Bại tinh, 13: Ám tinh, 14: Dâm tinh,
            15: Hình tinh
        direction (str, optional): Bắc Đẩu tinh, Nam Bắc Đẩu tinh
        yin_yang (str, optional): Âm Dương của sao
        is_chang_sheng (int, optional): 0/None: Không thuộc vòng Tràng sinh
                                        1: Thuộc vòng Tràng sinh
    """

    def __init__(
        self, star_id, name, element, category=2, direction="", yin_yang="", is_chang_sheng=0
    ):
        super().__init__()
        self.star_id = star_id
        self.name = name
        self.element = element
        self.category = category
        self.direction = direction
        self.yin_yang = yin_yang
        self.is_chang_sheng = is_chang_sheng
        self.element_css = five_element(element)["css"]
        self.miao_wang = None

    def set_miao_wang(self, dacTinh):
        """An Đặc tính cho sao: V, M, Đ, B, H
        Args: miao_wang (str): Đặc tính của sao, Vượng (V), Miếu (M),
                                Đắc (Đ), Bình (B), Hãm (H)
        Returns:
            object: self
        """
        self.miao_wang = dacTinh
        # self.name += " (%s)" % dacTinh
        # self.element_css = dt[dacTinh]
        return self

    def set_palace_position(self, palace_position):
        """Summary

        Returns:
            TYPE: Description
        """
        self.palace_position = palace_position
        return self


# Tử vi tinh hệ
ZI_WEI = Star(1, "Tử vi", "O", 1, "Đế tinh", 1, 0)
LIAN_ZHEN = Star(2, "Liêm trinh", "H", 1, "Bắc đẩu tinh", 1, 0)
TIAN_TONG = Star(3, "Thiên đồng", "T", 1, "Bắc đẩu tinh", 1, 0)
WU_QU = Star(4, "Vũ khúc", "K", 1, "Bắc đẩu tinh", -1, 0)
TAI_YANG = Star(5, "Thái Dương", "H", 1, "Nam đẩu tinh", 1, 0)
TIAN_JI = Star(6, "Thiên cơ", "M", 1, "Nam đẩu tinh", -1, 0)

# Thiên phủ tinh hệ
TIAN_FU = Star(7, "Thiên phủ", "O", 1, "Nam đẩu tinh", 1, 0)
TAI_YIN = Star(8, "Thái âm", "T", 1, "Bắc đẩu tinh", -1, 0)
TAN_LANG = Star(9, "Tham lang", "T", 1, "Bắc đẩu tinh", -1, 0)
JU_MEN = Star(10, "Cự môn", "T", 1, "Bắc đẩu tinh", -1, 0)
TIAN_XIANG = Star(11, "Thiên tướng", "T", 1, "Nam đẩu tinh", 1, 0)
TIAN_LIANG = Star(12, "Thiên lương", "M", 1, "Nam đẩu tinh", -1, 0)
QI_SHA = Star(13, "Thất sát", "K", 1, "Nam đẩu tinh", 1, 0)
PO_JUN = Star(14, "Phá quân", "T", 1, "Bắc đẩu tinh", -1, 0)

# Vòng Địa chi - Thái tuế
TAI_SUI = Star(15, "Thái tuế", "H", 15, "", 0)
SHAO_YANG = Star(16, "Thiếu dương", "H", 5)
SANG_MEN = Star(17, "Tang môn", "M", 12)
SHAO_YIN = Star(18, "Thiếu âm", "T", 5)
GUAN_FU_3 = Star(19, "Quan phù", "H", 12)
SI_FU = Star(20, "Tử phù", "K", 12)
SUI_PO = Star(21, "Tuế phá", "H", 12)
LONG_DE = Star(22, "Long đức", "T", 5)
BAI_HU = Star(23, "Bạch hổ", "K", 12)
FU_DE = Star(24, "Phúc đức", "O", 5)
DIAO_KE = Star(25, "Điếu khách", "H", 12)
ZHI_FU = Star(26, "Trực phù", "K", 16)

#  Vòng Thiên can - Lộc tồn
LU_CUN = Star(27, "Lộc tồn", "O", 3, "Bắc đẩu tinh")
BO_SHI = Star(
    109,
    "Bác sỹ",
    "T",
    5,
)
LI_SHI = Star(28, "Lực sĩ", "H", 2)
QING_LONG = Star(29, "Thanh long", "T", 5)
XIAO_HAO = Star(30, "Tiểu hao", "H", 12)
JIANG_JUN = Star(31, "Tướng quân", "M", 4)
ZOU_SHU = Star(32, "Tấu thư", "K", 3)
FEI_LIAN = Star(33, "Phi liêm", "H", 2)
XI_SHEN = Star(34, "Hỷ thần", "H", 5)
BING_FU = Star(35, "Bệnh phù", "O", 12)
DA_HAO = Star(36, "Đại hao", "H", 12)
FU_BING = Star(37, "Phục binh", "H", 13)
GUAN_FU_2 = Star(38, "Quan phù", "H", 12)

# Vòng Tràng sinh
ZHANG_SHENG = Star(39, "Tràng sinh", "T", 5, is_chang_sheng=1)
MU_YU = Star(40, "Mộc dục", "T", 14, is_chang_sheng=1)
GUAN_DAI = Star(41, "Quan đới", "K", 4, is_chang_sheng=1)
LIN_GUAN = Star(42, "Lâm quan", "K", 7, is_chang_sheng=1)
DI_WANG = Star(43, "Đế vượng", "K", 5, is_chang_sheng=1)
SHUAI = Star(44, "Suy", "T", 12, is_chang_sheng=1)
BING = Star(45, "Bệnh", "H", 12, is_chang_sheng=1)
SI_STAR = Star(46, "Tử", "H", 12, is_chang_sheng=1)
MU = Star(47, "Mộ", "O", is_chang_sheng=1)
JUE = Star(48, "Tuyệt", "O", 12, is_chang_sheng=1)
TAI = Star(49, "Thai", "O", 14, is_chang_sheng=1)
YANG_STAR = Star(50, "Dưỡng", "M", 2, is_chang_sheng=1)

# Lục sát
#    Kình dương đà la
TUO_LUO = Star(51, "Đà la", "K", 11)
QING_YANG = Star(52, "Kình dương", "K", 11)

#    Địa không - Địa kiếp
DI_KONG = Star(53, "Địa không", "H", 11)
DI_JIE = Star(54, "Địa kiếp", "H", 11)

#    Hỏa tinh - Linh tinh
LING_XING = Star(55, "Linh tinh", "H", 11)
HUO_XING = Star(56, "Hỏa tinh", "H", 11)

# Sao Âm Dương
#    Văn xương - Văn khúc
WEN_CHANG = Star(57, "Văn xương", "K", 6)
WEN_QU = Star(58, "Văn Khúc", "T", 6)

#    Thiên khôi - Thiên Việt
TIAN_KUI = Star(59, "Thiên khôi", "H", 6)
TIAN_YUE = Star(60, "Thiên việt", "H", 6)

#    Tả phù - Hữu bật
ZUO_FU = Star(61, "Tả phù", "O", 2)
YOU_BI = Star(62, "Hữu bật", "O", 2)

#    Long trì - Phượng các
LONG_CHI = Star(63, "Long trì", "T", 3)
FENG_GE = Star(64, "Phượng các", "O", 3)

#    Tam thai - Bát tọa
SAN_TAI = Star(65, "Tam thai", "M", 7)
BA_ZUO = Star(66, "Bát tọa", "T", 7)

#    Ân quang - Thiên quý
EN_GUANG = Star(67, "Ân quang", "M", 3)
TIAN_GUI = Star(68, "Thiên quý", "O", 3)

# Sao đôi khác
TIAN_KU = Star(69, "Thiên khốc", "T", 12)
TIAN_XU = Star(70, "Thiên hư", "T", 12)
TIAN_DE = Star(71, "Thiên đức", "H", 5)
YUE_DE = Star(72, "Nguyệt đức", "H", 5)
TIAN_XING = Star(73, "Thiên hình", "H", 15)
TIAN_YAO = Star(74, "Thiên riêu", "T", 13)
TIAN_YI = Star(75, "Thiên y", "T", 5)
GUO_YIN = Star(76, "Quốc ấn", "O", 6)
TANG_FU = Star(77, "Đường phù", "M", 4)
TAO_HUA = Star(78, "Đào hoa", "M", 8)
HONG_LUAN = Star(79, "Hồng loan", "T", 8)
TIAN_XI = Star(80, "Thiên hỷ", "T", 5)
TIAN_JIE = Star(81, "Thiên giải", "H", 5)
DI_JIE_STAR = Star(82, "Địa giải", "O", 5)
JIE_SHEN = Star(83, "Giải thần", "M", 5)
TAI_FU = Star(84, "Thai phụ", "K", 6)
FENG_GAO = Star(85, "Phong cáo", "O", 4)
TIAN_CAI = Star(86, "Thiên tài", "O", 2)
TIAN_SHOU = Star(87, "Thiên thọ", "O", 5)
TIAN_SHANG = Star(88, "Thiên thương", "O", 12)
TIAN_SHI = Star(89, "Thiên sứ", "T", 12)
TIAN_LUO = Star(90, "Thiên la", "O", 12)
DI_WANG_STAR = Star(91, "Địa võng", "O", 12)
HUA_KE = Star(92, "Hóa khoa", "T", 5)
HUA_QUAN = Star(93, "Hóa quyền", "T", 4)
HUA_LU = Star(94, "Hóa lộc", "M", 3)
HUA_JI = Star(95, "Hóa kỵ", "T", 13)
GU_SHEN = Star(96, "Cô thần", "O", 13)
GUA_SU = Star(97, "Quả tú", "O", 13)
TIAN_MA = Star(98, "Thiên mã", "H", 3)
PO_SUI = Star(99, "Phá toái", "H", 12)
TIAN_GUAN = Star(100, "Thiên quan", "H", 5)
TIAN_FU_STAR = Star(101, "Thiên phúc", "H", 5)
LIU_XIA = Star(102, "Lưu hà", "T", 12)
TIAN_CHU = Star(103, "Thiên trù", "O", 5)
JIE_SHA = Star(104, "Kiếp sát", "H", 11)
HUA_GAI = Star(105, "Hoa cái", "K", 14)
WEN_XING = Star(106, "Văn tinh", "H", 6)
DOU_JUN = Star(107, "Đẩu quân", "H", 5)
TIAN_KONG = Star(108, "Thiên không", "T", 11)
