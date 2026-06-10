import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test __init__() method
# =============================================
class TestLittleHardHat(unittest.TestCase):

    def test_init__localhost_wrong_type(self):
        with self.assertRaises(TypeError):
            LittleHardHat(
                localhost=56169,
                timeout=2
            )

    def test_init__localhost_empty_string(self):
        with self.assertRaises(ValueError):
            LittleHardHat(
                localhost="",
                timeout=2
            )

    def test_init__localhost_whitespace(self):
        with self.assertRaises(ValueError):
            LittleHardHat(
                localhost="   ",
                timeout=2
            )

    def test_init__timeout_wrong_type(self):
        with self.assertRaises(TypeError):
            LittleHardHat(
                localhost="192.168.1.1",
                timeout="two"
            )

    def test_init__timeout_zero(self):
        with self.assertRaises(ValueError):
            LittleHardHat(
                localhost="192.168.1.1",
                timeout=0
            )

    def test_init__timeout_negative(self):
        with self.assertRaises(ValueError):
            LittleHardHat(
                localhost="192.168.1.1",
                timeout=-1
            )