import unittest

import pytest

from lasotuvi.earth_plate import EarthPlate


@pytest.mark.diaban
class TestDiaBan(unittest.TestCase):
    def test_diaban_is_initializable(self):
        diaban = EarthPlate(1, 10)
        if diaban:
            self.assertTrue(diaban)
