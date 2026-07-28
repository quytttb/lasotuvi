"""
Conftest for pytest - shared fixtures and configuration
"""


import pytest
from faker import Faker


@pytest.fixture
def faker_vi():
    """Faker với locale Việt Nam"""
    return Faker(["vi_VN"])


@pytest.fixture
def sample_birth_date():
    """Ngày sinh mẫu cho testing"""
    return {
        "ngay": 15,
        "thang": 8,
        "nam": 1990,
        "gio": 1,  # Giờ Tý
        "gioi_tinh": 1,  # Nam
        "duong_lich": True,
        "time_zone": 7,
    }


@pytest.fixture
def known_test_cases():
    """Các test cases đã biết kết quả chính xác"""
    return [
        {
            "input": {"ngay": 15, "thang": 8, "nam": 1990, "duong_lich": True},
            "expected_lunar": {"ngay": 25, "thang": 6, "nam": 1990, "nhuan": False},
            "description": "Ngày thường năm 1990",
        },
        {
            "input": {"ngay": 29, "thang": 1, "nam": 2025, "duong_lich": True},
            "expected_lunar": {"ngay": 30, "thang": 12, "nam": 2024, "nhuan": False},
            "description": "Tết Nguyên Đán 2025",
        },
        {
            "input": {"ngay": 1, "thang": 1, "nam": 2000, "duong_lich": True},
            "expected_lunar": {"ngay": 25, "thang": 11, "nam": 1999, "nhuan": False},
            "description": "Thiên niên kỷ",
        },
    ]
