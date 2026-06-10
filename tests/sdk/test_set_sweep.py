import unittest
from littlehardhat import LittleHardHat, LittleHardHatError

# test_<funzione>__<condizione>

# =============================================
# Test set_sweep() method.
# =============================================
class TestSetSweep(unittest.TestCase):
    def setUp(self):
        self.board = LittleHardHat("192.168.1.1", 2)
                                   
    # --- Test wrong type ---
    def test_set_sweep__channel_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_sweep(
                channel="uno",
                mode="off"
            )

    def test_set_sweep__mode_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_sweep(
                channel=1,
                mode=[]
            )

    def test_set_sweep__NumberOfStep_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_sweep(
                channel=1,
                mode="on",
                NumberOfStep="cento",
                TimeForStep=100
            )

    def test_set_sweep__TimeForStep_wrong_type(self):
        with self.assertRaises(TypeError):
            self.board.set_sweep(
                channel=1,
                mode="on",
                NumberOfStep=100,
                TimeForStep="cento"
            )

    # --- Test wrong value ---
    def test_set_sweep__channel_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=0,
                mode="off"
            )

    def test_set_sweep__channel_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=20,
                mode="off"
            )

    def test_set_sweep__mode_wrong_value(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=0,
                mode="spento",
                NumberOfStep=100,
                TimeForStep=100
            )

    def test_set_sweep__NumberOfStep_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="on",
                NumberOfStep=0,
                TimeForStep=100
            )

    def test_set_sweep__NumberOfStep_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="on",
                NumberOfStep=255,
                TimeForStep=100
            )

    def test_set_sweep__TimeForStep_below_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="on",
                NumberOfStep=100,
                TimeForStep=9
            )

    def test_set_sweep__TimeForStep_above_range(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="on",
                NumberOfStep=9,
                TimeForStep=10001
            )

    # --- Test params combinations ---
    # --- mode: 'off' ---
    def test_set_sweep__mode_off_with_all_params(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="off",
                NumberOfStep=100,
                TimeForStep=100
            )

    def test_set_sweep__mode_off_with_only_number_of_step(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="off",
                NumberOfStep=100
            )

    def test_set_sweep__mode_off_with_only_time_for_step(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="off",
                TimeForStep=100
            )

    # --- mode: 'on' ---
    def test_set_sweep__mode_on_without_all_params(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="on"
            )

    def test_set_sweep__mode_on_with_only_number_of_step(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="on",
                NumberOfStep=100
            )

    def test_set_sweep__mode_on_with_only_time_for_step(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="on",
                TimeForStep=100
            )

    # --- mode: 'loop' ---
    def test_set_sweep__mode_loop_without_all_params(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="loop"
            )

    def test_set_sweep__mode_loop_with_only_number_of_step(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="loop",
                NumberOfStep=100
            )

    def test_set_sweep__mode_loop_with_only_time_for_step(self):
        with self.assertRaises(LittleHardHatError):
            self.board.set_sweep(
                channel=1,
                mode="loop",
                TimeForStep=100
            )