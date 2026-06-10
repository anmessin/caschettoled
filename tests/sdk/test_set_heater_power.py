import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test set_heater_power() method.
# =============================================
class TestSetHeaterPower(unittest.TestCase):
    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)
                                   
    def test_set_heater_power__heaterpower_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_heater_power(
                heaterpower="5"
            )

    def test_set_heater_power__heaterpower_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_heater_power(
                heaterpower=-1
            )

    def test_set_heater_power__heaterpower_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_heater_power(
                heaterpower=4096
            )