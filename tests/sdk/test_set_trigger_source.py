import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test set_trigger_source() method.
# =============================================
class TestSetTriggerSource(unittest.TestCase):
    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)
                                   
    def test_set_trigger_source__source_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_trigger_source(
                source=10
            )

    def test_set_trigger_source__source_wrong_value(self):
        with self.assertRaises(ValueError):
            self.board.set_trigger_source(
                source="interno"
            )