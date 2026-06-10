import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test set_frequency() method.
# =============================================
class TestSetFrequency(unittest.TestCase):
    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)
                                   
    def test_set_frequency__frequency_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_frequency(
                frequency="cinque mila"
            )

    def test_set_frequency__frequency_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_frequency(
                frequency=999
            )

    def test_set_frequency__frequency_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_frequency(
                frequency=10001
            )