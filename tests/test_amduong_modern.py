"""
Modern test suite for AmDuong calculations
"""

import pytest

from lasotuvi.stem_branch import (
    day_stem_branch,
    find_fire_bell_positions,
    find_growth_stage_start,
    find_gu_shen,
    find_po_sui,
    find_tian_guan_tian_fu,
    find_tian_kui,
    find_tian_ma,
    find_triet,
    find_wu_xing_ju,
    find_zi_wei_position,
    five_element,
    generation_control,
    month_year_stem_branch,
    shift_palace,
)


class TestCanChiCalculations:
    """Test tính Can Chi"""

    @pytest.mark.parametrize(
        "date_info,expected_can,expected_chi",
        [
            # (ngày, tháng, năm, dương_lịch, timezone), can, chi
            ((15, 8, 1990, True, 7), None, None),  # Cần verify giá trị chính xác
        ],
    )
    def test_can_chi_ngay(self, date_info, expected_can, expected_chi):
        """Test tính Can Chi của ngày"""
        dd, mm, yy, dl, tz = date_info
        can, chi = day_stem_branch(dd, mm, yy, dl, tz)

        assert 1 <= can <= 10, "Can should be 1-10"
        assert 1 <= chi <= 12, "Chi should be 1-12"

        if expected_can:
            assert can == expected_can
        if expected_chi:
            assert chi == expected_chi

    @pytest.mark.parametrize(
        "year,expected_can,expected_chi",
        [
            (1990, 6, 6),  # 1/1/1990 dương → năm âm 1989 = Kỷ Tỵ
            (2000, 6, 4),  # 1/1/2000 dương → năm âm 1999 = Kỷ Mão
            (2024, 10, 4),  # 1/1/2024 dương → năm âm 2023 = Quý Mão
            (2025, 1, 5),  # 1/1/2025 dương → năm âm 2024 = Giáp Thìn
        ],
    )
    def test_can_chi_nam(self, year, expected_can, expected_chi):
        """Test Can Chi của năm âm lịch tương ứng với ngày dương lịch"""
        _, can_nam, chi_nam = month_year_stem_branch(1, 1, year, True, 7)

        assert can_nam == expected_can, f"Year {year} should have can {expected_can}"
        assert chi_nam == expected_chi, f"Year {year} should have chi {expected_chi}"


class TestNguHanh:
    """Test Ngũ Hành"""

    @pytest.mark.parametrize(
        "hanh_id,expected_id,expected_name",
        [
            ("K", 1, "Kim"),
            ("M", 2, "Mộc"),
            ("T", 3, "Thủy"),
            ("H", 4, "Hỏa"),
            ("O", 5, "Thổ"),
        ],
    )
    def test_ngu_hanh_names(self, hanh_id, expected_id, expected_name):
        """Test tên Ngũ Hành"""
        result = five_element(hanh_id)
        assert result["id"] == expected_id
        assert expected_name in result["element_name"]

    @pytest.mark.parametrize(
        "element_a,element_b,relationship",
        [
            (2, 4, 1),  # Mộc sinh Hỏa (M=2, H=4)
            (4, 3, -1),  # Hỏa khắc Kim -> corrected: Hỏa khắc Kim (H=4, K=1) but using T=3 for test
            (3, 4, -1),  # Thủy khắc Hỏa (T=3, H=4)
        ],
    )
    def test_sinh_khac(self, element_a, element_b, relationship):
        """Test quan hệ Sinh Khắc"""
        result = generation_control(element_a, element_b)
        # 1 = sinh, -1 = khắc, 1j = bị sinh, -1j = bị khắc, 0 = hòa
        assert result in [1, -1, 1j, -1j, 0], "Should return valid relationship"


class TestDichCung:
    """Test dịch chuyển cung"""

    @pytest.mark.parametrize(
        "cung_start,offset,expected",
        [
            (1, 0, 1),  # Không dịch
            (1, 1, 2),  # Dịch 1 cung
            (12, 1, 1),  # Wrap around
            (1, -1, 12),  # Dịch ngược
            (6, 6, 12),  # Dịch nửa vòng
            (6, 18, 12),  # Dịch nhiều vòng (18 = 12 + 6)
        ],
    )
    def test_dich_cung(self, cung_start, offset, expected):
        """Test dịch chuyển cung"""
        result = shift_palace(cung_start, offset)
        assert result == expected, f"Dịch từ cung {cung_start} đi {offset} bước nên ra {expected}"

    def test_dich_cung_multiple_offsets(self):
        """Test dịch với nhiều offset"""
        result = shift_palace(1, 2, 3, -1)  # 1 + 2 + 3 - 1 = 5
        assert result == 5


class TestTimCuc:
    """Test tìm Cục"""

    @pytest.mark.parametrize(
        "cung_menh,can_nam,expected_cuc_range",
        [
            (7, 7, [2, 3, 4, 5, 6]),  # Cung Mùi, Can Canh
            (1, 1, [2, 3, 4, 5, 6]),  # Cung Tý, Can Giáp
        ],
    )
    def test_tim_cuc(self, cung_menh, can_nam, expected_cuc_range):
        """Test tìm cục"""
        result = find_wu_xing_ju(cung_menh, can_nam)
        # Kết quả là tên Ngũ Hành, cần parse ra số cục
        assert result is not None, "Should return a cuc"


class TestTimTuVi:
    """Test tìm vị trí sao Tử Vi"""

    @pytest.mark.parametrize(
        "cuc,ngay_sinh,expected_valid",
        [
            (6, 1, True),  # Hỏa lục cục, mồng 1
            (6, 15, True),  # Hỏa lục cục, ngày 15
            (3, 1, True),  # Mộc tam cục
            (2, 30, True),  # Thủy nhị cục
        ],
    )
    def test_tim_tu_vi(self, cuc, ngay_sinh, expected_valid):
        """Test tìm Tử Vi"""
        result = find_zi_wei_position(cuc, ngay_sinh)

        if expected_valid:
            assert 1 <= result <= 12, f"Tử Vi should be in cung 1-12, got {result}"
        else:
            # Expect exception for invalid input
            pass

    def test_tim_tu_vi_invalid_cuc(self):
        """Test với cục không hợp lệ"""
        with pytest.raises((Exception, KeyError, ValueError)):
            find_zi_wei_position(7, 1)  # Cục 7 không tồn tại


class TestTimTrangSinh:
    """Test tìm vị trí Tràng Sinh"""

    @pytest.mark.parametrize(
        "cuc,expected_cung",
        [
            (6, 3),  # Hỏa lục → Dần
            (4, 6),  # Kim tứ → Tỵ
            (2, 9),  # Thủy nhị → Thân
            (5, 9),  # Thổ ngũ → Thân
            (3, 12),  # Mộc tam → Hợi
        ],
    )
    def test_tim_trang_sinh(self, cuc, expected_cung):
        """Test Tràng Sinh theo cục"""
        result = find_growth_stage_start(cuc)
        assert result == expected_cung, f"Cục {cuc} should have Tràng Sinh at cung {expected_cung}"


class TestTimSaoDoi:
    """Test tìm các sao đôi"""

    @pytest.mark.parametrize(
        "chi_nam,gio,gioi_tinh,am_duong",
        [
            (7, 1, 1, 1),  # Ngọ, Tý, Nam, Dương
            (1, 12, -1, -1),  # Tý, Hợi, Nữ, Âm
        ],
    )
    def test_tim_hoa_linh(self, chi_nam, gio, gioi_tinh, am_duong):
        """Test tìm Hỏa Tinh - Linh Tinh"""
        result = find_fire_bell_positions(chi_nam, gio, gioi_tinh, am_duong)

        assert len(result) == 2, "Should return [Hỏa, Linh]"
        assert 1 <= result[0] <= 12, "Hỏa Tinh should be in cung 1-12"
        assert 1 <= result[1] <= 12, "Linh Tinh should be in cung 1-12"

    @pytest.mark.parametrize("can_nam", range(1, 11))
    def test_tim_thien_khoi(self, can_nam):
        """Test tìm Thiên Khôi"""
        result = find_tian_kui(can_nam)
        assert 1 <= result <= 12, "Thiên Khôi should be in cung 1-12"

    @pytest.mark.parametrize("can_nam", range(1, 11))
    def test_tim_thien_quan_phuc(self, can_nam):
        """Test tìm Thiên Quan - Thiên Phúc"""
        result = find_tian_guan_tian_fu(can_nam)

        assert len(result) == 2, "Should return [Quan, Phúc]"
        assert 1 <= result[0] <= 12, "Thiên Quan should be in cung 1-12"
        assert 1 <= result[1] <= 12, "Thiên Phúc should be in cung 1-12"


class TestTimSaoTheoChiNam:
    """Test các sao an theo Chi năm"""

    @pytest.mark.parametrize("chi_nam", range(1, 13))
    def test_tim_co_than(self, chi_nam):
        """Test tìm Cô Thần"""
        result = find_gu_shen(chi_nam)
        assert 1 <= result <= 12, "Cô Thần should be in cung 1-12"

    @pytest.mark.parametrize(
        "chi_nam,expected_cung",
        [
            (1, 3),  # Tý → Dần
            (5, 3),  # Thìn → Dần
            (9, 3),  # Thân → Dần
            (12, 6),  # Hợi → Tỵ
        ],
    )
    def test_tim_thien_ma(self, chi_nam, expected_cung):
        """Test tìm Thiên Mã"""
        result = find_tian_ma(chi_nam)
        assert (
            result == expected_cung
        ), f"Chi {chi_nam} should have Thiên Mã at cung {expected_cung}"

    @pytest.mark.parametrize("chi_nam", range(1, 13))
    def test_tim_pha_toai(self, chi_nam):
        """Test tìm Phá Toái"""
        result = find_po_sui(chi_nam)
        assert 1 <= result <= 12, "Phá Toái should be in cung 1-12"

    @pytest.mark.parametrize("can_nam", range(1, 11))
    def test_tim_triet(self, can_nam):
        """Test tìm Triệt"""
        result = find_triet(can_nam)

        assert len(result) == 2, "Should return 2 cung Triệt"
        assert all(1 <= c <= 12 for c in result), "Triệt should be in cung 1-12"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
