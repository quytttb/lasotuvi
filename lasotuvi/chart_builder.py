"""
(c) 2016 doanguyen <dungnv2410@gmail.com>.
"""

from lasotuvi.earth_plate import EarthPlate
from lasotuvi.stars import (
    BA_ZUO,
    BAI_HU,
    BING,
    BING_FU,
    BO_SHI,
    DA_HAO,
    DI_JIE,
    DI_JIE_STAR,
    DI_KONG,
    DI_WANG,
    DI_WANG_STAR,
    DIAO_KE,
    DOU_JUN,
    EN_GUANG,
    FEI_LIAN,
    FENG_GAO,
    FENG_GE,
    FU_BING,
    FU_DE,
    GU_SHEN,
    GUA_SU,
    GUAN_DAI,
    GUAN_FU_2,
    GUAN_FU_3,
    GUO_YIN,
    HONG_LUAN,
    HUA_GAI,
    HUA_JI,
    HUA_KE,
    HUA_LU,
    HUA_QUAN,
    HUO_XING,
    JIANG_JUN,
    JIE_SHA,
    JIE_SHEN,
    JU_MEN,
    JUE,
    LI_SHI,
    LIAN_ZHEN,
    LIN_GUAN,
    LING_XING,
    LIU_XIA,
    LONG_CHI,
    LONG_DE,
    LU_CUN,
    MU,
    MU_YU,
    PO_JUN,
    PO_SUI,
    QI_SHA,
    QING_LONG,
    QING_YANG,
    SAN_TAI,
    SANG_MEN,
    SHAO_YANG,
    SHAO_YIN,
    SHUAI,
    SI_FU,
    SI_STAR,
    SUI_PO,
    TAI,
    TAI_FU,
    TAI_SUI,
    TAI_YANG,
    TAI_YIN,
    TAN_LANG,
    TANG_FU,
    TAO_HUA,
    TIAN_CAI,
    TIAN_CHU,
    TIAN_DE,
    TIAN_FU,
    TIAN_FU_STAR,
    TIAN_GUAN,
    TIAN_GUI,
    TIAN_JI,
    TIAN_JIE,
    TIAN_KONG,
    TIAN_KU,
    TIAN_KUI,
    TIAN_LIANG,
    TIAN_LUO,
    TIAN_MA,
    TIAN_SHANG,
    TIAN_SHI,
    TIAN_SHOU,
    TIAN_TONG,
    TIAN_XI,
    TIAN_XIANG,
    TIAN_XING,
    TIAN_XU,
    TIAN_YAO,
    TIAN_YI,
    TIAN_YUE,
    TUO_LUO,
    WEN_CHANG,
    WEN_QU,
    WEN_XING,
    WU_QU,
    XI_SHEN,
    XIAO_HAO,
    YANG_STAR,
    YOU_BI,
    YUE_DE,
    ZHANG_SHENG,
    ZHI_FU,
    ZI_WEI,
    ZOU_SHU,
    ZUO_FU,
)
from lasotuvi.stem_branch import (
    EARTHLY_BRANCHES,
    HEAVENLY_STEMS,
    find_fire_bell_positions,
    find_growth_stage_start,
    find_gu_shen,
    find_luu_tru,
    find_po_sui,
    find_tian_guan_tian_fu,
    find_tian_kui,
    find_tian_ma,
    find_triet,
    find_wu_xing_ju,
    find_zi_wei_position,
    five_element,
    month_year_stem_branch,
    shift_palace,
    to_lunar_ymd,
)


def build_earth_plate(day, month, year, birth_hour, gender, is_solar, timezone):
    nn, tt, nnnn = day, month, year
    if is_solar is True:
        nn, tt, nnnn, is_leap_month = to_lunar_ymd(nn, tt, nnnn, is_solar, timezone)
    month_stem, year_stem, year_branch = month_year_stem_branch(nn, tt, nnnn, False, timezone)

    plate = EarthPlate(tt, birth_hour)

    year_stem_yin_yang = HEAVENLY_STEMS[year_stem]["yin_yang"]
    year_branch_yin_yang = EARTHLY_BRANCHES[year_branch]["yin_yang"]

    # Bản Mệnh chính là Ngũ hành nạp âm của năm sinh
    # ben_ming_name = nayin_element(year_stem, year_branch)

    wu_xing_ju_element_id = find_wu_xing_ju(plate.life_palace, year_stem)
    cuc = five_element(wu_xing_ju_element_id)
    wu_xing_ju = cuc["wu_xing_ju"]

    # Nhập đại hạn khi đã biết được số cục
    # Theo sách Số tử vi dưới góc nhìn khoa học
    # Dương Nam - Âm Nữ theo chiều thuận
    # Âm Nam - Dương Nữ theo chiều nghịch
    plate = plate.assign_da_xian(wu_xing_ju, gender * year_branch_yin_yang)

    # Nhập tiểu hạn
    xiao_xian_start = shift_palace(11, -3 * (year_branch - 1))
    plate = plate.assign_xiao_xian(xiao_xian_start, gender, year_branch)

    # Bắt đầu an Tử vi tinh hệ
    zi_wei_position = find_zi_wei_position(wu_xing_ju, nn)
    plate.place_stars(zi_wei_position, ZI_WEI)

    lian_zhen_position = shift_palace(zi_wei_position, 4)
    plate.place_stars(lian_zhen_position, LIAN_ZHEN)

    tian_tong_position = shift_palace(zi_wei_position, 7)
    plate.place_stars(tian_tong_position, TIAN_TONG)

    wu_qu_position = shift_palace(zi_wei_position, 8)
    plate.place_stars(wu_qu_position, WU_QU)

    tai_yang_position = shift_palace(zi_wei_position, 9)
    plate.place_stars(tai_yang_position, TAI_YANG)

    tian_ji_position = shift_palace(zi_wei_position, 11)
    plate.place_stars(tian_ji_position, TIAN_JI)

    # Thiên phủ tinh hệ
    # zi_wei_position = 4
    tian_fu_position = shift_palace(3, 3 - zi_wei_position)
    plate.place_stars(tian_fu_position, TIAN_FU)

    tai_yin_position = shift_palace(tian_fu_position, 1)
    plate.place_stars(tai_yin_position, TAI_YIN)

    tan_lang_position = shift_palace(tian_fu_position, 2)
    plate.place_stars(tan_lang_position, TAN_LANG)

    ju_men_position = shift_palace(tian_fu_position, 3)
    plate.place_stars(ju_men_position, JU_MEN)

    tian_xiang_position = shift_palace(tian_fu_position, 4)
    plate.place_stars(tian_xiang_position, TIAN_XIANG)

    tian_liang_position = shift_palace(tian_fu_position, 5)
    plate.place_stars(tian_liang_position, TIAN_LIANG)

    qi_sha_position = shift_palace(tian_fu_position, 6)
    plate.place_stars(qi_sha_position, QI_SHA)

    po_jun_position = shift_palace(tian_fu_position, 10)
    plate.place_stars(po_jun_position, PO_JUN)

    # Vòng Lộc tồn
    # Vị trí sao Lộc tồn ở Can của năm sinh trên địa bàn
    #  sao Bác sỹ ở cùng cung với Lộc tồn
    lu_cun_position = HEAVENLY_STEMS[year_stem]["earth_plate_position"]
    plate.place_stars(lu_cun_position, LU_CUN, BO_SHI)

    gender_yin_yang = gender * year_stem_yin_yang
    li_shi_position = shift_palace(lu_cun_position, 1 * gender_yin_yang)
    plate.place_stars(li_shi_position, LI_SHI)

    qing_long_position = shift_palace(lu_cun_position, 2 * gender_yin_yang)
    plate.place_stars(qing_long_position, QING_LONG)

    xiao_hao_position = shift_palace(lu_cun_position, 3 * gender_yin_yang)
    plate.place_stars(xiao_hao_position, XIAO_HAO)

    jiang_jun_position = shift_palace(lu_cun_position, 4 * gender_yin_yang)
    plate.place_stars(jiang_jun_position, JIANG_JUN)

    zou_shu_position = shift_palace(lu_cun_position, 5 * gender_yin_yang)
    plate.place_stars(zou_shu_position, ZOU_SHU)

    fei_lian_position = shift_palace(lu_cun_position, 6 * gender_yin_yang)
    plate.place_stars(fei_lian_position, FEI_LIAN)

    xi_shen_position = shift_palace(lu_cun_position, 7 * gender_yin_yang)
    plate.place_stars(xi_shen_position, XI_SHEN)

    bing_fu_position = shift_palace(lu_cun_position, 8 * gender_yin_yang)
    plate.place_stars(bing_fu_position, BING_FU)

    da_hao_position = shift_palace(lu_cun_position, 9 * gender_yin_yang)
    plate.place_stars(da_hao_position, DA_HAO)

    fu_bing_position = shift_palace(lu_cun_position, 10 * gender_yin_yang)
    plate.place_stars(fu_bing_position, FU_BING)

    guan_fu_2_position = shift_palace(lu_cun_position, 11 * gender_yin_yang)
    plate.place_stars(guan_fu_2_position, GUAN_FU_2)

    # Vòng Địa chi - Thái tuế
    tai_sui_position = year_branch
    plate.place_stars(tai_sui_position, TAI_SUI)

    shao_yang_position = shift_palace(tai_sui_position, 1)
    plate.place_stars(shao_yang_position, SHAO_YANG, TIAN_KONG)

    sang_men_position = shift_palace(tai_sui_position, 2)
    plate.place_stars(sang_men_position, SANG_MEN)

    shao_yin_position = shift_palace(tai_sui_position, 3)
    plate.place_stars(shao_yin_position, SHAO_YIN)

    guan_fu_3_position = shift_palace(tai_sui_position, 4)
    plate.place_stars(guan_fu_3_position, GUAN_FU_3)

    si_fu_position = shift_palace(tai_sui_position, 5)
    plate.place_stars(si_fu_position, SI_FU, YUE_DE)

    sui_po_position = shift_palace(tai_sui_position, 6)
    plate.place_stars(sui_po_position, SUI_PO)

    long_de_position = shift_palace(tai_sui_position, 7)
    plate.place_stars(long_de_position, LONG_DE)

    bai_hu_position = shift_palace(tai_sui_position, 8)
    plate.place_stars(bai_hu_position, BAI_HU)

    fu_de_position = shift_palace(tai_sui_position, 9)
    plate.place_stars(fu_de_position, FU_DE, TIAN_DE)

    diao_ke_position = shift_palace(tai_sui_position, 10)
    plate.place_stars(diao_ke_position, DIAO_KE)

    zhi_fu_position = shift_palace(tai_sui_position, 11)
    plate.place_stars(zhi_fu_position, ZHI_FU)

    #  Vòng ngũ hành cục Tràng sinh
    # !!! Đã sửa !!! *LƯU Ý Phần này đã sửa* Theo cụ Thiên Lương: Nam -> Thuận,
    # Nữ -> Nghịch (Không phù hợp)
    # **ISSUE 2**: Dương nam, Âm nữ theo chiều thuận, Âm nam Dương nữ theo
    # chiều nghịch

    growth_start_position = find_growth_stage_start(wu_xing_ju)
    plate.place_stars(growth_start_position, ZHANG_SHENG)

    mu_yu_position = shift_palace(growth_start_position, gender_yin_yang * 1)
    plate.place_stars(mu_yu_position, MU_YU)

    guan_dai_position = shift_palace(growth_start_position, gender_yin_yang * 2)
    plate.place_stars(guan_dai_position, GUAN_DAI)

    lin_guan_position = shift_palace(growth_start_position, gender_yin_yang * 3)
    plate.place_stars(lin_guan_position, LIN_GUAN)

    di_wang_position = shift_palace(growth_start_position, gender_yin_yang * 4)
    plate.place_stars(di_wang_position, DI_WANG)

    shuai_position = shift_palace(growth_start_position, gender_yin_yang * 5)
    plate.place_stars(shuai_position, SHUAI)

    bing_position = shift_palace(growth_start_position, gender_yin_yang * 6)
    plate.place_stars(bing_position, BING)

    si_position = shift_palace(growth_start_position, gender_yin_yang * 7)
    plate.place_stars(si_position, SI_STAR)

    mu_position = shift_palace(growth_start_position, gender_yin_yang * 8)
    plate.place_stars(mu_position, MU)

    jue_position = shift_palace(growth_start_position, gender_yin_yang * 9)
    plate.place_stars(jue_position, JUE)

    tai_position = shift_palace(growth_start_position, gender_yin_yang * (-1))
    plate.place_stars(tai_position, TAI)

    yang_position = shift_palace(growth_start_position, gender_yin_yang * (-2))
    plate.place_stars(yang_position, YANG_STAR)

    # An sao đôi
    #    Kình dương - Đà la
    tuo_luo_position = shift_palace(lu_cun_position, -1)
    plate.place_stars(tuo_luo_position, TUO_LUO)

    qing_yang_position = shift_palace(lu_cun_position, 1)
    plate.place_stars(qing_yang_position, QING_YANG)

    #  Không - Kiếp
    # Khởi giờ Tý ở cung Hợi, đếm thuận đến giờ sinh được cung Địa kiếp
    di_jie_position = shift_palace(11, birth_hour)
    plate.place_stars(di_jie_position, DI_JIE)

    di_kong_position = shift_palace(12, 12 - di_jie_position)
    plate.place_stars(di_kong_position, DI_KONG)

    huo_xing_position, ling_xing_position = find_fire_bell_positions(
        year_branch, birth_hour, gender, year_stem_yin_yang
    )
    plate.place_stars(huo_xing_position, HUO_XING)
    plate.place_stars(ling_xing_position, LING_XING)

    long_chi_position = shift_palace(5, year_branch - 1)
    plate.place_stars(long_chi_position, LONG_CHI)

    feng_ge_position = shift_palace(2, 2 - long_chi_position)
    plate.place_stars(feng_ge_position, FENG_GE, JIE_SHEN)

    zuo_fu_position = shift_palace(5, tt - 1)
    plate.place_stars(zuo_fu_position, ZUO_FU)

    you_bi_position = shift_palace(2, 2 - zuo_fu_position)
    plate.place_stars(you_bi_position, YOU_BI)

    wen_qu_position = shift_palace(5, birth_hour - 1)
    plate.place_stars(wen_qu_position, WEN_QU)

    wen_chang_position = shift_palace(2, 2 - wen_qu_position)
    plate.place_stars(wen_chang_position, WEN_CHANG)

    san_tai_position = shift_palace(5, tt + nn - 2)
    plate.place_stars(san_tai_position, SAN_TAI)

    ba_zuo_position = shift_palace(2, 2 - san_tai_position)
    plate.place_stars(ba_zuo_position, BA_ZUO)

    # ! Vị trí sao Ân Quang - Thiên Quý
    # ! Lấy cung thìn làm mồng 1 đếm thuận đến ngày sinh,
    # ! lui lại một cung để lấy đó làm giờ tý đếm thuận đến giờ sinh là
    #  Ân Quang
    # ! Thiên Quý đối với Ân Quang qua trục Sửu Mùi
    # @ en_guang_position = shift_palace(5, nn + birth_hour - 3)
    # @ tian_gui_position = shift_palace(2, 2 - en_guang_position)
    # Phía trên là cách an Quang-Quý theo cụ Vu Thiên
    # Sau khi tìm hiểu thì Quang-Quý sẽ được an theo Xương-Khúc như sau:
    # Ân Quang − Xem Văn Xương ở cung nào, kể cung ấy là mồng một
    # bắt đầu đếm thoe chiều thuận đến ngày sinh, lùi lại một cung,
    # an Ân Quang.
    # Thiên Quý − Xem Văn Khúc ở cung nào, kể cung ấy là mồng một,
    # !!! bắt đầu đếm theo chiều nghịch đến ngày sinh, lùi lại một cung,
    # an Thiên Quý.!!!
    # ??? Thiên Quý ở đối cung của Ân Quang qua trục Sửu Mùi mới chính xác???

    en_guang_position = shift_palace(wen_chang_position, nn - 2)
    plate.place_stars(en_guang_position, EN_GUANG)

    tian_gui_position = shift_palace(2, 2 - en_guang_position)
    plate.place_stars(tian_gui_position, TIAN_GUI)

    tian_kui_position = find_tian_kui(year_stem)
    plate.place_stars(tian_kui_position, TIAN_KUI)

    tian_yue_position = shift_palace(5, 5 - tian_kui_position)
    plate.place_stars(tian_yue_position, TIAN_YUE)

    tian_xu_position = shift_palace(7, year_branch - 1)
    plate.place_stars(tian_xu_position, TIAN_XU)

    tian_ku_position = shift_palace(7, -year_branch + 1)
    plate.place_stars(tian_ku_position, TIAN_KU)

    tian_cai_position = shift_palace(plate.life_palace, year_branch - 1)
    plate.place_stars(tian_cai_position, TIAN_CAI)

    tian_shou_position = shift_palace(plate.body_palace, year_branch - 1)
    plate.place_stars(tian_shou_position, TIAN_SHOU)

    hong_luan_position = shift_palace(4, -year_branch + 1)
    plate.place_stars(hong_luan_position, HONG_LUAN)

    tian_xi_position = shift_palace(hong_luan_position, 6)
    plate.place_stars(tian_xi_position, TIAN_XI)

    #  Thiên Quan - Thiên Phúc
    tian_guan_position, tian_fu_star_position = find_tian_guan_tian_fu(year_stem)
    plate.place_stars(tian_guan_position, TIAN_GUAN)
    plate.place_stars(tian_fu_star_position, TIAN_FU_STAR)

    tian_xing_position = shift_palace(10, tt - 1)
    plate.place_stars(tian_xing_position, TIAN_XING)

    tian_yao_position = shift_palace(tian_xing_position, 4)
    plate.place_stars(tian_yao_position, TIAN_YAO, TIAN_YI)

    gu_shen_position = find_gu_shen(year_branch)
    plate.place_stars(gu_shen_position, GU_SHEN)

    gua_su_position = shift_palace(gu_shen_position, -4)
    plate.place_stars(gua_su_position, GUA_SU)

    wen_xing_position = shift_palace(qing_yang_position, 2)
    plate.place_stars(wen_xing_position, WEN_XING)

    tang_fu_position = shift_palace(wen_xing_position, 2)
    plate.place_stars(tang_fu_position, TANG_FU)

    guo_yin_position = shift_palace(tang_fu_position, 3)
    plate.place_stars(guo_yin_position, GUO_YIN)

    # Thai phụ - Phong Cáo
    tai_fu_position = shift_palace(wen_qu_position, 2)
    plate.place_stars(tai_fu_position, TAI_FU)

    feng_gao_position = shift_palace(wen_qu_position, -2)
    plate.place_stars(feng_gao_position, FENG_GAO)

    # Thiên giải - Địa giải
    #    Theo cụ Thiên Lương: Lấy cung Thân làm tháng Giêng, đếm thuận nhưng
    #    nhảy cung là Thiên giải. Một số trang web đếm nhưng không nhảy cung???
    #    Liệu phương cách nào đúng?
    tian_jie_position = shift_palace(9, (2 * tt) - 2)
    plate.place_stars(tian_jie_position, TIAN_JIE)

    di_jie_star_position = shift_palace(zuo_fu_position, 3)
    plate.place_stars(di_jie_star_position, DI_JIE_STAR)

    # Thiên la - Địa võng, Thiên thương - Thiên sứ
    tian_luo_position = 5
    plate.place_stars(tian_luo_position, TIAN_LUO)

    di_wang_net_position = 11
    plate.place_stars(di_wang_net_position, DI_WANG_STAR)

    tian_shang_position = plate.servants_palace
    plate.place_stars(tian_shang_position, TIAN_SHANG)

    tian_shi_position = plate.health_palace
    plate.place_stars(tian_shi_position, TIAN_SHI)

    # Vòng Thiên mã
    tian_ma_position = find_tian_ma(year_branch)
    plate.place_stars(tian_ma_position, TIAN_MA)

    hua_gai_position = shift_palace(tian_ma_position, 2)
    plate.place_stars(hua_gai_position, HUA_GAI)

    jie_sha_position = shift_palace(tian_ma_position, 3)
    plate.place_stars(jie_sha_position, JIE_SHA)

    tao_hua_position = shift_palace(jie_sha_position, 4)
    plate.place_stars(tao_hua_position, TAO_HUA)

    # Phá toái
    po_sui_position = find_po_sui(year_branch)
    plate.place_stars(po_sui_position, PO_SUI)

    # Đẩu quân
    dou_jun_position = shift_palace(year_branch, -tt + birth_hour)
    plate.place_stars(dou_jun_position, DOU_JUN)

    #  Tứ Hóa
    # An theo 10 câu của cụ Thiên Lương trong cuốn
    # Số tử vi dưới mắt khoa học

    if year_stem == 1:
        hua_lu_position = lian_zhen_position
        hua_quan_position = po_jun_position
        hua_ke_position = wu_qu_position
        hua_ji_position = tai_yang_position
    elif year_stem == 2:
        hua_lu_position = tian_ji_position
        hua_quan_position = tian_liang_position
        hua_ke_position = zi_wei_position
        hua_ji_position = tai_yin_position
    elif year_stem == 3:
        hua_lu_position = tian_tong_position
        hua_quan_position = tian_ji_position
        hua_ke_position = wen_chang_position
        hua_ji_position = lian_zhen_position
    elif year_stem == 4:
        hua_lu_position = tai_yin_position
        hua_quan_position = tian_tong_position
        hua_ke_position = tian_ji_position
        hua_ji_position = ju_men_position
    elif year_stem == 5:
        hua_lu_position = tan_lang_position
        hua_quan_position = tai_yin_position
        hua_ke_position = you_bi_position
        hua_ji_position = tian_ji_position
    elif year_stem == 6:
        hua_lu_position = wu_qu_position
        hua_quan_position = tan_lang_position
        hua_ke_position = tian_liang_position
        hua_ji_position = wen_qu_position
    elif year_stem == 7:
        hua_lu_position = tai_yang_position
        hua_quan_position = wu_qu_position
        hua_ke_position = tian_tong_position
        hua_ji_position = tai_yin_position
    elif year_stem == 8:
        hua_lu_position = ju_men_position
        hua_quan_position = tai_yang_position
        hua_ke_position = wen_qu_position
        hua_ji_position = wen_chang_position
    elif year_stem == 9:
        hua_lu_position = tian_liang_position
        hua_quan_position = zi_wei_position
        hua_ke_position = tian_fu_position
        hua_ji_position = wu_qu_position
    elif year_stem == 10:
        hua_lu_position = po_jun_position
        hua_quan_position = ju_men_position
        hua_ke_position = tai_yin_position
        hua_ji_position = tan_lang_position

    plate.place_stars(hua_lu_position, HUA_LU)
    plate.place_stars(hua_quan_position, HUA_QUAN)
    plate.place_stars(hua_ke_position, HUA_KE)
    plate.place_stars(hua_ji_position, HUA_JI)

    #  An Lưu Hà - Thiên Trù
    # Sách cụ Thiên Lương không đề cập đến 2 sao này
    # Mong mọi người kiểm chứng
    liu_xia_position, tian_chu_position = find_luu_tru(year_stem)
    plate.place_stars(liu_xia_position, LIU_XIA)
    plate.place_stars(tian_chu_position, TIAN_CHU)

    # An Tuần, Triệt
    xun_end = shift_palace(year_branch, 10 - year_stem)
    xun_palace_1 = shift_palace(xun_end, 1)
    xun_palace_2 = shift_palace(xun_palace_1, 1)
    plate.assign_xun(xun_palace_1, xun_palace_2)

    triet_palace_1, triet_palace_2 = find_triet(year_stem)
    plate.assign_triet(triet_palace_1, triet_palace_2)
    return plate
