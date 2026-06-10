import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test set_temperature() method.
# =============================================
class TestSetTemperature(unittest.TestCase):
    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)
                                   
    def test_set_temperature__temperature_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_temperature(
                temperature="uno"
            )

    def test_set_temperature__temperature_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_temperature(
                temperature=24
            )

    def test_set_temperature__temperature_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_temperature(
                temperature=80.1
            )