import unittest

import pytest

from lasotuvi.chart_builder import build_earth_plate
from lasotuvi.heaven_plate import HeavenPlate


@pytest.mark.thienban
class TestThienBan(unittest.TestCase):
    def test_thienban_initializable(self):
        plate = build_earth_plate(24, 10, 1991, 7, 1, True, 7)
        heaven = HeavenPlate(24, 10, 1991, 7, 1, "asdf", plate)
        assert heaven is not None
        assert heaven.bureau_name
        assert heaven.life_master
