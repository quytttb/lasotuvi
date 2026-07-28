"""
Test suite for DiaBan module - Địa bàn calculations
"""

import pytest

from lasotuvi.earth_plate import EarthPlate, Palace, apply_star_miao_wang


class TestCungDiaBan:
    """Test cung địa bàn basic functionality"""

    @pytest.mark.parametrize("cung_id", range(1, 13))
    def test_cung_creation(self, cung_id):
        """Test tạo cung địa bàn"""
        cung = Palace(cung_id)

        assert cung.index == cung_id
        assert cung.palace_element in ["Thủy", "Thổ", "Mộc", "Hỏa", "Kim"]
        assert cung.stars == []
        assert cung.yin_yang in [1, -1]
        assert cung.branch_name in [
            "Tý",
            "Sửu",
            "Dần",
            "Mão",
            "Thìn",
            "Tỵ",
            "Ngọ",
            "Mùi",
            "Thân",
            "Dậu",
            "Tuất",
            "Hợi",
        ]

    def test_cung_am_duong(self):
        """Test âm dương của cung"""
        # Cung lẻ là Dương (+1)
        cung1 = Palace(1)  # Tý
        assert cung1.yin_yang == 1

        # Cung chẵn là Âm (-1)
        cung2 = Palace(2)  # Sửu
        assert cung2.yin_yang == -1

    def test_them_sao(self):
        """Test thêm sao vào cung"""
        from lasotuvi.stars import ZI_WEI

        cung = Palace(7)  # Ngọ
        cung.add_star(ZI_WEI)

        assert len(cung.stars) == 1
        assert cung.stars[0]["name"] == "Tử vi"


class TestDiaBan:
    """Test địa bàn calculations"""

    @pytest.mark.parametrize(
        "thang,gio",
        [
            (1, 1),  # Tháng Giêng, giờ Tý
            (6, 7),  # Tháng 6, giờ Ngọ
            (12, 12),  # Tháng Chạp, giờ Hợi
        ],
    )
    def test_dia_ban_creation(self, thang, gio):
        """Test tạo địa bàn"""
        db = EarthPlate(thang, gio)

        assert db.lunar_birth_month == thang
        assert db.lunar_birth_hour == gio
        assert len(db.palaces) == 13  # Index 0-12, ignore 0
        assert hasattr(db, "life_palace")
        assert hasattr(db, "body_palace")

    def test_cung_menh_calculation(self):
        """Test tính cung Mệnh"""
        # Tháng 8, giờ Tý (1)
        db = EarthPlate(8, 1)

        # Cung Mệnh phải nằm trong khoảng 1-12
        assert 1 <= db.life_palace <= 12

        # Kiểm tra cung Mệnh có tên đúng không
        cung_menh = db.palaces[db.life_palace]
        assert cung_menh.palace_name == "Mệnh"

    def test_12_cung_names(self):
        """Test 12 cung có tên đầy đủ"""
        db = EarthPlate(6, 1)

        expected_names = [
            "Mệnh",
            "Phụ mẫu",
            "Phúc đức",
            "Điền trạch",
            "Quan lộc",
            "Nô bộc",
            "Thiên di",
            "Tật Ách",
            "Tài Bạch",
            "Tử tức",
            "Phu thê",
            "Huynh đệ",
        ]

        found_names = []
        for i in range(1, 13):
            if hasattr(db.palaces[i], "palace_name"):
                found_names.append(db.palaces[i].palace_name)

        # Tất cả 12 tên cung phải có
        for name in expected_names:
            assert name in found_names, f"Missing cung: {name}"

    @pytest.mark.parametrize(
        "cuc,gioi_tinh",
        [
            (2, 1),  # Thủy nhị, Nam
            (3, -1),  # Mộc tam, Nữ
            (6, 1),  # Hỏa lục, Nam
        ],
    )
    def test_nhap_dai_han(self, cuc, gioi_tinh):
        """Test nhập đại hạn"""
        db = EarthPlate(8, 1)
        am_duong_cung = 1  # Giả sử cung là dương

        db = db.assign_da_xian(cuc, gioi_tinh * am_duong_cung)

        # Kiểm tra mỗi cung có đại hạn
        for i in range(1, 13):
            assert hasattr(db.palaces[i], "da_xian_age")
            assert isinstance(db.palaces[i].da_xian_age, int)
            assert db.palaces[i].da_xian_age > 0

    @pytest.mark.parametrize(
        "chi_nam,gioi_tinh",
        [
            (1, 1),  # Tý, Nam
            (7, -1),  # Ngọ, Nữ
            (12, 1),  # Hợi, Nam
        ],
    )
    def test_nhap_tieu_han(self, chi_nam, gioi_tinh):
        """Test nhập tiểu hạn"""
        db = EarthPlate(8, 1)
        db = db.assign_xiao_xian(db.life_palace, gioi_tinh, chi_nam)

        # Kiểm tra mỗi cung có tiểu hạn
        for i in range(1, 13):
            assert hasattr(db.palaces[i], "xiao_xian_branch")


class TestDacTinhSao:
    """Test đặc tính sao (Vượng, Miếu, Đắc, Bình, Hãm)"""

    def test_dac_tinh_sao_exists(self):
        """Test hàm apply_star_miao_wang tồn tại và hoạt động"""
        from lasotuvi.stars import Star, ZI_WEI

        # Tạo bản sao sao Tử Vi để test
        sao_test = Star(ZI_WEI.star_id, ZI_WEI.name, ZI_WEI.element)

        # Tử Vi ở cung Tý (1)
        apply_star_miao_wang(1, sao_test)

        # Kiểm tra sao có thuộc tính miao_wang
        assert hasattr(sao_test, "miao_wang")

    @pytest.mark.parametrize("cung_so", range(1, 13))
    def test_dac_tinh_all_cungs(self, cung_so):
        """Test đặc tính sao ở tất cả 12 cung"""
        from lasotuvi.stars import Star, ZI_WEI

        # Tạo bản sao sao Tử Vi để test
        sao_test = Star(ZI_WEI.star_id, ZI_WEI.name, ZI_WEI.element)

        apply_star_miao_wang(cung_so, sao_test)

        # Kiểm tra có thuộc tính miao_wang
        assert hasattr(sao_test, "miao_wang")


class TestIntegration:
    """Integration tests for DiaBan module"""

    def test_full_dia_ban_setup(self):
        """Test thiết lập địa bàn đầy đủ"""
        from lasotuvi.chart_builder import build_earth_plate

        # Ngày sinh: 15/8/1990, giờ Tý, Nam
        db = build_earth_plate(15, 8, 1990, 1, 1, True, 7)

        # Kiểm tra địa bàn đã setup đầy đủ
        assert db is not None
        assert len(db.palaces) == 13

        # Kiểm tra có sao trong các cung
        total_sao = sum(len(db.palaces[i].stars) for i in range(1, 13))
        assert total_sao > 0, "Should have stars in cungs"

    @pytest.mark.parametrize(
        "birth_data",
        [
            (15, 8, 1990, 1, 1),  # Dương nam
            (1, 1, 2000, 7, -1),  # Dương nữ
            (25, 6, 1990, 1, 1),  # Âm nam (convert từ 15/8/1990)
        ],
    )
    def test_various_birth_dates(self, birth_data):
        """Test với nhiều ngày sinh khác nhau"""
        from lasotuvi.chart_builder import build_earth_plate

        dd, mm, yy, gio, gioi_tinh = birth_data
        db = build_earth_plate(dd, mm, yy, gio, gioi_tinh, True, 7)

        assert db is not None
        assert 1 <= db.life_palace <= 12
        assert 1 <= db.body_palace <= 12


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
