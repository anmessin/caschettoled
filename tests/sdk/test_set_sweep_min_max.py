import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test set_sweep_min() method.
# =============================================
class TestSetSweepMin(unittest.TestCase):
    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)
                                   
    def test_set_sweep_min__sweep_min_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_sweep_min(
                sweep_min="cinquecento"
            )

    def test_set_sweep_min__sweep_min_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep_min(
                sweep_min=-1
            )

    def test_set_sweep_min__sweep_min_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep_min(
                sweep_min=4096
            )
            
# =============================================
# Test set_sweep_max() method.
# =============================================
class TestSetSweepMax(unittest.TestCase):
    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)
                                   
    def test_set_sweep_max__sweep_max_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_sweep_max(
                sweep_max="cinquecento"
            )

    def test_set_sweep_max__sweep_max_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep_max(
                sweep_max=-1
            )

    def test_set_sweep_max__sweep_max_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep_max(
                sweep_max=4096
            )