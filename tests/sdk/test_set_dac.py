import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test set_dac() method.
# =============================================
class TestSetDac(unittest.TestCase):
    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)
                                   
    def test_set_dac__channel_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_dac(
                channel="uno",
                dac_value=1000
            )

    def test_set_dac__dac_value_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_dac(
                channel=1,
                dac_value=1000.0
            )

    def test_set_dac__channel_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_dac(
                channel=0,
                dac_value=1000
            )

    def test_set_dac__channel_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_dac(
                channel=20,
                dac_value=1000
            )

    def test_set_dac__dac_value_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_dac(
                channel=1,
                dac_value=-1
            )

    def test_set_dac__dac_value_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_dac(
                channel=1,
                dac_value=4096
            )