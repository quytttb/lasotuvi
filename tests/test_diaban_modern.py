"""
Test suite for DiaBan module - Địa bàn calculations
"""

import pytest

from lasotuvi.DiaBan import cungDiaBan, dacTinhSao, diaBan


class TestCungDiaBan:
    """Test cung địa bàn basic functionality"""

    @pytest.mark.parametrize("cung_id", range(1, 13))
    def test_cung_creation(self, cung_id):
        """Test tạo cung địa bàn"""
        cung = cungDiaBan(cung_id)

        assert cung.cungSo == cung_id
        assert cung.hanhCung in ["Thủy", "Thổ", "Mộc", "Hỏa", "Kim"]
        assert cung.cungSao == []
        assert cung.cungAmDuong in [1, -1]
        assert cung.cungTen in [
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
        cung1 = cungDiaBan(1)  # Tý
        assert cung1.cungAmDuong == 1

        # Cung chẵn là Âm (-1)
        cung2 = cungDiaBan(2)  # Sửu
        assert cung2.cungAmDuong == -1

    def test_them_sao(self):
        """Test thêm sao vào cung"""
        from lasotuvi.Sao import saoTuVi

        cung = cungDiaBan(7)  # Ngọ
        cung.themSao(saoTuVi)

        assert len(cung.cungSao) == 1
        assert cung.cungSao[0]["saoTen"] == "Tử vi"


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
        db = diaBan(thang, gio)

        assert db.thangSinhAmLich == thang
        assert db.gioSinhAmLich == gio
        assert len(db.thapNhiCung) == 13  # Index 0-12, ignore 0
        assert hasattr(db, "cungMenh")
        assert hasattr(db, "cungThan")

    def test_cung_menh_calculation(self):
        """Test tính cung Mệnh"""
        # Tháng 8, giờ Tý (1)
        db = diaBan(8, 1)

        # Cung Mệnh phải nằm trong khoảng 1-12
        assert 1 <= db.cungMenh <= 12

        # Kiểm tra cung Mệnh có tên đúng không
        cung_menh = db.thapNhiCung[db.cungMenh]
        assert cung_menh.cungChu == "Mệnh"

    def test_12_cung_names(self):
        """Test 12 cung có tên đầy đủ"""
        db = diaBan(6, 1)

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
            if hasattr(db.thapNhiCung[i], "cungChu"):
                found_names.append(db.thapNhiCung[i].cungChu)

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
        db = diaBan(8, 1)
        am_duong_cung = 1  # Giả sử cung là dương

        db = db.nhapDaiHan(cuc, gioi_tinh * am_duong_cung)

        # Kiểm tra mỗi cung có đại hạn
        for i in range(1, 13):
            assert hasattr(db.thapNhiCung[i], "cungDaiHan")
            assert isinstance(db.thapNhiCung[i].cungDaiHan, int)
            assert db.thapNhiCung[i].cungDaiHan > 0

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
        db = diaBan(8, 1)
        db = db.nhapTieuHan(db.cungMenh, gioi_tinh, chi_nam)

        # Kiểm tra mỗi cung có tiểu hạn
        for i in range(1, 13):
            assert hasattr(db.thapNhiCung[i], "cungTieuHan")


class TestDacTinhSao:
    """Test đặc tính sao (Vượng, Miếu, Đắc, Bình, Hãm)"""

    def test_dac_tinh_sao_exists(self):
        """Test hàm dacTinhSao tồn tại và hoạt động"""
        from lasotuvi.Sao import Sao, saoTuVi

        # Tạo bản sao sao Tử Vi để test
        sao_test = Sao(saoTuVi.saoID, saoTuVi.saoTen, saoTuVi.saoNguHanh)

        # Tử Vi ở cung Tý (1)
        dacTinhSao(1, sao_test)

        # Kiểm tra sao có thuộc tính saoDacTinh
        assert hasattr(sao_test, "saoDacTinh")

    @pytest.mark.parametrize("cung_so", range(1, 13))
    def test_dac_tinh_all_cungs(self, cung_so):
        """Test đặc tính sao ở tất cả 12 cung"""
        from lasotuvi.Sao import Sao, saoTuVi

        # Tạo bản sao sao Tử Vi để test
        sao_test = Sao(saoTuVi.saoID, saoTuVi.saoTen, saoTuVi.saoNguHanh)

        dacTinhSao(cung_so, sao_test)

        # Kiểm tra có thuộc tính saoDacTinh
        assert hasattr(sao_test, "saoDacTinh")


class TestIntegration:
    """Integration tests for DiaBan module"""

    def test_full_dia_ban_setup(self):
        """Test thiết lập địa bàn đầy đủ"""
        from lasotuvi.App import lapDiaBan

        # Ngày sinh: 15/8/1990, giờ Tý, Nam
        db = lapDiaBan(diaBan, 15, 8, 1990, 1, 1, True, 7)

        # Kiểm tra địa bàn đã setup đầy đủ
        assert db is not None
        assert len(db.thapNhiCung) == 13

        # Kiểm tra có sao trong các cung
        total_sao = sum(len(db.thapNhiCung[i].cungSao) for i in range(1, 13))
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
        from lasotuvi.App import lapDiaBan

        dd, mm, yy, gio, gioi_tinh = birth_data
        db = lapDiaBan(diaBan, dd, mm, yy, gio, gioi_tinh, True, 7)

        assert db is not None
        assert 1 <= db.cungMenh <= 12
        assert 1 <= db.cungThan <= 12


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
