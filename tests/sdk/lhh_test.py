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

if __name__ == "__main__":
    unittest.main()