import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test _get() method.
# =============================================
class TestGet(unittest.TestCase):

    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)

    def test_get__params_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board._get(
                params="hello"
            )